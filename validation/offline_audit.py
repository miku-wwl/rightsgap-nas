"""Reusable credential-free artifact audit. No model/NAS/network calls.

Optional exact-value secret scanning is reported separately when a key exists.
Historical evidence is read only. The audit writes only its new chosen receipt.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
from decimal import Decimal
from pathlib import Path

from strict_evaluation import citation_audit, PASS, FAIL, NOT_RUN

ROOT = Path(__file__).resolve().parent.parent
P13 = ROOT / 'validation/results/phase1-3'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def official_check(phase='phase1-3'):
    meta = load(P13 / 'toolchain.json')
    kit = Path(meta['kit_path'])
    checker = kit / 'scripts/check-skill.mjs'
    if sha(checker) != meta['checker_sha256']:
        raise ValueError('Official checker changed')
    run = subprocess.run(['node', str(checker), str(ROOT / 'rightsgap-media-reuse')], capture_output=True)
    folder = ROOT / ('validation/results/' + phase)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'official-static.json').write_bytes(run.stdout)
    save(folder / 'official-static-execution.json', {'command': ['node', str(checker), str(ROOT / 'rightsgap-media-reuse')],
        'exit_code': run.returncode, 'stderr': run.stderr.decode('utf-8'), 'checker_sha256': sha(checker),
        'catalog_version': meta['catalog_version'], 'archive_version': '0.7.3', 'archive_sha256': meta['archive_sha256'],
        'node_version': subprocess.check_output(['node', '--version'], text=True).strip(), 'layer': 'OFFICIAL STATIC ONLY; ULIYA/NAS NOT_RUN'})
    return run.returncode


def historical_metrics():
    folder = ROOT / 'validation/results/phase1-2'
    plan = load(folder / 'deepseek-flash-prompts.json')
    expected = load(ROOT / 'validation/fixtures/phase1-2/expected.json')['cases']
    raw = load(folder / 'deepseek-flash-results.json')['responses']
    stored = load(folder / 'deepseek-flash-review.json')
    metrics = dict(responses=len(raw), scenario_labels_matched=0, scenario_labels_total=0,
                   dimension_labels_matched=0, dimension_labels_total=0, quotations_exact=0, quotation_occurrences=0,
                   historical_expanded_strict_answers=sum(r['strict_accepted'] for r in stored['responses'] if r['suite'] == 'new-adversarial'))
    for r in raw:
        answer = json.loads(r['raw_response']['choices'][0]['message']['content'])
        req = next(p for p in plan['requests'] if p['request_id'] == r['request_id'])
        user = json.loads(req['payload']['messages'][1]['content'])
        e = expected[r['case_id']]
        if r['suite'] == 'identical-primary':
            metrics['scenario_labels_total'] += 1
            metrics['scenario_labels_matched'] += answer.get('status') == e['status']
            metrics['quotation_occurrences'] += 1
            metrics['quotations_exact'] += isinstance(answer.get('quote'), str) and bool(answer['quote']) and answer['quote'] in user['evidence']
        else:
            for n, name in enumerate(('scenario_A', 'scenario_B')):
                metrics['scenario_labels_total'] += 1
                metrics['scenario_labels_matched'] += answer[name]['status'] == e['overall_statuses'][n]
                for dim, target in e['dimension_statuses'][n].items():
                    metrics['dimension_labels_total'] += 1
                    metrics['dimension_labels_matched'] += answer[name]['dimensions'][dim]['status'] == target
            quotes = citation_audit(answer, user['sources'])
            metrics['quotation_occurrences'] += len(quotes)
            metrics['quotations_exact'] += sum(q['exact'] for q in quotes)
    return metrics


def audit(output):
    baseline = load(P13 / 'baseline-integrity.json')
    checks = []
    def check(identifier, value, detail=''):
        if any(c['id'] == identifier for c in checks):
            raise ValueError('Duplicate audit ID')
        checks.append({'id': identifier, 'state': PASS if value is True else FAIL, 'detail': detail})
    protected = [p for p in baseline['protected_paths'] if sha(ROOT / p) != baseline['tracked_sha256'][p]]
    check('historical_artifacts_byte_exact', not protected, 'All 73 selected historical files; no rewriting or normalized comparison')
    check('pre_change_skill_snapshot_preserved', all(sha(P13 / 'baseline-skill' / Path(p).relative_to('rightsgap-media-reuse')) == value
        for p, value in baseline['tracked_sha256'].items() if p.startswith('rightsgap-media-reuse/')))
    fixture = ROOT / 'validation/fixtures/phase1-3/cases-v2.json'
    check('new_expectation_integrity', sha(fixture) == load(fixture.parent / 'freeze-v2.json')['cases_sha256'])
    v1, v2 = load(fixture.parent / 'cases-v1.json'), load(fixture)
    check('fixture_wording_revision_preserves_all_expected_labels', [(r['id'], r['expected']) for r in v1['cases']] == [(r['id'], r['expected']) for r in v2['cases']])
    old = historical_metrics()
    check('historical_observations_reconcile', old == dict(responses=16, scenario_labels_matched=26, scenario_labels_total=26,
        dimension_labels_matched=120, dimension_labels_total=120, quotations_exact=233, quotation_occurrences=233, historical_expanded_strict_answers=8))
    execution = load(ROOT / 'validation/results/phase1-2/deepseek-flash-execution.json')
    peak = Decimal(0)
    totals = dict(prompt_tokens=0, completion_tokens=0, total_tokens=0, reasoning_tokens=0)
    for a in execution['attempts']:
        u = a['usage']
        peak += (Decimal(u['prompt_cache_hit_tokens']) * Decimal('.006') + Decimal(u['prompt_cache_miss_tokens']) * Decimal('.30') + Decimal(u['completion_tokens']) * Decimal('1.20')) / Decimal(1000000)
        for key in ('prompt_tokens', 'completion_tokens', 'total_tokens'):
            totals[key] += u[key]
        totals['reasoning_tokens'] += u['completion_tokens_details']['reasoning_tokens']
    check('historical_usage_and_cost_recalculated', totals['total_tokens'] == 100176 and peak == Decimal('0.107351964'))
    all_ids = []
    suite_ok = {}
    for name, detail_key in (('regression', 'check_details'), ('hardening', 'assertions'), ('targeted-tests', 'assertions')):
        result = load(P13 / (name + '.json'))
        details = result[detail_key]
        all_ids += [c.get('id', c.get('name')) for c in details]
        passed = sum(c['passed'] is True for c in details)
        suite_ok[name] = passed == len(details) and passed == result['checks']['passed'] and result['checks']['failed'] == 0
        check(name + '_raw_assertions_reconcile', suite_ok[name])
    check('global_assertion_ids_unique', len(all_ids) == len(set(all_ids)))
    skill = ROOT / 'rightsgap-media-reuse'
    files = sorted(p for p in skill.rglob('*') if p.is_file())
    root_text = (skill / 'SKILL.md').read_text(encoding='utf-8')
    check('skill_markdown_only_package', all(p.suffix == '.md' and (p.name == 'SKILL.md' and p.parent == skill or p.parent == skill / 'references') for p in files))
    links = re.findall(r'\]\(([^)]+)\)', root_text)
    check('all_references_directly_linked_and_resolve', all(str(p.relative_to(skill)).replace('\\', '/') in links for p in files if p.name != 'SKILL.md') and all((skill / t).is_file() for t in links))
    combined = '\n'.join(p.read_text(encoding='utf-8') for p in files)
    targets = set(re.findall(r'delegate --target ([a-z-]+)', combined))
    check('documented_read_only_delegate_targets', targets == {'file-agent', 'document-agent'} and 'delegate --target knowledge-agent' not in combined)
    check('saving_stays_disabled', 'Saving is disabled' in root_text and 'save delegation' in combined.lower())
    check('no_executable_parent_commands', not re.search(r'`(?:cli\.invoke|python |docker |curl |wget )', combined))
    check('documentary_vs_legal_uncertainty_explicit', 'Do not invent an unresolved priority dispute' in combined and 'prohibited scope' in combined)
    static = load(P13 / 'official-static.json')
    static_run = load(P13 / 'official-static-execution.json')
    check('official_static_check_pass', static_run['exit_code'] == 0 and static['status'] == 'static-pass' and static['summary']['errors'] == static['summary']['warnings'] == 0)
    check('current_checked_skill_hashes', all(sha(skill / f['path']) == f['sha256'] for f in static['files']))
    # Only this explicitly selected project tree is inspected, never NAS roots.
    selected = [ROOT / 'AGENTS.md', ROOT / '.gitattributes']
    for folder in ('docs', 'validation', 'rightsgap-media-reuse'):
        selected += [p for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in ('.py', '.json', '.md', '.txt') and '__pycache__' not in p.parts]
    patterns = [rb'\bAKIA[0-9A-Z]{16}\b', rb'\bgh[pousr]_[A-Za-z0-9_]{20,}\b', rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b', rb'\bsk-[A-Za-z0-9]{32,}\b']
    check('obvious_credential_patterns_absent', not any(re.search(pattern, p.read_bytes()) for p in selected for pattern in patterns), 'Pattern scan does not cover every possible encoded secret')
    key = os.environ.get('DEEPSEEK_API_KEY', '').encode()
    exact = dict(state=NOT_RUN, reason='No exact secret available; ordinary audit is credential-free') if not key else dict(
        state=PASS if not any(key in p.read_bytes() for p in selected) else FAIL,
        reason='Exact configured value checked without printing or retaining it')
    git_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() if (ROOT / '.git').exists() else None
    check('no_commit_during_authorized_work', git_head is None or git_head == baseline['head'], 'Git absence in an unpacked review archive is allowed; evidence is hashed independently')
    result = dict(layer='ORDINARY OFFLINE AUDIT; NO MODEL/NAS REQUESTS', status=PASS if all(c['state'] == PASS for c in checks) and exact['state'] != FAIL else FAIL,
        checks=checks, check_count=len(checks), passed=sum(c['state'] == PASS for c in checks), protected_files=len(baseline['protected_paths']),
        changed_protected_files=protected, historical_phase12_metrics=old, historical_usage=totals, historical_peak_usd=str(peak),
        regression_suites=suite_ok, global_assertion_ids=len(all_ids), exact_secret_scan=exact,
        explicit_limits=['Curated semantics, not arbitrary-language entailment', 'No actual expert execution', 'No NAS runtime or approval enforcement'])
    save(output, result)
    print(json.dumps({k: result[k] for k in ('status', 'check_count', 'passed', 'protected_files', 'global_assertion_ids', 'exact_secret_scan')}, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=P13 / 'offline-audit.json')
    parser.add_argument('--check-skill', choices=('phase1-3', 'phase2'))
    args = parser.parse_args()
    if args.check_skill:
        raise SystemExit(official_check(args.check_skill))
    if not any(args.output.resolve().is_relative_to(ROOT / ('validation/results/' + p)) for p in ('phase1-3', 'phase2')):
        raise SystemExit('Refusing historical result destination')
    raise SystemExit(0 if audit(args.output)['status'] == PASS else 1)
