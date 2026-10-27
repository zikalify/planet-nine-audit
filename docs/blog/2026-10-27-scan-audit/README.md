# Scan-level audit of IRAS F02211-4844 (Phan et al. 2025 candidate)

Research files accompanying the 27 October 2026 research-diary post
"Audit log: re-checking the raw IRAS scans behind one reported Planet Nine candidate".

## Layout
- `code/` - runnable analysis pipeline (Python 3, numpy only). `c1_fits.py` regenerates
  the per-crossing fit table from the raw SCANPI products in `data/profiles/`.
- `data/profiles/` - raw SCANPI source-fit scan products (60 micron, band 3) for the
  12 default crossings at the catalog position (35.74075, -48.5125 J2000).
- `data/wide/` - the 20 wide-window crossings.
- `data/disp/` - SCANPI query products at 10 displaced positions (the late-epoch
  parallax test). `data/disp_coverage.json` maps positions to covering crossings.
- `data/*.json`, `data/*.csv`, `data/*.txt` - intermediate and final tables
  (fit results, field nulls, injection recovery, Horizons ephemeris excerpts).
- `historical/` - earlier scripts kept for provenance only; superseded by `code/`.
- `live-excerpts/` - archived copies of the public SCANPI documentation pages used
  (IRSA), captured 27 October 2026.

## Caveats
- All scan data are from IRSA's SCANPI service (IRAS mission archives).
- `data/per_scan_audit_table.csv` is an earlier provenance table; its formal
  uncertainty column (sA) is known to disagree with the regenerated fits in
  `code/c1_fits.py` output (`data/c1_b3_fits.json`). Do not quote significance
  values from it; the disagreement is unresolved.
- Formal fit uncertainties are white-noise approximations; scan noise is strongly
  correlated (lag-1 autocorrelation 0.96-0.99), so only the empirical null
  measurements in `data/` are defensible scatter estimates.
- Not peer reviewed.
