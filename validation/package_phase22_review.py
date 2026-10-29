"""Create one sanitized engineering review ZIP with exact manifests; no upload."""
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import PurePosixPath
from phase22_common import ROOT, OUT, FIX, load, save, sha, now

ZIP=ROOT/'rightsgap-phase2-2-review.zip'
REVIEW=ROOT/'review-phase22'
OMIT={
    'rightsgap-phase13-phase2-review.zip':'Older review ZIP duplicates included source/evidence; not an official submission',
    'rightsgap-phase2-1-review.zip':'Older review ZIP duplicates included source/evidence; not an official submission',
    'validation/results/phase1-2/deepseek-flash-results.json':'Historical private-reasoning payload; previously sanitized final answers retained separately',
    'validation/results/phase2/llm-results.json':'Historical private-reasoning payload; previously sanitized final answers retained separately',
}
PATTERNS=[rb'\bAKIA[0-9A-Z]{16}\b',rb'\bgh[pousr]_[A-Za-z0-9_]{20,}\b',rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b',rb'\bsk-[A-Za-z0-9]{32,}\b',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']


def digest(data):return hashlib.sha256(data).hexdigest()


def main():
    if ZIP.exists():raise SystemExit('Review ZIP already exists; refuse unreviewed overwrite')
    if load(OUT/'audit.json')['status']!='PASS' or load(OUT/'protected-history.json')['status']!='PASS':
        raise SystemExit('Offline audits must pass first')
    b=load(OUT/'baseline.json');REVIEW.mkdir(exist_ok=True)
    for name,h in b['tracked_sha256'].items():
        if name not in b['allowed_existing_edits'] and sha(ROOT/name)!=h:raise SystemExit('Protected source changed: '+name)
    save(REVIEW/'archive-scope.json',dict(purpose='ENGINEERING REVIEW ONLY; NOT COMPETITION ZIP',
        baseline_head=b['baseline_head'],protected_workspace_count=244,
        omitted_files=[dict(path=n,sha256=b['tracked_sha256'][n],reason=r) for n,r in OMIT.items()],
        included_history_reason='Frozen regression inputs, original runners and recorded provenance support offline reproduction. No unrelated project assets.',
        exact_secret_scan='NOT_RUN; credentials deliberately not read',
        no_new_model_observations=True,source_of_historical_sanitized_answers='review-phase21/historical-phase12-finals.json and historical-phase2-finals.json'))
    (REVIEW/'README.md').write_text('# Engineering review inventory\n\nRead [the primary review README](../PHASE22_REVIEW.md), [hardening report](../docs/19-phase2-2-report-contract-hardening.md) and [validation/gates](../docs/20-phase2-2-validation-report.md).\n\nThis is not the official competition ZIP. Current external, human, Uliya and NAS review are NOT_RUN. Saving is DISABLED.\n\n[file-manifest.json](file-manifest.json) and [SHA256SUMS.txt](SHA256SUMS.txt) cover payload files; their own inventory entries are excluded to avoid recursive hashes. [archive-scope.json](archive-scope.json) declares historical omissions.\n',encoding='utf-8',newline='\n')
    for args,name in [(['diff','--stat'],'git-diff-summary.txt'),(['status','--short','--untracked-files=all'],'git-status-before-package.txt')]:
        result=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True)
        (REVIEW/name).write_bytes(result.stdout)
    candidates={ROOT/n for n in b['tracked_sha256'] if n not in OMIT}
    candidates.update((ROOT/'validation').glob('*.py'))
    candidates.update(ROOT/'docs'/n for n in ['19-phase2-2-report-contract-hardening.md','20-phase2-2-validation-report.md','21-round1-english-proposal-draft.md','22-round1-submission-readiness-checklist.md'])
    candidates.add(ROOT/'PHASE22_REVIEW.md')
    for folder in [FIX,OUT,REVIEW]:candidates.update(p for p in folder.rglob('*') if p.is_file())
    entries={}
    for path in sorted(candidates):
        name=path.relative_to(ROOT).as_posix()
        if path.is_symlink():raise SystemExit('No symlink in engineering package')
        if path.name in ('file-manifest.json','SHA256SUMS.txt') and path.parent==REVIEW:continue
        if path.name.startswith('.env') or any(p in ('.git','node_modules','.venv','__pycache__') for p in path.parts):raise SystemExit('Disallowed package path')
        if path.suffix.lower() in ('.pem','.key','.pyc') or re.search(r'(^|/)(credentials|secrets)[.\-]',name.lower()):raise SystemExit('Sensitive package path')
        entries[name]=path.read_bytes()
    if any(re.search(rx,body) for body in entries.values() for rx in PATTERNS):raise SystemExit('Common credential-pattern check failed; no value displayed')
    required={'PHASE22_REVIEW.md','docs/19-phase2-2-report-contract-hardening.md','docs/20-phase2-2-validation-report.md',
        'docs/21-round1-english-proposal-draft.md','docs/22-round1-submission-readiness-checklist.md',
        'validation/fixtures/phase2-2/deterministic-v1.json','validation/fixtures/phase2-2/holdout-v1.json',
        'validation/results/phase2-2/gates.json','validation/results/phase2-2/human-review-worksheet.md',
        'validation/results/phase2-2/official-static.json','validation/results/phase2-2/audit.json','review-phase22/README.md'}
    if not required<=set(entries):raise SystemExit('Required artifact missing')
    manifest=dict(generated_at=now(),purpose='ENGINEERING REVIEW ONLY',baseline_head=b['baseline_head'],
        manifest_and_checksums_self_excluded=True,
        files=[dict(path=n,bytes=len(body),sha256=digest(body)) for n,body in sorted(entries.items())],
        gates=load(OUT/'gates.json'),secret_scan='Common patterns PASS; exact-value scan NOT_RUN; not exhaustive')
    save(REVIEW/'file-manifest.json',manifest)
    (REVIEW/'SHA256SUMS.txt').write_text(''.join(digest(body)+'  '+n+'\n' for n,body in sorted(entries.items())),encoding='utf-8',newline='\n')
    entries['review-phase22/file-manifest.json']=(REVIEW/'file-manifest.json').read_bytes()
    entries['review-phase22/SHA256SUMS.txt']=(REVIEW/'SHA256SUMS.txt').read_bytes()
    with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,body in sorted(entries.items()):archive.writestr(name,body)
    with zipfile.ZipFile(ZIP) as archive:
        names=archive.namelist()
        checks=dict(crc=archive.testzip() is None,no_duplicate_names=len(names)==len({n.casefold() for n in names}),
            safe_relative_paths=all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and ':' not in n and '\\' not in n for n in names),
            required_artifacts=required<=set(names),all_payload_bytes_exact=all(archive.read(n)==body for n,body in entries.items()),
            manifest_hashes=all(digest(archive.read(r['path']))==r['sha256'] for r in manifest['files']),
            no_omitted_raw_or_prior_archives=not set(OMIT)&set(names),
            common_secret_patterns_absent=not any(re.search(rx,archive.read(n)) for n in names for rx in PATTERNS),
            only_four_current_skill_markdown=len([n for n in names if n.startswith('rightsgap-media-reuse/')])==4 and all(n.endswith('.md') for n in names if n.startswith('rightsgap-media-reuse/')),
            included_protected_bytes=all(digest(archive.read(n))==h for n,h in b['tracked_sha256'].items() if n not in b['allowed_existing_edits'] and n not in OMIT))
        if not all(checks.values()):raise SystemExit('Archive integrity failed: '+repr(checks))
    result=dict(status='PASS',checked_at=now(),archive=str(ZIP),sha256=sha(ZIP),bytes=ZIP.stat().st_size,
        entries=len(entries),checks=checks,actual_model_calls=0,human_review='NOT_RUN',uliya_runtime='NOT_RUN',nas_runtime='NOT_RUN',
        exact_secret_scan='NOT_RUN; no credentials read',scope='ENGINEERING REVIEW ZIP ONLY; final competition PDF/ZIP NOT_CREATED')
    save(ROOT/'rightsgap-phase2-2-review-verification.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
