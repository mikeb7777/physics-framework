// Poster v7: the origin sequence as one glowing 3D structure down the right of the poster.
// Each stage occupies one seventh of the structure, and its text sits level with it on the
// left, joined by a short line. The substrate's points also rise faintly behind the headline.
// Points and links live in a slab (x across, v down, z into the page), are turned and
// projected with perspective, and drawn as added light.
(function () {
  const W = 2328, H = 3480, K = 2, N = 7;
  const cv = document.getElementById('art'), g = cv.getContext('2d');
  g.scale(K, K);
  g.fillStyle = '#04060d'; g.fillRect(0, 0, W, H);
  [[1660, 1700, 950, 'rgba(70,60,190,.20)'], [1700, 2350, 760, 'rgba(160,40,150,.15)'], [1600, 650, 800, 'rgba(40,90,200,.12)']]
    .forEach(([x, y, r, c]) => { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, c); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H); });

  let sd = 7; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const V0 = 1225, VH = 1360;                      // stages run from poster y 1225 to 2585
  const CX = 1690, HALF = 540, DEPTH = 400, TH = -.55, F = 2000, TILT = .16;
  const mid = i => (i + .5) / N, lo = i => i / N, hi = i => (i + 1) / N;
  function P(x, v, z) {
    const X = x * HALF, Z = z * DEPTH;
    const Xr = X * Math.cos(TH) - Z * Math.sin(TH), Zr = X * Math.sin(TH) + Z * Math.cos(TH);
    const p = F / (F + Zr);
    return [CX + Xr * p, V0 + v * VH + Zr * TILT, p];
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

  // 1 substrate: formless points, rising faintly up behind the headline
  for (let i = 0; i < 1700; i++) { const v = -0.72 + Math.pow(rnd(), .7) * (hi(0) + .72);
    const a = v < 0 ? .12 + .5 * (1 + v / .72) : .8;
    node(rnd() * 2 - 1, v, rnd() * 2 - 1, .8 + rnd() * 1.6, '#a78bff', (.25 + rnd() * .6) * a); }
  // 2 crystallization: points settle onto a lattice
  { const S = .16, idx = {}, A = lo(1) + .012, B = hi(1) - .012, DV = (B - A) / 5;
    for (let L = 0; L <= 5; L++) { const v = A + L * DV, t = L / 5, j = (1 - t) * .07;
      for (let x = -1; x <= 1.001; x += S) for (let z = -1; z <= 1.001; z += S)
        idx[[L, x.toFixed(2), z.toFixed(2)]] = node(x + (rnd() - .5) * j, v, z + (rnd() - .5) * j, 1.2 + t * 1.6, '#5b8cff', .4 + .55 * t); }
    Object.entries(idx).forEach(([k, i]) => { const [L, x, z] = k.split(',').map(Number); const t = L / 5; if (t < .35) return;
      [[L, x + S, z], [L, x, z + S], [L + 1, x, z]].forEach(([a, b, c]) => { const j = idx[[a, b.toFixed(2), c.toFixed(2)]];
        if (j !== undefined) link(i, j, '#5b8cff', .34 * t); }); });
  }
  // a square sheet of linked points, shaped by fn
  const sheet = (v0, col, a, fn) => { const M = 26, id = [];
    for (let i = 0; i <= M; i++) { id[i] = []; for (let k = 0; k <= M; k++) { const x = -1 + 2 * i / M, z = -1 + 2 * k / M;
      id[i][k] = node(x, v0 + fn(x, z), z, 1.6, col, a * .9); } }
    for (let i = 0; i <= M; i++) for (let k = 0; k <= M; k++) { if (i < M) link(id[i][k], id[i + 1][k], col, a * .55); if (k < M) link(id[i][k], id[i][k + 1], col, a * .55); } };
  // 3 spacetime emerges: a sheet bent by a mass
  sheet(mid(2) - .02, '#45c8ff', .9, (x, z) => .055 * Math.exp(-((x - .25) ** 2 + (z + .1) ** 2) / .09));
  // 4 quantum fields: a sheet rippling from two sources
  sheet(mid(3), '#3ff0d8', .85, (x, z) => .008 * (Math.cos(Math.hypot(x + .55, z) * 22) + Math.cos(Math.hypot(x - .55, z) * 22)));
  // 5 particles and forces: clean curved tracks, each with a bright head
  for (let i = 0; i < 22; i++) {
    let x = rnd() * 1.6 - .8, v = mid(4) - .03 + rnd() * .06, z = rnd() * 1.6 - .8, a = rnd() * 6.28;
    const c = (rnd() < .5 ? -1 : 1) * (.05 + rnd() * .08), col = rnd() < .5 ? '#c8fff0' : '#9fe8ff';
    let st = .04, prev = null;
    for (let k = 0; k < 34; k++) { x += Math.cos(a) * st; z += Math.sin(a) * st; a += c * (1 + k * .06); st *= .985;
      const n = node(x, v, z, k === 33 ? 5 : .6, col, k === 33 ? 1 : .2 + .6 * k / 33); if (prev !== null) link(prev, n, col, .25 + .6 * k / 33, 2.2); prev = n; }
  }
  // 6 stars and renewal: stars, and a galaxy turning in the slab
  for (let i = 0; i < 340; i++) node(rnd() * 2 - 1, lo(5) + .01 + rnd() * (1 / N - .02), rnd() * 2 - 1,
    .8 + Math.pow(rnd(), 3) * 7, rnd() < .7 ? '#ffd9a0' : '#ffffff', .4 + rnd() * .6);
  for (let arm = 0; arm < 3; arm++) for (let i = 0; i < 700; i++) {
    const t = i / 700, th = t * 7 + arm * 2.09, rad = .04 + t * .55, sc = (1 - t) * .05 + .02;
    node(.15 + Math.cos(th) * rad + (rnd() - .5) * sc, mid(5) + (rnd() - .5) * .01, Math.sin(th) * rad + (rnd() - .5) * sc,
      .7 + rnd() * 1.6, rnd() < .6 ? '#ffb45a' : '#fff1d6', .35 + (1 - t) * .5);
  }
  node(.15, mid(5), 0, 26, '#ffd27a', 1);
  // 7 consciousness: a web of filaments, like the cosmic web and like neurons
  { const ids = [];
    for (let i = 0; i < 380; i++) { const hub = rnd() < .08;
      ids.push(node(rnd() * 2 - 1, lo(6) + .01 + rnd() * (1 / N - .03), rnd() * 2 - 1, hub ? 6 + rnd() * 6 : 1.4 + rnd() * 2, hub ? '#ffe28a' : (rnd() < .5 ? '#ff5fd2' : '#a78bff'), hub ? 1 : .8)); }
    ids.forEach(i => { const a = nodes[i];
      ids.map(j => [j, Math.hypot(a.x - nodes[j].x, (a.v - nodes[j].v) * 9, a.z - nodes[j].z)]).filter(e => e[0] !== i)
        .sort((p, q) => p[1] - q[1]).slice(0, 3).forEach(([j, d]) => { if (d < .42) link(i, j, rnd() < .5 ? '#ff5fd2' : '#a78bff', .5 * (1 - d / .42) + .12, 1.8); }); });
  }

  const proj = nodes.map(n => P(n.x, n.v, n.z));
  g.globalCompositeOperation = 'lighter';
  links.forEach(l => { const [x1, y1, p1] = proj[l.i], [x2, y2, p2] = proj[l.j];
    g.strokeStyle = l.col; g.globalAlpha = Math.min(1, l.a * (p1 + p2) / 2); g.lineWidth = l.w * (p1 + p2) / 2;
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); });
  nodes.map((n, i) => [n, proj[i]]).sort((a, b) => a[1][2] - b[1][2]).forEach(([n, [x, y, p]]) => {
    if (n.a <= 0) return; const s = n.r * p * 7;
    g.globalAlpha = Math.min(1, n.a); g.drawImage(sprite(n.col), x - s / 2, y - s / 2, s, s); });
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';

  // place each stage's text level with its stage, and join them with a short line
  const wrap = document.querySelector('.wrap'), off = wrap.getBoundingClientRect();
  const svg = document.getElementById('leaders'); let out = '';
  document.querySelectorAll('.st').forEach(el => {
    const i = +el.dataset.i, v = mid(i);
    const yc = V0 + v * VH;                          // stage centre on the poster
    el.style.top = (yc - 34 - off.top) + 'px';       // stage name sits on that line
    let left = Infinity;                             // nearest edge of the structure at this height
    for (const x of [-1, 1]) for (const z of [-1, 1]) left = Math.min(left, P(x, v, z)[0]);
    const col = getComputedStyle(el).getPropertyValue('--c').trim();
    const rg = document.createRange(); rg.selectNodeContents(el.querySelector('h3'));
    const x1 = rg.getBoundingClientRect().right + 30, x2 = Math.max(x1 + 80, left + 60);
    out += `<line x1="${x1}" y1="${yc - 6}" x2="${x2}" y2="${yc - 6}" stroke="${col}" stroke-width="2.5" opacity=".75"/>` +
           `<circle cx="${x2}" cy="${yc - 6}" r="7" fill="${col}"/>`;
  });
  svg.innerHTML = out;
})();
