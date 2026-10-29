"""Run frozen synthetic cases. No NAS, network, subprocess or LLM execution."""
import copy
import hashlib
import json
import argparse
from pathlib import Path

from reference_policy import (DIMENSIONS, POSITIVE, CONFLICT, GAP, AMBIGUOUS, UNASSESSED,
                              assess, compare, save_policy)
from clause_fixtures import load_baseline, review_ledger

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Historical oracle regression; writes only new phase results')
parser.add_argument('--output', type=Path, default=ROOT / 'results/phase1-3/regression.json')
destination = parser.parse_args().output.resolve()
if not any(destination.is_relative_to(ROOT / ('results/' + phase)) for phase in ('phase1-3', 'phase2')):
    raise SystemExit('Refusing to overwrite historical evidence; select a Phase 1.3/2 output path')
destination.parent.mkdir(parents=True, exist_ok=True)
ORACLE_HASH = "62c3b0dfec26705f765fcab497d9891cc858694ea546623d489e06286266cc59"
checks, failed, results = [], [], {}
test_ids = set()


def check(name, actual, expected=True):
    if name in test_ids:
        raise ValueError('Duplicate test identifier: ' + name)
    test_ids.add(name)
    ok = actual == expected
    checks.append({"name": name, "passed": ok})
    if not ok:
        failed.append({"name": name, "actual": actual, "expected": expected})


oracle_bytes = (ROOT / "fixtures/oracle.json").read_bytes()
if hashlib.sha256(oracle_bytes).hexdigest() != ORACLE_HASH:
    raise SystemExit("Frozen oracle hash mismatch; evaluation refused")
oracle = json.loads(oracle_bytes)
source_hash = hashlib.sha256((ROOT / "fixtures/oracle-source.md").read_bytes()).hexdigest()
if source_hash != oracle["source_sha256"]:
    raise SystemExit("Frozen dossier hash mismatch; evaluation refused")
corpus = load_baseline()
docs, scenarios = corpus["documents"], corpus["scenarios"]
reviews = review_ledger(docs + [corpus['supplement']])
policy_flags = {'reviews': reviews, 'coverage': True}
negative_expected = negative_false_positive = 0
positive_citations = positive_missing = dimension_citations = dimension_missing = 0
changed_present = changed_absent = 0
baseline = {}

for asset in corpus["assets"]:
    rows, delta = compare(asset, scenarios, docs, **policy_flags)
    changes = [cell for cell in delta['evidence_status_delta'] if cell['status_changed']]
    baseline[asset] = {"rows": rows, "changes": changes, 'three_layer_delta': delta}
    expected = oracle["baseline"][asset]
    check(f"baseline/{asset}/S1-S2/overall", [row["status"] for row in rows], expected)
    for scenario_index, (row, wanted) in enumerate(zip(rows, expected), 1):
        if wanted != POSITIVE:
            negative_expected += 1
            negative_false_positive += row["status"] == POSITIVE
        if row["status"] == POSITIVE:
            positive_citations += bool(row["citations"])
            positive_missing += not row["citations"]
            check(f"baseline/{asset}/S{scenario_index}/all_dimensions_positive",
                  all(row["dimensions"][d]["status"] == POSITIVE for d in DIMENSIONS))
        for cell in row["dimensions"].values():
            if cell["status"] in (POSITIVE, CONFLICT):
                dimension_citations += bool(cell["citations"])
                dimension_missing += not cell["citations"]
        for citation in row["citations"]:
            observed = next(doc for doc in docs if doc["path"] == citation["source"])
            prefix = f"baseline/{asset}/S{scenario_index}/{citation['document_id']}/{citation['clause_id']}/{citation['dimension']}"
            check(prefix + '/source_membership', citation["quote"] in observed["text"])
            check(prefix + '/no_invented_page', "page" not in citation)
    for change in changes:
        changed_present += bool(change["citations"])
        changed_absent += not change["citations"]
check("delta/A001/S1-S2/changed_status_dimensions", [c["dimension"] for c in baseline["A001"]["changes"]],
      ["purpose", "channel", "territory", "time_window"])
check("delta/A002/S1-S2/no_status_changes", baseline["A002"]["changes"], [])

variants = {}
simple_flags = {
    "denied": {"denied": True}, "partial": {"partial": True}, "truncated": {"truncated": True},
    "unknown_coverage": {"coverage": False}, "unknown_state": {"state": "unexpected"},
    "duplicate_basename": {"mapping": False},
    **{state: {"state": state} for state in ("failed", "cancelled", "waiting_user", "waiting_approval")}
}
for name, expected in oracle["negative_variants"].items():
    working = copy.deepcopy(docs)
    scenario = copy.deepcopy(scenarios[0])
    flags = simple_flags.get(name, {})
    if name == "missing_result":
        working = None
    if name in ("missing_source", "out_of_scope_source"):
        working[0]["path"] = "" if name == "missing_source" else "outside/secret.pdf"
    if name in ("missing_quote", "fabricated_quote", "unsourced_summary"):
        working[0]["findings"][0]["quote"] = "" if name != "fabricated_quote" else "A001 is safe for any use."
    if name == "empty_completed":
        working = []  # explicitly fully reviewed empty relevant evidence in this mock
    if name == "licensee_mutation":
        scenario["licensee"] = "StudioC"
    if name.startswith("repair_"):
        working.append(copy.deepcopy(corpus["supplement"]))
        scenario = scenarios[1]
        if name == "repair_unreadable":
            flags = {"denied": True}
        else:
            fact = working[-1]["findings"][0]
            fact.pop("supersedes")
            fact.pop("authority_basis")
            fact["ambiguity"] = "Precedence not established"
            working[-1]["text"] = working[-1]["text"].replace("supersedes only L1 restrictions conflicting with", "claims, with unresolved precedence over L1,")
            fact["quote"] = fact["quote"].replace("supersedes only L1 restrictions conflicting with", "claims, with unresolved precedence over L1,")
            fact['amendments'][0].update(precedence='unknown', quote=fact['quote'])
    variant_reviews = review_ledger(working) if name == 'repair_no_precedence' else reviews
    result = assess("A001", scenario, working, **{**policy_flags, 'reviews': variant_reviews, **flags})
    variants[name] = result
    case_scenario = 'S2' if name.startswith('repair_') else 'S1'
    check(f"negative/{name}/A001/{case_scenario}/overall", result["status"], expected)
    check(f"negative/{name}/A001/{case_scenario}/six_dimensions_retained", set(result["dimensions"]), set(DIMENSIONS))
    negative_expected += 1
    negative_false_positive += result["status"] == POSITIVE

repaired = {}
repair_positive_present = repair_positive_missing = 0
for asset in corpus["assets"]:
    # Two-document affected revision; other rows retain original six-document receipt.
    relevant = [docs[0], corpus["supplement"]] if asset == "A001" else docs
    rows, _ = compare(asset, scenarios, relevant, **policy_flags)
    repaired[asset] = rows
    check(f"repair/{asset}/S1-S2/overall", [r["status"] for r in rows],
          oracle["repair"].get(asset, oracle["baseline"][asset]))
    for scenario_index, row in enumerate(rows, 1):
        for dimension, cell in row["dimensions"].items():
            if row["status"] == POSITIVE:
                repair_positive_present += bool(cell["citations"])
                repair_positive_missing += not cell["citations"]
            for citation in cell["citations"]:
                document = next(d for d in relevant if d["path"] == citation["source"])
                check(f"repair/{asset}/S{scenario_index}/{citation['document_id']}/{citation['clause_id']}/{dimension}/source_membership",
                      citation["quote"] in document["text"])
    if asset != "A001":
        check(f"repair/{asset}/S1-S2/independence_from_A001", rows, baseline[asset]["rows"])

injected = copy.deepcopy(docs)
injected[1]["text"] += "\n" + corpus["injection"]
for asset in corpus["assets"]:
    rows, _ = compare(asset, scenarios, injected, **policy_flags)
    check(f"injection/{asset}/S1-S2/unchanged_results", rows, baseline[asset]["rows"])
    check(f"injection/{asset}/S1-S2/no_operations", [op for row in rows for op in row["operations"]], [])

purpose_only = [scenarios[0], {**scenarios[0], "purpose": scenarios[1]["purpose"]}]
_, mutation_delta = compare("A001", purpose_only, docs, **policy_flags)
check("mutation/purpose-only/A001/S1-S2/isolated_dimension", [c["dimension"] for c in mutation_delta['evidence_status_delta'] if c['status_changed']], ["purpose"])
for asset in corpus["assets"]:
    same_rows, same_changes = compare(asset, [scenarios[0], scenarios[0]], docs, **policy_flags)
    check(f"repeat/{asset}/S1-S1/stable_assessment", same_rows[0], same_rows[1])
    check(f"repeat/{asset}/S1-S1/no_status_delta", same_changes['evidence_status_delta'], [])
    check(f"repeat/{asset}/S1-S1/fixed_scope", docs, corpus["documents"])

save_cases = {
    "audit_only": ({}, 0, False),
    "not_reviewed": ({"requested": True, "approval": "approved", "nonoverwrite": True}, 0, False),
    "denied": ({"requested": True, "reviewed": True, "approval": "denied", "nonoverwrite": True}, 0, False),
    "waiting_approval": ({"requested": True, "reviewed": True, "approval": "waiting_approval", "nonoverwrite": True}, 0, False),
    "collision_unknown": ({"requested": True, "reviewed": True, "approval": "approved"}, 0, False),
    "unverified_completion": ({"requested": True, "reviewed": True, "approval": "approved", "nonoverwrite": True, "completed": True}, 0, False),
    "verified_completion": ({"requested": True, "reviewed": True, "approval": "approved", "nonoverwrite": True, "completed": True,
                             "evidence": {"verified": True, "outputFile": "synthetic/reports/new.md", "contentBytes": 20}}, 0, False)
}
save_results = {}
for name, (inputs, attempts, saved) in save_cases.items():
    outcome = save_policy(**inputs)
    save_results[name] = outcome
    check(f"save/{name}/whole_report/all_assets/attempts", outcome["save_attempts"], attempts)
    check(f"save/{name}/whole_report/all_assets/success", outcome["saved"], saved)

results = {
    "layer": "LOCAL POLICY REFERENCE MODEL WITH MANUAL MOCK ANNOTATIONS; NOT SKILL/LLM/NAS EXECUTION",
    "oracle_sha256": ORACLE_HASH, "oracle_source_sha256": source_hash,
    "checks": {"total": len(checks), "passed": len(checks) - len(failed), "failed": len(failed), 'unique_ids': len(test_ids)},
    "metrics": {"baseline_asset_scenario_rows": 12, "baseline_dimension_cells": 72,
                "negative_asset_scenario_cases": negative_expected, "false_positive_support_count": negative_false_positive,
                "positive_rows_citations_present": positive_citations, "positive_rows_citations_absent": positive_missing,
                "sourced_dimension_cells_citations_present": dimension_citations, "sourced_dimension_cells_citations_absent": dimension_missing,
                "changed_dimensions_explanations_present": changed_present, "changed_dimensions_explanations_absent": changed_absent,
                "repair_positive_dimension_citations_present": repair_positive_present,
                "repair_positive_dimension_citations_absent": repair_positive_missing,
                "negative_variants": len(variants), "save_policy_cases": len(save_cases),
                "denied_approval_cases": 1, "unauthorized_mock_save_attempts": sum(v["save_attempts"] for k, v in save_results.items() if k in ("audit_only", "not_reviewed", "denied", "waiting_approval", "collision_unknown"))},
    "baseline": baseline, "repair": repaired, "negative_variants": variants,
    "save_policy": save_results, "failed_cases": failed, "check_details": checks,
    "limitations": ["Manually labelled terms and mock coverage; no natural-language extraction or authenticity check",
                    "Injection is inert fixture text in this model; actual model resistance is untested",
                    "Save states are simulated; no platform approval or write was executed",
                    "No PDFs/JPEGs generated or parsed; no exact NAS response schema assumed",
                    "No measured Uliya reasoning accuracy or real-world false-positive rate"]
}
destination.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline='\n')
print(json.dumps({"checks": results["checks"], "metrics": results["metrics"], "failed_cases": failed}, indent=2))
raise SystemExit(1 if failed else 0)
