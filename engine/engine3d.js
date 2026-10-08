// engine3d.js — unit cubes in a cube (3D), same paths as engine2d.js: piece(γ, τ) = γ·[(1-τ)·cube ⊕ τ·½·ball].
// Adapted from soft-to-rigid-packing/src/cubes/sim3.js (n = 12 record). Original header:
// Soft→rigid CUBE packer (3D). Shape: rounded cube = cube of half-side s = 0.5 - r dilated by r.
//   r = 0.5 → unit-diameter ball; r = 0 → rigid unit cube. Every intermediate fits inside the unit cube.
// Energy: Σ_pairs (2r - sd_core)_+² + Σ wall violations² + μ·L. Orientation = quaternion, analytic gradients.
(function (root) {
  let N = 11;
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function gauss(rng) { let u = 0; while (u === 0) u = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rng()); }

  // ---------- small vector helpers (arrays of length 3) ----------
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const scl = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
  const norm = a => Math.hypot(a[0], a[1], a[2]);

  // quaternion [w,x,y,z] → rotation matrix columns (local axes in world frame)
  function axes(q) {
    const [w, x, y, z] = q;
    return [
      [1 - 2 * (y * y + z * z), 2 * (x * y + w * z), 2 * (x * z - w * y)],
      [2 * (x * y - w * z), 1 - 2 * (x * x + z * z), 2 * (y * z + w * x)],
      [2 * (x * z + w * y), 2 * (y * z - w * x), 1 - 2 * (x * x + y * y)],
    ];
  }
  // q ← exp(ω) q  (world-frame rotation vector ω)
  function rotq(q, wx, wy, wz) {
    const th = Math.hypot(wx, wy, wz);
    if (th < 1e-16) return q;
    const h = th / 2, sh = Math.sin(h) / th;
    const dw = Math.cos(h), dx = wx * sh, dy = wy * sh, dz = wz * sh;
    const [w, x, y, z] = q;
    const r = [dw * w - dx * x - dy * y - dz * z, dw * x + dx * w + dy * z - dz * y, dw * y - dx * z + dy * w + dz * x, dw * z + dx * y - dy * x + dz * w];
    const m = Math.hypot(r[0], r[1], r[2], r[3]);
    return [r[0] / m, r[1] / m, r[2] / m, r[3] / m];
  }

  // ---------- core distance between two boxes (half-side s) with gradient ----------
  // Returns sd (negative = penetration depth from SAT) and fills grad: [dcA(3), dωA(3), dcB(3), dωB(3)].
  const GR = new Float64Array(12);
  function segClosest(p1, q1, p2, q2) {
    // closest points between segments p1q1 and p2q2 (Ericson)
    const d1 = sub(q1, p1), d2 = sub(q2, p2), r = sub(p1, p2);
    const a = dot(d1, d1), e = dot(d2, d2), f = dot(d2, r);
    let s, t;
    const c = dot(d1, r), b = dot(d1, d2), den = a * e - b * b;
    s = den > 1e-14 ? Math.min(1, Math.max(0, (b * f - c * e) / den)) : 0;
    t = (b * s + f) / e;
    if (t < 0) { t = 0; s = Math.min(1, Math.max(0, -c / a)); }
    else if (t > 1) { t = 1; s = Math.min(1, Math.max(0, (b - c) / a)); }
    const c1 = add(p1, scl(d1, s)), c2 = add(p2, scl(d2, t));
    return [c1, c2];
  }
  const SG = [[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1], [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]];
  const EDGES = (() => { const e = []; for (let i = 0; i < 8; i++) for (let j = i + 1; j < 8; j++) { let d = 0; for (let k = 0; k < 3; k++) if (SG[i][k] !== SG[j][k]) d++; if (d === 1) e.push([i, j]); } return e; })();
  function boxVerts(c, A, s) { return SG.map(g => [c[0] + s * (g[0] * A[0][0] + g[1] * A[1][0] + g[2] * A[2][0]), c[1] + s * (g[0] * A[0][1] + g[1] * A[1][1] + g[2] * A[2][1]), c[2] + s * (g[0] * A[0][2] + g[1] * A[1][2] + g[2] * A[2][2])]); }
  function pointBox(p, c, A, s) {
    const d = sub(p, c);
    let q = [c[0], c[1], c[2]];
    for (let k = 0; k < 3; k++) { let t = dot(d, A[k]); t = t < -s ? -s : t > s ? s : t; q = add(q, scl(A[k], t)); }
    return q;
  }
  function sdBoxes(cA, AA, cB, AB, s, cutoff) {
    if (cutoff === undefined) cutoff = Infinity;
    const D = sub(cB, cA);
    if (s <= 1e-12) {
      const d = norm(D) || 1e-300, n = scl(D, -1 / d); // n from B to A
      GR.fill(0); GR[0] = n[0]; GR[1] = n[1]; GR[2] = n[2]; GR[6] = -n[0]; GR[7] = -n[1]; GR[8] = -n[2];
      return norm(D);
    }
    // SAT over 15 axes
    let minO = Infinity, best = null, sep = false;
    const cand = [];
    for (let k = 0; k < 3; k++) cand.push([AA[k], 'A', k, -1], [AB[k], 'B', k, -1]);
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
      const w = cross(AA[i], AB[j]), l = norm(w);
      if (l > 1e-9) cand.push([scl(w, 1 / l), 'X', i, j, w, l]);
    }
    for (const ax of cand) {
      const u = ax[0];
      const rA = s * (Math.abs(dot(u, AA[0])) + Math.abs(dot(u, AA[1])) + Math.abs(dot(u, AA[2])));
      const rB = s * (Math.abs(dot(u, AB[0])) + Math.abs(dot(u, AB[1])) + Math.abs(dot(u, AB[2])));
      const o = rA + rB - Math.abs(dot(u, D));
      if (o < 0) { sep = true; if (-o >= cutoff) return -o; break; }
      if (o < minO) { minO = o; best = ax; }
    }
    if (!sep) {
      // sd = -o ; analytic gradient of o along the minimizing axis
      const [u, kind, i, j, w, l] = best;
      const sig = Math.sign(dot(u, D)) || 1;
      // du = JA ωA + JB ωB, represented by functions applying transposes
      // o = s Σ|u·a_k| + s Σ|u·b_k| - sig u·D
      // do/dcA = sig u ; do/dcB = -sig u
      // do/dωA = Σ s sA_k (a_k × u) + JAᵀ g ; do/dωB = Σ s sB_k (b_k × u) + JBᵀ g, where g = Σ s sA_k a_k + Σ s sB_k b_k - sig D
      let g = scl(D, -sig);
      let tA = [0, 0, 0], tB = [0, 0, 0];
      for (let k = 0; k < 3; k++) {
        const sa = Math.sign(dot(u, AA[k])), sb = Math.sign(dot(u, AB[k]));
        g = add(g, add(scl(AA[k], s * sa), scl(AB[k], s * sb)));
        tA = add(tA, scl(cross(AA[k], u), s * sa));
        tB = add(tB, scl(cross(AB[k], u), s * sb));
      }
      // JᵀA g and JᵀB g
      let JAg = [0, 0, 0], JBg = [0, 0, 0];
      if (kind === 'A') { JAg = cross(AA[i], g); /* du = ωA × a_i  ⇒ g·du = ωA·(a_i × g) */ }
      else if (kind === 'B') { JBg = cross(AB[i], g); }
      else {
        // u = w/|w|, w = a_i × b_j ; du = P dw / l ; dw = (ωA×a_i)×b_j + a_i×(ωB×b_j)
        const a = AA[i], b = AB[j];
        const h = scl(sub(g, scl(u, dot(u, g))), 1 / l); // P g / l
        // h·((ωA×a)×b) = (ωA×a)·(b×h) = ωA·(a×(b×h))
        JAg = cross(a, cross(b, h));
        // h·(a×(ωB×b)) = (ωB×b)·(h×a) = ωB·(b×(h×a))
        JBg = cross(b, cross(h, a));
      }
      const dA = add(tA, JAg), dB = add(tB, JBg);
      // sd = -o
      GR[0] = -sig * u[0]; GR[1] = -sig * u[1]; GR[2] = -sig * u[2];
      GR[3] = -dA[0]; GR[4] = -dA[1]; GR[5] = -dA[2];
      GR[6] = sig * u[0]; GR[7] = sig * u[1]; GR[8] = sig * u[2];
      GR[9] = -dB[0]; GR[10] = -dB[1]; GR[11] = -dB[2];
      return -minO;
    }
    // separated: exact distance via vertex-box and edge-edge features
    const VA = boxVerts(cA, AA, s), VB = boxVerts(cB, AB, s);
    let d2 = Infinity, pA = null, pB = null;
    for (const v of VA) { const q = pointBox(v, cB, AB, s), e = sub(v, q), dd = dot(e, e); if (dd < d2) { d2 = dd; pA = v; pB = q; } }
    for (const v of VB) { const q = pointBox(v, cA, AA, s), e = sub(q, v), dd = dot(e, e); if (dd < d2) { d2 = dd; pA = q; pB = v; } }
    for (const [i1, j1] of EDGES) for (const [i2, j2] of EDGES) {
      const [c1, c2] = segClosest(VA[i1], VA[j1], VB[i2], VB[j2]);
      const e = sub(c1, c2), dd = dot(e, e);
      if (dd < d2) { d2 = dd; pA = c1; pB = c2; }
    }
    const d = Math.sqrt(d2) || 1e-300, n = scl(sub(pA, pB), 1 / d);
    const tA = cross(sub(pA, cA), n), tB = cross(sub(pB, cB), n);
    GR[0] = n[0]; GR[1] = n[1]; GR[2] = n[2]; GR[3] = tA[0]; GR[4] = tA[1]; GR[5] = tA[2];
    GR[6] = -n[0]; GR[7] = -n[1]; GR[8] = -n[2]; GR[9] = -tB[0]; GR[10] = -tB[1]; GR[11] = -tB[2];
    return Math.sqrt(d2);
  }
  // value-only SAT overlap test for certification (true if interiors overlap by more than tol)
  function boxesOverlap(cA, AA, cB, AB, s, tol) {
    const D = sub(cB, cA);
    const axs = [AA[0], AA[1], AA[2], AB[0], AB[1], AB[2]];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) { const w = cross(AA[i], AB[j]), l = norm(w); if (l > 1e-9) axs.push(scl(w, 1 / l)); }
    for (const u of axs) {
      const rA = s * (Math.abs(dot(u, AA[0])) + Math.abs(dot(u, AA[1])) + Math.abs(dot(u, AA[2])));
      const rB = s * (Math.abs(dot(u, AB[0])) + Math.abs(dot(u, AB[1])) + Math.abs(dot(u, AB[2])));
      if (rA + rB - Math.abs(dot(u, D)) <= tol) return false;
    }
    return true;
  }
  // half extent of a rounded cube along world axis e (0,1,2)
  function halfExt(A, e, s, r) { return s * (Math.abs(A[0][e]) + Math.abs(A[1][e]) + Math.abs(A[2][e])) + r; }

  // ---------- state ----------
  function makeState(seed, L0) {
    const rng = mulberry32(seed * 7919 + 13);
    const st = { rng, L: L0, vL: 0, r: 0.5, step: 0, phase: 'init', frames: [], log: [],
      C: [], Q: [], V: [], W: [] };
    for (let i = 0; i < N; i++) {
      st.C.push([0.7 + rng() * (L0 - 1.4), 0.7 + rng() * (L0 - 1.4), 0.7 + rng() * (L0 - 1.4)]);
      let q = [gauss(rng), gauss(rng), gauss(rng), gauss(rng)]; const m = Math.hypot(...q); st.Q.push(q.map(v => v / m));
      st.V.push([0, 0, 0]); st.W.push([0, 0, 0]);
    }
    return st;
  }

  function dyn(st, r, mu, noise, moveL, sOverride) {
    const beta = 0.85, cap = 0.03, lr = 0.04, s = sOverride !== undefined ? sOverride : 0.5 - r;
    const A = st.Q.map(axes);
    const GC = st.C.map(() => [0, 0, 0]), GW = st.C.map(() => [0, 0, 0]);
    const lim = (2 * (s * Math.sqrt(3) + r) + 1e-3) ** 2;
    for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
      const D = sub(st.C[j], st.C[i]); if (dot(D, D) > lim) continue;
      st.evals = (st.evals || 0) + 1;
      const sd = sdBoxes(st.C[i], A[i], st.C[j], A[j], s, 2 * r);
      const o = 2 * r - sd; if (o <= 0) continue;
      const c = -2 * o;
      for (let k = 0; k < 3; k++) { GC[i][k] += c * GR[k]; GW[i][k] += c * GR[3 + k]; GC[j][k] += c * GR[6 + k]; GW[j][k] += c * GR[9 + k]; }
    }
    let gL = mu;
    for (let i = 0; i < N; i++) for (let e = 0; e < 3; e++) {
      const h = halfExt(A[i], e, s, r);
      // dh/dω = s Σ_k sgn(A_k[e]) (a_k × ê)
      const dh = [0, 0, 0];
      for (let k = 0; k < 3; k++) { const sg = Math.sign(A[i][k][e]); const ex = [0, 0, 0]; ex[e] = 1; const cx = cross(A[i][k], ex); dh[0] += s * sg * cx[0]; dh[1] += s * sg * cx[1]; dh[2] += s * sg * cx[2]; }
      let q = h - st.C[i][e];
      if (q > 0) { GC[i][e] -= 2 * q; for (let k = 0; k < 3; k++) GW[i][k] += 2 * q * dh[k]; if (moveL) gL -= 2 * q; }
      q = st.C[i][e] + h - st.L;
      if (q > 0) { GC[i][e] += 2 * q; for (let k = 0; k < 3; k++) GW[i][k] += 2 * q * dh[k]; if (moveL) gL -= 2 * q; }
    }
    for (let i = 0; i < N; i++) {
      const V = st.V[i], W = st.W[i];
      for (let k = 0; k < 3; k++) { V[k] = beta * V[k] - lr * GC[i][k]; W[k] = s <= 1e-9 ? 0 : beta * W[k] - lr * GW[i][k]; }
      const vm = norm(V); if (vm > cap) for (let k = 0; k < 3; k++) V[k] *= cap / vm;
      const wm = norm(W); if (wm > cap) for (let k = 0; k < 3; k++) W[k] *= cap / wm;
      for (let k = 0; k < 3; k++) st.C[i][k] += V[k] + (noise > 0 ? noise * gauss(st.rng) : 0);
      let wx = W[0], wy = W[1], wz = W[2];
      if (noise > 0 && s > 1e-9) { wx += 1.5 * noise * gauss(st.rng); wy += 1.5 * noise * gauss(st.rng); wz += 1.5 * noise * gauss(st.rng); }
      st.Q[i] = rotq(st.Q[i], wx, wy, wz);
    }
    if (moveL) {
      st.vL = beta * st.vL - 0.02 * gL;
      if (Math.abs(st.vL) > cap) st.vL = Math.sign(st.vL) * cap;
      const d = st.vL / 2; for (let i = 0; i < N; i++) for (let k = 0; k < 3; k++) st.C[i][k] += d;
      st.L += st.vL;
    }
    st.r = r; st.step++;
  }

  function snap(st) {
    const f = { ph: st.phase, r: +st.r.toFixed(4), L: +st.L.toFixed(5), s: st.step, p: [] };
    for (let i = 0; i < N; i++) f.p.push(...st.C[i].map(v => +v.toFixed(4)), ...st.Q[i].map(v => +v.toFixed(5)));
    st.frames.push(f);
  }

  // Certified legalization: scale centres apart until no pair of rigid unit cubes overlaps (SAT, tol 1e-12),
  // then measure the tight axis-aligned bounding cube.
  function legalize(C, Q) {
    const A = Q.map(axes);
    const cen = [0, 1, 2].map(k => C.reduce((a, c) => a + c[k], 0) / N);
    const pos = k => C.map(c => [cen[0] + k * (c[0] - cen[0]), cen[1] + k * (c[1] - cen[1]), cen[2] + k * (c[2] - cen[2])]);
    const ok = k => { const P = pos(k); for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) if (boxesOverlap(P[i], A[i], P[j], A[j], 0.5, 1e-12)) return false; return true; };
    let lo = 1, hi = 1;
    if (!ok(1)) { hi = 1.0001; while (!ok(hi)) hi = 1 + (hi - 1) * 2; for (let it = 0; it < 70; it++) { const m = (lo + hi) / 2; if (ok(m)) hi = m; else lo = m; } }
    const P = pos(hi);
    const mn = [Infinity, Infinity, Infinity], mx = [-Infinity, -Infinity, -Infinity];
    for (let i = 0; i < N; i++) for (let e = 0; e < 3; e++) { const h = halfExt(A[i], e, 0.5, 0); mn[e] = Math.min(mn[e], P[i][e] - h); mx[e] = Math.max(mx[e], P[i][e] + h); }
    const side = Math.max(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]);
    const off = [0, 1, 2].map(e => mn[e] - (side - (mx[e] - mn[e])) / 2);
    return { side, k: hi, C: P.map(p => [p[0] - off[0], p[1] - off[1], p[2] - off[2]]), Q: Q.map(q => q.slice()) };
  }

  const PATHS = { harden: { gamma0: 1, tau0: 1 }, grow: { gamma0: 0.35, tau0: 0 }, rigid: { gamma0: 1, tau0: 0 },
    'harden-half': { gamma0: 1, tau0: 0.5 } };
  function run(cfg) {
    const c = Object.assign({ seed: 1, n: 12, method: 'harden', budget: 1, compress: 1667, morph: 15000, settle: 1000, mu: 0.02,
      noise: 0.015, noiseMorph: 0.004, noiseScale: 1, frames: 150 }, cfg);
    const t0 = Date.now();
    N = c.n; const L0 = Math.max(3, 1.8 * Math.cbrt(N) + 0.5);
    const path = Object.assign({}, PATHS[c.method]); if (!PATHS[c.method]) throw new Error('unknown method ' + c.method);
    if (c.gamma0 !== undefined) path.gamma0 = c.gamma0; if (c.tau0 !== undefined) path.tau0 = c.tau0;
    const st = makeState(c.seed, L0); st.evals = 0;
    const nC = Math.round(c.compress * c.budget), nM = Math.round(c.morph * c.budget), nS = Math.round(c.settle * c.budget);
    const every = Math.max(1, Math.floor((nC + nM + nS) / c.frames));
    let gam = path.gamma0, tau = path.tau0;
    const sr = () => [0.5 * gam * (1 - tau), 0.5 * gam * tau];
    const frames = [];
    const snap3 = (ph) => { const f = { ph, s: st.step, g: +gam.toFixed(4), u: +tau.toFixed(4), L: +st.L.toFixed(5), p: [] };
      for (let i = 0; i < N; i++) f.p.push(...st.C[i].map(v => +(v - st.L / 2).toFixed(4)), ...st.Q[i].map(v => +v.toFixed(5))); frames.push(f); };
    snap3('start');
    const nz = c.noise * c.noiseScale, nzM = c.noiseMorph * c.noiseScale;
    for (let k = 0; k < nC; k++) { const [s, r] = sr(); dyn(st, r, c.mu * 3, nz * (1 - k / nC), true, s); if (st.step % every === 0) snap3('compress'); }
    for (let k = 0; k < nM; k++) { const u = k / nM; gam = path.gamma0 + (1 - path.gamma0) * u; tau = path.tau0 * (1 - u); const [s, r] = sr();
      dyn(st, r, c.mu, nzM * (1 - u), true, s); if (st.step % every === 0) snap3('morph'); }
    gam = 1; tau = 0;
    for (let k = 0; k < nS; k++) { dyn(st, 0, c.mu * Math.pow(1e-4, k / nS), 0, true, 0.5); if (st.step % every === 0) snap3('settle'); }
    snap3('settle');
    const leg = legalize(st.C, st.Q);
    const h = leg.side / 2, poses = leg.C.map((p, i) => [p[0] - h, p[1] - h, p[2] - h, ...leg.Q[i]]);
    frames.push({ ph: 'legal', s: st.step, g: 1, u: 0, L: +leg.side.toFixed(6), p: poses.flatMap(p => [...p.slice(0, 3).map(v => +v.toFixed(5)), ...p.slice(3).map(v => +v.toFixed(6))]) });
    return { L: leg.side, Lsoft: st.L, scale: leg.k, poses, frames, evals: st.evals, steps: st.step, ms: Date.now() - t0, cfg: c };
  }

  const api = { run, legalize, sdBoxes, GR, boxesOverlap, axes, rotq, halfExt, setN: n => { N = n; } };
  if (typeof module !== 'undefined') module.exports = api; else root.Packer3 = api;
})(this);
