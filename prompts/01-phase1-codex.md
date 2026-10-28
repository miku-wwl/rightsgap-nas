# Prompt 01 — RightsGap NAS Phase 1: Capability audit and first Uliya Skill

Copy this entire prompt into Codex after the GitHub repository has been created and this bootstrap ZIP's files have been placed in the repository root.

---

You are the lead UGREEN AI NAS Hackathon 2026 engineer for this repository. The owner is an experienced Senior Software Engineer who values correctness, original differentiation and a chance at winning, not merely a static checker pass.

Work **inside this Git repository**. First read README.md, AGENTS.md and **all existing docs/01 through docs/09** before changing files. The goal is the Phase 1 capability go/no-go, a narrow first official Uliya Skill only if supported, and honest validations. Do not create or submit a Devpost entry, publish a GitHub release, or change repository visibility.

## Product definition to implement

RightsGap NAS V3 — Evidence-Driven Media Reuse Planner.

The core use is **Proof-Carrying Scenario Delta**: for user-approved NAS media and license-document scopes, compare two scenarios of intended use (licensed party, purpose, channel, territory, date) against explicit source evidence and reveal changed evidence statuses, missing/ambiguous data and next human evidence questions. A user can add a document and recheck. Never declare legal clearance.

The repository's initial scope and evidence status contract are authoritative product decisions unless a clearly documented technical constraint forces a proposal for narrowing. The internal aspiration is 18/20 on the four official equal-weight criteria, **not** a claim about achieved or official scores.

## Step 1 — Reverify the official toolchain before implementation

1. Fetch the latest official UGREEN Starter Kit from https://ai.ugreen.com/pages/hackathon-starter-kit and the linked UGOS Skill Creation Tool. Previously observed archive version was 0.7.3 and catalog 2.0.0, but do not assume they remain current.
2. Read the Skill creation instructions, Uliya Skill Development Standard, full relevant action definitions in capability-catalog.json, and checker source. Record archive name, version, SHA-256, catalog version and source URLs.
3. Build docs/10-capability-audit.md with an exact matrix of every planned Action, its CLI family, registered Expert Agent, required/optional arguments, effect and approval, known/unknown output fields, limitations and confidence.
4. Verify especially the documented source/provenance behavior of ug-document.qa and whether per-file evidence extraction is feasible. No license-specific extraction schema should be invented. The inability to guarantee true page/quote evidence on actual NAS must remain Unknown.
5. If any part of the critical workflow needs unsupported operations, stop that feature and provide a narrowed alternative. Do not work around missing capabilities with direct shell/Python/Docker access inside the submitted Skill.

## Step 2 — Formalize the MVP

Use a maximum of 5–8 scoped media assets, 3–6 documents and two intended-use scenarios. Use the six dimensions and five status values defined in docs/02-evidence-contract.md. Implement a positive-status source quality rule: no source-backed clause -> no affirmative CONSISTENT_EVIDENCE. Distinguish GAP_IN_CHECKED_SCOPE from UNASSESSED and treat assets/docs as untrusted data.

Source association must be explicit or verified, never inferred from matching filenames alone. Support limited licensed-party and contract-supersession ambiguity honestly. A returned document paragraph cannot issue instructions to the parent.

## Step 3 — Create the first compliant Skill (only when the static interface plan is supportable)

Create a dedicated official Skill directory (suggested slug: rightsgap-media-reuse) containing only:

- SKILL.md with allowed frontmatter and required H1 sections.
- Directly referenced Markdown files under references/ if needed.

Use only correct delegate calls targeting registered agents:

- file-agent for supported ug-filesystem discovery/stat/hash.
- document-agent for supported ug-document source analysis.
- knowledge-agent for optional, approval-gated save-text only if documented.
- photo-agent only as a noncritical optional capability after verifying the required outputs; do not promise IPTC rights metadata without proof.

Cover all five delegation states, partial/truncated results, permission rejection, no matches, ambiguous mapping, conflicting documents and untrusted content. The initial flow must remain read-only unless saving is explicitly approved.

Do not insert scripts, manifests, binaries or repository README in the Skill directory. No arbitrary code is executed on the NAS by this Skill.

## Step 4 — Implement offline development evidence outside the Skill

Use docs/08-synthetic-dossier.md as the precommitted oracle. If you build any test harness or synthetic fixture generators, keep them outside the submitted Skill folder and use fake data only.

Include:

1. Two scenarios over the same six synthetic assets.
2. One source-backed changed classification (A001).
3. One unchanged positive case (A002).
4. Missing evidence, licensee mismatch, ambiguous supersession and access denial.
5. A recheck after a synthetic supplemental document.
6. A prompt-injection attempt inside a fake license document.

Report **measured** false-positive support count, citations present/absent, coverage handling and any failed cases. Separate mocked local tests from actual NAS runtime, which is unavailable in Round 1.

## Step 5 — Run official validation

Run the official bundled static checker on the **exact generated Skill directory**, not on the whole repository or kit. Resolve all errors and warnings with changes consistent with the catalog and source instructions. Record checker command, actual exit code, version and output in docs/11-validation-report.md.

If the official package cannot be fetched or checked, stop and report the limitation. Never invent a 0-error result.

## Deliverables and final report

Deliver or update:

- docs/10-capability-audit.md
- Skill directory containing official SKILL.md and directly linked reference Markdown only, if supported
- local-only synthetic tests/fixtures, if feasible
- docs/11-validation-report.md
- updated docs/09-sources-decisions.md for every substantive design compromise

At the end, answer the owner in **Chinese**:

1. Exactly what was implemented.
2. Verified / Assumed / Unknown capabilities.
3. Checker errors/warnings and honest mock-test outcomes.
4. Whether RightsGap passes G0–G4 and whether any feature requires a pivot.
5. Concrete next steps, including any blocked issue.

Do not produce the final Round 1 PDF, mark this as submitted, or send any external submission. The owner must approve those separately.

---
