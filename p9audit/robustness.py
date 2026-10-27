"""Sensitivity of SCT26 clustering statistics to detection-epoch and frame conventions.

Recomputes the Simple/2D/3D statistics under variant detection epochs
(first_obs / arc midpoint / last_obs from JPL SBDB) using internally
consistent two-body propagation from full-precision SBDB elements.
Baseline for comparison: the Horizons first_obs geometry in data/sct26-sample.json.
"""
import json, math, sys, datetime
import numpy as np
from p9audit.propagate import helio_ecliptic
from p9audit import clustering

def jd(datestr):
    d = datetime.date.fromisoformat(datestr)
    return d.toordinal() + 1721424.5

def variant_sample(sample_path, full_path, which):
    S = json.load(open(sample_path)); F = json.load(open(full_path))['objects']
    out = []
    for o in S['objects']:
        f = F[o['name']]
        if which == 'first_obs': t = jd(f['first_obs'])
        elif which == 'last_obs': t = jd(f['last_obs'])
        else:
            t = (jd(f['first_obs']) + jd(f['last_obs'])) / 2
        el = f['elements']
        a, e, inc = el['a'], el['e'], el['i']
        varpi = (el['om'] + el['w']) % 360.0
        x, y, z, r = helio_ecliptic(np.array([a]), np.array([e]), np.array([inc]),
                                    np.array([varpi]), np.array([el['om']]), np.array([el['ma']]),
                                    f['epoch_jd'], t)
        lon = math.degrees(math.atan2(y[0], x[0])) % 360.0
        lat = math.degrees(math.asin(z[0] / r[0]))
        phi = math.degrees(math.acos(max(-1, min(1, (a*(1-e*e)/r[0] - 1)/e))))
        out.append({'name': o['name'], 'membership': o['membership'],
                    'elements': {'a': a, 'e': e, 'inc': inc, 'varpi': varpi, 'Omega': el['om']},
                    'detection': {'ecl_lon': lon, 'ecl_lat': lat, 'r_au': float(r[0])},
                    'phi_deg': phi})
    return out

def run(sample_path, full_path):
    base = json.load(open(sample_path))['objects']
    # sanity: propagated first_obs vs stored Horizons geometry
    v0 = variant_sample(sample_path, full_path, 'first_obs')
    bmap = {o['name']: o for o in base}
    diffs = []
    for o in v0:
        b = bmap[o['name']]
        dl = abs((o['detection']['ecl_lon'] - b['detection']['ecl_lon'] + 180) % 360 - 180)
        db = abs(o['detection']['ecl_lat'] - b['detection']['ecl_lat'])
        diffs.append(math.hypot(dl * math.cos(math.radians(b['detection']['ecl_lat'])), db))
    results = {}
    for which in ('first_obs', 'midpoint', 'last_obs'):
        objs = variant_sample(sample_path, full_path, which)
        tmp = '/tmp/_rob_%s.json' % which
        json.dump({'objects': objs}, open(tmp, 'w'))
        results[which] = clustering.run_all(tmp)
    return diffs, results

if __name__ == '__main__':
    diffs, results = run('data/sct26-sample.json', 'data/sct26-elements-full.json')
    d = np.array(diffs) * 3600
    print(f"propagation-vs-Horizons at first_obs: median {np.median(d):.0f}\" max {d.max():.0f}\"")
    keys = list(results['first_obs'].keys())
    for k in keys:
        row = [results[w][k] for w in ('first_obs', 'midpoint', 'last_obs')]
        try:
            zs = [r['z'] for r in row]; ds = [r['dir'] for r in row]
            print(f"{k}: z {zs[0]:.2f}/{zs[1]:.2f}/{zs[2]:.2f}  dir {ds[0]:.0f}/{ds[1]:.0f}/{ds[2]:.0f}")
        except (TypeError, KeyError):
            print(k, row[0])
