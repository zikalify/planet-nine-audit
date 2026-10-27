# Planet Nine Search Audit

A research prototype for **auditing search coverage under competing hypothetical-planet models**. It does not know where Planet Nine is, establish that it exists, or track a detected planet.

## Why build this?

Ephemeris prediction, survey simulation and moving-source detection already exist. Sorcha simulates discovery selection, KBMOD searches images, and Planet Nein has used the Planet Nine reference population with Sorcha. Rebuilding these would not be an honest innovation claim.

This small complementary tool asks: **does a proposed follow-up still add coverage when model weights change and overlapping searches are not assumed independent?** It exposes assumptions that a single attractive sky map can hide. This is an engineering hypothesis about usefulness, not a claim of scientific novelty or validated research impact.

## Run in under a minute

Python 3.10+, no runtime dependencies or network required:

```sh
python3 -m unittest discover -s tests -v
python3 -m p9audit.cli examples --selected archive-a archive-b --output examples/audit.json
```

Or `pip install .` then `p9audit examples --selected archive-a archive-b --output audit.json`.

**Every bundled probability in `examples/` is invented.** Its models are not fitted to observations. The output is labelled SYNTHETIC. Do not cite it as real sky coverage or discovery probability.

## What works

- Multiple weighted particle models, normalized separately.
- Survey-level per-particle detection probabilities with explicit provenance.
- Unknown-dependence union bounds for searches sharing a dependence group.
- Explicit conditional-independence assumption between groups.
- Conditional null-likelihood intervals, not a posterior probability of existence.
- Worst-model lower-bound ranking of incremental follow-up coverage.
- Full input SHA-256 hashes, stable JSON and strict complete-matrix validation.
- Great-circle angular separation utility tested across RA wrap and poles.

No external data are downloaded or sent by the CLI. No automatic latest-research service runs. The literature snapshot was checked on **27 October 2026**.

## What still needs scientific work

This is not ready to schedule telescope time or support published exclusion claims. A researcher must supply calibrated survey-level probabilities from injection/recovery experiments or a validated simulator. A circular field and magnitude cutoff are not adequate substitutes for cadence, masks, linking, motion limits and efficiency. Grouping is a scientific judgment: if independence is not defensible, put the searches together and accept wider bounds.

No new orbit posterior, image ingestion, orbit fitting, ephemeris propagation, observatory visibility, candidate confirmation or live telescope integration is included. Ranking ignores cost, weather and operational feasibility. Widely different or correlated priors can change the answer. A finite set of models is not all possible hypotheses.

See [research review](docs/research.md), [method and derivation](docs/method.md), [input specification](docs/data-contract.md), and [next validation steps](docs/roadmap.md).

## Real-data reproducibility check

A separate command audits the **published binary detectability flags** in Caltech's historical 100,000-row v3 population. It uses the joint flags exactly as provided, with no independence assumption, no new exclusion calculation and no new orbit inference. The exact verified MD5 is required. This must not be confused with the synthetic probability-matrix example.

Download `reference_population.csv` from https://data.caltech.edu/records/8fjad-x7y61 and run:

```sh
python3 -m p9audit.caltech /path/to/reference_population.csv --output caltech-summary.json
```

A reproducible summary is included in `examples/caltech-v3-summary.json`; the 13 MB source data are not bundled. Coordinates in the source are at **1 June 2018**, not today. The output records source checksums and exact joint-flag counts. These model-conditional fractions are not a confidence level that the planet has been ruled out.

## What the toy result demonstrates

For the selected overlapping archives, the narrow toy model has conditional coverage between 65.0% and 82.5%, but the broad toy model has 35.0% to 47.5%. The next-field ranking chooses the invented south field by its worst-model lower gain (15.75 percentage points versus 1.75 for north). Those numbers only illustrate how assumptions change a decision. They are not real sky coordinates, measured telescope efficiencies or a recommendation to observe a southern field.

For large populations, the complete probability matrix grows with particles times searches. This first version loads it into memory and is intended for small research audits. Benchmark before adopting it at survey scale. It intentionally does not hide missing matrix entries behind a zero default.

## Static website and GitHub Pages

The self-contained interactive site is in `docs/index.html`. Open it locally to try the toy-model controls and the exact historical joint-flag explorer. It runs entirely in the browser with no accounts, uploads, tracking or network data fetches. The mathematical demo is intentionally separate from the historical dataset summary.

Run the site arithmetic tests with `node tests/site.test.cjs`. Browser checks also exercised the controls, reset and JSON download, checked console errors, and verified no horizontal overflow at 320px and 390px widths.

The repository also includes a root entry for Pages configured to publish main / (the setting found on the live repository). It uses the same assets under docs/site. No settings change is needed in that case.

For a fresh /docs setup: in this repo, Settings > Pages > Build and deployment > Source: Deploy from a branch > Branch: main > folder: /docs > Save. No custom workflow file or build dependencies are needed. GitHub may use its own Pages build process. The site URL is whatever GitHub shows after publishing; the repository alone does not prove the site is deployed.
