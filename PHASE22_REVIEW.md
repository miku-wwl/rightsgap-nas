# RightsGap NAS Phase 2.2 engineering review

**PARTIAL overall; authorized offline engineering complete. Phase 3 materials are DRAFT only.** Read [the hardening report](docs/19-phase2-2-report-contract-hardening.md), [validation/gates](docs/20-phase2-2-validation-report.md), [English proposal](docs/21-round1-english-proposal-draft.md) and [submission checklist](docs/22-round1-submission-readiness-checklist.md).

This engineering ZIP is **not** the official competition Skill ZIP. It deliberately includes local Python tests and synthetic attack evidence, which must never enter the submitted Markdown Skill. Saving remains DISABLED. No current external, independent human, Uliya or NAS result is claimed. No paid request, commit, push or Devpost submission occurred.

Verified local results: historical four suites 1,186/1,186; Phase 2.1 590/590; separate old clarification 6/6; Phase 2.2 oracle/contracts 657/657 and new evaluator controls 34/34. These are dependent assertions, not independent documents. Current official checker exit 0 with zero errors/warnings. The initial two regression-orchestration failures and optional public-source HTTP 403 failure are preserved in the reports and receipts.

The frozen twelve-request synthetic DeepSeek plan is unpaid and unexecuted. Proposed conservative peak ceiling USD 0.2998599, cap USD 0.30. No Phase 2.2 authorization or credential was read/inferred from earlier spending. The plan has no callable API executor. Later authorization requires freeze/price revalidation, no retries/fallback, actual returned model identifiers and separate content-bound citation/semantic review. Do not tune this final holdout after observations.

## Review first

- Read the exact changes to Input Delta, source identity/state, independent versus coupled grants and evidence-repair questions in the Markdown references.
- Inspect [H21-K original findings](validation/results/phase2-2/H21-K-investigation.json). Its original projection dispute and three conservative mismatches remain unresolved for human adjudication; the old expectation and 3/12 score are unchanged.
- Complete [the human worksheet](validation/results/phase2-2/human-review-worksheet.md). It has eight new representative cases, exact excerpts, expected statuses, NOT_RUN current model statuses, specific repair questions and no signatures.
- Use [gates.json](validation/results/phase2-2/gates.json). G0/G1/G2 PASS; G3–G7 NOT_RUN. The human worksheet and null semantic template are preparation, not endorsements.

## Credential-free reproduction

Unpack to a disposable local directory. Standard-library Python is sufficient for the new tests; no paid call, optional model runner, fixture regeneration or NAS is needed:

```powershell
python -B validation/run_phase22.py
python -B validation/test_phase22_evaluator.py
```

These overwrite only their Phase 2.2 result files in that disposable copy. Preserve the original archive for comparison. `phase22_cases.py`, `prepare_phase22_baseline.py` and `prepare_phase22_materials.py` are one-time authoring/capture tools and refuse to overwrite frozen records; do not rerun them as tests.

The original four-suite replay can run from a second disposable unpacked copy before other historical runners modify its outputs:

```powershell
python -B validation/replay_phase21_history.py
```

For the other historical suites, run `run_phase21.py`, `test_phase21_evaluator.py` and `check_phase21_clarifications.py` in a disposable copy. Their outputs are historical paths; never run them in the protected working repository during review. `validate_phase22.py` is the original-workspace orchestrator and requires the complete starting tracked-byte manifest; the archive explicitly omits old ZIPs and two private-reasoning payloads, so its complete-workspace audit is not a standalone archive command. Do not claim omitted bytes were checked from this ZIP.

The actual current official check can be reproduced with Node and the separately obtained [current official kit](https://ai.ugreen.com/pages/hackathon-starter-kit): invoke its `scripts/check-skill.mjs` against the unpacked `rightsgap-media-reuse` directory. Verify tool hashes against `validation/results/phase2-2/toolchain.json`. The original workstation path is recorded for provenance, not a portable dependency. The archive does not redistribute the tool itself or invent a license for it.

## Integrity and disclosure

`review-phase22/file-manifest.json` and `SHA256SUMS.txt` account for every included payload; the manifest/checksum files themselves are excluded from their own recursive inventory. The separate archive verification JSON records CRC, byte/hash checks, safe names, duplicate checks and ZIP SHA-256. `archive-scope.json` identifies omitted old review ZIPs and private-reasoning payloads with their original hashes. Previously sanitized historical final answers already in `review-phase21/` retain their origin; they are not new Phase 2.2 observations.

No `.env`, credential file, `.git`, dependency folder, new private document or unnecessary unrelated project asset is included. Credential checks use common patterns only; exact-value scanning is NOT_RUN because this task deliberately does not read credentials. This is not a guarantee against every encoded secret. All fixture documents are synthetic, and instruction-shaped text stays labelled untrusted test data.

Final owner decisions remain: actual evidence review, further spending if desired, final project/track, eligibility and member declarations, truthful AI/third-party disclosure and final proposal approval. Final PDF, official ZIP and Devpost submission each remain unperformed. Round 1 does not require real NAS evidence; any runtime claim or Round 2 footage still requires genuine assigned access.
