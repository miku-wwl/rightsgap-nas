"""Phase 2.2 LOCAL report oracle/checks. Never execute Markdown, tools or NAS.

Exact structure can be checked mechanically. Entailment and question adequacy
still require source/content-bound semantic review; string shape is insufficient.
"""
import copy
from effective_assessment import evaluate, complete
from reference_policy import DIMENSIONS as D, POSITIVE as C

INPUTS = {'licensed_party':'licensee', 'purpose':'purpose', 'channel':'channel',
          'territory':'territory', 'time_window':'date'}
STATES = {'CONSISTENT_EVIDENCE','EXPLICIT_CONFLICT','GAP_IN_CHECKED_SCOPE','AMBIGUOUS_EVIDENCE','UNASSESSED'}


def input_delta(scenarios, *, variable_party=False):
    if len(scenarios) != 2:
        raise ValueError('Exactly two scenarios required')
    if not variable_party and scenarios[0]['licensee'] != scenarios[1]['licensee']:
        raise ValueError('Licensed party is fixed in this Skill workflow')
    return [dict(dimension=d, before=scenarios[0][k], after=scenarios[1][k]) for d,k in INPUTS.items()
            if scenarios[0][k] != scenarios[1][k]]


def deltas(scenarios, rows):
    inputs = input_delta(scenarios)
    changed = {r['dimension'] for r in inputs}
    status, proof = [], []
    for d in D:
        a,b = [r['dimensions'][d] for r in rows]
        if d not in changed and a['status'] == b['status']:
            continue
        common = dict(dimension=d, status_A=a['status'], status_B=b['status'],
                      input_changed=d in changed, status_changed=a['status'] != b['status'])
        status.append(common)
        proof.append(dict(**common, evidence_A=a.get('support', []) + a.get('conflicts', []),
            evidence_B=b.get('support', []) + b.get('conflicts', []),
            explanation='Same source revision; check qualified conditions and actual dependencies for this dimension.',
            uncertainty=copy.deepcopy(rows[0].get('dependency_blockers', {}).get(d, []) + rows[1].get('dependency_blockers', {}).get(d, []))))
    return dict(input_delta=inputs, evidence_status_delta=status, proof_delta=proof)


def source_receipt(case, rows):
    selected = case['selected_documents']
    docs = {d['path']:d for d in case['documents'] if d.get('path') in selected}
    facts = []
    for path in selected:
        doc = docs.get(path, {})
        read = bool(isinstance(doc.get('context'), str) and doc['context'].strip())
        done = complete(doc, case['authorized_roots'])
        facts.append(dict(path=path, read=read, state=doc.get('state', 'missing'),
            completeness='complete' if done else 'incomplete_or_unknown',
            access_error='denied' if doc.get('denied') else doc.get('access_error'),
            limitation=None if done else 'Selected relevant context unavailable/incomplete',
            source_revision=doc.get('source_revision', 'Unknown')))
    return dict(authorized_roots=case['authorized_roots'], selected_sources=list(selected),
        actually_read_sources=[s['path'] for s in facts if s['read']],
        unavailable_selected_sources=[s['path'] for s in facts if s['completeness']!='complete'],
        source_revision=case['source_revision'], source_states=facts,
        dependencies=[dict(scenario=label, dimension=d, blockers=blockers) for label,row in zip(['A','B'], rows)
            for d,blockers in row.get('dependency_blockers', {}).items()],
        untrusted_references=copy.deepcopy(case.get('untrusted_evidence', [])))


def repair_questions(case, rows):
    questions = []
    for scenario,row in zip(['A','B'], rows):
        for dimension,cell in row['dimensions'].items():
            if cell['status'] == C:
                continue
            paths = sorted({b['source'] for b in row.get('dependency_blockers', {}).get(dimension, []) if b.get('source')})
            if paths:
                missing = 'Complete source text and documentary scope for ' + ', '.join(paths)
                request = 'Provide the complete selected source and its verifiable asset/dimension scope clause, including any explicit exclusion; a reassurance cannot establish completeness.'
            elif case.get('category') == 'unknown-authority':
                missing = f'Documented authority and precedence of M over G/G1 for {dimension}'
                request = f'Provide the source and exact clause establishing M authority to replace G/G1 {dimension} for the stated commercial-catalogue scenario; full amendment text alone does not establish this relationship.'
            elif cell.get('conflicts'):
                cites = cell['conflicts']
                sources = ', '.join(sorted({x['source'] for x in cites}))
                missing = f'A source-backed resolution of the observed {dimension} contradiction in {sources}'
                request = f'Provide a documented applicable amendment expressly targeting the conflicting {dimension} clause, with authority/precedence and scope; otherwise preserve the cited contradiction.'
            elif case.get('category') == 'irrelevant-citation':
                missing = f'A substantive identifying span for {case["asset"]}; the supplied citation does not establish {dimension}'
                request = 'Provide the exact identifying clause and actual selected source context, or an explicitly cited asset-to-agreement association. Mere quotation membership does not supply the missing connection.'
            else:
                missing = f'An applicable documentary grant or qualification establishing {dimension} for this specific intended use'
                request = f'Provide the complete clause and source establishing {dimension} under the actual purpose/channel/territory/date conditions; do not reuse independent-looking terms from an inapplicable coupled profile.'
            questions.append(dict(asset=case['asset'], scenario=scenario, dimension=dimension,
                missing=missing, requested_evidence=request,
                remaining_unknown='Real legal authenticity/enforceability, unselected agreements and completeness of any new evidence remain Unknown until separately checked.',
                question=f'For {case["asset"]}, Scenario {scenario}, {dimension}: what source resolves {missing}? The effective judgment remains blocked pending source review.',
                evidence_required=True))
    return questions


def compare22(case):
    rows = [evaluate(case, s) for s in case['scenarios']]
    return dict(layer='CURATED OFFLINE ORACLE; NOT MARKDOWN/ULIYA/NAS EXECUTION',
        assessments=rows, **deltas(case['scenarios'], rows), scope_receipt=source_receipt(case, rows),
        human_review_questions=repair_questions(case, rows), human_review='PENDING',
        saving='DISABLED', operations=[])


def unique_strings(value):
    return isinstance(value,list) and all(isinstance(v,str) for v in value) and len(value)==len(set(value))


def check_scope(receipt, expected):
    """Reject literal contamination, never strip annotations or normalize paths."""
    if not isinstance(receipt,dict):
        return False
    keys = ('selected_sources','actually_read_sources','unavailable_selected_sources')
    if any(not unique_strings(receipt.get(k)) or set(receipt[k]) != set(expected[k]) for k in keys):
        return False
    if receipt.get('authorized_roots') != expected['authorized_roots'] or receipt.get('source_revision') != expected['source_revision']:
        return False
    states = receipt.get('source_states')
    if not isinstance(states,list) or any(not isinstance(s,dict) or not isinstance(s.get('path'),str) for s in states):
        return False
    if len(states)!=len(expected['source_states']) or len({s['path'] for s in states})!=len(states):
        return False
    if {s['path']:s for s in states} != {s['path']:s for s in expected['source_states']}:
        return False
    dep = receipt.get('dependencies')
    if not isinstance(dep,list) or any(not isinstance(r,dict) or r.get('dimension') not in D or r.get('scenario') not in ('A','B') for r in dep):
        return False
    if dep != expected['dependencies']:
        return False
    return receipt.get('untrusted_references') == expected['untrusted_references']


def question_shape(question):
    if not isinstance(question,dict):
        return False
    fields=('asset','missing','requested_evidence','remaining_unknown','question')
    if any(not isinstance(question.get(k),str) or not question[k].strip() for k in fields):
        return False
    text = ' '.join(question[k] for k in fields).lower()
    forbidden = ('confirm that no other restrictions apply','or simply confirm','your reassurance is sufficient',
                 'approval replaces','no document is needed','just confirm','confirm no restrictions')
    return (question.get('dimension') in D and question.get('scenario') in ('A','B')
        and question.get('evidence_required') is True and not any(s in text for s in forbidden))
