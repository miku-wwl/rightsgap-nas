# 10 — Phase 1 capability audit

Audit date: **2026-10-29, Pacific/Auckland**. Labels describe evidence level, not device success.

Phase 1.1 update: the official page still links the same archive/hash. Active candidate families are now only ug-filesystem/file-agent and ug-document/document-agent. save-text remains a reviewed but **excluded** capability; no save delegation is present. Clause-level relations and three delta layers are report/reasoning concepts, not new Actions or asserted UGOS fields. See [docs/12](12-phase1-1-review.md) for current validation and the observed local-model limitations. The matrix below preserves complete audited definitions, including excluded candidates.

## Provenance and reading record

**Verified:** the complete [Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit), its linked User Agreement, Privacy Policy and Content Submission and Publication Standards were read. The current download link resolves to [uliya-skill-kit-0.7.3-en.zip](https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898). This is the current observed page link, not a claim that no other archive exists.

| Artifact | Verified value |
| --- | --- |
| Archive version | 0.7.3 (archive filename; no separate package manifest/version) |
| Archive SHA-256 | `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3` |
| Catalog version / generatedAt | `2.0.0` / `2026-09-01` |
| Catalog SHA-256 | `c927fd8e233696cd152baf98468368912c13c08aabeac353f0ee95c46c0428e6` |
| check-lib.mjs SHA-256 | `a4020044c1138f1937777d8a600df9d304ea00bf4f3bd20ae5e00883ad6542a7` |
| check-skill.mjs SHA-256 | `6a9e8ad164862ab787f45e577c2e2bc98cfb31cea10f5ec291cb6550eb51fb52` |
| Checker format | `2.0.0`; no independently declared checker release version |
| Original download/extraction location | `D:\Ollama\Temp\rightsgap-phase1-20261029\` (development machine only) |

Read in full: kit `SKILL.md`; `docs/skill-development-standard.md`; all `references/*.md` and their examples; the template; both checker source files; both JSON schemas; complete selected Action definitions. Exact selected definitions are retained in [capability-selection.json](../validation/official/capability-selection.json), outside the Skill. JSON array selectors below refer to `data/capability-catalog.json` inside the linked archive. Some official English descriptions are incomplete translations; this audit preserves uncertainty rather than repairing them into invented contracts.

**Verified:** nine CLI families map uniquely to six agents. Selected families are `ug-filesystem` → `file-agent`, `ug-document` → `document-agent`, optional `ug-knowledge` → `knowledge-agent`. `ug-photo` → `photo-agent` was reviewed and excluded. The parent delegates business instructions; each expert selects its own documented CLI/Action. Parent-level CLI execution is prohibited.

## Exact Action matrix

All parameters below have catalog type **string**, except `extract.dedupe` which is **boolean**. All are nonrepeatable except the explicitly marked repeatable parameters. Numeric bounds on string-typed parameters are recorded exactly as published; they do not imply integer type. Required means catalog-required, not a new parent input requirement.

| CLI.Action / selected use | Registered expert | Required arguments | Optional arguments (complete list) | Effect / approval | Documented output and limitations |
| --- | --- | --- | --- | --- | --- |
| `ug-filesystem.find` / bounded discovery | `file-agent` | `path` | `pattern`; `type` = all/dir/file/image/video/audio/archive/documents/font/application; `min-size`, `max-size` ≥0; `date-type` 0..3; `start-timestamp`, `end-timestamp` ≥0; `max-depth` ≥0; `limit` ≥0 | read / none | Literal summary: `file、realpath` and `fileId`. No complete list/envelope, pagination, limit-hit, symlink confinement or omission fields documented. |
| `ug-filesystem.stat` / verify each actual path | `file-agent` | `path` | none | read / none | Literal summary `realpath、、time stat`; exact field layout and stable identity unknown. |
| `ug-filesystem.sha256sum` / optional integrity | `file-agent` | `path` | none | read / none | SHA-256 described; key/encoding layout unknown. Hash is not evidence of rights or derivative equivalence. |
| `ug-document.qa` / per-file evidence request | `document-agent` | `query` | `file` (repeatable); `intent` = qa/content_read/extraction/period/condition/comparison/summary/outline/semantic_lookup/locate_content; `content-scope` = auto/preview/full (default auto); `top-k` 1..20; `entities` (repeatable); `answer-mode` = direct/list/table/prose; `evidence-mode` = balanced/focused/broad; `max-files` 1..200 (default 60); `body-cap` ≥1000 | read / none | Literal summary: `` `answer`、/evidence、coverage、Read ``. Only `answer` has an explicit code-form field name; evidence/coverage mentioned but no nested schema, quote/path/page keys or guarantees. |
| `ug-knowledge.save-text` / optional reviewed save | `knowledge-agent` | none | `path`; `content`; `content-ref`; `filename-hint` | state-change / **workflow** | Summary names `verified=true`, `outputFile`, `contentBytes`; no overwrite/exclusive-create switch, collision semantics or approval payload schema. Do not relabel approval as gateway. |
| `ug-document.extract` / reviewed, excluded | `document-agent` | `query` | `file` (repeatable); `schema` = auto/invoice/contract/expense/receipt/medical-report/purchase_order/mixed/mixed_reconciliation (default auto); `content-scope` = auto/preview/full; `max-files` 1..500 (default 60); `body-cap` ≥1000; `dedupe` boolean (default true) | read / none | Literal summary `data、、coverage、failures`; no license schema, no guaranteed rights fields. Not needed for initial Skill. |
| `ug-document.reconcile` / reviewed, excluded | `document-agent` | none | `query`; `file` (repeatable); `max-files` 1..200 (default 60) | read / none | Literal summary `result、、 coverage`; no precedence/authority/supersession guarantee. Parent preserves ambiguity. |
| `ug-photo.meta` / reviewed, excluded | `photo-agent` | none | `path` (repeatable); `raw` | read / none | Literal summary `EXIF/data、failure/`; no IPTC/XMP rights, licensed-party or release schema. |

For each row, source selector: `clis[name=CLI].actions[name=Action]` in the archive catalog; owner is `clis[name=CLI].agent`. Definitions include effect, approval and returnSummary; see the linked extracted selection for exact spelling, required/repeatable flags, defaults, examples and completionEvidence.

**Common knowns:** catalog invocation envelope describes `{ok:true,data:{}}` or `{ok:false,error:{}}`, owned by child workflows. Read completionEvidence says `ok=true` with real data; save completion additionally references operation/approval/failure. Public delegation states are `completed`, `failed`, `cancelled`, `waiting_user`, `waiting_approval` in kit instructions. Neither envelope is a license-specific evidence schema.

**Common unknowns for every selected Action:** `permissions.knowledgeStatus`, `prerequisites.knowledgeStatus`, `errorCodes.knowledgeStatus` and `stability` are all `unknown`; every example has `outputStatus=unknown`. Approval `none` is not blanket file authorization. Runtime permissions, exact errors, supported formats/OCR, returned evidence fidelity, performance and model routing remain **Unknown**. Confidence is high in the declarations, unmeasured in NAS execution.

## Critical document-source feasibility

**Verified at static interface level:** `qa.file` can identify a single file, `query` can ask for six-dimensional source clauses, and `intent=content_read` plus `content-scope=full` can request source context. This supports an attempted per-file review, without inventing a license extraction schema. The parent sends actual verified paths and the two scenario tuples in each self-contained instruction; the expert owns parameter selection.

**Unknown:** the real service may return only a summary, no reproducible clause, no page, insufficient source attribution, or incomplete text despite `full`. No schema guarantees that a quote is verbatim or that retrieval covered every relevant clause. `top-k`, `body-cap` and `max-files` are bounds, not completeness proofs. A second source-context request is an additional observation through the same expert, not independent document authenticity verification.

**Decision: conditional GO for a static, source-gated candidate; NO-GO for an unconditional evidence-positive/runtime claim.** Positive or explicit-conflict assessment requires an actual document path, a clause present in returned source context, established asset association and adequate completed coverage. If any is unavailable, stop that dependent judgment, retain UNASSESSED/AMBIGUOUS_EVIDENCE, and offer the narrower evidence locator plus human questions. GAP_IN_CHECKED_SCOPE requires positively known completed scope, never just an empty search answer. Do not claim actual page/quote fidelity before target-device inspection.

## Narrowing and approvals

- Initial audit is read-only. Discovery and per-file analysis stay inside owner-approved media and document lists: 5–8 media assets, 3–6 documents, two scenarios. Discovery overflow/unknown completeness cannot silently truncate into an affirmative report; ask for an explicit smaller set.
- A/B uses identical evidence and licensed party. Added evidence is a new approved revision; affected recheck may use a 1–2 asset subset and at most six source documents. Preserve original scope receipts for unchanged rows; no claim of a new complete audit over seven documents.
- Save is optional, only through `knowledge-agent`, with reviewed exact text and user-authorized destination plus the expert's workflow approval. The catalog does not guarantee exclusive creation. If the expert cannot establish a non-overwriting destination, stop save and return the report in chat. No new parameter is invented to force it.
- Contract priority is established only by explicit observed clauses and a user-confirmed applicability/authority basis, never latest filename/date or a visual signature. Unresolved authority or competing clauses remain ambiguous.
- Photo metadata, specialized extraction, automatic reconciliation, background watchers, file mutation and external publication are excluded. No arbitrary NAS runtime is introduced.

## Checker source findings

The checker allows only `SKILL.md` and ordinary `.md` files under `references/`, each directly linked from the root. It disallows root README despite the Starter Kit's older illustrative tree. It checks name/directory agreement, simple name+description frontmatter, required H1 headings, delegation syntax, six registered targets, evidence mappings and five status tokens; it scans scripts/direct access/credentials and other prohibited patterns. Limits: 1 MiB/file, 10 MiB/package, 100 files; recommended body ≤500 lines. Use `# Orchestration` and `# Generation-time capability evidence` with Unicode-arrow mappings: the template's `# Expert orchestration` and ASCII mapping instructions do not match the actual checker patterns.

**Limitation:** the checker loads CLI ownership but does not validate Action parameters, evidence truth, approval enforcement or reasoning. Zero warnings does not establish runtime correctness. Official [Rules](https://ugreenhackathon.devpost.com/rules) and [Resources](https://ugreenhackathon.devpost.com/resources) were rechecked; no NAS run is claimed, and no submission, release, visibility change or external contact is performed.
