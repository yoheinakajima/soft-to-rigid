// engine2d.js — packing n congruent convex pieces in the smallest container (2D).
//
// A piece is a regular k-gon with unit side (k = 0 means a unit-diameter circle). Its *shape state* is
//   piece(γ, τ) = γ · [ (1-τ) P  ⊕  τ ρ D ]
// where P is the polygon about its incenter, ρ its inradius and D the unit disk. τ = 1 is the inscribed
// disk, τ = 0 the polygon; γ scales the whole piece. Every method is a *path* through (γ, τ):
//   harden : γ = 1,  τ : 1 → 0      (start as the inscribed disk, harden into the polygon)  — ours
//   grow   : τ = 0,  γ : γ0 → 1     (rigid polygon growing in size, Lubachevsky–Stillinger style)
//   rigid  : γ = 1,  τ = 0          (full polygon from the start; same schedule)
//   sa     : rigid pieces, Metropolis simulated annealing on poses and container size
//   pc     : rigid pieces, perturbation–compression (shrink, relax, perturb on failure)
// The container is centred at the origin with size L (square: side, triangle: side, circle: radius).
// Energy: E = Σ_pairs (2r - sd(cores))_+² + Σ_vertices (wall violation)_+² + μ L.
'use strict';

// ---------- random ----------
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function gauss(rng) { let u = 0; while (u === 0) u = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rng()); }

// ---------- pieces ----------
function makePiece(k) {
  if (k === 0) return { k: 0, g: [], rho: 0.5, R: 0.5, area: Math.PI / 4, sym: 0 };
  const rho = 1 / (2 * Math.tan(Math.PI / k)), R = 1 / (2 * Math.sin(Math.PI / k)), g = [];
  // vertices CCW about the incenter; first edge is horizontal at the bottom
  for (let i = 0; i < k; i++) { const a = -Math.PI / 2 - Math.PI / k + 2 * Math.PI * i / k; g.push(R * Math.cos(a), R * Math.sin(a)); }
  return { k, g, rho, R, area: k * rho / 2, sym: 2 * Math.PI / k };
}
const PIECES = { circle: 0, triangle: 3, square: 4, pentagon: 5, hexagon: 6, octagon: 8 };

// ---------- containers (centred at origin, size L) ----------
function makeContainer(type) {
  const s3 = Math.sqrt(3);
  if (type === 'square') return { type, normals: [1, 0, 0, 1, -1, 0, 0, -1], beta: [0.5, 0.5, 0.5, 0.5], area: 1 };
  if (type === 'triangle') { // equilateral, side L, centroid at origin, one side at the bottom
    const nr = [], b = 1 / (2 * s3);
    for (const a of [-Math.PI / 2, Math.PI / 6, 5 * Math.PI / 6]) nr.push(Math.cos(a), Math.sin(a));
    return { type, normals: nr, beta: [b, b, b], area: s3 / 4 };
  }
  if (type === 'circle') return { type, circle: true, area: Math.PI };
  throw new Error('unknown container ' + type);
}

// ---------- state ----------
// Poses in flat arrays; per-piece world core vertices cached in VW.
function State(n, piece, cont, seed) {
  this.n = n; this.P = piece; this.C = cont; this.rng = mulberry32(seed * 7919 + 13);
  this.X = new Float64Array(n); this.Y = new Float64Array(n); this.T = new Float64Array(n);
  this.VX = new Float64Array(n); this.VY = new Float64Array(n); this.VT = new Float64Array(n);
  this.GX = new Float64Array(n); this.GY = new Float64Array(n); this.GT = new Float64Array(n);
  this.VW = new Float64Array(n * Math.max(1, piece.k) * 2);
  this.L = 1; this.vL = 0; this.gam = 1; this.tau = 0; this.step = 0; this.evals = 0;
}
const st_core = (st) => st.gam * (1 - st.tau);          // core scale
const st_r = (st) => st.P.k === 0 ? st.gam * st.P.rho : st.gam * st.tau * st.P.rho; // rounding radius
function placeAll(st) {
  const k = st.P.k, g = st.P.g, s = st_core(st), V = st.VW;
  if (k === 0) return;
  for (let i = 0; i < st.n; i++) {
    const c = Math.cos(st.T[i]) * s, d = Math.sin(st.T[i]) * s, x = st.X[i], y = st.Y[i], o = i * 2 * k;
    for (let m = 0; m < k; m++) { const gx = g[2 * m], gy = g[2 * m + 1]; V[o + 2 * m] = x + gx * c - gy * d; V[o + 2 * m + 1] = y + gx * d + gy * c; }
  }
}

// ---------- signed distance between two cores, with gradient ----------
// G = d sd / d(x_i, y_i, t_i, x_j, y_j, t_j)
const G = new Float64Array(6);
function sdPair(st, i, j) {
  st.evals++;
  const k = st.P.k, X = st.X, Y = st.Y;
  if (k === 0 || st_core(st) <= 0) {
    const dx = X[i] - X[j], dy = Y[i] - Y[j], d = Math.hypot(dx, dy) || 1e-300;
    G[0] = dx / d; G[1] = dy / d; G[2] = 0; G[3] = -dx / d; G[4] = -dy / d; G[5] = 0; return d;
  }
  const V = st.VW, oa = i * 2 * k, ob = j * 2 * k;
  // separating-axis test over the edge normals of both polygons
  let minO = Infinity, sep = false, bux = 0, buy = 0, own = 0, bA = 0, bB = 0, bc = 0;
  for (let w = 0; w < 2 && !sep; w++) {
    const o = w === 0 ? oa : ob;
    for (let e = 0; e < k; e++) {
      const f = (e + 1) % k, ex = V[o + 2 * f] - V[o + 2 * e], ey = V[o + 2 * f + 1] - V[o + 2 * e + 1], el = Math.hypot(ex, ey);
      const ux = ey / el, uy = -ex / el; // outward normal for CCW order
      let a0 = Infinity, a1 = -Infinity, b0 = Infinity, b1 = -Infinity, ia0 = 0, ia1 = 0, ib0 = 0, ib1 = 0;
      for (let m = 0; m < k; m++) {
        const pa = V[oa + 2 * m] * ux + V[oa + 2 * m + 1] * uy, pb = V[ob + 2 * m] * ux + V[ob + 2 * m + 1] * uy;
        if (pa < a0) { a0 = pa; ia0 = m; } if (pa > a1) { a1 = pa; ia1 = m; }
        if (pb < b0) { b0 = pb; ib0 = m; } if (pb > b1) { b1 = pb; ib1 = m; }
      }
      const oA = a1 - b0, oB = b1 - a0, ov = Math.min(oA, oB);
      if (ov < 0) { sep = true; break; }
      if (ov < minO) { minO = ov; bux = ux; buy = uy; own = w; if (oA <= oB) { bc = 1; bA = ia1; bB = ib0; } else { bc = -1; bA = ia0; bB = ib1; } }
    }
  }
  if (!sep) {
    const pax = V[oa + 2 * bA], pay = V[oa + 2 * bA + 1], pbx = V[ob + 2 * bB], pby = V[ob + 2 * bB + 1];
    const g0 = bc * bux, g1 = bc * buy;
    let g2 = bc * (bux * (-(pay - Y[i])) + buy * (pax - X[i]));
    let g5 = -bc * (bux * (-(pby - Y[j])) + buy * (pbx - X[j]));
    const du = bc * ((-buy) * (pax - pbx) + bux * (pay - pby));
    if (own === 0) g2 += du; else g5 += du;
    G[0] = -g0; G[1] = -g1; G[2] = -g2; G[3] = g0; G[4] = g1; G[5] = -g5;
    return -minO;
  }
  // separated: closest vertex–edge pair
  let d2 = Infinity, pAx = 0, pAy = 0, pBx = 0, pBy = 0;
  for (let w = 0; w < 2; w++) {
    const ov = w === 0 ? oa : ob, oe = w === 0 ? ob : oa; // vertex owner, edge owner
    for (let m = 0; m < k; m++) {
      const vx = V[ov + 2 * m], vy = V[ov + 2 * m + 1];
      for (let e = 0; e < k; e++) {
        const f = (e + 1) % k, ax = V[oe + 2 * e], ay = V[oe + 2 * e + 1], dx = V[oe + 2 * f] - ax, dy = V[oe + 2 * f + 1] - ay;
        let u = ((vx - ax) * dx + (vy - ay) * dy) / (dx * dx + dy * dy); u = u < 0 ? 0 : u > 1 ? 1 : u;
        const cx = ax + u * dx, cy = ay + u * dy, q = (vx - cx) * (vx - cx) + (vy - cy) * (vy - cy);
        if (q < d2) { d2 = q; if (w === 0) { pAx = vx; pAy = vy; pBx = cx; pBy = cy; } else { pAx = cx; pAy = cy; pBx = vx; pBy = vy; } }
      }
    }
  }
  const d = Math.sqrt(d2) || 1e-300, nx = (pAx - pBx) / d, ny = (pAy - pBy) / d;
  G[0] = nx; G[1] = ny; G[2] = nx * (-(pAy - Y[i])) + ny * (pAx - X[i]);
  G[3] = -nx; G[4] = -ny; G[5] = -(nx * (-(pBy - Y[j])) + ny * (pBx - X[j]));
  return Math.sqrt(d2);
}

// ---------- energy gradient ----------
// accumulates into GX, GY, GT; returns dE/dL from the walls (without pressure) and max violation
function gradient(st) {
  const n = st.n, k = st.P.k, r = st_r(st), R = st.gam * st.P.R, cut = 2 * R + 1e-9;
  st.GX.fill(0); st.GY.fill(0); st.GT.fill(0);
  placeAll(st);
  let maxO = 0, gL = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const dx = st.X[j] - st.X[i], dy = st.Y[j] - st.Y[i];
    if (dx * dx + dy * dy > cut * cut) continue;
    const sd = sdPair(st, i, j), o = 2 * r - sd;
    if (o <= 0) continue;
    if (o > maxO) maxO = o;
    const c = -2 * o;
    st.GX[i] += c * G[0]; st.GY[i] += c * G[1]; st.GT[i] += c * G[2];
    st.GX[j] += c * G[3]; st.GY[j] += c * G[4]; st.GT[j] += c * G[5];
  }
  // walls: every core vertex (or the centre, for circles / pure disks)
  const C = st.C, V = st.VW, L = st.L, pts = k === 0 || st_core(st) <= 0 ? 1 : k;
  for (let i = 0; i < n; i++) for (let m = 0; m < pts; m++) {
    const vx = pts === 1 ? st.X[i] : V[i * 2 * k + 2 * m], vy = pts === 1 ? st.Y[i] : V[i * 2 * k + 2 * m + 1];
    const px = -(vy - st.Y[i]), py = vx - st.X[i]; // dv/dθ
    if (C.circle) {
      const rr = Math.hypot(vx, vy) || 1e-300, q = rr + r - L;
      if (q > 0) { const ax = vx / rr, ay = vy / rr; st.GX[i] += 2 * q * ax; st.GY[i] += 2 * q * ay; st.GT[i] += 2 * q * (ax * px + ay * py); gL -= 2 * q; if (q > maxO) maxO = q; }
    } else {
      const N_ = C.normals;
      for (let w = 0; w < C.beta.length; w++) {
        const ax = N_[2 * w], ay = N_[2 * w + 1], q = ax * vx + ay * vy + r - C.beta[w] * L;
        if (q > 0) { st.GX[i] += 2 * q * ax; st.GY[i] += 2 * q * ay; st.GT[i] += 2 * q * (ax * px + ay * py); gL -= 2 * q * C.beta[w]; if (q > maxO) maxO = q; }
      }
    }
  }
  if (st.tau >= 0.9999 || k === 0) st.GT.fill(0);
  return { gL, maxO };
}

// one momentum step; container size L is dynamic under pressure mu when moveL
function step(st, mu, noise, noiseT, moveL, lr) {
  const beta = 0.85, cap = 0.03 * st.P.R / 0.7071;
  lr = lr || 0.04;
  const { gL } = gradient(st);
  for (let i = 0; i < st.n; i++) {
    st.VX[i] = beta * st.VX[i] - lr * st.GX[i];
    st.VY[i] = beta * st.VY[i] - lr * st.GY[i];
    st.VT[i] = beta * st.VT[i] - lr * st.GT[i];
    const vm = Math.hypot(st.VX[i], st.VY[i]);
    if (vm > cap) { st.VX[i] *= cap / vm; st.VY[i] *= cap / vm; }
    if (Math.abs(st.VT[i]) > 0.03) st.VT[i] = Math.sign(st.VT[i]) * 0.03;
    st.X[i] += st.VX[i]; st.Y[i] += st.VY[i]; st.T[i] += st.VT[i];
    if (noise > 0) { st.X[i] += noise * gauss(st.rng); st.Y[i] += noise * gauss(st.rng); }
    if (noiseT > 0) st.T[i] += noiseT * gauss(st.rng);
  }
  if (moveL) {
    st.vL = beta * st.vL - 0.02 * (mu + gL);
    if (Math.abs(st.vL) > cap) st.vL = Math.sign(st.vL) * cap;
    st.L += st.vL;
  }
  st.step++;
}

// ---------- exact-ish final measurement ----------
// Rigid pieces (γ=1, τ=0). Scale centres apart about their mean until no pair overlaps (SAT, 1e-12),
// then the smallest container (any translation, fixed orientation) holding every vertex.
function worldVerts(P, x, y, t) {
  if (P.k === 0) return null;
  const out = [], c = Math.cos(t), d = Math.sin(t);
  for (let m = 0; m < P.k; m++) { const gx = P.g[2 * m], gy = P.g[2 * m + 1]; out.push([x + gx * c - gy * d, y + gx * d + gy * c]); }
  return out;
}
function rigidSd(P, a, b) { // a, b = [x, y, t]
  const st = new State(2, P, makeContainer('square'), 1);
  st.X[0] = a[0]; st.Y[0] = a[1]; st.T[0] = a[2]; st.X[1] = b[0]; st.Y[1] = b[1]; st.T[1] = b[2];
  st.gam = 1; st.tau = 0; placeAll(st);
  return sdPair(st, 0, 1) - (P.k === 0 ? 1 : 0);
}
function minEnclosingCircle(pts) { // Welzl, iterative with shuffle-free incremental version
  let c = [pts[0][0], pts[0][1]], r = 0;
  const inC = (p) => Math.hypot(p[0] - c[0], p[1] - c[1]) <= r + 1e-14;
  const circ2 = (a, b) => { c = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; r = Math.hypot(a[0] - c[0], a[1] - c[1]); };
  const circ3 = (a, b, q) => {
    const bx = b[0] - a[0], by = b[1] - a[1], cx = q[0] - a[0], cy = q[1] - a[1], D = 2 * (bx * cy - by * cx);
    if (Math.abs(D) < 1e-300) return false;
    const ux = (cy * (bx * bx + by * by) - by * (cx * cx + cy * cy)) / D, uy = (bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by)) / D;
    c = [a[0] + ux, a[1] + uy]; r = Math.hypot(ux, uy); return true;
  };
  for (let i = 1; i < pts.length; i++) if (!inC(pts[i])) {
    c = [pts[i][0], pts[i][1]]; r = 0;
    for (let j = 0; j < i; j++) if (!inC(pts[j])) {
      circ2(pts[i], pts[j]);
      for (let m = 0; m < j; m++) if (!inC(pts[m])) circ3(pts[i], pts[j], pts[m]);
    }
  }
  return { c, r };
}
// tight container for given rigid poses; returns {L, cx, cy}
function tightContainer(P, C, poses) {
  const pts = [];
  for (const p of poses) { if (P.k === 0) pts.push([p[0], p[1]]); else pts.push(...worldVerts(P, p[0], p[1], p[2])); }
  const pad = P.k === 0 ? 0.5 : 0;
  if (C.circle) { const m = minEnclosingCircle(pts); return { L: m.r + pad, cx: m.c[0], cy: m.c[1] }; }
  const h = [];
  for (let w = 0; w < C.beta.length; w++) { let mx = -Infinity; for (const q of pts) mx = Math.max(mx, C.normals[2 * w] * q[0] + C.normals[2 * w + 1] * q[1]); h.push(mx + pad); }
  if (C.type === 'square') {
    const wx = h[0] + h[2], wy = h[1] + h[3], L = Math.max(wx, wy);
    return { L, cx: (h[0] - h[2]) / 2, cy: (h[1] - h[3]) / 2 };
  }
  // triangle: all three walls tight: a_w·c = h_w - βL, L = Σh / (3β)
  const b = C.beta[0], L = (h[0] + h[1] + h[2]) / (3 * b), N_ = C.normals;
  const r0 = h[0] - b * L, r1 = h[1] - b * L, det = N_[0] * N_[3] - N_[1] * N_[2];
  return { L, cx: (r0 * N_[3] - N_[1] * r1) / det, cy: (N_[0] * r1 - r0 * N_[2]) / det };
}
function legalize(P, C, X, Y, T) {
  const n = X.length;
  let mx = 0, my = 0; for (let i = 0; i < n; i++) { mx += X[i]; my += Y[i]; } mx /= n; my /= n;
  const cut = 2 * P.R + 1e-9;
  const ok = (s) => {
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const a = [mx + s * (X[i] - mx), my + s * (Y[i] - my), T[i]], b = [mx + s * (X[j] - mx), my + s * (Y[j] - my), T[j]];
      if (Math.hypot(a[0] - b[0], a[1] - b[1]) > cut) continue;
      if (rigidSd(P, a, b) < -1e-12) return false;
    }
    return true;
  };
  let lo = 1, hi = 1;
  if (!ok(1)) { hi = 1.0001; while (!ok(hi)) hi = 1 + (hi - 1) * 2; for (let it = 0; it < 60; it++) { const m = (lo + hi) / 2; if (ok(m)) hi = m; else lo = m; } }
  const poses = [];
  for (let i = 0; i < n; i++) poses.push([mx + hi * (X[i] - mx), my + hi * (Y[i] - my), T[i]]);
  const tc = tightContainer(P, C, poses);
  return { L: tc.L, scale: hi, poses: poses.map(p => [p[0] - tc.cx, p[1] - tc.cy, p[2]]) };
}

// ---------- frames for replays ----------
function snap(st, frames, ph) {
  const p = [];
  for (let i = 0; i < st.n; i++) p.push(+st.X[i].toFixed(4), +st.Y[i].toFixed(4), +st.T[i].toFixed(4));
  frames.push({ ph, s: st.step, g: +st.gam.toFixed(4), u: +st.tau.toFixed(4), L: +st.L.toFixed(5), p });
}

// ---------- gradient-path methods: harden / grow / rigid (+ ablations) ----------
function initState(cfg, P, C) {
  const st = new State(cfg.n, P, C, cfg.seed);
  // start container: area = fill * total piece area
  st.L = Math.sqrt(cfg.fill * cfg.n * P.area / C.area);
  for (let i = 0; i < cfg.n; i++) {
    // uniform inside the container, away from walls
    for (let tries = 0; tries < 1000; tries++) {
      const x = (st.rng() - 0.5) * st.L * 2, y = (st.rng() - 0.5) * st.L * 2;
      let inside;
      if (C.circle) inside = Math.hypot(x, y) < st.L - P.R;
      else { inside = true; for (let w = 0; w < C.beta.length; w++) if (C.normals[2 * w] * x + C.normals[2 * w + 1] * y > C.beta[w] * st.L - P.R) inside = false; }
      if (inside) { st.X[i] = x; st.Y[i] = y; break; }
    }
    st.T[i] = st.rng() * 2 * Math.PI;
  }
  return st;
}
function runPath(cfg) {
  const P = makePiece(PIECES[cfg.piece]), C = makeContainer(cfg.container);
  const st = initState(cfg, P, C), frames = [], B = cfg.budget;
  const nC = Math.round(cfg.compress * B), nM = Math.round(cfg.morph * B), nS = Math.round(cfg.settle * B);
  const total = nC + nM + nS, every = Math.max(1, Math.floor(total / cfg.frames));
  const path = cfg.path; // {gamma0, tau0}
  const areaC = P.k ? Math.PI * P.rho * P.rho / P.area : 1; // inscribed-disk share of the piece's area
  const shapeAt = (u) => { // u in [0,1] along the morph
    if (path.area) { // grow-area: rigid polygon scaled so its area follows harden's area schedule
      const t = 1 - u; st.tau = 0; st.gam = Math.sqrt(1 - (1 - areaC) * t * t); return;
    }
    if (path.snap) { st.gam = 1; st.tau = u === 0 ? 1 : 0; return; } // snap: disks, then polygons at once
    st.gam = path.gamma0 + (1 - path.gamma0) * u;
    st.tau = path.tau0 * (1 - u);
  };
  shapeAt(0); snap(st, frames, 'start');
  const noisePos = (u, ph) => ph === 'compress' ? cfg.noise * (1 - u) : cfg.noiseMorph * (cfg.noisePeak ? Math.exp(-((u - cfg.noisePeak) ** 2) / 0.005) : (1 - u));
  for (let s = 0; s < nC; s++) {
    const u = s / nC, nz = noisePos(u, 'compress');
    step(st, cfg.mu * 3, nz, nz * 1.5, true); if (st.step % every === 0) snap(st, frames, 'compress');
  }
  for (let s = 0; s < nM; s++) {
    const u = s / nM; shapeAt(u);
    const nz = noisePos(u, 'morph');
    step(st, cfg.mu, nz, nz * 1.5, true); if (st.step % every === 0) snap(st, frames, 'morph');
  }
  shapeAt(1);
  for (let s = 0; s < nS; s++) {
    const mu = cfg.mu * Math.pow(1e-4, s / nS);
    step(st, mu, 0, 0, true); if (st.step % every === 0) snap(st, frames, 'settle');
  }
  snap(st, frames, 'settle');
  return finish(st, P, C, frames);
}
function finish(st, P, C, frames) {
  const leg = legalize(P, C, st.X, st.Y, st.T);
  frames.push({ ph: 'legal', s: st.step, g: 1, u: 0, L: +leg.L.toFixed(6), p: leg.poses.flatMap(p => [+p[0].toFixed(5), +p[1].toFixed(5), +p[2].toFixed(5)]) });
  return { L: leg.L, Lsoft: st.L, scale: leg.scale, poses: leg.poses, frames, evals: st.evals, steps: st.step };
}

// ---------- simulated annealing (rigid) ----------
// Metropolis on single-piece moves and container moves. Energy as above with r = 0 and weight lam on
// overlaps; temperature decays geometrically. Budget is matched to the gradient methods in pair evaluations.
function localE(st, i, r) {
  // energy terms involving piece i (pairs + walls); poses taken from st, VW must be current for all
  const n = st.n, R = st.P.R, cut = 2 * R + 1e-9; let e = 0;
  for (let j = 0; j < n; j++) if (j !== i) {
    const dx = st.X[j] - st.X[i], dy = st.Y[j] - st.Y[i];
    if (dx * dx + dy * dy > cut * cut) continue;
    const o = 2 * r - sdPair(st, i, j); if (o > 0) e += o * o;
  }
  return e + wallE(st, i, r);
}
function wallE(st, i, r) {
  const k = st.P.k, C = st.C, V = st.VW, pts = k === 0 ? 1 : k; let e = 0;
  for (let m = 0; m < pts; m++) {
    const vx = k === 0 ? st.X[i] : V[i * 2 * k + 2 * m], vy = k === 0 ? st.Y[i] : V[i * 2 * k + 2 * m + 1];
    if (C.circle) { const q = Math.hypot(vx, vy) + r - st.L; if (q > 0) e += q * q; }
    else for (let w = 0; w < C.beta.length; w++) { const q = C.normals[2 * w] * vx + C.normals[2 * w + 1] * vy + r - C.beta[w] * st.L; if (q > 0) e += q * q; }
  }
  return e;
}
function placeOne(st, i) {
  const k = st.P.k; if (k === 0) return;
  const g = st.P.g, c = Math.cos(st.T[i]), d = Math.sin(st.T[i]), o = i * 2 * k;
  for (let m = 0; m < k; m++) { const gx = g[2 * m], gy = g[2 * m + 1]; st.VW[o + 2 * m] = st.X[i] + gx * c - gy * d; st.VW[o + 2 * m + 1] = st.Y[i] + gx * d + gy * c; }
}
function runSA(cfg) {
  const P = makePiece(PIECES[cfg.piece]), C = makeContainer(cfg.container);
  const st = initState(cfg, P, C), frames = [];
  st.gam = 1; st.tau = 0; placeAll(st);
  const r = P.k === 0 ? 0.5 : 0, lam = cfg.saLambda, mu = cfg.mu;
  const evalBudget = cfg.evalBudget, T0 = cfg.saT0, T1 = cfg.saT1;
  let E = 0; for (let i = 0; i < st.n; i++) E += localE(st, i, r) / 2 + wallE(st, i, r) / 2; // rough start
  let step = 0, dx = 0.2, acc = 0, tried = 0;
  const every = Math.max(1, Math.floor(evalBudget / cfg.frames));
  let nextSnap = 0;
  snap(st, frames, 'start');
  while (st.evals < evalBudget) {
    const u = st.evals / evalBudget, T = T0 * Math.pow(T1 / T0, u);
    if (st.rng() < 1 / (st.n + 1)) { // container move
      const old = st.L, dL = -Math.abs(gauss(st.rng)) * dx * 0.05 * (st.rng() < 0.7 ? 1 : -1);
      let e0 = 0; for (let i = 0; i < st.n; i++) e0 += wallE(st, i, r);
      st.L = old + dL;
      let e1 = 0; for (let i = 0; i < st.n; i++) e1 += wallE(st, i, r);
      st.evals += st.n;
      const dE = lam * (e1 - e0) + mu * dL;
      if (!(dE <= 0 || st.rng() < Math.exp(-dE / T))) st.L = old;
    } else {
      const i = Math.floor(st.rng() * st.n), ox = st.X[i], oy = st.Y[i], ot = st.T[i];
      const e0 = localE(st, i, r);
      st.X[i] += dx * gauss(st.rng); st.Y[i] += dx * gauss(st.rng); if (P.k) st.T[i] += dx * 1.5 * gauss(st.rng);
      placeOne(st, i);
      const e1 = localE(st, i, r), dE = lam * (e1 - e0);
      tried++;
      if (dE <= 0 || st.rng() < Math.exp(-dE / T)) acc++;
      else { st.X[i] = ox; st.Y[i] = oy; st.T[i] = ot; placeOne(st, i); }
      if (tried === 200) { const rate = acc / tried; dx *= rate > 0.4 ? 1.2 : rate < 0.2 ? 0.8 : 1; dx = Math.min(Math.max(dx, 1e-4), 0.5); acc = 0; tried = 0; }
    }
    step++;
    if (st.evals >= nextSnap) { st.step = step; snap(st, frames, 'anneal'); nextSnap += every; }
  }
  // short zero-pressure relax to remove residual penalty overlap before legalization
  for (let s = 0; s < 300; s++) step_relax(st);
  st.step = step; snap(st, frames, 'relax');
  return finish(st, P, C, frames);
}
function step_relax(st) { st.gam = 1; st.tau = 0; step(st, 0, 0, 0, false, 0.04); }

// ---------- perturbation–compression (rigid) ----------
// Gensane–Ryckelynck style: shrink the container by δ, relax overlaps at fixed size; if it relaxes to
// feasibility keep it and grow δ, otherwise undo and halve δ; after repeated failures perturb a few pieces.
function relaxFixed(st, iters) {
  st.VX.fill(0); st.VY.fill(0); st.VT.fill(0);
  let m = 1;
  for (let s = 0; s < iters; s++) { step(st, 0, 0, 0, false, 0.04); if ((s & 15) === 15) { m = gradient(st).maxO; if (m < 2e-7) break; } }
  return gradient(st).maxO;
}
function runPC(cfg) {
  const P = makePiece(PIECES[cfg.piece]), C = makeContainer(cfg.container);
  const st = initState(cfg, P, C), frames = [];
  st.gam = 1; st.tau = 0;
  const save = () => ({ X: Float64Array.from(st.X), Y: Float64Array.from(st.Y), T: Float64Array.from(st.T), L: st.L });
  const load = (s) => { st.X.set(s.X); st.Y.set(s.Y); st.T.set(s.T); st.L = s.L; };
  const scale = (f) => { for (let i = 0; i < st.n; i++) { st.X[i] *= f; st.Y[i] *= f; } st.L *= f; };
  snap(st, frames, 'start');
  for (let g = 0; g < 60 && relaxFixed(st, 400) > 2e-7; g++) scale(1.01);
  let best = save(), delta = 0.02, fails = 0;
  const every = Math.max(1, Math.floor(cfg.evalBudget / cfg.frames)); let nextSnap = every;
  while (st.evals < cfg.evalBudget) {
    const prev = save();
    if (fails >= 3) {
      const kk = 1 + Math.floor(st.rng() * 3);
      for (let m = 0; m < kk; m++) { const i = Math.floor(st.rng() * st.n); st.X[i] += cfg.pcKick * P.R * gauss(st.rng); st.Y[i] += cfg.pcKick * P.R * gauss(st.rng); st.T[i] += 2 * cfg.pcKick * gauss(st.rng); }
      if (relaxFixed(st, 2 * cfg.pcRelax) < 2e-7) { best = save(); delta = Math.max(delta, 0.002); } else { load(prev); delta = 0.004; }
      fails = 0;
    } else {
      scale(1 - delta);
      if (relaxFixed(st, cfg.pcRelax) < 2e-7) { best = save(); delta = Math.min(delta * 1.3, 0.02); }
      else { load(prev); delta *= 0.5; if (delta < 1e-5) { fails++; delta = 0.003; } }
    }
    if (st.evals >= nextSnap) { snap(st, frames, 'compress'); nextSnap += every; }
  }
  load(best); snap(st, frames, 'best');
  return finish(st, P, C, frames);
}

// ---------- entry ----------
const DEFAULTS = {
  seed: 1, n: 11, piece: 'square', container: 'square', method: 'harden', budget: 1,
  compress: 2500, morph: 7500, settle: 1500, mu: 0.02, fill: 3.2, frames: 150,
  noise: 0.015, noiseMorph: 0.004, noisePeak: 0,
  saLambda: 1, saT0: 1e-3, saT1: 1e-7, pcKick: 0.15, pcRelax: 600, noiseScale: 1,
};
const METHOD_PATHS = {
  harden: { gamma0: 1, tau0: 1 },
  'harden-half': { gamma0: 1, tau0: 0.5 },      // ablation: start half-rounded
  'harden-quarter': { gamma0: 1, tau0: 0.25 },
  grow: { gamma0: 0.35, tau0: 0 },
  snap: { gamma0: 1, tau0: 1, snap: true },          // ablation: disk compression, then rigid polygons at once
  'grow-area': { gamma0: 1, tau0: 0, area: true },  // ablation: rigid growth with harden's area schedule
  rigid: { gamma0: 1, tau0: 0 },
};
function run(cfg) {
  const c = Object.assign({}, DEFAULTS, cfg);
  c.noise *= c.noiseScale; c.noiseMorph *= c.noiseScale;
  const t0 = Date.now();
  let res;
  if (c.method === 'sa' || c.method === 'pc') {
    // equal budget: pair evaluations of a harden run at this n and budget, measured once and cached
    if (!c.evalBudget) c.evalBudget = matchedEvals(c);
    res = c.method === 'sa' ? runSA(c) : runPC(c);
  } else {
    const base = c.method.replace(/-noisepeak$/, '');
    if (c.method.endsWith('-noisepeak')) c.noisePeak = 0.85;
    if (!METHOD_PATHS[base]) throw new Error('unknown method ' + c.method);
    c.path = Object.assign({}, METHOD_PATHS[base]);
    if (c.gamma0 !== undefined) c.path.gamma0 = c.gamma0;
    if (c.tau0 !== undefined) c.path.tau0 = c.tau0;
    res = runPath(c);
  }
  res.ms = Date.now() - t0;
  res.cfg = c;
  return res;
}
const _evalCache = {};
function matchedEvals(c) {
  const key = [c.n, c.piece, c.container, c.budget].join('/');
  if (!_evalCache[key]) {
    const r = runPath(Object.assign({}, c, { method: 'harden', path: METHOD_PATHS.harden, seed: 999999, frames: 2 }));
    _evalCache[key] = r.evals;
  }
  return _evalCache[key];
}

module.exports = { gradient, run, makePiece, makeContainer, legalize, tightContainer, rigidSd, PIECES, METHOD_PATHS, DEFAULTS, State, sdPair, G, placeAll };
