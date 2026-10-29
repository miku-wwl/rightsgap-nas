"""Replay actual historical runners in an isolated copy; never overwrite history."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'


def main():
    baseline=json.loads((OUT/'baseline.json').read_text(encoding='utf-8'))
    preferred=Path('D:/Ollama/Temp')
    copy_root=Path(tempfile.mkdtemp(prefix='rightsgap-p21-history-',dir=preferred if preferred.exists() else None))
    omitted=[]
    for name,wanted in baseline['tracked_sha256'].items():
        if name.endswith('.zip') or name in ('validation/results/phase1-2/deepseek-flash-results.json','validation/results/phase2/llm-results.json'):
            omitted.append(name);continue  # Not used by these four deterministic runners.
        source=ROOT/name
        data=source.read_bytes()
        if name.startswith('rightsgap-media-reuse/'):
            data=(OUT/'baseline-skill'/Path(name).relative_to('rightsgap-media-reuse')).read_bytes()
        if name not in baseline['allowed_existing_edits'] and hashlib.sha256(data).hexdigest()!=wanted:
            raise SystemExit('Historical tracked file changed: '+name)
        target=copy_root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    env=dict(os.environ);env.pop('DEEPSEEK_API_KEY',None);env['PYTHONDONTWRITEBYTECODE']='1'
    runs=[];all_ids=[];summaries={}
    tasks=[('regression','run_offline.py','phase1-3/regression.json','check_details'),
        ('hardening','run_hardening.py','phase1-3/hardening.json','assertions'),
        ('phase13','run_phase13.py','phase1-3/targeted-tests.json','assertions'),
        ('workflow','run_phase2.py','phase2/workflow-tests.json','assertions')]
    for name,script,result_path,key in tasks:
        command=[sys.executable,'-B','validation/'+script]
        run=subprocess.run(command,cwd=copy_root,env=env,capture_output=True)
        runs.append(dict(id=name,command=command,cwd=str(copy_root),exit_code=run.returncode,
            stdout=run.stdout.decode('utf-8'),stderr=run.stderr.decode('utf-8'),credentials_removed=True))
        if run.returncode:break
        result_file=copy_root/'validation/results'/result_path
        result=json.loads(result_file.read_text(encoding='utf-8'))
        rows=result[key];all_ids.extend(r.get('id',r.get('name')) for r in rows)
        summaries[name]=dict(passed=sum(r['passed'] for r in rows),total=len(rows),result_sha256=hashlib.sha256(result_file.read_bytes()).hexdigest(),assertions=rows)
    result=dict(status='PASS' if len(runs)==4 and all(r['exit_code']==0 for r in runs) and all(s['passed']==s['total'] for s in summaries.values()) and len(all_ids)==len(set(all_ids)) else 'FAIL',
        recorded_at=datetime.now(timezone.utc).isoformat(),baseline_head=baseline['baseline_head'],
        replay_layer='Original Python runners and frozen fixtures in isolated baseline Skill copy; not execution of current Markdown',
        historical_outputs_untouched=True,omitted_unneeded_execution_payloads=omitted,commands=runs,suites=summaries,passed=sum(s['passed'] for s in summaries.values()),total=len(all_ids),unique_ids=len(set(all_ids)))
    (OUT/'historical-replay.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:result[k] for k in ['status','passed','total','unique_ids']},indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)


if __name__=='__main__':main()
