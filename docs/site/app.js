/* Planet Nine: current evidence map (UI layer; math in p9math.js).
 * All positions derive from published data (live-data.json meta). No invented observations. */
'use strict';

let DATA = null;
const canvas = document.getElementById('sky');
const ctx = canvas.getContext('2d');

function drawCurve(eqFn, w, h, style, dash) {
  ctx.strokeStyle = style; ctx.setLineDash(dash || []); ctx.lineWidth = 1.2; ctx.beginPath();
  let prev = null;
  for (let d = 0; d <= 360; d += 2) {
    const [ra, dec] = eqFn(d);
    const [x, y] = project(ra, dec, w, h);
    if (prev && Math.abs(x - prev[0]) > w / 2) ctx.moveTo(x, y);
    else if (!prev) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
    prev = [x, y];
  }
  ctx.stroke(); ctx.setLineDash([]);
}

function drawGrid(w, h) {
  const ui = Math.max(1, 900 / (canvas.getBoundingClientRect().width || w));
  ctx.font = Math.round(11 * ui) + 'px system-ui';
  ctx.strokeStyle = '#2a3550'; ctx.lineWidth = 0.6; ctx.fillStyle = '#7a87a8';
  for (let ra = 0; ra < 360; ra += 30) {
    ctx.beginPath();
    for (let dec = -89; dec <= 89; dec += 2) {
      const [x, y] = project(ra, dec, w, h);
      if (dec === -89) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    const [lx, ly] = project(ra, -8, w, h);
    ctx.fillText('RA ' + ra + '°', lx - 18, ly);
  }
  for (let dec = -60; dec <= 60; dec += 30) {
    ctx.beginPath();
    for (let ra = 0; ra <= 360; ra += 2) {
      const [x, y] = project(ra, dec, w, h);
      if (ra === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    const [lx, ly] = project(178, dec, w, h);
    ctx.fillText((dec > 0 ? '+' : '') + dec + '°', lx + 4, ly - 3);
  }
}

function render(jd) {
  const w = canvas.width, h = canvas.height;
  const ui = Math.max(1, 900 / (canvas.getBoundingClientRect().width || w));
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#0d1220'; ctx.fillRect(0, 0, w, h);
  drawGrid(w, h);
  if (document.getElementById('lyGal').checked) {
    drawCurve(l => G2E(l, 0), w, h, '#8a5cf688', [6, 5]);
    drawCurve(l => G2E(l, 10), w, h, '#8a5cf644', [2, 5]);
    drawCurve(l => G2E(l, -10), w, h, '#8a5cf644', [2, 5]);
  }
  drawCurve(l => eclipticToEq(l, 0), w, h, '#3f6f9f66', [10, 6]);

  if (document.getElementById('lyExcl').checked) {
    const g = DATA.excluded_grid_1deg; let maxc = 1;
    for (const row of g) for (const c of row) if (c > maxc) maxc = c;
    for (let di = 0; di < 180; di++) for (let ri = 0; ri < 360; ri++) {
      const c = g[di][ri]; if (!c) continue;
      const [x, y] = project(ri + 0.5, di - 90 + 0.5, w, h);
      const a = 0.05 + 0.35 * Math.sqrt(c / maxc);
      ctx.fillStyle = 'rgba(90,140,255,' + a.toFixed(3) + ')';
      ctx.fillRect(x - 2, y - 2, 4.5, 4.5);
    }
  }

  const u = DATA.unexcluded, N = u.a.length;
  const earth = earthEcliptic(jd);
  let nShown = 0, rsum = 0;
  if (document.getElementById('lyUnex').checked) {
    const cell = {}; let maxc = 1;
    for (let i = 0; i < N; i++) {
      const [ra, dec, r] = propagate(u.a[i], u.e[i], u.inc[i], u.varpi[i], u.Omega[i], u.M[i], jd, earth);
      const key = Math.floor(dec + 90) * 360 + Math.floor(ra);
      cell[key] = (cell[key] || 0) + 1;
      nShown++; rsum += r;
    }
    for (const k in cell) if (cell[k] > maxc) maxc = cell[k];
    for (const k in cell) {
      const key = +k, di = Math.floor(key / 360), ri = key % 360, c = cell[k];
      const [x, y] = project(ri + 0.5, di - 90 + 0.5, w, h);
      const t = Math.sqrt(c / maxc);
      ctx.fillStyle = 'rgba(255,' + Math.round(190 - 130 * t) + ',' + Math.round(90 - 60 * t) + ',' + (0.10 + 0.75 * t).toFixed(3) + ')';
      ctx.fillRect(x - 2.2, y - 2.2, 5, 5);
    }
  }

  if (document.getElementById('lyCand').checked) {
    const labels = [];
    DATA.candidates.forEach((c, idx) => {
      const [x, y] = project(c.ra, c.dec, w, h);
      const m = 7 * ui;
      ctx.fillStyle = '#ffd34d'; ctx.strokeStyle = '#7a5c00'; ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x, y - m); ctx.lineTo(x + m * 0.85, y); ctx.lineTo(x, y + m); ctx.lineTo(x - m * 0.85, y); ctx.closePath();
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#ffd34d'; ctx.font = Math.round(10 * ui) + 'px system-ui';
      const name = c.name.split(' (')[0] + ' · ' + String(c.epoch).slice(0, 4);
      const lw = ctx.measureText(name).width;
      let ly = y + 3 * ui;
      while (labels.some(L => Math.abs(L.x - (x + 8 * ui)) < (L.w + lw) / 2 + 6 * ui && Math.abs(L.y - ly) < 12 * ui)) ly += 13 * ui;
      if (ly !== y + 3 * ui) {
        ctx.strokeStyle = 'rgba(255,211,77,0.5)';
        ctx.beginPath(); ctx.moveTo(x + 4 * ui, y + 4 * ui); ctx.lineTo(x + 8 * ui, ly - 3 * ui); ctx.stroke();
      }
      ctx.fillText(name, x + 8 * ui, ly);
      labels.push({ x: x + 8 * ui + lw / 2, y: ly, w: lw });
      c._px = [x, y]; c._idx = idx;
    });
  }

  document.getElementById('mapStats').textContent =
    DATA.meta.unexcluded_count.toLocaleString() + ' model samples not excluded by the published ZTF/DES/PS1 searches, shown for ' +
    new Date((jd - 2440587.5) * 86400000).toISOString().slice(0, 10) +
    (nShown ? ' (mean heliocentric distance ~' + Math.round(rsum / nShown) + ' AU)' : '') +
    '. Model epoch 2018-06-01; two-body propagation; not a detection.';
}

function currentJD() {
  return jdFromDate(new Date()) + (+document.getElementById('dateSlider').value);
}

function updateDateLabel() {
  const off = +document.getElementById('dateSlider').value;
  const d = new Date(Date.now() + off * 86400000);
  document.getElementById('dateLabel').textContent = d.toISOString().slice(0, 10) + (off === 0 ? ' (today)' : '');
  document.getElementById('asof').textContent = d.toISOString().slice(0, 10);
}

function fillPanels() {
  const tb = document.querySelector('#clTable tbody');
  const res = DATA.clustering.results, cmp = DATA.clustering.anchor_comparison;
  const names = { simple: 'Simple (resultant length)', cl2d: '2D conditional likelihood', cl3d: '3D conditional likelihood' };
  tb.innerHTML = '';
  for (const m of ['simple', 'cl2d', 'cl3d']) {
    for (const s of ['BB21', 'SCT25', 'SCT26']) {
      const r = res[s][m], c = cmp[m][s];
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + names[m] + '</td><td>' + s + '</td><td>' + res[s].N + '</td>' +
        '<td>' + r.Z.toFixed(2) + ' σ</td><td>' + c.Z_published.toFixed(1) + ' σ</td>' +
        '<td>' + r.direction_deg.toFixed(1) + '°</td><td>' + c.direction_published.toFixed(0) + '°</td>';
      tb.appendChild(tr);
    }
  }
  document.getElementById('tracker').textContent =
    'Tracker: ' + DATA.meta.mpc_distant_census_current +
    ' distant MPC objects currently meet the paper census filters (90<a<1000 AU, q>30 AU, uncertainty U<7). ' +
    'New discoveries cannot be added to the clustering sample until a published long-term stability classification exists for them; the sample above is the documented published one.';

  const st = document.getElementById('sampleTable');
  let shtml = '<table><thead><tr><th>Object</th><th>Sample</th><th>a (AU)</th><th>e</th><th>i (deg)</th><th>ϖ (deg)</th><th>First obs used</th><th>Orbit solution</th></tr></thead><tbody>';
  for (const o of DATA.sample) {
    shtml += '<tr><td>' + o.name + '</td><td>' + o.membership + '</td><td>' + o.a + '</td><td>' + o.e + '</td><td>' + o.inc +
      '</td><td>' + o.varpi + '</td><td>' + o.first_obs + '</td><td>' + o.soln_date.slice(0, 10) + '</td></tr>';
  }
  st.innerHTML = shtml + '</tbody></table>';

  const cl = document.getElementById('candList');
  cl.innerHTML = '';
  DATA.candidates.forEach(c => {
    const div = document.createElement('div');
    div.className = 'cand';
    div.innerHTML = '<strong>' + c.name + '</strong> — RA ' + c.ra.toFixed(3) + '°, Dec ' + c.dec.toFixed(3) + '° (J2000, epoch ' + c.epoch + ')<br>' +
      '<span class="src">' + c.source + '</span><br>' + c.note;
    cl.appendChild(div);
  });
  document.getElementById('buildinfo').textContent =
    'Build ' + DATA.meta.build_date_utc + ' · ' + DATA.meta.model + ' · CSV MD5 ' + DATA.meta.record_md5_verified +
    ' · ' + DATA.meta.propagation;
}

canvas.addEventListener('click', ev => {
  if (!DATA) return;
  const rect = canvas.getBoundingClientRect();
  const x = (ev.clientX - rect.left) * (canvas.width / rect.width);
  const y = (ev.clientY - rect.top) * (canvas.height / rect.height);
  let best = null, bd = Math.max(18, 18 * (canvas.width / rect.width));
  DATA.candidates.forEach(c => {
    if (!c._px) return;
    const d = Math.hypot(c._px[0] - x, c._px[1] - y);
    if (d < bd) { bd = d; best = c; }
  });
  const panel = document.getElementById('candDetail');
  if (best) {
    panel.hidden = false;
    panel.innerHTML = '<strong>' + best.name + '</strong><br>RA ' + best.ra + '°, Dec ' + best.dec + '° (J2000, epoch ' + best.epoch + ')<br>' +
      '<span class="src">' + best.source + '</span><br>' + best.note;
  } else panel.hidden = true;
});

fetch('../site/live-data.json').then(r => r.json()).then(d => {
  DATA = d;
  updateDateLabel();
  render(currentJD());
  fillPanels();
  document.getElementById('dateSlider').addEventListener('input', () => { updateDateLabel(); render(currentJD()); });
  for (const id of ['lyUnex', 'lyExcl', 'lyCand', 'lyGal']) document.getElementById(id).addEventListener('change', () => render(currentJD()));
  setInterval(() => { if (+document.getElementById('dateSlider').value === 0) { updateDateLabel(); render(currentJD()); } }, 60000);
});
