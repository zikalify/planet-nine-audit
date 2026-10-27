"""Keplerian propagation of the published Planet Nine reference population.

Conventions
-----------
- Input elements: J2000 heliocentric osculating (a [AU], e, inc, varpi, Omega
  [deg], M at epoch [deg]), exactly as published in the CaltechDATA v3
  reference population (epoch JD 2458270.0 = 1 June 2018).
- Two-body (Kepler) propagation with the Gaussian constant k. Validated in
  tests/test_propagate.py against (1) the dataset's own published epoch
  RA/Dec and (2) full n-body JPL Horizons positions of real Sedna-class
  objects over the same time span. See docs/validation.md.
- Geocentric correction uses a low-precision solar position (accuracy
  ~0.01 deg), negligible versus the parallax scale of the map (<=0.12 deg)
  and the ~0.015 deg limit set by the 2-decimal published element precision.
- Outputs: geocentric astrometric-style J2000 RA/Dec (no aberration).
"""

import numpy as np

K = 0.01720209895           # Gaussian gravitational constant, AU^1.5 day^-1
EPOCH_V3 = 2458270.5        # JD(TDB) 2018-06-01 00:00, matches header "JD=2458270.0" (TT/TDB rounding)
OBLIQUITY_J2000 = np.radians(23.4392911)
AU_KM = 1.495978707e8


def _kepler_E(M, e):
    E = np.array(M, dtype=float, copy=True)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def helio_ecliptic(a, e, inc, varpi, Omega, M0, jd_from, jd_to):
    """Heliocentric ecliptic J2000 Cartesian position (AU) at jd_to."""
    a = np.asarray(a, float); e = np.asarray(e, float)
    n = K / a ** 1.5
    M = np.mod(np.radians(M0) + n * (jd_to - jd_from), 2 * np.pi)
    E = _kepler_E(M, e)
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e * np.cos(E))
    om = np.radians(np.asarray(varpi, float) - np.asarray(Omega, float))
    Om = np.radians(np.asarray(Omega, float)); i = np.radians(np.asarray(inc, float))
    xo, yo = r * np.cos(nu), r * np.sin(nu)
    cw, sw = np.cos(om), np.sin(om)
    cO, sO = np.cos(Om), np.sin(Om)
    ci, si = np.cos(i), np.sin(i)
    x = (cO * cw - sO * sw * ci) * xo + (-cO * sw - sO * cw * ci) * yo
    y = (sO * cw + cO * sw * ci) * xo + (-sO * sw + cO * cw * ci) * yo
    z = (sw * si) * xo + (cw * si) * yo
    return x, y, z, r


def earth_ecliptic(jd):
    """Low-precision heliocentric ecliptic J2000 position of Earth (AU).

    Mean-elements approximation (Vallado-style fundamental arguments);
    longitude/radius accurate to ~0.01 deg / ~1e-4 AU. Adequate for a
    parallax correction of order 1/R rad with R>=150 AU.
    """
    T = (jd - 2451545.0) / 36525.0
    L = np.radians(np.mod(280.460 + 36000.771 * T, 360.0))       # mean longitude
    g = np.radians(np.mod(357.528 + 35999.050 * T, 360.0))       # mean anomaly
    lam = L + np.radians(1.915) * np.sin(g) + np.radians(0.020) * np.sin(2 * g)  # ecliptic longitude (apparent-ish)
    R = 1.00014 - 0.01671 * np.cos(g) - 0.00014 * np.cos(2 * g)
    # Geocentric solar direction -> heliocentric Earth position is opposite.
    return np.array([-R * np.cos(lam), -R * np.sin(lam), np.zeros_like(R) if np.ndim(R) else 0.0])


def geo_radec(a, e, inc, varpi, Omega, M0, jd_from, jd_to, earth=None):
    """Geocentric J2000 RA/Dec (deg) and heliocentric range (AU)."""
    x, y, z, r = helio_ecliptic(a, e, inc, varpi, Omega, M0, jd_from, jd_to)
    ex, ey, ez = earth if earth is not None else earth_ecliptic(jd_to)
    xg, yg, zg = x - ex, y - ey, z - ez
    yq = yg * np.cos(OBLIQUITY_J2000) - zg * np.sin(OBLIQUITY_J2000)
    zq = yg * np.sin(OBLIQUITY_J2000) + zg * np.cos(OBLIQUITY_J2000)
    d = np.sqrt(xg ** 2 + yq ** 2 + zq ** 2)
    ra = np.degrees(np.arctan2(yq, xg)) % 360.0
    dec = np.degrees(np.arcsin(zq / d))
    return ra, dec, r
