"""Credential-free internal artifact audit and explicit acceptance gates."""
import ast
import json
import re
import subprocess
from phase22_common import ROOT, OUT, FIX, sha, load, save, now, verify_freeze


def main():
    rows=[]
    def check(name,ok,detail=None): rows.append(dict(id='p22-audit/'+name,passed=ok is True,detail=detail))
    b=load(OUT/'baseline.json')
    protected={n:h for n,h in b['tracked_sha256'].items() if n not in b['allowed_existing_edits']}
    check('protected_history',all((ROOT/n).is_file() and sha(ROOT/n)==h for n,h in protected.items()),dict(files=len(protected)))
    fixtures=verify_freeze('deterministic-v1.json'); holdout=verify_freeze('holdout-v1.json')
    freeze=load(OUT/'llm-freeze.json')
    check('study_and_current_candidate_frozen',all(sha(ROOT/n)==h for n,h in {**freeze['hashes'],**freeze['candidate_sha256']}.items()))
    check('fresh_case_ids',len(fixtures['cases'])==17 and len(holdout['cases'])==12 and len({c['id'] for c in fixtures['cases']+holdout['cases']})==29)
    h=load(OUT/'historical-regression.json'); d=load(OUT/'deterministic.json'); e=load(OUT/'evaluator-controls.json')
    check('historical_suites',h['status']=='PASS' and h['passed']==h['total']==1782 and all(s['exit_code']==0 and s['total']>0 and s['passed']==s['total'] for s in h['suites'].values()))
    check('original_baseline_1186',load(OUT/'historical-baseline-replay.json')['status']=='PASS' and load(OUT/'historical-baseline-replay.json')['passed']==1186)
    check('new_deterministic',d['status']=='PASS' and d['passed']==d['total']==657)
    check('new_evaluator_controls',e['status']=='PASS' and e['passed']==e['total']==34)
    assertions=[r for s in h['suites'].values() for r in s['assertions']]+d['assertions']+e['assertions']
    ids=[r.get('id',r.get('name')) for r in assertions]
    check('global_assertion_ids',len(ids)==len(set(ids))==2473 and all(r['passed'] is True for r in assertions))
    static=load(OUT/'official-static-execution.json'); raw=load(OUT/'official-static.json')
    check('current_official_static',static['status']=='PASS' and static['exit_code']==0 and raw['summary']['errors']==raw['summary']['warnings']==0 and all(sha(ROOT/n)==v for n,v in static['exact_skill_sha256'].items()))
    check('skill_package_boundary',static['only_supported_markdown'] is True and static['all_references_linked'] is True and len(static['exact_skill_sha256'])==4)
    check('initial_failures_retained',(OUT/'initial-execution-1.json').is_file() and sum(r['exit_code']!=0 for r in load(OUT/'initial-execution-1.json'))==2)
    check('current_execution_all_commands_pass',all(r['exit_code']==0 for r in load(OUT/'execution.json')))
    external=load(OUT/'external-status.json');plan=load(OUT/'llm-plan.json')
    check('no_external_observation_or_cost',external['status']=='NOT_RUN' and external['attempted_requests']==external['actual_estimated_cost_usd']==0 and external['returned_model_ids']==[] and all(v=='NOT_RUN' for v in external['metrics'].values()))
    check('unpaid_plan_bounds',plan['external_authorization'] is False and plan['proposed_request_count']==len(plan['requests'])==12 and plan['conservative_maximum_estimated_cost_usd']<=.30 and plan['actual_requests']==0)
    cost=round(sum((r['input_token_upper_bound']*.30+r['payload']['max_tokens']*1.20)/1e6 for r in plan['requests']),9)
    check('cost_arithmetic',cost==plan['conservative_maximum_estimated_cost_usd'],dict(proposed_maximum_usd=cost,actual_new_cost_usd=0))
    check('no_expected_labels_in_payload',all('expected' not in json.loads(r['payload']['messages'][1]['content']) and 'tools' not in r['payload'] and r['payload']['model']=='deepseek-flash' for r in plan['requests']))
    review=load(OUT/'human-review-status.json');template=load(OUT/'semantic-review-template.json')
    check('no_fabricated_human_or_semantic_review',review['status']=='NOT_RUN' and review['human_reviewer'] is None and review['signoff'] is None and template['status']=='NOT_RUN' and all(v is None for r in template['reviews'].values() for v in r['checks'].values()))
    k=load(OUT/'H21-K-investigation.json')
    check('H21K_dispute_retained',len(k['mismatches'])==3 and k['historical_expectation_changed'] is False and k['actual_tools_executed'] is False)
    proposal=ROOT/'docs/21-round1-english-proposal-draft.md'; text=proposal.read_text(encoding='utf-8')
    block=text.split('<!-- RESPONSES_START -->')[1].split('<!-- RESPONSES_END -->')[0]
    substantive=' '.join(line for line in block.splitlines() if not line.startswith('##'))
    counts=dict(substantive_whitespace_words=len(substantive.split()),including_headings_whitespace_words=len(block.split()),
        substantive_lexical_words=len(re.findall(r'\b[\w]+(?:[-/][\w]+)*\b',substantive)),
        substantive_split_hyphen_slash_words=len(re.findall(r'\b\w+\b',substantive)),
        proposal_sha256=sha(proposal),headings=len(re.findall(r'^## \d+\.',block,re.M)))
    save(OUT/'proposal-word-count.json',counts)
    check('proposal_ten_questions_under_500',counts['headings']==10 and max(v for k,v in counts.items() if k.endswith('words'))<=500,counts)
    check('draft_limits_disclosed',all(s in text for s in ('DRAFT','Verified:','Assumed:','Unknown:','Not Run:','3/12','saving is disabled')))
    required=['docs/19-phase2-2-report-contract-hardening.md','docs/20-phase2-2-validation-report.md','docs/21-round1-english-proposal-draft.md','docs/22-round1-submission-readiness-checklist.md']
    check('required_reports',all((ROOT/n).is_file() for n in required))
    new_python=[p for p in (ROOT/'validation').glob('*.py') if p.relative_to(ROOT).as_posix() not in b['tracked_sha256']]
    for path in new_python:ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    check('new_python_syntax',bool(new_python))
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True)
    check('git_diff_check',diff.returncode==0,dict(exit_code=diff.returncode,stdout=diff.stdout.decode(),stderr=diff.stderr.decode()))
    current=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    check('head_unchanged',current==b['baseline_head'])
    changed=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
    check('existing_changes_scoped',set(changed)<=set(b['allowed_existing_edits']),dict(existing_changed_paths=changed))
    patterns=[rb'\bAKIA[0-9A-Z]{16}\b',rb'\bgh[pousr]_[A-Za-z0-9_]{20,}\b',rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b',rb'\bsk-[A-Za-z0-9]{32,}\b',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    files=[p for folder in [ROOT/'rightsgap-media-reuse',FIX,OUT] for p in folder.rglob('*') if p.is_file()]
    files+=new_python+[ROOT/n for n in required]
    check('common_secret_patterns_absent',not any(re.search(rx,p.read_bytes()) for p in files for rx in patterns))
    result=dict(status='PASS' if all(r['passed'] for r in rows) else 'FAIL',recorded_at=now(),assertions=rows,
        passed=sum(r['passed'] for r in rows),total=len(rows),failures=[r for r in rows if not r['passed']],
        exact_secret_scan='NOT_RUN: credentials deliberately never read',
        secret_scan_limit='Common-pattern scan of explicit project artifacts is not an exhaustive secret detector',
        protected_file_count=len(protected),unique_regression_assertion_ids=len(set(ids)))
    save(OUT/'audit.json',result)
    gates={
        'G0':dict(status=static['status'],scope='Current official static checker only'),
        'G1':dict(status=h['status'],passed=h['passed'],total=h['total'],original_four_suites=1186),
        'G2':dict(status='PASS' if d['status']==e['status']=='PASS' else 'FAIL',passed=d['passed']+e['passed'],total=d['total']+e['total']),
        'G3':dict(status='NOT_RUN',reason='No separate Phase 2.2 paid authorization',unsafe_positives='NOT_RUN',unsupported_accepted_citations='NOT_RUN',unauthorized_source_contamination='NOT_RUN'),
        'G4':dict(status='NOT_RUN',metrics=external['metrics']),
        'G5':dict(status='NOT_RUN',reason='Worksheet prepared, no actual independent human review'),
        'G6':dict(status='NOT_RUN',reason='No genuine Uliya execution'),
        'G7':dict(status='NOT_RUN',reason='No authorized NAS access')}
    save(OUT/'gates.json',dict(project='RightsGap NAS',phase='2.2 + Phase 3 Draft',baseline_head=b['baseline_head'],current_head=current,
        initial_worktree_status='CLEAN at first inspection',offline_engineering_status=result['status'],engineering_status='PARTIAL' if result['status']=='PASS' else 'FAIL',
        gates=gates,save_feature='DISABLED',new_api_requests=0,estimated_additional_cost_usd=0,
        proposed_requests=12,proposed_conservative_maximum_cost_usd=cost,round1_proposal_draft='READY' if result['status']=='PASS' else 'PARTIAL',
        round1_final_pdf='NOT_CREATED',round1_final_zip='NOT_CREATED',git_commit_created=False,git_push_performed=False,devpost_submitted=False,
        final_recommendation='CONDITIONAL_GO' if result['status']=='PASS' else 'NO_GO',recommendation_scope='Owner draft review and explicitly authorized further validation, not automatic final submission or runtime success'))
    print(json.dumps(dict(status=result['status'],passed=result['passed'],total=result['total'],failures=result['failures'],unique_regression_ids=len(set(ids)))))
    raise SystemExit(0 if result['status']=='PASS' else 1)


if __name__=='__main__':main()
