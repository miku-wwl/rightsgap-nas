# 07 — Development roadmap and submission separation

All dates below use **Pacific/Auckland (NZDT)** unless labelled otherwise. Target dates are internal milestones, not official instructions.

## Development phases

| Phase | Suggested dates | Deliverable / exit gate |
| --- | --- | --- |
| 0 Research & Registration | Complete as of 2026-10-28 | UGREEN registration confirmed; independent rule/tool research |
| 1 Technical Go/No-Go | Oct 28–30 | Current catalog audit; exact core Action/Agent plan; source quality feasibility |
| 2 Skill architecture | Oct 30–Nov 1 | Output status contract, bounded test corpus, proper delegation and error policy |
| 3 Initial Uliya Skill | Nov 1–6 | Root SKILL.md and directly linked references only; supported agent calls |
| 4 Static and behavior validation | Nov 6–10 | 0 checker errors/warnings; separate local evidence tests; honest failures documented |
| 5 Round 1 package + review | Nov 10–14 | English PDF and Skill-only ZIP, manual content QA, explicit owner approval for submission |
| 6 Assigned NAS (if finalist) | Nov 22–28 PT | One allocated test day; real device actions, recheck, demo recording |
| 7 Round 2 final (if finalist) | Nov 29–Dec 1 NZDT | Final tested package and public YouTube video under 3 min |

## Official deadlines

- Round 1: **2026-11-15 23:45 PST** = **2026-11-16 20:45 NZDT**.
- Round 2: **2026-11-30 23:45 PST** = **2026-12-01 20:45 NZDT**.
- NAS testing: one assigned remote iDX6011 Pro 64GB day between Nov 22 and Nov 28 Pacific Time, only if selected.

Reference: https://ugreenhackathon.devpost.com/rules

## Round 1 requirements

1. English PDF with **ten substantive responses totaling no more than 500 English words**, using the ten official questions. Prior research indicated PDF size cap of 1 MB; reverify in current official form/rules before exporting.
2. Initial Skill ZIP **no more than 10 MB**, root SKILL.md required, optional directly linked references/*.md. No executable scripts, extra runtime, real private data or credentials.
3. English Devpost fields, appropriate track, team/AI disclosures and third-party materials disclosures.
4. No NAS running video required for Round 1; optional local tests cannot be described as NAS execution.
5. Owner approval before clicking final Submit; inspect confirmation receipt. Registration alone is not submission.

### PDF content questions (paraphrased; consult current rule wording)

Skill function; target user/problem; solution; user flow; substantive differentiation; NAS capabilities per step; technical approach/agents/permissions/data; current development state; two core and one edge test; known limitations.

## Skill ZIP assembly protocol

- Generate under a dedicated skill directory, separate from README and docs.
- Verify frontmatter, allowed files, references, registered agents and checker diagnostics against current official package.
- ZIP only that exact validated directory in the structure required by the checker.
- Review archive listing and size. Keep a distinct copy of Round 1 submission materials after submitting.
- Never put this entire developer repository bootstrap ZIP into Devpost's Skill ZIP field.

## Round 2 rehearsal protocol

1. Have synthetic, original PDFs and small image corpus ready before the assigned day.
2. During access verify login, Skill installation, valid file paths, model/QA source output, and actual approval prompts.
3. Execute Scenario A and B; capture source and honest delta. Test a denied/partial case. Save report only if supported and approved.
4. Record the actual NAS UI/workflow and retain non-sensitive logs/evidence before credentials expire.
5. Create a public YouTube demo under three minutes, narrated/subtitled in English; do not use unauthorized third-party media or fabricated runtime screens.
6. Submit the same project's final Skill package, disclosures and video to the private finalist link after owner approval.

Official guidance: https://ugreenhackathon.devpost.com/resources
