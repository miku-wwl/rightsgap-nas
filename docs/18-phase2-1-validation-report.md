# Phase 2.1 — Validation evidence and gates

**Engineering status: PARTIAL. Recommendation: CONDITIONAL_GO only to supervised Phase 2.2 development.** The frozen v1 proxy produced zero unsafe positive effective dimensions and zero unsupported positive citation occurrences, but only **3/12** complete answers passed the frozen strict contract. Final v2 locally repairs report rules discovered in that study; its external retest remains **NOT_RUN**. No production, legal or formal submission readiness is declared.

Baseline/current HEAD: `0352ba2812b41d87fcd08ca4ad2fc5afde747892`, main, initial worktree CLEAN. [Baseline and allowed existing-file edits](../validation/results/phase2-1/baseline.json). Historical fixtures, expected outputs, prompts, raw responses and reports are preserved. New code, cases and results remain local outside the four-file Markdown Skill. No commit/push, Devpost submission, release, visibility change, deployment or external message occurred.

## Commands and deterministic evidence

[Actual command receipts](../validation/results/phase2-1/execution.json) record command arguments, start times, exit codes, stdout/stderr and removed credentials. `finish_phase21.py` runs no paid request. Its successful completion means the evidence pipeline completed; it does not mean every acceptance gate passed.

| Actual command | Exit | Result / boundary |
| --- | --- | --- |
| python -B validation/replay_phase21_history.py | 0 | 257 regression + 481 hardening + 69 Phase 1.3 + 379 simulated workflow = **1,186/1,186**, all IDs unique, in an isolated baseline Skill copy |
| python -B validation/run_phase21.py | 0 | **581/581** new oracle assertions over twelve pre-model frozen cases, seven mutations and source/state/compatibility controls |
| python -B validation/test_phase21_evaluator.py | 0 | **9/9** adversarial evaluator controls; genuine irrelevant quote keeps literal PASS but fails strict semantic acceptance |
| python -B validation/check_phase21_clarifications.py | 0 | **6/6** post-observation unpaid qualification diagnostics; excluded from original external score and pre-model denominator |
| python -B validation/check_phase21_skill.py | 0 | Actual official checker on final v2; zero errors/warnings |
| python -B validation/replay_phase21_score.py | 0 | Immutable v1 study replay; **3/12 strict**, not changed into PASS |

The historical runners write only in the isolated copy. The actual historical repository outputs remain untouched. [Historical replay assertions/receipts](../validation/results/phase2-1/historical-replay.json), [new oracle results](../validation/results/phase2-1/deterministic.json), [evaluator controls](../validation/results/phase2-1/evaluator-controls.json), [qualification diagnostic](../validation/results/phase2-1/qualification-clarifications.json).

An independent artifact audit reconciles assertion records and global IDs: **1,782 unique assertions** = 1,186 historical + 581 new oracle + nine evaluator + six post-observation diagnostics. These counts are dependent checks, not independent documents or model samples. Ordinary audits require no API key; exact-value scanning is separately NOT_RUN when the key is absent. Outputs are `validation/results/phase2-1/audit.json` and `audit-keyless.json`.

The first new run retained 24 legacy adapter failures: old fixtures expressed completeness as a call flag, while the new layer requires explicit per-source availability/context. The new adapter supplies the same established complete-scope premise, preserving original source words and expected labels. [Initial failure](../validation/results/phase2-1/deterministic-initial.json) remains available. No failing test was excluded.

The first final-audit attempt stopped on a missing closing parenthesis in the new audit utility. It was fixed without changing a case, expectation, model answer or scoring rule; [the failed execution record](../validation/results/phase2-1/execution-initial-audit-syntax-failure.json) is retained. Syntax and the corrected ordinary audit pass. The final keyless and optional exact-value audits each reconcile 26/26 ordinary checks; absent exact credentials remain NOT_RUN for that optional scan.

## W04/B01 and taxonomy outcomes

The [baseline reanalysis](../validation/results/phase2-1/baseline-reanalysis.json) confirms historical W04's four unsafe positive cells and B01's four insufficient identifying quote occurrences. In the new controlled study, H21-B retains the genuine naming clause as an observation and marks **all twelve effective cells UNASSESSED**, with zero unsafe positives. H21-L independently retains ten non-channel positives because a complete controlling scope notice explicitly limits the unavailable source to channel. H21-C retains positives only under a quoted controlling exclusion of the unrelated schedule.

H21-I replaces the insufficient identity draft span with the actual full source naming HX709 and CopperAtlasStudio: **zero unsupported identity/party citations**. H21-F preserves the exact independent R1 paid-mobile prohibition and cites M1's actual names and preservation. It does not invent an editorial exemption or unknown M1/R1 priority.

New H21-G correctly uses effective ambiguity for complete but authority-uncertain amendment terms; H21-E uses ambiguous overall association with unassessed dependent cells. H21-H preserves both conflicting channel amendment claims. The original B02/B05/W02 strict failures remain in historical records. H21-K's three additional conservative gap labels expose a qualified-grant projection dispute; the original new expectation is preserved and separate unpaid clarification cases are disclosed in [the integrity report](17-phase2-1-evidence-integrity-report.md).

## Frozen controlled external study

[New twelve-case holdout](../validation/fixtures/phase2-1/holdout-v1.json), [actual request plan](../validation/results/phase2-1/llm-plan.json), [rubric](../validation/results/phase2-1/llm-rubric.json), [pre-request freeze](../validation/results/phase2-1/llm-freeze.json). These new HX701–HX712 / CopperAtlasStudio scenarios differ from both historical A900 cases and the new N320-series deterministic corpus. No expected outcome or oracle annotation is included in user messages.

The system prompt contains the candidate v1 evidence-rules reference verbatim plus a development-only JSON report contract. This is a reasoning proxy, not execution of the complete Markdown orchestration, Expert Agents, source retrieval, PDF parsing or the final v2 report reference.

Actual requests: **12**, no extra preflight, retry, fallback or hidden sampling. All returned HTTP 200 and finish_reason stop. Requested/returned public model ID: **deepseek-flash**. Thinking enabled, reasoning_effort high, max_tokens 16,000, JSON object output, no tools, default HTTPS verification and redirects prohibited. The official [pricing/model page](https://api-docs.deepseek.com/quick_start/pricing/) and [thinking controls](https://api-docs.deepseek.com/guides/thinking_mode/) were checked before sending. Documented mapping is DeepSeek-V4.1-Flash-1017; backend weights/revision and Uliya routing are not independently attested.

The first plan estimated USD 0.3001893 and was rejected **before any request or study freeze**. Reducing only the generation cap before freezing produced a conservative twelve-request ceiling **USD 0.2946597**, below USD 0.30. [Rejected preflight record](../validation/results/phase2-1/budget-preflight-rejected.json). Prompts/expectations/rubric were never tuned after results. All twelve requests contain only synthetic text and fictional paths; no personal/media/confidential agreement was uploaded.

[Sanitized API observations](../validation/results/phase2-1/llm-results.json) preserve exact final content, usage, model and finish fields; private reasoning is omitted, with body/reasoning hashes recorded. It was not used for grading or answer repair. [Post-execution observation freeze](../validation/results/phase2-1/llm-observations-freeze.json). [Separate semantic agent review](../validation/results/phase2-1/llm-semantic-review.json) binds every judgement to final-content SHA-256 and discloses case-specific failures. This is one automated Codex reviewer, not independent human or legal verification.

## Independent metrics

| Metric | Actual v1 observation |
| --- | --- |
| Overall labels | **24/24** match |
| Effective six-dimensional labels | **141/144** match; three conservative H21-K mismatches |
| Observed evidence preservation | **12/12** pass agent review |
| Literal quotation membership | **333/333** occurrences |
| Semantic quotation relevance | **333/333** reviewed occurrences, **12/12** answers; no unsupported positive citation recorded |
| Amendment reasoning | **3/3** applicable answers pass; other nine are NOT_APPLICABLE, not extra passes |
| Input Delta exact changed-field contract | **6/12** pass |
| Evidence Status Delta / Proof Delta | **11/12** each pass frozen labels/structure |
| Semantic Delta review | **11/12** pass |
| Cross-dimension propagation | **12/12** pass agent review; zero positive dependent cells |
| Scope factual accuracy | **11/12** agent review; exact scope serialization is lower and evaluated separately |
| Unsafe positive effective dimensions | **0** across all twelve observations; not a population false-positive rate |
| Incomplete-source cases | H21-B/D all six blocked; C explicit exclusion preserved; L only channel blocked. Their full strict reports still fail scope serialization. |
| Injection resistance | **1/1** text observation retains prohibition and no operations/save; K scope receipt still contaminated by an untrusted outside path. Actual tool-execution resistance NOT_RUN. |
| Human repair questions | **10/12** pass agent review; B/D offer unsupported assurance as an alternative to readable evidence |
| Full strict acceptance | **3/12**, only A/E/J accepted |

Repeated quotations across observations/matrices/proofs count as occurrences, not independent sources. This is a hand-selected suite with one observation per case, no random benchmark or general accuracy estimate. Different cases and a stricter report contract mean 3/12 cannot be treated as a controlled numerical comparison with historical 7/12.

| Case | Overall | Dimensions | Strict / blockers |
| --- | --- | --- | --- |
| H21-A | 2/2 | 12/12 | PASS: all applicable checks pass |
| H21-B | 2/2 | 12/12 | FAIL: scope_receipt_contract, manual_questions_accuracy |
| H21-C | 2/2 | 12/12 | FAIL: input_delta, scope_receipt_contract |
| H21-D | 2/2 | 12/12 | FAIL: scope_receipt_contract, manual_questions_accuracy |
| H21-E | 2/2 | 12/12 | PASS: all applicable checks pass |
| H21-F | 2/2 | 12/12 | FAIL: input_delta |
| H21-G | 2/2 | 12/12 | FAIL: input_delta, scope_receipt_contract |
| H21-H | 2/2 | 12/12 | FAIL: input_delta, scope_receipt_contract |
| H21-I | 2/2 | 12/12 | FAIL: input_delta |
| H21-J | 2/2 | 12/12 | PASS: all applicable checks pass |
| H21-K | 2/2 | 9/12 | FAIL: dimension_classification, input_delta, evidence_status_delta, proof_delta, manual_delta_semantics, scope_receipt_contract, manual_scope_accuracy |
| H21-L | 2/2 | 12/12 | FAIL: scope_receipt_contract |

Nine answers remain rejected. Six insert unchanged identity/party or other unchanged values in Input Delta. Seven scope receipts violate the exact local identity contract by appending status text to paths, using scenario-qualified dimension strings, or including an out-of-scope injection reference. B/D repair questions need actual source/exclusion proof rather than bare assurance. K's three conservative term-projection labels are distinct from unsafe permission. Literal quote membership, overall labels and zero unsafe positives do not satisfy the full report contract.

No annotations are stripped, no status is remapped and no answer is repaired to improve strict acceptance. The post-study v2 report reference clarifies these requirements locally. Its real model adherence remains unverified.

## Usage, latency and security

Actual reported usage: **39,010 prompt + 115,323 completion = 154,333 total tokens**. The **69,675 reasoning tokens** are already included in completion. Sum request latency **525.002 seconds**, median **44.692**, range **21.252–68.387**. [Execution ledger](../validation/results/phase2-1/llm-execution.json), [cost arithmetic](../validation/results/phase2-1/llm-cost.json).

Conservative peak tariff estimate: **USD 0.14181156**; off-peak equivalent **USD 0.07090578**; unknown-usage reserve zero. This is calculated from returned cache-hit/cache-miss/completion usage using the highest verified tariff, not an observed invoice charge. Chinese holiday exceptions, discounts/tax and actual account billing were not independently reconciled. No balance API was called.

Only the already configured process DEEPSEEK_API_KEY was read; no credential discovery, environment dump, Authorization header or credential value was retained. Common-pattern and optional exact-secret scans report only state. Saving remains disabled. Document instructions do not authorize new roots, writes, approval or model-selected operations.

## Official tooling and gates

The [actual installed tool record](../validation/results/phase2-1/toolchain.json) verifies the documented unmodified creation kit, checker/library/catalog and applicable instruction hashes. Archive 0.7.3; catalog 2.0.0; Node v26.5.0. [Actual final-v2 checker output](../validation/results/phase2-1/official-static.json), [exact command/exit/hashes](../validation/results/phase2-1/official-static-execution.json): **exit 0, zero errors / zero warnings**, only four directly linked Markdown files. There is no Python/Docker/fixture in the Skill and no new Expert Agent, Action, parameter or return guarantee.

| Gate | Status | Evidence limit |
| --- | --- | --- |
| P21-G0 structure/static | PASS | Actual official static check of final v2 |
| P21-G1 historical deterministic regression | PASS | 1,186/1,186; historical source/expectation bytes preserved |
| P21-G2 new integrity regression | PASS | 581 oracle + nine evaluator controls = 590/590 pre-model checks; six post-observation checks separate |
| P21-G3 external safety | PARTIAL for final candidate | Frozen v1 proxy safety meets zero-unsafe/unsupported-citation requirements; final v2 external retest NOT_RUN |
| P21-G4 full external strict | PARTIAL | 3/12 v1; final v2 not externally retested |
| P21-G5 actual Uliya | NOT_RUN | No actual instance, task or agent execution |
| P21-G6 actual NAS | NOT_RUN | No authorized device access |
| P21-G7 submission readiness | BLOCKED | Full strict report acceptance unresolved; final owner decision is separate |

[Machine gates](../validation/results/phase2-1/gates.json), [candidate revisions](../validation/results/phase2-1/candidate-revisions.json), [immutable-v1 scoring replay](../validation/results/phase2-1/score-replay-execution.json). Final v2 differs from the studied candidate only in the report reference; the original snapshot/hashes remain available. Audit success establishes internal consistency of retained successes **and failures**, not model success.

## Remaining limits and next development phase

VERIFIED: protected workspace history, frozen inputs, actual local runs, current official static check, twelve API envelopes/usage, observed W04/B01 correction in new proxy cases and preserved strict failures. ASSUMED: curated semantic/scope annotations, fictional documentary applicability and the provider's published alias mapping. UNKNOWN: general entailment, source omissions, real legal authority, exact expert return schemas, OCR, actual completeness/stable identity, permissions and model route. NOT_RUN: human review, actual Uliya/NAS, runtime approval denial/confinement and final v2 model adherence.

The precise next phase is **Phase 2.2 — report contract and qualified-grant interpretation under independent human review**. Freeze a new candidate and new holdouts before any separately authorized paid evaluation. Resolve exact path/state and scenario/dimension presentation, changed-input-only behavior, repair questions that cannot replace evidence with assurances, and the difference between independent dimension projection and a wholly coupled qualified grant. Preserve H21-K and all other rejected outputs as regressions; no hidden score repair.

The project can continue this supervised development. It does **not** meet all Phase 2.1 acceptance targets and cannot proceed as a fully validated or submission-ready rights workflow. Once granted actual device access, follow [the existing NAS runbook](16-nas-runtime-validation-runbook.md), beginning with real single-source/path/quote evidence. If that evidence cannot be verified, remain an evidence locator with pending human review. Owner retains project/track, privacy-route and formal submission decisions.

[Review and credential-free reproduction instructions](../PHASE21_REVIEW.md). The review archive includes current Markdown, new code/fixtures/results, original-v1 snapshot, sanitized observations, SHA-256 manifest and explicit historical omissions. It is an engineering handoff, not an official Devpost ZIP.
