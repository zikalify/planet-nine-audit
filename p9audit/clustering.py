"""Apsidal-clustering statistics for distant TNOs.

Independent implementation of the conditional-likelihood method published by
Siraj, Chyba & Tremaine (2026, ApJ 1003 76, arXiv:2604.25990), applied to a
sample reconstructed from published sources (data/sct26-sample.json).

Method notes (see the paper for derivations):
- Simple: mean resultant length R of the longitudes of perihelion; Monte
  Carlo null preserving sample size (as in the paper's Section VI).
- 2D conditional likelihood: conditioning on (lambda, r, a, e) at detection
  leaves two admissible longitudes of perihelion, varpi = lambda -/+ phi with
  phi = arccos((a(1-e^2)/r - 1)/e). Per-object likelihood is
  f(varpi_obs) / (f(varpi+) + f(varpi-)) with f a von Mises(mu, kappa)
  distribution; the normalising Bessel factor cancels object-by-object.
- 3D conditional likelihood: the two admissible perihelion-direction unit
  vectors are the rotations of the observed position unit vector within the
  orbital plane by +/-phi about the orbital pole. f is a von Mises-Fisher
  distribution about a preferred direction k; the normaliser cancels
  object-by-object in the same way.
- Significance Z = sqrt(2 * (logL_ML - logL_null)); the null kappa=0 gives
  logL_null = -N ln 2 in both 2D and 3D.

Validated against every published anchor in the paper's Table 1; see
docs/validation.md and tests/test_clustering.py.
"""

import json
import math

import numpy as np
from scipy.stats import norm

ANCHORS = {  # Siraj, Chyba & Tremaine 2026, Table 1 (significance sigma, direction deg)
    "simple": {"BB21": (2.5, 58.0), "SCT25": (2.8, 67.0), "SCT26": (1.6, 58.0)},
    "cl2d":   {"BB21": (2.2, 41.0), "SCT25": (2.7, 126.0), "SCT26": (1.7, 143.0)},
    "cl3d":   {"BB21": (2.4, 43.0), "SCT25": (2.7, 125.0), "SCT26": (1.9, 151.0)},
}
NEW_IN_SCT26 = ("2017 OF201", "2021 RR205", "2023 KQ14", "2024 FX26")


def load_sample(path):
    with open(path) as fh:
        doc = json.load(fh)
    return doc["objects"]


def sample_subsets(objects):
    bb21 = [o for o in objects if o["membership"].startswith("BB21")]
    sct25 = [o for o in objects if "SCT25" in o["membership"]]
    return {"BB21": bb21, "SCT25": sct25, "SCT26": list(objects)}


def simple_stats(sample, trials=300000, seed=7):
    w = np.radians([o["elements"]["varpi"] for o in sample])
    n = len(w)
    C, S = np.cos(w).mean(), np.sin(w).mean()
    R = math.hypot(C, S)
    mu = math.degrees(math.atan2(S, C)) % 360.0
    csd = math.degrees(math.sqrt(-2 * math.log(R))) if R < 1 else 0.0
    rng = np.random.default_rng(seed)
    Rmc = np.abs(np.exp(1j * rng.uniform(0, 2 * np.pi, (trials, n))).mean(axis=1))
    p = max((Rmc > R).mean(), 0.5 / trials)
    return {"Z": float(norm.isf(p)), "direction_deg": float(mu), "circ_std_deg": float(csd),
            "R": float(R), "p_value": float(p)}


def _varpi_pm(obj):
    lam = obj["detection"]["ecl_lon"]
    phi = obj["phi_deg"]
    return math.radians((lam - phi) % 360.0), math.radians((lam + phi) % 360.0)


def cl2d(sample):
    obs = np.radians([o["elements"]["varpi"] for o in sample])
    adm = np.array([_varpi_pm(o) for o in sample])
    n = len(sample)

    def logL(mu, kap):
        num = kap * np.cos(obs - mu)
        den = np.logaddexp(kap * np.cos(adm[:, 0] - mu), kap * np.cos(adm[:, 1] - mu))
        return float((num - den).sum())

    best = (-np.inf, 0.0, 0.0)
    for mu in np.linspace(0, 2 * np.pi, 1440, endpoint=False):
        for kap in np.linspace(0, 6, 241):
            v = logL(mu, kap)
            if v > best[0]:
                best = (v, mu, kap)
    v, mu, kap = best
    for mu2 in np.linspace(mu - math.radians(1), mu + math.radians(1), 81):
        for kap2 in np.linspace(max(0.0, kap - 0.05), kap + 0.05, 41):
            v2 = logL(mu2, kap2)
            if v2 > v:
                v, mu, kap = v2, mu2, kap2
    dll = v - (-n * math.log(2))
    return {"Z": float(math.sqrt(max(0.0, 2 * dll))),
            "direction_deg": float(math.degrees(mu) % 360.0), "kappa": float(kap),
            "delta_logL": float(dll)}


def _cl3d_logL(sample):
    eobs, epm = [], []
    for o in sample:
        el, det = o["elements"], o["detection"]
        i = math.radians(el["inc"]); Om = math.radians(el["Omega"])
        w = math.radians((el["varpi"] - el["Omega"]) % 360.0)
        e_obs = np.array([
            math.cos(Om) * math.cos(w) - math.sin(Om) * math.sin(w) * math.cos(i),
            math.sin(Om) * math.cos(w) + math.cos(Om) * math.sin(w) * math.cos(i),
            math.sin(w) * math.sin(i)])
        lam = math.radians(det["ecl_lon"]); beta = math.radians(det["ecl_lat"])
        rh = np.array([math.cos(beta) * math.cos(lam), math.cos(beta) * math.sin(lam), math.sin(beta)])
        j = np.array([math.sin(i) * math.sin(Om), -math.sin(i) * math.cos(Om), math.cos(i)])
        u = np.cross(j, rh)
        phi = math.radians(o["phi_deg"])
        ep = math.cos(phi) * rh - math.sin(phi) * u
        em = math.cos(phi) * rh + math.sin(phi) * u
        eobs.append(e_obs)
        epm.append([ep / np.linalg.norm(ep), em / np.linalg.norm(em)])
    eobs = np.array(eobs); epm = np.array(epm)
    n = len(sample)

    def logL(K, kap):
        num = kap * (eobs @ K.T)
        d0 = kap * np.einsum("ni,mi->nm", epm[:, 0, :], K)
        d1 = kap * np.einsum("ni,mi->nm", epm[:, 1, :], K)
        return (num - np.logaddexp(d0, d1)).sum(axis=0)

    m = 2000
    kk = np.arange(m) + 0.5
    z = 1 - 2 * kk / m
    th = math.pi * (1 + 5 ** 0.5) * kk
    K = np.stack([np.sqrt(1 - z * z) * np.cos(th), np.sqrt(1 - z * z) * np.sin(th), z], axis=1)
    best = (-np.inf, None, 0.0)
    for kap in np.linspace(0, 6, 121):
        v = logL(K, kap)
        mi = int(v.argmax())
        if v[mi] > best[0]:
            best = (float(v[mi]), K[mi], kap)
    v, k0, kap = best
    for _ in range(3):
        t1 = np.cross(k0, [0, 0, 1]); t1 /= np.linalg.norm(t1)
        t2 = np.cross(k0, t1)
        Ks = []
        for da in np.linspace(-0.05, 0.05, 21):
            for db in np.linspace(-0.05, 0.05, 21):
                kv = k0 + da * t1 + db * t2
                Ks.append(kv / np.linalg.norm(kv))
        Ks = np.array(Ks)
        for kap2 in np.linspace(max(0.0, kap - 0.1), kap + 0.1, 41):
            vv = logL(Ks, kap2)
            mi = int(vv.argmax())
            if vv[mi] > v:
                v, k0, kap = float(vv[mi]), Ks[mi], kap2
    dll = v - (-n * math.log(2))
    lon = math.degrees(math.atan2(k0[1], k0[0])) % 360.0
    lat = math.degrees(math.asin(float(np.clip(k0[2], -1, 1))))
    return {"Z": float(math.sqrt(max(0.0, 2 * dll))),
            "direction_deg": float(lon), "direction_lat_deg": float(lat),
            "kappa": float(kap), "delta_logL": float(dll),
            "logL_max": float(v), "_logL_fn": logL, "_n": n}


def cl3d(sample):
    return _cl3d_logL(sample)


def profile3d_direction(sample, lon_step=0.5, lat_step=1.0, kap_max=8.0, kap_step=0.05):
    """Profile the 3D conditional log-likelihood over ecliptic longitude of the
    preferred direction, maximizing over latitude and kappa (SCT26 Sec. VI).
    Returns the ML longitude and the 1-sigma envelope (delta logL = 0.5)."""
    r = _cl3d_logL(sample)
    logL = r["_logL_fn"]
    lons = np.arange(0.0, 360.0, lon_step)
    lats = np.radians(np.arange(-90.0, 90.0 + 1e-9, lat_step))
    lr = np.radians(lons)
    K = np.stack([np.cos(lats)[None, :] * np.cos(lr)[:, None],
                  np.cos(lats)[None, :] * np.sin(lr)[:, None],
                  np.broadcast_to(np.sin(lats)[None, :], (len(lons), len(lats)))], axis=2)
    Kf = K.reshape(-1, 3)
    prof = np.full(len(lons), -np.inf)
    gmax = -np.inf
    for kap in np.arange(0.0, kap_max + 1e-9, kap_step):
        v = logL(Kf, kap).reshape(len(lons), len(lats))
        prof = np.maximum(prof, v.max(axis=1))
        gmax = max(gmax, float(v.max()))
    gmax = max(gmax, r["logL_max"])
    ml_lon = float(lons[int(prof.argmax())])
    thr = gmax - 0.5
    above = prof >= thr
    i0 = int(prof.argmax())
    lo, hi = i0, i0
    while above[(lo - 1) % len(lons)] and (i0 - lo) < len(lons): lo -= 1
    while above[(hi + 1) % len(lons)] and (hi - i0) < len(lons): hi += 1
    minus = (i0 - lo) * lon_step
    plus = (hi - i0) * lon_step
    return {"ml_lon": ml_lon, "plus_deg": float(plus), "minus_deg": float(minus),
            "global_logL_max": float(gmax), "threshold": float(thr),
            "refined_ml_lon": r["direction_deg"]}


def run_all(sample_path):
    objects = load_sample(sample_path)
    subsets = sample_subsets(objects)
    out = {}
    for name, sub in subsets.items():
        out[name] = {
            "N": len(sub),
            "simple": simple_stats(sub),
            "cl2d": cl2d(sub),
            "cl3d": cl3d(sub),
        }
    return out


def compare_to_anchors(results, z_tol=0.15, dir_tol=3.0):
    """Return per-cell comparison with the paper's published Table 1 values."""
    comp = {}
    for method, key in (("simple", "simple"), ("cl2d", "cl2d"), ("cl3d", "cl3d")):
        comp[method] = {}
        for sample_name, (z_pub, dir_pub) in ANCHORS[method].items():
            got = results[sample_name][key]
            dz = got["Z"] - z_pub
            ddir = abs((got["direction_deg"] - dir_pub + 180) % 360 - 180)
            comp[method][sample_name] = {
                "Z": got["Z"], "Z_published": z_pub, "dZ": dz,
                "direction_deg": got["direction_deg"], "direction_published": dir_pub,
                "dDirection_deg": ddir,
                "within_tolerance": abs(dz) <= z_tol and ddir <= dir_tol,
            }
    return comp
