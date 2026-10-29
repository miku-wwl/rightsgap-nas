"""Manually reviewed SYNTHETIC interpretations. Never an UGOS response adapter.

The fixed fixture phrases are deliberately labelled here. The policy receives a
separate ledger made BEFORE adversarial mutations; unknown claims cannot simply
declare themselves reviewed. This does not solve arbitrary text entailment.
"""
import copy
import json
from pathlib import Path
from reference_policy import interpretation_key

ROOT = Path(__file__).resolve().parent
INDEPENDENT = ('Independent restriction R1: digital/social advertising is prohibited for A001 '
               'for StudioA; this restriction survives any amendment to the use grant.')


def load_baseline():
    corpus = json.loads((ROOT / 'fixtures/corpus.json').read_text(encoding='utf-8-sig'))
    docs = copy.deepcopy(corpus['documents'])
    supplement = copy.deepcopy(corpus['supplement'])
    for doc in docs + [supplement]:
        for finding in doc['findings']:
            finding.update(clause_id='grant', kind='grant')
    fact = supplement['findings'][0]
    fact.update(clause_id='amended-use', kind='amendment',
                conditions={'licensed_party': ['StudioA'], 'purpose': ['paid commercial advertising']})
    fact['amendments'] = [{
        'target_document': 'L1', 'target_clause': 'grant',
        'dimensions': ['purpose', 'channel', 'territory', 'time_window'],
        'conditions': {'asset_identity': ['A001'], 'licensed_party': ['StudioA'],
                       'purpose': ['paid commercial advertising']},
        'quote': fact['quote'], 'authority_basis': 'established_in_synthetic_premise',
        'applicability': 'established_for_fixture', 'precedence': 'explicit_clause_relationship'
    }]
    corpus.update(documents=docs, supplement=supplement)
    return corpus


def review_ledger(documents):
    return {interpretation_key(doc, fact): {'basis': 'Manual review of fixed synthetic clause; not legal authentication',
                                          'source': doc['path'], 'document_id': doc['id'],
                                          'clause_id': fact['clause_id'], 'asset': fact['asset']}
            for doc in documents for fact in doc['findings']}


def independent_restriction(document):
    document['text'] += '\n' + INDEPENDENT
    document['findings'].append({'asset': 'A001', 'clause_id': 'R1', 'kind': 'restriction',
                                'quote': INDEPENDENT, 'terms': {'channel': ['own news website']},
                                'exclusive': ['channel'], 'conditions': {'licensed_party': ['StudioA']}})


def adversarial_case(name):
    corpus = load_baseline()
    asset, scenario = 'A001', copy.deepcopy(corpus['scenarios'][1])
    docs = [copy.deepcopy(corpus['documents'][0]), copy.deepcopy(corpus['supplement'])]
    flags = {'coverage': True}
    if name in ('partial_amendment_independent_restriction', 'explicitly_preserved_restriction', 'removed_original_clause'):
        independent_restriction(docs[0])
    fact = docs[1]['findings'][0]
    relation = fact['amendments'][0]
    if name == 'ambiguous_authority':
        relation['authority_basis'] = 'unknown'
    elif name == 'unknown_applicability':
        relation['applicability'] = 'unknown'
    elif name == 'missing_precedence':
        relation['precedence'] = 'unknown'
    elif name == 'conflicting_amendments':
        competing = copy.deepcopy(docs[1])
        competing['id'] = 'L8'
        competing['path'] = 'synthetic/licenses/L8_competing_amendment.pdf'
        q = 'L8 claims to amend L1 grant for A001 and StudioA for paid commercial advertising on digital/social advertising channels, only in New Zealand, not worldwide, from 2026-01-01 through 2027-12-31. No precedence over L7 is established.'
        competing['text'] = q
        competing['findings'][0].update(quote=q, terms={**fact['terms'], 'territory': ['New Zealand']}, exclusive=['territory'])
        competing['findings'][0]['amendments'][0]['quote'] = q
        docs.append(competing)
    elif name == 'unrelated_asset_amendment':
        docs[1]['text'] = docs[1]['text'].replace('A001', 'A002')
        fact['quote'] = fact['quote'].replace('A001', 'A002')
        fact['asset'] = 'A002'
        fact['terms']['asset_identity'] = ['A002']
        relation['conditions']['asset_identity'] = ['A002']
        relation['quote'] = fact['quote']
    elif name == 'different_licensed_party':
        docs[1]['text'] = docs[1]['text'].replace('StudioA', 'StudioB')
        fact['quote'] = fact['quote'].replace('StudioA', 'StudioB')
        fact['terms']['licensed_party'] = ['StudioB']
        fact['conditions']['licensed_party'] = ['StudioB']
        relation['conditions']['licensed_party'] = ['StudioB']
        relation['quote'] = fact['quote']
    elif name == 'one_dimension_amendment':
        scenario = {**corpus['scenarios'][0], 'purpose': 'paid commercial advertising'}
        q = 'For A001 and StudioA, L7 replaces only the purpose restriction in L1 grant with editorial and paid commercial advertising. Every other L1 clause and dimension remains effective.'
        docs[1]['text'] = q
        fact.update(quote=q, terms={'purpose': ['editorial', 'paid commercial advertising']})
        relation.update(dimensions=['purpose'], quote=q)
    elif name == 'missing_target_clause':
        relation['target_clause'] = 'unknown-clause'
    elif name == 'unresolved_conflict_before_amendment':
        q = 'Applicability of the beneficiary identity in L1 remains disputed and is not resolved by a use-only amendment.'
        docs[0]['text'] += '\n' + q
        docs[0]['findings'].append({'asset': 'A001', 'clause_id': 'identity-dispute', 'kind': 'grant',
                                    'quote': q, 'terms': {'licensed_party': ['StudioA']},
                                    'ambiguity': 'Unresolved beneficiary applicability'})
    elif name == 'same_document_conflicting_findings':
        asset = 'A002'
        docs = [copy.deepcopy(corpus['documents'][1])]
        q = 'Contradictory clause C2: A002 is limited to editorial purpose only; no relationship to the earlier grant is established.'
        docs[0]['text'] += '\n' + q
        docs[0]['findings'].append({'asset': asset, 'clause_id': 'C2', 'kind': 'grant', 'quote': q,
                                    'terms': {'purpose': ['editorial']}, 'exclusive': ['purpose']})
    # Trusted manual review is frozen before corruption/attribution mutations.
    reviews = review_ledger(docs)
    if name == 'missing_amendment_source':
        docs[1]['path'] = ''
    elif name == 'removed_original_clause':
        docs[0]['text'] = docs[0]['text'].replace(INDEPENDENT, '')
    elif name == 'existing_quote_wrong_dimension':
        fact['quote'] = 'SYNTHETIC; no legal effect.'  # exists, entails none of the claimed terms
    elif name == 'wrong_source_attribution':
        docs[1]['path'] = docs[0]['path']
    elif name == 'missing_semantic_review':
        reviews = {}
    elif name == 'source_path_traversal':
        docs[1]['path'] = 'synthetic/licenses/../../outside.pdf'
    elif name == 'unknown_coverage':
        flags['coverage'] = False
    return asset, scenario, docs, reviews, flags
