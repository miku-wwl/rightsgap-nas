"""Local policy model only: consumes manual mock annotations, not UGOS or an LLM.

It does not execute the Markdown Skill or extract clauses from PDF/text. The corpus
contains fictional paths and human-labelled terms. This model tests the proposed
status/coverage rules, not the target model's ability to follow them.
"""

DIMENSIONS = ("asset_identity", "licensed_party", "purpose", "channel", "territory", "time_window")
POSITIVE = "CONSISTENT_EVIDENCE"
CONFLICT = "EXPLICIT_CONFLICT"
GAP = "GAP_IN_CHECKED_SCOPE"
AMBIGUOUS = "AMBIGUOUS_EVIDENCE"
UNASSESSED = "UNASSESSED"


def assess(asset, scenario, documents, *, state="completed", coverage=True,
           denied=False, partial=False, truncated=False, mapping=True):
    """All keyword flags are local test controls, not documented platform fields."""
    result = {"asset": asset, "status": UNASSESSED,
              "dimensions": {d: {"status": UNASSESSED, "citations": []} for d in DIMENSIONS}, "citations": [],
              "coverage": coverage, "delegation_state": state, "operations": []}
    if state != "completed" or not coverage or denied or partial or truncated or documents is None:
        result["reason"] = "Unavailable result or incomplete relevant scope"
        return result
    if not mapping:
        result.update(status=AMBIGUOUS, reason="Association requires explicit resolution")
        return result

    observations = []
    for document in documents:
        for finding in document["findings"]:
            if finding["asset"] != asset:
                continue
            if not document.get("path", "").startswith("synthetic/licenses/"):
                result["reason"] = "Missing or out-of-scope source"
                return result
            if not finding.get("quote") or finding["quote"] not in document["text"]:
                result["reason"] = "Absent or fabricated clause"
                return result
            observations.append((document, finding))

    # Known fixture authority/precedence is supplied by the synthetic premise.
    # This is not extraction, cryptographic proof or signature authentication.
    overrides = set()
    selected = []
    for document, finding in observations:
        if finding.get("only_purpose") and finding["only_purpose"] != scenario["purpose"]:
            continue
        if finding.get("supersedes"):
            if not finding.get("authority_basis"):
                result.update(status=AMBIGUOUS, reason="Unresolved supplement authority")
                return result
            overrides.add(finding["supersedes"])
        selected.append((document, finding))
    selected = [(doc, fact) for doc, fact in selected if doc["id"] not in overrides]
    if any(fact.get("ambiguity") for _, fact in selected):
        result.update(status=AMBIGUOUS, reason="Unresolved competing agreements")
        return result

    wanted = dict(zip(DIMENSIONS, (asset, scenario["licensee"], scenario["purpose"],
                                  scenario["channel"], scenario["territory"], scenario["date"])))
    for dimension in DIMENSIONS:
        supported, conflicting = [], []
        for document, finding in selected:
            terms = finding["terms"].get(dimension)
            if terms is None:
                continue
            citation = {"source": document["path"], "quote": finding["quote"], "dimension": dimension}
            matches = (terms[0] <= wanted[dimension] <= terms[1]) if dimension == "time_window" else wanted[dimension] in terms
            if matches:
                supported.append(citation)
            elif dimension in finding.get("exclusive", []) or (dimension == "licensed_party" and wanted[dimension] in finding.get("excluded_parties", [])):
                conflicting.append(citation)
        citations = conflicting or supported
        result["dimensions"][dimension] = {"status": CONFLICT if conflicting else POSITIVE if supported else GAP,
                                           "citations": citations}
        result["citations"].extend(citations)
    statuses = {cell["status"] for cell in result["dimensions"].values()}
    result["status"] = CONFLICT if CONFLICT in statuses else GAP if GAP in statuses else POSITIVE
    return result


def compare(asset, scenarios, documents, **flags):
    rows = [assess(asset, scenario, documents, **flags) for scenario in scenarios]
    changes = []
    for dimension in DIMENSIONS:
        before = rows[0]["dimensions"].get(dimension, {"status": UNASSESSED})
        after = rows[1]["dimensions"].get(dimension, {"status": UNASSESSED})
        if before["status"] != after["status"]:
            changes.append({"dimension": dimension, "before": before["status"], "after": after["status"],
                            "citations": before.get("citations", []) + after.get("citations", [])})
    return rows, changes


def save_policy(*, requested=False, reviewed=False, approval="none", nonoverwrite=False,
                completed=False, evidence=None):
    """Simulates a write boundary; never writes a report or calls a service."""
    if not requested or not reviewed or not nonoverwrite or approval != "approved":
        return {"save_attempts": 0, "saved": False, "approval": approval}
    evidence = evidence or {}
    verified = (completed and evidence.get("verified") is True
                and bool(evidence.get("outputFile"))
                and isinstance(evidence.get("contentBytes"), int) and evidence["contentBytes"] > 0)
    return {"save_attempts": 1, "saved": verified, "approval": approval}
