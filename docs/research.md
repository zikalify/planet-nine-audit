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

Method: propagated all 100,000 CaltechDATA v3 reference samples (epoch 2018-06-01) back to each candidate's observation epoch with the repo's validated two-body propagator, then computed distances from each candidate position to the nearest sampled orbits. For the Phan et al. (2025) IRAS/AKARI pair we additionally computed the best JOINT match: the single sample minimizing the RSS of its 1983 and 2006/07 separations (a two-epoch linkage test). Candidate coordinates were independently re-verified against the source papers for this test: Phan et al. Table 2 (35.74075, -48.5125; 35.18379, -49.2135; equinox not stated, J2000 assumed - a wrong-equinox error would be ~1 deg at most, negligible here) and the AKARI paper Table 2 (42.676, -15.021, epoch 2007/07/28; 45.297, -16.711, epoch 2006/07/30; explicitly J2000, position error ellipses 3.5 x 2.3 arcsec).

Finite-sample calibration: to interpret "no sample near a position" we measured the ensemble's own sky nearest-neighbor spacing at each epoch: median 0.19-0.20 deg, p95 0.81 deg, worst-case fringe gap ~8 deg. A candidate farther from every sample than the ensemble's own largest internal gap is outside the SAMPLED support; the underlying continuous posterior density there cannot be bounded from the sample alone.

Results (k-th nearest sampled orbit, unexcluded set):
| Candidate | Epoch used | 1st | 5th | 20th |
|---|---|---|---|---|
| IRAS F02211-4844 | 1983-07-15 | 21.3 deg | 26.1 deg | 30.2 deg |
| AKARI-MUSL J0220440-491247 | 2007-01-01 | 21.7 deg | 26.3 deg | 29.9 deg |
| FISSSDL J0250422-150114 | 2007-07-28 | 2.1 deg | 5.1 deg | 8.4 deg |
| FISSSDL J0301112-164240 | 2006-07-30 | 4.4 deg | 7.8 deg | 9.7 deg |

Best single-sample joint match for the IRAS/AKARI pair: RSS 30.4 deg (21.3 + 21.7 deg; nearest sampled orbit at ~1008 AU). For the excluded set: RSS 22.5 deg.

Reading, stated carefully:
- The Phan et al. pair lies far outside the sky region populated by the supplied ensemble: its nearest sampled orbit is ~100x the ensemble's median spacing and ~3x its worst fringe gap, at both epochs. So within the published v3 sample, no BB21-family orbit comes near the pair. This is a statement about the finite published sample, not a formal bound on the continuous BB21 posterior, and not evidence the candidate is physically false - Phan et al. selected the pair by angular separation (implying 500-700 AU) and did not claim BB21 sky-region consistency. We found no published quantification of the pair against the v3 ensemble sky map in our bounded literature check; we do not assert none exists.
- The FISSSDL candidates' nearest sampled orbits (2.1 deg, 4.4 deg) are comparable to the ensemble's own largest fringe gaps (~8 deg). They sit at or just beyond the sparsely sampled fringe. That is geometric proximity, not calibrated consistency; no density/support threshold is established here.
- Margins for the pair are robust to all quantified error sources: two-body propagation drift over 35 yr (~0.1-0.3 deg worst case), arcsec-to-arcmin positional errors, observation windows of months.

Limits: (1) one published model only; BB21 is not the 2026 evidence state (SCT26 weakens clustering to ~1.9 sigma over about half the sky; no newer public ensemble found in our review). (2) Finite-sample statements only, calibrated as above. (3) The IRAS/AKARI linkage itself is unconfirmed by its authors. (4) Reproducibility: inputs are the published CSV (MD5-verified) and the paper coordinates above; code in this repo's history.

Next cross-evidence test identified: cross-match the candidate positions/epochs against the known moving-object catalog (MPC MPChecker). Scripted CGI access is explicitly unsupported by MPC and JPL exposes no position-at-epoch identification API here, so this needs the browser-driven form; queued in TODO.md.

## Numerical sensitivity check 2026-10-27: CL statistic vs detection-geometry inputs

Question: how much does the SCT26 conditional-likelihood statistic change when its detection-geometry inputs are perturbed along each object's orbit?

2026-10-27: the diary's earlier presentation of these shifted values as a stress test of the published result was withdrawn; this section is the dated record of what changed and why.

Scope audit (done before interpretation): the paper's method conditions on the MEASURED (lambda, r, a, e) at detection - the position where a survey actually detected each object (arXiv:2604.25990, Sec. II-III). Only the discovery-era geometry corresponds to a real detection process under that definition. Arc-midpoint and last-observation positions are synthetic inputs: no survey detected these objects there. The variants below are therefore numerical sensitivity probes, NOT validated alternative analyses, and their shifted values say nothing direct about the correctness of the published 1.9 sigma, which used the appropriate inputs.

Method: for all 25 sample objects we fetched full-precision JPL SBDB orbit solutions (data/sct26-elements-full.json, retrieved 2026-10-27, with first_obs/last_obs arc dates) and rebuilt detection geometry under three input choices - first observation (baseline, matching the paper), arc midpoint, last observation - using the repo's two-body propagator. Sanity: propagated vs Horizons geometry at first_obs agrees to median 63", max 218" (rounding/drift scale, docs/validation.md). Median observation-arc length is 11.6 yr (max 35.4 yr); the input perturbation itself is large: median 10.7 deg, max 38.6 deg of along-track motion between first and last observation. Frame check: heliocentric vs barycentric placement is bounded by the Sun-SSB offset, verified via Horizons at 0.0049 AU on 2007-07-15; worst-case angular effect ~0.007 deg - negligible.

Results (significance Z / direction; midpoint and last-obs columns are synthetic-input probes only):
| Sample | Method | first_obs (baseline) | arc midpoint* | last_obs* | Published |
|---|---|---|---|---|---|
| BB21 | Simple | 2.52/58 | 2.52/58 | 2.52/58 | 2.5/58 |
| SCT25 | Simple | 2.78/67 | 2.78/67 | 2.78/67 | 2.8/67 |
| SCT26 | Simple | 1.65/58 | 1.65/58 | 1.65/58 | 1.6/58 |
| BB21 | 2D CL | 2.17/41 | 2.02/39 | 2.08/35 | 2.2/41 |
| SCT25 | 2D CL | 2.72/126 | 2.35/132 | 1.86/134 | 2.7/126 |
| SCT26 | 2D CL | 1.74/143 | 1.47/155 | 1.10/164 | 1.7/143 |
| BB21 | 3D CL | 2.40/43 | 2.09/41 | 2.09/35 | 2.4/43 |
| SCT25 | 3D CL | 2.74/125 | 2.40/134 | 2.01/140 | 2.7/125 |
| SCT26 | 3D CL | 1.92/150 | 1.70/165 | 1.43/178 | 1.9/151 |

Reading: Simple statistics are exactly invariant (they use only orbital elements). Measured changes under the synthetic perturbations (median 10.7 deg along-track, max 38.6 deg): SCT26 3D 1.92 -> 1.43 sigma and direction 150 -> 178 deg; SCT26 2D 1.74 -> 1.10 sigma; SCT25 3D 2.74 -> 2.01 sigma; BB21 3D 2.40 -> 2.09 sigma. We report only these measured input and output changes. The perturbed runs are not comparable to the published analysis (different, synthetic inputs), so no conclusion about the published significance follows in either direction, and no positional-tolerance or error-budget claim is made: the two probe points do not establish a response curve.

Limits: variants use propagated geometry from current orbit solutions (two-body), not actual astrometry; SBDB solutions evolve over time; this is a numerical sensitivity measurement by this project, not peer reviewed. Code: p9audit/robustness.py. Data: data/sct26-sample.json, data/sct26-elements-full.json.

## Replication 2026-10-27: profiled 1-sigma direction interval (SCT26 Sec. VI method)

Measurement only. The paper constructs direction uncertainties by profiling the conditional log-likelihood over the preferred-direction ecliptic longitude, maximizing over latitude and kappa, and taking the envelope where the drop from the global maximum is 0.5. We implemented the same procedure (p9audit/clustering.py profile3d_direction, 0.5-deg longitude grid, 1-deg latitude grid, kappa step 0.05) on our reconstructed sample.

Result vs published (SCT26, 3D method): ours 149.0 deg (+35.0/-58.5); published 151 deg (+34/-59). Within the same tolerances as our anchor reproductions. BB21 and SCT25 intervals also computed (42.5 +33.0/-15.5; 124.5 +29.0/-37.5); the paper's Table 1 interval anchor available to us is the SCT26 one. Regression test added (tests/test_clustering.py ProfileIntervalTest). This is a replication of a published uncertainty calculation, not a new inference. The direction in question is the fitted clustering direction of the TNO orbits' perihelion longitudes; it is not, and cannot be read as, a sky position of any planet.
