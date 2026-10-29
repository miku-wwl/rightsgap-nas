# 12 — Phase 1.1 correctness hardening review

Date: **2026-10-29, Pacific/Auckland**. Starting HEAD: `2c828fddb8892913fb2b68410c247fee6c0de0a1`; initial worktree clean. All changes local; no commit, push, release, visibility change, external message or submission.

## Executive summary

**CONDITIONAL GO to Phase 2 architecture and controlled report review.** The identified document-level supersession defect was reproduced and fixed at clause/dimension level. A partial amendment no longer removes an independent restriction. Scenario comparison now reports input, evidence-status and proof layers, including unchanged support. Saving is explicitly disabled. Real synthetic images and PDFs now exist outside the Skill.

Deterministic acceptance: **738/738 assertions, 738 unique IDs, zero failures**; **0 false-positive support / 52 named non-positive case evaluations**. Real local fixture extraction/rendering passes. Exact current Skill: **official checker exit 0, zero errors/warnings/info**. These findings do not establish Uliya or NAS behavior.

A separate **local phi4-mini blind text-only probe is PARTIAL**: final classifications matched **2/3**, exact quotes **1/3**, and the required A002 input delta **0/1**. None is accepted as a complete verified RightsGap report. This is a material model-reliability risk, not a reason to hide failures or claim all behavior passed.

## Defects found and exact fixes

| Defect | Fix / boundary |
| --- | --- |
| A `supersedes` reference suppressed every finding in the original document | `reference_policy.assess` now applies scoped edges to `(original document, original clause, affected dimension)` only. Source observations remain visible with active/inactive state. |
| Independent clauses could disappear with a use-only amendment | Separate clause identities and kinds; independent restrictions veto broad grants. Inactive dimensions do not remove unrelated clauses, parties or unresolved ambiguity. |
| Unknown authority/priority could be treated as an override | Edge validation requires explicit target, affected dimensions, conditions and separately labelled synthetic authority/applicability/precedence basis. Unknowns preserve ambiguity; missing source fails closed. |
| Comparison omitted changed inputs with unchanged statuses | `compare` returns `input_delta`, `evidence_status_delta` and `proof_delta`. Status rows include `status_changed=false` rather than disappearing. |
| Existing quote membership was treated as sufficient evidence | A separate trusted manual fixture-review ledger binds source identity, clause, interpretation and relations. Missing/mutated bindings fail closed. This is controlled fixture review, not automatic semantic verification. |
| Omitting a known independent finding could evade the policy | Expected reviewed clauses are reconciled with observed clauses; missing or altered known findings yield UNASSESSED. Unknown source text still requires real semantic review. |
| Coverage defaulted to true | Coverage now defaults to unknown/false. `completed` without independently supplied completed relevant scope cannot produce a positive or completed-scope gap. |
| 206 assertions contained only 158 unique names | Regressions now include scenario/document/clause/dimension where relevant and reject duplicate IDs; cross-suite uniqueness is checked. There were 48 repeated-name occurrences before this change. |
| Conditional save command remained present despite unknown safe-write behavior | Removed knowledge-agent mapping and save delegation from the current candidate. Even alleged approval cannot enable saving; chat report only. |
| Fixtures were fictional path labels | Added six original JPEGs and nine real PDFs, extracted text, page counts, hashes and rendered visual evidence. |
| Exploratory local-model requests leaked expected status labels | Preserved that run as exploratory and excluded its label matches from accuracy evidence. A corrected blind run withheld labels, with no other prompt tuning. |

All local structures above are **test/report contracts**, not invented UGOS response fields or a NAS program. The submitted candidate remains Markdown orchestration using documented file-agent/document-agent ownership and supported read capabilities.

## Clause-level supersession demonstration

Before the fix, the mandatory attack reproduced **CONSISTENT_EVIDENCE instead of EXPLICIT_CONFLICT**. Raw evidence: [pre-fix-defect.json](../validation/results/phase1-1/pre-fix-defect.json). This is a newly discovered historical false positive; the earlier 0/29 metric never covered this case.

The versioned physical variant uses [L1](../validation/fixtures/physical/licenses/L1_A001.pdf) and [partial L7](../validation/fixtures/physical/licenses/L7_A001_amendment.pdf):

| Original clause/dimension | L7 relationship | Current treatment for S2 |
| --- | --- | --- |
| L1 grant: purpose, channel, territory, time | Explicitly replaces these use restrictions for A001 / StudioA / paid commercial advertising | Only these four grant dimensions become inactive; L7 supplies their replacement evidence. |
| L1 grant: asset identity and licensed party | Unaffected | Original source remains active. |
| L1 independent R1: channel prohibition | No amendment target; other original terms preserved | R1 remains active and conflicting. |

Exact surviving R1 clause:

> Independent restriction R1: digital/social advertising is prohibited for A001 for StudioA; this restriction survives any amendment to the use grant.

Final result is **EXPLICIT_CONFLICT**, including when the policy uses text actually extracted from the two real PDFs. The report retains the R1 citation and the original grant's source, rather than deleting L1. Every edge records original agreement/clause, amendment/clause, dimensions, conditions, source relationship and authority/precedence basis.

The authority basis is an **Assumed fictional fixture premise**; documentary wording and applicability are assessed within that premise. Real legal authority remains **Unknown**. No signature recognition or legal authentication is claimed.

The original frozen repair case, which has no independent R1, still produces its original expected positive repair result. The physical R1 variant is separately versioned; it does not rewrite the original oracle.

## Three-layer Scenario Delta examples

A002 uses the same L2 source and licensed party in both scenarios:

| Dimension / input delta | A | B | Evidence status A → B |
| --- | --- | --- | --- |
| Purpose | editorial | paid commercial advertising | CONSISTENT_EVIDENCE → CONSISTENT_EVIDENCE |
| Channel | own news website | digital/social advertising | CONSISTENT_EVIDENCE → CONSISTENT_EVIDENCE |
| Territory | New Zealand | worldwide | CONSISTENT_EVIDENCE → CONSISTENT_EVIDENCE |
| Date | 2026-11-01 | 2027-06-01 | CONSISTENT_EVIDENCE → CONSISTENT_EVIDENCE |

Proof for all four rows is the actual clause in [L2_A002.pdf](../validation/fixtures/physical/licenses/L2_A002.pdf):

> A002 is licensed to StudioA for editorial use on its own news website and for paid commercial advertising on digital/social advertising channels, worldwide including New Zealand, from 2026-01-01 through 2028-12-31.

Explanation: each changed intended input remains inside the explicitly modelled terms; the source did not change. Each proof row carries source/clause, dimension, A/B statuses, explanation and uncertainty. This is documentary consistency for the evaluated dimensions, not clearance.

A004 keeps overall **GAP_IN_CHECKED_SCOPE** in both scenarios, but its channel changes **CONSISTENT_EVIDENCE → GAP_IN_CHECKED_SCOPE**. The actual [L3 clause](../validation/fixtures/physical/licenses/L3_A004.pdf) says “StudioA may publish A004 online on its own news website.” It supports the first website channel; it does not establish the advertising channel. This is a gap in the fully reviewed fixture scope, not an invented prohibition. The channel change stays visible alongside the four input changes and other unresolved dimensions.

Machine-readable examples: [hardening.json](../validation/results/phase1-1/hardening.json), `delta_examples`. A/B uses one fixed source revision. Adding L7 is a separate evidence revision, never an input change disguised as new evidence.

## Test results and denominators

Original bytes preserved:

- `fixtures/oracle.json`: `62c3b0dfec26705f765fcab497d9891cc858694ea546623d489e06286266cc59`.
- `fixtures/oracle-source.md` and original docs/08: `10b9fdc4658cd194acf8bb78175677c596963440ff889d6ee617df460484ab31`.
- New separately frozen [adversarial-v1 expectations](../validation/fixtures/adversarial-v1-expected.json): `99dfd337e04a77e7a780310b5ff87186d68da12f353ad049c8e6bbaa60b71fbc`.

The new expectations were written and hashed before policy changes. Old `results/offline.json` and old checker output remain untouched. New results live under `results/phase1-1/`.

| Layer / command | Actual result |
| --- | --- |
| `python -B validation/run_offline.py` | Exit **0**; **257/257** assertions; **257** unique IDs. Original baseline/repair statuses and all 20 original negative expectations unchanged. |
| `python -B validation/run_hardening.py` | Exit **0**; **481/481** assertions; **481** unique IDs. |
| Cross-suite ID reconciliation | **738 assertions / 738 unique IDs**, zero duplicates. |
| Reference regression negatives | **0 false-positive support / 29** named case evaluations. |
| New adversarial + mutation negatives | **0 / 23**: 18 non-positive adversarial cases + five mutations. |
| New adversarial cases | **20/20** overall expected outcomes, including two positive controls. |
| Additional mutations | **5/5**: remove known finding, remove known clause text, alter interpretation, unknown coverage, truncation. All fail closed. |
| New citation assertions | **358/358** source-membership/manual-review-binding checks; not 358 independent documents. |
| Baseline positive citation coverage | **3/3** positive asset/scenario rows; **33/33** supported/conflicting dimension cells have citations. |
| Baseline actual status changes | **5/5** retain explanations; A002 additionally has four unchanged status rows with four proof rows. |
| Save boundary | All seven regression inputs yield **zero save attempts**, including alleged approved/verified completion. |

The two former positive-save expectations were deliberately withdrawn because the current feature is disabled, not because an amendment test failed. Their old outcomes remain in historical Phase 1 evidence. No frozen oracle value was changed.

The 20 cases cover partial amendments with/without independent restrictions; unknown authority, applicability and priority; missing amendment source; competing amendments; unrelated asset; different party; one-dimension change; preserved restrictions; removed clauses; a real but irrelevant quote; conflicting findings within one document; wrong source; missing semantic review; traversal; unknown coverage; missing target; and unresolved original conflict. Additional local command round trips cover spaces, apostrophes, Unicode, duplicate basenames and command/instruction-shaped data. No shell command, expert or NAS operation is executed by those tests.

Raw results: [regression.json](../validation/results/phase1-1/regression.json), [hardening.json](../validation/results/phase1-1/hardening.json), [process exit records](../validation/results/phase1-1/test-execution.json). Exact IDs and failed-case arrays are retained; all deterministic failure arrays are empty.

## Real synthetic fixture evidence

[Physical manifest](../validation/fixtures/physical/manifest.json) contains file identities, SHA-256, page counts, extracted text, dimensions and the actual-source partial-amendment result. Dataset:

- **6 original JPEGs**, 800×520, explicit fixture mappings, decoded/verified with Pillow; geometric test cards only, no people or third-party images.
- **6 base license PDFs**, **1 partial amendment**, **1 image-only scanned edge PDF**, **1 inert prompt-injection PDF**: **9 PDFs**, one page each.
- Every PDF visibly states **SYNTHETIC TEST DOCUMENT — NOT LEGALLY OPERATIVE**. Eight text PDFs yield the expected clauses; the image-only scan has **zero extracted text characters**, as intended. No OCR was run or inferred.
- All nine PDFs rendered with local Poppler. [PDF contact sheet](../validation/results/phase1-1/pdf-contact-sheet.png) and [media contact sheet](../validation/results/phase1-1/media-contact-sheet.png) visually inspected: no clipping/overlap, readable labels and deliberate scan limitation.
- Local versions: reportlab **5.1.0**, pypdf **6.21.4**, Pillow **13.0.0**. Optional fixture dependencies were installed into an isolated temporary directory, not the project Skill or global runtime; pinned in [requirements-fixtures.txt](../validation/requirements-fixtures.txt).

These PDFs are fixture documents, not the final Round 1 PDF. All nine must not be silently treated as one initial audit: select the six base sources, then small explicitly authorized variant subsets. The physical L1 includes independent R1 and is labelled a Phase 1.1 variant. The original frozen text corpus remains unchanged.

## Delegation reliability and local model probe

The Skill directly links a [fully instantiated synthetic example](../rightsgap-media-reuse/references/delegation-example.md). It includes literal roots, exact paths, asset identities, party, both scenarios, associations, upstream observations and scope bounds. The local builder accepts only the two current read-only registered targets, rejects missing context/traversal and quotes a single instruction argument. Round-trip tests are local argument-parsing evidence only; NAS path resolution and Uliya parsing remain Unknown.

A local Ollama service was available, so three fixed text probes were run with **phi4-mini:latest**, temperature 0, context request 4096, output cap 450. The first exploratory request builder accidentally included expected labels. That run remains preserved but its status matches are excluded from accuracy claims. A corrected blind run removed expected labels from the actual user messages without tuning other prompt wording. Exact prompts were saved before each run. Model digest is recorded in [local-model-identity.json](../validation/results/phase1-1/local-model-identity.json). These prompts exercise policy ideas, not the full Markdown Skill, registered experts or NAS.

| Probe metric | Observed result |
| --- | --- |
| Blind final classification agreement | **2/3**; A002 incorrectly labelled EXPLICIT_CONFLICT |
| Blind exact quote present in supplied text | **1/3**; partial-restriction answer spliced nonadjacent clauses; A002 invented a quote from its own explanation |
| Required A002 four-dimensional input delta | **0/1**; wrong identifiers and invented conflicts between scenario inputs |
| Explicit `save_requested=false` output | **2/3**; third omitted the field, not an observed write |
| Fully accepted product-quality answers | **0/3** on manual review |

The blind injection case had the expected final label, a genuine restriction quote and save=false, but its input delta used a use-value rather than a dimension identifier. One inert sample does not demonstrate robust injection resistance. The deterministic injection test merely verifies inert-data handling. **Model-level prompt-injection resistance is not established.** No tool execution or save occurred in either text-only probe. Successful request completion is not a semantic PASS.

Blind raw output: [local-model-blind.json](../validation/results/phase1-1/local-model-blind.json); actual blinded messages: [local-model-blind-prompts.json](../validation/results/phase1-1/local-model-blind-prompts.json); manual review: [local-model-blind-review.json](../validation/results/phase1-1/local-model-blind-review.json). Exploratory raw output, prompts and review remain at their original `local-model*.json` paths. This layer is **PARTIAL**, kept separate from 738 deterministic passes.

## Static validation evidence

Rechecked the current Starter Kit link; it still identifies archive **0.7.3**, SHA-256 `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`. Catalog **2.0.0**, checker format **2.0.0**; official selected declarations and original checker source remain authoritative. No new CLI/Action/parameter or output schema was added.

Actual unmodified checker command:

```powershell
node "D:\Ollama\Temp\rightsgap-phase1-20261029\extracted\uliya-skill-kit\scripts\check-skill.mjs" "D:\workshop\oct\rightsgap-nas\rightsgap-media-reuse"
```

Result: **exit 0**, `static-pass`, **0 errors / 0 warnings / 0 info**, diagnostics `[]`, empty stderr, Node **v26.5.0**. Package: **4 Markdown files, 29,185 bytes**; every reference directly linked; no scripts, binaries, PDFs, images, README or runtime inside the package.

| Skill-relative file | Actual checked SHA-256 |
| --- | --- |
| SKILL.md | `2dee4f62b99ee2da2d4998e372a28d8d2de1954f4abd0f9b95f2ddad8d98eddd` |
| references/evidence-rules.md | `8e3ecbbd220f434f2b07e1ece4cf157dfc6f9d33f3ab7aa84569733f4e73cb6a` |
| references/report-and-recheck.md | `f9ff95e210c7e96312f657e07faca48ca76892d62512b7d7a51319cd59332732` |
| references/delegation-example.md | `06932d6856d0f37af41a6963ddc626e7f4d10a57e72970c875d4652eb0a3534f` |

[Checker output](../validation/results/phase1-1/checker.json), [execution metadata](../validation/results/phase1-1/checker-execution.json), [stderr](../validation/results/phase1-1/checker.stderr.txt). Static PASS does not certify semantic correctness, installation, approval enforcement or NAS runtime.

Final [read-only review](../validation/results/phase1-1/final-review.json) confirms current Skill hashes, 738 globally unique IDs, 15 physical file identities, working local links, preserved original oracle hashes and unchanged historical Git content. Historical Windows JSON line endings were compared with Git normalization; original files were not rewritten. A [fresh official archive download](../validation/results/phase1-1/toolchain.json) matches the inspected archive SHA-256 exactly.

## Remaining failure modes; Verified / Assumed / Unknown

- **Verified:** reproduced old false positive; scoped clause/dimension fix on synthetic data; frozen-oracle regression; unique IDs; three-layer delta; manual-review-binding rejection tests; actual local PDF/image extraction/rendering; read-only package and official checker result.
- **Assumed:** trusted fixture annotations correctly express their limited fictional clauses, and explicitly established fictional authority/applicability premises can be used for these tests. They do not authenticate contracts.
- **Unknown:** arbitrary language entailment, omissions of previously unseen restrictions, actual expert source/coverage fidelity, legal authority, real file-to-agreement applicability, OCR on NAS, data routing, platform permissions, path confinement, model variability and actual device installation/execution.
- **Observed limitation:** blind local phi4-mini produced an incorrect A002 classification and inaccurate explanation/proof. Status agreement alone is not enough. A local source ledger is not a deployable semantic validator and is never invoked by the Markdown Skill.
- **Save:** disabled. Neither chat consent nor mock approval can supply unknown non-overwrite behavior. A future feature needs separately documented safety and workflow approval; no bypass is proposed.

## Updated G0–G4 and recommendation

| Gate | Current assessment |
| --- | --- |
| G0 capability fidelity | **PASS for the narrowed static interface plan**; only supported read-only expert ownership is active. Source-output guarantees still Unknown. |
| G1 evidence safety | **PARTIAL overall**; deterministic reference controls PASS with 0/52 false-positive support. Actual model semantic grounding not passed/verified. |
| G2 counterfactual correctness | **PARTIAL overall**; clause-level and three-layer deterministic cases PASS. Blind local A002 classification/explanation fails; Uliya behavior Unknown. |
| G3 approval/least privilege | **PASS for the local read-only design**, **PARTIAL for platform behavior**. Saving disabled; no denied approval bypass; actual NAS confinement not tested. |
| G4 Uliya technical validation | **Static portion PASS**, **overall PARTIAL**: installation, compatibility and actual NAS execution NOT RUN. |

Proceed to **Phase 2 under CONDITIONAL GO**: use this bounded Markdown design and real synthetic dataset for source-by-source human walkthroughs, then validate the actual assigned Uliya configuration when access is granted. Do not present local model answers as acceptable product reports without checking source clauses, conditions and all delta layers. If target QA cannot supply verifiable context/coverage, stop affirmative comparison and narrow to the evidence locator. Keep saving disabled. Owner retains project/track and formal submission decisions.

The 18/20 target remains an internal aspiration; no achieved score, finalist prediction or legal/NAS clearance claim is made.
