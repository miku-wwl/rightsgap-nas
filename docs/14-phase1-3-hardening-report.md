# Phase 1.3 — Policy and validation hardening

Baseline: `e19976c2eb214c7dbcee529ba8c37b8b47ec0aef`. Initial worktree: clean. **PHASE_1_3_STATUS=PASS; PHASE_2_START_AUTHORIZED=YES.** All eight mandatory engineering gates passed. These are deterministic and static engineering results; actual Uliya and NAS execution remain NOT_RUN.

## Observed defects and root causes

The pre-change policy was actually exercised against an editorial grant with no channel term plus an independent paid-social prohibition. It incorrectly returned CONSISTENT_EVIDENCE for an unmentioned website channel, and EXPLICIT_CONFLICT for unmentioned print. The prohibited social channel correctly conflicted. [Before-fix evidence](../validation/results/phase1-3/pre-fix-semantics.json).

The cause was a complement-based restriction representation: `terms.channel=[own news website]` plus `exclusive`. The common `if matches: support.append` path treated that restriction as a grant and treated every alternative as prohibited. A trusted fixture-review binding did not correct this structural error.

The historical evaluator accepted every result without a literal `False` check; `None`, absent semantic fields and incomplete review coverage could escape mandatory failure. Its audit also required a key, an old HEAD and a particular staging state, overwrote historical audit files, and required a local tool path. Those historical sources/results are preserved; new validation is versioned separately.

## Implementation and before/after behavior

| Area | Corrected behavior |
| --- | --- |
| Semantic kinds | Explicit GRANT, RESTRICTION and AMENDMENT internal types. Unknown kinds fail closed. These are local annotations, not UGOS fields. |
| Restrictions | Explicit `prohibits` scope; matching scope gives sourced conflict. A nonmatching prohibition supplies neither support nor an invented prohibition. Complement-shaped old restrictions are rejected. |
| Qualified grants | Reviewed purpose/channel bundles stay coupled. Full positive use needs a coherent grant family or explicit amendment linkage; partial terms from incompatible grants cannot be stitched together. |
| Amendments | Only the targeted original clause/dimensions under established applicability and conditions become inactive. A restriction can be replaced only when explicitly targeted. Other dimensions and restrictions remain visible. |
| Missing observations | Expected selected sources can be supplied explicitly; missing, denied, truncated, unreviewed or altered known clauses cannot create positives. |
| Reasoning contract | Separates documentary applicability, explicit R1 preservation, genuinely unknown priority, and actual legal authenticity/enforceability UNKNOWN. The last fact alone cannot invent a priority dispute. |
| Strict evaluator v2 | PASS / FAIL / NOT_APPLICABLE / NOT_ELICITED / NOT_RUN. Every applicable mandatory check must PASS. Missing/null/unreviewed checks block acceptance; exclusions require trusted test metadata and a reason. |
| Ordinary audit | No credentials, model, NAS or network calls required. Exact-key scan is optional: NOT_RUN when absent. Statistics, source attribution, hashes, IDs, package boundaries and stored static output are checked independently. |
| Historical runners | Write only into Phase 1.3/2 paths; refuse historical destinations. Existing oracle expectations remain unchanged. |

The narrow Skill changes are in its two existing references: explicit grant/prohibition distinctions, coupled conditions, and accurate documentary versus legal uncertainty. No new agent, Action, parameter, backend or save feature was added. Four Markdown files remain the complete package.

Final packaging QA also normalized one residual CRLF in the modified policy and the nine-line delegation example to LF, with no meaning change. This prevents the existing Git line-ending policy from changing checked candidate/source hashes on a later checkout. The two pre-normalization source files, original pre-Phase-2 gate decision, checked hashes and executions remain in [the retained initial gate snapshot](../validation/results/phase1-3/pre-lf-normalization/gates.json). The complete Phase 1.3 gate and Phase 2 local checks were rerun for the final bytes; no frozen/model artifact changed.

## Frozen expectations and preservation

[Baseline manifest](../validation/results/phase1-3/baseline-integrity.json) hashes the starting tracked files and identifies **73 protected historical files**. All 73 remain byte-exact. Original Phase 1/1.1 oracles, docs/13, Phase 1.2 expected results, every Phase 1.2 result and its three historical evaluation scripts are preserved. [Pre-change Skill snapshot](../validation/results/phase1-3/baseline-skill/SKILL.md) retains the exact old four-file candidate for historical hash checks.

New targeted inputs/expected outcomes were frozen separately. A v1 fixture helper accidentally described all four replacement terms even in a one-dimension amendment. This was noticed before candidate policy tests, corrected in a retained v2 input snapshot, and **all 16 expected overall labels remained identical**. V1 and its receipt remain available; this is a source-wording correction, not a label change after a failure.

- [Cases v2](../validation/fixtures/phase1-3/cases-v2.json): SHA-256 `73af7df29252bb2cff48f43f0ae5783dc5b9bc2cda9ca56d619a5c05abfb8516`.
- [Freeze v2](../validation/fixtures/phase1-3/freeze-v2.json), [retained v1](../validation/fixtures/phase1-3/cases-v1.json).
- Original oracle: `62c3b0dfec26705f765fcab497d9891cc858694ea546623d489e06286266cc59`.
- Phase 1.1 oracle: `99dfd337e04a77e7a780310b5ff87186d68da12f353ad049c8e6bbaa60b71fbc`.

The historical Phase 1.2 observations independently reconcile to **16 responses, 26/26 scenario labels, 120/120 dimension labels, 233/233 quotation occurrences and 8/10 historical expanded strict answers**. Both rejected explanations remain rejected in the historical record. Their 100,176 tokens and USD 0.107351964 historical peak estimate remain unchanged. No new model request was used to obtain Phase 1.3 PASS.

## Regression and targeted evidence

| Layer | Actual result |
| --- | --- |
| Historical oracle regression | **257/257**, exit 0; no frozen expectation change |
| Historical hardening regression | **481/481**, exit 0; no regression |
| New target suite | **16 R01–R08/B01–B08 cases**, plus coupled-source/removal controls |
| Strict evaluator attacks | **15 attack cases rejected as required**, with two accepted positive controls |
| New assertions | **69/69**, exit 0 |
| Cross-suite identifiers | **807/807 unique assertion IDs**; not 807 independent model/doc tests |
| Ordinary offline audit | **20/20** checks PASS |
| Audit with DEEPSEEK_API_KEY removed from child environment | **20/20** ordinary checks PASS; exact-value scan **NOT_RUN** |

R01–R08 cover restriction-only false support, actual prohibition, unmentioned alternatives, independent restriction survival, inactive superseded grants, unaffected dimensions, incompatible grants and incomplete evidence. B01–B08 distinguish preserved restrictions, genuine competing priority, explicit restriction replacement, another-clause amendments, unknown authority, condition boundaries, unknown legal authenticity and citation preservation of both sides.

Evaluator attacks exercise missing review, null review, absent quote, genuine irrelevant quote, correct label/wrong explanation, absent Delta, wrong path, invented page, missing field, omitted restriction evidence, prohibited affirmative status, unelicited fields, absent mandatory check and NOT_RUN mandatory review. The irrelevant-quote control retains PASS for quotation membership and still fails semantic acceptance. This verifies rejection gates, not an automatic natural-language entailment solver.

Preparing Phase 2 failure cases exposed another boundary in the new evaluator: `quotes_required=false` initially marked all quote checks NOT_APPLICABLE even if an answer attempted a fabricated quotation. [The actual pre-fix control](../validation/results/phase1-3/optional-quote-before-fix.json) was incorrectly accepted. E15 now requires every attempted quotation to trigger source checks; only a genuinely quote-free, explicitly inapplicable case may use NOT_APPLICABLE. The complete Phase 1.3 gate was rerun successfully before any Phase 2 paid request; expected labels and historical results were unchanged.

An initial source edit produced an indentation error before historical tests could execute. It was corrected, and the captured gate run executes both regressions successfully. No historical output was overwritten during that failed attempt.

Commands, stdout/stderr and actual exit codes: [execution.json](../validation/results/phase1-3/execution.json). Detailed [target tests](../validation/results/phase1-3/targeted-tests.json), [regression](../validation/results/phase1-3/regression.json), [hardening](../validation/results/phase1-3/hardening.json), [ordinary audit](../validation/results/phase1-3/offline-audit.json), [keyless audit](../validation/results/phase1-3/offline-audit-keyless.json).

```powershell
python -B validation/run_phase13_gate.py
```

This command performs only local tests/audits and the official local static check. Reproduction requires Python 3.10+; rerunning the official checker additionally needs Node and the verified kit. No key is required for ordinary auditing.

## Official platform verification and static check

The [current Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit) still links archive 0.7.3. A fresh download matches SHA-256 `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`. Catalog **2.0.0**, generated 2026-09-01; unchanged checker SHA-256 `6a9e8ad164862ab787f45e577c2e2bc98cfb31cea10f5ec291cb6550eb51fb52`. Complete Starter Kit, linked terms, kit instructions/standard/references and selected Actions were reviewed.

Verified declarations remain ug-filesystem → file-agent (find/stat/optional sha256sum) and ug-document → document-agent (qa). Permission prerequisites, exact return schemas, OCR, coverage, stable identities and actual device execution remain UNKNOWN. Full [selected catalog definitions](../validation/results/phase1-3/capability-selection.json) and [fresh provenance](../validation/results/phase1-3/toolchain.json) are outside the Skill.

Actual official check: **exit 0, static-pass, 0 errors / 0 warnings / 0 info**, empty diagnostics/stderr. [Raw output with exact four checked files/hashes](../validation/results/phase1-3/official-static.json), [command/tool/process record](../validation/results/phase1-3/official-static-execution.json). This is static validation only.

## Mandatory decision

| Gate | Result | Evidence |
| --- | --- | --- |
| P13-G1 grant/restriction semantics | PASS | R01–R08 plus reproduced old false positive |
| P13-G2 amendment priority | PASS | B01–B08 with source/condition boundaries |
| P13-G3 mandatory evaluation checks | PASS | 15 rejecting attack controls, two positive controls |
| P13-G4 historical bytes | PASS | 73 protected files unchanged |
| P13-G5 historical regression | PASS | 257 + 481 assertions, no rewritten expectations |
| P13-G6 official static validation | PASS | Exit 0, zero errors/warnings |
| P13-G7 security/authorization | PASS for observed engineering actions | Secret checks, no write dispatcher, unchanged Git HEAD, authorized local changes/research only |
| P13-G8 credential-free audit | PASS | Child environment without key; ordinary checks pass, exact scan NOT_RUN |

[Machine gate decision](../validation/results/phase1-3/gates.json) authorizes automatic Phase 2 engineering. [Passed source hashes](../validation/results/phase1-3/passed-source-hashes.json) identify the exact gated implementation.

VERIFIED: controlled deterministic semantics, strict evaluation rejection, preserved history, local audits and official static result. ASSUMED: the curated interpretation ledger faithfully represents these short fictional clauses. UNKNOWN: arbitrary language entailment, real source completeness, document authority, actual Uliya model behavior and NAS permissions. NOT_RUN: Uliya/NAS execution and platform approval enforcement. Saving remains disabled.

Phase 2 proceeds with supervised simulated expert results, keeping its engineering and actual-runtime gates separate. No Git commit/push, release, visibility change, deployment, external message, Devpost submission or final Round 1 PDF is authorized/performed by this phase.
