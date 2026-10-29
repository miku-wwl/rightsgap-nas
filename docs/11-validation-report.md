# 11 — Phase 1 implementation and validation report

## Current update — Phase 1.1 (2026-10-29)

This report below preserves historical Phase 1 evidence. Current implementation and full review are in [docs/12](12-phase1-1-review.md). The document-level supersession defect is fixed; saving is now explicitly disabled; the candidate has four Markdown files. Current official checker: exit 0, 0 errors / 0 warnings. Deterministic results: **738/738 unique assertions passed**, **0 false-positive support / 52 named non-positive case evaluations**. Six real synthetic JPEGs and nine PDFs are generated, extracted/rendered and kept outside the Skill. A separate three-case local phi4-mini blind probe is **PARTIAL**: classifications 2/3, exact quotes 1/3, A002 input delta 0/1; it is not included in deterministic PASS counts. An earlier exploratory probe leaked expected labels and is excluded from accuracy evidence. NAS runtime remains NOT RUN. The old 206-assertion run had 158 unique names and did not cover the newly reproduced independent-restriction false positive.

Date: **2026-10-29, Pacific/Auckland**. Starting Git HEAD: `718220ebeced9aa2d99918f80a17f0bf3a2ed2fd`. Initial worktree was clean. Changes remain local and uncommitted.

## Outcome and implementation

**Conditional GO for the static, source-gated RightsGap candidate.** The supported interface permits attempting bounded discovery, per-file document QA and an evidence-driven two-scenario comparison. It does not guarantee verifiable quotations, complete document coverage, correct model reasoning or NAS execution. Those failures stop dependent judgments and narrow the output to an evidence locator and human questions. No unsupported runtime workaround was created.

Implemented [rightsgap-media-reuse/SKILL.md](../rightsgap-media-reuse/SKILL.md) plus two directly linked Markdown references. The package contains **exactly three files / 22,962 bytes**: no README, tests, scripts, fixtures, manifests or binaries. It defines bounded 5–8 asset / 3–6 document discovery, explicit associations, fixed-party A/B scenarios, all six evidence dimensions and five statuses, real-result handoff between registered experts, coverage receipts, source-gated classification, repair/recheck, untrusted-evidence rules and all five public delegation states. Permission denials, incomplete/missing/truncated outputs, no matches and ambiguous amendments have explicit conservative paths.

Optional reviewed save is described only through knowledge-agent and documented workflow approval. Its no-overwrite precondition cannot currently be established from the catalog alone: **save is blocked whenever the expert lacks verified supported safety behavior**, including the present absence of target-device evidence. No NAS save was attempted. No photo metadata rights extraction, specialized license schema, automatic supersession, file mutation, publishing or external transmission feature was added.

The [capability audit](10-capability-audit.md) records exact Action arguments, ownership, effects, approvals, original return summaries and unknowns. [Decision register](09-sources-decisions.md) records the resulting scope compromises. The original evidence contract and frozen dossier remain unchanged.

## Official static checker — Verified PASS

The unmodified checker downloaded through the current official Starter Kit was run on the exact generated Skill directory, not the repository or kit:

```powershell
node "D:\Ollama\Temp\rightsgap-phase1-20261029\extracted\uliya-skill-kit\scripts\check-skill.mjs" "D:\workshop\oct\rightsgap-nas\rightsgap-media-reuse"
```

| Evidence | Actual result |
| --- | --- |
| Official archive | `uliya-skill-kit-0.7.3-en.zip` |
| Catalog / checker format | `2.0.0` / `2.0.0` (no independent checker release field) |
| Node | `v26.5.0` |
| Process exit code | **0**, captured immediately after checker process |
| Status | `static-pass` |
| Errors / warnings / info | **0 / 0 / 0** |
| Diagnostics | `[]`; no diagnostics suppressed |
| Stderr | empty |

Raw output: [checker.json](../validation/results/checker.json), [execution metadata](../validation/results/checker-execution.json), [stderr](../validation/results/checker.stderr.txt). Official source checksums are in docs/10. Checked file hashes:

| Exact Skill-relative file | SHA-256 |
| --- | --- |
| SKILL.md | `67c85646060a8efe54d50e8d92ec011d3e9911e44a85345cae3bdf04f312ed5c` |
| references/evidence-rules.md | `3b3414133ab633ea4b34e4774fe1941795240067b257c2bf1515167f5c9a935d` |
| references/report-and-recheck.md | `876fc5d7b5ee94a25415ee8dab6361c0f6ce7be1d71c0074253c0437ae1cf055` |

The checker mechanically validates package format, ownership, delegation syntax and safety patterns. Its source does not prove Action semantics, returned quotes, reasoning or enforcement. Commands in the Skill are authoring forms: runtime task assembly must include literal authorized values and actual upstream results; no real NAS command was dispatched during this phase.

Final read-only review verified all three current Skill hashes still match the checker output, package size/file count, local Markdown links, clean whitespace and the unchanged original dossier hash. `git diff --check` passed. Scoped `.gitattributes` rules preserve Skill LF bytes and frozen oracle bytes across Windows checkouts; no Git configuration was changed. Existing-file edits are limited to README and docs/03, 05, 09 status/decision updates.

## Frozen oracle and offline evidence — Verified local policy results

Before writing the Skill or evaluator, copied the original dossier to [oracle-source.md](../validation/fixtures/oracle-source.md) and wrote fixed expected statuses in [oracle.json](../validation/fixtures/oracle.json). Hashes were observed before implementation and the runner refuses changed oracle bytes:

- Dossier snapshot SHA-256: `10b9fdc4658cd194acf8bb78175677c596963440ff889d6ee617df460484ab31`.
- Oracle SHA-256: `62c3b0dfec26705f765fcab497d9891cc858694ea546623d489e06286266cc59`.

This is a local chronological freeze, not external preregistration or a signed/committed oracle. The original docs/08 was not tuned after seeing results. Additional negative-case expectations were frozen at the same point.

Run:

```powershell
python -B validation/run_offline.py
```

Actual exit code **0**, Python **3.13.9**, **206 assertions passed / 206 total; 0 failed**. Full observations, individual checks, denominators and failures are in [offline.json](../validation/results/offline.json). Test implementation and scope are explained in [validation/README.md](../validation/README.md).

**Layer limitation:** this is a deterministic Python reference model consuming manually labelled synthetic terms and mock coverage. It does **not** execute SKILL.md, query a model, call experts, parse PDF/JPEG files or verify platform behavior. Fictional `.pdf`/`.jpg` paths are fixture identities; no physical images/PDFs or real source data were used. It is outside the Skill directory and is not a replacement NAS application.

| Frozen case | S1 actual | S2 actual |
| --- | --- | --- |
| A001 | CONSISTENT_EVIDENCE | EXPLICIT_CONFLICT |
| A002 | CONSISTENT_EVIDENCE | CONSISTENT_EVIDENCE |
| A003 | GAP_IN_CHECKED_SCOPE | GAP_IN_CHECKED_SCOPE |
| A004 | GAP_IN_CHECKED_SCOPE | GAP_IN_CHECKED_SCOPE |
| A005 | EXPLICIT_CONFLICT | EXPLICIT_CONFLICT |
| A006 | AMBIGUOUS_EVIDENCE | AMBIGUOUS_EVIDENCE |

A001 changed purpose, channel, territory and time evidence statuses. A002 remained unchanged. A004's channel-level status changed while its overall gap remained, so the baseline has **five dimension delta entries**. All are reported, not just the headline A001 transition. After the explicitly scoped L1+L7 two-document recheck, A001 S2 becomes CONSISTENT_EVIDENCE under the fictional authority premise; S1 and A002–A006 retain their prior results. Other rows retain the original six-document receipt rather than claiming a fresh seven-document audit.

| Measured metric | Result and denominator |
| --- | --- |
| Baseline coverage | 12 asset/scenario rows; 72 dimension cells |
| False-positive support | **0 / 29** expected non-positive cases: 9 baseline negatives/ambiguous rows + 20 injected variants |
| Positive-row citations | **3 present / 0 absent**, baseline positive rows only |
| Supported/conflicting dimension citations | **33 present / 0 absent**, baseline evidence-bearing dimension cells |
| Changed-dimension explanations | **5 present / 0 absent**, baseline A/B changes |
| Positive dimension citations after recheck | **24 present / 0 absent**, four positive asset/scenario rows × six dimensions |
| Failure/negative variants | **20 / 20** expected outcomes; six dimension entries retained in each |
| Simulated save boundary | **7 / 7** scenarios; one denial, zero save attempts after denial |
| Unauthorized mock save attempts | **0** across audit-only, unreviewed, denied, pending and unknown collision cases |
| Failed cases | none in this reference-model run |

Variants cover denied, partial, truncated and missing results; missing/out-of-scope source; missing/fabricated clause; unknown coverage/state; failed, cancelled, waiting_user and waiting_approval; duplicate basename; unsupported summary; a known-complete empty scope; licensee mutation; unreadable amendment; and unknown amendment precedence. Metamorphic checks cover identical inputs, purpose-only mutation, unrelated-asset stability and citation conservation. The malicious fake paragraph changes no policy outputs and creates no simulated operations.

**Do not generalize these numbers:** evidence annotations and coverage are supplied to the model, not discovered. Substring membership does not prove that a clause semantically supports every dimension; that interpretation is manually labelled. The injection test checks that this deterministic policy ignores inert text; actual Uliya prompt-injection resistance is **NOT RUN**. The seven save cases model intended policy, not actual platform approval or writes. No real-world false-positive rate or target-model reliability was measured.

## G0–G4 decision

| Gate | Phase 1 assessment | Remaining condition |
| --- | --- | --- |
| G0 capability fidelity | **PASS for the narrowed static interface plan** | Source/quote/coverage fidelity remains Unknown on NAS; no unconditional positive or save promise. Unsupported branches stop. |
| G1 evidence safety | **PARTIAL** — source rules implemented; local policy negatives 0/29 false positive | Actual Skill/model must preserve six-field support and conservative failure handling. |
| G2 counterfactual correctness | **PARTIAL** — frozen baseline, repair and metamorphic model cases pass | Real model variability, exact source grounding and actual amendment handling NOT RUN. |
| G3 approval / least privilege | **PARTIAL** — read-only default and explicit stop boundaries; simulated denial pass | NAS confinement, platform approval and safe-new-save behavior NOT RUN; unsafe/unknown save remains blocked. |
| G4 Uliya technical validation | **PARTIAL overall; static portion PASS** — 0 errors/0 warnings | Installation, compatibility and same-core assigned-device execution NOT RUN. Round 1 requires no NAS run; it still cannot be claimed. |

No claim that all G0–G4 fully pass, no achieved 18/20 score and no judge-facing G5 footage. No major product pivot is justified solely by incomplete catalog output schema, since a conditional per-file attempt is supported. Pivot the failed feature to **Media License Evidence Locator** if real QA only returns unsupported summaries or associations cannot be established. Safe saving and photo rights metadata are deferred rather than promised.

## Verified / Assumed / Unknown

- **Verified:** current page-linked archive/hash, selected catalog declarations, unique agent ownership, source-gated Markdown artifact, exact-package official static pass, local reference-policy results and their recorded denominators.
- **Assumed:** the configured Uliya model can follow these instructions, construct self-contained tasks, interpret the six dimensions and preserve context over the bounded corpus. Local policy tests do not verify these assumptions.
- **Unknown:** real quoted-source/page accuracy, complete QA coverage, OCR/formats, exact nested return schemas, permissions/errors, path confinement, stable identity between reads, runtime latency/model reliability, configured local/cloud route, non-overwrite save semantics and real approval outcomes. No NAS credentials/access were supplied or sought.

## Recommended next steps and blocked issues

1. Owner review of scope/name/track and the evidence-locator fallback remains pending; no final project or submission decision was made on the owner's behalf. Do not create final Round 1 PDF, release or submit without separate authorization. No license was chosen.
2. Before device access, manually review representative expected reports against the Skill and seek authorized creator feedback if desired. A future model-based evaluation must be labelled separately and record actual model/configuration; it must not be presented as NAS proof.
3. If Round 2 access is granted, first install this same core Skill and capture actual inventory and a **single known file's QA/source-context response**. Check a real clause against the displayed source, missing-page behavior, scan coverage and format limits. This is the primary blocker to runtime-positive claims.
4. Execute S1/S2 over original synthetic media/PDFs prepared for that authorized test, then denial, truncation/empty-source, duplicate identity, A006 priority ambiguity and the inert document-injection case. Record real expert states, per-field citations, false positives, omissions, timing and any failures. Do not synthesize NAS footage.
5. Verify configured model routing and disclosed data handling before sensitive data. Enable optional save only after supported non-overwriting behavior and workflow approval/denial are established; otherwise keep chat-only output. If provenance or association fails, stop positive comparison and report a narrower evidence locator rather than claiming success.

No Git commit/push, Devpost entry/submission, release, repository visibility change or third-party message was performed. Official web downloads were read-only development research, not Skill runtime network calls.
