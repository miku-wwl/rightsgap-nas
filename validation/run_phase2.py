"""Frozen end-to-end simulated workflow and failure-monotonicity tests."""
import copy
import hashlib
import json
from pathlib import Path

from clause_fixtures import review_ledger
from delegation_context import decode
from reference_policy import POSITIVE, UNASSESSED, DIMENSIONS
from workflow_simulation import run_workflow, recheck, render_report

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results/phase2'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    gates = json.loads((ROOT / 'results/phase1-3/gates.json').read_text(encoding='utf-8'))
    if gates['status'] != 'PASS' or not gates['phase2_start_authorized']:
        raise SystemExit('Phase 1.3 mandatory gate did not authorize Phase 2')
    for path, wanted in json.loads((ROOT / 'results/phase1-3/passed-source-hashes.json').read_text(encoding='utf-8')).items():
        if hashlib.sha256((ROOT.parent / path).read_bytes()).hexdigest() != wanted:
            raise SystemExit('Gated implementation changed; revalidate Phase 1.3 before continuing')
    frozen = ROOT / 'fixtures/phase2/workflows-v1.json'
    receipt = json.loads((frozen.parent / 'freeze.json').read_text(encoding='utf-8'))
    if hashlib.sha256(frozen.read_bytes()).hexdigest() != receipt['input_and_expectations_sha256']:
        raise SystemExit('Frozen workflow inputs or expected results changed')
    cases = json.loads(frozen.read_text(encoding='utf-8'))['cases']
    checks, ids, results, mutation_results = [], set(), {}, {}
    def check(name, actual, wanted=True):
        if name in ids:
            raise ValueError('Duplicate workflow assertion: ' + name)
        ids.add(name)
        checks.append(dict(id=name, passed=actual == wanted,
            actual=sorted(actual) if isinstance(actual, set) else actual,
            expected=sorted(wanted) if isinstance(wanted, set) else wanted))
    for case in cases:
        report = run_workflow(case)
        expected = case['expected']
        focus = expected['focus_asset']
        statuses = [r['status'] for r in report['assessments'][focus]]
        prefix = 'workflow/' + case['id']
        check(prefix + '/focused_statuses', statuses, expected['statuses'])
        check(prefix + '/no_operational_side_effect', report['operations'], [])
        check(prefix + '/no_actual_expert_calls', report['actual_expert_calls'], 0)
        check(prefix + '/scope_receipt_exact_selected_set', report['scope_receipt']['selected_documents'], case['selected_documents'])
        check(prefix + '/one_document_per_request', all(len(e['request_paths']) == 1 for e in report['transcript'] if e['target'] == 'document-agent'))
        for event in report['transcript']:
            target, context = decode(event['authoring_command_not_dispatched'])
            check(prefix + '/self_contained/' + str(len([c for c in checks if c['id'].startswith(prefix + '/self_contained/')])),
                target == event['target'] and context['licensed_party'] == case['licensed_party'] and context['scenario_A'] == case['scenarios'][0] and context['scenario_B'] == case['scenarios'][1])
        actual_sources = {d['path']: d for d in case['document_results']}
        citations = [c for rows in report['assessments'].values() for row in rows for c in row['citations']]
        quote_ok = all(c['source'] in actual_sources and c['quote'] in actual_sources[c['source']].get('context', '') for c in citations)
        check(prefix + '/no_fabricated_source_quote', quote_ok)
        supported = [cell for rows in report['assessments'].values() for row in rows for cell in row['dimensions'].values() if cell['status'] == POSITIVE]
        check(prefix + '/every_positive_cell_has_active_reviewed_support', all(bool(cell.get('support')) and all(c['active'] and c['review_basis'] for c in cell['support']) for cell in supported))
        if case['id'] == 'T12':
            a1, a2 = case['assets']['A001'], case['assets']['A002']
            check(prefix + '/same_basename_distinct_full_paths', a1 != a2 and a1.rsplit('/', 1)[-1] == a2.rsplit('/', 1)[-1])
            check(prefix + '/no_cross_asset_grant_reuse', all(c['source'] != case['associations']['A002'][0]
                for row in report['assessments']['A001'] for c in row['citations']))
        if case['id'] in ('T02', 'T03', 'T17', 'T18'):
            delta = report['deltas']['A002']
            for layer in ('input_delta', 'evidence_status_delta', 'proof_delta'):
                check(prefix + '/four_' + layer, {r['dimension'] for r in delta[layer]}, {'purpose', 'channel', 'territory', 'time_window'})
            check(prefix + '/unchanged_positive_proof', all(r['status_A'] == r['status_B'] == POSITIVE and r['sources_A'] and r['sources_B'] for r in delta['proof_delta']))
        update = None
        if expected['recheck'] is not None:
            update = recheck(case, report)
            check(prefix + '/recheck_B', update['overall_statuses'][1], expected['recheck'])
            check(prefix + '/update_no_operations', update['operations'], [])
            if case['id'] != 'T20':
                check(prefix + '/bounded_affected_recheck', len(update['scope_receipt']['selected_assets']) == 1 and len(update['scope_receipt']['selected_documents']) == 2)
                check(prefix + '/unaffected_receipt_not_refreshed', update['unaffected_rows']['receipt_revision'] == 'r1' and update['unaffected_rows']['freshly_reassessed'] is False)
            if case['id'] == 'T14':
                check(prefix + '/independent_R1_preserved', any(c['clause_id'] == 'R1' and c['active'] for c in update['assessments']['A001'][1]['dimensions']['channel']['conflicts']))
            elif case['id'] == 'T16':
                row = update['assessments']['A001'][1]
                check(prefix + '/purpose_only_replacement', row['dimensions']['purpose']['status'], POSITIVE)
                check(prefix + '/other_three_restrictions_survive', [row['dimensions'][d]['status'] for d in ('channel', 'territory', 'time_window')], ['EXPLICIT_CONFLICT'] * 3)
            elif case['id'] == 'T20':
                check(prefix + '/stale_positives_blocked', update['completion_status'] == 'BLOCKED' and update['previous_results_historical_only'] is True)
        check(prefix + '/repair_questions_present_when_unresolved', not report['repair_questions'] if all(r['status'] == POSITIVE for rows in report['assessments'].values() for r in rows) else bool(report['repair_questions']))
        case_checks = [c for c in checks if c['id'].startswith(prefix + '/')]
        results[case['id']] = dict(description=case['description'], expected_behavior=expected, actual_statuses=statuses,
            source_association=case['associations'], quote_fidelity='PASS' if citations and quote_ok else 'NOT_APPLICABLE' if not citations else 'FAIL',
            quote_occurrences=len(citations), scope_correct=report['scope_receipt']['selected_documents'] == case['selected_documents'],
            fail_closed=all(a != POSITIVE for a, e in zip(statuses, expected['statuses']) if e != POSITIVE),
            operation_attempts=0, verdict='PASS' if all(c['passed'] for c in case_checks) else 'FAIL',
            report=report, recheck=update)
    normal = cases[1]
    rank = {'UNASSESSED': 0, 'AMBIGUOUS_EVIDENCE': 1, 'EXPLICIT_CONFLICT': 2, 'GAP_IN_CHECKED_SCOPE': 3, POSITIVE: 4}
    for name in ('remove_evidence', 'lose_coverage', 'summary_replacement', 'remove_restriction', 'change_asset', 'change_party', 'add_unresolved_conflict'):
        c = copy.deepcopy(next(x for x in cases if x['id'] == 'T14') if name == 'remove_restriction' else normal)
        focus, baseline_status = 'A002', POSITIVE
        d = c['document_results'][1]
        if name == 'remove_evidence':
            d['text'] = d['text'].replace(d['findings'][0]['quote'], '')
            d['context'] = d['text']
        elif name == 'lose_coverage':
            d['coverage_complete'] = False
        elif name == 'summary_replacement':
            d.update(text='Unsupported favorable summary.', context=None, findings=[])
        elif name == 'remove_restriction':
            d = c['document_results'][0]
            d['findings'] = [f for f in d['findings'] if f['clause_id'] != 'R1']
            focus, baseline_status = 'A001', 'EXPLICIT_CONFLICT'
        elif name == 'change_asset':
            c['assets']['A099'] = c['assets'].pop('A002')
            c['associations']['A099'] = c['associations'].pop('A002')
            focus = 'A099'
        elif name == 'change_party':
            c['licensed_party'] = 'StudioC'
            for s in c['scenarios']: s['licensee'] = 'StudioC'
        elif name == 'add_unresolved_conflict':
            old = c['document_results'][2]['path']
            q = 'A002 is licensed to StudioA for editorial purpose only; paid commercial advertising is explicitly excluded. Its priority relative to L2 is unresolved.'
            extra = {'id': 'UNRESOLVED', 'path': 'synthetic/licenses/competing_A002.pdf', 'text': q, 'context': q,
                'state': 'completed', 'coverage_complete': True, 'revision': 'r2',
                'findings': [{'asset': 'A002', 'clause_id': 'C1', 'kind': 'GRANT', 'quote': q,
                    'terms': {'asset_identity': ['A002'], 'licensed_party': ['StudioA'], 'purpose': ['editorial']}, 'exclusive': ['purpose']}]}
            c['document_results'][2] = extra
            c['selected_documents'][2] = extra['path']
            c['inventory']['paths'] = [extra['path'] if p == old else p for p in c['inventory']['paths']]
            c['inventory']['resolved_paths'].pop(old)
            c['inventory']['resolved_paths'][extra['path']] = extra['path']
            c['trusted_reviews'].update(review_ledger([extra]))
        report = run_workflow(c)
        update = recheck(c, report) if name == 'remove_restriction' else None
        actual = update['overall_statuses'][1] if update else report['assessments'][focus][1]['status']
        check('monotonic/' + name, rank[actual] <= rank[baseline_status] and actual != POSITIVE)
        mutation_results[name] = dict(baseline_status=baseline_status, mutated_status=actual, nonfavorable=rank[actual] <= rank[baseline_status], operations=report['operations'])
    scope_controls = {}
    for name in ('failed', 'cancelled', 'waiting_user', 'waiting_approval', 'unknown', 'out_of_root', 'unauthorized_update'):
        c = copy.deepcopy(normal)
        if name == 'out_of_root':
            c['inventory']['resolved_paths'][c['selected_documents'][0]] = 'outside/other-share.pdf'
        elif name == 'unauthorized_update':
            c['update']['authorized'] = False
        else:
            c['document_results'][0]['state'] = name
        r = run_workflow(c)
        if name == 'unauthorized_update':
            observed = recheck(c, r)['overall_statuses']
        else:
            observed = [row['status'] for row in r['assessments']['A002']]
        check('scope-state/' + name, observed, [UNASSESSED, UNASSESSED])
        check('scope-state/' + name + '/zero_operations', r['operations'], [])
        scope_controls[name] = dict(statuses=observed, simulated_reads=len(r['transcript']), operations=r['operations'])
    OUT.mkdir(parents=True, exist_ok=True)
    example = results['T04']
    (OUT / 'example-report.md').write_text(render_report(example['report'], example['recheck']), encoding='utf-8', newline='\n')
    output = dict(layer='SIMULATED_EXPERT_RESULTS; ACTUAL ULIYA/NAS NOT_RUN', fixture_sha256=receipt['input_and_expectations_sha256'],
        workflow_cases=len(results), workflow_passed=sum(r['verdict'] == 'PASS' for r in results.values()),
        mutation_properties=len(mutation_results), scope_state_controls=len(scope_controls),
        checks={'total': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks), 'unique_ids': len(ids)},
        workflows=results, failure_monotonicity=mutation_results, scope_state_controls_results=scope_controls,
        assertions=checks, failures=[c for c in checks if not c['passed']],
        limitations=['Ordering is the conservative evidence-status precedence, not a legal risk score.',
            'Mutations apply to known curated clauses/coverage and a trusted review ledger; arbitrary unseen text omissions remain UNKNOWN.',
            'Command strings were constructed and parsed locally, never dispatched.'])
    save(OUT / 'workflow-tests.json', output)
    print(json.dumps({k: output[k] for k in ('workflow_cases', 'workflow_passed', 'mutation_properties', 'scope_state_controls', 'checks', 'failures')}, indent=2))
    raise SystemExit(1 if output['failures'] else 0)


if __name__ == '__main__':
    main()
