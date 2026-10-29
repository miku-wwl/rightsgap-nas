# Original synthetic physical test dataset — version 1.1

Every image/document is synthetic and safe for local development sharing: no real people, signatures, private data, credentials or third-party media. Every PDF visibly states SYNTHETIC TEST DOCUMENT — NOT LEGALLY OPERATIVE. The JPEGs are original geometric test cards with explicit A001–A006 identities in the manifest; pixels/filenames are not rights evidence.

`media/` contains six JPEGs. `licenses/` contains six base agreement PDFs, L7 partial amendment, EDGE image-only scan and L9 inert prompt-injection sample. Eight PDFs have extractable text; the scan deliberately has none. No OCR or NAS-format compatibility is claimed.

This is a separately versioned adversarial variant: **L1 includes independent restriction R1**. L7 changes the use grant only and must leave R1 effective, so the affected S2 result remains EXPLICIT_CONFLICT. The original frozen corpus's repair-positive expectation stays unchanged and is tested separately. Do not conflate the variants.

Select at most six documents per initial review. Use the six base sources for the initial scope; test L1+L7 or a small edge/injection subset as separately authorized revisions. Do not treat all nine as an approved initial corpus.

`manifest.json` contains actual file hashes, page counts, extracted text, media dimensions and the partial-amendment result using real local PDF source paths. Local render/contact-sheet evidence is under `validation/results/phase1-1/`. These are test fixtures, never the final Round 1 PDF or proof of legal authority, Uliya execution or NAS runtime.
