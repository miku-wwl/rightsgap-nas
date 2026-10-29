"""Separate post-observation, unpaid qualification diagnostics; no score repair."""
import hashlib
import json
from pathlib import Path

from effective_assessment import compare_effective

ROOT=Path(__file__).resolve().parent


def main():
    path=ROOT/'fixtures/phase2-1/qualification-clarifications-v1.json'
    receipt=json.loads(path.with_name('qualification-clarifications-freeze.json').read_text(encoding='utf-8'))
    if hashlib.sha256(path.read_bytes()).hexdigest()!=receipt['sha256']:raise SystemExit('Clarification source/expectation changed')
    cases=json.loads(path.read_text(encoding='utf-8'))['cases'];checks=[];results={}
    for c in cases:
        r=compare_effective(c);rows=r['assessments'];results[c['id']]=r
        values=[row['status'] for row in rows]
        dimensions=[{d:x['status'] for d,x in row['dimensions'].items()} for row in rows]
        for suffix,ok in [('overall',values==c['expected']['overall']),('dimensions',dimensions==c['expected']['dimensions']),('R1_preserved',bool(rows[1]['observed_conflicts'].get('purpose')))]:
            checks.append(dict(id='p21-clarification/'+c['id']+'/'+suffix,passed=ok))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),assertions=checks,results=results,
        layer='POST-OBSERVATION UNPAID DIAGNOSTIC; does not change original strict 3/12 or frozen holdout expectations')
    (ROOT/'results/phase2-1/qualification-clarifications.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:result[k] for k in ['status','passed','total','layer']},indent=2));raise SystemExit(0 if result['status']=='PASS' else 1)


if __name__=='__main__':main()
