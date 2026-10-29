"""Versioned, curated synthetic clause interpretations; NOT UGOS fields.

Expected labels below are authored from literal clauses, never policy output.
Run --freeze once before tests; later runs verify the immutable JSON snapshot.
"""
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

POS = 'CONSISTENT_EVIDENCE'
CON = 'EXPLICIT_CONFLICT'
GAP = 'GAP_IN_CHECKED_SCOPE'
AMB = 'AMBIGUOUS_EVIDENCE'
UNA = 'UNASSESSED'
ROOT = Path(__file__).resolve().parent
ASSET = 'A900'
A = dict(licensee='StudioA', purpose='editorial', channel='own news website', territory='New Zealand', date='2026-11-01')
B = dict(licensee='StudioA', purpose='paid commercial advertising', channel='paid social advertising', territory='worldwide', date='2027-06-01')
DIMS = ('asset_identity', 'licensed_party', 'purpose', 'channel', 'territory', 'time_window')


def fact(clause, kind, quote, terms=None, **extra):
    return dict(asset=ASSET, clause_id=clause, kind=kind, quote=quote, terms=terms or {}, **extra)


def doc(name, *findings):
    return dict(id=name, path='synthetic/licenses/' + name + '.pdf',
                text='SYNTHETIC ONLY; no legal effect.\n' + '\n'.join(f['quote'] for f in findings), findings=list(findings))


def grant(*, broad=False, no_channel=False):
    if broad:
        q = 'A900 is licensed to StudioA for editorial or paid commercial advertising, on its own news website or paid social advertising channels, worldwide including New Zealand, from 2026-01-01 through 2028-12-31.'
        terms = dict(asset_identity=[ASSET], licensed_party=['StudioA'], purpose=['editorial', 'paid commercial advertising'],
                     channel=['own news website', 'paid social advertising'], territory=['New Zealand', 'worldwide'], time_window=['2026-01-01', '2028-12-31'])
    else:
        q = 'A900 is licensed to StudioA for editorial use on its own news website in New Zealand from 2026-01-01 through 2026-12-31.'
        terms = dict(asset_identity=[ASSET], licensed_party=['StudioA'], purpose=['editorial'],
                     channel=['own news website'], territory=['New Zealand'], time_window=['2026-01-01', '2026-12-31'])
    if no_channel:
        q = 'A900 is licensed to StudioA for editorial use in New Zealand from 2026-01-01 through 2026-12-31. No channel grant is stated.'
        terms.pop('channel')
    return fact('G1', 'GRANT', q, terms)


def restriction(channels=None):
    channels = channels or ['paid social advertising']
    q = 'Independent R1 prohibits use of A900 by StudioA on ' + ' and '.join(channels) + ' channels. R1 survives amendments that do not expressly target R1.'
    return fact('R1', 'RESTRICTION', q, prohibits={'channel': channels}, conditions={'licensed_party': ['StudioA']})


def amendment(*, target='G1', dimensions=None, conditional=True, authority=True, preserve=True):
    dimensions = dimensions or ['purpose', 'channel', 'territory', 'time_window']
    terms = {'purpose': ['paid commercial advertising'], 'channel': ['paid social advertising'],
             'territory': ['New Zealand', 'worldwide'], 'time_window': ['2026-01-01', '2028-12-31']}
    terms = {d: terms[d] for d in dimensions}
    condition = {'licensed_party': ['StudioA']}
    if conditional:
        condition['purpose'] = ['paid commercial advertising']
    if target == 'R1':
        condition['channel'] = ['paid social advertising']
    replacement = ', '.join(dimensions)
    words = {'purpose': 'purpose: paid commercial advertising', 'channel': 'channel: paid social advertising',
             'territory': 'territory: worldwide including New Zealand', 'time_window': 'time: 2026-01-01 through 2028-12-31'}
    q = ('For A900 and StudioA' + (' and paid commercial advertising only' if conditional else '') +
         ', M1 replaces only ' + target + ' dimensions ' + replacement +
         ' with these affirmative grant terms: ' + '; '.join(words[d] for d in dimensions) +
         '. All unmentioned dimensions and clauses remain effective.')
    if conditional and target == 'G1':
        q += ' G1 continues to govern editorial uses.'
    if preserve:
        q += ' Independent R1 remains fully effective.'
    relation = dict(target_document='ORIGINAL', target_clause=target, dimensions=dimensions, conditions=copy.deepcopy(condition),
        quote=q, authority_basis='established_in_synthetic_premise' if authority else 'unknown',
        applicability='established_for_fixture', precedence='explicit_clause_relationship')
    return fact('M1', 'AMENDMENT', q, terms, conditions=condition, amendments=[relation])


def cases():
    rows = []

    def add(identifier, documents, scenario, expected, **checks):
        rows.append(dict(id=identifier, asset=ASSET, scenario=copy.deepcopy(scenario), documents=copy.deepcopy(documents),
            coverage=True, expected=expected, checks=checks,
            authority='ASSUMED fixed synthetic documentary applicability; real legal authority UNKNOWN'))

    sparse = doc('ORIGINAL', grant(no_channel=True), restriction())
    add('R01', [sparse], A, GAP, dimension_status={'channel': GAP}, no_restriction_support=True)
    add('R02', [sparse], {**A, 'channel': 'paid social advertising'}, CON, dimension_status={'channel': CON}, active_restriction=True)
    add('R03', [sparse], {**A, 'channel': 'print'}, GAP, dimension_status={'channel': GAP}, no_restriction_support=True)
    partial = [doc('ORIGINAL', grant(), restriction()), doc('AMENDMENT', amendment())]
    add('R04', partial, B, CON, dimension_status={'channel': CON}, active_restriction=True)
    one = [doc('ORIGINAL', grant()), doc('AMENDMENT', amendment(dimensions=['purpose'], conditional=False, preserve=False))]
    add('R05', one, A, GAP, dimension_status={'purpose': GAP}, inactive=[['ORIGINAL', 'G1', 'purpose']])
    add('R06', one, {**A, 'purpose': 'paid commercial advertising'}, POS,
        unaffected=['asset_identity', 'licensed_party', 'channel', 'territory', 'time_window'])
    first = grant()
    first['quote'] = 'Only the qualified combination editorial use on its own news website in New Zealand during 2026 is granted to StudioA for A900; no other combination is granted.'
    second = grant()
    second.update(clause_id='G2', quote='Only the qualified combination paid commercial advertising on paid social advertising worldwide during 2027 is granted to StudioA for A900; no other combination is granted.',
        terms=dict(asset_identity=[ASSET], licensed_party=['StudioA'], purpose=['paid commercial advertising'], channel=['paid social advertising'], territory=['worldwide'], time_window=['2027-01-01', '2027-12-31']))
    # Separate independent grant families; partial matching cells cannot be stitched.
    add('R07', [doc('EDITORIAL', first), doc('ADVERTISING', second)],
        {**A, 'channel': 'paid social advertising', 'date': '2027-06-01'}, GAP, coherent_bundle_required=True)
    add('R08', [doc('ORIGINAL', grant(broad=True))], A, UNA, truncated=True, no_positive=True)
    add('B01', partial, B, CON, active_restriction=True, no_invented_priority=True)
    incompatible = grant()
    incompatible.update(quote='A900 is licensed to StudioA for editorial use only; paid commercial advertising is expressly excluded.',
        terms=dict(asset_identity=[ASSET], licensed_party=['StudioA'], purpose=['editorial']), exclusive=['purpose'])
    disputed = [doc('EARLIER', incompatible), doc('LATER', grant(broad=True))]
    add('B02', disputed, {**A, 'purpose': 'paid commercial advertising'}, AMB, both_sources=['EARLIER', 'LATER'])
    replacement = amendment(target='R1', dimensions=['channel'], preserve=False)
    replacement['quote'] += ' This replacement is limited to paid social advertising; the broadcast prohibition remains unchanged.'
    replacement['amendments'][0]['quote'] = replacement['quote']
    replaced = [doc('ORIGINAL', grant(broad=True), restriction(['paid social advertising', 'broadcast'])), doc('AMENDMENT', replacement)]
    add('B03', replaced, B, POS, inactive=[['ORIGINAL', 'R1', 'channel']], secondary_scenario={**B, 'channel': 'broadcast'}, secondary_expected=CON)
    add('B04', [doc('ORIGINAL', grant(broad=True), restriction()), doc('AMENDMENT', amendment(dimensions=['purpose']))], B, CON, active_restriction=True)
    add('B05', [doc('ORIGINAL', grant()), doc('AMENDMENT', amendment(authority=False, preserve=False))], B, AMB, no_applied_override=True)
    add('B06', [doc('ORIGINAL', grant()), doc('AMENDMENT', amendment(preserve=False))], A, POS,
        no_applied_override=True, secondary_scenario=B, secondary_expected=POS)
    add('B07', [doc('ORIGINAL', grant(broad=True), restriction())], B, CON, active_restriction=True, no_invented_priority=True)
    add('B08', disputed, {**A, 'purpose': 'paid commercial advertising'}, AMB, both_sources=['EARLIER', 'LATER'])
    return rows


def freeze():
    folder = ROOT / 'fixtures/phase1-3'
    folder.mkdir(parents=True, exist_ok=True)
    path, receipt = folder / 'cases-v2.json', folder / 'freeze-v2.json'
    payload = {'version': 'phase1-3-v2', 'layer': 'CURATED SYNTHETIC INTERNAL FIXTURES; NOT UGOS',
               'cases': cases(), 'expected_authoring': 'Literal source requirements authored before candidate policy changes; no model output used.'}
    raw = (json.dumps(payload, indent=2) + '\n').encode()
    if path.exists():
        if path.read_bytes() != raw:
            raise SystemExit('Frozen Phase 1.3 inputs/expectations differ; refusing replacement')
    else:
        path.write_bytes(raw)
        receipt.write_text(json.dumps({'frozen_at': datetime.now(timezone.utc).isoformat(),
            'cases_sha256': hashlib.sha256(raw).hexdigest()}, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'cases': len(payload['cases']), 'sha256': hashlib.sha256(raw).hexdigest()}))


if __name__ == '__main__':
    freeze()
