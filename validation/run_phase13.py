"""Targeted policy/precedence and strict-evaluator attack suite. No network."""
import copy
import hashlib
import json
from pathlib import Path

from clause_fixtures import load_baseline, review_ledger
from reference_policy import assess, DIMENSIONS, POSITIVE, GAP, UNASSESSED
from strict_evaluation import judge, accept, content_hash, MANUAL, PASS, FAIL, NOT_RUN, NOT_ELICITED

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results/phase1-3'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def controls(restricted=False):
    path = 'synthetic/licenses/evaluator-control.pdf'
    grant = 'A900 is licensed to StudioA for editorial or paid commercial advertising on its own news website or paid social advertising channels, worldwide including New Zealand, from 2026-01-01 through 2028-12-31.'
    identity = 'This agreement identifies A900 and StudioA.'
    restriction = 'Independent R1 prohibits A900 use by StudioA on paid social advertising channels.'
    sources = [{'path': path, 'page': None, 'clauses': [{'id': 'G1', 'text': grant}, {'id': 'ID', 'text': identity}]}]
    if restricted:
        sources[0]['clauses'].append({'id': 'R1', 'text': restriction})
    citation = lambda clause, quote: dict(source=path, clause_id=clause, quote=quote, page=None)
    pos, con = 'CONSISTENT_EVIDENCE', 'EXPLICIT_CONFLICT'
    a = dict.fromkeys(DIMENSIONS, pos)
    b = dict(a, channel=con) if restricted else dict(a)
    changed = {'purpose': {'before': 'editorial', 'after': 'paid commercial advertising'},
               'channel': {'before': 'own news website', 'after': 'paid social advertising'},
               'territory': {'before': 'New Zealand', 'after': 'worldwide'},
               'time_window': {'before': '2026-11-01', 'after': '2027-06-01'}}
    case = dict(asset_id='A900', licensed_party='StudioA', sources=sources, profile='full',
        expected={'overall': [pos, con if restricted else pos], 'dimensions': [a, b], 'input_delta': changed},
        required_citations=[[path, 'R1']] if restricted else [],
        features={'amendment': {'applicable': False, 'reason': 'No amendment exists in this fixed control'},
                  'injection': {'applicable': False, 'reason': 'No injection exists in this fixed control'}})
    answer = dict(asset_id='A900', licensed_party='StudioA', input_delta=[dict(dimension=d, **values) for d, values in changed.items()],
        evidence_status_delta=[], proof_delta=[], amendment_reasoning=[], uncertainty=['Real legal authority UNKNOWN; synthetic scope only.'], save_requested=False, operations=[])
    for n, (name, labels) in enumerate((('scenario_A', a), ('scenario_B', b))):
        cells = {}
        for dim in DIMENSIONS:
            c = citation('R1', restriction) if restricted and n == 1 and dim == 'channel' else citation('G1', grant)
            cells[dim] = dict(status=labels[dim], evidence=[c], explanation=('R1 explicitly prohibits B channel; independent restriction active.' if labels[dim] == con else 'This source expressly supports the stated qualified dimension.'), uncertainty=['Legal authority UNKNOWN.'])
        answer[name] = dict(status=case['expected']['overall'][n], dimensions=cells)
    for dim in changed:
        answer['evidence_status_delta'].append(dict(dimension=dim, status_A=a[dim], status_B=b[dim], status_changed=a[dim] != b[dim]))
        answer['proof_delta'].append(dict(dimension=dim, status_A=a[dim], status_B=b[dim], evidence_A=copy.deepcopy(answer['scenario_A']['dimensions'][dim]['evidence']), evidence_B=copy.deepcopy(answer['scenario_B']['dimensions'][dim]['evidence']),
            explanation='Changed inputs retain the explicit grant except B channel, which is prohibited by preserved R1.' if restricted else 'Both changed inputs fall inside the same express grant.', uncertainty=['Actual legal authority UNKNOWN.']))
    return case, answer


def reviewed(content, **overrides):
    return {'content_sha256': content_hash(content), 'reviewer': 'Curated evaluator-control review; not an LLM answer',
            'checks': {**dict.fromkeys(MANUAL, True), **overrides}}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frozen = ROOT / 'fixtures/phase1-3/cases-v2.json'
    receipt = json.loads((frozen.parent / 'freeze-v2.json').read_text(encoding='utf-8'))
    if hashlib.sha256(frozen.read_bytes()).hexdigest() != receipt['cases_sha256']:
        raise SystemExit('Frozen target expectations changed')
    assertions, case_results, ids = [], {}, set()
    def check(name, actual, wanted=True):
        if name in ids:
            raise ValueError('Duplicate targeted assertion: ' + name)
        ids.add(name)
        assertions.append(dict(id=name, passed=actual == wanted, actual=actual, expected=wanted))
    for case in json.loads(frozen.read_text(encoding='utf-8'))['cases']:
        documents, rules = case['documents'], case['checks']
        flags = dict(coverage=True, expected_sources=[d['path'] for d in documents], reviews=review_ledger(documents), truncated=rules.get('truncated', False))
        row = assess(case['asset'], case['scenario'], documents, **flags)
        prefix = 'phase13/' + case['id']
        check(prefix + '/overall', row['status'], case['expected'])
        for dim, status in rules.get('dimension_status', {}).items():
            check(prefix + '/' + dim, row['dimensions'][dim]['status'], status)
        if rules.get('no_restriction_support'):
            check(prefix + '/restriction_never_supports', all(c['semantic_type'] != 'RESTRICTION' for cell in row['dimensions'].values() for c in cell.get('support', [])))
        if rules.get('active_restriction'):
            check(prefix + '/R1_active_conflict', any(c['clause_id'] == 'R1' and c['active'] for c in row['dimensions']['channel'].get('conflicts', [])))
        for source, clause, dim in rules.get('inactive', []):
            check(prefix + '/' + clause + '/' + dim + '/superseded_not_support', any(c['document_id'] == source and c['clause_id'] == clause and not c['active'] for c in row['dimensions'][dim]['citations']) and not any(c['document_id'] == source and c['clause_id'] == clause for c in row['dimensions'][dim]['support']))
        for dim in rules.get('unaffected', []):
            check(prefix + '/' + dim + '/unaffected_original_support', any(c['document_id'] == 'ORIGINAL' and c['active'] for c in row['dimensions'][dim]['support']))
        if rules.get('no_positive') or rules.get('coherent_bundle_required'):
            check(prefix + '/not_affirmative', row['status'] != POSITIVE)
        if rules.get('no_invented_priority'):
            check(prefix + '/documentary_priority_not_invented', not any('priority' in u.lower() or 'precedence' in u.lower() for u in row['uncertainties']))
            check(prefix + '/real_legal_authority_unknown', row['authority']['legal_authority'], 'Unknown')
        if rules.get('no_applied_override'):
            check(prefix + '/no_override_applied', not any(edge['state'] == 'applied_to_clause_dimension_only' for edge in row['supersession']))
        if rules.get('both_sources'):
            check(prefix + '/both_sides_visible', set(rules['both_sources']) <= {c['document_id'] for c in row['dimensions']['purpose']['citations']})
        if rules.get('secondary_scenario'):
            secondary = assess(case['asset'], rules['secondary_scenario'], documents, **flags)
            check(prefix + '/condition_boundary', secondary['status'], rules['secondary_expected'])
            row['secondary_result'] = secondary
        case_results[case['id']] = row
    # A real coupled-purpose/channel clause must not be treated as a cross product.
    corpus = load_baseline()
    mixed = {**corpus['scenarios'][0], 'channel': 'digital/social advertising'}
    mixed_row = assess('A002', mixed, corpus['documents'], coverage=True, reviews=review_ledger(corpus['documents']))
    check('phase13/R07/coupled_single_clause_is_not_cross_product', mixed_row['status'], GAP)
    case_results['R07-coupled-source'] = mixed_row
    # Positive evidence cannot survive a coverage loss or silent known-clause removal.
    documents = copy.deepcopy(json.loads(frozen.read_text(encoding='utf-8'))['cases'][0]['documents'])
    reviews = review_ledger(documents)
    damaged = copy.deepcopy(documents)
    damaged[0]['findings'] = [f for f in damaged[0]['findings'] if f['clause_id'] != 'R1']
    lost = assess('A900', corpus['scenarios'][0], damaged, coverage=True, reviews=reviews)
    check('phase13/R08/known_restriction_removed_without_supersession', lost['status'], UNASSESSED)
    attacks = {}
    for number in range(1, 12):
        case, answer = controls(restricted=number in (10, 11))
        content = json.dumps(answer, sort_keys=True)
        review = reviewed(content)
        if number == 1:
            review = None
        elif number == 2:
            review['checks']['semantic_grounding'] = None
        elif number == 3:
            for name in ('scenario_A', 'scenario_B'):
                for cell in answer[name]['dimensions'].values():
                    cell['evidence'] = []
            for row in answer['proof_delta']:
                row['evidence_A'] = row['evidence_B'] = []
        elif number == 4:
            answer['scenario_B']['dimensions']['purpose']['evidence'][0].update(clause_id='ID', quote='This agreement identifies A900 and StudioA.')
            review['checks'].update(semantic_grounding=False, citation_semantics=False)
        elif number == 5:
            answer['scenario_B']['dimensions']['purpose']['explanation'] = 'An advertising prohibition grants editorial use.'
            review['checks']['explanation_accuracy'] = False
        elif number == 6:
            answer.pop('proof_delta')
        elif number == 7:
            answer['scenario_A']['dimensions']['purpose']['evidence'][0]['source'] = 'outside/same-basename.pdf'
        elif number == 8:
            answer['scenario_A']['dimensions']['purpose']['evidence'][0]['page'] = 1
        elif number == 9:
            answer.pop('licensed_party')
        elif number == 10:
            def remove_r1(value):
                if isinstance(value, dict):
                    if value.get('clause_id') == 'R1':
                        value.update(clause_id='G1', quote=case['sources'][0]['clauses'][0]['text'])
                    for v in value.values(): remove_r1(v)
                elif isinstance(value, list):
                    for v in value: remove_r1(v)
            remove_r1(answer)
            review['checks']['source_preservation'] = False
        elif number == 11:
            answer['scenario_B']['status'] = POSITIVE
            answer['scenario_B']['dimensions']['channel']['status'] = POSITIVE
            review['checks']['no_false_affirmatives'] = False
        content = json.dumps(answer, sort_keys=True)
        if review is not None:
            review['content_sha256'] = content_hash(content)
        verdict = judge(content, case, review)
        check('evaluator/E' + str(number).zfill(2) + '/reject', verdict['strict_accepted'], False)
        if number == 4:
            check('evaluator/E04/genuine_quote_not_enough', verdict['checks']['quotation_fidelity']['state'], PASS)
        attacks['E' + str(number).zfill(2)] = verdict
    ne = accept({'feature': {'state': NOT_ELICITED, 'reason': 'Deliberate narrow prompt'}}, {'feature': {'requested': False, 'reason': 'Deliberate narrow prompt'}})
    check('evaluator/E12/unelicited_not_pass_count', ne['state_counts'][PASS], 0)
    check('evaluator/E12/full_contract_cannot_hide_as_unelicited', accept({'feature': {'state': NOT_ELICITED, 'reason': 'claimed'}}, {'feature': {'requested': True}})['strict_accepted'], False)
    check('evaluator/E13/missing_mandatory_check', accept({}, {'semantic': {'requested': True}})['strict_accepted'], False)
    check('evaluator/E14/not_run_mandatory_check', accept({'semantic': {'state': NOT_RUN, 'reason': 'pending'}}, {'semantic': {'requested': True}})['strict_accepted'], False)
    case, answer = controls()
    case.update(quotes_required=False, no_quote_reason='No verified source supplied')
    case['sources'] = []
    content = json.dumps(answer, sort_keys=True)
    attempted_quote = judge(content, case, reviewed(content))
    check('evaluator/E15/unsolicited_quote_still_requires_source', attempted_quote['checks']['quotation_fidelity']['state'], FAIL)
    check('evaluator/E15/no_optional_quote_bypass', attempted_quote['strict_accepted'], False)
    attacks['E15'] = attempted_quote
    for restricted in (False, True):
        case, answer = controls(restricted)
        content = json.dumps(answer, sort_keys=True)
        check('evaluator/positive-control/' + str(restricted), judge(content, case, reviewed(content))['strict_accepted'])
    output = dict(layer='DETERMINISTIC POLICY + EVALUATOR ATTACK CONTROLS; NOT MARKDOWN/LLM/ULIYA/NAS EXECUTION',
        cases_sha256=receipt['cases_sha256'], targeted_cases=16, evaluator_attack_cases=15, positive_evaluator_controls=2,
        checks={'total': len(assertions), 'passed': sum(c['passed'] for c in assertions), 'failed': sum(not c['passed'] for c in assertions), 'unique_ids': len(ids)},
        case_results=case_results, evaluator_attacks=attacks, assertions=assertions,
        failures=[c for c in assertions if not c['passed']])
    save(OUT / 'targeted-tests.json', output)
    print(json.dumps({k: output[k] for k in ('targeted_cases', 'evaluator_attack_cases', 'positive_evaluator_controls', 'checks', 'failures')}, indent=2))
    raise SystemExit(1 if output['failures'] else 0)


if __name__ == '__main__':
    main()
