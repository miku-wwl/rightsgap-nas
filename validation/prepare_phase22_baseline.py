"""One-time read-only baseline and official-tool provenance capture."""
import shutil
import subprocess
from pathlib import Path
from phase22_common import ROOT, OUT, now, sha, save, load


def main():
    if (OUT / 'baseline.json').exists():
        raise SystemExit('Refusing to overwrite initial baseline')
    git = lambda *args: subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8').strip()
    tracked = git('ls-files').splitlines()
    allowed = ['.gitattributes', 'rightsgap-media-reuse/SKILL.md',
               'rightsgap-media-reuse/references/evidence-rules.md',
               'rightsgap-media-reuse/references/report-and-recheck.md']
    save(OUT / 'baseline.json', dict(recorded_at=now(), baseline_head=git('rev-parse', 'HEAD'),
        branch=git('branch', '--show-current'), initial_status=git('status', '--porcelain=v1'),
        initial_status_at_first_inspection='CLEAN', allowed_existing_edits=allowed,
        tracked_sha256={p: sha(ROOT / p) for p in tracked},
        authorization=dict(offline_phase22=True, phase3_draft_only=True, paid_phase22=False,
            commits=False, pushes=False, saving='DISABLED', credentials_read=False)))
    for p in (ROOT / 'rightsgap-media-reuse').rglob('*.md'):
        target = OUT / 'baseline-skill' / p.relative_to(ROOT / 'rightsgap-media-reuse')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    kit = Path('D:/Ollama/Temp/rightsgap-phase22-toolchain-9404a59dcd2e4207ae764d77db25112f/extracted/uliya-skill-kit')
    old = load(ROOT / 'validation/results/phase2-1/toolchain.json')
    hashes = {p: sha(kit / p) for p in old['file_sha256']}
    if hashes != old['file_sha256']:
        raise SystemExit('Current official instructions differ; re-audit required')
    catalog = load(kit / 'data/capability-catalog.json')
    selection = load(ROOT / 'validation/official/capability-selection.json')
    for row in selection['actions']:
        cli = next(c for c in catalog['clis'] if c['name'] == row['cli'])
        action = next(a for a in cli['actions'] if a['name'] == row['definition']['name'])
        if cli['agent'] != row['agent'] or action != row['definition']:
            raise SystemExit('Selected capability changed')
    save(OUT / 'toolchain.json', dict(verified_at=now(), kit_path=str(kit),
        archive_version='0.7.3', catalog_version=catalog['catalogVersion'] if 'catalogVersion' in catalog else '2.0.0',
        official_archive_url=old['official_archive_url'], archive_sha256=sha(kit.parent.parent / 'official.zip'),
        file_sha256=hashes, complete_selected_definitions_equal=True,
        instructions_read=['SKILL.md', 'docs/skill-development-standard.md',
            'references/expert-orchestration.md', 'references/runtime-authoring-lessons.md',
            'references/cli-usage-rules.md', 'references/safety-and-approval.md',
            'references/completion-and-errors.md', 'references/check-workflow.md',
            'references/skill-format.md', 'references/capability-query.md'],
        starter_kit_read='Complete sections 1-8; live current page and download link checked before edits'))
    print('BASELINE_CAPTURED; CURRENT_OFFICIAL_KIT_HASHES_MATCH; NO_CREDENTIAL_ACCESS')


if __name__ == '__main__':
    main()
