# RightsGap NAS

**Evidence-Driven Media Reuse Planner** | UGREEN AI NAS Hackathon 2026

> Bootstrap v0.1, 2026-10-28 (Pacific/Auckland). These are development specifications, not a working UGREEN NAS Skill, tested runtime, or submitted entry.

## Product idea

Small creative teams store media files, licenses, releases and amendments in separate NAS folders. A license that supported an editorial use in New Zealand in 2026 may not support paid worldwide advertising in 2027.

**RightsGap compares two explicit media-use scenarios with bounded source evidence on NAS, shows exactly which claims change and why, and identifies what still needs human review.** It never declares that a use is legally cleared.

## Three core user interactions

1. **Compare Uses:** select an authorized asset/document set and two intended-use scenarios.
2. **Explain Evidence:** show a source-linked, field-by-field scenario delta and the coverage limitations.
3. **Recheck Changes:** when a user supplies supplemental evidence, reevaluate the affected items and list unresolved questions.

## Engineering architecture

This project must become an official **Uliya Markdown orchestration Skill**, using registered expert agents through delegation. Required candidates: file-agent for ug-filesystem and document-agent for ug-document. knowledge-agent is optional for an approval-gated report save. photo-agent metadata is optional only if its relevant output is verified. Catalog support is not runtime proof.

## Repository contents

| Path | Meaning |
| --- | --- |
| AGENTS.md | Mandatory development and safety guardrails |
| docs/01-product-brief.md | Personas, product contract, MVP, exclusions |
| docs/02-evidence-contract.md | Input fields, states, citations, invariants |
| docs/03-architecture-capabilities.md | Expert plan, action map, runtime unknowns |
| docs/04-quality-gates-scorecard.md | 16.9 baseline to conditional 18/20 target |
| docs/05-validation-plan.md | Synthetic, metamorphic and failure-injection tests |
| docs/06-competition-and-risks.md | Competitors, differentiation and risks |
| docs/07-roadmap-submission.md | Dates, Round 1/2 requirements, checklists |
| docs/08-synthetic-dossier.md | Six asset fixtures with frozen expected outcomes |
| docs/09-sources-decisions.md | Official sources and open decisions |
| prompts/01-phase1-codex.md | First actionable Codex prompt after repository creation |

## Important packaging distinction

The **repository bootstrap ZIP is not the Devpost Skill ZIP**. Repository README, docs, prompts and future local test harnesses must **not** be copied wholesale into the official Skill package. A UGREEN Skill package may contain the valid root SKILL.md plus its directly linked Markdown references/ files; no executable scripts or general-purpose runtime. Follow the current official checker.

## Status

- UGREEN event registration: confirmed by entrant.
- Project: recommended RightsGap V3 direction, final scope still subject to technical go/no-go.
- Working Uliya Skill: not generated yet.
- Official checker on RightsGap: not run.
- Real NAS execution: not tested.
- 18/20: internal aspirational score, not a judge score or achieved test result.

## Official references

- Rules: https://ugreenhackathon.devpost.com/rules
- Resources: https://ugreenhackathon.devpost.com/resources
- Starter Kit: https://ai.ugreen.com/pages/hackathon-starter-kit
- Official kit archive link observed 2026-10-28: https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898

The contributor should personally review the final English PDF wording and disclose AI assistance. No software license is selected yet; do not add one without the owner's choice.
