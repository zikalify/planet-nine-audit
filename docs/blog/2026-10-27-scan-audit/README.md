# WITHDRAWN - fitting-method flaw (27 October 2026)

**The pipeline in this directory contains a fitting-method flaw: the scan-fit objective
(scipy-free matched-filter chi-squared in response_lib.refit, used by c1_fits.py and the
sensitivity/coverage scripts) compares chi-squared sums evaluated over different subsets
of each scan profile for different candidate positions, which biases the fits toward
zero-amplitude solutions at the window edge. All fit-based numerical outputs in this
bundle (work/*.json, per_scan_audit_table.csv amplitudes and uncertainties, and every
number derived from them) are INVALIDATED and must not be used or cited. The raw SCANPI
products (profiles/, wide/, disp/) are unaffected and remain valid archival data.**

The analysis is being rerun with a corrected fitter and will be republished only after an
independent review of the corrected method. This bundle is retained for provenance.

---

# Scan-level audit of IRAS F02211-4844 (Phan et al. 2025 candidate)

Research bundle accompanying the 27 October 2026 research-diary post
"Re-checking the raw IRAS scans behind one reported Planet Nine candidate".
Self-contained: every documented command runs from a clean checkout with no
environment variables (Python 3 + numpy only).

## Layout
- Pipeline scripts (this dir): p9paths.py (path config), response_lib.py, response.py,
  final_stats.py, sensitivity.py, sensitivity2.py, coverage.py, coverage2.py, geo.py,
  c1_fits.py, fig1_v3.py, fig2_v3.py
- historical/ - earlier analysis scripts, provenance only; NOT part of the runnable
  pipeline. Their products are superseded by the shipped intermediates.
- profiles/ - 12 default-run SCANPI srcfit tables at the catalog position (b3, 60 micron)
- wide/ - 20 wide re-run srcfit tables (det_distance=3.0, cross_scan=3.0)
- disp/ - 10 displaced-position query dirs (sep1_p1..p4, aug28_q1..q4, sep1_c, aug28_c),
  raw SCANPI output
- work/ - shipped intermediates: all_tight.json, sensitivity.json,
  sensitivity2_window.json, response_rows.json, disp_coverage.json, per_scan_fits.json,
  c1_b3_fits.json
- Templates b3_coadd_median.tbl / b4_coadd_median.tbl (coadd median profiles,
  peak-normalized, edge-subtracted), horizons.txt (JPL Horizons Earth vectors),
  displaced_points.txt (tested positions + workspace IDs), per_scan_audit_table.csv
- live-excerpts/ - archived copies of the public SCANPI documentation pages used,
  captured 27 October 2026

## Paths
p9paths.py sets the roots; defaults match this layout. Override with env vars:
P9WORK P9PROF P9WIDE P9DISP P9TEMPL. Regenerated intermediates go to work/.

## Reproduce
    python3 c1_fits.py        # per-crossing fits at the catalog position -> work/c1_b3_fits.json
    python3 geo.py            # geometry validation vs queried coordinates (max err 0.007 arcmin)
    python3 response.py       # cross-scan response controls             -> work/response_rows.json
    python3 final_stats.py    # tight-crossing nulls                     -> work/all_tight.json
    python3 sensitivity.py    # field null + injections                  -> work/sensitivity.json
    python3 sensitivity2.py   # actual-window null/injections            -> work/sensitivity2_window.json
    python3 coverage.py       # displaced-point coverage                 -> work/disp_coverage.json
    python3 coverage2.py      # grid-closure points
    python3 fig1_v3.py        # diagnostic figure (fixed-position profiles)
    python3 fig2_v3.py        # diagnostic figure (displaced-position nulls)

Regenerated JSONs reproduce the shipped work/ files byte-identically (verified from a
clean extract 27 October 2026 by a separate AI computational check; the fit-table
regeneration was additionally re-run byte-identical on the archived raw products).

## Data sources (all public archival)
- SCANPI program interface (IRSA): https://irsa.ipac.caltech.edu/cgi-bin/Scanpi/nph-scanpi
  - fixed-position query: locstr=35.74075 -48.5125, band3=60um&band4=100um, mode=PI
  - displaced-position queries (10 points, same parameters): coordinates + workspace IDs
    in displaced_points.txt
- JPL Horizons Earth heliocentric vectors: horizons.txt (query parameters in file header)
- SCANPI input parameter docs: https://irsa.ipac.caltech.edu/IRASdocs/scanpi_inputs.html
- SCANPI program interface docs: https://irsa.ipac.caltech.edu/applications/Scanpi/docs/ScanpiProgramInterface.html
- Paper: https://arxiv.org/abs/2504.17288 (Phan et al. 2025)

## Key empirical conventions
- Template: coadd median profile, peak-normalized, edge-subtracted
- Uncertainties: empirical null = MAD of matched-filter amplitude away from the source in
  the same profile (scan noise is 96-99% lag-1 correlated; formal white-noise errors invalid)
- Displaced-position predictions: JPL vectors, anchors at Jun 26 and Jul 20 1983,
  d=500/600/700 AU, orbital motion <=0.3 arcmin neglected (covered by grid spacing)

## Caveats
- per_scan_audit_table.csv is an earlier provenance table; its formal uncertainty column
  (sA) is known to disagree with the regenerated fits (c1_fits.py output). Do not quote
  significance values from it; the disagreement is unresolved.
- Remaining numbers are provisional. Not peer reviewed.
