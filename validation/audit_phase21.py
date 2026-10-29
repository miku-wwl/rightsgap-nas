"""Credential-optional, network-free Phase 2.1 artifact/provenance audit."""
import argparse
import hashlib
import json
import os
import re
import subprocess
from decimal import Decimal
from pathlib import Path

from evaluate_phase21 import judge21
from strict_evaluation import citation_audit,content_hash

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'
OMISSIONS={'rightsgap-phase13-phase2-review.zip','validation/results/phase1-2/deepseek-flash-results.json','validation/results/phase2/llm-results.json'}


def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main(output):
    checks=[]
    def check(identifier,ok,detail=''):
        if identifier in {c['id'] for c in checks}:raise ValueError('Duplicate audit identifier')
        checks.append(dict(id=identifier,state='PASS' if ok is True else 'FAIL',detail=detail))
    base=load(OUT/'baseline.json');allowed=set(base['allowed_existing_edits'])
    archived=not (ROOT/'.git').exists() and (ROOT/'review-phase21/archive-scope.json').exists()
    missing=[p for p in base['tracked_sha256'] if not (ROOT/p).is_file()]
    check('baseline_omissions_explicit',not missing or archived and set(missing)<=OMISSIONS,'ZIP omits old ZIP and two private-reasoning payloads; sanitized final answers retained separately')
    protected=[p for p in base['tracked_sha256'] if p not in allowed and (ROOT/p).is_file()]
    changed=[p for p in protected if sha(ROOT/p)!=base['tracked_sha256'][p]]
    check('historical_bytes_unchanged',not changed,f'{len(protected)} protected files present checked; {len(missing)} declared omissions in standalone ZIP' if archived else f'All {len(protected)} protected files checked')
    check('baseline_skill_snapshot_exact',all(sha(OUT/'baseline-skill'/Path(p).relative_to('rightsgap-media-reuse'))==h for p,h in base['tracked_sha256'].items() if p.startswith('rightsgap-media-reuse/')))
    if (ROOT/'.git').exists():
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        check('head_unchanged',head==base['baseline_head'])
    else:check('git_absent_archive_allowed',archived)
    fixture=ROOT/'validation/fixtures/phase2-1/deterministic-v1.json'
    check('new_deterministic_expectations_frozen',sha(fixture)==load(fixture.with_name('freeze.json'))['sha256'])
    d=load(OUT/'deterministic.json');cases=load(fixture)['cases'];by_id={c['id']:c for c in cases}
    actual=list(d['cases'].values())
    check('deterministic_outcomes_recalculate',all([r['status'] for r in x['actual']['assessments']]==x['expected']['overall'] and [{k:v['status'] for k,v in r['dimensions'].items()} for r in x['actual']['assessments']]==x['expected']['dimensions'] for x in actual))
    check('deterministic_no_unsafe_positive',not any(cell['status']=='CONSISTENT_EVIDENCE' and x['expected']['dimensions'][i][dim]!='CONSISTENT_EVIDENCE' for x in actual for i,row in enumerate(x['actual']['assessments']) for dim,cell in row['dimensions'].items()))
    check('observed_provenance_recalculate',all(any(doc['path']==o['source'] and o['quote'] in doc['text'] for doc in by_id[k]['documents']) for k,x in d['cases'].items() for row in x['actual']['assessments'] for o in row['observed_evidence']))
    history=load(OUT/'historical-replay.json');controls=load(OUT/'evaluator-controls.json');clarify=load(OUT/'qualification-clarifications.json')
    ids=[a['id'] for a in d['assertions']]+[a['id'] for a in controls['assertions']]+[a['id'] for a in clarify['assertions']]
    for s in history['suites'].values():ids += [r.get('id',r.get('name')) for r in s['assertions']]
    check('assertion_statistics_recalculate',d['checks']==dict(passed=sum(a['passed'] for a in d['assertions']),total=len(d['assertions']),failed=sum(not a['passed'] for a in d['assertions']),unique_ids=len({a['id'] for a in d['assertions']})))
    check('all_required_local_regressions_pass',history['status']=='PASS' and d['checks']['failed']==0 and controls['passed']==controls['total'] and clarify['passed']==clarify['total'])
    check('global_assertion_ids_unique',len(ids)==len(set(ids)),f'{len(ids)} assertions across layers; not independent model samples')
    static=load(OUT/'official-static.json');run=load(OUT/'official-static-execution.json')
    check('actual_official_static_pass',run['exit_code']==0 and static['summary']['errors']==static['summary']['warnings']==0 and run['only_supported_markdown'] and run['all_references_linked'])
    check('final_candidate_static_hashes',all(sha(ROOT/'rightsgap-media-reuse'/p)==h for p,h in run['exact_skill_sha256'].items()))
    freeze=load(OUT/'llm-freeze.json')
    check('frozen_prompts_expectations_rubric_and_evaluator',all(sha(ROOT/p)==h for p,h in freeze['hashes'].items()))
    check('study_candidate_v1_exact',all(sha(OUT/'study-candidate-v1'/Path(p).relative_to('rightsgap-media-reuse'))==h for p,h in freeze['candidate_sha256'].items()))
    check('final_v2_change_is_report_only',all(sha(ROOT/p)==h for p,h in freeze['candidate_sha256'].items() if not p.endswith('report-and-recheck.md')) and sha(ROOT/'rightsgap-media-reuse/references/report-and-recheck.md')!=freeze['candidate_sha256']['rightsgap-media-reuse/references/report-and-recheck.md'])
    observations=load(OUT/'llm-observations-freeze.json')
    check('model_observations_usage_unchanged',all(sha(OUT/p)==h for p,h in observations['hashes'].items()))
    llm=load(OUT/'llm-results.json')['responses'];holdout=load(ROOT/'validation/fixtures/phase2-1/holdout-v1.json')['cases'];reviews=load(OUT/'llm-semantic-review.json')['reviews'];stored=load(OUT/'llm-review.json')
    score_rows=[];over=dim=exact=quotes=0
    for c in holdout:
        r=next(x for x in llm if x['id']==c['id']);choice=r['raw_response']['choices'][0];content=choice['message']['content'];a=json.loads(content)
        v=judge21(content,c,reviews[c['id']],choice.get('finish_reason'),choice['message'].get('tool_calls'))
        score_rows.append(v==next(x for x in stored['observations'] if x['id']==c['id'])['verdict'] and reviews[c['id']]['content_sha256']==content_hash(content))
        over+=sum(x==y for x,y in zip(v['observed_overall'],c['expected']['overall']));dim+=sum(v['dimension_matches']);q=citation_audit(a,c['sources']);quotes+=len(q);exact+=sum(x['exact'] for x in q)
    check('external_scoring_review_bindings_reproduce',len(llm)==len(holdout)==12 and len({r['id'] for r in llm})==12 and all(score_rows))
    check('external_metric_arithmetic_recalculate',stored['summary']['overall_labels']==dict(matched=over,total=24) and stored['summary']['effective_dimensions']==dict(matched=dim,total=144) and stored['summary']['literal_quotes']==dict(matched=exact,total=quotes))
    check('no_private_reasoning_in_new_envelopes',all('reasoning_content' not in r['raw_response']['choices'][0]['message'] and r['raw_response']['sanitization']['final_content_unchanged'] is True for r in llm))
    plan=load(OUT/'llm-plan.json')['requests']
    check('synthetic_plan_no_tools_or_oracle_leak',all('tools' not in r['payload'] and 'expected' not in json.loads(r['payload']['messages'][1]['content']) and json.loads(r['payload']['messages'][1]['content'])['synthetic_only'] is True for r in plan))
    attempts=load(OUT/'llm-execution.json')['attempts'];cost=load(OUT/'llm-cost.json');amount=Decimal(0);usage=dict(prompt_tokens=0,completion_tokens=0,total_tokens=0,reasoning_tokens=0)
    for a in attempts:
        u=a['usage'];hit=u.get('prompt_cache_hit_tokens',0);miss=u.get('prompt_cache_miss_tokens',u['prompt_tokens']-hit)
        if hit+miss!=u['prompt_tokens']:raise ValueError('Provider cache arithmetic mismatch')
        amount+=(Decimal(hit)*Decimal('.006')+Decimal(miss)*Decimal('.30')+Decimal(u['completion_tokens'])*Decimal('1.20'))/Decimal(1000000)
        for k in ('prompt_tokens','completion_tokens','total_tokens'):usage[k]+=u[k]
        usage['reasoning_tokens']+=u.get('completion_tokens_details',{}).get('reasoning_tokens',0)
    check('usage_cost_budget_recalculate',usage==cost['reported_usage'] and abs(amount-Decimal(str(cost['estimated_peak_usd'])))<Decimal('0.000000000001') and len(attempts)<=12 and Decimal(str(cost['budget_accounted_usd']))<=Decimal('.30') and freeze['conservative_ceiling_usd']<=.30)
    check('model_identity_is_public_alias_only',all(a.get('returned_model')==r['raw_response'].get('model')=='deepseek-flash' for a,r in zip(attempts,llm)) and freeze['backend_independently_attested'] is False)
    gates=load(OUT/'gates.json')
    check('gates_keep_strict_failure_and_runtime_unknown',gates['gates']['P21-G4']['status']=='PARTIAL' and gates['gates']['P21-G5']['status']==gates['gates']['P21-G6']['status']=='NOT_RUN' and gates['final_candidate_external_retest']=='NOT_RUN' and gates['engineering_status']=='PARTIAL')
    selected=[]
    for folder in ['rightsgap-media-reuse','validation/fixtures/phase2-1','validation/results/phase2-1','review-phase21']:
        if (ROOT/folder).exists():selected += [p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ('.py','.json','.md','.txt','.patch')]
    selected += list((ROOT/'validation').glob('*phase21*.py'))+[ROOT/'validation/effective_assessment.py',ROOT/'.gitattributes']
    selected += [ROOT/'docs'/n for n in ['17-phase2-1-evidence-integrity-report.md','18-phase2-1-validation-report.md']]+[ROOT/'PHASE21_REVIEW.md']
    selected=[p for p in selected if p.exists() and '__pycache__' not in p.parts]
    patterns=[rb'\bAKIA[0-9A-Z]{16}\b',rb'\bgh[pousr]_[A-Za-z0-9_]{20,}\b',rb'\bgithub_pat_[A-Za-z0-9_]{20,}\b',rb'\bsk-[A-Za-z0-9]{32,}\b',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    check('common_credential_patterns_absent',not any(re.search(rx,p.read_bytes()) for p in selected for rx in patterns))
    key=os.environ.get('DEEPSEEK_API_KEY','').strip().encode();secret=dict(state='NOT_RUN',reason='No exact process secret available; ordinary audit remains credential-free') if not key else dict(state='PASS' if not any(key in p.read_bytes() for p in selected) else 'FAIL',reason='Exact value checked without output/persistence')
    links=[]
    for p in [ROOT/'PHASE21_REVIEW.md',ROOT/'docs/17-phase2-1-evidence-integrity-report.md',ROOT/'docs/18-phase2-1-validation-report.md']+list((ROOT/'rightsgap-media-reuse').rglob('*.md')):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if not target.startswith(('http://','https://','#')):links.append((p.parent/target.split('#',1)[0]).is_file())
    check('current_markdown_links_resolve',all(links),str(len(links))+' local file links')
    value=dict(status='PASS' if all(c['state']=='PASS' for c in checks) and secret['state']!='FAIL' else 'FAIL',checks=checks,
        passed=sum(c['state']=='PASS' for c in checks),total=len(checks),protected_present_checked=len(protected),changed_protected=changed,declared_archive_omissions=missing,
        global_unique_assertions=len(ids),exact_secret_scan=secret,recalculated_peak_usd=str(amount),
        scope='Ordinary offline integrity audit; semantic reviews checked for binding/consistency, not independently rejudged',
        limitations=['No model/NAS requests','Full workspace history is verified only when present; ZIP omissions are explicit','Current v2 external inference NOT_RUN; original v1 strict 3/12 retained'])
    output.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({k:value[k] for k in ['status','passed','total','protected_present_checked','global_unique_assertions','exact_secret_scan']},indent=2));raise SystemExit(0 if value['status']=='PASS' else 1)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=OUT/'audit.json');args=p.parse_args()
    if not args.output.resolve().is_relative_to(OUT):raise SystemExit('Refusing historical/outside output')
    main(args.output)
