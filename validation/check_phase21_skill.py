"""Run the actual installed official checker against the current Markdown Skill."""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'


def main():
    meta=json.loads((OUT/'toolchain.json').read_text(encoding='utf-8'))
    kit=Path(meta['kit_path'])
    if any(hashlib.sha256((kit/p).read_bytes()).hexdigest()!=h for p,h in meta['file_sha256'].items()):
        raise SystemExit('Official tool changed; stop static check')
    skill=ROOT/'rightsgap-media-reuse'
    command=['node',str(kit/'scripts/check-skill.mjs'),str(skill)]
    run=subprocess.run(command,capture_output=True)
    (OUT/'official-static.json').write_bytes(run.stdout)
    raw=json.loads(run.stdout)
    files=[p for p in skill.rglob('*') if p.is_file()]
    root_text=(skill/'SKILL.md').read_text(encoding='utf-8')
    links=re.findall(r'\]\(([^)]+)\)',root_text)
    allowed=all(p.suffix=='.md' and (p.name=='SKILL.md' and p.parent==skill or p.parent==skill/'references') for p in files)
    linked=all(p.relative_to(skill).as_posix() in links for p in files if p.name!='SKILL.md') and all((skill/p).is_file() for p in links)
    result=dict(command=command,checked_at=datetime.now(timezone.utc).isoformat(),exit_code=run.returncode,
        stderr=run.stderr.decode('utf-8'),archive_version=meta['archive_version'],catalog_version=meta['catalog_version'],
        checker_sha256=meta['file_sha256']['scripts/check-skill.mjs'],node_version=subprocess.check_output(['node','--version'],text=True).strip(),
        only_supported_markdown=allowed,all_references_linked=linked,
        exact_skill_sha256={p.relative_to(skill).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        status='PASS' if run.returncode==0 and raw['summary']['errors']==raw['summary']['warnings']==0 and allowed and linked else 'FAIL',
        layer='Actual official STATIC check only; Uliya/NAS NOT_RUN')
    (OUT/'official-static-execution.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)


if __name__=='__main__':main()
