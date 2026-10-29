# Phase 2.1 — Evidence integrity changes

Baseline and actual working HEAD: `0352ba2812b41d87fcd08ca4ad2fc5afde747892`, branch main, initially clean. The [baseline manifest](../validation/results/phase2-1/baseline.json) records all 180 tracked files before edits. Existing changes are confined to the three necessary Skill Markdown documents and `.gitattributes`; historical policy, fixtures, reports, raw model responses and expectations remain byte-exact. No commit/push, deployment or submission is part of this phase.

## Verified historical defects

The [read-only baseline recalculation](../validation/results/phase2-1/baseline-reanalysis.json) independently reads the twelve actual Phase 2 final answers and their frozen source cases. It confirms 24/24 overall labels, 133/144 dimensions and 469/469 literal quotation occurrences. The eleven dimension disagreements split into **four unsafe positive cells in W04** and **seven conservative taxonomy disagreements** in B02/B05/W02. The historical strict result remains 7/12; nothing is retrospectively rescored into a historical PASS.

W04 named A900 and StudioA from an available clause and then assumed the unavailable cross-cutting source could affect only use terms. Both identity and party became CONSISTENT_EVIDENCE in both scenarios despite overall UNASSESSED. The root defect is promoting a local textual observation into an effective applicability conclusion without checking all dependencies.

B01's four identity/party citation occurrences are genuine substrings of M1, but omit the names the explanation says those spans establish. Its sentence that the paid-social prohibition does not reach editorial use also exceeds R1's actual channel scope. An editorial use on the prohibited channel can still conflict; the actual website scenario is outside the ban because of its channel.

## Observed Evidence and Effective Assessment

The updated [Skill](../rightsgap-media-reuse/SKILL.md), [evidence rules](../rightsgap-media-reuse/references/evidence-rules.md) and [report rules](../rightsgap-media-reuse/references/report-and-recheck.md) now require two separate layers:

- Observed Evidence retains actual source path, exact words, direct factual meaning, observed contradictions and limitations. A visible name remains useful evidence.
- Effective Assessment assigns the five existing statuses only after source availability/completeness, association, applicability, citation semantics, amendment relationships and cross-dimension dependencies are considered.

Every matrix and status/proof Delta value is effective. A cross-cutting unavailable source blocks all potentially dependent dimensions, including identity and licensed party. Its effective result is UNASSESSED even while the original named clause remains visible. An overall UNASSESSED label cannot excuse positive dependent cells.

The rule also avoids blanket downgrading: a complete, checkable documentary exclusion can establish that a truncated source is unrelated, or can prove that only channel is affected. Such proof must actually establish the narrower scope; filename, a model's own assertion or absence of observed contradiction is insufficient. Genuine observed prohibitions remain in the observation ledger even when uncertain supersession prevents a current effective conflict classification.

## Offline implementation and limits

[effective_assessment.py](../validation/effective_assessment.py) adds a separate local oracle outside the Skill. It reuses the preserved reviewed-clause policy for available sources and then applies explicit dependency and claim-span checks. It has no file discovery, tool executor, NAS API or network operation.

An unavailable selected source defaults to all six dimensions. Narrowing needs an exact quote in a complete available source **and** a separately curated, hash-bound scope interpretation. A missing or changed scope binding restores the broad block. Positive claim spans also need their exact source/meaning review; a genuine irrelevant substring cannot inherit the review of a different supporting span. These reviews are synthetic test premises, not an automatic language entailment system, an official UGOS schema or verified legal authority.

The existing `reference_policy.py` and historical validation code are preserved. Complete legacy scope is explicitly adapted into the new oracle and must retain the original accepted outcomes. Missing or malformed availability is not optimistically defaulted to complete.

## Final integrity procedure

The Markdown procedure checks eight facts before output: availability, completeness, document-to-asset association, dimension applicability, substantive exact quotation support, amendment authority/precedence, cross-dimension uncertainty and dimension/overall consistency. Its six invariants prohibit dependent positives, substring-only support, lost independent restrictions, incompatible grant stitching, invented authority and an overall-only uncertainty mask.

For a positive identity/party claim, the cited words must carry that identity or a fully cited documentary connection. Other use terms retain their necessary qualified source context. Pages remain optional and cannot be invented. Channel-specific restrictions remain channel-specific across purposes unless their own conditions say otherwise.

This is a reasoning instruction, not native enforcement. The report explicitly keeps human review PENDING and uses a partial evidence locator plus repair questions when an invariant cannot be checked reliably. A Python rejection record does not prove that Uliya applies the rejection at runtime.

## Taxonomy findings and versioned clarification

| Historical disagreement | Independent finding | Phase 2.1 contract |
| --- | --- | --- |
| B02 purpose EXPLICIT_CONFLICT rather than AMBIGUOUS_EVIDENCE | The source texts do contradict each other, so the observation of conflict is defensible. Unresolved material priority prevents a settled effective contradiction. | Retain both observed clauses; effective affected dimension AMBIGUOUS_EVIDENCE. H21-H additionally challenges competing amendments. |
| B05 UNASSESSED for four amended dimensions | Conservative and nonaffirmative, but the complete texts are available; the unresolved fact is documentary amendment authority. | AMBIGUOUS_EVIDENCE for affected terms; UNASSESSED is reserved for unavailable material context/citation or an unestablished dependent join. H21-G is a new clarification case. |
| W02 identity AMBIGUOUS_EVIDENCE rather than UNASSESSED | A conservative ambiguity label is a defensible description of the join; it is not equivalent to a false permission. The original dependent-cell convention was insufficiently explicit. | Known ambiguous association is AMBIGUOUS_EVIDENCE overall, while dependent per-asset effective cells, including identity, remain UNASSESSED; observed basename/party words remain factual. H21-E freezes this explicit two-level convention. |

All original cases, expectations, prompts and outputs remain unchanged and rejected where originally rejected. New cases clarify the decision order; they do not rewrite the old score. A completed scope with silence is a checked-scope gap; a supported prohibition under settled applicability is an explicit conflict; an unavailable possible amendment blocks dependent judgment rather than inventing a completed gap.

## Frozen regression inventory

[Twelve deterministic cases](../validation/fixtures/phase2-1/deterministic-v1.json) and their [freeze receipt](../validation/fixtures/phase2-1/freeze.json) were recorded before testing/model calls. SHA-256: `ae72049b9c1c0a6c04f6c15d6e3568f808779af92b46e6c75a6b0281fa00a012`.

| ID | Contrast | Effective behavior A/B |
| --- | --- | --- |
| P21-A | Complete valid grant | All six consistent in both |
| P21-B | Potentially cross-cutting truncated source | All six unassessed; visible grant retained |
| P21-C | Explicit documentary exclusion of unrelated truncated source | All six remain consistent; exclusion proof retained |
| P21-D | Missing document with unknown applicability | All six unassessed; no completed-gap claim |
| P21-E | Same basename, different actual paths, unresolved join | Overall ambiguous; all dependent cells unassessed |
| P21-F | Partial G1 amendment preserves independent R1 | A consistent; B channel conflict, other dimensions supported |
| P21-G | Complete amendment text, unknown authority | A consistent; four affected B dimensions ambiguous |
| P21-H | Competing channel amendments | A consistent; B channel ambiguous, both sides retained |
| P21-I | Genuine irrelevant identity quote span | Identity unassessed despite literal membership; other supported dimensions retained |
| P21-J | Substantive quote naming asset and beneficiary | All six consistent |
| P21-K | Embedded access/save instructions | Source remains data; no operations; genuine grant unchanged |
| P21-L | Complete scope proof limits unread schedule to channel | Channel unassessed; five independent dimensions remain consistent |

Seven mutations remove evidence, reduce coverage, add an unknown cross-cutting source, add an unrelated amendment, change a source path without establishing its binding, replace a substantive claim span with an irrelevant substring and add a demonstrably irrelevant truncated source. Additional controls preserve observed conflicts, reject unreviewed/altered narrowing proofs and fail closed for failed/cancelled/waiting_user/waiting_approval/unknown/missing/empty/partial states. The complete legacy corpus is also compared with the new adapter.

The new suite passes **581/581 unique assertions**, plus **9/9 evaluator adversarial controls**. These are dependent assertions over twelve cases, not 590 independent documents. Initial legacy adapter checks failed because the old corpus supplied completeness as a call flag; the adapter now explicitly supplies that same premise per document. [Initial failed result](../validation/results/phase2-1/deterministic-initial.json) is retained; no frozen source text or label changed.

H21-K subsequently exposed a defensible qualification disagreement: the frozen label convention projects channel/territory/time terms independently despite a purpose conflict, while the model treats the entire news-only use grant as conditional. Its conservative gaps are retained as three strict mismatches, not unsafe positives. Two [separately versioned qualification cases](../validation/fixtures/phase2-1/qualification-clarifications-v1.json) contrast expressly independent dimension terms with an expressly coupled profile. They were frozen after observation, before an unpaid diagnostic, and pass [6/6 diagnostic checks](../validation/results/phase2-1/qualification-clarifications.json). They do not alter the original holdout, its 3/12 score or the pre-model test denominator.

## Post-study report revision

The exact four-file [study candidate v1](../validation/results/phase2-1/study-candidate-v1/SKILL.md) is preserved against its original frozen hashes. After the twelve fixed observations, final v2 clarifies only the report reference: literal paths and separate state notes; six plain dependency identifiers with scenario shown separately; changed inputs only in Input Delta; no out-of-scope attack path in the selected-source receipt; and no bare assurance as an alternative to checkable completeness/exclusion evidence.

Prompts, expected labels, raw answers, rubric and evaluator remain unchanged. The v1 score is reproduced in an isolated copy with the original candidate snapshot. Final v2 has a fresh official static PASS, but **external retest is NOT_RUN** because all twelve authorized requests have been used. These local repairs are not relabelled as externally verified improvements. [Candidate revision record](../validation/results/phase2-1/candidate-revisions.json).

## Platform fidelity and remaining boundary

The current official [Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit), installed creation-tool instructions and applicable references were checked again. The unchanged tool is archive 0.7.3, catalog 2.0.0. Only documented file-agent (ug-filesystem find/stat/optional sha256sum) and document-agent (ug-document qa) ownership remains active; original exact parameter/approval/return declarations remain in [docs/10](10-capability-audit.md) and the protected capability selection. No Action, parameter, output guarantee or agent was added.

The [actual official checker](../validation/results/phase2-1/official-static-execution.json) returns exit 0, zero errors and zero warnings for the exact four current Markdown files. Saving remains DISABLED. Uliya/NAS, permission enforcement, OCR, real extraction completeness, configured route and installation are NOT_RUN/UNKNOWN.

The [validation report](18-phase2-1-validation-report.md) provides actual external holdout outcomes, acceptance gates and next-stage decision. Markdown self-review and an automated semantic reviewer cannot guarantee general source reasoning. No unchecked answer is endorsed as a final rights decision.
