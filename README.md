# Planet Nine: current evidence map

A real-data project around one question: **where could Planet Nine be tonight, given published evidence?**

Live site: <https://zikalify.github.io/planet-nine-audit/>

The site propagates a **published** orbit ensemble to today's date in your browser, subtracts what published telescope searches already ruled out, and shows the current state of the dynamical evidence that started the hunt. Every number traces to a published source; nothing is invented. It is not a detection and no such claim is made.

## What is here

- **Live sky map** (`docs/index.html`): 21,740 samples of the Brown & Batygin (2021) reference population that were **not** flagged as detectable by the published ZTF / DES / Pan-STARRS searches, propagated from their published 2018 elements to the current date, plus the excluded model region, published (unconfirmed) infrared candidate positions, and the galactic plane. Source: CaltechDATA v3, MD5-verified.
- **Dynamical evidence panel**: an independent implementation of the apsidal-clustering conditional likelihood of Siraj, Chyba & Tremaine (2026), applied to their sample reconstructed from published tables and JPL data. It reproduces every published significance and direction in the paper's Table 1 (measured deviation ≤0.05σ, ≤2°) and shows what the evidence actually says today: clustering near ~2σ, direction constrained to about half the sky.
- **Census tracker**: count of distant MPC objects currently meeting the paper's census filters, with the reason new objects cannot join the sample without published stability classifications.
- **Coverage-audit kernel** (`p9audit/core.py`): the earlier research prototype for bounding detection coverage across dependent searches. Its bundled example probabilities are **synthetic and labelled as such**; it is a methods library, not a result.

## Run the checks

Python 3.10+, no runtime dependencies beyond numpy/pandas/scipy:

```sh
python3 -m unittest discover -s tests -v   # includes anchor-reproduction tests
node tests/site.test.cjs                   # map math against published rows
```

Rebuild the site data from primary sources (downloads the 13 MB CSV, verifies its
MD5 against the record, recomputes everything):

```sh
python3 -m p9audit.build_live --output docs/site/live-data.json
```

## Honest limits

- The sky map is **conditional on a 2021 model**. The May 2026 clustering reassessment (Siraj, Chyba & Tremaine) weakened the underlying evidence to ~1.9σ and found existing sky maps too narrow. We show both, separately; we do not merge them into a false joint answer.
- Propagation is two-body. Measured drift versus full JPL n-body ephemerides over 2018-2026 is ≤ ~0.03° on real Sedna-class orbits; epoch reproduction is limited to ~0.01-0.06° by the two-decimal precision of the published elements. Neither matters at the map's ~1° resolution.
- Candidate markers are published but unconfirmed positions, each with its paper's own caveats.
- Nothing here locates Planet Nine, proves or disproves its existence, or schedules a telescope.

Docs: [research review](docs/research.md) · [method](docs/method.md) · [validation record](docs/validation.md) · [input contract](docs/data-contract.md) · [roadmap & project checklist](TODO.md)
