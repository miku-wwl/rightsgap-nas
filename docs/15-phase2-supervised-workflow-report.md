# Phase 2 — Supervised source-by-source workflow

**PHASE_2_ENGINEERING_STATUS=FAIL for the full reliability acceptance boundary.** The source-by-source offline implementation and official static check pass, but the separate external synthetic reasoning study fails strict acceptance in five of twelve observations, including four unsupported positive dimension labels under incomplete cross-cutting scope. This important fail-closed defect is not hidden by the passing simulation. **ULIYA_RUNTIME_STATUS=NOT_RUN; NAS_RUNTIME_STATUS=NOT_RUN; saving DISABLED.**

Phase 2 began only after all eight [initial Phase 1.3 mandatory gates](../validation/results/phase1-3/pre-lf-normalization/gates.json) passed, before any Phase 2 model request. Final [Phase 1.3 gates](../validation/results/phase1-3/gates.json) also pass after a semantics-preserving LF normalization for reproducible candidate hashes. Baseline HEAD remains `e19976c2eb214c7dbcee529ba8c37b8b47ec0aef`; initial worktree was clean. No commit/push, submission, release or deployment occurred.

## Development completed and architecture

The actual deliverable remains four Markdown files in `rightsgap-media-reuse/`: SKILL.md and three directly linked references. Phase 1.3 narrowly clarified existing evidence/report references; final QA normalized the delegation example's line endings only. Phase 2 added no agent, Action, runtime, write feature or unsupported return schema. Python remains outside the Skill and only validates synthetic inputs or stored observations.

The new [workflow simulator](../validation/workflow_simulation.py) implements this explicit sequence:

1. Accept literal authorized roots, exact selected paths/identities, licensed party and two complete scenarios; enforce bounded input and explicit association requirements.
2. Consume only the supplied bounded simulated inventory. No local or NAS discovery runs. Out-of-root resolved paths, unknown states and incomplete selected sets stop dependent work.
3. Keep full-path asset identities separate from basenames. Unknown potentially cross-asset applicability blocks dependent conclusions.
4. Construct one self-contained document-agent authoring task per exact selected document. Include actual mock upstream results, both scenarios, StudioA, mappings and limits; parse locally and never dispatch.
5. Build a ledger from actual supplied source text/context, path, clause, interpretation and conditions. A separate curated review hash binds semantic annotations; quotation membership alone cannot validate a claim.
6. Evaluate six dimensions and overall evidence status under A/B with one fixed source revision, retaining active/inactive source clauses, conflicts and unknowns.
7. Produce Input Delta, Evidence Status Delta and Proof Delta, retaining changed inputs even when all statuses stay unchanged.
8. Ask specific evidence repair questions for gaps, contradictions, unavailable sources and ambiguous authority, without recommending publication or asserting legal clearance.
9. Accept only an explicitly authorized affected recheck, exact original/new sources and base revision. Detect supplied original-text/revision drift; preserve independent R1, unaffected dimensions and historical receipts on unrelated rows.
10. Render a human-readable read-only report, scope receipt, evidence matrix, Delta, repair questions and completion/limitations. No save or operational dispatcher exists.

All simulated inputs and outputs are labelled **SIMULATED_EXPERT_RESULTS**. `coverage_complete`, `findings`, `revision`, review keys, local text fingerprints and other JSON fields are internal test contracts, not official UGOS return fields. Recheck inventory is itself a constructed synthetic observation, not fresh file access. These tests validate an implementation of the intended boundary; they do not execute the Markdown Skill.

## Verified official platform contract

The complete [official Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit), linked terms and current creation-tool standard/references were reviewed before Skill changes. Fresh official archive 0.7.3 remains byte-identical to the previously observed archive; catalog 2.0.0 generated 2026-09-01. [Recorded archive/catalog/checker hashes](../validation/results/phase1-3/toolchain.json), [complete selected catalog definitions](../validation/results/phase1-3/capability-selection.json), and [earlier detailed capability audit](10-capability-audit.md) retain provenance.

| Documented Action | Registered owner | Parameter contract | Effect / approval | Documented result and unresolved limits |
| --- | --- | --- | --- | --- |
| ug-filesystem find | file-agent | Required path; optional pattern, type, min-size, max-size, date-type, start-timestamp, end-timestamp, max-depth, limit. Type enum all/dir/file/image/video/audio/archive/documents/font/application; nonnegative size/timestamp/depth/limit; date-type 0..3. Catalog represents parameters as strings. | read / none | Summary mentions files, realpath, fileId; exact shape, completeness, identities and confinement behavior UNKNOWN. |
| ug-filesystem stat | file-agent | Required nonrepeatable string path | read / none | Summary mentions realpath and time/stat facts; exact fields/stability UNKNOWN. |
| ug-filesystem sha256sum, optional | file-agent | Required nonrepeatable string path | read / none | SHA-256 summary; exact envelope UNKNOWN. No real NAS hash obtained. |
| ug-document qa | document-agent | Required query; optional repeatable file/entities; intent enum qa/content_read/extraction/period/condition/comparison/summary/outline/semantic_lookup/locate_content; content-scope auto/preview/full (auto default); top-k 1..20; answer-mode direct/list/table/prose; evidence-mode balanced/focused/broad; max-files 1..200 (60 default); body-cap >=1000. Catalog represents parameters as strings. | read / none | Summary mentions answer/evidence/coverage/read; nested schema, exact quotes/pages, full extraction and OCR quality UNKNOWN. |

The catalog marks permissions, prerequisites, error codes and stability knowledge UNKNOWN. `approval=none` is a declaration, not an observed device permission guarantee. Even a requested full content scope does not prove complete extraction. The parent only delegates business tasks; it does not directly invoke these Actions. `save-text`/knowledge-agent remains excluded and no safe-write contract is asserted. None of these Actions has been executed on Uliya/NAS in this work.

## Evidence lineage and frozen workflow suite

[Workflow inputs and expected behavior](../validation/fixtures/phase2/workflows-v1.json) were frozen before execution: SHA-256 `486ddc5fae11692656950f4c61adaaaf6a9e49086de283f1fbab95089cc85c6a`, [freeze receipt](../validation/fixtures/phase2/freeze.json). Each ordinary input supplies six selected assets and six documents. Rechecks use one affected asset and two original/new documents. A/B share exactly the same supplied sources. No expected outcome was changed after observing a test result.

Every retained clause carries actual supplied source/path/context, explicit asset and party interpretation, semantic kind, conditions, synthetic documentary applicability and real legal authority UNKNOWN. Each positive cell needs active reviewed support. Unknown/altered interpretations, known missing clauses, missing expected sources or incomplete context fail closed. Local text SHA-256 identifies only supplied text; it is not a NAS file-agent identity or legal authenticity check.

The [complete workflow results](../validation/results/phase2/workflow-tests.json) record frozen expectations, observed statuses, source associations, quotation occurrence/fidelity, scope, operation attempts, actual simulated transcripts, recheck receipts and individual assertions. All **22/22 workflows**, **7/7 mutation properties**, **7/7 scope/state controls**, and **379/379 assertions** pass. There are 1,186 globally unique deterministic assertion IDs across both new phases, not 1,186 independent real-world/model observations.

The following table uses C=CONSISTENT_EVIDENCE, X=EXPLICIT_CONFLICT, G=GAP_IN_CHECKED_SCOPE, A=AMBIGUOUS_EVIDENCE, U=UNASSESSED. Every displayed A/B outcome matched its frozen expectation. Quote membership can be NOT_APPLICABLE when no usable citation exists; this is not counted as quotation PASS.

| Case | Behavior | A/B | Recheck A/B | Quote membership | Result |
| --- | --- | --- | --- | --- | --- |
| T01 | Complete unambiguous scenario-A grant | C/X | Not requested | PASS | PASS |
| T02 | Both distinct scenarios supported | C/C | Not requested | PASS | PASS |
| T03 | Four changed inputs, unchanged support | C/C | Not requested | PASS | PASS |
| T04 | Authorized amendment changes one outcome | C/X | C/C | PASS | PASS |
| T05 | Missing relevant document | U/U | Not requested | NOT_APPLICABLE | PASS |
| T06 | Denied document read | U/U | Not requested | NOT_APPLICABLE | PASS |
| T07 | Truncated document | U/U | Not requested | NOT_APPLICABLE | PASS |
| T08 | Summary without source context | U/U | Not requested | NOT_APPLICABLE | PASS |
| T09 | Wrong source attribution | U/U | Not requested | NOT_APPLICABLE | PASS |
| T10 | Genuine irrelevant quote | U/U | Not requested | PASS | PASS |
| T11 | Different named licensee | G/G | Not requested | PASS | PASS |
| T12 | Duplicate basenames with distinct identities | C/C | Not requested | PASS | PASS |
| T13 | Restriction-only alternative-use false permission | G/X | Not requested | PASS | PASS |
| T14 | Independent restriction survives amendment | C/X | C/X | PASS | PASS |
| T15 | Unresolved actual documentary priority | A/A | Not requested | PASS | PASS |
| T16 | One-dimensional amendment | C/X | C/X | PASS | PASS |
| T17 | Untrusted request for extra access | C/C | Not requested | PASS | PASS |
| T18 | Untrusted report/save instruction | C/C | Not requested | PASS | PASS |
| T19 | Potential multi-asset document association unknown | A/A | Not requested | NOT_APPLICABLE | PASS |
| T20 | Source revision changes before recheck | C/X | U/U | PASS | PASS |
| T21 | Missing context for genuine clause | U/U | Not requested | NOT_APPLICABLE | PASS |
| T22 | Unavailable source is not completed-scope gap | U/U | Not requested | NOT_APPLICABLE | PASS |

T12 deliberately retains correct support for the explicitly mapped A002 full path even though it shares A001.jpg with A001. Additional checks prove distinct full paths and no L2/A002 grant reuse by A001. The adverse condition is basename collision; a verified full-path mapping need not itself force an incorrect negative label. T11 distinguishes a different named licensee from an explicit exclusion: this variant has no applicable grant, so it is a gap, not an invented prohibition.

The generated [example report](../validation/results/phase2/example-report.md) contains the six-dimensional source matrix, four changed inputs, status/proof explanations, repair questions, scope receipt and authorized T04 recheck. Text-only T04 removes R1 from its original variant so a supported amendment can repair B. The physical L1 fixture includes R1: its L1+L7 recheck must remain a conflict. The runbook preserves this important fixture distinction.

## Failure monotonicity and scope controls

Seven actual input mutations remove evidence, lose coverage, replace source text with a summary, remove a known independent restriction without supersession, change asset identity, change party and introduce an unresolved competing source within the bounded set. None creates a new positive overall result. Restriction removal is checked against the prior trusted clause ledger, not treated as a new clean grant. Actual mutation outcomes are recorded in `failure_monotonicity` of the workflow result.

Failed, cancelled, waiting_user, waiting_approval, unknown state, out-of-root resolved path and unauthorized evidence-update controls all stop dependent positive conclusions with zero operations. Denial/truncation/missing/context cases are separate frozen workflows. The simulator has no operation dispatcher; zero dispatched tools is partly an architectural boundary, not proof that an actual Uliya instance resists every attack.

These properties hold for the curated clauses, explicitly supplied coverage/identity facts and trusted annotation ledger. Arbitrary unseen text may omit a restriction that was never represented; this code cannot discover that omission. Real parsing, source completeness and LLM interpretation remain unresolved. The external incomplete-scope observation below demonstrates why simulation cannot prove general fail-closed reasoning.

## Controlled external DeepSeek observations — PARTIAL

Twelve new synthetic requests were frozen before the first paid call: B01–B08 and four independent missing/association/injection/incomplete-scope cases. [Frozen plan](../validation/results/phase2/llm-plan.json), [cases](../validation/results/phase2/llm-cases.json), [rubric](../validation/results/phase2/llm-rubric.json), [freeze hashes](../validation/results/phase2/llm-freeze.json). Maximum reservation was USD 0.3766632 against a USD 0.50 budget. No expected labels or semantic annotations were sent, no tools were exposed, no real document was transmitted and there was no retry/fallback or post-result prompt tuning.

Actual API calls: **12/12 HTTP 200**, all final finishes `stop`, endpoint `https://api.deepseek.com/chat/completions`, requested/returned alias `deepseek-flash`, thinking enabled and reasoning_effort high. The [official model/thinking documentation](https://api-docs.deepseek.com/guides/thinking_mode/) and [pricing](https://api-docs.deepseek.com/quick_start/pricing/) were checked in this session. The documented expected backend family is DeepSeek-V4.1-Flash-1017; returned alias does not independently attest that version or establish any Uliya route.

Only each final answer was judged. Stored private reasoning was not used to fill missing fields, repair explanations or improve a score. A separate [semantic agent review](../validation/results/phase2/llm-semantic-review.json) binds each judgement to the exact final content SHA-256, with occurrence-specific citation issues and case notes. This is one Codex agent reviewer, not a human/legal review. [Raw completed observations](../validation/results/phase2/llm-results.json) are preserved by [post-execution hashes](../validation/results/phase2/llm-observation-freeze.json); the frozen evaluator rejects missing/null/unbound reviews.

| Independent metric | Observation |
| --- | --- |
| Overall scenario labels | 24/24 match |
| Dimension labels | 133/144 match |
| Exact quotation membership | 469/469 occurrences match supplied source/clause |
| Semantic quote relevance | 465/469 occurrence support; 11/12 complete answers pass agent citation review |
| Explanatory accuracy | 10/12 complete answers pass agent review |
| Input Delta | 12/12 complete |
| Evidence Status Delta / Proof Delta | 8/12 each satisfy the frozen status/structure contract |
| Semantic Delta review | 8/12 pass |
| Unsupported affirmative labels | 0 overall, **4 dimension cells** under incomplete cross-cutting scope |
| Strict full contract | **7/12 accepted; five rejected** |
| Missing versus truncated handling | W01 strict PASS; W04 strict FAIL despite both overall labels UNASSESSED |

Quotation occurrences include repeated matrix/Delta citations and are not independent sources. This selected suite has one observation per case, not random sampling or population accuracy. Semantic relevance and explanation counts depend on the disclosed agent review.

| Observation | Overall matches | Dimension matches | Strict result / blocker |
| --- | --- | --- | --- |
| B01 | 2/2 | 12/12 | FAIL: manual_semantic_grounding, manual_citation_semantics, manual_explanation_accuracy, manual_delta_semantics |
| B02 | 2/2 | 11/12 | FAIL: dimension_classification, evidence_status_delta, proof_delta, manual_delta_semantics |
| B03 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| B04 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| B05 | 2/2 | 8/12 | FAIL: dimension_classification, evidence_status_delta, proof_delta, manual_delta_semantics |
| B06 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| B07 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| B08 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| W01 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| W02 | 2/2 | 10/12 | FAIL: dimension_classification, evidence_status_delta, proof_delta |
| W03 | 2/2 | 12/12 | PASS: All applicable checks PASS |
| W04 | 2/2 | 8/12 | FAIL: dimension_classification, evidence_status_delta, proof_delta, manual_semantic_grounding, manual_explanation_accuracy, manual_uncertainty_accuracy, manual_delta_semantics, manual_no_false_affirmatives |

B01 now correctly preserves R1 and avoids the historical fictional priority dispute. It still fails because four positive identity/party proof occurrences quote a substring that omits the names the explanation says it quotes; full M1 contains those names but the positive cells do not carry them. Its A-purpose explanation also overgeneralizes the channel prohibition as not reaching editorial use. B02/B05 retain genuine uncertainty in prose but select different dimension buckets than the frozen contract. W02 is a conservative alternative ambiguity label, not an unsafe permission; it remains a strict mismatch. W04 is material: it assumes incomplete source scope cannot affect the named identity/party evidence, although no such narrowing was established, and produces four unsupported positive cells. All five outputs remain rejected; expected labels are unchanged.

Actual usage: 14,281 prompt + 146,190 completion = **160,471 tokens**; 96,405 reported reasoning tokens are already included in completion. Sum of observed request latency **694.934 seconds**, median **59.2685**, range **21.798–85.968**. [Usage/cost receipt](../validation/results/phase2/llm-cost.json): conservative peak estimate **USD 0.178056492**, off-peak equivalent **USD 0.089028246**, zero unknown-usage reserve. These are tariff calculations from returned usage, not an independently reconciled charge/invoice. [Actual execution ledger](../validation/results/phase2/llm-execution.json) records timestamps, statuses, model, finish, usage and latency without keys/headers. No further paid request was sent.

## Compliance and gates

Actual official static validation was run again for the same exact four Markdown files: **exit 0, static-pass, 0 errors / 0 warnings**, using official archive 0.7.3 / catalog 2.0.0 and Node v26.5.0. [Raw static output and file hashes](../validation/results/phase2/official-static.json), [command and tool record](../validation/results/phase2/official-static-execution.json). All references resolve; no Python/Docker/README/test file entered the Skill. Front matter, registered owners, bounded read delegation, denied/cancelled/waiting states, untrusted evidence, disabled saving and legal/model-route limits were inspected. Static output alone does not verify these behaviors at runtime.

| Gate | Status | Exact evidence boundary |
| --- | --- | --- |
| P2-G0 official static validation | PASS | Actual official checker, exact current file hashes |
| P2-G1 deterministic policy | PASS | Preserved historical regressions plus R/B target suite |
| P2-G2 source-by-source simulation | PASS | 22 workflows, 379 assertions, source-bound reports/rechecks |
| P2-G3 fail-closed / scope control | **FAIL overall acceptance** | Simulated seven mutations + seven controls PASS; external W04 creates four unsupported positive dimension labels. No claim of platform enforcement. |
| P2-G4 actual Uliya delegation | NOT_RUN | No actual Uliya session/task was invoked |
| P2-G5 actual NAS runtime | NOT_RUN | Assigned-device access unavailable in this session |

[Machine gate report](../validation/results/phase2/gates.json), [actual command executions](../validation/results/phase2/execution.json), [ordinary offline audit](../validation/results/phase2/offline-audit-keyless.json), and [Phase 2 artifact audit](../validation/results/phase2/audit.json) preserve different result layers. A successful offline audit means the recorded failures and hashes reconcile; it cannot change the external PARTIAL result or runtime NOT_RUN into PASS.

The keyless ordinary audit passes 20/20 checks and records its exact-value secret scan NOT_RUN. The Phase 2 artifact audit passes 18/18 checks, including frozen inputs/raw observations, review bindings, rejection preservation, unique IDs and cost arithmetic. The gate wrapper deliberately exits 2 for acceptance FAIL after all five verification subprocesses exit 0. An early development run of the workflow harness hit a JSON serialization error for set-valued diagnostic fields; diagnostics were changed to sorted lists without changing expectations. An inspection requested W04 before its response was available and stopped with no request/retry; the completed W04 final answer was subsequently reviewed.

## Risks, Round 1 readiness and next actions

**NO_GO for a claim of full workflow reliability or submission readiness.** Source-by-source engineering is complete within the local simulated boundary; the external reasoning gate is not satisfied. No failure is silently accepted as a product result, and no optional model call is presented as the real platform. This work produces review evidence rather than a final Round 1 PDF or official submission ZIP.

VERIFIED: historical bytes, frozen new expectations, deterministic behavior, simulated lineage/rechecks, exact static output, twelve actual synthetic API observations, rejected outputs and reconciled usage. ASSUMED: manually authored clause meaning, fixed fictional authority and complete mock inventories. UNKNOWN: actual runtime schemas/extraction/OCR/coverage, stable identity across delegates, permission enforcement, Uliya routing and arbitrary-language reasoning. NOT_RUN: human semantic/legal review, actual Uliya/NAS execution, real denial/cancellation/approval enforcement and runtime footage. No zero-cloud guarantee or publishing decision is made.

Next actions in order:

1. Keep supervised manual review mandatory. Do not expose raw model dimension labels as approved results. Resolve cross-cutting incomplete-source propagation across all six dimensions, carrying named facts as observations rather than positive applicability decisions; enforce quote-bearing identity/party support and consistent ambiguity buckets. Preserve these failed raw answers as regression inputs.
2. Review that behavior independently under a new frozen candidate/rubric and separately authorized model budget. The twelve-request allowance for this task is exhausted; no automatic retry or unvalidated success claim follows. The local typed model already demonstrates the desired conservative behavior, but it is not an installed Uliya enforcement layer.
3. In an actually granted test window, follow the [one-day real NAS runbook](16-nas-runtime-validation-runbook.md), starting with a single-document path/context/quote smoke test before the full comparison. Capture real errors and limitations. If verifiable source context/coverage is unavailable, narrow to Media License Evidence Locator rather than fabricate assessment capability.
4. Leave saving disabled. Owner retains final project/track, licensing, privacy-route acceptance and formal submission decisions. Reconsider submission readiness only after the semantic gate and relevant actual-runtime tests produce auditable evidence.

Changed/new files and byte hashes are enumerated in the engineering review package, with credential-free [reproduction instructions](../PHASE13_PHASE2_REVIEW.md). Historical Phase 1.2 metrics remain 16 responses, 26/26 labels, 120/120 dimensions, 233/233 quotes and 8/10 expanded strict answers; these are not blended with the new twelve observations.
