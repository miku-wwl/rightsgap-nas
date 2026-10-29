# RightsGap Phase 1.3 / Phase 2 engineering review

This is an **engineering REVIEW package**, not the official Devpost submission. Nothing here demonstrates actual Uliya or NAS execution. Saving is DISABLED. No paid request runs when the archive is opened or the offline commands below are executed.

**Phase 1.3 PASS; Phase 2 full reliability acceptance FAIL; recommendation NO_GO for submission readiness.** Static and simulated workflows pass, but the external study is strict 7/12 and includes four positive dimension labels under incomplete scope. Auditing those observations successfully does not turn them into accepted answers.

## Read first

- [Phase 1.3 result and root causes](docs/14-phase1-3-hardening-report.md).
- [Phase 2 workflow, observations and unresolved risks](docs/15-phase2-supervised-workflow-report.md).
- [One-day real NAS runbook](docs/16-nas-runtime-validation-runbook.md).
- [Generated human-readable simulated report](validation/results/phase2/example-report.md).

## Result layers

| Layer | Meaning / limits |
| --- | --- |
| Historical Phase 1/1.1/1.2 | Preserved observations and frozen expectations; 73 protected files are byte-exact. Old strict 8/10 is not rescored into a better historical claim. |
| Phase 1.3 reference policy | Curated synthetic annotations and deterministic tests, not execution of SKILL.md or arbitrary natural-language entailment. |
| Official static checker | Actual current official tool output for the exact four Markdown files. Static PASS cannot prove runtime behavior. |
| SIMULATED_EXPERT_RESULTS | Frozen source-by-source business observations. Authoring commands are constructed/parsed locally and never dispatched. Internal JSON fields are not official return schemas. |
| External DeepSeek | Separate synthetic text-only observations; no tools or real documents. PARTIAL strict results and rejected answers remain visible. Model alias is not independent backend proof. |
| Semantic review | Final-content-hash-bound Codex agent review against supplied text and frozen rubric; no human/legal review. The audit verifies the record, not its infallibility. |
| Uliya / NAS | Both NOT_RUN. The runbook describes future authorized work. |

VERIFIED applies to observed local checks, actual model envelopes/usage and exact static output. ASSUMED applies to curated documentary meanings, synthetic applicability and complete mock inventory. UNKNOWN includes actual OCR, source coverage, permission enforcement, response schemas, model route and real legal authority.

## Reproduce ordinary checks without credentials

Use Python 3.10+ from the unpacked repository root. The tools use only the Python standard library. These commands make no network/model/NAS requests and do not require an API key:

```powershell
python -B validation/run_offline.py
python -B validation/run_hardening.py
python -B validation/run_phase13.py
python -B validation/offline_audit.py
python -B validation/run_phase2.py
python -B validation/review_phase2_llm.py
python -B validation/audit_phase2.py
```

On the original workstation, `python -B validation/finish_phase2.py` additionally reruns the installed official checker and records engineering gates. It deliberately exits 2 for the observed Phase 2 acceptance FAIL even though its local verification subprocesses succeed. It makes no paid request. On another machine, use the separate portable official-check command below instead of the workstation-specific gate wrapper.

Without DEEPSEEK_API_KEY, the ordinary audit still passes its ordinary checks and records the exact-value secret scan NOT_RUN. Pattern scanning cannot prove absence of every encoded secret. To enforce a keyless child, remove the variable only from the child environment; do not print any environment value. No credential discovery is needed. `.git` is intentionally absent from the review ZIP and is not required for hash/statistic checks.

The historical runner output defaults now point to new Phase 1.3 results and refuse historical result destinations. Replaying these commands can replace **new** run receipts. Preserve the review archive before experimenting; never edit the historical or frozen expected evidence. Do not rerun fixture `freeze` preparation to change expectations.

Use the ZIP's exact file bytes for historical integrity reproduction. Older tracked fixtures/results can depend on the prior checkout's line-ending settings; a fresh Git checkout is not asserted to reproduce those raw historical worktree hashes. New gated sources/candidate bytes have explicit LF rules. The original gate and pre-normalization source/static receipts are retained under `validation/results/phase1-3/pre-lf-normalization/` to preserve the decision made before Phase 2 began.

## Reproduce the official static checker separately

The full gate runner on this workstation uses the original absolute kit location in `validation/results/phase1-3/toolchain.json`. It is an observed local path, not portable installation configuration. Independent reviewers can download/extract the verified official archive and run its checker directly against this candidate:

```powershell
node '<your actual extracted kit>/scripts/check-skill.mjs' './rightsgap-media-reuse'
```

Use a real local kit path in place of the worksheet text. Official [Starter Kit page](https://ai.ugreen.com/pages/hackathon-starter-kit) and [archive observed on 2026-10-29](https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898). Archive SHA-256: `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`; catalog 2.0.0. The exact checked Skill bytes/hashes and actual command exits are in each phase's `official-static*.json`. Future official changes require a fresh capability review.

Do not run `run_phase2_llm.py prepare/run` as part of reproduction: the study is already frozen and its authorized request budget was used. `review_phase2_llm.py` scores stored final answers offline. Its optional `--inspect B01` prints only supplied synthetic sources and deduplicated final content, never private reasoning. Raw API observations remain available for audit but private reasoning is not used to repair final answers.

## Inventory and scope

The archive includes baseline project context, historical evidence needed for integrity audits, changed/new sources, synthetic fixtures and new reports/results. Only `rightsgap-media-reuse/` is the candidate Skill: SKILL.md plus three directly linked references. All Python, reports, test inputs and credentials checks remain outside it.

`review/git-diff.patch`, `review/git-diff-summary.txt` and `review/file-manifest.json` account for tracked modifications and untracked deliverables. The ZIP verification receipt and ZIP SHA-256 are written beside the archive to avoid recursive self-hashing. They are local review evidence, not signatures or platform attestations.

No commit, push, release, deployment, visibility change, external message, final submission PDF or Devpost submission was performed. The owner's final project, licensing and formal submission decisions remain pending. Continue only with supervised review and the authorized real-runtime runbook; positive publication/legal decisions remain outside scope.
