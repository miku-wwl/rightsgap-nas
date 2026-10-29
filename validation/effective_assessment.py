"""Phase 2.1 offline effective-assessment oracle, never an Uliya adapter.

Inputs and semantic/scope reviews are curated synthetic test contracts. This
module does not retrieve files, interpret arbitrary text, dispatch experts or
run inside the Markdown Skill. Unknown dependencies default to all dimensions.
"""
import copy
import hashlib
import json

from reference_policy import (assess, interpretation_key, valid_path, DIMENSIONS,
    INPUT_KEYS, POSITIVE, CONFLICT, GAP, AMBIGUOUS, UNASSESSED)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def claim_key(doc, fact, dimension, span):
    return digest(dict(interpretation=interpretation_key(doc, fact), text=doc.get('text'),
        dimension=dimension, span=span))


def scope_key(proof):
    return digest(proof)


def complete(doc, roots):
    return bool(doc and doc.get('state') == 'completed' and doc.get('coverage_complete') is True
        and not any(doc.get(k) for k in ('denied', 'truncated', 'partial'))
        and valid_path(doc.get('path'), roots) and isinstance(doc.get('text'), str)
        and doc['text'].strip() and isinstance(doc.get('context'), str)
        and doc['text'] in doc['context'])


def dependency_scope(case, path, available):
    """Narrowing needs genuine complete proof AND an independent curated review."""
    proof = next((p for p in case.get('scope_proofs', []) if p.get('dependent_source') == path), None)
    if proof and scope_key(proof) in case.get('scope_reviews', {}):
        source = next((d for d in available if d['path'] == proof.get('source')), None)
        dims = proof.get('affected_dimensions')
        assets = proof.get('affected_assets')
        quote = proof.get('quote')
        if (source and isinstance(quote, str) and quote and quote in source['text']
            and isinstance(dims, list) and set(dims) <= set(DIMENSIONS)
            and isinstance(assets, list) and assets
            and case['scope_reviews'][scope_key(proof)].get('substantive_scope_review') is True):
            return (set(dims) if case['asset'] in assets else set()), proof
    return set(DIMENSIONS), None


def evaluate(case, scenario):
    roots = case['authorized_roots']
    selected = case['selected_documents']
    documents = case['documents']
    available = [d for d in documents if d.get('path') in selected and complete(d, roots)]
    usable_paths = {d['path'] for d in available}
    blockers, exclusions = {}, []
    for path in selected:
        if path not in usable_paths:
            dimensions, proof = dependency_scope(case, path, available)
            if not dimensions:
                exclusions.append(dict(source=path, proof=proof, basis='Reviewed explicit documentary exclusion'))
            for dimension in dimensions:
                blockers.setdefault(dimension, []).append(dict(source=path, reason='Unavailable potentially applicable source', narrowing_proof=proof))
    malformed = (not selected or len(selected) != len(set(selected))
        or len({d.get('path') for d in documents}) != len(documents)
        or any(d.get('path') not in selected for d in documents)
        or any(not valid_path(p, roots) for p in selected))
    if malformed:
        for dimension in DIMENSIONS:
            blockers.setdefault(dimension, []).append(dict(source=None, reason='Malformed, duplicate, out-of-root or enlarged selected scope'))
    base = assess(case['asset'], scenario, available, coverage=True,
        mapping=case.get('association_established') is True, reviews=case['interpretation_reviews'],
        source_roots=roots, expected_sources=[d['path'] for d in available])
    observations = []
    for doc in documents:
        if doc.get('path') not in selected:
            continue
        for fact in doc.get('findings', []):
            quote = fact.get('quote')
            if isinstance(quote, str) and quote and quote in (doc.get('text') or ''):
                observations.append(dict(source=doc['path'], clause_id=fact.get('clause_id'), quote=quote,
                    claimed_asset=fact.get('asset'), semantic_type=fact.get('kind'),
                    interpretation_reviewed=interpretation_key(doc, fact) in case['interpretation_reviews'],
                    scope_complete=complete(doc, roots), classification='OBSERVATION_ONLY'))
    cells = copy.deepcopy(base['dimensions'])
    observed_conflicts = {d: copy.deepcopy(c.get('conflicts', [])) for d, c in cells.items() if c.get('conflicts')}
    claim_issues = []
    for dimension, cell in cells.items():
        if cell['status'] == POSITIVE:
            accepted = []
            for citation in cell.get('support', []):
                doc = next((d for d in available if d['path'] == citation['source'] and d['id'] == citation['document_id']), None)
                fact = next((f for f in (doc or {}).get('findings', []) if f['clause_id'] == citation['clause_id']), None)
                span = (fact or {}).get('claim_spans', {}).get(dimension, (fact or {}).get('quote'))
                review = case.get('claim_reviews', {}).get(claim_key(doc, fact, dimension, span)) if doc and fact else None
                if (isinstance(span, str) and span and span in doc['text'] and review
                    and review.get('substantive_support') is True):
                    accepted.append({**citation, 'quote': span, 'claim_review_basis': review['reason']})
            if not accepted:
                claim_issues.append(dict(dimension=dimension, reason='No independently reviewed substantive citation-to-claim span'))
                blockers.setdefault(dimension, []).append(dict(source=None, reason=claim_issues[-1]['reason']))
            cell['support'] = accepted
        if dimension in blockers:
            cell.update(status=UNASSESSED, support=[], dependency_blockers=blockers[dimension])
    statuses = {c['status'] for c in cells.values()}
    if blockers or base['status'] == UNASSESSED:
        overall = UNASSESSED
    elif not case.get('association_established'):
        overall = AMBIGUOUS  # Known ambiguous join; dependent cells stay UNASSESSED.
    else:
        overall = (AMBIGUOUS if AMBIGUOUS in statuses else CONFLICT if CONFLICT in statuses
            else GAP if GAP in statuses else POSITIVE)
    questions = []
    for dimension, cell in cells.items():
        if cell['status'] == POSITIVE:
            continue
        paths = sorted({b['source'] for b in blockers.get(dimension, []) if b['source']})
        questions.append(dict(dimension=dimension, status=cell['status'], question=(
            f'Provide complete authorized context for {paths} and establish its effect on {case["asset"]}/{dimension}.' if paths else
            f'Which exact source clause establishes the asset/party join, substantive {dimension} support or documentary authority for {case["asset"]}?')))
    return dict(layer='SIMULATED_EXPERT_RESULTS; CURATED OFFLINE ORACLE', asset=case['asset'],
        status=overall, dimensions=cells, observed_evidence=observations, observed_conflicts=observed_conflicts,
        dependency_blockers=blockers, exclusions=exclusions, citation_issues=claim_issues,
        human_review_questions=questions, human_review='PENDING', operations=[], saving='DISABLED',
        scope_receipt=dict(selected_documents=selected, available_complete=sorted(usable_paths),
            unavailable=[p for p in selected if p not in usable_paths], source_revision=case['source_revision']),
        limits=['Curated interpretation and scope reviews, not automatic natural-language entailment',
            'No actual expert, filesystem, network or NAS operation; Markdown has no native enforcement'])


def compare_effective(case):
    rows = [evaluate(case, scenario) for scenario in case['scenarios']]
    layers = dict(input_delta=[], evidence_status_delta=[], proof_delta=[])
    for d, key in INPUT_KEYS.items():
        before, after = (s[key] for s in case['scenarios'])
        if before == after:
            continue
        a, b = [r['dimensions'][d] for r in rows]
        layers['input_delta'].append(dict(dimension=d, before=before, after=after))
        layers['evidence_status_delta'].append(dict(dimension=d, status_A=a['status'], status_B=b['status'], status_changed=a['status'] != b['status']))
        layers['proof_delta'].append(dict(dimension=d, status_A=a['status'], status_B=b['status'],
            evidence_A=a.get('support', []) + a.get('conflicts', []), evidence_B=b.get('support', []) + b.get('conflicts', []),
            explanation='Fixed source revision; effective applicability includes source dependencies and substantive quote review.',
            uncertainty=rows[0]['dependency_blockers'].get(d, []) + rows[1]['dependency_blockers'].get(d, [])))
    return dict(assessments=rows, delta=layers)
