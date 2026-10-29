# RightsGap Phase 2.1 engineering handoff

Read [the integrity implementation report](docs/17-phase2-1-evidence-integrity-report.md) and [the validation/gate report](docs/18-phase2-1-validation-report.md). This is an engineering review archive, not the official Round 1 submission. Saving is DISABLED. Actual Uliya and NAS execution are NOT_RUN.

The phase is **PARTIAL**. The frozen v1 external proxy has zero observed unsafe effective dimensions and zero unsupported positive citation occurrences, but strict acceptance is only **3/12**. The final v2 Markdown revision clarifies report formatting and repair questions after the study and has **no external retest**. Do not assign the v1 observations to a newly tested v2 Skill.

## Result layers

| Layer | What was actually observed |
| --- | --- |
| Historical raw evidence | Protected in the workspace by the 180-file starting manifest. The review ZIP omits the old ZIP and two old private-reasoning payloads; sanitized historical final answers are provided as derived files. |
| Historical deterministic replay | Original four runners, same frozen fixtures, in an isolated baseline Skill copy; 1,186 assertions. No historical workspace result overwritten. |
| Phase 2.1 oracle | Twelve pre-model frozen cases, seven mutations, state/scope/claim controls and legacy compatibility. Curated semantic annotations, no arbitrary text entailment. |
| Evaluator controls | Nine adversarial checks, including genuine irrelevant quote, missing semantic review and overall-only uncertainty mask. |
| Qualification diagnostic | Two separately frozen, unpaid cases created after H21-K to contrast expressly independent versus expressly coupled terms; six assertions. Not part of the original holdout or a score repair. |
| External v1 proxy | Twelve single synthetic requests. Final content and usage retained; private reasoning omitted. One Codex agent semantic reviewer; independent human review NOT_RUN. |
| Final v2 candidate | Four Markdown files, official static PASS. Report-only post-study clarification; external retest NOT_RUN. |
| Uliya / NAS | Both NOT_RUN; static, simulated and proxy results cannot fill runtime gates. |

## Reproduce without credentials or paid requests

Use Python 3.10+ from the unpacked project root. No third-party Python dependency is required for these commands:

```powershell
python -B validation/run_phase21.py
python -B validation/test_phase21_evaluator.py
python -B validation/check_phase21_clarifications.py
python -B validation/replay_phase21_history.py
python -B validation/replay_phase21_score.py
python -B validation/audit_phase21.py
```

These commands use explicit local fixture paths and stored final answers. They do not call any model, Expert Agent or NAS. The historical replay and score replay use temporary isolated directories and preserve the historical workspace files. New result receipts may be regenerated; keep the review ZIP before experimentation.

`replay_phase21_score.py` supplies the exact frozen v1 candidate snapshot to the unchanged study evaluator. Direct `evaluate_phase21.py` scoring from the final v2 root intentionally rejects the changed candidate hash. `evaluate_phase21.py --inspect H21-B` displays only provided source facts and deduplicated final answer text. There is no automatic answer normalization or private-reasoning repair.

The ordinary audit requires no key. If an exact process key is absent, its exact-value secret scan is NOT_RUN while ordinary checks still execute. Common-pattern checks cannot detect every possible encoded credential. No credential discovery is performed. The archive has no `.git`; audit explicitly reports the three omitted baseline payloads and verifies all available protected bytes rather than claiming to check missing data.

## Official checker reproduction

The workstation's actual tool location and checksums are recorded in [toolchain.json](validation/results/phase2-1/toolchain.json). To rerun the official static check on another machine, obtain the official kit from the [Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit), verify its recorded hashes, and run the observed supported form with a real local kit path:

```powershell
node '<your actual kit>/scripts/check-skill.mjs' './rightsgap-media-reuse'
```

The local `finish_phase21.py` wrapper uses the recorded workstation kit path, runs only offline/static checks and writes separate acceptance gates. Static success is not model or NAS success. Do not rerun the paid runner or fixture preparation: the study is frozen and all twelve authorized attempts have been used. Budget estimates are not invoices.

## Review contents and next work

`review-phase21/file-manifest.json` accounts for source/evidence hashes; `archive-scope.json` names omitted historical payloads. Derived historical final-answer files preserve final content and record their original source-file hashes; they are not replacements for historical raw files. The current four-file Skill contains no executable, fixture, README or test infrastructure.

Proceed only to supervised **Phase 2.2: report contract and qualified-grant interpretation**, with the final v2 output rules independently checked before any newly authorized holdout budget. Then use an actually authorized device window for [the real NAS runbook](docs/16-nas-runtime-validation-runbook.md). Human review remains pending, source contents remain untrusted, and no output is legal clearance or a publication decision. No commit, push, release, visibility change, external message or Devpost submission was performed in Phase 2.1.
