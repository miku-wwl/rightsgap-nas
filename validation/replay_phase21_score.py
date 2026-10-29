"""Replay the immutable v1 study against its exact candidate snapshot offline.

Final candidate v2 clarifies the report contract after observations. This helper
never relabels v1 results as v2 validation, alters a prompt or sends a request.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'


def main():
    preferred=Path('D:/Ollama/Temp')
    target=Path(tempfile.mkdtemp(prefix='rightsgap-p21-score-',dir=preferred if preferred.exists() else None))
    for source in (ROOT/'validation').glob('*.py'):
        q=target/'validation'/source.name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(source.read_bytes())
    files=[OUT/n for n in ['llm-freeze.json','llm-plan.json','llm-rubric.json','llm-results.json','llm-semantic-review.json','llm-cost.json']]
    files += [ROOT/'validation/fixtures/phase2-1/holdout-v1.json']
    for source in files:
        q=target/source.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(source.read_bytes())
    for source in (OUT/'study-candidate-v1').rglob('*.md'):
        q=target/'rightsgap-media-reuse'/source.relative_to(OUT/'study-candidate-v1');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(source.read_bytes())
    env=dict(os.environ);env.pop('DEEPSEEK_API_KEY',None)
    command=[sys.executable,'-B','validation/evaluate_phase21.py']
    run=subprocess.run(command,cwd=target,env=env,capture_output=True)
    result=dict(command=command,cwd=str(target),exit_code=run.returncode,stdout=run.stdout.decode('utf-8'),stderr=run.stderr.decode('utf-8'),
        study_candidate='Exact frozen v1 snapshot; final v2 external validation remains NOT_RUN',credentials_removed=True,network_requests=0)
    if run.returncode==0:
        (OUT/'llm-review.json').write_bytes((target/'validation/results/phase2-1/llm-review.json').read_bytes())
    (OUT/'score-replay-execution.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(result['stdout']);print('SCORE_REPLAY_EXIT='+str(run.returncode))
    raise SystemExit(run.returncode)


if __name__=='__main__':main()
