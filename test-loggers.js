/* Test loggers (testing-schedule.html), 2 Oct 2026.
   One bench data logger per test (modeled on a Graphtec GL260). Everything on it reports
   something true about its test:
     terminal block  the data sources the test reads from
     POWER / ARMED / RESULT lights   ARMED steady = pre-registered and waiting for data,
                     blinking = data window open, off = not yet pre-registered; RESULT shows the color
     screen          modes chosen with the MODE keys: the decision gauge, the measured plane,
                     history, papers per week from the Horizon Scanner's Living Review, timeline
     readout panel   time to the data, papers this week and this month, stage, record
     OUTCOME lamps   light only when the result arrives
     keys            RECORD = the dated pre-registration; REVIEW = the papers on this test;
                     ENTER = the prediction and all three outcomes; up/down = previous/next logger;
                     the blue status key = this test's row in the schedule
   Values that came before a prediction are labeled "before the test".
   The prediction and outcome text is the record's own (moved from validation.html). */
(function () {
  var T = {
    rc1: { id: 'COSMIC-005', topic: 'dark-energy', record: 'https://doi.org/10.5281/zenodo.22719514', stage: 'waiting', result: null,
           inputs: ['DESI BAO', 'CMB'], target: '2026-12-01T09:00:00', targetLabel: 'est. analysis window opens', documented: '2026-09-12',
           screens: ['gauge', 'quadrant', 'history', 'review', 'timeline'],
           lamps: { green: '≥ DR2 3.1σ, in quadrant', yellow: '2–3.1σ, in quadrant', red: '< 2σ or out of quadrant' },
           big: { k: 'DR2 · before the test', v: '3.1', u: 'σ' },
           gauge: { max: 6, zones: [[0, 2, 'red'], [2, 3.1, 'yellow'], [3.1, 6, 'green']], marks: [[5, '5σ']], parked: 3.1, parkedLabel: 'DR2 3.1σ · before the test', result: null },
           /* DESI DR2 (arXiv:2503.14738) and DR1 (arXiv:2404.03002): DESI BAO + CMB, no supernovae */
           quadrant: { x: [-1.6, 0.2], y: [-3.5, 1.5], fit: { x: -0.42, sx: 0.21, y: -1.75, sy: 0.58, rho: -0.9, label: 'DR2' } },
           history: [['DR1', 'Apr 2024', 2.6], ['DR2', 'Mar 2025', 3.1], ['DR3', '2027', null]] },
    rc2: { id: null, topic: 'working-memory', record: null, stage: 'documented', result: null,
           inputs: ['INTERNAL STUDY'], target: '2027-02-01T09:00:00', targetLabel: 'testing begins', documented: '2026-01-31',
           screens: ['timeline', 'review'], lamps: { green: 'Transfer-rate advantage', yellow: 'Advantage in some modalities', red: 'No measurable advantage' } },
    rc3: { id: 'COSMIC-008', topic: 'cmb-polarization', record: null, stage: 'documented', result: null,
           inputs: ['SIMONS OBS'], target: '2027-03-01T14:00:00', targetLabel: 'est. first results', documented: '2026-05-01',
           screens: ['timeline', 'review'], lamps: { green: 'Signature at predicted scale', yellow: 'Pattern at another scale', red: 'No predicted pattern' } },
    rc4: { id: 'COSMIC-013', topic: 'landauer-biology', record: null, stage: 'documented', result: null,
           inputs: ['INTERNAL STUDY'], target: '2027-04-01T12:00:00', targetLabel: 'testing window opens', documented: '2026-01-24',
           screens: ['timeline', 'review'], lamps: { green: 'Landauer heat detected', yellow: 'Below predicted size', red: 'No detectable signal' } },
    rc9: { id: 'COSMIC-007', topic: null, record: 'https://doi.org/10.5281/zenodo.22720954', stage: 'waiting', result: null,
           inputs: ['RUBIN LSST', 'EUCLID'], target: '2028-07-01T12:00:00', targetLabel: 'est. Data Release 1', documented: '2026-09-12',
           screens: ['timeline'], lamps: { green: '> 3σ at predicted scale and axis', yellow: 'Other scale or axis, or < 3σ', red: 'Statistically isotropic' } },
    rc5: { id: 'COSMIC-SD-001', topic: 'landauer', record: null, stage: 'documented', result: null,
           inputs: ['LHCb', 'ATLAS', 'CMS'], target: '2027-05-01T12:00:00', targetLabel: 'target data comparison', documented: '2026-05-21',
           screens: ['timeline', 'review'], lamps: { green: 'Landauer heat excess', yellow: 'Partial, below prediction', red: 'No Landauer excess' } },
    rc6: { id: 'COSMIC-SD-002', topic: null, record: null, stage: 'documented', result: null,
           inputs: ['PDG CKM'], target: '2027-06-01T12:00:00', targetLabel: 'derivation target', documented: '2026-05-21',
           screens: ['timeline'], lamps: { green: 'Matches PDG CKM values', yellow: 'Approximate match', red: 'No information structure' } },
    rc7: { id: 'COSMIC-SD-003', topic: 'qcd-entanglement', record: null, stage: 'documented', result: null,
           inputs: ['LATTICE QCD', 'EIC'], target: '2027-04-01T12:00:00', targetLabel: 'lattice QCD comparison', documented: '2026-05-21',
           screens: ['timeline', 'review'], lamps: { green: 'Scaling matches cosmology', yellow: 'Different functional form', red: 'No relationship' } },
    rc8: { id: 'COSMIC-SD-004', topic: 'qcd-entanglement', record: null, stage: 'documented', result: null,
           inputs: ['RHIC', 'ALICE'], target: '2027-02-01T12:00:00', targetLabel: 'RHIC / ALICE analysis', documented: '2026-05-21',
           screens: ['timeline', 'review'], lamps: { green: 'Entropy drop beyond thermal', yellow: 'Drop, different size', red: 'Fully thermal' } }
  };
  var ORDER = ['rc1', 'rc9', 'rc2', 'rc3', 'rc4', 'rc5', 'rc6', 'rc7', 'rc8'];
  var MODE = { gauge: 'DECISION GAUGE', quadrant: 'w₀–wₐ PLANE', history: 'HISTORY', review: 'PAPERS / WEEK', timeline: 'TIMELINE' };
  var STAGE = { documented: 'Documented', waiting: 'Registered', window: 'Data window open', green: 'Result: green', yellow: 'Result: yellow', red: 'Result: red' };
  var ZONE = { green: '#2ecc40', yellow: '#ffd21f', red: '#ff3b30' };
  var CH = ['#ffe14d', '#4dd2ff', '#ff6ec7', '#7dff7a', '#ff9f43'];
  var W = 260, H = 160, ns = 'http://www.w3.org/2000/svg';
  var FW = null;

  function el(t, a) { var e = document.createElementNS(ns, t); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function tx(s, x, y, a) { var t = el('text', Object.assign({ x: x, y: y, fill: '#e8e8e8', 'font-size': 10, 'font-family': 'IBM Plex Mono, monospace' }, a || {})); t.textContent = s; return t; }
  function frame(label) {
    var s = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': label });
    for (var i = 1; i < 10; i++) s.appendChild(el('line', { x1: i * W / 10, y1: 0, x2: i * W / 10, y2: H, stroke: '#2a2a2a', 'stroke-width': 1 }));
    for (var j = 1; j < 6; j++) s.appendChild(el('line', { x1: 0, y1: j * H / 6, x2: W, y2: j * H / 6, stroke: '#2a2a2a', 'stroke-width': 1 }));
    return s;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---- screens ---- */
  function gauge(c) {
    var g = c.gauge, s = frame('Decision gauge'), cx = W / 2, cy = 130, r = 96;
    s.innerHTML = ''; s.appendChild(el('rect', { width: W, height: H, fill: '#000' }));
    function pt(v, rr) { var a = Math.PI * (1 - v / g.max); return [cx + rr * Math.cos(a), cy - rr * Math.sin(a)]; }
    function arc(v0, v1, rr) { var p0 = pt(v0, rr), p1 = pt(v1, rr); return 'M' + p0 + ' A' + rr + ',' + rr + ' 0 0,1 ' + p1; }
    s.appendChild(el('path', { d: arc(0, g.max, r), stroke: '#222', 'stroke-width': 18, fill: 'none' }));
    g.zones.forEach(function (z) { s.appendChild(el('path', { d: arc(z[0], z[1], r), stroke: ZONE[z[2]], 'stroke-width': 13, fill: 'none' })); });
    for (var v = 0; v <= g.max; v++) { var a = pt(v, r - 12), b = pt(v, r - 20), t = pt(v, r - 31);
      s.appendChild(el('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: '#ddd', 'stroke-width': 1.5 }));
      s.appendChild(tx(v, t[0], t[1] + 4, { 'text-anchor': 'middle', 'font-size': 11 })); }
    g.marks.forEach(function (m) { var a = pt(m[0], r + 10), b = pt(m[0], r - 9), t = pt(m[0], r + 19);
      s.appendChild(el('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: '#fff', 'stroke-width': 2 }));
      s.appendChild(tx(m[1], t[0] + 4, t[1], { 'text-anchor': 'middle', fill: '#fff', 'font-size': 11 })); });
    var p = pt(g.parked, r - 6);
    s.appendChild(el('line', { x1: cx, y1: cy, x2: p[0], y2: p[1], stroke: '#9aa', 'stroke-width': 2.5, 'stroke-dasharray': '5 3' }));
    if (g.result != null) { var q = pt(g.result, r - 4); s.appendChild(el('line', { x1: cx, y1: cy, x2: q[0], y2: q[1], stroke: '#fff', 'stroke-width': 4, 'stroke-linecap': 'round' })); }
    s.appendChild(el('circle', { cx: cx, cy: cy, r: 6, fill: '#ccc' }));
    s.appendChild(tx(g.parkedLabel, cx, H - 6, { 'text-anchor': 'middle', fill: '#bcc', 'font-size': 10 }));
    s.appendChild(tx(g.result == null ? 'DR3 needle: awaiting data' : 'DR3 result', cx, 13, { 'text-anchor': 'middle', fill: '#ffe14d', 'font-size': 10 }));
    return s;
  }
  function quadrant(c) {
    var q = c.quadrant, s = frame('w0 against wa'), m = { l: 26, r: 6, t: 8, b: 18 };
    var X = function (v) { return m.l + (v - q.x[0]) / (q.x[1] - q.x[0]) * (W - m.l - m.r); };
    var Y = function (v) { return H - m.b - (v - q.y[0]) / (q.y[1] - q.y[0]) * (H - m.t - m.b); };
    s.appendChild(el('rect', { x: X(-1), y: Y(0), width: X(q.x[1]) - X(-1), height: Y(q.y[0]) - Y(0), fill: '#2ecc40', opacity: .22 }));
    s.appendChild(tx('PREDICTED QUADRANT', X(-1) + 5, Y(q.y[0]) - 5, { fill: '#7dff7a', 'font-size': 9 }));
    s.appendChild(el('line', { x1: X(-1), y1: m.t, x2: X(-1), y2: H - m.b, stroke: '#888', 'stroke-dasharray': '3 3' }));
    s.appendChild(el('line', { x1: m.l, y1: Y(0), x2: W - m.r, y2: Y(0), stroke: '#888', 'stroke-dasharray': '3 3' }));
    var f = q.fit, a = f.sx * f.sx, b = f.rho * f.sx * f.sy, d = f.sy * f.sy, tr = (a + d) / 2, det = Math.sqrt(Math.pow((a - d) / 2, 2) + b * b), l1 = tr + det, l2 = tr - det, ang = Math.atan2(l1 - a, b);
    [2, 1].forEach(function (k) { var pts = [];
      for (var i = 0; i <= 60; i++) { var t = i / 60 * 2 * Math.PI, u = k * Math.sqrt(l1) * Math.cos(t), w = k * Math.sqrt(Math.max(l2, 1e-6)) * Math.sin(t);
        pts.push(X(f.x + u * Math.cos(ang) - w * Math.sin(ang)).toFixed(1) + ',' + Y(f.y + u * Math.sin(ang) + w * Math.cos(ang)).toFixed(1)); }
      s.appendChild(el('polygon', { points: pts.join(' '), fill: '#4dd2ff', 'fill-opacity': k === 1 ? .4 : .15, stroke: '#4dd2ff', 'stroke-width': 1.2 })); });
    s.appendChild(tx(f.label, X(f.x) + 12, Y(f.y + 1.4 * f.sy), { fill: '#4dd2ff', 'font-size': 10 }));
    s.appendChild(tx(f.label + ' = before the test', W - 6, 13, { 'text-anchor': 'end', fill: '#4dd2ff', 'font-size': 9 }));
    s.appendChild(el('circle', { cx: X(-1), cy: Y(0), r: 4, fill: '#fff' }));
    s.appendChild(tx('ΛCDM', X(-1) - 5, Y(0) - 6, { 'text-anchor': 'end', fill: '#fff', 'font-size': 10 }));
    s.appendChild(tx('w₀', W - 8, H - 5, { 'text-anchor': 'end', 'font-size': 11 }));
    s.appendChild(tx('wₐ', 4, 16, { 'font-size': 11 }));
    s.appendChild(tx('−1', X(-1), H - 5, { 'text-anchor': 'middle', 'font-size': 9, fill: '#aaa' }));
    return s;
  }
  function history(c) {
    var h = c.history, g = c.gauge, s = frame('Significance at each release'), m = { l: 30, r: 8, t: 14, b: 26 }, n = h.length;
    var X = function (i) { return m.l + (i + .5) * (W - m.l - m.r) / n; }, Y = function (v) { return H - m.b - v / g.max * (H - m.t - m.b); };
    g.zones.forEach(function (z) { s.appendChild(el('rect', { x: m.l, y: Y(z[1]), width: W - m.l - m.r, height: Y(z[0]) - Y(z[1]), fill: ZONE[z[2]], opacity: .16 })); });
    [2, 3.1, 5].forEach(function (v) { s.appendChild(tx(v + 'σ', m.l - 4, Y(v) + 3, { 'text-anchor': 'end', 'font-size': 9, fill: '#bbb' })); });
    h.forEach(function (r, i) {
      if (r[2] != null) { s.appendChild(el('rect', { x: X(i) - 13, y: Y(r[2]), width: 26, height: Y(0) - Y(r[2]), fill: CH[i] }));
        s.appendChild(tx(r[2] + 'σ', X(i), Y(r[2]) - 4, { 'text-anchor': 'middle', 'font-size': 10, fill: '#fff' })); }
      else { s.appendChild(el('rect', { x: X(i) - 13, y: m.t, width: 26, height: Y(0) - m.t, fill: 'none', stroke: '#ffe14d', 'stroke-dasharray': '4 3' }));
        s.appendChild(tx('?', X(i), Y(3), { 'text-anchor': 'middle', 'font-size': 18, fill: '#ffe14d' })); }
      s.appendChild(tx(r[0], X(i), H - 13, { 'text-anchor': 'middle', 'font-size': 10 }));
      s.appendChild(tx(r[1], X(i), H - 3, { 'text-anchor': 'middle', 'font-size': 8, fill: '#aaa' }));
    });
    return s;
  }
  function review(c) {
    var s = frame('New papers per week bearing on this test');
    if (!FW) { s.appendChild(tx('loading the Living Review…', W / 2, H / 2, { 'text-anchor': 'middle' })); return s; }
    var now = new Date(FW.updated), weeks = 9, counts = new Array(weeks).fill(0);
    FW.items.forEach(function (i) { if (!match(c, i)) return; var w = Math.floor((now - new Date(i.date)) / 6048e5); if (w >= 0 && w < weeks) counts[weeks - 1 - w]++; });
    var mx = Math.max.apply(null, counts.concat([4])), m = { l: 22, r: 8, t: 14, b: 18 };
    var X = function (i) { return m.l + i * (W - m.l - m.r) / (weeks - 1); }, Y = function (v) { return H - m.b - v / mx * (H - m.t - m.b); };
    s.appendChild(el('polyline', { points: counts.map(function (v, i) { return X(i) + ',' + Y(v); }).join(' '), fill: 'none', stroke: '#ffe14d', 'stroke-width': 2.5 }));
    counts.forEach(function (v, i) { s.appendChild(el('circle', { cx: X(i), cy: Y(v), r: 3, fill: '#ffe14d' })); });
    s.appendChild(tx('0', m.l - 5, Y(0) + 3, { 'text-anchor': 'end', 'font-size': 9, fill: '#aaa' }));
    s.appendChild(tx(mx, m.l - 5, Y(mx) + 3, { 'text-anchor': 'end', 'font-size': 9, fill: '#aaa' }));
    s.appendChild(tx(weeks + ' weeks ago', m.l, H - 4, { 'font-size': 9, fill: '#aaa' }));
    s.appendChild(tx('this week', W - m.r, H - 4, { 'text-anchor': 'end', 'font-size': 9, fill: '#aaa' }));
    s.appendChild(tx('NEW PAPERS ON THIS TEST, PER WEEK', W / 2, 11, { 'text-anchor': 'middle', 'font-size': 9, fill: '#4dd2ff' }));
    return s;
  }
  function timeline(c) {
    var s = frame('Timeline from documentation to the data'), a = new Date(c.documented), b = new Date(c.target), now = new Date();
    var x0 = 20, x1 = W - 20, X = function (d) { return x0 + Math.min(1, Math.max(0, (d - a) / (b - a))) * (x1 - x0); }, y = 92;
    s.appendChild(el('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: '#666', 'stroke-width': 6, 'stroke-linecap': 'round' }));
    s.appendChild(el('line', { x1: x0, y1: y, x2: X(now), y2: y, stroke: '#4dd2ff', 'stroke-width': 6, 'stroke-linecap': 'round' }));
    s.appendChild(el('circle', { cx: x0, cy: y, r: 6, fill: '#4dd2ff' }));
    s.appendChild(el('circle', { cx: x1, cy: y, r: 7, fill: '#000', stroke: '#ffe14d', 'stroke-width': 2.5 }));
    s.appendChild(el('polygon', { points: (X(now) - 6) + ',' + (y - 18) + ' ' + (X(now) + 6) + ',' + (y - 18) + ' ' + X(now) + ',' + (y - 8), fill: '#fff' }));
    s.appendChild(tx('NOW', X(now), y - 22, { 'text-anchor': 'middle', fill: '#fff', 'font-size': 10 }));
    var f = function (d) { return d.toLocaleDateString(undefined, { month: 'short', year: 'numeric' }); };
    s.appendChild(tx((c.stage === 'waiting' ? 'Registered ' : 'Documented ') + f(a), x0, y + 26, { 'font-size': 9.5, fill: '#4dd2ff' }));
    s.appendChild(tx(f(b), x1, y + 26, { 'text-anchor': 'end', 'font-size': 9.5, fill: '#ffe14d' }));
    s.appendChild(tx(c.targetLabel, x1, y + 40, { 'text-anchor': 'end', 'font-size': 9, fill: '#ccc' }));
    var pct = Math.round(Math.min(1, Math.max(0, (now - a) / (b - a))) * 100);
    s.appendChild(tx(pct + '% of the way to the data', W / 2, 24, { 'text-anchor': 'middle', 'font-size': 11, fill: '#7dff7a' }));
    return s;
  }
  var DRAW = { gauge: gauge, quadrant: quadrant, history: history, review: review, timeline: timeline };
  function match(c, i) { return (c.topic && i.topics.indexOf(c.topic) >= 0) || (c.id && i.tests.indexOf(c.id) >= 0); }

  /* ---- one logger ---- */
  function build(key, src, grid) {
    var c = T[key], card = src.querySelector('#' + key); if (!c || !card) return null;
    var title = card.querySelector('h3').textContent, mname = (card.querySelector('.rc-mname') || {}).textContent || '',
        patch = (card.querySelector('.rc-mission') || {}).getAttribute ? card.querySelector('.rc-mission').getAttribute('src') : '';
    var stageCls = c.result ? 'res-' + c.result : c.stage === 'window' ? 'blink' : c.stage === 'waiting' ? 'on-amber' : '';
    var lg = document.createElement('article');
    lg.className = 'lg'; lg.id = 'logger-' + (c.id || key); lg.setAttribute('aria-label', title + ' test logger');
    lg.innerHTML =
      '<div class="lg-term" aria-label="Data sources">' + c.inputs.map(function (n) { return '<div class="lg-screw"><i></i><b>' + esc(n) + '</b></div>'; }).join('') + '</div>' +
      '<div class="lg-body">' +
        '<div class="lg-top"><div class="lg-vent"></div><div class="lg-leds">' +
          '<span class="lg-led power"><i></i>Power</span><span class="lg-led ' + (c.stage === 'window' ? 'blink' : c.stage === 'waiting' ? 'on-amber' : '') + '" title="Steady: pre-registered, waiting for data. Blinking: data window open. Off: not yet pre-registered."><i></i>Armed</span>' +
          '<span class="lg-led ' + (c.result ? 'res-' + c.result : '') + '"><i></i>Result</span></div></div>' +
        '<div class="lg-face"><div>' +
          '<div class="lg-brand">Ic<sup>2</sup> TEST LOGGER</div>' +
          '<div class="lg-lcd">' +
            '<div class="lg-hdr"><span class="md"></span><span class="id">' + esc(c.id || 'INTERNAL') + '</span><span class="clk"></span></div>' +
            '<div class="lg-main"><div class="lg-plot"></div><div class="lg-read">' +
              '<div class="ttl">READOUT</div>' +
              (c.big ? '<div class="lg-big"><span class="k">' + esc(c.big.k) + '</span><span class="v">' + esc(c.big.v) + '<span class="u"> ' + esc(c.big.u) + '</span></span></div>'
                     : '<div class="lg-big"><span class="k">TO ' + esc(c.targetLabel.toUpperCase()) + '</span><span class="v dd">--<span class="u"> days</span></span></div>') +
              '<div class="lg-row"><i class="c" style="background:' + CH[0] + '"></i><span class="k">T−</span><span class="v cd">--</span></div>' +
              '<div class="lg-row"><i class="c" style="background:' + CH[1] + '"></i><span class="k">Papers 7 d</span><span class="v p7">' + (c.topic || c.id ? '--' : 'n/a') + '</span></div>' +
              '<div class="lg-row"><i class="c" style="background:' + CH[2] + '"></i><span class="k">Papers 30 d</span><span class="v p30">' + (c.topic || c.id ? '--' : 'n/a') + '</span></div>' +
              '<div class="lg-row"><i class="c" style="background:' + CH[3] + '"></i><span class="k">Stage</span><span class="v">' + esc(STAGE[c.result || c.stage]) + '</span></div>' +
              '<div class="lg-row"><i class="c" style="background:' + CH[4] + '"></i><span class="k">Record</span><span class="v">' + (c.record ? 'DOI' : 'pending') + '</span></div>' +
            '</div></div>' +
            '<div class="lg-foot">OUTCOME <span class="lamp green' + (c.result === 'green' ? ' on' : '') + '" title="Green: ' + esc(c.lamps.green) + '"></span><span class="lamp yellow' + (c.result === 'yellow' ? ' on' : '') + '" title="Yellow: ' + esc(c.lamps.yellow) + '"></span><span class="lamp red' + (c.result === 'red' ? ' on' : '') + '" title="Red: ' + esc(c.lamps.red) + '"></span><span class="rule">G ' + esc(c.lamps.green) + '</span></div>' +
          '</div>' +
          '<div class="lg-model"><b>' + esc(mname.trim()) + '</b> logger &middot; ' + esc(title) + '</div>' +
        '</div>' +
        '<div class="lg-keys">' +
          '<button class="lg-key prev" type="button">&#9664; Mode</button><button class="lg-key next" type="button">Mode &#9654;</button>' +
          (c.record ? '<a class="lg-key red" href="' + c.record + '" target="_blank" rel="noopener" title="The dated pre-registration">Record</a>'
                    : '<span class="lg-key red" aria-disabled="true" title="Not yet pre-registered">Record</span>') +
          (c.topic ? '<a class="lg-key" href="media.html?fw=' + c.topic + '#field-watch" title="New papers bearing on this test">Review</a>'
                   : '<span class="lg-key" aria-disabled="true" title="No Living Review topic yet">Review</span>') +
          '<div class="lg-pad"><button class="up" type="button" aria-label="Previous logger">&#9650;</button><button class="lt" type="button" aria-label="Previous mode">&#9664;</button>' +
            '<button class="ent" type="button" aria-expanded="false" aria-label="Show the prediction and all three outcomes">ENTER</button>' +
            '<button class="rt" type="button" aria-label="Next mode">&#9654;</button><button class="dn" type="button" aria-label="Next logger">&#9660;</button></div>' +
          '<a class="lg-start" href="#' + (c.id || 'schedule') + '" title="This test in the schedule">' + (c.result ? 'RESULT IN' : c.stage === 'window' ? 'LOGGING' : c.stage === 'waiting' ? 'ARMED' : 'STANDBY') +
            '<small>' + (c.result ? 'see outcome' : c.stage === 'waiting' ? 'waiting for data' : 'not yet registered') + '</small></a>' +
        '</div>' +
        '</div>' +
      '</div>' +
      '<div class="lg-drawer"></div>';
    var body = card.querySelector('.rcard-body'); if (body) lg.querySelector('.lg-drawer').appendChild(body);
    grid.appendChild(lg);

    var mode = 0;
    function draw() {
      var name = c.screens[mode], p = lg.querySelector('.lg-plot');
      p.innerHTML = ''; p.appendChild(DRAW[name](c));
      lg.querySelector('.md').textContent = MODE[name] + '  ' + (mode + 1) + '/' + c.screens.length;
    }
    function step(d) { mode = (mode + d + c.screens.length) % c.screens.length; draw(); }
    lg.querySelector('.prev').onclick = function () { step(-1); }; lg.querySelector('.lt').onclick = function () { step(-1); };
    lg.querySelector('.next').onclick = function () { step(1); }; lg.querySelector('.rt').onclick = function () { step(1); };
    lg.querySelector('.ent').onclick = function () { var o = lg.classList.toggle('open'); this.setAttribute('aria-expanded', String(o)); };
    function go(d) { var all = Array.prototype.slice.call(document.querySelectorAll('.lg')), n = all[all.indexOf(lg) + d]; if (n) n.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    lg.querySelector('.up').onclick = function () { go(-1); };
    lg.querySelector('.dn').onclick = function () { go(1); };
    draw();
    return { lg: lg, c: c, redraw: draw, mode: function () { return c.screens[mode]; } };
  }

  function tick(list) {
    var now = new Date(), clk = now.toLocaleString(undefined, { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    list.forEach(function (L) {
      var diff = new Date(L.c.target) - now, d = Math.max(0, Math.floor(diff / 864e5)), h = Math.max(0, Math.floor(diff % 864e5 / 36e5)),
          m = Math.max(0, Math.floor(diff % 36e5 / 6e4)), s = Math.max(0, Math.floor(diff % 6e4 / 1e3)), p2 = function (n) { return String(n).padStart(2, '0'); };
      L.lg.querySelector('.clk').textContent = clk;
      L.lg.querySelector('.cd').textContent = diff > 0 ? d + 'd ' + p2(h) + ':' + p2(m) + ':' + p2(s) : 'due';
      var dd = L.lg.querySelector('.dd'); if (dd) dd.firstChild.nodeValue = diff > 0 ? d : 0;
    });
  }

  function init() {
    var src = document.getElementById('lg-src'), grid = document.getElementById('lg-grid'); if (!src || !grid) return;
    var list = ORDER.map(function (k) { return build(k, src, grid); }).filter(Boolean);
    src.parentNode.removeChild(src);
    /* mount them in a rack: a header plate, then shelves of two, each shelf screwed to the rails */
    var rack = grid; rack.className = 'lg-rack';
    var head = document.createElement('div'); head.className = 'lg-rack-head';
    head.innerHTML = '<span class="lg-ear l"><i></i><i></i></span><span class="lg-plate">Ic<sup>2</sup> RESEARCH INSTITUTE · TEST BENCH · ' + list.length + ' LOGGERS</span><span class="lg-ear r"><i></i><i></i></span>';
    rack.insertBefore(head, rack.firstChild);
    for (var i = 0; i < list.length; i += 2) {
      var shelf = document.createElement('div'); shelf.className = 'lg-shelf';
      shelf.innerHTML = '<span class="lg-ear l"><i></i><i></i></span><span class="lg-ear r"><i></i><i></i></span>';
      list.slice(i, i + 2).forEach(function (L) { shelf.appendChild(L.lg); });
      if (list.length - i === 1) { var blank = document.createElement('div'); blank.className = 'lg-blank'; blank.setAttribute('aria-hidden', 'true');
        blank.innerHTML = '<span>SLOT ' + (list.length + 1) + '</span><b>Reserved for the next test</b>'; shelf.appendChild(blank); }
      rack.appendChild(shelf);
    }
    var foot = document.createElement('div'); foot.className = 'lg-rack-foot'; rack.appendChild(foot);
    tick(list); setInterval(function () { tick(list); }, 1000);
    fetch('field-watch.json').then(function (r) { return r.json(); }).then(function (d) {
      FW = d; var now = new Date(d.updated);
      list.forEach(function (L) {
        if (!L.c.topic && !L.c.id) return;
        var c7 = 0, c30 = 0;
        d.items.forEach(function (i) { if (!match(L.c, i)) return; var age = (now - new Date(i.date)) / 864e5; if (age <= 7) c7++; if (age <= 30) c30++; });
        L.lg.querySelector('.p7').textContent = c7; L.lg.querySelector('.p30').textContent = c30;
        if (L.mode() === 'review') L.redraw();
      });
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
