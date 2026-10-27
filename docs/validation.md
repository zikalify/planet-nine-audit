# Validation record

Executed locally on 27 October 2026, Python 3.10:

- 26 automated tests passed (`python3 -m unittest discover -s tests -v`).
- Synthetic example output exactly reproduced byte-for-byte.
- Full Caltech v3 reference population downloaded from its record's own CSV link.
- Source MD5 verified against the live published record.
- 100,000 source rows parsed with binary flag and uniqueness checks.
- JSON summary reproduced exactly on a second run.
- Independent set-union implementation matched the 78,260-particle published-flag union.
- No source population redistributed, no credential included, no network actions in library runtime.

Not validated: new selection functions, real follow-up rankings, orbit predictions, scientific novelty, telescope usability, statistical calibration of any new astronomical inference. Unit tests do not certify these.

## Interactive site

- Node assertions passed for union counts, model intervals and follow-up ordering.
- Real Chrome tests passed for dependence toggles, reset, published survey toggles and JSON download.
- No browser console exceptions occurred.
- No horizontal overflow at 320px and 390px viewport widths.
- Desktop and full mobile screenshots inspected; text, controls, range bars, caveats, source links and source/demo separation checked.
- Live GitHub Pages deployment is a separate check, not established by local rendering.


## Live-map validation (27 October 2026, continued)

- Epoch reproduction: all 100,000 rows; geocentric RA/Dec from published
  elements vs the dataset's published RA/Dec: median 53 arcsec, p99 216
  arcsec. Monte Carlo over the published element precision (two decimals)
  gives median 55 arcsec, p99 214 arcsec: the residual is explained by input
  rounding. Fixture rows in tests/fixtures/v3-epoch-check.csv are real
  published rows; test tolerance 0.06 deg.
- Independent n-body comparison: JPL Horizons geometric state vectors
  (DE441, ICRF/J2000 ecliptic) for (90377) Sedna and 2013 SY99 at
  2018-06-01 and 2026-10-27. Elements from the 2018 vectors propagated
  two-body to 2026-10-27 differ from the Horizons n-body positions by 71
  arcsec (Sedna) and 111 arcsec (2013 SY99), i.e. <=0.031 deg over 8.4 years.
- Clustering anchors: all nine published cells of Siraj, Chyba & Tremaine
  2026 Table 1 reproduced (3 methods x 3 samples, significance and
  direction). Maximum deviation 0.05 sigma and 2 deg, attributed to
  element-solution epoch and detection-date conventions (docs/method.md).
  tests/test_clustering.py enforces +-0.15 sigma, +-3 deg.
- Site math: node assertions reproduce real published rows, projection
  geometry, and the galactic rotation (galactic centre at 266.4, -29.0).
- Full suite: 31 Python tests + node assertions pass.

Not validated: marginalized direction intervals; sensitivity to
detection-epoch conventions; any new scientific claim. The map is a
model-conditional visualization of published results, not a measurement.
