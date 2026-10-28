# Local development evidence — exclude from Skill packaging

This directory is not an Uliya runtime, a submitted Skill component or NAS footage. The only Skill candidate is `../rightsgap-media-reuse/`.

`fixtures/oracle-source.md` preserves the exact initial docs/08 bytes. `fixtures/oracle.json` freezes baseline statuses and negative expectations before the Skill and evaluator were written. Its SHA-256 is hardcoded in the runner; a mismatch refuses evaluation. This is a local chronological freeze, not a signed external preregistration or a Git commit. `corpus.json` holds six fictional asset identities, six fictional agreement texts, one amendment and an untrusted injection sample. PDF/JPEG paths are labels only; no physical PDFs or images were generated or parsed.

`reference_policy.py` is a manually annotated deterministic policy model. It checks source text membership, six-dimensional terms, scope failure precedence, scenario changes and a simulated save boundary. Its local structures are **not** documented UGOS response fields. It neither executes nor automatically validates the Markdown's natural-language reasoning; the Uliya model could still violate these rules. No LLM, NAS endpoint or cloud service is called.

Run from repository root:

```powershell
python -B validation/run_offline.py
```

Results are written to `results/offline.json`, including individual failures, denominators and limitations. Official checker results are separately retained in `results/checker.json` and `results/checker-execution.json`. Download the exact official archive from the audit's source URL and run its unmodified `scripts/check-skill.mjs` against the explicit Skill directory to reproduce the static check. `official/capability-selection.json` retains the eight reviewed Action definitions with source identity and catalog hash; it is development provenance, not an instruction to call those Actions directly.

No tests here prove real PDF extraction, document truth, prompt-injection resistance in a model, path confinement on NAS, approval enforcement or safe save behavior. Those require authorized target-device observations. The Round 2 checklist is in docs/11.
