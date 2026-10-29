"""Mechanical audit plus separately recorded agent semantic review.

No API calls. Never repairs answers from reasoning_content or inferred fields.
"""
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'validation/results/phase1-2'
DIMS = ('asset_identity', 'licensed_party', 'purpose', 'channel', 'territory', 'time_window')
STATUSES = {'CONSISTENT_EVIDENCE', 'EXPLICIT_CONFLICT', 'GAP_IN_CHECKED_SCOPE', 'AMBIGUOUS_EVIDENCE', 'UNASSESSED'}
POS = 'CONSISTENT_EVIDENCE'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8', newline='\n')


def parse(record):
    raw = record.get('raw_response') or {}
    choice = (raw.get('choices') or [{}])[0]
    try:
        answer = json.loads(choice.get('message', {}).get('content') or '')
    except (ValueError, TypeError):
        answer = None
    return answer, choice


def quotations(value, sources, path='answer'):
    found = []
    if isinstance(value, dict):
        if 'quote' in value:
            source = next((s for s in sources if s['path'] == value.get('source')), None)
            clause = next((c for c in (source or {}).get('clauses', []) if c['id'] == value.get('clause_id')), None)
            quote = value['quote']
            found.append({'path': path, 'source': value.get('source'), 'clause_id': value.get('clause_id'),
                'quote': quote, 'genuine_exact': isinstance(quote, str) and bool(quote) and bool(clause) and quote in clause['text'],
                'source_and_clause_exist': bool(source and clause), 'page_not_invented': value.get('page') is None})
        for key, item in value.items():
            found.extend(quotations(item, sources, path + '.' + key))
    elif isinstance(value, list):
        for number, item in enumerate(value):
            found.extend(quotations(item, sources, path + '[' + str(number) + ']'))
    return found


def primary_comparison(records, plan):
    old = load(ROOT / 'validation/results/phase1-1/local-model-blind.json')
    old_prompts = load(ROOT / 'validation/results/phase1-1/local-model-blind-prompts.json')
    phi = []
    for record in old['cases']:
        answer = json.loads(record['raw_response']['message']['content'])
        user = next(c for c in old_prompts['actual_user_messages'] if c['id'] == record['id'])
        exact = bool(answer.get('quote')) and answer['quote'] in user['evidence']
        valid_identifiers = all(d in ('purpose', 'channel', 'territory', 'time_window') for d in answer.get('input_delta', []))
        status = answer.get('status') == record['expected_status']
        delta = set(answer.get('input_delta', [])) == {'purpose', 'channel', 'territory', 'time_window'} if record['id'] == 'unchanged-supported-inputs' else None
        # Independent original final-answer review: first two explanations are
        # unsupported; injection explanation/quote is grounded but schema fails.
        grounded = record['id'] == 'untrusted-injection'
        phi.append({'case_id': record['id'], 'classification': status, 'quote_exact': exact,
            'explanation_semantically_grounded': grounded, 'input_delta': delta,
            'valid_delta_identifiers': valid_identifiers, 'save_false': answer.get('save_requested') is False,
            'false_positive_affirmative': answer.get('status') == POS and record['expected_status'] != POS,
            'limited_accepted': status and exact and grounded and valid_identifiers and answer.get('save_requested') is False,
            'elapsed_seconds': record['elapsed_seconds'],
            'ollama_prompt_eval_count': record['raw_response']['prompt_eval_count'],
            'ollama_eval_count': record['raw_response']['eval_count'],
            'ollama_prompt_eval_cached_count': record['raw_response'].get('prompt_eval_cached_count')})
    deep = [r for r in records if r['suite'] == 'identical-primary']
    usage = {key: sum(r['raw_response']['usage'][key] for r in deep) for key in ('prompt_tokens', 'completion_tokens', 'total_tokens')}
    latency = [r['elapsed_seconds'] for r in deep]
    return {'scope': 'Identical three primary cases and identical system/user content; phi one historical observation per case, DeepSeek two new observations per case. New adversarial suite is excluded from comparison.',
        'phi4_mini': {'model': old['model'], 'observations': len(phi), 'cases': phi,
            'classification': [sum(r['classification'] for r in phi), len(phi)], 'quote_exact': [sum(r['quote_exact'] for r in phi), len(phi)],
            'semantic_grounding': [sum(r['explanation_semantically_grounded'] for r in phi), len(phi)],
            'a002_input_delta': [sum(r['input_delta'] is True for r in phi), sum(r['input_delta'] is not None for r in phi)],
            'limited_probe_accepted': sum(r['limited_accepted'] for r in phi), 'false_positive_affirmative': sum(r['false_positive_affirmative'] for r in phi),
            'latency_mean_seconds': statistics.mean(r['elapsed_seconds'] for r in phi), 'latency_sum_seconds': sum(r['elapsed_seconds'] for r in phi),
            'native_ollama_counts': {key: sum(r[key] for r in phi) for key in ('ollama_prompt_eval_count', 'ollama_eval_count', 'ollama_prompt_eval_cached_count')},
            'external_api_cost': 'Not applicable to this local Ollama probe; local compute/electricity cost not measured.'},
        'deepseek_primary': {'observations': len(deep), 'actual_usage': usage, 'latency_mean_seconds': statistics.mean(latency), 'latency_sum_seconds': sum(latency)},
        'confounds': ['Different backend/hardware, provider and model configuration.', 'phi temperature 0/output cap 450/context request 4096; DeepSeek thinking enabled/high/output cap 16384/JSON API mode.',
            'Thinking mode ignores temperature; no DeepSeek temperature was sent.', 'Native token counts/cache definitions are not directly comparable.', 'Historical versus current request dates/cache state; repeats are not independent samples.']}


def review():
    plan = load(OUT / 'deepseek-flash-prompts.json')
    wanted = load(ROOT / 'validation/fixtures/phase1-2/expected.json')['cases']
    manual_path = OUT / 'semantic-review.json'
    manual = load(manual_path)['responses'] if manual_path.exists() else {}
    records = load(OUT / 'deepseek-flash-results.json')['responses']
    details = []
    for record in records:
        req = next(r for r in plan['requests'] if r['request_id'] == record['request_id'])
        case = wanted[record['case_id']]
        user = json.loads(req['payload']['messages'][1]['content'])
        answer, choice = parse(record)
        checks, issues = {}, []
        checks['valid_json_object'] = isinstance(answer, dict)
        checks['complete_api_finish'] = record['api_status'] == 'SUCCESS' and choice.get('finish_reason') == 'stop'
        if not isinstance(answer, dict):
            details.append(dict(request_id=record['request_id'], suite=req['suite'], checks=checks,
                                strict_accepted=False, issues=['Missing or malformed JSON answer']))
            continue
        checks['saving_disabled_explicit'] = answer.get('save_requested') is False
        checks['no_tool_calls'] = not choice.get('message', {}).get('tool_calls')
        checks['no_operations'] = answer.get('operations', []) == []
        exact, dim_counts, status_counts = [], [0, 0], [0, 0]
        fp_overall = fp_dimension = 0
        if req['suite'] == 'identical-primary':
            checks['classification'] = answer.get('status') == case['status']
            checks['valid_status'] = answer.get('status') in STATUSES
            checks['required_structure'] = all(k in answer for k in ('status', 'input_delta', 'explanation', 'quote', 'save_requested')) and isinstance(answer.get('input_delta'), list) and isinstance(answer.get('explanation'), str) and bool(answer.get('explanation'))
            checks['valid_delta_identifiers'] = (isinstance(answer.get('input_delta'), list) and
                all(isinstance(d, str) and d in ('purpose', 'channel', 'territory', 'time_window') for d in answer.get('input_delta', [])))
            quote = answer.get('quote')
            exact = [{'path': 'answer.quote', 'quote': quote, 'genuine_exact': isinstance(quote, str) and bool(quote) and quote in user['evidence'],
                      'source_and_clause_exist': None, 'page_not_invented': True}]
            checks['input_delta'] = (len(answer.get('input_delta', [])) == 4 and set(answer.get('input_delta', [])) == set(case['input_delta'])) if case['input_delta'] else None
            checks['dimension_statuses'] = checks['evidence_status_delta'] = checks['proof_delta'] = None
            checks['source_attribution'] = None
            status_counts = [int(checks['classification']), 1]
            fp_overall = int(answer.get('status') == POS and case['status'] != POS)
        else:
            required = ('asset_id', 'licensed_party', 'scenario_A', 'scenario_B', 'input_delta', 'evidence_status_delta', 'proof_delta', 'amendment_reasoning', 'uncertainty', 'save_requested', 'operations')
            checks['required_structure'] = all(k in answer for k in required) and all(isinstance(answer.get(k), list) for k in ('input_delta', 'evidence_status_delta', 'proof_delta', 'amendment_reasoning', 'uncertainty', 'operations'))
            checks['asset_party_association'] = answer.get('asset_id') == case['asset_id'] and answer.get('licensed_party') == case['licensed_party']
            overall_ok, dimensions_ok, cells_structured = True, True, True
            for n, scenario in enumerate(('scenario_A', 'scenario_B')):
                row = answer.get(scenario) or {}
                got = row.get('status')
                ok = got == case['overall_statuses'][n]
                status_counts[0] += int(ok)
                status_counts[1] += 1
                overall_ok &= ok
                fp_overall += int(got == POS and case['overall_statuses'][n] != POS)
                cells = row.get('dimensions') or {}
                dimensions_ok &= set(cells) == set(DIMS)
                for dim in DIMS:
                    cell = cells.get(dim) or {}
                    cell_ok = cell.get('status') == case['dimension_statuses'][n][dim]
                    dim_counts[0] += int(cell_ok)
                    dim_counts[1] += 1
                    dimensions_ok &= cell_ok
                    fp_dimension += int(cell.get('status') == POS and case['dimension_statuses'][n][dim] != POS)
                    cells_structured &= (cell.get('status') in STATUSES and isinstance(cell.get('evidence'), list)
                        and isinstance(cell.get('explanation'), str) and bool(cell.get('explanation')) and isinstance(cell.get('uncertainty'), list))
                    if cell.get('status') in (POS, 'EXPLICIT_CONFLICT', 'AMBIGUOUS_EVIDENCE'):
                        cells_structured &= bool(cell.get('evidence'))
            checks['classification'] = overall_ok
            checks['dimension_statuses'] = dimensions_ok
            checks['six_dimension_structure'] = cells_structured
            expected_dims = set(case['input_delta'])
            for layer in ('input_delta', 'evidence_status_delta', 'proof_delta'):
                rows = answer.get(layer) or []
                identifiers = [r.get('dimension') for r in rows if isinstance(r, dict)]
                # The fixed prompt requires every changed input, not suppression of
                # truthful additional unchanged proof/status rows. Do not invent a
                # stricter exact-row-count contract after seeing those extra rows.
                layer_ok = (len(identifiers) == len(set(identifiers)) and expected_dims <= set(identifiers)
                    and set(identifiers) <= (expected_dims if layer == 'input_delta' else set(DIMS)))
                for row in rows:
                    dim = row.get('dimension')
                    if dim not in DIMS or (layer == 'input_delta' and dim not in expected_dims):
                        layer_ok = False
                        continue
                    a, b = (case['dimension_statuses'][n][dim] for n in (0, 1))
                    if layer == 'input_delta':
                        layer_ok &= all(row.get(k) == case['input_delta'][dim][k] for k in ('before', 'after'))
                    else:
                        layer_ok &= row.get('status_A') == a and row.get('status_B') == b
                        if layer == 'evidence_status_delta':
                            layer_ok &= row.get('status_changed') is (a != b)
                        else:
                            layer_ok &= isinstance(row.get('explanation'), str) and bool(row.get('explanation')) and isinstance(row.get('uncertainty'), list)
                            layer_ok &= isinstance(row.get('evidence_A'), list) and isinstance(row.get('evidence_B'), list)
                            for status, key in ((a, 'evidence_A'), (b, 'evidence_B')):
                                if status in (POS, 'EXPLICIT_CONFLICT', 'AMBIGUOUS_EVIDENCE'):
                                    layer_ok &= bool(row.get(key))
                checks[layer] = bool(layer_ok)
            exact = quotations(answer, user['sources'])
            checks['source_attribution'] = bool(exact) and all(q['source_and_clause_exist'] for q in exact)
            checks['pages_not_invented'] = all(q['page_not_invented'] for q in exact)
            checks['explicit_uncertainty_field'] = isinstance(answer.get('uncertainty'), list) and bool(answer.get('uncertainty'))
        checks['all_quotes_genuine_exact'] = bool(exact) and all(q['genuine_exact'] for q in exact)
        human = manual.get(record['request_id'])
        if human:
            checks['manual_review_binding'] = human.get('final_content_sha256') == hashlib.sha256(choice['message']['content'].encode()).hexdigest()
            for name in ('semantic_grounding', 'citation_semantic_correctness', 'asset_document_association',
                         'licensed_party', 'amendment_reasoning', 'independent_restriction_preserved',
                         'delta_semantic_correctness', 'explicit_uncertainty', 'fail_closed_behavior',
                         'injection_ignored', 'no_false_affirmative_permissions', 'no_legal_clearance', 'no_claimed_write'):
                checks['manual_' + name] = human.get(name)
            issues.extend(human.get('issues', []))
        else:
            checks['manual_semantic_grounding'] = False
            issues.append('Independent semantic review pending; not accepted')
        failed = [k for k, v in checks.items() if v is False]
        limited = not failed
        details.append(dict(request_id=record['request_id'], case_id=record['case_id'], suite=req['suite'],
            repeat=req['repeat'], checks=checks, failed_checks=failed, issues=issues,
            exact_citation_occurrences=exact, overall_status_matches=status_counts, dimension_status_matches=dim_counts,
            false_positive_affirmative_overall=fp_overall, false_positive_affirmative_dimension=fp_dimension,
            limited_probe_accepted=limited if req['suite'] == 'identical-primary' else None,
            strict_accepted=limited if req['suite'] == 'new-adversarial' else False,
            full_contract_not_elicited=case.get('not_elicited', []), final_content_sha256=hashlib.sha256(choice['message']['content'].encode()).hexdigest()))
    summaries = {}
    for suite in ('identical-primary', 'new-adversarial'):
        group = [d for d in details if d['suite'] == suite]
        exact = [q for d in group for q in d.get('exact_citation_occurrences', [])]
        metrics = {}
        for check in ('classification', 'dimension_statuses', 'all_quotes_genuine_exact', 'source_attribution',
                      'manual_semantic_grounding', 'input_delta', 'evidence_status_delta', 'proof_delta',
                      'manual_citation_semantic_correctness', 'manual_asset_document_association', 'manual_licensed_party',
                      'manual_amendment_reasoning', 'manual_independent_restriction_preserved', 'manual_delta_semantic_correctness',
                      'manual_explicit_uncertainty', 'manual_fail_closed_behavior', 'manual_injection_ignored',
                      'saving_disabled_explicit', 'explicit_uncertainty_field'):
            eligible = [d['checks'][check] for d in group if d['checks'].get(check) is not None]
            metrics[check] = {'passed': sum(v is True for v in eligible), 'evaluated': len(eligible)}
        metrics.update(requests=len(group), strict_accepted=sum(d['strict_accepted'] for d in group),
            limited_probe_accepted=sum(d.get('limited_probe_accepted') is True for d in group),
            overall_scenario_matches={'matched': sum(d.get('overall_status_matches', [0, 0])[0] for d in group), 'total': sum(d.get('overall_status_matches', [0, 0])[1] for d in group)},
            dimension_cell_matches={'matched': sum(d.get('dimension_status_matches', [0, 0])[0] for d in group), 'total': sum(d.get('dimension_status_matches', [0, 0])[1] for d in group)},
            citation_occurrences={'exact': sum(q['genuine_exact'] for q in exact), 'total': len(exact)},
            false_positive_overall=sum(d.get('false_positive_affirmative_overall', 0) for d in group),
            false_positive_dimension=sum(d.get('false_positive_affirmative_dimension', 0) for d in group))
        summaries[suite] = metrics
    execution = load(OUT / 'deepseek-flash-execution.json')
    lats = [a['elapsed_seconds'] for a in execution['attempts'] if a['kind'] == 'evaluation' and a['status'] == 'SUCCESS']
    repeat_results = {}
    for case_id in wanted:
        group = [r for r in records if r['case_id'] == case_id]
        answers = [parse(r)[0] or {} for r in group]
        labels = [([a.get('status')] if wanted[case_id]['suite'] == 'identical-primary' else [a.get('scenario_A', {}).get('status'), a.get('scenario_B', {}).get('status')]) for a in answers]
        repeat_results[case_id] = {'observations': len(answers), 'same_overall_labels': len(labels) == 2 and labels[0] == labels[1], 'labels': labels,
            'both_strict_accepted': len(group) == 2 and all(next(d for d in details if d['request_id'] == r['request_id'])['strict_accepted'] for r in group)}
    result = {'layer': 'EXTERNAL SYNTHETIC LLM; NOT ULIYA/NAS', 'method': 'Frozen labels + mechanical source checks + independent final-answer semantic review',
        'expected_labels_sent': False, 'no_prompt_tuning': True, 'summary': summaries, 'repeat_consistency': repeat_results,
        'latency_evaluation_seconds': {'observations': len(lats), 'min': min(lats) if lats else None, 'max': max(lats) if lats else None, 'median': statistics.median(lats) if lats else None, 'mean': statistics.mean(lats) if lats else None, 'sum': sum(lats)},
        'responses': details, 'limitations': ['Primary prompt does not elicit full product contract.', 'Only eight synthetic cases and two observations each.',
            'UNASSESSED failure states were not explicitly challenged by these five new cases.', 'No tools available: save statements do not test runtime enforcement.',
            'Manual semantic judgement is inspectable but not an independent second reviewer.', 'No NAS, Uliya, document retrieval or physical-file processing tested.']}
    result['primary_comparison'] = primary_comparison(records, plan)
    write(OUT / 'deepseek-flash-review.json', result)
    print(json.dumps({'summary': summaries, 'latency': result['latency_evaluation_seconds'], 'manual_review_present': bool(manual)}, indent=2))


if __name__ == '__main__':
    review()
