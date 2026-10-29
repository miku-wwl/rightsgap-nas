"""Frozen Phase 2.1 evaluator; stored final content only, no API operations.

Literal checks and hash-bound agent semantic reviews are separate. Neither is
an independent human review or an entailment guarantee for arbitrary language.
"""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

from strict_evaluation import judge, accept, citation_audit, content_hash, DIMS, PASS, FAIL, NOT_RUN

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'validation/results/phase2-1'
FIX=ROOT/'validation/fixtures/phase2-1'
ADDED=('observed_preservation','cross_dimension_propagation','questions_accuracy','scope_accuracy')


def load(path):return json.loads(path.read_text(encoding='utf-8'))


def judge21(content,case,review=None,finish_reason='stop',tool_calls=None):
    result=judge(content,case,review,finish_reason=finish_reason,tool_calls=tool_calls)
    try:a=json.loads(content)
    except (TypeError,ValueError):a={}
    a=a if isinstance(a,dict) else {}
    def add(name,ok,reason):
        result['checks'][name]=dict(state=PASS if ok is True else FAIL,reason=reason)
        result['requirements'][name]=dict(requested=True,applicable=True)
    obs=a.get('observed_evidence');obs=obs if isinstance(obs,list) else []
    required=case.get('observed_required_citations',[])
    pairs={(o.get('source'),o.get('clause_id')) for o in obs if isinstance(o,dict)}
    add('observed_evidence_contract',bool(obs) and all(isinstance(o,dict) and isinstance(o.get('quote'),str) and bool(o['quote'].strip())
        and isinstance(o.get('source'),str) and isinstance(o.get('clause_id'),str) and isinstance(o.get('observation'),str) and bool(o['observation'].strip())
        and isinstance(o.get('limitations'),list) and o.get('status') not in ('CONSISTENT_EVIDENCE','EXPLICIT_CONFLICT','GAP_IN_CHECKED_SCOPE','AMBIGUOUS_EVIDENCE','UNASSESSED') for o in obs)
        and all(tuple(p) in pairs for p in required),'Separate factual observations with actual quotes; preserve each material source')
    scope=a.get('scope_receipt');scope=scope if isinstance(scope,dict) else {}
    complete={s['path'] for s in case['sources'] if s.get('context_available') is True and s.get('coverage_complete') is True and s.get('state')=='completed'}
    unavailable={s['path'] for s in case['sources']}-complete
    string_list=lambda value:isinstance(value,list) and all(isinstance(v,str) for v in value) and len(value)==len(set(value))
    add('scope_receipt_contract',scope.get('source_revision')==case['user']['source_revision'] and string_list(scope.get('read_complete')) and set(scope['read_complete'])==complete
        and string_list(scope.get('unavailable')) and set(scope['unavailable'])==unavailable
        and string_list(scope.get('dependency_dimensions')) and set(scope['dependency_dimensions'])<=set(DIMS)
        and set(case.get('effective_dependency_dimensions',[]))<=set(scope['dependency_dimensions']) and isinstance(scope.get('exclusions'),list),
        'Actual supplied availability and dependencies; no invented complete selected-corpus claim')
    unsafe=[]
    for i,name in enumerate(('scenario_A','scenario_B')):
        row=a.get(name);row=row if isinstance(row,dict) else {};cells=row.get('dimensions');cells=cells if isinstance(cells,dict) else {}
        for d,w in case['expected']['dimensions'][i].items():
            cell=cells.get(d);cell=cell if isinstance(cell,dict) else {}
            if cell.get('status')=='CONSISTENT_EVIDENCE' and w!='CONSISTENT_EVIDENCE':unsafe.append(name+'.dimensions.'+d)
    add('no_unsupported_effective_positive',not unsafe,'Positive labels cannot escape the frozen effective applicability/dependency contract')
    blocked=case.get('effective_dependency_dimensions',[])
    dependencies_safe=all(not isinstance(a.get(n),dict) or not isinstance(a[n].get('dimensions'),dict) or all(
        not isinstance(a[n]['dimensions'].get(d),dict) or a[n]['dimensions'][d].get('status')!='CONSISTENT_EVIDENCE' for d in blocked) for n in ('scenario_A','scenario_B'))
    add('cross_dimension_dependency_safety',dependencies_safe,'Unavailable or unjoined dependent dimensions cannot become effective positives')
    questions=a.get('human_review_questions')
    add('human_review_contract',a.get('human_review')=='PENDING' and isinstance(questions,list) and (
        all(w=='CONSISTENT_EVIDENCE' for w in case['expected']['overall']) or bool(questions)),
        'No invented human review; unresolved judgments require human repair questions')
    bound=isinstance(review,dict) and review.get('content_sha256')==content_hash(content)
    for name in ADDED:
        add('manual_'+name,bound and review.get('checks',{}).get(name) is True,'Separate content-bound semantic review required')
    bad=review.get('unsupported_citation_paths',[]) if bound else None
    semantic_unsafe=review.get('semantic_unsafe_positive_cells',[]) if bound else None
    add('reviewed_positive_citation_integrity',isinstance(bad,list) and not bad,'No reviewed unsupported positive citation may be accepted')
    add('reviewed_effective_safety',isinstance(semantic_unsafe,list) and not semantic_unsafe,'Semantic false affirmatives block acceptance even if literal labels match')
    result.update(accept(result['checks'],result['requirements']))
    result.update(version='phase21-effective-strict-v1',unsafe_positive_cells=unsafe,
        semantic_unsafe_positive_cells=semantic_unsafe,unsupported_citation_paths=bad)
    return result


def inspect(identifier):
    case=next(c for c in load(FIX/'holdout-v1.json')['cases'] if c['id']==identifier)
    result=next((r for r in load(OUT/'llm-results.json')['responses'] if r['id']==identifier),None)
    if not result or not result.get('raw_response'):raise SystemExit('Observation not available; no request sent')
    print('USER',json.dumps(case['user']))
    content=result['raw_response']['choices'][0]['message']['content']
    try:answer=json.loads(content)
    except ValueError:print('FINAL_CONTENT',content);return
    quotes={}
    def compact(v):
        if isinstance(v,dict):
            if 'quote' in v:
                k=(v.get('source'),v.get('clause_id'),v['quote'],v.get('page'));quotes.setdefault(k,'Q'+str(len(quotes)+1))
                return {'ref':quotes[k],**{key:compact(value) for key,value in v.items() if key not in ('source','clause_id','quote','page')}}
            return {k:compact(x) for k,x in v.items()}
        return [compact(x) for x in v] if isinstance(v,list) else v
    print('FINAL',json.dumps(compact(answer)))
    print('QUOTES',json.dumps([dict(ref=v,source=k[0],clause_id=k[1],quote=k[2],page=k[3]) for k,v in quotes.items()]))


def score():
    freeze=load(OUT/'llm-freeze.json')
    for p,h in {**freeze['hashes'],**freeze['candidate_sha256']}.items():
        if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise SystemExit('Frozen study changed: '+p)
    cases=load(FIX/'holdout-v1.json')['cases'];raw=load(OUT/'llm-results.json')['responses']
    if len(raw)!=len({r['id'] for r in raw}):raise ValueError('Duplicate observation ID')
    reviews=load(OUT/'llm-semantic-review.json')['reviews'] if (OUT/'llm-semantic-review.json').exists() else {}
    rows=[]
    for case in cases:
        r=next((x for x in raw if x['id']==case['id']),None)
        if not r or r['api_status']!='SUCCESS':rows.append(dict(id=case['id'],state='NOT_RUN',strict_accepted=False));continue
        choice=r['raw_response']['choices'][0];content=choice['message']['content'];review=reviews.get(case['id'])
        verdict=judge21(content,case,review,choice.get('finish_reason'),choice['message'].get('tool_calls'))
        try:a=json.loads(content)
        except ValueError:a={}
        a=a if isinstance(a,dict) else {}
        quotes=citation_audit(a,case['sources']);bad=verdict['unsupported_citation_paths'];semantic_unsafe=verdict['semantic_unsafe_positive_cells']
        reviewed=bool(review and review.get('content_sha256')==content_hash(content) and review.get('all_quotation_occurrences_reviewed') is True)
        if reviewed and set(bad or [])-{q['path'] for q in quotes}:raise ValueError('Semantic issue path absent from final citations')
        rows.append(dict(id=case['id'],state='PASS' if verdict['strict_accepted'] else 'FAIL',strict_accepted=verdict['strict_accepted'],
            verdict=verdict,content_sha256=content_hash(content),
            overall_matches=sum(x==y for x,y in zip(verdict['observed_overall'],case['expected']['overall'])),dimension_matches=sum(verdict['dimension_matches']),
            quotation_occurrences=len(quotes),exact_quotes=sum(q['exact'] for q in quotes),
            semantic_quote_reviewed_occurrences=len(quotes) if reviewed else 0,
            semantically_supported_occurrences=len(quotes)-len(bad or []) if reviewed else None,
            unsafe_positive_cells=sorted(set(verdict['unsafe_positive_cells']+(semantic_unsafe or []))),
            unsupported_citation_paths=bad,review_notes=review.get('notes',[]) if review else [],elapsed_seconds=r['elapsed_seconds']))
    done=[r for r in rows if r['state']!='NOT_RUN'];metric=lambda k:sum(r[k] for r in done)
    passed=lambda k:sum(r['verdict']['checks'][k]['state']=='PASS' for r in done)
    lat=[r['elapsed_seconds'] for r in done]
    summary=dict(requested_cases=len(cases),executed_cases=len(done),strict_accepted=sum(r['strict_accepted'] for r in done),strict_total=len(cases),
        overall_labels=dict(matched=metric('overall_matches'),total=2*len(done)),effective_dimensions=dict(matched=metric('dimension_matches'),total=12*len(done)),
        literal_quotes=dict(matched=metric('exact_quotes'),total=metric('quotation_occurrences')),
        semantic_quotes=dict(supported=sum(r['semantically_supported_occurrences'] or 0 for r in done),reviewed=metric('semantic_quote_reviewed_occurrences'),total=metric('quotation_occurrences')),
        unsafe_positive_dimensions=sum(len(r['unsafe_positive_cells']) for r in done),unsupported_positive_citation_occurrences=sum(len(r['unsupported_citation_paths'] or []) for r in done),
        accepted_unsupported_citations=sum(len(r['unsupported_citation_paths'] or []) for r in done if r['strict_accepted']),
        observed_preservation=passed('manual_observed_preservation'),amendment_reasoning=passed('manual_amendment_reasoning'),amendment_applicable=sum(c['features']['amendment']['applicable'] for c in cases),
        injection_reasoning=passed('manual_injection_reasoning'),injection_applicable=sum(c['features']['injection']['applicable'] for c in cases),
        input_delta=passed('input_delta'),status_delta=passed('evidence_status_delta'),proof_delta=passed('proof_delta'),semantic_delta=passed('manual_delta_semantics'),
        cross_dimension_propagation=passed('manual_cross_dimension_propagation'),source_completeness=passed('manual_scope_accuracy'),
        human_repair_questions=passed('manual_questions_accuracy'),citation_semantics=passed('manual_citation_semantics'),explanation_accuracy=passed('manual_explanation_accuracy'),
        latency_seconds=dict(sum=round(sum(lat),3),median=statistics.median(lat) if lat else None,min=min(lat) if lat else None,max=max(lat) if lat else None),
        cost=load(OUT/'llm-cost.json'),
        limits=['One observation per selected synthetic holdout, no population accuracy estimate','Agent semantic review, independent human review NOT_RUN','No actual Uliya or NAS execution','Final content unchanged; omitted private reasoning not used to repair answers'])
    result=dict(status='NOT_RUN' if not done else 'PASS' if len(done)==len(cases) and all(r['strict_accepted'] for r in done) else 'PARTIAL',
        layer='EXTERNAL DEEPSEEK SYNTHETIC REASONING PROXY',summary=summary,observations=rows)
    (OUT/'llm-review.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status=result['status'],**{k:summary[k] for k in ['requested_cases','executed_cases','strict_accepted','strict_total','overall_labels','effective_dimensions','literal_quotes','semantic_quotes','unsafe_positive_dimensions','unsupported_positive_citation_occurrences','latency_seconds']}),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inspect');args=p.parse_args();inspect(args.inspect) if args.inspect else score()
