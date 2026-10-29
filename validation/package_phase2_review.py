"""Build and inspect the engineering REVIEW ZIP, never a Devpost package.

Only this repository's explicit project folders and tracked context are used.
No upload, Git mutation, environment dump, external request or paid call occurs.
"""
import hashlib
import json
import os
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / 'rightsgap-phase13-phase2-review.zip'
RECEIPT = ROOT / 'rightsgap-phase13-phase2-review-verification.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout


def main():
    review = ROOT / 'review'
    review.mkdir(exist_ok=True)
    baseline = json.loads((ROOT / 'validation/results/phase1-3/baseline-integrity.json').read_text(encoding='utf-8'))
    if git('rev-parse', 'HEAD').decode().strip() != baseline['head']:
        raise ValueError('Unexpected Git HEAD; no archive created')
    if any(sha((ROOT / p).read_bytes()) != baseline['tracked_sha256'][p] for p in baseline['protected_paths']):
        raise ValueError('Protected historical bytes changed')
    diff_check = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True)
    if diff_check.returncode:
        raise ValueError('Git whitespace check failed')
    (review / 'git-diff.patch').write_bytes(git('diff', '--binary', '--no-ext-diff'))
    (review / 'git-diff-summary.txt').write_bytes(git('diff', '--stat'))
    (review / 'git-status.txt').write_bytes(git('status', '--short', '--untracked-files=all'))
    tracked = {p for p in git('ls-files', '-z').decode('utf-8').split('\0') if p}
    candidates = {ROOT / p for p in tracked}
    for folder in ('docs', 'validation', 'rightsgap-media-reuse', 'review'):
        candidates.update(p for p in (ROOT / folder).rglob('*') if p.is_file())
    candidates.add(ROOT / 'PHASE13_PHASE2_REVIEW.md')
    candidates.add(ROOT / '.gitattributes')
    manifest = review / 'file-manifest.json'
    candidates.discard(manifest)
    excluded, entries = [], {}
    for path in sorted(candidates):
        name = path.relative_to(ROOT).as_posix()
        lower = name.lower()
        forbidden = (path.is_symlink() or any(p in ('__pycache__', '.git', '.venv', 'node_modules', 'tmp', 'downloads', 'private-data', 'nas-dumps', 'real-user-fixtures') for p in path.relative_to(ROOT).parts)
            or path.name.startswith('.env') or path.suffix.lower() in ('.pyc', '.pem', '.key', '.log')
            or re.search(r'(^|/)(credentials|secrets)[.\-]', lower))
        if forbidden:
            excluded.append(name)
            continue
        if path.is_file():
            entries[name] = path.read_bytes()
    key = os.environ.get('DEEPSEEK_API_KEY', '').strip().encode()
    patterns = [rb'\bAKIA[0-9A-Z]{16}\b', rb'\bgh[pousr]_[A-Za-z0-9_]{20,}\b', rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b', rb'\bsk-[A-Za-z0-9]{32,}\b']
    if any(key and key in data or any(re.search(pattern, data) for pattern in patterns) for data in entries.values()):
        raise ValueError('Credential scan failed; no values printed or archived')
    required = {'AGENTS.md', 'PHASE13_PHASE2_REVIEW.md', 'docs/14-phase1-3-hardening-report.md', 'docs/15-phase2-supervised-workflow-report.md', 'docs/16-nas-runtime-validation-runbook.md',
        'validation/results/phase1-3/gates.json', 'validation/results/phase2/gates.json', 'validation/results/phase2/llm-results.json', 'validation/results/phase2/llm-review.json',
        'validation/results/phase2/official-static.json', 'validation/results/phase2/audit.json', 'validation/package_phase2_review.py'}
    if not required <= set(entries):
        raise ValueError('Required review artifact absent')
    skills = sorted(n for n in entries if n.startswith('rightsgap-media-reuse/'))
    if len(skills) != 4 or any(not n.endswith('.md') for n in skills):
        raise ValueError('Skill package boundary invalid')
    inventory = dict(purpose='Engineering REVIEW only; not Devpost submission', baseline_head=baseline['head'],
        generated_at=datetime.now(timezone.utc).isoformat(),
        files=[dict(path=n, sha256=sha(data), bytes=len(data), tracked_at_packaging=n in tracked) for n, data in sorted(entries.items())],
        manifest_self_excluded=True, exclusions=excluded,
        result_layers=dict(phase13='PASS', phase2_reliability='FAIL', external_strict='7/12; PARTIAL', uliya='NOT_RUN', nas='NOT_RUN', saving='DISABLED'),
        limits=['Content hashes, not signatures or NAS attestation', 'Credential pattern scans are not exhaustive', 'Manifest and ZIP receipt are excluded from recursive self-hashing'])
    write(manifest, inventory)
    entries['review/file-manifest.json'] = manifest.read_bytes()
    with zipfile.ZipFile(ZIP, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries.items()):
            archive.writestr(name, data)
    with zipfile.ZipFile(ZIP) as archive:
        names = archive.namelist()
        safe_names = all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and ':' not in n and '\\' not in n for n in names)
        checks = dict(crc_test=archive.testzip() is None, exact_names=set(names) == set(entries), safe_names=safe_names,
            no_duplicates=len(names) == len(set(n.casefold() for n in names)),
            all_entry_bytes_match=all(archive.read(n) == entries[n] for n in names), required_files=required <= set(names),
            all_73_protected_historical_files_match=all(sha(archive.read(p)) == baseline['tracked_sha256'][p] for p in baseline['protected_paths']),
            no_credential_patterns=not any(re.search(pattern, archive.read(n)) for n in names for pattern in patterns))
        exact = 'NOT_RUN' if not key else 'PASS' if not any(key in archive.read(n) for n in names) else 'FAIL'
        if not all(checks.values()) or exact == 'FAIL':
            raise ValueError('Archive verification failed')
    receipt = dict(status='PASS', archive=str(ZIP), archive_sha256=sha(ZIP.read_bytes()), archive_bytes=ZIP.stat().st_size,
        entries=len(entries), required_entries=len(required), verified_at=datetime.now(timezone.utc).isoformat(), checks=checks,
        exact_configured_secret_scan=exact, secret_scan_limit='No credential is printed or persisted; pattern scan is not exhaustive.',
        baseline_head=baseline['head'], git_commit_created=False, git_push_performed=False, devpost_submitted=False,
        result_layers=inventory['result_layers'], package_scope='Engineering REVIEW, never the official Devpost ZIP')
    write(RECEIPT, receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
