/* Sphere Chamber Mode Atlas: the acoustics model.

   A rigid-walled sphere of radius a, driven by point sources on its wall.
   Lengths are in units of a, so each mode is fixed by x = k·a and rings at
   f = x·c / (2π·a). Pressure modes are j_l(x r)·Y_lm(θ, φ) with j_l'(x) = 0
   at the wall, plus the uniform compression mode (x = 0).

   Driven response (modal sum with loss 1/Q):
     p(r) = Σ_n ψ_n(r) · Σ_i q_i ψ_n(s_i) / ( Λ_n · (x_n² − X² + i·x_n·X/Q) )

   Particles follow the Gor'kov radiation potential, constant factors dropped:
     U ∝ f1·|p|² − (3/2)·f2·|∇p|² / X²
   and gather at its minima. Everything here is standard linear acoustics. */
(function (root) {
  'use strict';

  const L_MAX = 8;          // highest angular order kept
  const X_MAX = 16;         // highest k·a kept
  const R_MAX = 1.25;       // radial tables run a little past the wall for gradients
  const NR = 1281;          // radial table samples (r = 1 falls on index 1024)
  const NY = (L_MAX + 1) * (L_MAX + 1);

  // ── spherical Bessel functions j_0 … j_{L+1} at x ──
  function sphj(L, x) {
    const n = Math.max(L, 1);
    const out = new Float64Array(n + 2);
    if (x < 1e-8) { out[0] = 1; return out; }
    const s = Math.sin(x), c = Math.cos(x);
    const j0 = s / x, j1 = s / (x * x) - c / x;
    if (x > n + 1) {                       // upward recurrence is stable here
      out[0] = j0; out[1] = j1;
      for (let l = 1; l <= n; l++) out[l + 1] = (2 * l + 1) / x * out[l] - out[l - 1];
      return out;
    }
    const start = n + 26 + Math.ceil(x);   // Miller's downward recurrence
    let jp = 0, jc = 1e-30;
    for (let l = start; l >= 1; l--) {
      const jm = (2 * l + 1) / x * jc - jp;
      jp = jc; jc = jm;
      if (l - 1 <= n + 1) out[l - 1] = jc;
      if (Math.abs(jc) > 1e200) {
        jc *= 1e-200; jp *= 1e-200;
        for (let i = Math.max(l - 1, 0); i <= n + 1; i++) out[i] *= 1e-200;
      }
    }
    const scale = Math.abs(j0) > Math.abs(j1) ? j0 / out[0] : j1 / out[1];
    for (let i = 0; i < out.length; i++) out[i] *= scale;
    return out;
  }
  const jl = (l, x) => sphj(l, x)[l];
  function djl(l, x) {
    if (x < 1e-8) return l === 1 ? 1 / 3 : 0;
    const a = sphj(l, x);
    return (l / x) * a[l] - a[l + 1];
  }

  // zeros of j_l' in (0, X_MAX]: the rigid-wall resonances of order l
  function dRoots(l) {
    const roots = [], h = 0.01;
    let x0 = 0.02, g0 = djl(l, x0);
    for (let x1 = x0 + h; x1 <= X_MAX; x1 += h) {
      const g1 = djl(l, x1);
      if (g0 * g1 < 0) {
        let lo = x0, hi = x1, glo = g0;
        for (let i = 0; i < 60; i++) {
          const mid = (lo + hi) / 2, gm = djl(l, mid);
          if (glo * gm <= 0) hi = mid; else { lo = mid; glo = gm; }
        }
        roots.push((lo + hi) / 2);
      }
      x0 = x1; g0 = g1;
    }
    return roots;
  }

  // ── real spherical harmonics, orthonormal on the sphere, index l² + l + m ──
  const K = new Float64Array(NY);
  (function () {
    const fact = n => { let f = 1; for (let i = 2; i <= n; i++) f *= i; return f; };
    for (let l = 0; l <= L_MAX; l++)
      for (let m = 0; m <= l; m++)
        K[l * l + l + m] = Math.sqrt((2 * l + 1) / (4 * Math.PI) * fact(l - m) / fact(l + m));
  })();
  function ylm(ct, phi, out) {
    const st = Math.sqrt(Math.max(0, 1 - ct * ct));
    let pmm = 1;
    for (let m = 0; m <= L_MAX; m++) {
      if (m > 0) pmm *= (2 * m - 1) * st;
      const cm = Math.cos(m * phi), sm = Math.sin(m * phi);
      let pl2 = 0, pl1 = 0;
      for (let l = m; l <= L_MAX; l++) {
        let p;
        if (l === m) p = pmm;
        else if (l === m + 1) p = ct * (2 * m + 1) * pmm;
        else p = ((2 * l - 1) * ct * pl1 - (l + m - 1) * pl2) / (l - m);
        pl2 = pl1; pl1 = p;
        const base = l * l + l;
        if (m === 0) out[base] = K[base] * p;
        else {
          const v = Math.SQRT2 * K[base + m] * p;
          out[base + m] = v * cm;
          out[base - m] = v * sm;
        }
      }
    }
    return out;
  }
  function ylmAt(v) {
    const r = Math.hypot(v[0], v[1], v[2]);
    return ylm(v[2] / r, Math.atan2(v[1], v[0]), new Float64Array(NY));
  }

  // ── radial families (l, n): resonance x, norm Λ, wall value, radial table ──
  const GROUPS = [];
  (function () {
    const kWall = Math.round((NR - 1) / R_MAX);
    GROUPS.push({ l: 0, n: 0, x: 0, lam: 1 / 3, wall: 1, R: new Float32Array(NR).fill(1) });
    for (let l = 0; l <= L_MAX; l++) {
      dRoots(l).forEach((x, i) => {
        const R = new Float32Array(NR);
        for (let k = 0; k < NR; k++) R[k] = jl(l, x * k * R_MAX / (NR - 1));
        const dr = 1 / kWall;
        let s = 0;
        for (let k = 0; k <= kWall; k++) {
          const r = k * dr, v = R[k] * R[k] * r * r;
          s += (k === 0 || k === kWall ? 1 : (k % 2 ? 4 : 2)) * v;
        }
        GROUPS.push({ l, n: i + 1, x, lam: s * dr / 3, wall: jl(l, x), R });
      });
    }
  })();
  const groupIndex = (l, n) => GROUPS.findIndex(g => g.l === l && g.n === n);
  const modeX = (l, n) => { const i = groupIndex(l, n); return i < 0 ? NaN : GROUPS[i].x; };

  // four transducers at the vertices of a regular tetrahedron, one straight up
  const TETRA = [
    [0, 0, 1],
    [2 * Math.SQRT2 / 3, 0, -1 / 3],
    [-Math.SQRT2 / 3, Math.sqrt(2 / 3), -1 / 3],
    [-Math.SQRT2 / 3, -Math.sqrt(2 / 3), -1 / 3],
  ];
  const TETRA_Y = TETRA.map(ylmAt);

  // Σ_i q_i Y_lm(s_i) for every (l, m); q_i = {re, im}
  function sourceSums(q, sy) {
    const cre = new Float64Array(NY), cim = new Float64Array(NY);
    q.forEach((qi, i) => {
      for (let k = 0; k < NY; k++) { cre[k] += qi.re * sy[i][k]; cim[k] += qi.im * sy[i][k]; }
    });
    return { cre, cim };
  }

  // how strongly a drive pattern feeds each radial family, independent of frequency
  function coupling(q, sy = TETRA_Y) {
    const { cre, cim } = sourceSums(q, sy);
    return GROUPS.map(g => {
      let s = 0;
      for (let m = -g.l; m <= g.l; m++) { const k = g.l * g.l + g.l + m; s += cre[k] * cre[k] + cim[k] * cim[k]; }
      return s * g.wall * g.wall / g.lam;
    });
  }

  function coefficients(X, Q, q, sy) {
    const { cre, cim } = sourceSums(q, sy);
    const list = [];
    let maxMag = 0;
    GROUPS.forEach((g, gi) => {
      const dRe = g.lam * (g.x * g.x - X * X), dIm = g.lam * g.x * X / Q, d2 = dRe * dRe + dIm * dIm;
      for (let m = -g.l; m <= g.l; m++) {
        const k = g.l * g.l + g.l + m;
        const nr = cre[k] * g.wall, ni = cim[k] * g.wall;
        if (nr === 0 && ni === 0) continue;
        const aRe = (nr * dRe + ni * dIm) / d2, aIm = (ni * dRe - nr * dIm) / d2;
        const mag = aRe * aRe + aIm * aIm;
        if (mag > maxMag) maxMag = mag;
        list.push({ gi, k, aRe, aIm, mag });
      }
    });
    return list.filter(c => c.mag > 1e-7 * maxMag);
  }

  // ── the field on an N³ grid over the cube around the sphere ──
  function field(opts) {
    const { X, Q, q, f1, f2 } = opts;
    const N = opts.N || 48, sy = opts.sy || TETRA_Y;
    const coeffs = coefficients(X, Q, q, sy);
    const byG = new Map();
    coeffs.forEach(c => { if (!byG.has(c.gi)) byG.set(c.gi, []); byG.get(c.gi).push(c); });
    const fams = [...byG.entries()].map(([gi, cs]) => ({
      R: GROUPS[gi].R, k: Int32Array.from(cs.map(c => c.k)),
      aRe: Float64Array.from(cs.map(c => c.aRe)), aIm: Float64Array.from(cs.map(c => c.aIm)),
    }));

    const h = 2 / (N - 1), N2 = N * N, N3 = N2 * N;
    const pRe = new Float32Array(N3), pIm = new Float32Array(N3), ok = new Uint8Array(N3);
    const Y = new Float64Array(NY), lim = 1 + 2.5 * h, tScale = (NR - 1) / R_MAX;
    for (let kz = 0; kz < N; kz++) {
      const z = -1 + kz * h;
      for (let jy = 0; jy < N; jy++) {
        const y = -1 + jy * h;
        for (let ix = 0; ix < N; ix++) {
          const x = -1 + ix * h, r = Math.sqrt(x * x + y * y + z * z);
          if (r > lim) continue;
          const id = ix + N * jy + N2 * kz;
          ylm(r > 1e-9 ? z / r : 1, Math.atan2(y, x), Y);
          const t = r * tScale, t0 = t | 0, fr = t - t0;
          let re = 0, im = 0;
          for (const F of fams) {
            const rv = F.R[t0] + (F.R[t0 + 1] - F.R[t0]) * fr;
            for (let e = 0; e < F.k.length; e++) {
              const v = rv * Y[F.k[e]];
              re += F.aRe[e] * v; im += F.aIm[e] * v;
            }
          }
          pRe[id] = re; pIm[id] = im; ok[id] = 1;
        }
      }
    }

    const U = new Float32Array(N3), uok = new Uint8Array(N3);
    const absP = new Float32Array(N3), inside = new Uint8Array(N3);
    const inv2h = 1 / (2 * h), X2 = X * X;
    let maxAbsP = 0;
    for (let kz = 1; kz < N - 1; kz++) for (let jy = 1; jy < N - 1; jy++) for (let ix = 1; ix < N - 1; ix++) {
      const id = ix + N * jy + N2 * kz;
      if (!(ok[id] && ok[id + 1] && ok[id - 1] && ok[id + N] && ok[id - N] && ok[id + N2] && ok[id - N2])) continue;
      const gxr = (pRe[id + 1] - pRe[id - 1]) * inv2h, gxi = (pIm[id + 1] - pIm[id - 1]) * inv2h;
      const gyr = (pRe[id + N] - pRe[id - N]) * inv2h, gyi = (pIm[id + N] - pIm[id - N]) * inv2h;
      const gzr = (pRe[id + N2] - pRe[id - N2]) * inv2h, gzi = (pIm[id + N2] - pIm[id - N2]) * inv2h;
      const g2 = gxr * gxr + gxi * gxi + gyr * gyr + gyi * gyi + gzr * gzr + gzi * gzi;
      const p2 = pRe[id] * pRe[id] + pIm[id] * pIm[id];
      U[id] = f1 * p2 - 1.5 * f2 * g2 / X2; uok[id] = 1;
      const x = -1 + ix * h, y = -1 + jy * h, z = -1 + kz * h;
      if (x * x + y * y + z * z <= 1) {
        inside[id] = 1; absP[id] = Math.sqrt(p2);
        if (absP[id] > maxAbsP) maxAbsP = absP[id];
      }
    }

    const Fx = new Float32Array(N3), Fy = new Float32Array(N3), Fz = new Float32Array(N3);
    const mags = [];
    for (let kz = 1; kz < N - 1; kz++) for (let jy = 1; jy < N - 1; jy++) for (let ix = 1; ix < N - 1; ix++) {
      const id = ix + N * jy + N2 * kz;
      if (!(uok[id + 1] && uok[id - 1] && uok[id + N] && uok[id - N] && uok[id + N2] && uok[id - N2])) continue;
      Fx[id] = -(U[id + 1] - U[id - 1]) * inv2h;
      Fy[id] = -(U[id + N] - U[id - N]) * inv2h;
      Fz[id] = -(U[id + N2] - U[id - N2]) * inv2h;
      if (inside[id]) mags.push(Math.hypot(Fx[id], Fy[id], Fz[id]));
    }
    mags.sort((a, b) => a - b);
    const maxF = mags.length ? mags[Math.floor(mags.length * 0.99)] : 0;

    // share of field energy carried by each radial family
    const energy = new Map();
    coeffs.forEach(c => energy.set(c.gi, (energy.get(c.gi) || 0) + c.mag * GROUPS[c.gi].lam));
    let total = 0; energy.forEach(v => { total += v; });
    const shares = [...energy.entries()]
      .map(([gi, e]) => ({ l: GROUPS[gi].l, n: GROUPS[gi].n, x: GROUPS[gi].x, share: total > 0 ? e / total : 0 }))
      .sort((a, b) => b.share - a.share);

    return { N, h, absP, inside, Fx, Fy, Fz, maxAbsP, maxF, shares };
  }

  // trilinear force at a point (grid units in, same units out)
  function sampleForce(F, x, y, z, out) {
    const N = F.N, N2 = N * N, lim = N - 1.0001;
    let gx = (x + 1) / F.h, gy = (y + 1) / F.h, gz = (z + 1) / F.h;
    gx = gx < 0 ? 0 : gx > lim ? lim : gx;
    gy = gy < 0 ? 0 : gy > lim ? lim : gy;
    gz = gz < 0 ? 0 : gz > lim ? lim : gz;
    const i = gx | 0, j = gy | 0, k = gz | 0, u = gx - i, v = gy - j, w = gz - k;
    const w000 = (1 - u) * (1 - v) * (1 - w), w100 = u * (1 - v) * (1 - w), w010 = (1 - u) * v * (1 - w), w110 = u * v * (1 - w);
    const w001 = (1 - u) * (1 - v) * w, w101 = u * (1 - v) * w, w011 = (1 - u) * v * w, w111 = u * v * w;
    const a = i + N * j + N2 * k;
    const idx = [a, a + 1, a + N, a + N + 1, a + N2, a + N2 + 1, a + N2 + N, a + N2 + N + 1];
    const wt = [w000, w100, w010, w110, w001, w101, w011, w111];
    let fx = 0, fy = 0, fz = 0;
    for (let c = 0; c < 8; c++) { fx += wt[c] * F.Fx[idx[c]]; fy += wt[c] * F.Fy[idx[c]]; fz += wt[c] * F.Fz[idx[c]]; }
    out[0] = fx; out[1] = fy; out[2] = fz;
    return out;
  }

  // grid points inside the sphere where |p| is near zero: the pressure nodal surfaces
  function nodePoints(F, threshold, maxCount) {
    const N = F.N, N2 = N * N, cut = threshold * F.maxAbsP, hits = [];
    for (let id = 0; id < F.absP.length; id++) if (F.inside[id] && F.absP[id] < cut) hits.push(id);
    const stride = Math.max(1, Math.ceil(hits.length / maxCount));
    const out = new Float32Array(Math.ceil(hits.length / stride) * 3);
    let o = 0;
    for (let n = 0; n < hits.length; n += stride) {
      const id = hits[n], kz = Math.floor(id / N2), jy = Math.floor((id - kz * N2) / N), ix = id - kz * N2 - jy * N;
      out[o++] = -1 + (ix + Math.random() - 0.5) * F.h;
      out[o++] = -1 + (jy + Math.random() - 0.5) * F.h;
      out[o++] = -1 + (kz + Math.random() - 0.5) * F.h;
    }
    return out.subarray(0, o);
  }

  // ── media and the radiation force budget ──
  const FLUIDS = {
    air: { name: 'air', rho: 1.204, c: 343, eta: 1.81e-5 },
    water: { name: 'water', rho: 997, c: 1482, eta: 8.9e-4 },
  };
  Object.values(FLUIDS).forEach(f => { f.kappa = 1 / (f.rho * f.c * f.c); });

  function particleProps(kind, R, fluid) {
    const fl = FLUIDS[fluid];
    if (kind === 'water') return { rho: 998, kappa: 4.48e-10 };
    if (kind === 'polystyrene') return { rho: 1050, kappa: 2.49e-10 };
    if (kind === 'soapBubble') return { rho: fl.rho + 3 * 5e-7 * 998 / R, kappa: fl.kappa };   // 500 nm film, gas inside
    throw new Error('unknown particle ' + kind);
  }
  function contrast(fluid, pp) {
    const fl = FLUIDS[fluid];
    const f1 = 1 - pp.kappa / fl.kappa;
    const f2 = 2 * (pp.rho - fl.rho) / (2 * pp.rho + fl.rho);
    return { f1, f2, phi: f1 + 1.5 * f2 };
  }
  // one-dimensional standing wave p = p0·cos(kx): F_max = |Φ|·V·k·p0² / (4ρc²)
  function forceBudget({ fluid, particle, R, f, p0 }) {
    const fl = FLUIDS[fluid], pp = particleProps(particle, R, fluid), con = contrast(fluid, pp);
    const k = 2 * Math.PI * f / fl.c, V = 4 / 3 * Math.PI * R ** 3, rc2 = fl.rho * fl.c * fl.c;
    const Fmax = Math.abs(con.phi) * V * k * p0 * p0 / (4 * rc2);
    const W = Math.abs(pp.rho - fl.rho) * V * 9.81;
    const pHold = Math.sqrt(4 * rc2 * Math.abs(pp.rho - fl.rho) * 9.81 / (Math.abs(con.phi) * k));
    const ref = fluid === 'air' ? 20e-6 : 1e-6;
    const spl = p => 20 * Math.log10((p / Math.SQRT2) / ref);
    const v = Fmax / (6 * Math.PI * fl.eta * R);
    const Re = fl.rho * v * 2 * R / fl.eta;
    const lambda = fl.c / f;
    return { ...con, pp, k, V, Fmax, W, ratio: W / Fmax, pHold, splHold: spl(pHold), splRef: fluid === 'air' ? '20 µPa' : '1 µPa', v, Re, lambda, tQuarter: lambda / 4 / v };
  }

  root.SphereModel = {
    L_MAX, X_MAX, GROUPS, TETRA, groupIndex, modeX, jl, djl,
    coupling, field, sampleForce, nodePoints,
    FLUIDS, particleProps, contrast, forceBudget,
  };
})(typeof window !== 'undefined' ? window : globalThis);
