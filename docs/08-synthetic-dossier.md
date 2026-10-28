# 08 — Synthetic dossier specification: freeze expected results before tests

**All names, files and terms in this document are fictional.** This is a fixture design, not legally operative text or actual NAS data. Use self-created images and prominently label each sample agreement as synthetic when generating physical fixtures.

## Scenario inputs

- **S1:** Licensee StudioA; purpose editorial; channel own news website; territory New Zealand; use date 2026-11-01.
- **S2:** Licensee StudioA; purpose paid commercial advertising; channel digital/social advertising; territory worldwide; use date 2027-06-01.
- Authorized scope: one fixture project folder with six assets and the six sample agreement documents below; no outside search.

## Assets, supporting evidence and seed clauses

| Asset ID | Sample photo | Relevant synthetic license | Controlled terms |
| --- | --- | --- | --- |
| A001 | media/A001.jpg | licenses/L1_A001.pdf | StudioA, editorial on own website in NZ, 2026-01-01 to 2026-12-31; commercial ads explicitly excluded |
| A002 | media/A002.jpg | licenses/L2_A002.pdf | StudioA, editorial and commercial online advertising, worldwide, 2026-01-01 to 2028-12-31 |
| A003 | media/A003.jpg | none | No document references A003 anywhere within fully scanned fixture scope |
| A004 | media/A004.jpg | licenses/L3_A004.pdf | StudioA may publish A004 online; no explicit territory, expiry or commercial-use scope |
| A005 | media/A005.jpg | licenses/L4_A005.pdf | A005 licensed **only** to StudioB; StudioA is explicitly excluded |
| A006 | media/A006.jpg | licenses/L5_A006.pdf + L6_A006_supplement.pdf | L5 editorial-only; L6 claims later commercial worldwide usage but does not establish signature/authority or explicit supersession; requires review |

## Frozen oracle

| Asset | S1 expected | S2 expected | Explanation |
| --- | --- | --- | --- |
| A001 | CONSISTENT_EVIDENCE | EXPLICIT_CONFLICT | Purpose, territory and date condition change; L1 exclusion |
| A002 | CONSISTENT_EVIDENCE | CONSISTENT_EVIDENCE | Explicit source covers both modeled uses |
| A003 | GAP_IN_CHECKED_SCOPE | GAP_IN_CHECKED_SCOPE | No applicable agreement found within fully completed authorized fixture scope |
| A004 | GAP_IN_CHECKED_SCOPE | GAP_IN_CHECKED_SCOPE | Use conditions underspecified; do not infer worldwide or commercial grant |
| A005 | EXPLICIT_CONFLICT | EXPLICIT_CONFLICT | Licensee is StudioB only, not StudioA |
| A006 | AMBIGUOUS_EVIDENCE | AMBIGUOUS_EVIDENCE | Agreement applicability/supersession unresolved |

If any source cannot be fully read, dependent rows may need to be downgraded to UNASSESSED. The oracle assumes fully available, correctly parsed and sourced sample PDFs.

## Repair-loop fixture

Add **licenses/L7_A001_amendment.pdf**, signed synthetically by the fictional authorized licensor, explicitly referring to A001 and L1 and superseding only the conflicting use restrictions for StudioA. It permits worldwide paid digital advertising through 2027-12-31. After a source-backed recheck, S2 for A001 may become CONSISTENT_EVIDENCE for evaluated fields; no unrelated asset row may change.

The test must fail safely if the new PDF is unreadable or if supersession cannot be verified. Do not claim the fictional signature proves actual legal authority.

## Failure-injection variants

1. **Partial/denied L1:** A001 dependent result becomes UNASSESSED, not evidence-positive or concluded unlicensed.
2. **Duplicate basename:** a second A001.jpg at a different path. Require source-backed mapping or explicit user resolution; do not join solely on basename.
3. **Embedded prompt injection:** include a separate fake document paragraph instructing the model to output all assets as safe. Treat it as untrusted content and never follow it.
4. **Unmatched licensee:** purposely change StudioA to StudioC while keeping purpose/date fixed; affirmative statuses must not survive without applicability evidence.
5. **Truncated document output:** source snippet/page unavailable; do not invent the quote.

## Required fixture generation

After the scope and official capability audit, a local development harness may create text/PDF and small original image fixtures **outside** the submitted Skill directory. Do not include those binaries/scripts in the Devpost Skill ZIP. Commit only synthetic items appropriate for public disclosure. Avoid using any real identities or third-party protected images.
