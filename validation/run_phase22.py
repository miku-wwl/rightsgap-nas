"""Exercise frozen Phase 2.2 sources, contrasts and rejection controls offline."""
import copy
from phase22_common import OUT, save, verify_freeze, now
from report_contract import compare22, check_scope, input_delta, question_shape, D, C


def main():
    cases=verify_freeze('deterministic-v1.json')['cases']; checks=[]; results={}; ids=set()
    def check(name,ok,detail=None):
        identifier='p22/'+name
        if identifier in ids: raise ValueError('Duplicate assertion ID')
        ids.add(identifier); checks.append(dict(id=identifier,passed=ok is True,detail=detail))
    for case in cases:
        report=compare22(case); results[case['id']]=report; prefix=case['id']
        rows=report['assessments']
        for i,row in enumerate(rows):
            check(f'{prefix}/overall/{i}',row['status']==case['expected']['overall'][i],dict(expected=case['expected']['overall'][i],actual=row['status']))
            for d in D:
                actual=row['dimensions'][d]['status']; expected=case['expected']['dimensions'][i][d]
                check(f'{prefix}/dimension/{i}/{d}',actual==expected,dict(expected=expected,actual=actual))
                if actual==C:
                    evidence=row['dimensions'][d]['support']
                    check(f'{prefix}/substantive_citation/{i}/{d}',bool(evidence) and all(c.get('claim_review_basis') and c['quote'] in next(doc['text'] for doc in case['documents'] if doc['path']==c['source']) for c in evidence))
            check(f'{prefix}/observations/{i}',bool(row['observed_evidence']) and all(o['classification']=='OBSERVATION_ONLY' for o in row['observed_evidence']))
        check(prefix+'/input_delta_exact',report['input_delta']==case['expected']['input_delta'])
        input_dims={r['dimension'] for r in case['expected']['input_delta']}
        status_dims={d for d in D if case['expected']['dimensions'][0][d]!=case['expected']['dimensions'][1][d]}
        union=input_dims|status_dims
        for key in ('evidence_status_delta','proof_delta'):
            check(prefix+'/'+key+'/coverage',{r['dimension'] for r in report[key]}==union and len(report[key])==len(union))
            check(prefix+'/'+key+'/flags',all(r['input_changed']==(r['dimension'] in input_dims) and r['status_changed']==(r['dimension'] in status_dims) for r in report[key]))
        receipt=report['scope_receipt']
        check(prefix+'/literal_paths',receipt['selected_sources']==case['selected_documents'] and {s['path'] for s in receipt['source_states']}==set(case['selected_documents']))
        check(prefix+'/no_unauthorized_source',set(receipt['actually_read_sources']+receipt['unavailable_selected_sources'])<=set(case['selected_documents']))
        check(prefix+'/separate_scenario_dimension',all(r['dimension'] in D and r['scenario'] in ('A','B') for r in receipt['dependencies']))
        check(prefix+'/no_operations',report['operations']==[] and report['saving']=='DISABLED' and report['human_review']=='PENDING')
        blocked={(s,d) for s,i in [('A',0),('B',1)] for d in D if case['expected']['dimensions'][i][d]!=C}
        check(prefix+'/repair_questions',all(question_shape(q) for q in report['human_review_questions']) and blocked<={(q['scenario'],q['dimension']) for q in report['human_review_questions']})
        if case['untrusted_evidence']:
            check(prefix+'/attack_preserved',receipt['untrusted_references']==case['untrusted_evidence'] and all(x['quote'] in next(d['text'] for d in case['documents'] if d['path']==x['source']) for x in receipt['untrusted_references']))
        if case['category']=='cross-cutting':
            check(prefix+'/W04_no_overall_mask',all(c['status']=='UNASSESSED' for row in rows for c in row['dimensions'].values()))
        if case['category']=='partial-amendment':
            check(prefix+'/B01_R1_preserved',bool(rows[1]['observed_conflicts'].get('channel')) and rows[1]['dimensions']['channel']['status']=='EXPLICIT_CONFLICT')
        if case['category']=='scope-narrowing':
            check(prefix+'/narrowing_has_source_proof',all(set(row['dependency_blockers'])=={'channel'} and row['dependency_blockers']['channel'][0]['narrowing_proof']['quote'] for row in rows))
    # Direct contrast tests operate on frozen scenario inputs, not on model text.
    same=results['P22-S07']; stable=results['P22-S08']; indirect=results['P22-Q03']
    check('contrast/no_input_or_status_change',same['input_delta']==same['evidence_status_delta']==same['proof_delta']==[])
    check('contrast/input_change_without_status_change',len(stable['input_delta'])==1 and all(not r['status_changed'] for r in stable['evidence_status_delta']))
    check('contrast/dependent_status_without_input_change',indirect['input_delta'][0]['dimension']=='channel' and len(indirect['input_delta'])==1 and any(r['dimension']=='purpose' and r['status_changed'] and not r['input_changed'] for r in indirect['evidence_status_delta']))
    pair=copy.deepcopy(cases[0]['scenarios']); pair[1]['licensee']='SeparateParty'
    check('contrast/variable_party_explicit',sum(r['dimension']=='licensed_party' for r in input_delta(pair,variable_party=True))==1)
    rejected=False
    try: input_delta(pair)
    except ValueError: rejected=True
    check('contrast/fixed_party_boundary',rejected)
    # Scope mutations must be rejected as-is, never fixed before scoring.
    truth=results['P22-S02']['scope_receipt']
    for name in ['path-annotation','scenario-qualified-dimension','outside-selected','outside-unavailable','read-complete-lie','missing-state','revision-in-path','duplicate-path','lost-attack']:
        expected=copy.deepcopy(truth); changed=copy.deepcopy(expected)
        if name=='path-annotation': changed['selected_sources'][0]+=' (state=truncated)'
        elif name=='scenario-qualified-dimension': changed['dependencies'][0]['dimension']='scenario_B.channel'
        elif name=='outside-selected': changed['selected_sources'].append('synthetic/private/payroll.txt')
        elif name=='outside-unavailable': changed['unavailable_selected_sources'].append('synthetic/private/payroll.txt')
        elif name=='read-complete-lie': changed['source_states'][1]['completeness']='complete'
        elif name=='missing-state': changed['source_states'][0].pop('state')
        elif name=='revision-in-path': changed['source_states'][0]['path']+=' @p22-frozen-r1'
        elif name=='duplicate-path': changed['source_states'].append(copy.deepcopy(changed['source_states'][0]))
        else:
            expected=results['P22-I01']['scope_receipt']; changed=copy.deepcopy(expected); changed['untrusted_references']=[]
        check('scope-rejection/'+name,not check_scope(changed,expected))
    # Read status is not the source identity; incomplete selected source can be read.
    c=copy.deepcopy(cases[1]); c['documents'][1]['context']=c['documents'][1]['text']
    r=compare22(c)['scope_receipt']; p=c['documents'][1]['path']
    check('scope/partial-read-still-unavailable',p in r['actually_read_sources'] and p in r['unavailable_selected_sources'])
    for state in ['failed','cancelled','waiting_user','waiting_approval','missing','partial','truncated','unknown','empty']:
        c=copy.deepcopy(cases[0]); c['documents'][0]['state']=state
        r=compare22(c)
        check('state/'+state,all(cell['status']=='UNASSESSED' for row in r['assessments'] for cell in row['dimensions'].values()) and r['operations']==[])
    c=copy.deepcopy(cases[0]); c['documents'][0]['denied']=True
    r=compare22(c)
    check('state/denied-approval-no-bypass',r['scope_receipt']['source_states'][0]['access_error']=='denied' and all(row['status']=='UNASSESSED' for row in r['assessments']) and r['operations']==[])
    q=results['P22-S02']['human_review_questions'][0]
    for name,text in [('assurance','Please confirm that no other restrictions apply.'),('alternative','Provide text or simply confirm it has no effect.'),('approval','Human approval replaces source completeness; no document is needed.')]:
        bad=copy.deepcopy(q); bad['requested_evidence']=text
        check('question-rejection/'+name,not question_shape(bad))
    for field in ('missing','dimension','requested_evidence','remaining_unknown'):
        bad=copy.deepcopy(q); bad.pop(field)
        check('question-rejection/missing-'+field,not question_shape(bad))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',recorded_at=now(),
        layer='DETERMINISTIC CURATED LOCAL ORACLE; NOT MARKDOWN/MODEL/ULIYA/NAS EXECUTION',
        cases=results,case_count=len(cases),assertions=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
        failures=[c for c in checks if not c['passed']],human_review='NOT_RUN')
    destination=OUT/'deterministic.json'
    if destination.exists() and load_failed(destination):
        save(OUT/('deterministic-retained-'+str(len(list(OUT.glob('deterministic-retained-*')))+1)+'.json'),__import__('json').loads(destination.read_text(encoding='utf-8')))
    save(destination,result)
    print(__import__('json').dumps({k:result[k] for k in ('status','case_count','passed','total','failures')}))
    raise SystemExit(0 if result['status']=='PASS' else 1)


def load_failed(path):
    return __import__('json').loads(path.read_text(encoding='utf-8')).get('status')!='PASS'


if __name__=='__main__': main()
