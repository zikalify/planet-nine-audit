"""Build the real-data site payloads for the live Planet Nine evidence map.

Inputs are published, verifiable sources only:
- CaltechDATA v3 reference population (MD5-checked against the record)
- data/sct26-sample.json (reconstructed SCT26 sample with provenance)
- MPC Distant.txt census snapshot (selection-criteria tracker)

No probabilities or observations are invented. See docs/method.md.
"""

import argparse
import datetime as _dt
import hashlib
import io
import json
import urllib.request

import numpy as np
import pandas as pd

from . import clustering, propagate

CALTECH_MD5 = "a38fa7579b4c9938b3deebecda55a845"
CALTECH_URL = "https://data.caltech.edu/records/8fjad-x7y61/files/reference_population.csv?download=1"
MPC_DISTANT_URL = "https://www.minorplanetcenter.net/iau/MPCORB/Distant.txt"

CANDIDATES = [
    {"name": "IRAS F02211-4844 (1983)", "ra": 35.74075, "dec": -48.5125,
     "epoch": "1983 Jun-Sep", "kind": "candidate",
     "source": "Phan et al. 2025, arXiv:2504.17288, Table 2",
     "note": "IRAS position of the single IRAS-AKARI candidate pair; source absent at this position in AKARI 23 years later. Authors state two survey positions do not determine an orbit; follow-up required. One AKARI band flux may be unreliable."},
    {"name": "AKARI-MUSL J0220440-491247 (2006/07)", "ra": 35.18379, "dec": -49.2135,
     "epoch": "2006-2007", "kind": "candidate",
     "source": "Phan et al. 2025, arXiv:2504.17288, Table 2",
     "note": "AKARI position of the same candidate pair, ~40 arcmin from the IRAS position 23 years earlier (consistent with orbital motion at several hundred AU, per the authors). Unconfirmed; follow-up required."},
    {"name": "FISSSDL J0250422-150114", "ra": 42.676, "dec": -15.021,
     "epoch": "2007-07-28", "kind": "candidate",
     "source": "AKARI far-infrared search 2025, arXiv:2506.12854, Table 2",
     "note": "Detected twice within 24 hours, not re-detected after six months. Fluxes vary between detections; physical properties unconstrained. Unconfirmed; could be a transient event."},
    {"name": "FISSSDL J0301112-164240", "ra": 45.297, "dec": -16.711,
     "epoch": "2006-07-30", "kind": "candidate",
     "source": "AKARI far-infrared search 2025, arXiv:2506.12854, Table 2",
     "note": "Same selection as the other AKARI candidate. The paper could not pair any candidates via expected Planet Nine parallax. Unconfirmed."},
]


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "p9audit-build/1.0"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def load_population(csv_path=None):
    if csv_path:
        raw = open(csv_path, "rb").read()
    else:
        raw = fetch(CALTECH_URL)
    md5 = hashlib.md5(raw).hexdigest()
    if md5 != CALTECH_MD5:
        raise SystemExit(f"MD5 mismatch for reference population: {md5} != {CALTECH_MD5}")
    p9 = pd.read_csv(io.BytesIO(raw), comment="#")
    p9.columns = [c.strip() for c in p9.columns]
    if len(p9) != 100000:
        raise SystemExit(f"expected 100000 rows, got {len(p9)}")
    return p9, md5


def mpc_census():
    raw = fetch(MPC_DISTANT_URL, timeout=60).decode("utf-8", "replace")
    n_census = 0
    for line in raw.splitlines():
        f = line.split()
        if len(f) < 12:
            continue
        try:
            a = float(f[10]); e = float(f[8]); u = int(f[11])
        except ValueError:
            continue
        q = a * (1 - e)
        if 90 < a < 1000 and q > 30 and u < 7:
            n_census += 1
    return n_census


def build(csv_path=None, mpc=True, build_jd=None):
    p9, md5 = load_population(csv_path)
    if build_jd is None:
        now = _dt.datetime.now(_dt.timezone.utc)
        build_jd = 2451545.0 + (now - _dt.datetime(2000, 1, 1, 12, tzinfo=_dt.timezone.utc)).total_seconds() / 86400.0

    excluded = p9[(p9.ZTF == 1) | (p9.DES == 1) | (p9.PS1 == 1)]
    unexcluded = p9[(p9.ZTF == 0) & (p9.DES == 0) & (p9.PS1 == 0)]
    if len(unexcluded) != 21740 or len(excluded) != 78260:
        raise SystemExit("published flag union changed: data integrity problem")

    # Packed unexcluded elements for client-side live propagation.
    pack = {
        "a": [round(v, 2) for v in unexcluded.a],
        "e": [round(v, 4) for v in unexcluded.e],
        "inc": [round(v, 2) for v in unexcluded.inc],
        "varpi": [round(v, 2) for v in unexcluded.varpi],
        "Omega": [round(v, 2) for v in unexcluded.Omega],
        "M": [round(v, 2) for v in unexcluded.M],
        "V": [round(v, 1) for v in unexcluded.V],
    }

    # Excluded-region density grid at build date (1 deg cells), labelled with build date.
    ra_e, dec_e, _ = propagate.geo_radec(excluded.a.values, excluded.e.values, excluded.inc.values,
                                         excluded.varpi.values, excluded.Omega.values, excluded.M.values,
                                         propagate.EPOCH_V3, build_jd)
    H, _, _ = np.histogram2d(np.floor(dec_e + 90).astype(int), np.floor(ra_e).astype(int),
                             bins=[180, 360], range=[[0, 180], [0, 360]])
    excluded_grid = H.astype(int).tolist()


    sample_doc = json.load(open("data/sct26-sample.json"))
    sample_list = [
        {"name": o["name"], "membership": o["membership"],
         "a": o["elements"]["a"], "e": o["elements"]["e"], "inc": o["elements"]["inc"],
         "varpi": o["elements"]["varpi"], "Omega": o["elements"]["Omega"],
         "first_obs": o["detection"]["first_obs"], "r_au": o["detection"]["r_au"],
         "soln_date": o["elements"]["soln_date"]}
        for o in sample_doc["objects"]
    ]
    cl = clustering.run_all("data/sct26-sample.json")
    cl_comp = clustering.compare_to_anchors(cl)

    census = mpc_census() if mpc else None
    today = _dt.datetime.now(_dt.timezone.utc).date().isoformat()
    return {
        "meta": {
            "build_date_utc": today,
            "build_jd": build_jd,
            "model": "Brown & Batygin 2021 reference population (CaltechDATA v3), 100,000 samples",
            "model_epoch": "JD 2458270.0 (2018-06-01), J2000 heliocentric osculating elements",
            "record": "https://data.caltech.edu/records/8fjad-x7y61",
            "record_md5_verified": md5,
            "exclusions": "Published binary detectability flags for ZTF (Brown & Batygin 2022), DES (Belyakov et al. 2022), PS1 (Brown et al. 2024), applied exactly as published",
            "unexcluded_count": int(len(unexcluded)),
            "excluded_count": int(len(excluded)),
            "propagation": "Two-body Kepler from published elements + geocentric correction; validated in docs/validation.md (epoch reproduction limited by published element precision: median ~53 arcsec; 8.4-yr drift vs JPL n-body <= ~111 arcsec on Sedna-class orbits)",
            "candidates": "Published infrared candidate positions (unconfirmed); see per-marker notes",
            "mpc_distant_census_current": census,
            "mpc_distant_census_note": "Count of MPC distant objects meeting the SCT26 census filters (90<a<1000 AU, q>30 AU, U<7) as of build date. Objects without a published 4-Gyr stability classification cannot be added to the clustering sample; see docs/method.md.",
        },
        "unexcluded": pack,
        "excluded_grid_1deg": excluded_grid,
        "candidates": CANDIDATES,
        "sample": sample_list,
        "clustering": {"results": cl, "anchor_comparison": cl_comp,
                       "anchors_source": "Siraj, Chyba & Tremaine 2026 (ApJ 1003 76, arXiv:2604.25990), Table 1"},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="local reference_population.csv (else downloaded)")
    ap.add_argument("--no-mpc", action="store_true")
    ap.add_argument("--output", default="docs/site/live-data.json")
    args = ap.parse_args()
    out = build(args.csv, mpc=not args.no_mpc)
    with open(args.output, "w") as fh:
        json.dump(out, fh, separators=(",", ":"))
    print("wrote", args.output)


if __name__ == "__main__":
    main()
