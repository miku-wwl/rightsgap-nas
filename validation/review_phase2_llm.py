"""Offline scoring of frozen synthetic model observations. Never sends requests.

Semantic judgements are a separate, content-bound agent review, not a human
review or an automatic entailment oracle. Raw reasoning is never used to repair
the final answer. Rejected answers stay rejected and raw results stay unchanged.
"""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

from strict_evaluation import MANUAL, content_hash, judge

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'validation/results/phase2'


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def inspect(identifier):
    case = next(c for c in load('llm-cases.json')['cases'] if c['id'] == identifier)
    result = next(r for r in load('llm-results.json')['responses'] if r['id'] == identifier)
    answer = json.loads(result['raw_response']['choices'][0]['message']['content'])
    quotes = {}
    def compact(value):
        if isinstance(value, dict):
            if 'quote' in value:
                key = (value.get('source'), value.get('clause_id'), value['quote'], value.get('page'))
                quotes.setdefault(key, 'Q' + str(len(quotes) + 1))
                return quotes[key]
            return {k: compact(v) for k, v in value.items()}
        return [compact(v) for v in value] if isinstance(value, list) else value
    print('SOURCES', json.dumps(case['sources']))
    print('ANSWER', json.dumps(compact(answer)))
    print('QUOTE_MAP', json.dumps([dict(ref=v, source=k[0], clause_id=k[1], quote=k[2], page=k[3]) for k, v in quotes.items()]))


def score():
    freeze = load('llm-freeze.json')
    for path, wanted in freeze['hashes'].items():
        if hashlib.sha256((OUT / path).read_bytes()).hexdigest() != wanted:
            raise ValueError('Frozen study artifact changed: ' + path)
    if hashlib.sha256((ROOT / 'validation/strict_evaluation.py').read_bytes()).hexdigest() != freeze['strict_evaluator_sha256']:
        raise ValueError('Frozen strict evaluator changed')
    cases = load('llm-cases.json')['cases']
    results = load('llm-results.json')['responses']
    if len({r['id'] for r in results}) != len(results):
        raise ValueError('Duplicate observations')
    reviews = load('llm-semantic-review.json')['reviews'] if (OUT / 'llm-semantic-review.json').exists() else {}
    observations = []
    for case in cases:
        result = next((r for r in results if r['id'] == case['id']), None)
        if not result or result['api_status'] != 'SUCCESS':
            observations.append(dict(id=case['id'], state='NOT_RUN', strict_accepted=False))
            continue
        raw = result['raw_response']
        choice = raw['choices'][0]
        content = choice['message']['content']
        review = reviews.get(case['id'])
        verdict = judge(content, case, review, finish_reason=choice.get('finish_reason'), tool_calls=choice['message'].get('tool_calls'))
        review_bound = review and review.get('content_sha256') == content_hash(content)
        reviewed_quotes = bool(review_bound and review.get('all_quotation_occurrences_reviewed') is True)
        irrelevant = set(review.get('semantically_insufficient_quote_paths', [])) if review_bound else set()
        quotes = verdict['exact_citations']
        if irrelevant - {q['path'] for q in quotes}:
            raise ValueError('Review references nonexistent citation occurrence')
        answer = json.loads(content)
        observations.append(dict(id=case['id'], state='PASS' if verdict['strict_accepted'] else 'FAIL',
            strict_accepted=verdict['strict_accepted'], verdict=verdict,
            expected_overall=case['expected']['overall'],
            scenario_label_matches=sum(a == b for a, b in zip(verdict['observed_overall'], case['expected']['overall'])),
            dimension_matches=sum(verdict['dimension_matches']),
            exact_quotes=sum(q['exact'] for q in quotes), quote_occurrences=len(quotes),
            semantic_quote_reviewed_occurrences=len(quotes) if reviewed_quotes else 0,
            semantic_quote_supported_occurrences=len(quotes) - len(irrelevant) if reviewed_quotes else None,
            content_sha256=content_hash(content),
            unsupported_positive_scenario_labels=sum(answer.get(n, {}).get('status') == 'CONSISTENT_EVIDENCE' and case['expected']['overall'][i] != 'CONSISTENT_EVIDENCE' for i, n in enumerate(('scenario_A', 'scenario_B'))),
            unsupported_positive_dimension_labels=sum(answer.get(n, {}).get('dimensions', {}).get(d, {}).get('status') == 'CONSISTENT_EVIDENCE' and target != 'CONSISTENT_EVIDENCE'
                for i, n in enumerate(('scenario_A', 'scenario_B')) for d, target in case['expected']['dimensions'][i].items()),
            review_notes=review.get('notes', []) if review_bound else ['Semantic review absent or not bound'],
            elapsed_seconds=result['elapsed_seconds']))
    executed = [r for r in observations if r['state'] != 'NOT_RUN']
    latencies = [r['elapsed_seconds'] for r in executed]
    metric = lambda field: sum(r[field] for r in executed)
    manual_pass = lambda key: sum(r['verdict']['checks']['manual_' + key]['state'] == 'PASS' for r in executed)
    check_pass = lambda key: sum(r['verdict']['checks'][key]['state'] == 'PASS' for r in executed)
    summary = dict(requested_cases=len(cases), executed_observations=len(executed),
        strict_accepted=sum(r['strict_accepted'] for r in executed), strict_total=len(cases),
        scenario_labels=dict(matched=metric('scenario_label_matches'), total=2 * len(executed)),
        dimension_labels=dict(matched=metric('dimension_matches'), total=12 * len(executed)),
        exact_quotation_membership=dict(matched=metric('exact_quotes'), total=metric('quote_occurrences')),
        semantic_quote_relevance=dict(supported=sum(r['semantic_quote_supported_occurrences'] or 0 for r in executed), reviewed=metric('semantic_quote_reviewed_occurrences'), total=metric('quote_occurrences'), method='Agent occurrence review, not automatic entailment'),
        semantic_quote_relevance_answers=dict(passed=manual_pass('citation_semantics'), total=len(executed)),
        explanatory_accuracy_answers=dict(passed=manual_pass('explanation_accuracy'), total=len(executed)),
        delta=dict(input_passed=check_pass('input_delta'), status_passed=check_pass('evidence_status_delta'), proof_passed=check_pass('proof_delta'), semantic_passed=manual_pass('delta_semantics'), total=len(executed)),
        unsupported_affirmatives=dict(scenario_labels=metric('unsupported_positive_scenario_labels'), dimension_labels=metric('unsupported_positive_dimension_labels'), semantic_no_false_affirmatives_answers=manual_pass('no_false_affirmatives'), note='Zero adverse-label false positives does not prove adequate positive citation support'),
        missing_or_incomplete_cases={r['id']: dict(state=r['state'], strict_accepted=r['strict_accepted'], observed_overall=r.get('verdict', {}).get('observed_overall')) for r in observations if r['id'] in ('W01', 'W04')},
        latency_seconds=dict(sum=round(sum(latencies), 3), median=statistics.median(latencies) if latencies else None, minimum=min(latencies) if latencies else None, maximum=max(latencies) if latencies else None),
        cost=load('llm-cost.json'),
        limitations=['12 hand-selected synthetic cases; no population accuracy estimate', 'One agent semantic reviewer, no human legal review', 'Response alias is not independent backend attestation', 'No actual Uliya, NAS, approval or tool execution', 'No final answer repaired from private model reasoning'])
    value = dict(layer='EXTERNAL SYNTHETIC TEXT LLM; NOT ULIYA/NAS', status='PASS' if len(executed) == len(cases) and all(r['strict_accepted'] for r in executed) else 'PARTIAL', summary=summary, observations=observations)
    (OUT / 'llm-review.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(status=value['status'], **summary), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inspect', help='Print only sources and deduplicated FINAL answer; never private reasoning')
    args = parser.parse_args()
    inspect(args.inspect) if args.inspect else score()
