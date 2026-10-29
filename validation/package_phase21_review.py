"""Create a sanitized, hash-manifested engineering review archive. No upload."""
import copy
import hashlib
import json
import os
import re
import subprocess
import zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'
ZIP=ROOT/'rightsgap-phase2-1-review.zip'
REVIEW=ROOT/'review-phase21'
OMIT={'rightsgap-phase13-phase2-review.zip':'Prior review archive duplicates historical source material',
    'validation/results/phase1-2/deepseek-flash-results.json':'Historical private reasoning payload; derived final-answer envelope supplied',
    'validation/results/phase2/llm-results.json':'Historical private reasoning payload; derived final-answer envelope supplied'}


def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')


def sanitize(value):
    if isinstance(value,dict):return {k:sanitize(v) for k,v in value.items() if k not in ('reasoning_content','Authorization','api_key','access_token','refresh_token')}
    if isinstance(value,list):return [sanitize(x) for x in value]
    return value


def main():
    baseline=load(OUT/'baseline.json');allowed=set(baseline['allowed_existing_edits'])
    for p,h in baseline['tracked_sha256'].items():
        if p not in allowed and sha((ROOT/p).read_bytes())!=h:raise ValueError('Historical source bytes changed: '+p)
    if load(OUT/'audit.json')['status']!='PASS' or load(OUT/'audit-keyless.json')['status']!='PASS':raise ValueError('Local audits not passed')
    REVIEW.mkdir(exist_ok=True)
    for name,source in [('historical-phase12-finals.json','validation/results/phase1-2/deepseek-flash-results.json'),('historical-phase2-finals.json','validation/results/phase2/llm-results.json')]:
        raw=load(ROOT/source);derived=sanitize(raw)
        save(REVIEW/name,dict(derived_from=source,original_file_sha256=baseline['tracked_sha256'][source],derivation='Private reasoning omitted; all final content strings unchanged; this file is not the original raw payload',data=derived))
    save(REVIEW/'archive-scope.json',dict(purpose='Engineering review, not official submission',baseline_head=baseline['baseline_head'],
        omitted_baseline_files=[dict(path=p,sha256=baseline['tracked_sha256'][p],reason=r) for p,r in sorted(OMIT.items())],
        limits='Full 176 protected source files verified in the workspace; standalone archive checks the 173 included protected files and reports three declared omissions.'))
    for args,name in [(['diff','--binary','--no-ext-diff'],'git-diff.patch'),(['diff','--stat'],'git-diff-summary.txt'),(['status','--short','--untracked-files=all'],'git-status.txt')]:
        r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True);(REVIEW/name).write_bytes(r.stdout)
    candidates={ROOT/p for p in baseline['tracked_sha256'] if p not in OMIT}
    candidates.update((ROOT/'validation').glob('*.py'))
    for folder in [ROOT/'validation/fixtures/phase2-1',OUT,REVIEW]:candidates.update(p for p in folder.rglob('*') if p.is_file())
    candidates.update([ROOT/'PHASE21_REVIEW.md',ROOT/'docs/17-phase2-1-evidence-integrity-report.md',ROOT/'docs/18-phase2-1-validation-report.md'])
    manifest=REVIEW/'file-manifest.json';candidates.discard(manifest);entries={}
    for p in sorted(candidates):
        name=p.relative_to(ROOT).as_posix()
        if p.is_symlink():raise ValueError('Symlink cannot enter review archive')
        if '__pycache__' in p.parts or p.name.startswith('.env') or p.suffix.lower() in ('.pyc','.pem','.key','.log') or re.search(r'(^|/)(credentials|secrets)[.\-]',name.lower()):continue
        if p.is_file():entries[name]=p.read_bytes()
    required={'PHASE21_REVIEW.md','docs/17-phase2-1-evidence-integrity-report.md','docs/18-phase2-1-validation-report.md','validation/fixtures/phase2-1/holdout-v1.json',
        'validation/results/phase2-1/llm-results.json','validation/results/phase2-1/llm-review.json','validation/results/phase2-1/official-static.json',
        'validation/results/phase2-1/gates.json','review-phase21/archive-scope.json','validation/audit_phase21.py','validation/replay_phase21_score.py'}
    if not required<=set(entries):raise ValueError('Required review artifact absent')
    skill_files=[n for n in entries if n.startswith('rightsgap-media-reuse/')]
    if len(skill_files)!=4 or any(not n.endswith('.md') for n in skill_files):raise ValueError('Invalid actual Skill package boundary')
    patterns=[rb'\bAKIA[0-9A-Z]{16}\b',rb'\bgh[pousr]_[A-Za-z0-9_]{20,}\b',rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b',rb'\bsk-[A-Za-z0-9]{32,}\b',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    key=os.environ.get('DEEPSEEK_API_KEY','').strip().encode()
    if any((key and key in b) or any(re.search(rx,b) for rx in patterns) for b in entries.values()):raise ValueError('Credential scan failed; values not printed')
    inventory=dict(generated_at=datetime.now(timezone.utc).isoformat(),baseline_head=baseline['baseline_head'],purpose='Engineering review only',
        files=[dict(path=n,sha256=sha(b),bytes=len(b)) for n,b in sorted(entries.items())],manifest_self_excluded=True,
        result_layers=dict(engineering='PARTIAL',v1_strict='3/12',v1_unsafe_positive_dimensions=0,final_v2_external='NOT_RUN',uliya='NOT_RUN',nas='NOT_RUN',saving='DISABLED'))
    save(manifest,inventory);entries['review-phase21/file-manifest.json']=manifest.read_bytes()
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n,b in sorted(entries.items()):z.writestr(n,b)
    with zipfile.ZipFile(ZIP) as z:
        names=z.namelist();checks=dict(crc=z.testzip() is None,no_duplicate_names=len(names)==len({n.casefold() for n in names}),
            safe_paths=all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and ':' not in n and '\\' not in n for n in names),
            required_files=required<=set(names),all_entry_bytes_match=all(z.read(n)==b for n,b in entries.items()),
            no_git_env_or_omitted_raw=not any(n.startswith('.git/') or Path(n).name.startswith('.env') or n in OMIT for n in names),
            credential_patterns_absent=not any(re.search(rx,z.read(n)) for n in names for rx in patterns),
            included_protected_files_exact=all(sha(z.read(p))==h for p,h in baseline['tracked_sha256'].items() if p not in allowed and p not in OMIT))
        exact='NOT_RUN' if not key else 'PASS' if not any(key in z.read(n) for n in names) else 'FAIL'
        if not all(checks.values()) or exact=='FAIL':raise ValueError('ZIP integrity failed')
    result=dict(status='PASS',archive=str(ZIP),sha256=sha(ZIP.read_bytes()),bytes=ZIP.stat().st_size,entries=len(entries),checked_at=datetime.now(timezone.utc).isoformat(),
        checks=checks,exact_secret_scan=exact,secret_scan_limit='Pattern scan is not exhaustive',scope='Engineering review only; no official submission or runtime claim')
    save(ROOT/'rightsgap-phase2-1-review-verification.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
