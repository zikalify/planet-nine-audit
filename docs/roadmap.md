# Next steps before a scientific result

1. Obtain at least two independently justified orbit ensembles, with epoch, frame, weights and publication provenance. The Caltech v3 population is a useful historical baseline, not the 2026 state of evidence.
2. Generate survey-level accepted-discovery probabilities using repeated Sorcha simulations or injection/recovery. Validate cadence, motion, depth, masks, bandpass, linkage and false-positive rejection. Do not relabel a toy CSV as data.
3. Build a tested adapter and reproduce a published search's exclusions within its stated assumptions before adding novel searches. Keep published already-excluded particles and new efficiency factors distinct to avoid double counting.
4. Compare the bounds against full joint simulations, especially searches sharing images. If independence is unsupported, merge dependence groups or supply a future explicit joint-outcome model.
5. Add an optional epoch-aware ephemeris layer using established integrators, including observer position, parallax, light time and frame conventions. Validate against independent ephemerides. Never convert this to a measured Planet Nine position.
6. Only then add telescope-cost, visibility/weather constraints, and coordinate-safe visualization with probability mass clearly conditional on each model.
7. Seek scientific review when the owner authorizes outreach. No review, researcher endorsement or telescope deployment has occurred.

Possible value is better reproducibility and visible model sensitivity. We have not established uniqueness, discovery impact or publishable novelty. The current deliverable is a working audit kernel and a documented research direction.

## Update policy

Manual research snapshot checked 2026-10-27. No background monitoring was requested or started. For updates, record full publication/version/date and changed assumptions, regenerate upstream inputs, rerun tests, archive prior input hashes and compare ranks. Do not automatically turn abstracts or media headlines into hard exclusions.
