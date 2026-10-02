/* Test-bench modules for the validation rack (2 Oct 2026).
   Each module reports something true about its test: the measurement the test decides,
   the decision rule drawn as the instrument's zones, three traffic lamps that light only
   when the result arrives, the stage of the test, and a live count of new papers bearing
   on it from the Horizon Scanner's Living Review (field-watch.json).
   Values that came before a prediction are labeled "before the test".
   Add a module: give the card data-bench="<key>" and add BENCH[<key>] below. */
(function () {
  var BENCH = {
    desi: {
      id: 'COSMIC-005', plate: 'COSMIC-005 · DESI DR3 · MIDNIGHT ERIDANUS',
      topic: 'dark-energy',
      record: 'https://doi.org/10.5281/zenodo.22719514',
      stage: 'waiting',            /* off | waiting | window | green | yellow | red */
      stageText: 'Registered · awaiting DR3 data',
      result: null,                /* 'green' | 'yellow' | 'red' once DESI publishes */
      lamps: { green: '≥ DR2 (3.1σ), in quadrant', yellow: '2σ to 3.1σ, in quadrant', red: '< 2σ or out of quadrant' },
      gauge: { max: 6, zones: [[0, 2, 'red'], [2, 3.1, 'yellow'], [3.1, 6, 'green']], marks: [[5, '5σ']],
               parked: { v: 3.1, label: 'DR2 3.1σ', note: 'before the test' }, result: null,
               title: 'Preference for evolving dark energy (DESI + CMB)' },
      screens: ['quadrant', 'history'],
      /* DESI DR2 (arXiv:2503.14738), DESI BAO + CMB, no supernovae; DR1 (arXiv:2404.03002) */
      quadrant: { x: [-1.6, 0.2], y: [-3.5, 1.5], fit: { x: -0.42, sx: 0.21, y: -1.75, sy: 0.58, rho: -0.9, label: 'DR2' } },
      history: [['DR1', 'Apr 2024', 2.6], ['DR2', 'Mar 2025', 3.1], ['DR3', '2027', null]]
    }
  };

  var LAMP = { green: '#3ddc5a', yellow: '#ffd21f', red: '#ff3b30' };
  var ZONE = { green: '#2e7d32', yellow: '#c9a400', red: '#c62828' };
  var PH = '#7dffa0';                                  /* phosphor */
  var ns = 'http://www.w3.org/2000/svg';
  function el(t, a, kids) { var e = document.createElementNS(ns, t); for (var k in a) e.setAttribute(k, a[k]); (kids || []).forEach(function (c) { e.appendChild(c); }); return e; }
  function txt(x, y, s, a) { var t = el('text', Object.assign({ x: x, y: y, fill: PH, 'font-size': 9, 'font-family': 'IBM Plex Mono, monospace' }, a || {})); t.textContent = s; return t; }

  function gauge(g) {
    var W = 170, H = 112, cx = 85, cy = 90, r = 66;
    var s = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': g.title });
    function pt(v, rr) { var a = Math.PI * (1 - v / g.max); return [cx + rr * Math.cos(a), cy - rr * Math.sin(a)]; }
    function arc(v0, v1, rr) { var p0 = pt(v0, rr), p1 = pt(v1, rr); return 'M' + p0 + ' A' + rr + ',' + rr + ' 0 0,1 ' + p1; }
    s.appendChild(el('path', { d: arc(0, g.max, r), stroke: '#0a200a', 'stroke-width': 13, fill: 'none' }));
    g.zones.forEach(function (z) { s.appendChild(el('path', { d: arc(z[0], z[1], r), stroke: ZONE[z[2]], 'stroke-width': 9, fill: 'none', opacity: .9 })); });
    for (var v = 0; v <= g.max; v++) { var a = pt(v, r - 9), b = pt(v, r - 15); s.appendChild(el('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: PH, 'stroke-width': 1, opacity: .7 }));
      var t = pt(v, r - 23); s.appendChild(txt(t[0], t[1] + 3, v, { 'text-anchor': 'middle', 'font-size': 8, opacity: .8 })); }
    g.marks.forEach(function (m) { var a = pt(m[0], r + 6), b = pt(m[0], r - 6); s.appendChild(el('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: '#fff', 'stroke-width': 1.5 }));
      var t = pt(m[0], r + 13); s.appendChild(txt(t[0], t[1], m[1], { 'text-anchor': 'middle', fill: '#fff', 'font-size': 8 })); });
    var p = g.parked, tip = pt(p.v, r - 4);
    s.appendChild(el('line', { x1: cx, y1: cy, x2: tip[0], y2: tip[1], stroke: '#cfd8e2', 'stroke-width': 2, 'stroke-dasharray': '3 2', opacity: .85 }));
    if (g.result != null) { var rt = pt(g.result, r - 2); s.appendChild(el('line', { x1: cx, y1: cy, x2: rt[0], y2: rt[1], stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round' })); }
    s.appendChild(el('circle', { cx: cx, cy: cy, r: 5, fill: '#cfd8e2' }));
    s.appendChild(txt(cx, cy + 15, p.label + ' · ' + p.note, { 'text-anchor': 'middle', 'font-size': 8.5, fill: '#cfd8e2' }));
    s.appendChild(txt(cx, 10, g.result == null ? 'DR3 NEEDLE: AWAITING DATA' : 'DR3 RESULT', { 'text-anchor': 'middle', 'font-size': 8, opacity: .85 }));
    return s;
  }

  function quadrant(q) {
    var W = 170, H = 120, m = { l: 24, r: 6, t: 8, b: 18 };
    var X = function (v) { return m.l + (v - q.x[0]) / (q.x[1] - q.x[0]) * (W - m.l - m.r); };
    var Y = function (v) { return H - m.b - (v - q.y[0]) / (q.y[1] - q.y[0]) * (H - m.t - m.b); };
    var s = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'w0 against wa: the predicted quadrant, the cosmological constant, and DR2' });
    s.appendChild(el('rect', { x: X(-1), y: Y(0), width: X(q.x[1]) - X(-1), height: Y(q.y[0]) - Y(0), fill: PH, opacity: .13 }));
    s.appendChild(txt(X(-1) + 3, Y(q.y[0]) - 4, 'PREDICTED', { 'font-size': 7.5, opacity: .9 }));
    s.appendChild(el('line', { x1: X(-1), y1: m.t, x2: X(-1), y2: H - m.b, stroke: PH, 'stroke-width': .6, opacity: .5, 'stroke-dasharray': '2 2' }));
    s.appendChild(el('line', { x1: m.l, y1: Y(0), x2: W - m.r, y2: Y(0), stroke: PH, 'stroke-width': .6, opacity: .5, 'stroke-dasharray': '2 2' }));
    var f = q.fit, a = f.sx * f.sx, b = f.rho * f.sx * f.sy, d = f.sy * f.sy;            /* covariance -> ellipse */
    var tr = (a + d) / 2, det = Math.sqrt(Math.pow((a - d) / 2, 2) + b * b), l1 = tr + det, l2 = tr - det;
    var ang = Math.atan2(l1 - a, b);
    [2, 1].forEach(function (k) {
      var pts = []; for (var i = 0; i <= 48; i++) { var t = i / 48 * 2 * Math.PI, u = k * Math.sqrt(l1) * Math.cos(t), w = k * Math.sqrt(Math.max(l2, 1e-6)) * Math.sin(t);
        pts.push(X(f.x + u * Math.cos(ang) - w * Math.sin(ang)).toFixed(1) + ',' + Y(f.y + u * Math.sin(ang) + w * Math.cos(ang)).toFixed(1)); }
      s.appendChild(el('polygon', { points: pts.join(' '), fill: '#cfd8e2', 'fill-opacity': k === 1 ? .35 : .15, stroke: '#cfd8e2', 'stroke-width': .8 }));
    });
    s.appendChild(txt(X(f.x) + 10, Y(f.y + 1.6 * f.sy), f.label, { 'font-size': 8.5, fill: '#cfd8e2' }));
    s.appendChild(txt(W - m.r, m.t + 6, f.label + ' = before the test', { 'text-anchor': 'end', 'font-size': 7, fill: '#cfd8e2', opacity: .85 }));
    s.appendChild(el('circle', { cx: X(-1), cy: Y(0), r: 3, fill: '#fff' }));
    s.appendChild(txt(X(-1) - 3, Y(0) - 4, 'ΛCDM', { 'font-size': 7.5, fill: '#fff', 'text-anchor': 'end' }));
    s.appendChild(txt(W - m.r, H - 4, 'w₀', { 'text-anchor': 'end', 'font-size': 9 }));
    s.appendChild(txt(3, m.t + 6, 'wₐ', { 'font-size': 9 }));
    s.appendChild(txt(X(-1), H - 4, '−1', { 'text-anchor': 'middle', 'font-size': 7.5, opacity: .8 }));
    s.appendChild(txt(m.l - 3, Y(0) + 3, '0', { 'text-anchor': 'end', 'font-size': 7.5, opacity: .8 }));
    return s;
  }

  function history(h, g) {
    var W = 170, H = 120, m = { l: 26, r: 8, t: 14, b: 24 }, n = h.length;
    var X = function (i) { return m.l + (i + .5) * (W - m.l - m.r) / n; };
    var Y = function (v) { return H - m.b - v / g.max * (H - m.t - m.b); };
    var s = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Significance at each DESI data release' });
    g.zones.forEach(function (z) { s.appendChild(el('rect', { x: m.l, y: Y(z[1]), width: W - m.l - m.r, height: Y(z[0]) - Y(z[1]), fill: ZONE[z[2]], opacity: .22 })); });
    [0, 2, 3.1, 5].forEach(function (v) { s.appendChild(txt(m.l - 3, Y(v) + 3, v + 'σ', { 'text-anchor': 'end', 'font-size': 7, opacity: .8 })); });
    h.forEach(function (r, i) {
      if (r[2] != null) { s.appendChild(el('rect', { x: X(i) - 9, y: Y(r[2]), width: 18, height: Y(0) - Y(r[2]), fill: '#cfd8e2', opacity: .85 }));
        s.appendChild(txt(X(i), Y(r[2]) - 3, r[2] + 'σ', { 'text-anchor': 'middle', 'font-size': 8, fill: '#fff' })); }
      else { s.appendChild(el('rect', { x: X(i) - 9, y: m.t, width: 18, height: Y(0) - m.t, fill: 'none', stroke: PH, 'stroke-dasharray': '3 2', opacity: .8 }));
        s.appendChild(txt(X(i), Y(g.max / 2), '?', { 'text-anchor': 'middle', 'font-size': 14 })); }
      s.appendChild(txt(X(i), H - 9, r[0], { 'text-anchor': 'middle', 'font-size': 8 }));
      s.appendChild(txt(X(i), H - 1, r[1], { 'text-anchor': 'middle', 'font-size': 6.5, opacity: .75 }));
    });
    return s;
  }

  var LABEL = { quadrant: 'QUADRANT', history: 'HISTORY' };

  function build(card, cfg) {
    /* nameplate in the rack bar */
    var bar = card.querySelector('.rack-bar .rack-spacer');
    if (bar) { bar.className = 'rack-spacer bench-plate'; bar.textContent = cfg.plate; }

    var b = document.createElement('div');
    b.className = 'bench';
    b.innerHTML =
      '<div class="bench-screens">' +
        '<div class="bench-screen"><div class="bench-cap"><span class="bench-mode"></span><span>MODE</span></div><div class="bench-a"></div></div>' +
        '<div class="bench-screen"><div class="bench-cap"><span>DECISION GAUGE</span><span>σ</span></div><div class="bench-b"></div></div>' +
        '<div class="bench-lamps" role="group" aria-label="Outcome lamps">' +
          ['green', 'yellow', 'red'].map(function (k) {
            return '<div class="bench-lamp-row"><span class="bench-lamp ' + k + (cfg.result === k ? ' on' : '') + '" title="' + k + '"></span>' +
                   '<span class="bench-rule"><b>' + k.toUpperCase() + '</b> ' + cfg.lamps[k] + '</span></div>'; }).join('') +
        '</div>' +
      '</div>' +
      '<div class="bench-strip">' +
        '<button class="bench-knob" type="button" aria-label="Change screen mode"><span></span></button>' +
        '<span class="bench-led ' + cfg.stage + '" aria-hidden="true"></span><span class="bench-stage">' + cfg.stageText + '</span>' +
        '<a class="bench-lcd" href="media.html?fw=' + cfg.topic + '#field-watch" title="New papers bearing on this test, from the Horizon Scanner">' +
          '<span class="lbl">LIVING REVIEW</span><span class="n7">--</span><span class="u">THIS WEEK ·</span><span class="n30">--</span><span class="u">THIS MONTH</span></a>' +
        '<a class="bench-btn" href="' + cfg.record + '" target="_blank" rel="noopener">RECORD</a>' +
        '<a class="bench-btn" href="media.html?fw=' + cfg.topic + '#field-watch">PAPERS</a>' +
      '</div>';
    var head = card.querySelector('.rcard-head');
    head.parentNode.insertBefore(b, head.nextSibling);

    var mode = 0;
    function draw() {
      var a = b.querySelector('.bench-a'), name = cfg.screens[mode];
      a.innerHTML = ''; a.appendChild(name === 'quadrant' ? quadrant(cfg.quadrant) : history(cfg.history, cfg.gauge));
      b.querySelector('.bench-mode').textContent = LABEL[name];
      b.querySelector('.bench-knob').style.setProperty('--rot', (mode * 90 - 45) + 'deg');
    }
    b.querySelector('.bench-b').appendChild(gauge(cfg.gauge));
    b.querySelector('.bench-knob').addEventListener('click', function () { mode = (mode + 1) % cfg.screens.length; draw(); });
    draw();

    fetch('field-watch.json').then(function (r) { return r.json(); }).then(function (d) {
      var now = new Date(d.updated || Date.now()), c7 = 0, c30 = 0;
      d.items.forEach(function (i) {
        if (i.topics.indexOf(cfg.topic) < 0 && i.tests.indexOf(cfg.id) < 0) return;
        var age = (now - new Date(i.date)) / 864e5;
        if (age <= 7) c7++; if (age <= 30) c30++;
      });
      b.querySelector('.n7').textContent = c7; b.querySelector('.n30').textContent = c30;
      if (c7) b.querySelector('.bench-lcd').classList.add('fresh');
    }).catch(function () {});
  }

  document.querySelectorAll('[data-bench]').forEach(function (card) {
    var cfg = BENCH[card.getAttribute('data-bench')];
    if (cfg) build(card, cfg);
  });
})();
