"""Run only local Phase 2 verification and record honest acceptance gates.

External requests are never sent here. A stored semantic failure cannot become
PASS because static, mock, or artifact checks pass. Missing runtime stays NOT_RUN.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'validation/results/phase2'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    tasks = [
        ('simulated-workflows', ['validation/run_phase2.py']),
        ('stored-external-score', ['validation/review_phase2_llm.py']),
        ('actual-official-static', ['validation/offline_audit.py', '--check-skill', 'phase2']),
        ('credential-free-offline-audit', ['validation/offline_audit.py', '--output', 'validation/results/phase2/offline-audit-keyless.json']),
        ('phase2-artifact-audit', ['validation/audit_phase2.py'])]
    commands = []
    for name, args in tasks:
        env = dict(os.environ)
        env.pop('DEEPSEEK_API_KEY', None)
        start = datetime.now(timezone.utc).isoformat()
        result = subprocess.run([sys.executable, '-B', *args], cwd=ROOT, env=env, capture_output=True)
        commands.append(dict(id=name, command=[sys.executable, '-B', *args], started_at=start,
            exit_code=result.returncode, stdout=result.stdout.decode('utf-8'), stderr=result.stderr.decode('utf-8'), credentials_removed=True))
        save('execution.json', commands)
        print(json.dumps(dict(command=name, exit_code=result.returncode)), flush=True)
        if result.returncode:
            raise SystemExit('Local verification failed; preserve error before evaluating gates')
    p13 = load(ROOT / 'validation/results/phase1-3/gates.json')
    workflow = load(OUT / 'workflow-tests.json')
    llm = load(OUT / 'llm-review.json')
    reliability_pass = llm['summary']['strict_accepted'] == llm['summary']['strict_total']
    gates = {
        'P2-G0': dict(status='PASS', layer='Actual official static checker, no runtime'),
        'P2-G1': dict(status='PASS' if p13['status'] == 'PASS' else 'FAIL', layer='Curated deterministic reference policy'),
        'P2-G2': dict(status='PASS' if workflow['workflow_cases'] == workflow['workflow_passed'] == 22 else 'FAIL', layer='SIMULATED_EXPERT_RESULTS only'),
        'P2-G3': dict(status='PASS' if reliability_pass else 'FAIL', simulated_controls='PASS', external_reasoning=llm['status'],
            layer='Fail-closed reliability acceptance includes actual external synthetic failures, not just passing mocks',
            unsupported_positive_dimension_labels=llm['summary']['unsupported_affirmatives']['dimension_labels'],
            runtime_enforcement='NOT_RUN'),
        'P2-G4': dict(status='NOT_RUN', reason='No actual Uliya Expert Agent session invoked'),
        'P2-G5': dict(status='NOT_RUN', reason='No authorized actual NAS session available')}
    result = dict(status='CONDITIONAL_PASS' if all(g['status'] == 'PASS' for k, g in gates.items() if k not in ('P2-G4', 'P2-G5')) else 'FAIL',
        phase2_start_authorized=p13['status'] == 'PASS', gates=gates,
        checked_at=datetime.now(timezone.utc).isoformat(), saving='DISABLED',
        recommendation='CONDITIONAL_GO' if reliability_pass else 'NO_GO',
        explanation='Implementation and static/simulation audits pass. Five frozen external answers remain rejected, including unsafe positive dimensions with incomplete scope. No full reliability or submission-ready claim.')
    save('gates.json', result)
    print('PHASE_2_ENGINEERING_STATUS=' + result['status'])
    print('ULIYA_RUNTIME_STATUS=NOT_RUN')
    print('NAS_RUNTIME_STATUS=NOT_RUN')
    # A completed evidence run is not an accepted candidate. Nonzero exit exposes
    # the actual acceptance failure to callers while preserving all reports.
    raise SystemExit(0 if result['status'] != 'FAIL' else 2)


if __name__ == '__main__':
    main()
