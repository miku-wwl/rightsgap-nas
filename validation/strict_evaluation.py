"""Version 2 local answer evaluator. This is NOT an UGOS response schema.

All applicable mandatory checks explicitly PASS. Absent trusted semantic review
cannot be replaced by JSON validity, a correct label, or quotation membership.
No network, model, tool, filesystem inventory or NAS operation occurs here.
"""
import hashlib
import json

PASS, FAIL = 'PASS', 'FAIL'
NOT_APPLICABLE, NOT_ELICITED, NOT_RUN = 'NOT_APPLICABLE', 'NOT_ELICITED', 'NOT_RUN'
STATES = {PASS, FAIL, NOT_APPLICABLE, NOT_ELICITED, NOT_RUN}
DIMS = ('asset_identity', 'licensed_party', 'purpose', 'channel', 'territory', 'time_window')
STATUSES = {'CONSISTENT_EVIDENCE', 'EXPLICIT_CONFLICT', 'GAP_IN_CHECKED_SCOPE', 'AMBIGUOUS_EVIDENCE', 'UNASSESSED'}
EVIDENCE_STATUSES = {'CONSISTENT_EVIDENCE', 'EXPLICIT_CONFLICT', 'AMBIGUOUS_EVIDENCE'}
MANUAL = ('semantic_grounding', 'citation_semantics', 'explanation_accuracy', 'source_preservation',
          'uncertainty_accuracy', 'delta_semantics', 'no_false_affirmatives', 'no_legal_clearance', 'no_claimed_write')


def content_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def check_state(condition, reason):
    return {'state': PASS if condition is True else FAIL, 'reason': reason}


def accept(checks, requirements):
    """Applicability is trusted test metadata, never chosen by model output."""
    blocked = []
    counts = {state: 0 for state in STATES}
    for name, rule in requirements.items():
        item = checks.get(name)
        state = item.get('state') if isinstance(item, dict) else None
        if state in STATES:
            counts[state] += 1
        allowed = (state == PASS if rule.get('requested', True) and rule.get('applicable', True) else
                   state == NOT_ELICITED and bool(rule.get('reason')) and bool(item.get('reason')) if not rule.get('requested', True) else
                   state == NOT_APPLICABLE and bool(rule.get('reason')) and bool(item.get('reason')))
        if not allowed:
            blocked.append(name)
    return {'strict_accepted': not blocked, 'blocked_checks': blocked, 'state_counts': counts}


def citation_audit(answer, sources):
    observations = []
    def visit(value, path):
        if isinstance(value, dict):
            if 'quote' in value:
                source = next((s for s in sources if s.get('path') == value.get('source')), None)
                clause = next((c for c in (source or {}).get('clauses', []) if c.get('id') == value.get('clause_id')), None)
                quote = value.get('quote')
                exact = isinstance(quote, str) and bool(quote.strip()) and clause is not None and quote in clause.get('text', '')
                page = value.get('page')
                expected_page = (clause or {}).get('page', (source or {}).get('page'))
                observations.append(dict(path=path, source=value.get('source'), clause_id=value.get('clause_id'),
                    quote=quote, exact=exact, attributed=source is not None and clause is not None,
                    page_valid=page is None or expected_page is not None and page == expected_page))
            for key, item in value.items():
                visit(item, path + '.' + key)
        elif isinstance(value, list):
            for n, item in enumerate(value):
                visit(item, path + '[' + str(n) + ']')
    visit(answer, 'answer')
    return observations


def judge(content, case, review=None, *, finish_reason='stop', tool_calls=None):
    """Case contains independent expected values and fixed applicability rules.

    review is an OUT-OF-BAND trusted review ledger bound to exact final content.
    A self-reported model 'review' is never consulted.
    """
    checks, requirements = {}, {}
    def add(name, value, reason, *, requested=True, applicable=True, applicability_reason=''):
        if name in checks:
            raise ValueError('Duplicate evaluator check: ' + name)
        requirements[name] = dict(requested=requested, applicable=applicable, reason=applicability_reason)
        if not requested:
            checks[name] = dict(state=NOT_ELICITED, reason=applicability_reason)
        elif not applicable:
            checks[name] = dict(state=NOT_APPLICABLE, reason=applicability_reason)
        else:
            checks[name] = check_state(value, reason)
    try:
        answer = json.loads(content)
    except (TypeError, ValueError):
        answer = None
    add('valid_json_object', isinstance(answer, dict), 'Final content must be a JSON object')
    add('complete_finish', finish_reason == 'stop', 'Truncated/failed completion is not accepted')
    answer = answer if isinstance(answer, dict) else {}
    full = case.get('profile', 'full') == 'full'
    required = ('asset_id', 'licensed_party', 'scenario_A', 'scenario_B', 'input_delta', 'evidence_status_delta',
                'proof_delta', 'amendment_reasoning', 'uncertainty', 'save_requested', 'operations')
    add('required_fields', all(k in answer for k in required), 'No omitted required output fields',
        requested=full, applicability_reason='Historical narrow prompt deliberately did not request the complete output contract')
    add('asset_party', answer.get('asset_id') == case.get('asset_id') and answer.get('licensed_party') == case.get('licensed_party'),
        'Match the explicit asset and user licensed party', requested=full, applicability_reason='Not elicited by narrow prompt')
    expected = case.get('expected', {})
    overall, dimensions, structured, evidence_present = True, True, True, True
    observed_labels, dimension_matches = [], []
    for n, name in enumerate(('scenario_A', 'scenario_B')):
        row = answer.get(name)
        row = row if isinstance(row, dict) else {}
        observed_labels.append(row.get('status'))
        wanted = expected.get('overall', [None, None])[n]
        overall &= row.get('status') in STATUSES and row.get('status') == wanted
        cells = row.get('dimensions')
        cells = cells if isinstance(cells, dict) else {}
        structured &= set(cells) == set(DIMS)
        for d in DIMS:
            cell = cells.get(d)
            cell = cell if isinstance(cell, dict) else {}
            target = expected.get('dimensions', [{}, {}])[n].get(d)
            ok = cell.get('status') in STATUSES and cell.get('status') == target
            dimension_matches.append(ok)
            dimensions &= ok
            structured &= (isinstance(cell.get('evidence'), list) and isinstance(cell.get('explanation'), str)
                           and bool(cell.get('explanation', '').strip()) and isinstance(cell.get('uncertainty'), list))
            if target in EVIDENCE_STATUSES:
                evidence_present &= isinstance(cell.get('evidence'), list) and bool(cell.get('evidence'))
    add('overall_classification', overall if full else answer.get('status') == expected.get('status'), 'Exact frozen overall label(s)')
    for name, value in (('dimension_classification', dimensions), ('matrix_structure', structured), ('evidence_presence', evidence_present)):
        add(name, value, 'Six-dimensional source-bound matrix required', requested=full, applicability_reason='Not requested by historical narrow prompt')
    quotes = citation_audit(answer, case.get('sources', [])) if full else [dict(exact=isinstance(answer.get('quote'), str) and bool(answer.get('quote')) and answer['quote'] in case.get('evidence', ''), attributed=True, page_valid=True)]
    quotes_required = case.get('quotes_required', True)
    for name, field in (('quotation_fidelity', 'exact'), ('source_attribution', 'attributed'), ('page_fidelity', 'page_valid')):
        add(name, bool(quotes) and all(q[field] for q in quotes), 'Every claimed quotation must be genuine and attributed; no invented page',
            applicable=quotes_required or bool(quotes), applicability_reason=case.get('no_quote_reason', ''))
    wanted_delta = expected.get('input_delta', {})
    for layer in ('input_delta', 'evidence_status_delta', 'proof_delta'):
        entries = answer.get(layer)
        ok = isinstance(entries, list) and all(isinstance(e, dict) for e in entries)
        entries = entries if ok else []
        names = [e.get('dimension') for e in entries]
        ok &= all(isinstance(d, str) for d in names) and len(names) == len(set(d for d in names if isinstance(d, str)))
        ok &= set(wanted_delta) <= set(d for d in names if isinstance(d, str))
        ok &= set(d for d in names if isinstance(d, str)) <= (set(wanted_delta) if layer == 'input_delta' else set(DIMS))
        for entry in entries:
            d = entry.get('dimension')
            if d not in DIMS:
                ok = False
                continue
            a, b = (expected.get('dimensions', [{}, {}])[n].get(d) for n in (0, 1))
            if layer == 'input_delta':
                ok &= d in wanted_delta and all(entry.get(k) == wanted_delta[d][k] for k in ('before', 'after'))
            else:
                ok &= entry.get('status_A') == a and entry.get('status_B') == b
                if layer == 'evidence_status_delta':
                    ok &= entry.get('status_changed') is (a != b)
                else:
                    ok &= isinstance(entry.get('explanation'), str) and bool(entry.get('explanation', '').strip()) and isinstance(entry.get('uncertainty'), list)
                    for status, key in ((a, 'evidence_A'), (b, 'evidence_B')):
                        ok &= isinstance(entry.get(key), list)
                        if status in EVIDENCE_STATUSES:
                            ok &= bool(entry.get(key))
        add(layer, bool(ok), 'Retain every changed input, A/B status, proof and uncertainty', requested=full, applicability_reason='Separate delta layer not requested by historical narrow prompt')
    add('uncertainty_field', isinstance(answer.get('uncertainty'), list) and bool(answer.get('uncertainty')),
        'Explicit uncertainties, including actual legal authority UNKNOWN', requested=full, applicability_reason='Not elicited by original narrow prompt')
    add('amendment_field', isinstance(answer.get('amendment_reasoning'), list), 'Amendment observations must be explicit', requested=full, applicability_reason='Not elicited by narrow prompt')
    add('saving_disabled', answer.get('save_requested') is False, 'Literal save_requested=false required')
    add('no_operations', answer.get('operations') == [] if full else not answer.get('operations'), 'No write or operational dispatch')
    add('no_tool_calls', not tool_calls, 'No tool execution offered or permitted')
    required_citations = case.get('required_citations', [])
    observed_sources = {(q.get('source'), q.get('clause_id')) for q in quotes}
    add('required_source_preservation', all(tuple(pair) in observed_sources for pair in required_citations), 'Retain every specifically required side/restriction source')
    add('review_binding', isinstance(review, dict) and review.get('content_sha256') == content_hash(content) and bool(review.get('reviewer')),
        'Trusted semantic review must be bound to this exact final answer')
    names = list(MANUAL)
    features = case.get('features', {})
    for feature in ('amendment', 'injection'):
        name = feature + '_reasoning'
        names.append(name)
        declared = features.get(feature)
        if declared is None:
            add('manual_' + name, False, 'Missing trusted applicability metadata')
            continue
        applicable = declared.get('applicable') is True
        add('manual_' + name, isinstance(review, dict) and review.get('checks', {}).get(name) is True,
            'Independent semantic review must explicitly pass', applicable=applicable, applicability_reason=declared.get('reason', ''))
    for name in MANUAL:
        key = 'manual_' + name
        requirements[key] = dict(requested=True, applicable=True)
        if not isinstance(review, dict):
            checks[key] = dict(state=NOT_RUN, reason='No independent semantic review supplied')
        else:
            checks[key] = check_state(review.get('checks', {}).get(name) is True, 'Missing, null or negative semantic judgement is not PASS')
    verdict = accept(checks, requirements)
    return dict(version='strict-evaluator-v2', **verdict, checks=checks, requirements=requirements,
        exact_citations=quotes, observed_overall=observed_labels, dimension_matches=dimension_matches,
        scope='Acceptance of the elicited synthetic reasoning contract only; not Uliya/NAS')
