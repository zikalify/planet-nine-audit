# Coverage calculation and assumptions

For each model, normalize positive particle weights to sum to one. Let `p_ij` be the survey-level probability of an accepted detection of particle i in search j. It is NOT merely the fraction of sky area visited, a single-exposure depth, or a raw simulator detection flag unless calibrated for this interpretation.

For searches in dependence group g, the unknown union probability obeys the standard Frechet/Boole bounds:

`L_ig = max_j p_ij`, `U_ig = min(1, sum_j p_ij)`.

If groups are conditionally independent given each particle, total detection bounds are

`L_i = 1 - product_g(1-L_ig)` and `U_i = 1 - product_g(1-U_ig)`.

Average each bound with model-specific normalized weights. With an observed null and a correct detection model, the null likelihood lies between `1-U` and `1-L`. **This is conditional on the model, not the probability that no planet exists.** We do not compute existence odds or reweight posteriors. That requires explicit model priors, alternative hypotheses and consistent selection accounting.

## Follow-up marginal gain

Subtracting the old lower bound from a new lower bound is NOT a valid lower bound on incremental coverage. Instead bound the probability that candidate C detects a particle while no selected search does.

For existing searches in C's dependence group, with probability sum S and maximum M, the extra probability within that group lies between `max(0,p_C-S)` and `min(p_C,1-M)`. Multiply these by the lower/upper miss bounds of all other independent groups, respectively. Average by model weights. Rank a single next search by the minimum lower gain across the supplied models, with an alphabetical tie break.

This conservative objective can produce zero gains and uninformative ties. That is useful evidence of missing dependence information, not a reason to invent precision. Bounds may be loose and rankings are not joint scheduling optimizations.

## Validation

Unit tests exercise exact independent cases, complete overlap, zeros/ones, invalid inputs, weight scaling, reproducibility and 100 seeded three-event joint distributions. For the joint-distribution tests, true union and true marginal gain are enumerated over all eight event outcomes and checked against bounds. Passing verifies arithmetic and some invariants, not astronomical calibration or scientific usefulness.

Standard probability reference: https://en.wikipedia.org/wiki/Fr%C3%A9chet_inequalities . The bounds are established mathematics, not a method invented by this project.


# Live map: propagation and conventions

The current-date positions are two-body (Kepler) propagations of the published
CaltechDATA v3 osculating elements (epoch JD 2458270.0, J2000 heliocentric),
with a geocentric correction using a low-precision Earth ephemeris (~0.01 deg).
Parallax at 150-1000 AU is at most ~0.4 deg, so the correction is included but
its own error is negligible. No aberration or light-time terms are applied;
their size at these distances is of order an arcsecond.

Accuracy budget, measured (docs/validation.md):
- Published elements carry two decimals. Re-deriving the dataset's own epoch
  RA/Dec from them has median ~53 arcsec error (p99 ~216 arcsec); a Monte
  Carlo of the element rounding alone reproduces this scatter, so the residual
  is input-precision limited, not a code error.
- Two-body drift versus full JPL Horizons n-body vectors over 2018-06-01 to
  2026-10-27: 71 arcsec for Sedna (a=481 AU), 111 arcsec for 2013 SY99
  (a=685 AU). Map cells are ~1 deg; the approximation is adequate.

# Clustering: conditional-likelihood implementation

Independent implementation of Siraj, Chyba & Tremaine (2026), Eqs. (6)-(22).
Per-object conditional likelihood uses the measured perihelion direction over
the two admissible directions fixed by the detection geometry; the von Mises /
von Mises-Fisher normalisers cancel object-by-object, and the null (kappa=0)
log-likelihood is -N ln 2. Significance Z = sqrt(2 delta log L); directions
are maximum-likelihood point estimates (marginalized intervals are a listed
open item in TODO.md).

Sample: data/sct26-sample.json, reconstructed from published sources with
per-object provenance. Conventions: current JPL SBDB heliocentric J2000
osculating elements (the paper used then-current JPL solutions and barycentric
a for cuts); detection geometry from JPL Horizons at the first observation in
the current orbit solution (may be a precovery). These convention differences
bound the agreement with the paper at <=0.05 sigma and <=2 deg on all nine
published anchors.

Tracker: new MPC objects meeting the census filters (90<a<1000 AU, q>30 AU,
U<7) are counted but NOT added to the clustering sample, because sample
membership requires a published 4-Gyr stability classification we cannot
recompute in this environment.
