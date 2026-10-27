# Project checklist

Maintained as work proceeds. Items are checked only when verified; dates are UTC.

## Evidence and data pipelines
- [x] Survey current research and existing tools (Sorcha, KBMOD, Planet Nein, published searches) — 2026-10-27
- [x] Verify the real ensemble exists and is intact (CaltechDATA v3, 100,000 rows, MD5 matches record) — 2026-10-27
- [x] Reproduce published joint-exclusion count (78,260 of 100,000 flagged by ZTF/DES/PS1) — 2026-10-27
- [x] Validate 2018→today propagation against the dataset's own published positions (rounding-limited, median ~53″) — 2026-10-27
- [x] Quantify two-body drift vs full JPL n-body on real Sedna-class orbits over 2018–2026 (71″ Sedna; 111″ 2013 SY99) — 2026-10-27
- [x] Reconstruct the SCT26 clustering sample (25 objects) from published sources with per-object provenance — 2026-10-27
- [x] Implement and validate Simple / 2D / 3D conditional-likelihood clustering statistics against all 9 published anchors (≤0.05σ, ≤2°) — 2026-10-27
- [x] Extract published infrared candidate positions (Phan 2025 pair; two AKARI 2025 candidates) with the papers' own caveats — 2026-10-27

## Live evidence map
- [x] Client-side current-date propagation of the unexcluded population — 2026-10-27
- [x] Excluded-region overlay from published flags — 2026-10-27
- [x] Candidate markers with source notes — 2026-10-27
- [x] Clustering evidence panel with ours-vs-published table — 2026-10-27
- [x] MPC census tracker with stability-classification caveat — 2026-10-27
- [x] Browser visual checks (desktop + mobile, live deployment) — 2026-10-27
- [x] Replace the toy synthetic demo on the public site with this map — 2026-10-27

## Open research leads (not started or not validated)
- [x] Detection-epoch sensitivity of CL statistics: SCT26 3D 1.92->1.43 sigma, 2D 1.74->1.10 sigma across first/mid/last-obs conventions; direction swings ~28 deg; frame effect ~0.007 deg negligible (docs/research.md) — 2026-10-27
- [ ] Marginalized direction uncertainties matching the paper's 151°(+34/−59) (we report ML direction; intervals not yet reproduced)
- [x] Two-epoch candidate-vs-ensemble test, finite-sample calibrated (IRAS/AKARI pair: nearest sampled orbit 21 deg away at both epochs, far outside sampled support; FISSSDL: fringe-proximity only; see docs/research.md) — 2026-10-27
- [ ] Parallax-search null field (arXiv:2504.05473) overlap check against candidate positions
- [ ] Cross-match published candidates against the current MPC known-object catalog with documented method
- [ ] Re-run the census/clustering tracker when Rubin publishes new distant TNOs with stability classifications
- [ ] Calibrated survey selection functions (Sorcha-scale) — currently infeasible in this compute environment; would need to reproduce a published search's exclusions first
- [ ] Independent scientific review — only if the owner authorizes outreach
