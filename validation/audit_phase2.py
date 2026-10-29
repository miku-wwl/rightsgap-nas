"""Credential-free Phase 2 evidence audit. No API, NAS or paid requests."""
import hashlib
import json
from pathlib import Path

from strict_evaluation import content_hash, judge

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'validation/results/phase2'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = []
    def check(identifier, condition, detail=''):
        if identifier in {c['id'] for c in checks}:
            raise ValueError('Duplicate audit identifier')
        checks.append(dict(id=identifier, state='PASS' if condition is True else 'FAIL', detail=detail))
    p13 = ROOT / 'validation/results/phase1-3'
    check('phase13_mandatory_gates', load(p13 / 'gates.json')['status'] == 'PASS')
    check('phase13_gated_sources_unchanged', all(sha(ROOT / p) == h for p, h in load(p13 / 'passed-source-hashes.json').items()))
    fixtures = ROOT / 'validation/fixtures/phase2'
    check('workflow_expectations_frozen', sha(fixtures / 'workflows-v1.json') == load(fixtures / 'freeze.json')['input_and_expectations_sha256'])
    workflow = load(OUT / 'workflow-tests.json')
    rows = workflow['assertions']
    check('workflow_assertion_statistics', workflow['checks'] == dict(total=len(rows), passed=sum(r['passed'] for r in rows), failed=sum(not r['passed'] for r in rows), unique_ids=len({r['id'] for r in rows})))
    check('all_workflows_and_controls_pass', workflow['workflow_cases'] == workflow['workflow_passed'] == 22 and workflow['checks']['failed'] == 0 and workflow['mutation_properties'] == workflow['scope_state_controls'] == 7)
    ids = [r['id'] for r in rows]
    for name, key in (('regression', 'check_details'), ('hardening', 'assertions'), ('targeted-tests', 'assertions')):
        ids += [r.get('id', r.get('name')) for r in load(p13 / (name + '.json'))[key]]
    check('all_deterministic_assertion_ids_unique', len(ids) == len(set(ids)), str(len(ids)) + ' assertions, not independent real-world observations')
    check('simulation_provenance_and_zero_operations', all(r['report']['layer'] == 'SIMULATED_EXPERT_RESULTS' and r['operation_attempts'] == 0 and r['report']['actual_expert_calls'] == 0 and not r['report']['operations'] for r in workflow['workflows'].values()))
    check('one_document_per_simulated_request', all(len(t['request_paths']) == 1 for r in workflow['workflows'].values() for t in r['report']['transcript'] if t['target'] == 'document-agent'))
    static, execution = load(OUT / 'official-static.json'), load(OUT / 'official-static-execution.json')
    check('phase2_actual_official_static_check', execution['exit_code'] == 0 and static['status'] == 'static-pass' and static['summary']['errors'] == static['summary']['warnings'] == 0)
    check('exact_current_static_skill_files', all(sha(ROOT / 'rightsgap-media-reuse' / f['path']) == f['sha256'] for f in static['files']))
    freeze = load(OUT / 'llm-freeze.json')
    check('frozen_llm_inputs_and_rubric_unchanged', all(sha(OUT / p) == h for p, h in freeze['hashes'].items()) and sha(ROOT / 'validation/run_phase2_llm.py') == freeze['runner_sha256'] and sha(ROOT / 'validation/strict_evaluation.py') == freeze['strict_evaluator_sha256'])
    raw_freeze = load(OUT / 'llm-observation-freeze.json')
    check('raw_model_observations_unchanged', all(sha(OUT / p) == h for p, h in raw_freeze['hashes'].items()))
    raw = load(OUT / 'llm-results.json')['responses']
    plan = load(OUT / 'llm-plan.json')['requests']
    cases = load(OUT / 'llm-cases.json')['cases']
    reviews = load(OUT / 'llm-semantic-review.json')['reviews']
    scored = load(OUT / 'llm-review.json')
    check('unique_fixed_model_observations', len({r['id'] for r in raw}) == len(raw) and {r['id'] for r in raw} <= {c['id'] for c in cases} and len(raw) <= 12)
    check('synthetic_no_tools_no_answer_leakage', all('tools' not in p['payload'] and 'expected' not in json.dumps(p['payload']) and json.loads(p['payload']['messages'][1]['content'])['synthetic_only'] is True for p in plan))
    repeated = []
    for result in raw:
        if result['api_status'] != 'SUCCESS':
            continue
        identifier = result['id']
        case = next(c for c in cases if c['id'] == identifier)
        choice = result['raw_response']['choices'][0]
        content = choice['message']['content']
        review = reviews.get(identifier)
        verdict = judge(content, case, review, finish_reason=choice.get('finish_reason'), tool_calls=choice['message'].get('tool_calls'))
        stored = next(r for r in scored['observations'] if r['id'] == identifier)
        repeated.append(verdict == stored['verdict'] and review.get('content_sha256') == content_hash(content))
    check('strict_scoring_and_review_bindings_reproduce', len(repeated) == scored['summary']['executed_observations'] and all(repeated))
    check('rejections_remain_unaccepted', all(r['strict_accepted'] is (not bool(r['verdict']['blocked_checks'])) for r in scored['observations'] if r['state'] != 'NOT_RUN'), 'PARTIAL external reasoning is not turned into PASS')
    cost = load(OUT / 'llm-cost.json')
    attempts = load(OUT / 'llm-execution.json')['attempts']
    units = lambda u: (u.get('prompt_cache_hit_tokens', 0) * .006 + u.get('prompt_cache_miss_tokens', u['prompt_tokens'] - u.get('prompt_cache_hit_tokens', 0)) * .3 + u['completion_tokens'] * 1.2) / 1_000_000
    known = sum(units(a['usage']) for a in attempts if a.get('usage'))
    check('requests_usage_and_budget_reconcile', len(attempts) == cost['calls_attempted'] <= 12 and abs(known - cost['known_peak_estimate_usd']) < 1e-12 and cost['budget_accounted_usd'] <= .50 and sum(a.get('usage', {}).get('total_tokens', 0) for a in attempts) == cost['reported_usage']['total_tokens'])
    readme = (ROOT / 'PHASE13_PHASE2_REVIEW.md').read_text(encoding='utf-8')
    reports = [(ROOT / ('docs/' + p)).read_text(encoding='utf-8') for p in ('14-phase1-3-hardening-report.md', '15-phase2-supervised-workflow-report.md', '16-nas-runtime-validation-runbook.md')]
    check('reports_separate_runtime_and_result_layers', all('NOT_RUN' in r for r in reports) and 'SIMULATED_EXPERT_RESULTS' in readme and 'PARTIAL' in reports[1] and str(workflow['checks']['total']) + '/' + str(workflow['checks']['total']) in reports[1])
    result = dict(layer='PHASE2 ORDINARY OFFLINE AUDIT; NO CREDENTIALS/API/NAS', status='PASS' if all(c['state'] == 'PASS' for c in checks) else 'FAIL',
        checks=checks, passed=sum(c['state'] == 'PASS' for c in checks), total=len(checks), globally_unique_deterministic_assertions=len(ids),
        limits=['Semantic agent reviews are read, hash-bound and rerun through the rubric, not independently rejudged by this audit', 'Recorded official check is verified against exact candidate hashes; no NAS execution'])
    (OUT / 'audit.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
