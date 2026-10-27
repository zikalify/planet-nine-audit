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
