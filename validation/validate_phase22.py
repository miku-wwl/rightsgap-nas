"""Run all authorized offline checks with a credential-free child environment.

Historical runners execute in an isolated copy. Their protected workspace
fixtures/results are never overwritten. Static checking uses the fresh kit.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from phase22_common import ROOT, OUT, load, save, sha, now


def clean_env():
    names=('PATH','SystemRoot','WINDIR','COMSPEC','PATHEXT','TEMP','TMP','USERPROFILE','APPDATA','LOCALAPPDATA')
    # Only ordinary OS paths are read. No credential lookup or environment dump.
    return {**{n:os.environ[n] for n in names if n in os.environ},'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}


def main():
    if (OUT/'execution.json').exists():
        previous=load(OUT/'execution.json')
        if any(r['exit_code'] for r in previous):
            retained=OUT/('initial-execution-'+str(len(list(OUT.glob('initial-execution-*')))+1)+'.json')
            save(retained,previous)
            save(retained.with_name(retained.stem+'-regression.json'),load(OUT/'historical-regression.json'))
    executions=[]
    def run(identifier,command,cwd=ROOT):
        started=now(); result=subprocess.run(command,cwd=cwd,env=clean_env(),capture_output=True)
        receipt=dict(id=identifier,command=command,cwd=str(cwd),started_at=started,ended_at=now(),exit_code=result.returncode,
            stdout=result.stdout.decode('utf-8',errors='replace'),stderr=result.stderr.decode('utf-8',errors='replace'),
            credential_environment_not_forwarded=True)
        executions.append(receipt);save(OUT/'execution.json',executions)
        print(__import__('json').dumps(dict(command=identifier,exit_code=result.returncode)),flush=True)
        return result
    baseline=load(OUT/'baseline.json')
    altered=[n for n,h in baseline['tracked_sha256'].items() if n not in baseline['allowed_existing_edits'] and (not (ROOT/n).is_file() or sha(ROOT/n)!=h)]
    if altered: raise SystemExit('Protected tracked bytes changed: '+repr(altered))
    destination=Path(tempfile.mkdtemp(prefix='rightsgap-p22-regression-',dir='D:/Ollama/Temp'))
    # Explicit tracked project paths only; never copy .git, .env or dependency folders.
    omissions=[]
    for name in baseline['tracked_sha256']:
        if name.endswith('.zip') or name in ('validation/results/phase1-2/deepseek-flash-results.json','validation/results/phase2/llm-results.json'):
            omissions.append(name);continue
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
    # Replay in a pristine copy BEFORE any runner can regenerate historical outputs.
    run('original-baseline-replay',[sys.executable,'-B','validation/replay_phase21_history.py'],destination)
    if (destination/'validation/results/phase2-1/historical-replay.json').exists():
        shutil.copyfile(destination/'validation/results/phase2-1/historical-replay.json',OUT/'historical-baseline-replay.json')
    tasks=[('historical-regression','run_offline.py','phase1-3/regression.json','check_details'),
        ('historical-hardening','run_hardening.py','phase1-3/hardening.json','assertions'),
        ('phase13','run_phase13.py','phase1-3/targeted-tests.json','assertions'),
        ('phase2-simulation','run_phase2.py','phase2/workflow-tests.json','assertions'),
        ('phase21','run_phase21.py','phase2-1/deterministic.json','assertions'),
        ('phase21-evaluator','test_phase21_evaluator.py','phase2-1/evaluator-controls.json','assertions'),
        ('phase21-qualification','check_phase21_clarifications.py','phase2-1/qualification-clarifications.json','assertions')]
    suites={};all_ids=[]
    for identifier,script,path,key in tasks:
        if identifier=='phase2-simulation':
            # The historical runner intentionally binds its old gated Skill bytes.
            # Restore only that historical snapshot in this disposable copy;
            # do not change the gate, expected outcomes or current worktree Skill.
            for p in (destination/'validation/results/phase2-1/baseline-skill').rglob('*.md'):
                target=destination/'rightsgap-media-reuse'/p.relative_to(destination/'validation/results/phase2-1/baseline-skill')
                shutil.copyfile(p,target)
        result=run(identifier,[sys.executable,'-B','validation/'+script],destination)
        target=destination/'validation/results'/path
        data=load(target) if target.exists() else {}
        rows=data.get(key,[])
        suites[identifier]=dict(exit_code=result.returncode,passed=sum(r['passed'] is True for r in rows),total=len(rows),
            result_sha256=sha(target) if target.exists() else None,assertions=rows)
        all_ids.extend(r.get('id',r.get('name')) for r in rows)
    save(OUT/'historical-regression.json',dict(status='PASS' if all(s['exit_code']==0 and s['passed']==s['total'] and s['total']>0 for s in suites.values()) and len(all_ids)==len(set(all_ids)) else 'FAIL',
        suites=suites,passed=sum(s['passed'] for s in suites.values()),total=len(all_ids),unique_assertion_ids=len(set(all_ids)),
        historical_phase13_phase2_total=sum(suites[n]['total'] for n in ['historical-regression','historical-hardening','phase13','phase2-simulation']),
        replay_layer='Original unmodified runners/fixtures in isolated copy; Phase2 deliberately uses its exact historical gated Skill snapshot. No Markdown execution.',
        workspace_history_untouched=True,omitted_unneeded_payloads=omissions,cwd=str(destination)))
    # New results have their own paths and cannot overwrite old scores.
    run('phase22-deterministic',[sys.executable,'-B','validation/run_phase22.py'])
    run('phase22-evaluator-controls',[sys.executable,'-B','validation/test_phase22_evaluator.py'])
    meta=load(OUT/'toolchain.json');kit=Path(meta['kit_path'])
    if any(sha(kit/n)!=h for n,h in meta['file_sha256'].items()):raise SystemExit('Official kit changed')
    result=run('official-static',['node',str(kit/'scripts/check-skill.mjs'),str(ROOT/'rightsgap-media-reuse')])
    (OUT/'official-static.json').write_bytes(result.stdout)
    raw=__import__('json').loads(result.stdout)
    import re
    skill=ROOT/'rightsgap-media-reuse';files=[p for p in skill.rglob('*') if p.is_file()]
    links=re.findall(r'\]\(([^)]+)\)',(skill/'SKILL.md').read_text(encoding='utf-8'))
    allowed=all(p.suffix=='.md' and (p.name=='SKILL.md' and p.parent==skill or p.parent==skill/'references') for p in files)
    linked=all(p.relative_to(skill).as_posix() in links for p in files if p.name!='SKILL.md') and all((skill/p).is_file() for p in links)
    save(OUT/'official-static-execution.json',dict(status='PASS' if result.returncode==0 and raw['summary']['errors']==raw['summary']['warnings']==0 and allowed and linked else 'FAIL',
        **executions[-1],only_supported_markdown=allowed,all_references_linked=linked,
        exact_skill_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in files},
        archive_sha256=meta['archive_sha256'],catalog_sha256=meta['file_sha256']['data/capability-catalog.json'],
        checker_sha256=meta['file_sha256']['scripts/check-skill.mjs'],layer='ACTUAL OFFICIAL STATIC ONLY; Uliya/NAS NOT_RUN'))
    protected=[n for n in baseline['tracked_sha256'] if n not in baseline['allowed_existing_edits']]
    intact={n:sha(ROOT/n)==baseline['tracked_sha256'][n] for n in protected}
    save(OUT/'protected-history.json',dict(status='PASS' if all(intact.values()) else 'FAIL',total=len(intact),passed=sum(intact.values()),files=intact,
        frozen_fixture_count=sum(n.startswith('validation/fixtures/') for n in protected),
        includes_historical_model_outputs=True,credential_access=False))
    passed=all(r['exit_code']==0 for r in executions) and all(intact.values()) and allowed and linked
    print('OFFLINE_EXECUTION='+('PASS' if passed else 'FAIL'))
    raise SystemExit(0 if passed else 1)


if __name__=='__main__':main()
