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
| The starter page links the 0.7.3 kit | Verified on 2026-10-28 | Recheck before implementation |
| Catalog 2.0.0 lists 9 CLI families / 6 registered agents | Verified in prior archive audit | Must independently re-read current archive in Phase 1 |
| ug-document.qa can be instructed to seek file-specific evidence | Verified at declaration/parameter level in prior audit | Actual quote and citation quality Unknown |
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

## Owner decisions intentionally pending

- Final project name/track after technical go/no-go.
- Whether the GitHub repository eventually becomes public.
- Whether to add an open-source license.
- Whether to use real user interview feedback in the submission.
- Any real user data or NAS external model routing decisions.
- Actual Devpost final submission.
