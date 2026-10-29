"""Read-only evaluation evidence checks; no paid/API/NAS operations.

Runs the previously verified unchanged official static checker, preserving all
historical results and all submitted Skill bytes.
"""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from run_deepseek_flash import ROOT, OUT, EXPECTED, verify_freeze, ceiling
from review_deepseek_flash import quotations


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = []
    seen = set()
    # Materialize the audit receipt before checking the report's self-link.
    # An interrupted run remains visibly IN_PROGRESS, never a stale PASS.
    (OUT / 'local-evaluation-checks.json').write_text('{"status":"IN_PROGRESS"}\n', encoding='utf-8')

    def check(name, ok):
        if name in seen:
            raise ValueError('Duplicate local assertion ID: ' + name)
        seen.add(name)
        checks.append({'id': name, 'passed': bool(ok)})

    plan = verify_freeze()
    check('frozen_runner_prompts_expectations_and_all_protected_files_unchanged', True)
    execution = load(OUT / 'deepseek-flash-execution.json')
    results = load(OUT / 'deepseek-flash-results.json')
    review = load(OUT / 'deepseek-flash-review.json')
    cost = load(OUT / 'deepseek-flash-cost.json')
    manual = load(OUT / 'semantic-review.json')
    rubric = load(OUT / 'rubric-freeze.json')
    check('rubric_hash_unchanged', sha(OUT / 'review-rubric.json') == rubric['review_rubric_sha256'])
    attempts = execution['attempts']
    check('one_preflight_and_exactly_16_evaluations', len(attempts) == 17 and sum(a['kind'] == 'preflight' for a in attempts) == 1 and sum(a['kind'] == 'evaluation' for a in attempts) == 16)
    check('no_duplicate_attempt_ids_or_retries', len({a['request_id'] for a in attempts}) == 17)
    check('all_actual_http_200_success_and_complete_finish', execution['status'] == 'COMPLETE' and all(a['status'] == 'SUCCESS' and a['http_status'] == 200 and a['finish_reason'] == 'stop' for a in attempts))
    check('requested_model_only_and_thinking_high', all(r['payload']['model'] == 'deepseek-flash' and r['payload']['thinking'] == {'type': 'enabled'} and r['payload']['reasoning_effort'] == 'high' and 'tools' not in r['payload'] for r in plan['requests']))
    check('returned_model_field_preserved_not_falsely_relabelled_backend', all(a['returned_model'] == 'deepseek-flash' for a in attempts))
    check('positive_reasoning_usage_and_content_observed', all(a['reasoning_content_present'] and a['usage']['completion_tokens_details']['reasoning_tokens'] > 0 for a in attempts))
    start = min(a['started_at'] for a in attempts if a['kind'] == 'evaluation')
    check('rubric_frozen_before_first_evaluation', datetime.fromisoformat(rubric['frozen_before_evaluation_utc'].replace('Z', '+00:00')) < datetime.fromisoformat(start))
    check('expected_cases_frozen_before_preflight', datetime.fromisoformat(load(EXPECTED)['created_before_any_evaluation']) < datetime.fromisoformat(attempts[0]['started_at']))
    bound = ceiling(plan['preflight']) + sum(ceiling(r['payload']) for r in plan['requests'])
    check('whole_plan_peak_reservation_below_one_dollar', bound < 1)
    total, prompt, completion, reasoning, peak = 0, 0, 0, 0, Decimal(0)
    for a in attempts:
        usage = a['usage']
        total += usage['total_tokens']
        prompt += usage['prompt_tokens']
        completion += usage['completion_tokens']
        reasoning += usage['completion_tokens_details']['reasoning_tokens']
        check('usage_arithmetic/' + a['request_id'], usage['prompt_tokens'] + usage['completion_tokens'] == usage['total_tokens'] and usage['prompt_cache_hit_tokens'] + usage['prompt_cache_miss_tokens'] == usage['prompt_tokens'])
        peak += (Decimal(usage['prompt_cache_hit_tokens']) * Decimal('.006') + Decimal(usage['prompt_cache_miss_tokens']) * Decimal('.30') + Decimal(usage['completion_tokens']) * Decimal('1.20')) / Decimal(1000000)
    check('independent_decimal_cost_reconciliation', abs(peak - Decimal(str(cost['budget_accounted_usd']))) < Decimal('0.000000001'))
    check('no_unknown_usage_and_under_budget', cost['unknown_usage_reservation_usd'] == 0 and peak < 1)
    check('actual_usage_totals_reconcile', cost['actual_reported_usage_totals'] == dict(prompt_tokens=prompt, completion_tokens=completion, total_tokens=total, reasoning_tokens=reasoning))
    check('all_16_raw_answers_have_individual_semantic_reviews', len(results['responses']) == len(review['responses']) == len(manual['responses']) == 16)
    for row in results['responses']:
        content = row['raw_response']['choices'][0]['message']['content']
        check('manual_content_binding/' + row['request_id'], hashlib.sha256(content.encode()).hexdigest() == manual['responses'][row['request_id']]['final_content_sha256'])
        check('json_parse/' + row['request_id'], isinstance(json.loads(content), dict))
    for row in review['responses']:
        if row['suite'] == 'new-adversarial':
            check('strict_acceptance_never_hides_failed_check/' + row['request_id'], row['strict_accepted'] == (not row['failed_checks']))
    # Negative controls exercise the actual quote checker against common plausible
    # false supports: wrong source with the same clause ID, stitched words, page invention.
    sources = [{'path': 'synthetic/team-one/license.pdf', 'clauses': [{'id': 'G1', 'text': 'Editorial only. Commercial advertising is prohibited.'}]},
               {'path': 'synthetic/team-two/license.pdf', 'clauses': [{'id': 'G1', 'text': 'A different asset is licensed.'}]}]
    good = dict(source=sources[0]['path'], clause_id='G1', quote='Commercial advertising is prohibited.', page=None)
    check('negative_control/genuine_correctly_attributed_quote', quotations(good, sources)[0]['genuine_exact'])
    check('negative_control/wrong_source_even_with_duplicate_basename', not quotations(dict(good, source=sources[1]['path']), sources)[0]['genuine_exact'])
    check('negative_control/stitched_quote', not quotations(dict(good, quote='Editorial only. Advertising is prohibited.'), sources)[0]['genuine_exact'])
    check('negative_control/invented_page', not quotations(dict(good, page=1), sources)[0]['page_not_invented'])
    check('negative_control/missing_quote_never_genuine', not quotations(dict(good, quote=''), sources)[0]['genuine_exact'])
    check('known_semantic_explanation_failures_are_rejected', all(not r['strict_accepted'] and 'manual_explicit_uncertainty' in r['failed_checks'] for r in review['responses'] if r['case_id'] == 'partial-amendment'))
    staged_paths = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()
    loose_paths = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    new_names = sorted(set(staged_paths) | set(loose_paths))
    new_paths = [ROOT / p for p in new_names]
    key = os.environ.get('DEEPSEEK_API_KEY', '').encode()
    check('configured_secret_not_present_in_any_new_file', bool(key) and not any(key in p.read_bytes() for p in new_paths if p.is_file()))
    text_paths = [p for p in new_paths if p.is_file() and p.suffix in ('.py', '.md', '.json', '.txt')]
    check('new_text_files_have_no_trailing_whitespace', all(not line.endswith((' ', '\t')) for p in text_paths for line in p.read_text(encoding='utf-8-sig').splitlines()))
    for path in text_paths:
        if path.suffix == '.json':
            load(path)
    check('all_new_json_artifacts_parse', True)
    check('git_head_unchanged_no_commit', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == execution['git_head'])
    staged_eol_rules = {
        'docs/13-deepseek-flash-validation.md text eol=lf',
        'validation/check_phase1_2.py text eol=lf',
        'validation/review_deepseek_flash.py text eol=lf',
        'validation/run_deepseek_flash.py text eol=lf',
        'validation/fixtures/phase1-2/** text eol=lf',
        'validation/results/phase1-2/** text eol=lf'}
    attrs_diff = subprocess.check_output(['git', 'diff', 'HEAD', '--', '.gitattributes'], cwd=ROOT, text=True).splitlines()
    additions = {line[1:] for line in attrs_diff if line.startswith('+') and not line.startswith('+++')}
    changed_tracked = subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=ROOT, text=True).splitlines()
    allowed_scope = lambda p: (p == '.gitattributes' or p == 'docs/13-deepseek-flash-validation.md' or
        p in ('validation/check_phase1_2.py', 'validation/review_deepseek_flash.py', 'validation/run_deepseek_flash.py') or
        p.startswith('validation/fixtures/phase1-2/') or p.startswith('validation/results/phase1-2/'))
    check('changed_file_scope_is_phase1_2_and_staged_lf_rules', set(changed_tracked) == set(new_names) and all(allowed_scope(p) for p in changed_tracked) and '.gitattributes' in changed_tracked and additions == staged_eol_rules and not any(line.startswith('-') and not line.startswith('---') for line in attrs_diff))
    stable_paths = ['docs/13-deepseek-flash-validation.md', 'validation/check_phase1_2.py', 'validation/review_deepseek_flash.py', 'validation/run_deepseek_flash.py',
        'validation/fixtures/phase1-2/expected.json', 'validation/results/phase1-2/deepseek-flash-results.json']
    attrs_ok = all(subprocess.check_output(['git', 'check-attr', 'eol', '--', p], cwd=ROOT, text=True).rstrip().endswith(': eol: lf') for p in stable_paths)
    raw_blob_ok = all(subprocess.check_output(['git', 'hash-object', '--', p], cwd=ROOT, text=True).strip() == subprocess.check_output(['git', 'ls-files', '--stage', '--', p], cwd=ROOT, text=True).split()[1] for p in stable_paths)
    check('new_frozen_files_keep_lf_bytes_in_git', attrs_ok and raw_blob_ok)
    for path in (ROOT / 'validation').glob('*phase1_2*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    compile((ROOT / 'validation/run_deepseek_flash.py').read_text(), 'run_deepseek_flash.py', 'exec')
    compile((ROOT / 'validation/review_deepseek_flash.py').read_text(), 'review_deepseek_flash.py', 'exec')
    check('new_python_sources_compile_without_execution_or_pycache', True)
    report = ROOT / 'docs/13-deepseek-flash-validation.md'
    checker = Path('D:/Ollama/Temp/rightsgap-phase1-20261029/extracted/uliya-skill-kit/scripts/check-skill.mjs')
    check('official_checker_source_hash', sha(checker) == '6a9e8ad164862ab787f45e577c2e2bc98cfb31cea10f5ec291cb6550eb51fb52')
    run = subprocess.run(['node', str(checker), str(ROOT / 'rightsgap-media-reuse')], capture_output=True)
    (OUT / 'skill-static-check.json').write_bytes(run.stdout)
    static = json.loads(run.stdout)
    check('unchanged_skill_official_static_check', run.returncode == 0 and static.get('status') == 'static-pass' and static.get('diagnostics') == [])
    (OUT / 'skill-static-execution.json').write_text(json.dumps({'exit_code': run.returncode, 'checker_sha256': sha(checker),
        'stderr': run.stderr.decode('utf-8'), 'layer': 'Static only; not NAS/Uliya runtime'}, indent=2) + '\n', encoding='utf-8', newline='\n')
    # Create dependent evidence first, then validate the report links.
    for number, target in enumerate(re.findall(r'\]\(([^)]+)\)', report.read_text(encoding='utf-8')), 1):
        if '://' in target or target.startswith('#'):
            continue
        check('report_local_link/' + str(number) + '/' + target, (report.parent / target.split('#')[0]).exists())
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    check('tracked_diff_whitespace', True)
    output = {'layer': 'LOCAL EVALUATION EVIDENCE CHECKS + OFFICIAL STATIC CHECK; NO API CALLS',
        'checks': {'total': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks), 'unique_ids': len(seen)},
        'assertions': checks, 'whole_run_reserved_peak_ceiling_usd': bound,
        'reconciled_reported_usage': dict(prompt_tokens=prompt, completion_tokens=completion, total_tokens=total, reasoning_tokens=reasoning),
        'reconciled_peak_cost_usd': str(peak), 'protected_file_count': len(load(OUT / 'freeze.json')['protected_sha256']),
        'evidence_sha256': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in [EXPECTED, OUT / 'deepseek-flash-execution.json', OUT / 'deepseek-flash-prompts.json', OUT / 'deepseek-flash-results.json', OUT / 'deepseek-flash-review.json', OUT / 'deepseek-flash-cost.json', report]},
        'NAS_runtime': 'NOT RUN', 'Uliya_execution': 'NOT RUN'}
    (OUT / 'local-evaluation-checks.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: output[k] for k in ('checks', 'whole_run_reserved_peak_ceiling_usd', 'reconciled_reported_usage', 'reconciled_peak_cost_usd', 'protected_file_count')}, indent=2))
    if output['checks']['failed']:
        raise SystemExit('Evidence validation failed; inspect local-evaluation-checks.json')


if __name__ == '__main__':
    main()
