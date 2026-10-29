"""Supervised source-by-source SIMULATED_EXPERT_RESULTS workflow.

No filesystem discovery, delegate dispatch, model API, or NAS operation. Inputs
are explicit frozen business observations, NOT claimed UGOS return schemas.
"""
import copy
import hashlib
from pathlib import PurePosixPath

from delegation_context import command_for
from reference_policy import assess, compare, valid_path, interpretation_key, DIMENSIONS, INPUT_KEYS, UNASSESSED, AMBIGUOUS, GAP, CONFLICT

LAYER = 'SIMULATED_EXPERT_RESULTS'


def body_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def context_for(case, selected, upstream):
    return {'authorized_roots': case['authorized_roots'], 'asset_paths': list(case['assets'].values()),
        'document_paths': selected, 'asset_identities': case['assets'], 'licensed_party': case['licensed_party'],
        'scenario_A': case['scenarios'][0], 'scenario_B': case['scenarios'][1],
        'associations': {a: [p for p in paths if p in selected] for a, paths in case['associations'].items()},
        'upstream_results': upstream, 'scope_boundaries': {'max_assets': 8, 'max_documents': 6, 'depth': 2, 'no_external_paths': True}}


def empty_rows(case, reason, status=UNASSESSED):
    rows = {}
    for asset in case['assets']:
        r = assess(asset, case['scenarios'][0], None)
        r.update(status=status, reason=reason)
        rows[asset] = [copy.deepcopy(r), copy.deepcopy(r)]
    return rows


def run_workflow(case):
    if case.get('layer') != LAYER:
        raise ValueError('Only explicitly simulated frozen inputs are accepted')
    selected = case['selected_documents']
    roots = case['authorized_roots']
    transcript, issues, examined, valid_docs = [], [], [], []
    report = {'layer': LAYER, 'id': case.get('id'), 'operations': [], 'actual_expert_calls': 0,
        'scope_receipt': {'authorized_roots': roots, 'selected_assets': case['assets'], 'selected_documents': selected,
            'licensed_party': case['licensed_party'], 'scenarios': case['scenarios'], 'source_revision': case['source_revision'],
            'examined_documents': examined, 'denied': [], 'missing': [], 'truncated': [], 'errors': issues,
            'coverage_complete': False, 'coverage_basis': 'Only the explicitly supplied selected synthetic result set; no actual folder or NAS coverage claim'},
        'transcript': transcript, 'source_ledger': [], 'assessments': {}, 'deltas': {}, 'repair_questions': [],
        'source_fingerprints': {}, 'completion_status': 'PARTIAL', 'saving': 'DISABLED',
        'runtime': {'ULIYA_RUNTIME_STATUS': 'NOT_RUN', 'NAS_RUNTIME_STATUS': 'NOT_RUN'}}
    inputs_ok = bool(case['assets']) and bool(case['licensed_party']) and len(case['scenarios']) == 2
    inputs_ok &= all(all(s.get(key) for key in ('purpose', 'channel', 'territory', 'date', 'licensee')) and s['licensee'] == case['licensed_party'] for s in case['scenarios'])
    inputs_ok &= len(case['assets']) <= 8 and len(selected) <= 6 and len(selected) == len(set(selected))
    if case.get('mode') == 'initial':
        inputs_ok &= 5 <= len(case['assets']) <= 8 and 3 <= len(selected) <= 6
    paths = list(case['assets'].values()) + selected
    inputs_ok &= all(valid_path(path, roots) for path in paths)
    if not inputs_ok:
        issues.append('Missing, malformed, over-bound or out-of-root authorized input')
        report['assessments'] = empty_rows(case, issues[-1])
        return finalize(report, case)
    transcript.append({'layer': LAYER, 'target': 'file-agent', 'request_paths': paths,
        'authoring_command_not_dispatched': command_for('file-agent', context_for(case, selected, {'user_authorized_scope_only': True}))})
    inventory = case.get('inventory', {})
    returned = inventory.get('paths', [])
    inventory_ok = inventory.get('state') == 'completed' and inventory.get('complete') is True
    inventory_ok &= len(returned) == len(set(returned)) and set(returned) == set(paths)
    inventory_ok &= all(valid_path(inventory.get('resolved_paths', {}).get(p), roots) for p in paths)
    transcript[-1]['simulated_response'] = copy.deepcopy(inventory)
    if not inventory_ok:
        issues.append('Inventory incomplete, denied, unknown, outside scope or not the exact selected set; dependent reads stopped')
        report['assessments'] = empty_rows(case, issues[-1])
        return finalize(report, case)
    coverage = True
    source_results = case.get('document_results', [])
    for n, path in enumerate(selected):
        event = {'layer': LAYER, 'target': 'document-agent', 'request_paths': [path],
            'authoring_command_not_dispatched': command_for('document-agent', context_for(case, [path], {
                'verified_mock_inventory': inventory, 'requested_exact_path': path,
                'prior_document_observations': [{'path': d['path'], 'state': d['state']} for d in valid_docs]}))}
        transcript.append(event)
        observed = copy.deepcopy(source_results[n]) if n < len(source_results) else {'state': 'missing'}
        event['simulated_response'] = observed
        state = observed.get('state')
        if observed.get('denied'):
            report['scope_receipt']['denied'].append(path)
        if state == 'missing':
            report['scope_receipt']['missing'].append(path)
        if observed.get('truncated'):
            report['scope_receipt']['truncated'].append(path)
        usable = (state == 'completed' and observed.get('path') == path and observed.get('coverage_complete') is True
                  and not observed.get('denied') and not observed.get('truncated')
                  and isinstance(observed.get('id'), str) and bool(observed.get('id'))
                  and isinstance(observed.get('findings'), list) and all(isinstance(f, dict) for f in observed.get('findings', []))
                  and isinstance(observed.get('text'), str) and isinstance(observed.get('context'), str)
                  and observed['text'] in observed['context'])
        if not usable:
            coverage = False
            issues.append('Unusable source response for ' + path + ': ' + str(state) + '; no source rehydration or fallback')
            if state in ('failed', 'cancelled', 'waiting_user', 'waiting_approval'):
                break
            continue
        examined.append(path)
        valid_docs.append(observed)
        report['source_fingerprints'][path] = {'revision': observed.get('revision'), 'supplied_text_sha256': body_hash(observed['text']),
            'basis': 'Local fingerprint of supplied simulated text only, not file-agent SHA-256 or NAS identity'}
        for finding in observed.get('findings', []):
            report['source_ledger'].append({'source': path, 'document_id': observed['id'], 'clause_id': finding.get('clause_id'),
                'quote': finding.get('quote'), 'context': observed['context'], 'asset': finding.get('asset'),
                'kind': finding.get('kind'), 'conditions': finding.get('conditions', {}), 'terms': finding.get('terms', {}),
                'prohibits': finding.get('prohibits', {}), 'documentary_applicability': 'ASSUMED curated synthetic premise',
                'unknown': ['Real legal authenticity/enforceability', 'Actual Expert Agent return fidelity'],
                'source_quote_membership': isinstance(finding.get('quote'), str) and finding['quote'] in observed['context'],
                'semantic_review_available': interpretation_key(observed, finding) in case['trusted_reviews']})
    coverage &= len(examined) == len(selected)
    report['scope_receipt']['coverage_complete'] = bool(coverage)
    if not case.get('association_established'):
        issues.append('Document may affect multiple assets; association is unresolved and no narrow positive scope is inferred')
    for asset in case['assets']:
        rows, delta = compare(asset, case['scenarios'], valid_docs, coverage=bool(coverage), reviews=case['trusted_reviews'],
            mapping=case.get('association_established') is True, expected_sources=selected, source_roots=roots)
        report['assessments'][asset] = rows
        report['deltas'][asset] = delta
    return finalize(report, case)


def finalize(report, case):
    for asset, rows in report['assessments'].items():
        for n, row in enumerate(rows):
            for dimension, cell in row['dimensions'].items():
                status = cell['status']
                if status == 'CONSISTENT_EVIDENCE':
                    continue
                scenario = case['scenarios'][n]
                key = INPUT_KEYS.get(dimension)
                wanted = scenario.get(key) if key else asset if dimension == 'asset_identity' else case['licensed_party']
                if row['status'] == AMBIGUOUS and not case.get('association_established'):
                    question = f'Which selected source and exact asset identifier establish the association for {asset}? Resolve the potentially cross-asset document before comparison.'
                elif status == UNASSESSED:
                    question = f'Restore complete authorized source/context for {asset} {dimension} before assessing {wanted}; which selected document can supply it?'
                elif status == CONFLICT:
                    question = f'For {asset} and {case["licensed_party"]}, is there an explicit authorized clause amending the cited {dimension} contradiction for {wanted}? Preserve independent restrictions.'
                elif status == GAP:
                    question = f'Which source expressly grants {case["licensed_party"]} the {dimension} value {wanted} for {asset}? Provide its path and exact clause; the checked-scope gap is not permission.'
                else:
                    question = f'For {asset} {dimension}, which actual clause or authority basis resolves the cited documentary ambiguity for {wanted}?'
                report['repair_questions'].append({'asset': asset, 'scenario': 'A' if n == 0 else 'B', 'dimension': dimension, 'status': status, 'question': question})
    if report['scope_receipt']['coverage_complete'] and case.get('association_established') and not any(
            r['status'] == UNASSESSED for rows in report['assessments'].values() for r in rows):
        report['completion_status'] = 'COMPLETED_BOUNDED_EVIDENCE_REPORT'
    report['limitations'] = ['SIMULATED_EXPERT_RESULTS only; commands were never dispatched.',
        'Source texts, completeness and semantic annotations are curated fixtures, not retrieved facts.',
        'Source quote membership is necessary, not an arbitrary-language semantic verifier.',
        'Actual model routing, OCR, path confinement, permissions and Uliya/NAS execution UNKNOWN/NOT_RUN.',
        'No legal clearance or publishing decision; saving DISABLED.']
    return report


def recheck(case, previous):
    update = case.get('update') or {}
    affected = update.get('affected_assets', [])
    stopped = {'layer': LAYER, 'overall_statuses': [UNASSESSED, UNASSESSED], 'operations': [], 'completion_status': 'BLOCKED',
               'previous_revision': previous['scope_receipt']['source_revision'], 'previous_results_historical_only': True}
    if not update.get('authorized') or update.get('base_revision') != previous['scope_receipt']['source_revision'] or not affected or not set(affected) <= set(case['assets']):
        return dict(stopped, reason='Missing explicit affected scope or evidence-update authorization')
    if update.get('changed_original'):
        changed = update['changed_original']
        fingerprint = previous['source_fingerprints'].get(changed['path'])
        if not fingerprint or fingerprint['revision'] != changed.get('revision') or fingerprint['supplied_text_sha256'] != body_hash(changed['text']):
            return dict(stopped, reason='Original source revision drift; fresh bounded read required, no stale positive carried forward')
    old = [d for d in case['document_results'] if any(f.get('asset') in affected for f in d.get('findings', []))]
    new = update.get('new_documents', [])
    if not new or any(not valid_path(d.get('path'), case['authorized_roots']) for d in new):
        return dict(stopped, reason='New document absent or outside authorized roots')
    focused = copy.deepcopy(case)
    focused.update(mode='recheck', assets={a: case['assets'][a] for a in affected}, source_revision='r2',
        selected_documents=[d['path'] for d in old + new], document_results=copy.deepcopy(old + new))
    focused['associations'] = {a: focused['selected_documents'] for a in affected}
    paths = list(focused['assets'].values()) + focused['selected_documents']
    focused['inventory'] = {'state': 'completed', 'complete': True, 'paths': paths, 'resolved_paths': {p: p for p in paths}}
    current = run_workflow(focused)
    current['evidence_update_authorization'] = {'authorized': True, 'affected_assets': affected, 'new_sources': [d['path'] for d in new],
        'previous_revision': previous['scope_receipt']['source_revision'], 'new_revision': 'r2'}
    current['overall_statuses'] = [r['status'] for r in current['assessments'][affected[0]]]
    current['evidence_revision_changes'] = {a: {'previous': [r['status'] for r in previous['assessments'][a]],
        'current': [r['status'] for r in current['assessments'][a]], 'basis': 'Actual supplied new clauses and explicit scoped amendment edges'} for a in affected}
    current['unaffected_rows'] = {'assets': [a for a in case['assets'] if a not in affected],
        'receipt_revision': previous['scope_receipt']['source_revision'], 'freshly_reassessed': False}
    return current


def render_report(report, update=None):
    receipt = report['scope_receipt']
    lines = ['# RightsGap supervised example report', '', '**SIMULATED_EXPERT_RESULTS — Uliya/NAS NOT_RUN.**', '',
        f'Completion: {report["completion_status"]}. Saving: DISABLED. Licensed party: {receipt["licensed_party"]}. Revision: {receipt["source_revision"]}.',
        '', '## Scope receipt', '', f'Authorized roots: {receipt["authorized_roots"]}.',
        f'Selected assets: {len(receipt["selected_assets"])}. Selected documents: {len(receipt["selected_documents"])}. Actually examined in this simulation: {len(receipt["examined_documents"])}.',
        f'Complete selected supplied scope: {receipt["coverage_complete"]}. Denied: {receipt["denied"]}. Missing: {receipt["missing"]}. Truncated: {receipt["truncated"]}.',
        '', '## Overall asset results', '', '| Asset | A | B |', '| --- | --- | --- |']
    lines += [f'| {a} | {rows[0]["status"]} | {rows[1]["status"]} |' for a, rows in report['assessments'].items()]
    lines += ['', '## Six-dimensional matrix', '', '| Asset | Dimension | A | B | Actual supplied source clauses |', '| --- | --- | --- | --- | --- |']
    def escaped(text):
        return str(text).replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ')
    for asset, rows in report['assessments'].items():
        for dim in DIMENSIONS:
            cites = { (c['source'], c['quote']) for row in rows for c in row['dimensions'][dim].get('citations', []) if c['active'] }
            proof = '; '.join(escaped(p) + ': “' + escaped(q) + '”' for p, q in sorted(cites)) or 'No usable source support; see repair question.'
            lines.append(f'| {asset} | {dim} | {rows[0]["dimensions"][dim]["status"]} | {rows[1]["dimensions"][dim]["status"]} | {proof} |')
    lines += ['', '## Three-layer Scenario Delta', '']
    for asset, delta in report['deltas'].items():
        lines += [f'### {asset}', '', '| Changed input | A → B | Evidence A → B | Proof / uncertainty |', '| --- | --- | --- | --- |']
        for item in delta['input_delta']:
            dim = item['dimension']
            status = next(s for s in delta['evidence_status_delta'] if s['dimension'] == dim)
            proof = next(s for s in delta['proof_delta'] if s['dimension'] == dim)
            paths = sorted({c['source'] for c in proof['sources_A'] + proof['sources_B']})
            lines.append(f'| {dim} | {escaped(item["before"])} → {escaped(item["after"])} | {status["before"]} → {status["after"]} | {escaped(proof["explanation"])} Sources: {escaped(paths)}. {escaped(proof["uncertainty"])} |')
        lines.append('')
    lines += ['## Evidence repair questions', '']
    lines += ['- ' + escaped(q['question']) for q in report['repair_questions']]
    if update:
        lines += ['', '## Explicitly authorized evidence recheck', '',
            'Affected A001 only; original unrelated rows retain their r1 receipt and are not claimed freshly assessed.',
            'Observed outcome A/B: ' + escaped(update['overall_statuses']) + '.',
            'Source revision r2 uses only original L1 and supplied L7. Its exact amendment citations remain in the machine report.']
    lines += ['', '## Limits', ''] + ['- ' + text for text in report['limitations']]
    return '\n'.join(lines) + '\n'
