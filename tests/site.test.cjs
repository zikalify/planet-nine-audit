/* Node assertions for the evidence-map math (docs/site/p9math.js). */
'use strict';
const m = require('../docs/site/p9math.js');
let failures = 0;
function check(name, cond) {
  if (!cond) { failures++; console.error('FAIL: ' + name); }
  else console.log('ok: ' + name);
}

// Mollweide geometry
const [cx, cy] = m.project(180, 0, 1200, 640);
check('map center', Math.abs(cx - 600) < 1 && Math.abs(cy - 320) < 1);
const [x0] = m.project(0, 0, 1200, 640);
const [x359] = m.project(359.9, 0, 1200, 640);
check('RA wrap edges symmetric', Math.abs(x0 - (1200 - x359)) < 3);
const [px, py] = m.project(180, 90, 1200, 640);
check('north pole top center', Math.abs(px - 600) < 1 && py >= 0 && py < 40);

// Real published dataset rows (CaltechDATA v3, MD5-verified) at the dataset epoch.
// Tolerance 0.06 deg: published elements carry two decimals (see docs/validation.md).
const EARTH = m.earthEcliptic(m.EPOCH_JD);
const rows = [
  [249.58, 0.074, 12.50, 252.85, 48.03, 72.60, 340.9044, -21.0693],
  [375.45, 0.232, 14.13, 237.85, 111.55, 55.36, 322.4211, -21.4985],
  [944.92, 0.502, 18.60, 237.12, 95.17, 71.09, 12.2508, -14.9859],
];
rows.forEach((r, i) => {
  const [ra, dec] = m.propagate(r[0], r[1], r[2], r[3], r[4], r[5], m.EPOCH_JD, EARTH);
  const dra = Math.abs(((ra - r[6] + 180 + 360) % 360) - 180);
  check('epoch RA/Dec row ' + i, dra < 0.06 && Math.abs(dec - r[7]) < 0.06);
});

// Coordinate rotations
const [raE, decE] = m.eclipticToEq(0, 0);
check('ecliptic origin', Math.abs(raE) < 1e-9 && Math.abs(decE) < 1e-9);
const [raG, decG] = m.G2E(0, 0);
check('galactic centre ~ (266.4, -29.0)', Math.abs(raG - 266.4) < 0.2 && Math.abs(decG + 29.0) < 0.2);

// Kepler solver extreme eccentricity
const E = m.keplerE(3.0, 0.9);
check('kepler residual', Math.abs(E - 0.9 * Math.sin(E) - 3.0) < 1e-12);

if (failures) { console.error(failures + ' failures'); process.exit(1); }
console.log('all site math assertions passed');
