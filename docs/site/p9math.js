/* Pure math for the Planet Nine evidence map. Shared by app.js (browser) and site.test.cjs (node).
 * Conventions documented in docs/method.md: J2000 heliocentric osculating elements,
 * two-body Kepler propagation, low-precision Earth position for the geocentric correction. */
'use strict';

const D2R = Math.PI / 180, R2D = 180 / Math.PI;
const EPOCH_JD = 2458270.5;            // 2018-06-01 00:00 TDB, dataset epoch
const J2000 = 2451545.0;
const GK = 0.01720209895;              // Gaussian constant, AU^1.5/day
const OBL = 23.4392911 * D2R;

function jdFromDate(d) { return d.getTime() / 86400000 + 2440587.5; }

function keplerE(M, e) {
  let E = M;
  for (let i = 0; i < 25; i++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
  return E;
}

function earthEcliptic(jd) {
  // Low-precision heliocentric ecliptic J2000 Earth position (AU); ~0.01 deg accuracy.
  const T = (jd - J2000) / 36525;
  const L = (280.460 + 36000.771 * T) * D2R;
  const g = (357.528 + 35999.050 * T) * D2R;
  const lam = L + 1.915 * D2R * Math.sin(g) + 0.020 * D2R * Math.sin(2 * g);
  const R = 1.00014 - 0.01671 * Math.cos(g) - 0.00014 * Math.cos(2 * g);
  return [-R * Math.cos(lam), -R * Math.sin(lam), 0];
}

// Propagate one particle (a AU, angles deg, M0 at EPOCH_JD) to jd; returns [raDeg, decDeg, rHelioAU].
function propagate(a, e, inc, varpi, Omega, M0, jd, earth) {
  const n = GK / Math.pow(a, 1.5);
  const M = ((M0 * D2R + n * (jd - EPOCH_JD)) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
  const E = keplerE(M, e);
  const nu = 2 * Math.atan2(Math.sqrt(1 + e) * Math.sin(E / 2), Math.sqrt(1 - e) * Math.cos(E / 2));
  const r = a * (1 - e * Math.cos(E));
  const om = (varpi - Omega) * D2R, Om = Omega * D2R, i = inc * D2R;
  const xo = r * Math.cos(nu), yo = r * Math.sin(nu);
  const cw = Math.cos(om), sw = Math.sin(om), cO = Math.cos(Om), sO = Math.sin(Om), ci = Math.cos(i), si = Math.sin(i);
  const x = (cO * cw - sO * sw * ci) * xo + (-cO * sw - sO * cw * ci) * yo;
  const y = (sO * cw + cO * sw * ci) * xo + (-sO * sw + cO * cw * ci) * yo;
  const z = (sw * si) * xo + (cw * si) * yo;
  const xg = x - earth[0], yg = y - earth[1], zg = z - earth[2];
  const yq = yg * Math.cos(OBL) - zg * Math.sin(OBL);
  const zq = yg * Math.sin(OBL) + zg * Math.cos(OBL);
  const d = Math.sqrt(xg * xg + yq * yq + zq * zq);
  let ra = Math.atan2(yq, xg) * R2D; if (ra < 0) ra += 360;
  return [ra, Math.asin(zq / d) * R2D, r];
}

// Mollweide projection centered on RA=180; RA increases to the left (sky convention).
function project(ra, dec, w, h) {
  let lon = ra - 180; if (lon > 180) lon -= 360; if (lon < -180) lon += 360;
  const lam = -lon * D2R, lat = dec * D2R;
  let th = lat;
  if (Math.abs(Math.abs(lat) - Math.PI / 2) > 1e-9) {
    for (let i = 0; i < 12; i++) th -= (2 * th + Math.sin(2 * th) - Math.PI * Math.sin(lat)) / (2 + 2 * Math.cos(2 * th));
  } else { th = Math.sign(lat) * Math.PI / 2; }
  const R = Math.min(w / (4 * Math.SQRT2), h / (2 * Math.SQRT2));
  return [w / 2 + R * (2 * Math.SQRT2 / Math.PI) * lam * Math.cos(th),
          h / 2 - R * Math.SQRT2 * Math.sin(th)];
}

// Galactic (l,b) -> equatorial J2000 (RA, Dec), built from the IAU galactic pole and centre.
const G2E = (() => {
  const poleRa = 192.85948 * D2R, poleDec = 27.12825 * D2R;
  const cenRa = 266.405 * D2R, cenDec = -28.936175 * D2R;
  const P = [Math.cos(poleDec) * Math.cos(poleRa), Math.cos(poleDec) * Math.sin(poleRa), Math.sin(poleDec)];
  const C = [Math.cos(cenDec) * Math.cos(cenRa), Math.cos(cenDec) * Math.sin(cenRa), Math.sin(cenDec)];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  let Y = cross(P, C); const ny = Math.hypot(...Y); Y = Y.map(v => v / ny);
  return (l, b) => {
    const cb = Math.cos(b * D2R), sb = Math.sin(b * D2R), cl = Math.cos(l * D2R), sl = Math.sin(l * D2R);
    const v = [0, 1, 2].map(i => cb * cl * C[i] + cb * sl * Y[i] + sb * P[i]);
    let ra = Math.atan2(v[1], v[0]) * R2D;
    return [((ra % 360) + 360) % 360, Math.asin(v[2] / Math.hypot(...v)) * R2D];
  };
})();

// Ecliptic J2000 (lon,lat) -> equatorial (RA, Dec).
function eclipticToEq(lam, beta) {
  const lb = lam * D2R, bt = beta * D2R;
  const sdec = Math.sin(bt) * Math.cos(OBL) + Math.cos(bt) * Math.sin(OBL) * Math.sin(lb);
  const dec = Math.asin(sdec);
  const ra = Math.atan2(Math.sin(lb) * Math.cos(OBL) - Math.tan(bt) * Math.sin(OBL), Math.cos(lb)) * R2D;
  return [((ra % 360) + 360) % 360, dec * R2D];
}

if (typeof module !== 'undefined') module.exports = { jdFromDate, keplerE, earthEcliptic, propagate, project, G2E, eclipticToEq, EPOCH_JD, J2000, D2R, R2D };
