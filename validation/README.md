# Local development evidence — exclude from Skill packaging

This directory is not an Uliya runtime, a submitted Skill component or NAS footage. The only Skill candidate is `../rightsgap-media-reuse/`.

`fixtures/oracle-source.md` preserves the exact initial docs/08 bytes. `fixtures/oracle.json` froze baseline statuses and negative expectations before the Skill and evaluator were written. Its SHA-256 is hardcoded in the runner; a mismatch refuses evaluation. This was a local chronological freeze, not signed external preregistration. `corpus.json` holds the original six fictional asset identities, six agreement texts, one amendment and an untrusted injection sample. Those original paths remain labels. New Phase 1.1 physical artifacts live separately under `fixtures/physical/` and do not alter the original oracle or corpus.

`reference_policy.py` is a deterministic clause/dimension policy model. It requires explicit completed coverage and a separate trusted manual-review ledger for exact source/clause interpretation, reconciles known reviewed clauses, preserves independent restrictions, and applies only scoped amendment edges. Its local structures are **not** documented UGOS response fields or automatic language entailment. It does not execute the Markdown's natural-language reasoning. `clause_fixtures.py` supplies labelled synthetic interpretations; the actual Uliya model could violate them. Saving is now disabled even with supplied mock approval.

Run from repository root:

```powershell
python -B validation/run_offline.py
python -B validation/run_hardening.py
```

Original Phase 1 results and oracle bytes remain unchanged. Current results are written to `results/phase1-1/regression.json` and `hardening.json`; both reject duplicate assertion IDs. The original 206 assertions had 158 unique names. New separately frozen `fixtures/adversarial-v1-expected.json` covers partial amendments, independent restrictions, uncertain authority, wrong sources and semantic misattribution. The two old approved-save expectations are retired because saving is deliberately disabled; their historical results remain available.

`fixtures/physical/` now contains six ORIGINAL geometric JPEGs, six synthetic agreement PDFs, one partial amendment, one image-only scan and one inert injection PDF. The physical L1 includes independent R1 and is a separately labelled variant. Its manifest records actual identities, extracted text, hashes, rendered checks and a source-grounded restriction result. These are not the final Round 1 PDF. Select bounded source subsets; all nine PDFs do not fit the initial six-document bound.

To regenerate physical fixtures, install the pinned optional `requirements-fixtures.txt` in an isolated environment, then run `python -B validation/build_physical.py`. The PDF skill's artifact marker must precede an authoring invocation; read-only verification does not need it. Generated render previews and contact sheets are in `results/phase1-1/`. Text extraction uses pypdf; all nine PDFs render through Poppler. The scan deliberately has no text layer; OCR is not asserted.

`delegation_context.py` only constructs and locally parses commands. It never dispatches them; tests cover complete context, Unicode, apostrophes, spaces, duplicate identities, instruction-shaped data and rejected traversal. The Skill directly links a complete synthetic command example.

Optional `run_local_model.py` performs three bounded **local Ollama text-only probes**, separately from policy tests, and persists exact prompts/raw responses. It is not Uliya, registered expert or full SKILL.md execution. Initial exploratory `local-model.json` accidentally included expected labels in user input, so its status matches are excluded from accuracy claims. The corrected `local-model-blind.json` withholds expected labels; no other prompt wording is tuned. Record all failures, missing fields, invalid quotes and explanation defects; a correct final label alone is insufficient. No tools or save are executed by this model probe.

Current official checker evidence is retained under `results/phase1-1/checker*.json`; historical checker evidence remains at the original location. Download the exact official archive from the audit's source URL and run its unmodified `scripts/check-skill.mjs` against the explicit Skill directory. `official/capability-selection.json` retains eight reviewed Action definitions outside the package; it is development provenance, not a direct invocation instruction.

The physical layer proves only local PDF/image decoding, known clause presence and rendering. None of these tests proves arbitrary semantic extraction, document truth, robust model injection resistance, path confinement on NAS, platform approval, safe save behavior or actual Uliya/NAS execution. See docs/12 for current measured results, blind-model limitations and the conditional Phase 2 recommendation.
