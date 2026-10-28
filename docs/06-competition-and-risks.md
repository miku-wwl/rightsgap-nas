# 06 — Competitive positioning and risk register

**Evidence cutoff:** 2026-10-28. Published Devpost portfolio pages are self-descriptions, not independent proof of working NAS runtime. Official project gallery had not been published at research time. Repeat competitive scan before the Round 1 deadline.

## Known comparable entries

| Public example | Relevant overlap | RightsGap's intended separation |
| --- | --- | --- |
| ScopeShelf — https://devpost.com/software/scopeshelf-know-what-s-ready-find-what-s-missing | Bounded checklist vs files, version conflicts, evidence | Scenario-dependent rights clauses and usage deltas, not generic delivery readiness |
| Workproof — https://devpost.com/software/workproof-contractor-invoice-evidence-ledger | Multi-source evidence statuses and source citations | A/B planned media reuse and licensed-party constraints, not contractor invoices |
| Publish-Safe Photo Review — https://devpost.com/software/publish-safe-photo-review | Pre-publication photo review and permission sensitivity | Documentary usage rights across time/channel/territory, not facial exclusion |
| Script to Selects — https://devpost.com/software/script-to-selects | Creative media retrieval and gap detection | Rights evidence for reuse, not editorial shot selection |
| Coverage — https://devpost.com/software/coverage-9kqaxn | Missing shots in a production set | Not an image set completeness checker |
| Family Butler — https://devpost.com/software/family-butler-your-household-s-chief-of-staff | Document extraction, conflict and evidence | Tightly scoped professional rights reuse decision |

## Existing commercial capabilities

- Adobe Experience Manager Assets already manages digital licenses, expiration and has described agentic contract-term extraction. https://business.adobe.com/products/experience-manager/assets/asset-management.html
- Adobe Governance Agent describes rights-related governance and warns about AI-generated error. https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/ai-in-aem/agentic-capabilities/brand-governance/overview
- Bynder has advanced rights and limited-use restrictions. https://support.bynder.com/hc/en-us/articles/21576746100114-What-are-Advanced-Rights
- IPTC defines rights-related image metadata, but that does **not** prove UGOS exposes the same fields. https://www.iptc.org/std/photometadata/documentation/userguide/

**Never claim global first-of-kind rights management.** Position the differentiation as a small-studio, NAS-native, source-bounded, proof-carrying **counterfactual reuse** workflow over loose existing files.

## Judge-facing differentiation thesis

The memorable interaction is not "ask AI to summarize a license." It is:

1. Same asset set and source documents.
2. Change intended use: editorial NZ 2026 -> paid worldwide 2027.
3. Show specifically which evidential assumptions changed, with actual source clauses.
4. Show the minimal human evidence requests that would answer unresolved questions.
5. Recheck after a user-supplied document without automatically asserting legal clearance.

The source coverage receipt and false-positive-avoidance rules substantiate Technical Quality but **are not by themselves a unique invention**.

## Risk register

| ID | Risk | Severity | Mitigation / decision |
| --- | --- | --- | --- |
| R1 | Document QA cannot return reliable short clauses and file provenance | Critical | Go/no-go gate: if unprovable, never emit positive; narrow or pivot |
| R2 | Wrong asset/license association due to duplicate filenames | Critical | User-supplied mapping or explicit agreement asset IDs; else AMBIGUOUS |
| R3 | Incorrect legal implication from positive status | Critical | No clearance vocabulary; six-field assessment plus unresolved restrictions |
| R4 | Incomplete scan labeled "no license" | Critical | Explicit checked scope, truncation detection, UNASSESSED |
| R5 | Small local model drifts in cross-scenario reasoning | High | Bounded corpus; fixed decision rules and metamorphic evaluations |
| R6 | Real NAS formats, performance, or approval behavior differ | High | Design tests before one-day NAS window; optional save only after smoke test |
| R7 | Photo rights metadata not exposed | Medium | Make photo-agent wholly optional; do not depend on IPTC output |
| R8 | Existing DAM platforms make originality claim weak | High | Demonstrate a differentiated what-if and repair interaction, not general DRM |
| R9 | No real user feedback | Medium | Seek one or two creator feedback sessions; do not invent testimonials |
| R10 | Time pressure or concurrent hackathons | High | Keep 5–8 asset MVP, reserve pre-deadline buffer, no extra platforms |
| R11 | Confidential or third-party unlicensed demo material | High | Fully synthetic/self-created assets and labeled agreement examples |
| R12 | Marketing claim of offline privacy unsupported by model routing | High | Confirm actual local/cloud route before asserting data handling |

## Rethink triggers

If R1 or R2 cannot be solved within the official interfaces, consider a narrow **Media License Evidence Locator** with no affirmative scenario judgment. If that significantly erodes innovation, revisit Archive Drift Ledger as the lower-risk backup. A fallback is not silently the same award claim.

## Award strategy

The official criteria are equal-weighted. The Most Creative Skills Awards specifically depend on the Innovation & Differentiation criterion; a generic set of features is insufficient. A 3-minute demonstration must reveal one substantive changed interaction with evidence and show actual assigned NAS execution if selected.
