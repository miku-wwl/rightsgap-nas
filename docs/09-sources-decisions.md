# 09 — Source register, verification labels and decisions

## Source precedence

1. Official UGREEN/Devpost Rules.
2. Current official Uliya Skill Creation Tool, capability-catalog.json, standards and checker code.
3. Official Starter Kit and Resources/FAQs.
4. Target NAS runtime observations (once assigned).
5. External platform/vendor original documentation (for competitor benchmarking).
6. Public competitors' self-authored Devpost pages (claims, not independently verified implementations).

## Official source register (checked 2026-10-28)

- UGREEN Hackathon Rules: https://ugreenhackathon.devpost.com/rules
- Resources and FAQ: https://ugreenhackathon.devpost.com/resources
- Starter Kit: https://ai.ugreen.com/pages/hackathon-starter-kit
- Developer package link on official page (observed as 0.7.3): https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898
- SkillHub publication/safety standard: https://api.ugnas.com/api/system/v1/ua/agreement/page?acceptLanguage=en-US&agreementCode=skillhub-publish-audit-spec
- Official Devpost gallery (publication incomplete at research time): https://ugreenhackathon.devpost.com/project-gallery

## Primary industry sources

- Adobe AEM Assets governance: https://business.adobe.com/products/experience-manager/assets/asset-management.html
- Adobe DRM documentation: https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/manage/drm
- Adobe Governance Agent: https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/ai-in-aem/agentic-capabilities/brand-governance/overview
- Bynder Advanced Rights: https://support.bynder.com/hc/en-us/articles/21576746100114-What-are-Advanced-Rights
- IPTC Photo Metadata standard: https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html
- IPTC Photo Metadata user guide: https://www.iptc.org/std/photometadata/documentation/userguide/

## Verified / Assumed / Unknown ledger

| Claim | Evidence level | Notes |
| --- | --- | --- |
| 4 official criteria equally weighted | Verified | Official Rules |
| First round up to 30 finalists; NAS not required | Verified | Official Rules |
| Finalists receive one allocated NAS testing day | Verified | Official Rules |
| The starter page links the 0.7.3 kit | Verified again on 2026-10-29 | Current fetched archive/hash recorded in docs/10 |
| Catalog 2.0.0 lists 9 CLI families / 6 registered agents | Verified independently in Phase 1 | Current archive and checker source read; exact selected definitions retained |
| ug-document.qa can be instructed to seek file-specific evidence | Verified at current declaration/parameter level | Actual quote, source-context and citation quality Unknown |
| photo.meta returns IPTC rights / licensee / release fields | Unknown | Do not put in MVP critical path |
| Parent model applies six-field scenario rules reliably | Assumed | Requires mock and real NAS evaluation |
| Exact asset-to-license association is automatic | Not verified; must not assume | Use explicit mapping / direct document references |
| Fully offline / zero cloud egress | Unknown | Depends on actual model routing |
| Static validation equals successful NAS runtime | False | Distinct verification layers |
| 18/20 is achieved | False | Aspirational internal target |

## Decision log

### D001 — Candidate selection (2026-10-28)

Preferred candidate RightsGap NAS V3, **conditional** on verifying a supported source-evidence path. Rejected generic contract audit as primary idea due to public competition overlap. Owner has authorized initial repository documentation, not final Devpost submission.

### D002 — Product differentiator

Core innovation is a source-backed *use scenario delta*, optionally followed by user-supplied evidence repair and recheck. Do not expand into generalized digital rights enforcement.

### D003 — Safety status wording

Use CONSISTENT_EVIDENCE, EXPLICIT_CONFLICT, GAP_IN_CHECKED_SCOPE, AMBIGUOUS_EVIDENCE, UNASSESSED. No legal clearance or rights verification outcome.

### D004 — Interface discipline

Read official catalog and actual checker before creating Skill. Parent only delegates; all runtime model/cloud details Unknown until tested.

### D005 — Packaging discipline

Repository bootstrap ZIP is for source control. Devpost requires a separate narrowly structured Skill ZIP and PDF. Never conflate them.

### D006 — Conditional source-gated GO (2026-10-29)

Re-fetched the current [Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit) and its linked [0.7.3 archive](https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898); archive SHA-256 `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`. Read the full creation instructions, standard, references, selected Action definitions and checker. [docs/10](10-capability-audit.md) is the exact current capability record. The current page-linked user agreement, privacy policy and [publication standard](https://api.ugnas.com/api/system/v1/ua/agreement/page?acceptLanguage=en-US&agreementCode=skillhub-publish-audit-spec) were also read; no account action or submission was taken.

Per-file QA is statically supported, but the catalog has no guaranteed quote/path/page schema or full-coverage proof. Generate a conditional source-gated candidate: unsupported source verification stops dependent positive/conflict judgment. Narrow to evidence location and human questions if actual returns are inadequate. This preserves the six-dimension/five-status product contract without pretending runtime provenance is solved.

### D007 — Exclude unsupported enrichment (2026-10-29)

Do not use `ug-document.extract`, `ug-document.reconcile` or `ug-photo.meta` in the first candidate. They were audited, but license schemas, automatic legal supersession and IPTC rights fields are not guaranteed. Use source clauses plus explicit applicability/authority premises; retain A006 ambiguity. No arbitrary NAS executable is a fallback.

### D008 — Local evidence is a reference model, not Skill execution (2026-10-29)

Froze original docs/08 bytes and fixed oracle expectations before creating the Skill or evaluator. Retain fixture terms as manually labelled, synthetic observations outside the package. Do not market deterministic policy tests as LLM evaluation, PDF parsing, actual injection resistance, approval enforcement or NAS runtime. The fixture filenames are fictional, not created PDF/JPEG artifacts. Exact measurements and limitations are in docs/11.

### D009 — Save requires more than a documented Action (2026-10-29)

`ug-knowledge.save-text` exists and uses **workflow** approval, not an assumed gateway value. Its documented output names include `verified`, `outputFile`, `contentBytes`; collision/exclusive-create behavior is Unknown. Optional save must stop before mutation unless supported behavior establishes a new non-overwriting destination and actual workflow approval. No invented flag, file-agent write or custom runtime can supply the missing guarantee. Present-day runtime-safe save is unverified and therefore blocked; the report remains available in chat.

### D010 — Follow current checker over inconsistent examples (2026-10-29)

The Starter Kit's illustrative README tree is looser than the actual checker. The template's orchestration heading and ASCII mapping examples also differ from the checker regex. Use only SKILL.md plus directly linked references/*.md; H1 Orchestration, Generation-time capability evidence, and Unicode-arrow mappings. Actual exact-package checker result: exit 0, 0 errors, 0 warnings. This is not NAS success. No versioned release was created because owner approval is required by AGENTS.md.

### D011 — Keep recheck scope genuinely bounded (2026-10-29)

The frozen dossier has six base documents plus L7. The repair evaluates the affected A001 against L1+L7, not a silently enlarged seven-document review. Unchanged rows keep original six-document provenance. If real impact or source stability cannot be established, ask for mapping or a fresh bounded review; do not copy historical positives as current facts.

## Phase 1.1 decisions (2026-10-29)

- **D012 — Clause-level correction:** reproduced an independent-restriction false positive in the original local reference policy. Replace document-level suppression with exact clause/dimension edges, preserving unrelated restrictions and unresolved conflicts. Keep original oracle, text corpus and historical results unchanged; freeze a separate adversarial-v1 expectation file before policy changes. Current evidence is in [docs/12](12-phase1-1-review.md).
- **D013 — Three delta layers and semantic boundary:** report input changes even when statuses remain unchanged, with actual proof and uncertainty. A controlled external manual-review ledger protects local test interpretations; it is not general language entailment or an invented expert schema. Real physical PDFs/images are separate fixtures, not submitted Skill contents.
- **D014 — Disable saving:** remove the active knowledge-agent mapping and save command while non-overwrite behavior is unknown. Return reports in chat even with alleged approval. The older conditional-save architecture is historical; any future implementation requires documented safety and a reviewed Skill change.
- **D015 — Honest model limitations:** a fixed three-case local phi4-mini blind probe returned 2/3 correct classifications, 1/3 exact quotes and 0/1 required A002 input delta. An earlier exploratory request leaked expected labels and is excluded from accuracy evidence. Record PARTIAL separately from deterministic passes. No claim of model-level injection resistance, full Skill execution or NAS success. Proceed to Phase 2 only conditionally, preserving human review and the evidence-locator fallback.

## Owner decisions intentionally pending (unchanged)

- Final project name/track after technical go/no-go.
- Whether the GitHub repository eventually becomes public.
- Whether to add an open-source license.
- Whether to use real user interview feedback in the submission.
- Any real user data or NAS external model routing decisions.
- Actual Devpost final submission.
