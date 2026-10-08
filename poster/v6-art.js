// Poster v6: the origin sequence as one glowing 3D structure, top to bottom.
// Points and links live in a slab (x across, v down the poster, z into the page),
// are turned and projected with perspective, and drawn as added light.
// Each numbered card gets a leader line to the matching depth of the structure.
(function () {
  const W = 2328, H = 3480, K = 2;
  const cv = document.getElementById('art'), g = cv.getContext('2d');
  g.scale(K, K);
  g.fillStyle = '#04060d'; g.fillRect(0, 0, W, H);
  // a soft nebula wash behind the structure
  [[1640, 1500, 900, 'rgba(70,60,190,.22)'], [1700, 2350, 800, 'rgba(160,40,150,.16)'], [1500, 700, 700, 'rgba(40,90,200,.14)']]
    .forEach(([x, y, r, c]) => { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, c); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H); });

  let sd = 7; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const V0 = 260, VH = 2330;                        // the structure spans poster y 260 .. 2590
  const CX = 1660, HALF = 560, DEPTH = 420, TH = -.55, F = 2000;
  function P(x, v, z) {                             // slab coords -> screen [x, y, scale]
    const X = x * HALF, Z = z * DEPTH;
    const Xr = X * Math.cos(TH) - Z * Math.sin(TH), Zr = X * Math.sin(TH) + Z * Math.cos(TH);
    const p = F / (F + Zr);
    return [CX + Xr * p, V0 + v * VH + Zr * .22, p];
  }
  const sprites = {};
  function sprite(col) {
    if (sprites[col]) return sprites[col];
    const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
    const gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, '#ffffff'); gr.addColorStop(.18, col); gr.addColorStop(1, 'rgba(0,0,0,0)');
    x.fillStyle = gr; x.fillRect(0, 0, 64, 64); return (sprites[col] = c);
  }
  const nodes = [], links = [];
  const node = (x, v, z, r, col, a) => (nodes.push({ x, v, z, r, col, a }), nodes.length - 1);
  const link = (i, j, col, a, w = 1.4) => links.push({ i, j, col, a, w });
  const band = (v, a, b, f = .035) => Math.max(0, Math.min(1, (v - a) / f, (b - v) / f));

  // 1 substrate: formless points
  for (let i = 0; i < 1300; i++) { const v = Math.pow(rnd(), .8) * .2;
    node(rnd() * 2 - 1, v, rnd() * 2 - 1, .8 + rnd() * 1.6, '#a78bff', (.25 + rnd() * .6) * band(v, -.1, .2)); }
  // 2 crystallization: points settle onto a lattice
  { const S = .16, idx = {};
    for (let v = .17; v <= .33; v += .028) for (let x = -1; x <= 1.001; x += S) for (let z = -1; z <= 1.001; z += S) {
      const t = (v - .17) / .16, j = (1 - t) * .07;
      idx[[v.toFixed(3), x.toFixed(2), z.toFixed(2)]] = node(x + (rnd() - .5) * j, v + (rnd() - .5) * j * .3, z + (rnd() - .5) * j, 1.2 + t * 1.6, '#5b8cff', (.35 + .6 * t) * band(v, .17, .335, .025));
    }
    Object.entries(idx).forEach(([k, i]) => { const [v, x, z] = k.split(',').map(Number);
      const t = (v - .17) / .16; if (t < .35) return;
      [[v, x + S, z], [v, x, z + S], [v + .028, x, z]].forEach(([a, b, c]) => { const j = idx[[a.toFixed(3), b.toFixed(2), c.toFixed(2)]];
        if (j !== undefined) link(i, j, '#5b8cff', .32 * t); }); });
  }
  // 3 spacetime emerges: a sheet bent by a mass
  const sheet = (v0, col, a, fn) => { const N = 26, id = [];
    for (let i = 0; i <= N; i++) { id[i] = []; for (let k = 0; k <= N; k++) { const x = -1 + 2 * i / N, z = -1 + 2 * k / N;
      id[i][k] = node(x, v0 + fn(x, z), z, 1.6, col, a * .9); } }
    for (let i = 0; i <= N; i++) for (let k = 0; k <= N; k++) { if (i < N) link(id[i][k], id[i + 1][k], col, a * .55); if (k < N) link(id[i][k], id[i][k + 1], col, a * .55); } };
  sheet(.41, '#45c8ff', .9, (x, z) => .085 * Math.exp(-((x - .25) ** 2 + (z + .1) ** 2) / .09));
  // 4 quantum fields: a sheet rippling from two sources
  sheet(.535, '#3ff0d8', .85, (x, z) => .012 * (Math.cos(Math.hypot(x + .55, z) * 22) + Math.cos(Math.hypot(x - .55, z) * 22)));
  // 5 particles and forces: clean curved tracks, each with a bright head
  for (let i = 0; i < 22; i++) {
    let x = rnd() * 1.6 - .8, v = .615 + rnd() * .06, z = rnd() * 1.6 - .8, a = rnd() * 6.28;
    const c = (rnd() < .5 ? -1 : 1) * (.05 + rnd() * .08), col = rnd() < .5 ? '#c8fff0' : '#9fe8ff';
    let st = .04, prev = null;
    for (let k = 0; k < 34; k++) { x += Math.cos(a) * st; z += Math.sin(a) * st; a += c * (1 + k * .06); st *= .985;
      const n = node(x, v, z, k === 33 ? 5 : .6, col, k === 33 ? 1 : .2 + .6 * k / 33); if (prev !== null) link(prev, n, col, .25 + .6 * k / 33, 2.2); prev = n; }
  }
  // 6 stars and renewal: stars, and a galaxy turning in the slab
  for (let i = 0; i < 380; i++) { const v = .71 + rnd() * .11;
    node(rnd() * 2 - 1, v, rnd() * 2 - 1, .8 + Math.pow(rnd(), 3) * 7, rnd() < .7 ? '#ffd9a0' : '#ffffff', .4 + rnd() * .6); }
  for (let arm = 0; arm < 3; arm++) for (let i = 0; i < 700; i++) {
    const t = i / 700, th = t * 7 + arm * 2.09, rad = .04 + t * .55, sc = (1 - t) * .05 + .02;
    node(.15 + Math.cos(th) * rad + (rnd() - .5) * sc, .765 + (rnd() - .5) * .012, Math.sin(th) * rad + (rnd() - .5) * sc,
      .7 + rnd() * 1.6, rnd() < .6 ? '#ffb45a' : '#fff1d6', .35 + (1 - t) * .5);
  }
  node(.15, .765, 0, 26, '#ffd27a', 1);
  // 7 consciousness: a web of filaments, like the cosmic web and like neurons
  { const ids = [];
    for (let i = 0; i < 420; i++) { const hub = rnd() < .08;
      ids.push(node(rnd() * 2 - 1, .83 + rnd() * .17, rnd() * 2 - 1, hub ? 6 + rnd() * 6 : 1.4 + rnd() * 2, hub ? '#ffe28a' : (rnd() < .5 ? '#ff5fd2' : '#a78bff'), hub ? 1 : .8)); }
    ids.forEach(i => { const a = nodes[i];
      ids.map(j => [j, Math.hypot(a.x - nodes[j].x, (a.v - nodes[j].v) * 9, a.z - nodes[j].z)]).filter(e => e[0] !== i)
        .sort((p, q) => p[1] - q[1]).slice(0, 3).forEach(([j, d]) => { if (d < .42) link(i, j, rnd() < .5 ? '#ff5fd2' : '#a78bff', .5 * (1 - d / .42) + .12, 1.8); }); });
  }

  // draw: links, then nodes, as added light, far things first
  const proj = nodes.map(n => P(n.x, n.v, n.z));
  g.globalCompositeOperation = 'lighter';
  links.forEach(l => { const [x1, y1, p1] = proj[l.i], [x2, y2, p2] = proj[l.j];
    g.strokeStyle = l.col; g.globalAlpha = Math.min(1, l.a * (p1 + p2) / 2); g.lineWidth = l.w * (p1 + p2) / 2;
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); });
  nodes.map((n, i) => [n, proj[i]]).sort((a, b) => a[1][2] - b[1][2]).forEach(([n, [x, y, p]]) => {
    if (n.a <= 0) return; const s = n.r * p * 7;
    g.globalAlpha = Math.min(1, n.a); g.drawImage(sprite(n.col), x - s / 2, y - s / 2, s, s); });
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';

  // leader lines from each card into its stage of the structure
  const VSTAGE = [.11, .26, .41, .535, .645, .765, .9];
  const svg = document.getElementById('leaders'); let out = '';
  document.querySelectorAll('.c6').forEach(card => {
    const i = +card.dataset.i, r = card.getBoundingClientRect();
    const col = getComputedStyle(card).getPropertyValue('--c').trim();
    const x1 = r.right, y1 = r.top + 46;
    const [tx, ty] = P(-.35, VSTAGE[i], .2);
    const ex = Math.max(x1 + 120, tx), ey = ty;
    out += `<path d="M${x1},${y1} H${x1 + 60} L${ex},${ey}" fill="none" stroke="${col}" stroke-width="3" opacity=".85"/>` +
           `<circle cx="${ex}" cy="${ey}" r="11" fill="none" stroke="${col}" stroke-width="3"/><circle cx="${ex}" cy="${ey}" r="4" fill="${col}"/>`;
  });
  svg.innerHTML = out;
})();
