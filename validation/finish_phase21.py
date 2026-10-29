"""Complete local checks and record separate, evidence-limited Phase 2.1 gates.

No paid requests. PASS from an audit never repairs a rejected model answer.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'


def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(name,v):(OUT/name).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    executions=[]
    def command(name,args,keyless=True):
        env=dict(os.environ)
        if keyless:env.pop('DEEPSEEK_API_KEY',None)
        cmd=[sys.executable,'-B',*args];started=datetime.now(timezone.utc).isoformat()
        r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True)
        executions.append(dict(id=name,command=cmd,started_at=started,exit_code=r.returncode,stdout=r.stdout.decode('utf-8'),stderr=r.stderr.decode('utf-8'),credentials_removed=keyless))
        save('execution.json',executions);print(json.dumps(dict(command=name,exit_code=r.returncode)),flush=True)
        if r.returncode:raise SystemExit('Required local check failed: '+name)
    command('historical-isolated-replay',['validation/replay_phase21_history.py'])
    command('new-deterministic',['validation/run_phase21.py'])
    command('evaluator-controls',['validation/test_phase21_evaluator.py'])
    command('post-observation-qualification-diagnostic',['validation/check_phase21_clarifications.py'])
    command('official-static-final-v2',['validation/check_phase21_skill.py'])
    command('immutable-v1-score-replay',['validation/replay_phase21_score.py'])
    score=load(OUT/'llm-review.json');s=score['summary'];static=load(OUT/'official-static-execution.json')
    history=load(OUT/'historical-replay.json');d=load(OUT/'deterministic.json');controls=load(OUT/'evaluator-controls.json')
    safe=s['executed_cases']==12 and s['unsafe_positive_dimensions']==s['unsupported_positive_citation_occurrences']==0
    gates={
        'P21-G0':dict(status=static['status'],scope='Actual official static check of final v2 four-file Markdown candidate'),
        'P21-G1':dict(status=history['status'],passed=history['passed'],total=history['total'],scope='Historical deterministic behavior, isolated baseline copy'),
        'P21-G2':dict(status='PASS' if d['checks']['failed']==0 and controls['status']=='PASS' else 'FAIL',passed=d['checks']['passed']+controls['passed'],total=d['checks']['total']+controls['total'],scope='Pre-model frozen deterministic integrity cases and evaluator controls; post-observation diagnostics separate'),
        'P21-G3':dict(status='PARTIAL' if safe else 'FAIL',frozen_v1_proxy_safety='PASS' if safe else 'FAIL',unsafe_positive_effective_dimensions=s['unsafe_positive_dimensions'],unsupported_positive_citations=s['unsupported_positive_citation_occurrences'],accepted_unsupported_citations=s['accepted_unsupported_citations'],final_v2_external_retest='NOT_RUN',scope='No new W04/B01 safety violation in twelve v1 proxy observations; v2 report revision untested externally'),
        'P21-G4':dict(status='PASS' if score['status']=='PASS' else 'PARTIAL',passed=s['strict_accepted'],total=s['strict_total'],scope='Frozen v1 full external contract; all failures retained; final v2 external inference NOT_RUN'),
        'P21-G5':dict(status='NOT_RUN',reason='No actual Uliya instance invoked'),
        'P21-G6':dict(status='NOT_RUN',reason='No authorized real NAS access in this session'),
        'P21-G7':dict(status='BLOCKED',reason='Full strict acceptance unresolved; final owner submission/project decisions and real runtime evidence remain separate')}
    result=dict(engineering_status='PARTIAL' if safe else 'FAIL',gates=gates,final_recommendation='CONDITIONAL_GO' if safe else 'NO_GO',
        recommendation_scope='Continue supervised Phase 2.2 report-contract and qualification validation; no submission/production readiness',
        final_candidate_external_retest='NOT_RUN',observed_vs_effective=True,saving='DISABLED',checked_at=datetime.now(timezone.utc).isoformat(),
        git_commit_created=False,git_push_performed=False,devpost_submitted=False)
    save('gates.json',result)
    revisions=load(OUT/'candidate-revisions.json');revisions['final_candidate_sha256']={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'rightsgap-media-reuse').rglob('*.md')};save('candidate-revisions.json',revisions)
    command('credential-free-audit',['validation/audit_phase21.py','--output','validation/results/phase2-1/audit-keyless.json'])
    command('optional-exact-secret-audit',['validation/audit_phase21.py'],keyless=False)
    print('PHASE21_ENGINEERING_STATUS='+result['engineering_status'])
    print('EXTERNAL_LLM_STRICT='+str(s['strict_accepted'])+'/'+str(s['strict_total']))
    print('FINAL_CANDIDATE_EXTERNAL_RETEST=NOT_RUN')
    print('ULIYA_RUNTIME=NOT_RUN\nNAS_RUNTIME=NOT_RUN')


if __name__=='__main__':main()
