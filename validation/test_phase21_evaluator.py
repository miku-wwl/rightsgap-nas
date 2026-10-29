"""Adversarial offline controls for the frozen effective-answer evaluator."""
import copy
import json
from pathlib import Path

from evaluate_phase21 import judge21, ADDED
from phase21_holdout import build
from strict_evaluation import MANUAL,content_hash

OUT=Path(__file__).resolve().parent/'results/phase2-1'


def positive_answer(case):
    s=case['sources'][0];q=s['clauses'][0]
    cite=dict(source=s['path'],clause_id=q['id'],quote=q['text'],page=None)
    row=dict(status='CONSISTENT_EVIDENCE',dimensions={d:dict(status='CONSISTENT_EVIDENCE',evidence=[copy.deepcopy(cite)],explanation='Exact synthetic source grants the stated dimension within its conditions.',uncertainty=[]) for d in case['expected']['dimensions'][0]})
    a=dict(asset_id=case['asset_id'],licensed_party=case['licensed_party'],scenario_A=copy.deepcopy(row),scenario_B=copy.deepcopy(row),
        observed_evidence=[{**cite,'observation':'The clause directly states the named asset, beneficiary and use terms.','limitations':['Synthetic text; actual legal authenticity unknown.']}],
        input_delta=[dict(dimension=d,**v) for d,v in case['expected']['input_delta'].items()],
        evidence_status_delta=[],proof_delta=[],amendment_reasoning=[],uncertainty=['Actual legal authenticity/enforceability UNKNOWN.'],
        scope_receipt=dict(source_revision=case['user']['source_revision'],read_complete=[s['path']],unavailable=[],dependency_dimensions=[],exclusions=[]),
        human_review_questions=[],human_review='PENDING',save_requested=False,operations=[])
    for d in case['expected']['input_delta']:
        a['evidence_status_delta'].append(dict(dimension=d,status_A='CONSISTENT_EVIDENCE',status_B='CONSISTENT_EVIDENCE',status_changed=False))
        a['proof_delta'].append(dict(dimension=d,status_A='CONSISTENT_EVIDENCE',status_B='CONSISTENT_EVIDENCE',evidence_A=[copy.deepcopy(cite)],evidence_B=[copy.deepcopy(cite)],explanation='The same quoted grant covers both changed inputs.',uncertainty=[]))
    return a


def review(content):
    return dict(content_sha256=content_hash(content),reviewer='Curated evaluator control; not actual model or human review',checks=dict.fromkeys([*MANUAL,*ADDED],True),
        unsupported_citation_paths=[],semantic_unsafe_positive_cells=[],all_quotation_occurrences_reviewed=True)


def main():
    base=build()[0];original=positive_answer(base);rows=[]
    for name in ['complete_positive','missing_review','null_semantics','missing_observations','missing_scope','false_human_approval','irrelevant_positive_quote','W04_overall_only_mask','narrow_scope_overblocked']:
        case=copy.deepcopy(base);a=copy.deepcopy(original);missing=False
        if name=='missing_review':missing=True
        elif name=='missing_observations':a.pop('observed_evidence')
        elif name=='missing_scope':a.pop('scope_receipt')
        elif name=='false_human_approval':a['human_review']='APPROVED'
        elif name=='irrelevant_positive_quote':a['scenario_A']['dimensions']['asset_identity']['evidence'][0]['quote']='across the world'
        elif name=='W04_overall_only_mask':
            case=copy.deepcopy(build()[1]);a['asset_id']=case['asset_id'];a['scenario_A']['status']=a['scenario_B']['status']='UNASSESSED'
        elif name=='narrow_scope_overblocked':
            case=copy.deepcopy(build()[-1]);a['asset_id']=case['asset_id']
            for n in ('scenario_A','scenario_B'):
                a[n]['status']='UNASSESSED'
                for c in a[n]['dimensions'].values():c['status']='UNASSESSED'
        content=json.dumps(a);r=None if missing else review(content)
        if name=='null_semantics':r['checks']['cross_dimension_propagation']=None
        if name=='irrelevant_positive_quote':
            r['checks']['citation_semantics']=False;r['unsupported_citation_paths']=['answer.scenario_A.dimensions.asset_identity.evidence[0]']
        v=judge21(content,case,r)
        wanted=name=='complete_positive'
        passed=v['strict_accepted']==wanted
        if name=='irrelevant_positive_quote':passed&=v['checks']['quotation_fidelity']['state']=='PASS'
        if name=='W04_overall_only_mask':passed&=not v['checks']['cross_dimension_dependency_safety']['state']=='PASS'
        rows.append(dict(id='p21-evaluator/'+name,passed=passed,expected_acceptance=wanted,actual_acceptance=v['strict_accepted'],blocked=v['blocked_checks']))
    result=dict(status='PASS' if all(r['passed'] for r in rows) else 'FAIL',passed=sum(r['passed'] for r in rows),total=len(rows),assertions=rows,
        scope='Adversarial evaluator controls, not model observations')
    (OUT/'evaluator-controls.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)


if __name__=='__main__':main()
