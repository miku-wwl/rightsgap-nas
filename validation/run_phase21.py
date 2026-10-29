"""Execute frozen Phase 2.1 integrity cases and meaningful mutations offline."""
import copy
import hashlib
import json
from pathlib import Path

from effective_assessment import compare_effective, evaluate
from phase21_cases import grant, amendment, add_restriction, reviewed
from reference_policy import DIMENSIONS, POSITIVE as C, CONFLICT as X, UNASSESSED as U

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/phase2-1'


def main():
    folder=ROOT/'fixtures/phase2-1'
    raw=(folder/'deterministic-v1.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=json.loads((folder/'freeze.json').read_text(encoding='utf-8'))['sha256']:
        raise SystemExit('Frozen expectations changed')
    cases=json.loads(raw)['cases']
    checks=[];ids=set();results={}
    def check(identifier, condition, detail=None):
        identifier='p21/'+identifier
        if identifier in ids: raise ValueError('Duplicate assertion '+identifier)
        ids.add(identifier);checks.append(dict(id=identifier,passed=condition is True,detail=detail))
    for case in cases:
        report=compare_effective(case);rows=report['assessments'];prefix=case['id']
        for i,row in enumerate(rows):
            check(prefix+f'/overall/{i}',row['status']==case['expected']['overall'][i],dict(expected=case['expected']['overall'][i],actual=row['status']))
            for d,wanted in case['expected']['dimensions'][i].items():
                cell=row['dimensions'][d]
                check(prefix+f'/effective/{i}/{d}',cell['status']==wanted,dict(expected=wanted,actual=cell['status']))
                check(prefix+f'/no_unsafe_positive/{i}/{d}',cell['status']!=C or wanted==C)
                if cell['status']==C:
                    check(prefix+f'/substantive_quote/{i}/{d}',bool(cell['support']) and all(c.get('claim_review_basis') and c['quote'] for c in cell['support']))
            check(prefix+f'/no_operations/{i}',row['operations']==[] and row['saving']=='DISABLED')
            check(prefix+f'/observations_are_facts/{i}',all(o['classification']=='OBSERVATION_ONLY' for o in row['observed_evidence']))
            check(prefix+f'/preserve_known_quote/{i}',any(o['quote']==case['documents'][0]['findings'][0]['quote'] for o in row['observed_evidence']))
            if prefix in ('P21-B','P21-D'):
                check(prefix+f'/W04_all_six_blocked/{i}',all(c['status']==U for c in row['dimensions'].values()) and bool(row['observed_evidence']))
            if prefix=='P21-C':check(prefix+f'/documentary_exclusion/{i}',bool(row['exclusions']) and not row['dependency_blockers'])
            if prefix=='P21-L':check(prefix+f'/narrow_channel_dependency/{i}',set(row['dependency_blockers'])=={'channel'} and sum(c['status']==C for c in row['dimensions'].values())==5)
        required={d for d,k in {'purpose':'purpose','channel':'channel','territory':'territory','time_window':'date'}.items() if case['scenarios'][0][k]!=case['scenarios'][1][k]}
        for layer in ('input_delta','evidence_status_delta','proof_delta'):
            check(prefix+'/'+layer,{r['dimension'] for r in report['delta'][layer]}==required)
        check(prefix+'/pending_human_review',all(r['human_review']=='PENDING' for r in rows))
        results[prefix]=dict(category=case['category'],expected=case['expected'],actual=report)
    base=copy.deepcopy(cases[0]);mutations={}
    for name in ('remove_evidence','reduce_coverage','add_cross_cutting_dependency','unrelated_amendment_preserves_R1','change_source_path','irrelevant_substring','irrelevant_truncation_preserves_unaffected_dimensions'):
        c=copy.deepcopy(base)
        if name=='remove_evidence':
            c['documents'][0]['text']='';c['documents'][0]['context']=''
        elif name=='reduce_coverage':c['documents'][0]['coverage_complete']=False
        elif name=='add_cross_cutting_dependency':
            p='synthetic/p21/licenses/new-unread-source.pdf';c['selected_documents'].append(p)
        elif name=='unrelated_amendment_preserves_R1':
            c=copy.deepcopy(next(x for x in cases if x['id']=='P21-F'))
            # A separate amendment targets purpose, never independent R1.
            extra=amendment(c['asset'],dimensions=['purpose'],identifier='UNRELATED')
            c['documents'].append(extra);c['selected_documents'].append(extra['path']);reviewed(c)
        elif name=='change_source_path':
            new='synthetic/p21/licenses/unestablished-new-path.pdf';c['documents'][0]['path']=new;c['selected_documents']=[new]
        elif name=='irrelevant_substring':c['documents'][0]['findings'][0]['claim_spans']={'licensed_party':'worldwide including Canada'}
        else:c=copy.deepcopy(next(x for x in cases if x['id']=='P21-C'))
        r=evaluate(c,c['scenarios'][1]);positive={d for d,x in r['dimensions'].items() if x['status']==C}
        if name=='unrelated_amendment_preserves_R1':
            ok=r['dimensions']['channel']['status']==X and bool(r['observed_conflicts'].get('channel'))
        elif name=='irrelevant_truncation_preserves_unaffected_dimensions':ok=positive==set(DIMENSIONS) and r['status']==C
        elif name=='irrelevant_substring':ok=r['dimensions']['licensed_party']['status']==U
        else:ok=not positive
        check('metamorphic/'+name,ok,dict(overall=r['status'],positive_dimensions=sorted(positive)))
        mutations[name]=r
    # Genuine observed prohibition survives even when its effective outcome is
    # blocked by a separate potentially cross-cutting unread source.
    c=copy.deepcopy(next(x for x in cases if x['id']=='P21-F'))
    p='synthetic/p21/licenses/unknown-supersession.pdf';c['selected_documents'].append(p)
    r=evaluate(c,c['scenarios'][1])
    check('controls/observed_conflict_retained',r['status']==U and bool(r['observed_conflicts'].get('channel')) and r['dimensions']['channel']['status']==U)
    # A claim that a proof exists cannot replace the independent scope review.
    c=copy.deepcopy(next(x for x in cases if x['id']=='P21-C'));c['scope_reviews']={}
    r=evaluate(c,c['scenarios'][0]);check('controls/unreviewed_scope_claim',all(x['status']==U for x in r['dimensions'].values()))
    c=copy.deepcopy(next(x for x in cases if x['id']=='P21-L'));c['scope_proofs'][0]['affected_dimensions']=[]
    r=evaluate(c,c['scenarios'][0]);check('controls/altered_narrowing_proof',all(x['status']==U for x in r['dimensions'].values()))
    for state in ('failed','cancelled','waiting_user','waiting_approval','unknown','missing','empty','partial'):
        c=copy.deepcopy(base);c['documents'][0]['state']=state
        r=evaluate(c,c['scenarios'][0]);check('controls/state/'+state,r['status']==U and all(x['status']==U for x in r['dimensions'].values()) and r['operations']==[])
    literal_case=next(x for x in cases if x['id']=='P21-I');fact=literal_case['documents'][0]['findings'][0]
    check('controls/literal_membership_is_not_semantics',fact['claim_spans']['asset_identity'] in fact['quote'] and results['P21-I']['actual']['assessments'][0]['dimensions']['asset_identity']['status']==U)
    # Legacy complete-scope behavior must agree for the original 72 cells.
    from clause_fixtures import load_baseline,review_ledger
    from reference_policy import assess
    corpus=load_baseline()
    for asset in corpus['assets']:
        asset_id=asset if isinstance(asset,str) else asset['id']
        legacy_docs=copy.deepcopy(corpus['documents'])
        # The old corpus passed completeness as a call flag, rather than per
        # source metadata. Supply that same explicit premise to this adapter.
        for doc in legacy_docs:
            doc.update(state='completed',coverage_complete=True,context=doc['text'])
        c=dict(asset=asset_id,authorized_roots=['synthetic/licenses'],selected_documents=[d['path'] for d in legacy_docs],documents=legacy_docs,
            source_revision='legacy-complete',association_established=True,scope_proofs=[],scope_reviews={})
        reviewed(c)
        for n,s in enumerate(corpus['scenarios']):
            old=assess(asset_id,s,corpus['documents'],coverage=True,reviews=review_ledger(corpus['documents']))
            new=evaluate(c,s)
            check(f'legacy-complete/{asset_id}/{n}/overall',new['status']==old['status'])
            check(f'legacy-complete/{asset_id}/{n}/dimensions',[v['status'] for v in new['dimensions'].values()]==[v['status'] for v in old['dimensions'].values()])
    failures=[c for c in checks if not c['passed']]
    output=dict(layer='CURATED OFFLINE EFFECTIVE-ASSESSMENT; NOT ULIYA/NAS',fixture_sha256=hashlib.sha256(raw).hexdigest(),cases=results,
        case_count=len(cases),metamorphic_results=mutations,metamorphic_count=len(mutations),
        assertions=checks,checks=dict(passed=len(checks)-len(failures),total=len(checks),failed=len(failures),unique_ids=len(ids)),failures=failures)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'deterministic.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(checks=output['checks'],failures=failures),indent=2))
    raise SystemExit(1 if failures else 0)


if __name__=='__main__':main()
