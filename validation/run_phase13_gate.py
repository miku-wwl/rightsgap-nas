"""Mandatory engineering gate. Local subprocesses only; no paid calls."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'validation/results/phase1-3'


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    commands = [
        ('historical-regression', ['validation/run_offline.py']),
        ('historical-hardening', ['validation/run_hardening.py']),
        ('targeted-policy-and-evaluator', ['validation/run_phase13.py']),
        ('official-static', ['validation/offline_audit.py', '--check-skill', 'phase1-3']),
        ('offline-audit', ['validation/offline_audit.py']),
        ('credential-free-audit', ['validation/offline_audit.py', '--output', 'validation/results/phase1-3/offline-audit-keyless.json'])]
    executions = []
    for name, args in commands:
        env = dict(os.environ)
        if name == 'credential-free-audit':
            env.pop('DEEPSEEK_API_KEY', None)
        started = datetime.now(timezone.utc).isoformat()
        run = subprocess.run([sys.executable, '-B', *args], cwd=ROOT, env=env, capture_output=True)
        record = dict(id=name, command=[sys.executable, '-B', *args], started_at=started,
            exit_code=run.returncode, stdout=run.stdout.decode('utf-8'), stderr=run.stderr.decode('utf-8'),
            credentials_removed=name == 'credential-free-audit')
        executions.append(record)
        write('execution.json', executions)
        print(json.dumps({'command': name, 'exit_code': run.returncode}), flush=True)
        if run.returncode:
            break
    completed = len(executions) == len(commands) and all(e['exit_code'] == 0 for e in executions)
    target = read('targeted-tests.json')
    audit = read('offline-audit.json')
    keyless = read('offline-audit-keyless.json') if completed else {}
    gates = {
        'P13-G1': target['checks']['failed'] == 0 and all(target['case_results'][f'R{n:02}']['status'] != 'CONSISTENT_EVIDENCE' for n in (1, 3, 7, 8)),
        'P13-G2': target['checks']['failed'] == 0 and len([k for k in target['case_results'] if k.startswith('B')]) == 8,
        'P13-G3': target['checks']['failed'] == 0 and target['evaluator_attack_cases'] >= 14,
        'P13-G4': audit['changed_protected_files'] == [],
        'P13-G5': all(audit['regression_suites'].values()),
        'P13-G6': read('official-static-execution.json')['exit_code'] == 0 and read('official-static.json')['summary']['errors'] == read('official-static.json')['summary']['warnings'] == 0,
        'P13-G7': audit['status'] == 'PASS' and audit['exact_secret_scan']['state'] != 'FAIL',
        'P13-G8': completed and keyless.get('status') == 'PASS' and keyless.get('exact_secret_scan', {}).get('state') == 'NOT_RUN'}
    status = 'PASS' if completed and all(gates.values()) else 'FAIL'
    result = {'phase': '1.3', 'status': status, 'gates': {k: 'PASS' if v else 'FAIL' for k, v in gates.items()},
        'phase2_start_authorized': status == 'PASS', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'limitations': ['Curated internal semantics', 'One agent semantic evaluator', 'No Uliya/NAS runtime'],
        'optional_exact_scan_without_key': keyless.get('exact_secret_scan')}
    write('gates.json', result)
    if status == 'PASS':
        paths = ['validation/reference_policy.py', 'validation/clause_fixtures.py', 'validation/strict_evaluation.py',
                 'validation/run_phase13.py', 'validation/offline_audit.py', 'validation/phase13_cases.py']
        paths += [str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'rightsgap-media-reuse').rglob('*.md')]
        write('passed-source-hashes.json', {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths})
    print('PHASE_1_3_STATUS=' + status)
    print('PHASE_2_START_AUTHORIZED=' + ('YES' if status == 'PASS' else 'NO'))
    raise SystemExit(0 if status == 'PASS' else 1)


if __name__ == '__main__':
    main()
