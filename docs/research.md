# Research review

Checked 27 October 2026. This is a targeted primary-source review, not a claim to have exhausted every paper, archive, codebase or proprietary survey.

## Answer

A known current location of Planet Nine is not established by the sources reviewed. We can propagate hypothetical orbit samples, but those are conditional model predictions, not measurements of a confirmed object. Existing tools already handle detailed ephemerides, survey selection and moving-source image searches. The useful prototype direction chosen here is a transparent audit of coverage, dependence and sensitivity to alternative model weights. It remains a proposed engineering contribution; neither novelty nor scientific impact has been established.

## Options considered

| Option | Existing support | Decision |
|---|---|---|
| Display a current Planet Nine pinpoint | No confirmed orbit in the reviewed primary sources | Reject: false precision |
| Rebuild survey simulator or image search | Sorcha, KBMOD, and Planet Nein already address these | Reuse upstream methods, do not duplicate |
| Audit coverage across models and overlapping searches | Standard probability bounds plus explicit scientific inputs | Build a small transparent kernel; validate before real use |
| Confirm infrared candidates | Requires new observations and orbit linkage | Outside this software-only prototype |

## Evidence and disagreements

### Historical reference population

CaltechDATA's Version 3.0 contains 100,000 synthetic orbital/physical samples drawn from Brown and Batygin (2021), plus ZTF, DES and Pan-STARRS search flags. The live CSV header specifies an epoch of JD 2458270.0 (1 June 2018) and J2000 heliocentric osculating elements. Its RA/Dec are **at that epoch**, not the current date. The record is dated 5 April 2023 and lists CC0 rights. This is a historical model, not a 2026 posterior and not a detection catalog.

Record: https://data.caltech.edu/records/8fjad-x7y61

CSV inspected directly (first lines and count): https://data.caltech.edu/records/8fjad-x7y61/files/reference_population.csv?download=1

README inspected directly: https://data.caltech.edu/records/8fjad-x7y61/files/README.TXT?download=1

The orbit analysis is Brown and Batygin (2021): https://arxiv.org/html/2108.09868 . These sources provide a model-conditioned basis for simulations, not evidence that any sampled object exists.

### 2026 clustering reassessment

Siraj, Chyba and Tremaine, *Measuring Apsidal Clustering*, published 15 May 2026, introduce a conditional-likelihood approach. For their expanded sample of 25 objects, they report a drop in clustering significance from 2.7 sigma to 1.9 sigma and a poorly constrained clustering direction. They argue previously used sky probability distributions are too narrow. The footprint-insensitivity claim has stated population-model and solution-symmetry assumptions; it is not proof that all selection biases disappear or that Planet Nine is ruled out.

https://iopscience.iop.org/article/10.3847/1538-4357/ae6586

### Targeted parallax search

The version of *A targeted, parallax-based search for Planet Nine* reviewed here searches about 98 square degrees and reports no credible candidates within its field and magnitude limits, with 85% confidence exclusion limits around Sloan r=21.0-21.4. Its field selection relies on a debated scenario. This is a local, sensitivity-limited null, not an all-sky exclusion. It demonstrates that parallax-based search methods already exist and that single-exposure depth alone is not a discovery function.

https://arxiv.org/html/2504.05473

### Infrared candidate claims are not confirmed orbits

Phan et al. (2025), *A Search for Planet Nine with IRAS and AKARI Data*, identify one candidate pair after selection and inspection. The paper explicitly says two survey positions do not determine the full orbit and calls for follow-up; an AKARI flux measurement may be unreliable. We do not extrapolate a unique 2026 location from this pair.

https://arxiv.org/html/2504.17288v1

*A Far-Infrared Search for Planet Nine Using AKARI All-Sky Survey* (2025) reports two possible candidates requiring follow-up. These are not two confirmed planets and do not settle the Planet Nine hypothesis.

https://arxiv.org/html/2506.12854

A dated October 2026 BBC Sky at Night article still discusses the earlier IRAS/AKARI candidate and the inadequacy of two positions. This secondary source was used only to cross-check the recent media context, not as new scientific confirmation:

https://www.skyatnightmagazine.com/news/planet-9-iras-akari-survey-evidence

The disagreement between dynamical-model predictions and weaker clustering evidence is preserved, not averaged into one precise map. This prototype does not fit a new joint posterior or claim to resolve the debate.

## Existing software and reuse

- **Sorcha** forward-models survey selection for an input synthetic population, including ephemerides, apparent brightness and discovery selection. Its documented constraints include cadence, pointing, magnitude, motion and software efficiencies. It uses ASSIST/REBOUND and supports external ephemerides. https://sorcha.readthedocs.io/en/stable/overview.html ; https://github.com/dirac-institute/sorcha
- **KBMOD** searches astronomical images for moving sources using maximum-likelihood methods and GPU tooling. Our CSV arithmetic is not an alternative to this image processing. https://github.com/DiracInstitute/kbmod
- **Planet Nein** explicitly combines Planet Nine reference populations, LSST pointing data and Sorcha. This is a direct overlap with the original broad idea, so a generic orbit/survey tracker would not be presented as new. https://github.com/ASTR302-Group-A/planet-nein

## Limits and what could change the recommendation

No live Rubin survey schedule, full calibrated search mask, new follow-up observation or new posterior was imported. No discovery odds or telescope-ready target coordinates are produced. We do not merge infrared candidates into the dynamical population. New confirmed astrometry and an accepted orbit would permit real ephemerides; new well-characterized survey selection and alternative ensembles would enable real coverage audits. Scientific review is still needed before claiming usefulness to researchers.

The current mathematical machinery is established probability theory, not a new scientific detection method: https://en.wikipedia.org/wiki/Fr%C3%A9chet_inequalities .

## Executed real-data check

The complete published v3 CSV was downloaded, its MD5 matched the record's `a38fa7579b4c9938b3deebecda55a845`, and all 100,000 rows were checked. The union of published ZTF/DES/PS1 binary detectability flags contains 78,260 particles; 21,740 have no positive flag. An independent Python set-union calculation reproduced that count. This **78.26% model fraction is not a confidence level**, is not a new exclusion result, and is not current 2026 sky coverage. The joint flag table and checksums are in `examples/caltech-v3-summary.json`. No current position was inferred.


## 27 October 2026 additions: live evidence map sources

- Siraj, Chyba & Tremaine 2026 full text (method Eqs. 6-22, sample Section V,
  Table 1 anchors): https://arxiv.org/html/2604.25990 and
  https://iopscience.iop.org/article/10.3847/1538-4357/ae6586
- Siraj, Chyba & Tremaine 2025 sample table (51 objects with elements;
  asterisks mark the 11 BB21 objects): https://arxiv.org/html/2410.18170v2
- Per-object elements: JPL SBDB API (orbit solution ids and dates recorded in
  data/sct26-sample.json). Detection geometry: JPL Horizons API, retrieved
  2026-10-27.
- Phan et al. 2025 IRAS/AKARI candidate pair (Table 2 coordinates;
  authors: two positions do not determine an orbit, follow-up required):
  https://arxiv.org/html/2504.17288v1
- AKARI far-infrared search 2025 (two candidates, Table 2 coordinates;
  unconfirmed, transient events not excluded):
  https://arxiv.org/html/2506.12854
- MPC census snapshot: https://www.minorplanetcenter.net/iau/MPCORB/Distant.txt

No public post-2021 Planet Nine orbit ensemble was found in this review; the
claim is bounded to sources checked here, not a universal negative.

## Cross-evidence test 2026-10-27: published IR candidates vs the BB21 ensemble at their observation epochs

Question (user-asked): do the published far-infrared candidate positions survive comparison against the published Planet Nine model ensemble, evaluated at the candidates' own observation epochs?

Method: propagated all 100,000 CaltechDATA v3 reference samples (epoch 2018-06-01) back to each candidate's observation epoch with the repo's validated two-body propagator, then computed the minimum angular separation from each candidate position to (a) the 21,740 samples not flagged by published ZTF/DES/PS1 searches and (b) the 78,260 flagged samples. For the Phan et al. (2025) IRAS/AKARI pair we additionally computed the best JOINT match: the single sample minimizing the RSS of its 1983 and 2006/07 separations (a two-epoch linkage test).

Results:
| Candidate | Epoch used | Min sep to unexcluded | Min sep to excluded |
|---|---|---|---|
| IRAS F02211-4844 | 1983-07-15 | 21.3 deg | 15.4 deg |
| AKARI-MUSL J0220440-491247 | 2007-01-01 | 21.7 deg | 16.3 deg |
| IRAS+AKARI best single-sample joint | both | RSS 30.4 deg (21.3 + 21.7) | RSS 22.5 deg |
| FISSSDL J0250422-150114 | 2007-07-28 | 2.1 deg | 1.3 deg |
| FISSSDL J0301112-164240 | 2006-07-30 | 4.4 deg | 1.3 deg |

Reading: the Phan et al. IRAS/AKARI pair lies ~21 deg outside the entire BB21 model sky region at both epochs; no ensemble sample, excluded or not, comes near either position. Under the BB21 orbit family specifically, the pair is not a model-consistent Planet Nine. Phan et al. selected the pair by separation (42-69.6 arcmin, implying 500-700 AU) and did not publish a comparison against the BB21 sky region, so this quantification appears new, though the direction of the conclusion matches the paper's own caution. The two FISSSDL (AKARI 2025) positions sit 1.3-4.4 deg from the model band edge, geometrically consistent with the BB21 family at this coarse level - consistency, not support.

Limits: (1) tests consistency with ONE published model; BB21 is not the 2026 evidence state (SCT26 weakens clustering to ~1.9 sigma over about half the sky, and no newer public ensemble was found in our review), so "inconsistent with BB21" is not "not Planet Nine". (2) Two-body propagation 35 years back from 2018: measured drift vs JPL n-body over 8.4 years is 71-111 arcsec; even linearly extrapolated (~0.1-0.3 deg) it is negligible against a 21 deg margin. (3) Candidate positional uncertainties (arcmin scale) and the IRAS 3-month observation window are likewise negligible. (4) The IRAS/AKARI linkage itself is unconfirmed by its authors. (5) Reproducibility: script and exact epochs are in tests/fixtures/ and this repo's history; inputs are the published CSV (MD5-verified) and published candidate coordinates.

Next cross-evidence test identified: cross-match the candidate positions/epochs against the known moving-object catalog (MPC MPChecker). Scripted CGI access is explicitly unsupported by MPC and JPL exposes no position-at-epoch identification API here, so this needs the browser-driven form; queued in TODO.md.
