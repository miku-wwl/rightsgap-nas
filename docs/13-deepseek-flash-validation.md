# 13 — Phase 1.2 DeepSeek Flash reasoning validation

Date: **2026-10-29**. Starting HEAD: `2807c78764bd109c6af1bce82be83e1ddac53b84`; initial worktree clean. This is a **synthetic text-only external LLM evaluation**. Changes are retained locally for independent review.

## 1. Executive Summary

**Phase 1.2 acceptance: PARTIAL. Decision: CONDITIONAL_GO for supervised Phase 2 architecture and source-by-source walkthroughs.** DeepSeek improved substantially over the historical phi4-mini observations on the same three narrow prompts. It did not pass every expanded reasoning-answer requirement: both new partial-amendment answers introduced an unsupported unresolved-priority statement despite explicitly preserved R1.

| Measured result | Verified observation |
| --- | --- |
| API requests | **16/16 successful evaluations**, plus **1/1 successful connectivity preflight**; no retries or substitutions |
| Overall label agreement | **16/16 requests**; **26/26 individual scenario labels** across the two differently structured suites |
| New-case dimension labels | **120/120** cells match frozen expectations |
| Exact final-answer quotations | **233/233 citation occurrences**; **16/16** responses have only genuine supplied quotations |
| Semantic explanation review | Primary **6/6** narrow probes; new suite **8/10** expanded answers |
| Strict acceptance within elicited new format | **8/10**; both partial-amendment explanations rejected |
| A002 four-input delta | Primary **2/2**; new expanded A002 **2/2**, including status and proof layers |
| False-positive affirmative conclusions | **0/18** expected non-positive overall scenario evaluations; **0/30** expected non-positive new dimension cells |
| Disabled-save declaration | **16/16** explicitly return `save_requested=false`; zero returned tool calls/operations or claimed writes |
| Usage including preflight | **100,176 tokens**: 12,281 input + 87,895 completion, including 57,355 reasoning tokens |
| Estimated expenditure | **USD 0.107351964 peak-price upper estimate**; off-peak equivalent USD 0.053675982; invoice not inspected |

Label agreement, quotation fidelity and strict answer acceptance are separate metrics. The six original prompts do not request a complete matrix, separate status/proof layers or full source paths. Their missing fields are **NOT_ELICITED**, never inferred as passing a complete product report. The expanded format is also a reasoning test, not full Skill execution or an operational scope receipt.

## 2. API Model Identity

Official documentation currently lists `deepseek-flash` as served by **DeepSeek-V4.1-Flash-1017**. The October 17 change log confirms that mapping. [Official model documentation](https://api-docs.deepseek.com/), [official update](https://api-docs.deepseek.com/updates/).

| Identity fact | Evidence / limit |
| --- | --- |
| Provider endpoint actually called | `https://api.deepseek.com/chat/completions` |
| Requested model in all 17 payloads | `deepseek-flash` |
| Actual response `model` in all 17 responses | **`deepseek-flash`** |
| Observed `system_fingerprint` | `bc19ba97cbe016479903222bb1578db6`, identical across this run |
| Expected family | DeepSeek-V4.1-Flash-1017, according to the official ID-to-version mapping |
| Independent backend-version proof | **Unknown**: the response returns the public ID, not a separate version attestation; fingerprint meaning is not independently established |
| Uliya model identity | **Unknown**; this API is not evidence of Uliya's model routing |

No request used `deepseek-v4-pro`, `deepseek-chat`, `deepseek-reasoner` or a legacy alias. A successful public-ID response must not be relabelled as an independently observed version string.

## 3. Test Configuration

The official thinking guide documents `thinking.type=enabled` and `reasoning_effort=high`; temperature has no effect in thinking mode. Requests explicitly set those two thinking controls, JSON output, non-streaming transport and a 16,384-token generation cap. No temperature, tools, file upload, search or model fallback was supplied. [Thinking controls](https://api-docs.deepseek.com/guides/thinking_mode/), [Chat Completions fields](https://api-docs.deepseek.com/api/create-chat-completion/).

The one minimal preflight used a 512-token cap and requested only `{"ok":true}`. It returned HTTP 200, that exact JSON, 86 tokens and 1.077 seconds. Every response had nonempty reasoning content and positive reasoning-token usage. These observations show accepted thinking requests and returned reasoning; the provider does not independently echo/attest its internal effort setting.

Security and spending controls:

- Used the owner's existing `DEEPSEEK_API_KEY` process configuration. Only availability was reported. The value and Authorization headers were never printed, persisted or embedded in code.
- Sent only frozen synthetic text; no personal/confidential documents, local machine paths, real media, PDF uploads or NAS contents were sent.
- Used default HTTPS certificate validation, disallowed redirects, supplied no executable tools and implemented no response-to-operation dispatch.
- Recorded an attempt before sending, allowed one preflight and at most 16 evaluation attempts, and stopped on any request/model-identity error. There were zero errors and no retries.
- Reserved cost at the highest documented tariff before each request. The initial full-plan ceiling, including preflight, was **USD 0.335805**, below the owner's USD 1 limit.
- Final local checks scan every new file for the actual configured secret without displaying it. This is an exact-value leak check, not a proof about every possible encoded secret.

## 4. Evaluation Methodology

Read completely: AGENTS.md, docs/02, docs/10–12, SKILL.md and every reference, reference_policy.py, run_hardening.py and all three historical blind prompt/result/review files. Existing work was preserved. The old deterministic oracle was not used to manufacture LLM answers.

Before any evaluation request, froze eight cases, all 16 final request payloads and a scoring rubric. The three primary system/user message contents are byte-for-byte identical to the original Python `json.dumps` message construction, with expected labels excluded. Each case was sent twice with identical payloads and independent conversations. The five new cases use a separately fixed expanded system prompt; that suite is excluded from the direct model comparison.

| Frozen artifact | SHA-256 |
| --- | --- |
| [New expected results](../validation/fixtures/phase1-2/expected.json) | `148782389252dd933ac8cd6b169c6f986ca19807dfa5be67ec5a9f2c4d187daf` |
| [Actual request plan](../validation/results/phase1-2/deepseek-flash-prompts.json) | `356b18bd9d19129872f5bd843a2f1f301efa558d01dcad98db7f8937b810f436` |
| [Review rubric](../validation/results/phase1-2/review-rubric.json) | `d8b2171a0c36e1cec91f000eb03ea3ebcf495f1ef60967f89101c1eee5ff9c50` |

[Freeze receipts](../validation/results/phase1-2/freeze.json) and [rubric timing](../validation/results/phase1-2/rubric-freeze.json) establish a local chronological freeze, not external preregistration. The runner refuses changed expectations, request text, runner code or protected baseline bytes. No prompts or expected outcomes were tuned after responses. No Skill file was modified.

Evaluation used final `content` only. Provider `reasoning_content` is retained in raw responses but was not used to repair incomplete or incorrect answers. Mechanical checks verify JSON structure, statuses, all changed inputs, source/clause identity, contiguous quote membership, pages and returned operation declarations. Codex separately read **each of the 16 final answers** against the supplied clauses and fixed scenario conditions. [Semantic judgements](../validation/results/phase1-2/semantic-review.json) bind every review to the actual final-content SHA-256. This is one agent evaluator; no independent second reviewer or owner sign-off is claimed.

Every positive/conflicting/ambiguous dimension must have the relevant source context; a real quote alone is insufficient. Proof/status layers may include truthful additional unchanged rows: the fixed instructions require coverage of changed inputs and do not prohibit extra observations. No expectation was changed to accommodate those rows. Missing evidence stays empty with a stated gap. Strict new-answer acceptance requires all applicable structural and semantic checks, including accurate uncertainty.

## 5. phi4-mini vs DeepSeek Comparison

Only the **same three original blind cases** are compared below. Historical phi4-mini has one observation per case; DeepSeek has two. The earlier phi4 exploratory run leaked expected labels and remains excluded.

| Primary metric | phi4-mini:latest, historical 3 observations | deepseek-flash, 6 observations |
| --- | --- | --- |
| Overall classification | **2/3** | **6/6** |
| Genuine contiguous quote | **1/3** | **6/6** |
| Source-grounded explanation | **1/3** | **6/6** |
| A002 four-dimensional Input Delta | **0/1** | **2/2** |
| R1-based amendment explanation | **0/1** | **2/2** |
| Explicit save=false | **2/3** | **6/6** |
| False affirmative overall status | **0/2** non-positive cases | **0/4** non-positive observations |
| Limited probe acceptance | **0/3** | **6/6** |
| Mean measured latency | **14.201 s** | **4.888 s** |
| Native token accounting | Ollama prompt_eval_count 706; eval_count 475; cached prompt count 348 separately reported | API 1,802 input + 4,626 completion = **6,428** total |
| External API cost | Not applicable to local Ollama; compute/electricity unmeasured | **USD 0.005978904** peak estimate for these six calls |

Primary injection observations preserved the prohibition and save boundary for both models. phi4's injection answer still used a use-value instead of a valid dimension identifier, so its limited output fails the requested structure. DeepSeek's two samples do not establish robust injection resistance.

These observations support improvement on these particular prompts. They are not a controlled general benchmark: model/backend/hardware, output cap (phi4 450 versus DeepSeek 16,384), context configuration, thinking/JSON settings, cache state, request date and repetition count differ. Tokenizers and native cache counters differ. The five expanded adversarial cases were not run on phi4 and are not pooled into a comparative accuracy claim.

## 6. Classification Results

| Case / expected label(s) | Repeat 1 | Repeat 2 | Acceptance boundary |
| --- | --- | --- | --- |
| Primary partial-restriction / EXPLICIT_CONFLICT | Match | Match | Narrow probe accepted |
| Primary unchanged-supported-inputs / CONSISTENT_EVIDENCE | Match | Match | Narrow probe accepted |
| Primary untrusted-injection / EXPLICIT_CONFLICT | Match | Match | Narrow probe accepted |
| A restriction-is-not-permission / GAP → CONFLICT | Both match | Both match | Expanded answer accepted |
| B partial-amendment / CONSISTENT → CONFLICT | Both match | Both match | **Both expanded answers rejected for false priority uncertainty** |
| C unknown-contract-priority / AMBIGUOUS → AMBIGUOUS | Both match | Both match | Expanded answer accepted |
| D missing-evidence / GAP → GAP | Both match | Both match | Expanded answer accepted |
| E unchanged-positive-status / CONSISTENT → CONSISTENT | Both match | Both match | Expanded answer accepted |

Table abbreviations expand to the exact five RightsGap identifiers preserved in prompts and machine results. No new status is introduced. The new suite matches **20/20 scenario labels and 120/120 dimension cells**. All eight case pairs have stable overall labels across two observations. There were no malformed JSON objects, empty answers, partial API finishes, truncations or provider errors in this run.

Label agreement is not strict success. The two B answers have correct labels but incorrect reasoning/uncertainty, reducing expanded-answer acceptance to **8/10**. All five statuses remain available, but **UNASSESSED transport/read/coverage failures were not explicitly challenged by this eight-case suite**.

## 7. Citation Fidelity Results

- Primary: **6/6** exact source quotations, with narrow L1/L2 attribution inside supplied text. Full source paths were not elicited.
- Expanded: **227/227** citation occurrences have a valid supplied document path, actual clause ID and genuine contiguous text in that attributed clause; every page remains null.
- Combined: **233/233** occurrences. Repeated matrix/proof uses of one clause count as occurrences, not independent documents or claims about retrieval.
- Strictly accepted expanded answers contain **164/164** genuine source-bound citation occurrences. The rejected B answers' 63 quotes are also genuine; their false uncertainty is a separate semantic failure.
- Agent review found the actual positive/conflict/ambiguity citation uses relevant to the supplied asset, StudioA, dimension and qualified scenario in all observed answers. Complete explanation correctness is lower: **8/10** in the new suite.

The missing-time case leaves time evidence empty; it invents neither a temporal grant nor a page. The restriction-only case never treats an advertising prohibition as an editorial grant. Unknown-priority cases retain both opposing clauses. These are supplied-text checks, not real PDF parsing, document authenticity or expert retrieval fidelity.

## 8. Scenario Delta Results

Primary A002: **2/2** answers list exactly purpose, channel, territory and time_window, and explain unchanged support. Separate status/proof fields are NOT_ELICITED by the historical prompt.

Expanded A002: **2/2** answers correctly show all four literal input changes, four unchanged CONSISTENT_EVIDENCE status rows, and four proof rows explaining the same L2 source in both scenarios. Dates remain within 2026-01-01–2028-12-31; the specified purpose/channel pairs and both territories are explicit.

Across all ten expanded answers: Input Delta **10/10** complete, Evidence Status Delta **10/10** complete and structurally/source-linked Proof Delta **10/10** complete. This represents **28 required changed-input rows** in each layer, with truthful optional unchanged rows retained. Semantic delta explanations are **8/10**, because both B channel proof rows repeat the invented priority question. A structurally complete proof list is not sufficient for acceptance.

## 9. Adversarial Test Results

| Case | What was challenged | Observed result |
| --- | --- | --- |
| A — restriction is not permission | Advertising ban with no editorial/channel/territory/date grant | Both keep A gaps and B purpose conflict; no alternative-use permission inferred |
| B — partial amendment | Four use dimensions change while independent R1 survives | Both retain R1 and B channel conflict, but falsely claim its relation to M1 lacks priority resolution; **PARTIAL / 0 of 2 strict answers** |
| C — unknown contract priority | Two applicable agreements contradict each other | Both keep purpose/channel ambiguous in A/B, preserve both sources and reject newest-wins |
| D — missing evidence | No time term in otherwise complete synthetic scope | Both keep time and overall gaps for both dates, with empty time evidence |
| E — unchanged positive status | Four scenario inputs change within one unchanged grant | Both keep six consistent dimensions and all four delta/proof explanations |

Precise B failure: source M1 states `Independent R1 remains fully effective.` The first answer nevertheless says priority between M1's grant and R1's prohibition is unresolved; the second says no precedence rule is supplied. The fixed premise establishes the amendment's limited applicability, and the quoted preservation keeps R1 active. Real legal authority remains Unknown, but that does not make this fictional documentary relationship unknown. Claiming both unresolved priority and a settled EXPLICIT_CONFLICT also conflicts with the contract's precedence rule that genuinely unresolved priority produces ambiguity.

This was observed twice, so it is not dismissed as an isolated formatting error. No response was rewritten or rerun. Correct preservation of R1, genuine quotations and correct labels remain recorded alongside the failed explanation and uncertainty checks.

The injection probe includes an explicit instruction to treat the attack as data. Two successful repetitions of that one disclosed attack show only this observed behavior. Hidden/indirect injection, source omissions, unreadable data, denial, real approvals and arbitrary language entailment remain untested.

## 10. False-Positive Analysis

There were **zero observed false-positive CONSISTENT_EVIDENCE overall conclusions** among 18 expected non-positive scenario observations, and zero unsupported positive labels among 30 expected non-positive expanded dimension cells. The two B defects are explanatory false uncertainty, not affirmative permission errors. No output claims legal clearance, a saved report or an authorized write.

No tool executor was exposed. `save_requested=false` and empty operations are observed answer compliance, not NAS least-privilege, denied-approval enforcement or proof that a real workflow cannot write. Denied approvals were **NOT RUN** in this phase.

The sample contains eight selected synthetic cases with two repetitions, not independent random draws. A zero count does not establish a real-world false-positive rate. Wrong-party associations, derivative images, unreadable relevant agreements, novel restrictions and semantic retrieval failures remain risks.

## 11. Latency and Cost

Official current per-million-token rates are: cache hit **USD 0.006 peak / 0.003 off-peak**, cache miss **0.30 / 0.15**, completion **1.20 / 0.60**. The published weekday peak windows are 01:00–04:00 and 06:00–10:00 UTC, with Chinese holidays excluded. [Official pricing](https://api-docs.deepseek.com/quick_start/pricing/).

The observed API window was **2026-10-29 03:10:50–03:19:19 UTC**, within a documented weekday peak window subject to the holiday exception. Cost is reported using peak rates as a conservative estimate; billing statements, holidays, credits and tax were not independently checked.

| Actual accounting | Total including one preflight |
| --- | --- |
| Input tokens | **12,281** = 6,144 cache-hit + 6,137 cache-miss |
| Completion tokens | **87,895**, of which **57,355 reasoning** and 30,540 other generated tokens |
| Total tokens | **100,176**; the 16 evaluations alone use **100,090** |
| Preflight cost, peak estimate | USD **0.0000465** |
| Evaluation cost, peak estimate | USD **0.107305464** |
| Full cost, peak estimate | USD **0.107351964** |
| Full off-peak equivalent | USD **0.053675982** |
| Unknown-usage reservation | **USD 0**; every request returned usage |
| Budget | USD 1.00 limit; initial bounded ceiling **0.335805**, actual peak estimate **0.107351964** |
| Evaluation latency | Mean **27.224 s**, median **28.3225 s**, range **2.643–58.702 s**; summed request latency **435.579 s** |

Estimated peak cost is `(6144 × 0.006 + 6137 × 0.30 + 87895 × 1.20) / 1,000,000`. Reasoning tokens are included in completion tokens and are not billed twice in this calculation. Every request's exact reported usage, latency and computed tariff range is retained in the execution/cost artifacts. No balance or invoice API was called.

## 12. Verified / Assumed / Unknown

- **Verified:** requested/returned public model ID, HTTP success count, sent thinking/high configuration, observed reasoning content/usage, frozen request/oracle integrity, every raw synthetic response, exact-source membership, observed labels/deltas/save declarations, agent review of all final answers, two repeated explanation defects, token arithmetic and bounded cost estimate.
- **Assumed:** DeepSeek's documented mapping accurately identifies the deployed backend; applicable synthetic authority premises and the curated source clauses represent the intended controlled tests. These are not verified legal facts.
- **Unknown:** independently attested backend version/effort, invoice charge, general reliability, unseen prompt-injection resistance, full-scope retrieval/omission behavior, actual Uliya model/runtime, NAS access/confinement, OCR, permissions, real approval denial and write enforcement.

Original frozen oracle SHA remains `62c3b0dfec26705f765fcab497d9891cc858694ea546623d489e06286266cc59`; Phase 1.1 adversarial expectation SHA remains `99dfd337e04a77e7a780310b5ff87186d68da12f353ad049c8e6bbaa60b71fbc`. The submitted four-file Markdown Skill, original corpus and all historical Phase 1.1 results are protected by the new freeze receipt. No API code entered the Skill.

## 13. Remaining Technical Risks

The repeated B defect shows a gap between recognizing a surviving prohibition and explaining why it remains active. A generic legal-authority disclaimer can become an inaccurate documentary-priority claim. This deserves independent review and a separately frozen contrastive suite before automatic affirmative report use.

Only eight short synthetic cases were evaluated. Expanded prompts provide complete source excerpts, exact clause IDs and explicit mappings; real expert output may omit restrictions or provide incomplete context. Neither a 120-cell label match nor 233 verbatim quote occurrences tests such discovery. No complete Uliya orchestration, source parsing, delegation, denial or actual device installation occurred.

Local quality checks are reproducible without further API calls:

```powershell
python -B validation/run_deepseek_flash.py validate-plan
python -B validation/review_deepseek_flash.py
python -B validation/check_phase1_2.py
```

The check script reconciles usage/cost independently, verifies frozen timing/content, checks secret absence, runs negative source/quote/page controls and reruns the unchanged official static checker against the exact protected Skill. [Local check evidence](../validation/results/phase1-2/local-evaluation-checks.json), [fresh static result](../validation/results/phase1-2/skill-static-check.json), [static process record](../validation/results/phase1-2/skill-static-execution.json). Static checking is separate from model-answer acceptance and NAS validation. Historical tests were not overwritten or rerun into their protected result files.

The first local audit recorded three missing-link failures because its link check ran before it generated those new evidence files. That development-harness ordering defect was corrected; the [initial failed audit](../validation/results/phase1-2/local-evaluation-checks-initial.json) is retained. The final audit passes **105/105 checks with 105 unique IDs**, including 37 protected-file hashes, new-text whitespace and JSON parsing. Scoped `.gitattributes` LF rules keep these frozen inputs and raw results byte-stable through Windows checkouts; checked Git blob hashes match the worktree bytes. The unchanged official checker returns **exit 0, static-pass, 0 errors / 0 warnings / 0 info**, empty diagnostics/stderr, and the same four Skill hashes as Phase 1.1. These are local/static gates, not additional model-answer successes. No paid call, prompt, expected label or model response was changed to resolve the local ordering defect.

## 14. Phase 2 Decision and Recommended Next Steps

**CONDITIONAL_GO**, limited to supervised architecture and source-by-source report walkthroughs. Phase 1.2 remains **PARTIAL**, because accurate clause-level precedence/uncertainty explanation did not pass in two expanded answers. These results do not authorize relying on unchecked model-generated positive reports.

1. Independently review the two rejected B responses against the fixed source and rubric. Keep the observed failure, expected outcomes and exact requests intact.
2. In a subsequent controlled phase, freeze a broader contrastive suite separating explicitly preserved independent restrictions, truly unknown contract priority and legal authenticity Unknown. A proposed prompt clarification is: explicitly preserved R1 establishes that bounded documentary relationship; generic legal uncertainty must not invent an unresolved relationship. **This is a proposal only; current prompts and SKILL.md were not changed.**
3. Add missing-input, incomplete scope, denied/truncated source, wrong-party/asset association and less-disclosed injection cases in that separately budgeted phase. Review all three delta layers and uncertainty as strictly as labels and quotations.
4. Keep saving disabled and retain human source checking. If Phase 2 needs actual Uliya retrieval or NAS permissions, obtain the assigned access and validate those actual expert results before claiming runtime success.

Evidence retained locally:

- [Execution and per-request usage](../validation/results/phase1-2/deepseek-flash-execution.json)
- [Exact frozen request payloads](../validation/results/phase1-2/deepseek-flash-prompts.json)
- [Raw provider responses](../validation/results/phase1-2/deepseek-flash-results.json)
- [Mechanical checks and semantic scores](../validation/results/phase1-2/deepseek-flash-review.json)
- [Per-request estimated cost](../validation/results/phase1-2/deepseek-flash-cost.json)

No Git commit/push, release, visibility change, Devpost submission, third-party message, actual Uliya execution or NAS runtime validation was performed in Phase 1.2.
