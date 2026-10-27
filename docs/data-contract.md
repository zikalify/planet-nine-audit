# Input contract

The CLI accepts a directory with four files, all UTF-8. CSV columns must appear in the exact order below. Each supplied model must have positive finite weights and unique particle IDs within that model. Models need not share the same particles.

## particles.csv

`model,particle,weight`

The model is a named hypothesis/ensemble. Weight is an unnormalized positive mass. Supply a correctly weighted ensemble from an external source, not a hand-picked set of best-looking orbits. Distinguish prior samples, posterior samples and already search-filtered samples. Do not apply published exclusions twice.

## searches.csv

`search,dependence_group,source`

`source` is required provenance. A search is a whole discovery process, not a visit. Give searches the same dependence group whenever conditional independence is not justified: shared images, shared masks or linkage/calibration failures are examples. A single common group is conservative and needs no independence between the searches inside it.

## detections.csv

`model,particle,search,p_detect`

A **complete** particle-by-search matrix is required, including explicit zero probabilities. This prevents accidentally treating missing calibration as a surveyed non-detection. Each probability must be finite in [0,1]. Duplicates, unknown keys and missing rows fail. Zeros must mean established zero detectability within the supplied model, not unknown coverage.

One binary realization of a survey simulator is generally not an estimate of a probability. Use repeated calibrated realizations/injection recovery or a justified analytic model. Include uncertainty in separate scenarios; this version does not infer efficiency uncertainty.

## metadata.json

Required fields:

- `label`: descriptive dataset label.
- `synthetic`: JSON true/false, not a string.
- `coordinate_epoch`: epoch/time-scale/frame of the upstream calculations, or an explicit reason not applicable.
- `probability_definition`: what counts as an accepted detection, including the relevant time span and selection.
- `independent_groups_assumption`: explicit explanation for any between-group independence.
- `model_sources`: object mapping every model name to source/version and upstream assumptions.

Record bandpasses, brightness/albedo models, observing epochs, simulator version, selection configuration, known survey overlap and generation seed in additional metadata. The output copies metadata and hashes all four inputs. It does not independently verify that the supplied scientific provenance is true.

No automatic Sorcha adapter is claimed. Sorcha output describes simulated detections and discovery selection; constructing a calibrated survey-level probability matrix remains a validation step.
