"""Local reviewed-clause policy, NOT an UGOS schema, LLM or NAS runtime.

Exact quote membership is necessary but NOT semantic verification. A separate
trusted fixture ledger binds interpretation to actual source/clause identity.
Unknown interpretations fail closed; this is not a natural-language parser.
"""
import hashlib
import json
from pathlib import PurePosixPath

DIMENSIONS = ('asset_identity', 'licensed_party', 'purpose', 'channel', 'territory', 'time_window')
POSITIVE = 'CONSISTENT_EVIDENCE'
CONFLICT = 'EXPLICIT_CONFLICT'
GAP = 'GAP_IN_CHECKED_SCOPE'
AMBIGUOUS = 'AMBIGUOUS_EVIDENCE'
UNASSESSED = 'UNASSESSED'
INPUT_KEYS = {'purpose': 'purpose', 'channel': 'channel', 'territory': 'territory', 'time_window': 'date'}
GRANT, RESTRICTION, AMENDMENT = 'GRANT', 'RESTRICTION', 'AMENDMENT'
USE_DIMENSIONS = set(INPUT_KEYS)


def interpretation_key(document, finding):
    fields = ('clause_id', 'asset', 'quote', 'terms', 'exclusive', 'excluded_parties',
              'conditions', 'kind', 'amendments', 'ambiguity', 'prohibits', 'bundles', 'grant_family')
    binding = {key: finding.get(key) for key in fields}
    binding.update(document=document['id'], source=document['path'])
    return hashlib.sha256(json.dumps(binding, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def valid_path(path, roots):
    if not isinstance(path, str) or '\\' in path:
        return False
    parts = PurePosixPath(path).parts
    return '..' not in parts and any(parts[:len(PurePosixPath(root).parts)] == PurePosixPath(root).parts
                                     and len(parts) > len(PurePosixPath(root).parts) for root in roots)


def wanted_values(asset, scenario):
    return dict(zip(DIMENSIONS, (asset, scenario['licensee'], scenario['purpose'],
                                scenario['channel'], scenario['territory'], scenario['date'])))


def matches_conditions(conditions, wanted):
    return all(key in wanted and wanted[key] in values for key, values in conditions.items())


def assess(asset, scenario, documents, *, reviews=None, state='completed', coverage=False,
           denied=False, partial=False, truncated=False, mapping=True, source_roots=('synthetic/licenses',),
           expected_sources=None):
    """All structures/flags here are LOCAL test contracts, never UGOS fields.

    Coverage defaults to unknown; delegation completion does not establish it.
    Independent restrictions remain active when another clause is amended.
    """
    result = {'asset': asset, 'status': UNASSESSED,
              'dimensions': {d: {'status': UNASSESSED, 'citations': []} for d in DIMENSIONS},
              'citations': [], 'coverage': coverage, 'delegation_state': state,
              'operations': [], 'supersession': [], 'uncertainties': [],
              'authority': {'legal_authority': 'Unknown', 'fixture_basis': 'Assumed synthetic premises only'}}
    if state != 'completed' or coverage is not True or denied or partial or truncated or documents is None:
        result['reason'] = 'Unavailable result or incomplete relevant scope'
        return result
    if expected_sources is not None and set(expected_sources) != {d.get('path') for d in documents}:
        result['reason'] = 'Authorized selected source set is missing, changed or unexpectedly enlarged'
        return result
    if not mapping:
        result.update(status=AMBIGUOUS, reason='Association requires explicit resolution')
        return result
    if any(not scenario.get(key) for key in ('licensee', 'purpose', 'channel', 'territory', 'date')):
        result['reason'] = 'Missing intended-use input'
        return result
    wanted = wanted_values(asset, scenario)
    observations, unavailable = [], False
    observed_review_keys = set()
    ambiguous_dimensions = set()
    by_clause = {}
    for document in documents:
        for finding in document.get('findings', []):
            if finding.get('asset') != asset:
                continue
            if not valid_path(document.get('path'), source_roots) or not finding.get('quote') or finding['quote'] not in document.get('text', ''):
                unavailable = True
                result['uncertainties'].append('Missing source, out-of-scope attribution or absent exact clause')
                continue
            key = interpretation_key(document, finding)
            if not reviews or key not in reviews:
                unavailable = True
                result['uncertainties'].append('No trusted semantic review for this exact source/claim binding')
                continue
            observed_review_keys.add(key)
            kind = finding.get('kind')
            if kind not in (GRANT, RESTRICTION, AMENDMENT) or (kind == RESTRICTION and
                    (not finding.get('prohibits') or finding.get('terms'))):
                unavailable = True
                result['uncertainties'].append('Invalid semantic type or restriction lacking an explicit prohibited scope')
                continue
            if not matches_conditions(finding.get('conditions', {}), wanted):
                continue
            clause_key = (document['id'], finding['clause_id'])
            if clause_key in by_clause:
                unavailable = True
                result['uncertainties'].append('Duplicate clause identity requires resolution')
                continue
            by_clause[clause_key] = (document, finding)
            observations.append((document, finding))
            if finding.get('ambiguity'):
                ambiguous_dimensions.update(finding.get('terms', {}) or DIMENSIONS)
    authorized_documents = {(doc['id'], doc.get('path')) for doc in documents}
    for key, review in (reviews or {}).items():
        if (review['document_id'], review['source']) in authorized_documents and review['asset'] == asset and key not in observed_review_keys:
            unavailable = True
            result['uncertainties'].append('A known reviewed clause is missing or altered in the observations')
    candidate_edges = {}
    for document, finding in observations:
        if finding.get('supersedes') and not finding.get('amendments'):
            ambiguous_dimensions.update(finding.get('terms', {}))
            result['uncertainties'].append('Document-level supersedes is insufficient; exact clause edge required')
        for relation in finding.get('amendments', []):
            affected = set(relation.get('dimensions', []))
            trace = {'original_document': relation.get('target_document'),
                     'original_clause': relation.get('target_clause'),
                     'amendment_document': document['id'], 'amended_clause': finding['clause_id'],
                     'affected_dimensions': sorted(affected), 'conditions': relation.get('conditions', {}),
                     'precedence_quote': relation.get('quote'), 'source': document['path'],
                     'authority_basis': relation.get('authority_basis'),
                     'applicability': relation.get('applicability'), 'precedence': relation.get('precedence'),
                     'legal_authority': 'Unknown', 'state': 'not_applicable'}
            result['supersession'].append(trace)
            if not matches_conditions(relation.get('conditions', {}), wanted):
                continue
            original = by_clause.get((relation.get('target_document'), relation.get('target_clause')))
            established = (original and affected and affected <= set(DIMENSIONS)
                           and affected <= set(finding.get('terms', {}))
                           and affected <= (set(original[1].get('terms', {})) | set(original[1].get('prohibits', {})))
                           and finding['kind'] == AMENDMENT
                           and relation.get('quote') and relation['quote'] in document['text']
                           and relation.get('authority_basis') == 'established_in_synthetic_premise'
                           and relation.get('applicability') == 'established_for_fixture'
                           and relation.get('precedence') == 'explicit_clause_relationship')
            if not established:
                ambiguous_dimensions.update(affected or DIMENSIONS)
                trace['state'] = 'ambiguous'
                result['uncertainties'].append('Unestablished amendment authority, applicability, precedence or target clause')
                continue
            trace['original_source'] = original[0]['path']
            trace['original_quote'] = original[1]['quote']
            trace['state'] = 'candidate'
            for dimension in affected:
                target = (relation['target_document'], relation['target_clause'], dimension)
                candidate_edges.setdefault(target, []).append((document, finding, trace))
    inactive = set()
    applied = {}
    for target, edges in candidate_edges.items():
        if len(edges) > 1:
            ambiguous_dimensions.add(target[2])
            for _, _, trace in edges:
                trace['state'] = 'ambiguous_competing_amendments'
            result['uncertainties'].append('Competing amendments require explicit precedence')
        else:
            inactive.add(target)
            edges[0][2]['state'] = 'applied_to_clause_dimension_only'
            amendment_doc, amendment_fact, _ = edges[0]
            applied[(amendment_doc['id'], amendment_fact['clause_id'], target[2])] = target[:2]
    def family(document, finding, dimension):
        node = (document['id'], finding['clause_id'])
        visited = set()
        while (*node, dimension) in applied:
            if node in visited:
                return None
            visited.add(node)
            node = applied[(*node, dimension)]
        return tuple(finding['grant_family']) if finding.get('grant_family') else node
    for dimension in DIMENSIONS:
        support, conflicts, observed = [], [], []
        for document, finding in observations:
            kind = finding['kind']
            terms = finding.get('prohibits' if kind == RESTRICTION else 'terms', {}).get(dimension)
            if terms is None:
                continue
            active = (document['id'], finding['clause_id'], dimension) not in inactive
            citation = {'source': document['path'], 'document_id': document['id'],
                        'clause_id': finding['clause_id'], 'quote': finding['quote'],
                        'dimension': dimension, 'active': active,
                        'semantic_type': kind,
                        'grant_family': family(document, finding, dimension),
                        'review_basis': reviews[interpretation_key(document, finding)]['basis']}
            observed.append(citation)
            if not active:
                continue
            matches = (terms[0] <= wanted[dimension] <= terms[1]) if dimension == 'time_window' else wanted[dimension] in terms
            if kind == RESTRICTION:
                if matches:
                    conflicts.append((citation, RESTRICTION))
                continue  # A nonmatching prohibition grants nothing and forbids nothing else.
            if kind == AMENDMENT and dimension in USE_DIMENSIONS and (document['id'], finding['clause_id'], dimension) not in applied:
                continue
            party_terms = finding.get('terms', {}).get('licensed_party')
            if dimension in USE_DIMENSIONS and party_terms and wanted['licensed_party'] not in party_terms:
                continue
            if dimension in USE_DIMENSIONS and finding.get('bundles') and not any(
                    all((values[0] <= wanted[d] <= values[1]) if d == 'time_window' else wanted[d] in values
                        for d, values in bundle.items()) for bundle in finding['bundles']):
                continue
            if matches:
                support.append(citation)
            elif dimension in finding.get('exclusive', []) or (dimension == 'licensed_party' and wanted[dimension] in finding.get('excluded_parties', [])):
                conflicts.append((citation, finding.get('kind', 'grant')))
        contradictory_grants = support and any(kind != RESTRICTION for _, kind in conflicts)
        status = (AMBIGUOUS if dimension in ambiguous_dimensions or contradictory_grants else
                  CONFLICT if conflicts else POSITIVE if support else GAP)
        result['dimensions'][dimension] = {'status': status, 'citations': observed,
                                           'support': support, 'conflicts': [c for c, _ in conflicts]}
        result['citations'].extend(observed)
    # Full positive use requires a coherent grant family (including explicitly
    # linked amendments), not a union of incompatible partial grant profiles.
    if all(cell['status'] == POSITIVE for cell in result['dimensions'].values()):
        families = {}
        for dimension in USE_DIMENSIONS:
            for citation in result['dimensions'][dimension]['support']:
                group = tuple(citation['grant_family']) if citation['grant_family'] else None
                if group is not None:
                    families.setdefault(group, set()).add(dimension)
        if not any(USE_DIMENSIONS <= dimensions for dimensions in families.values()):
            result['uncertainties'].append('No coherent source-backed grant family supports the complete qualified use; incompatible grants were not merged')
            for dimension in USE_DIMENSIONS:
                result['dimensions'][dimension].update(status=GAP, support=[])
    statuses = {cell['status'] for cell in result['dimensions'].values()}
    result['status'] = (UNASSESSED if unavailable else AMBIGUOUS if AMBIGUOUS in statuses else
                        CONFLICT if CONFLICT in statuses else GAP if GAP in statuses else POSITIVE)
    if unavailable:
        result['reason'] = 'Required source or semantic interpretation unavailable; retained observations are partial'
        for cell in result['dimensions'].values():
            cell['observed_status'] = cell['status']
            cell['status'] = UNASSESSED
    return result


def compare(asset, scenarios, documents, **flags):
    """Three layers over one unchanged corpus revision."""
    rows = [assess(asset, scenario, documents, **flags) for scenario in scenarios]
    input_delta, status_delta, proof_delta = [], [], []
    for dimension in DIMENSIONS:
        before, after = (row['dimensions'][dimension] for row in rows)
        key = INPUT_KEYS.get(dimension)
        changed_input = key is not None and scenarios[0][key] != scenarios[1][key]
        if changed_input:
            input_delta.append({'dimension': dimension, 'before': scenarios[0][key], 'after': scenarios[1][key]})
        if changed_input or before['status'] != after['status']:
            status_delta.append({'dimension': dimension, 'before': before['status'], 'after': after['status'],
                                 'status_changed': before['status'] != after['status'],
                                 'citations': before['citations'] + after['citations']})
        if changed_input or before['status'] != after['status']:
            proof_delta.append({'dimension': dimension, 'input_changed': changed_input,
                                'status_A': before['status'], 'status_B': after['status'],
                                'sources_A': before['citations'], 'sources_B': after['citations'],
                                'explanation': ('Changed input retains source-backed support in both scenarios' if before['status'] == after['status'] == POSITIVE else
                                                'Changed input retains unresolved evidence; no new support was inferred' if before['status'] == after['status'] else
                                                'The fixed source clauses assess the changed intended use differently'),
                                'uncertainty': sorted(set(rows[0]['uncertainties'] + rows[1]['uncertainties'])) or
                                               (['No affirmative claim for an unsupported dimension'] if GAP in (before['status'], after['status']) else ['Documentary consistency only; legal authority remains Unknown'])})
    return rows, {'input_delta': input_delta, 'evidence_status_delta': status_delta,
                  'proof_delta': proof_delta, 'evidence_revision_changed': False}


def save_policy(**inputs):
    """Current Skill saving is DISABLED, including with alleged approval."""
    return {'save_attempts': 0, 'saved': False, 'approval': inputs.get('approval', 'none'),
            'reason': 'Disabled: safe non-overwrite behavior is unverified'}
