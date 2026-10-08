// Replay viewers and in-browser verifier. Geometry matches engine/engine2d.js and engine/engine3d.js.
(function () {
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const K = { circle: 0, triangle: 3, square: 4, pentagon: 5, hexagon: 6, octagon: 8 };

  function piece(name) {
    const k = K[name];
    if (!k) return { k: 0, g: [], rho: 0.5, R: 0.5 };
    const rho = 1 / (2 * Math.tan(Math.PI / k)), R = 1 / (2 * Math.sin(Math.PI / k)), g = [];
    for (let i = 0; i < k; i++) { const a = -Math.PI / 2 - Math.PI / k + 2 * Math.PI * i / k; g.push([R * Math.cos(a), R * Math.sin(a)]); }
    return { k, g, rho, R };
  }
  // container outline (centred at origin) as a path
  function containerPath(ctx, type, L) {
    ctx.beginPath();
    if (type === 'circle') ctx.arc(0, 0, L, 0, 2 * Math.PI);
    else if (type === 'square') ctx.rect(-L / 2, -L / 2, L, L);
    else { const ri = L / (2 * Math.sqrt(3)), rc = 2 * ri; for (let i = 0; i < 3; i++) { const a = -Math.PI / 2 + Math.PI + 2 * Math.PI * i / 3; i ? ctx.lineTo(rc * Math.cos(a), rc * Math.sin(a)) : ctx.moveTo(rc * Math.cos(a), rc * Math.sin(a)); } ctx.closePath(); }
  }
  const outerR = (type, L) => type === 'circle' ? L : type === 'square' ? L / Math.SQRT2 : L / Math.sqrt(3);
  // rounded polygon γ·[(1-τ)P ⊕ τρD] at (x, y, θ)
  function piecePath(ctx, P, x, y, t, g, u) {
    ctx.beginPath();
    if (!P.k) { ctx.arc(x, y, 0.5 * g, 0, 2 * Math.PI); return; }
    const s = g * (1 - u), r = g * u * P.rho, c = Math.cos(t), d = Math.sin(t);
    const V = P.g.map(([a, b]) => [x + s * (a * c - b * d), y + s * (a * d + b * c)]);
    if (s < 1e-6) { ctx.arc(x, y, r, 0, 2 * Math.PI); return; }
    const k = P.k;
    for (let e = 0; e < k; e++) {
      const A = V[e], B = V[(e + 1) % k], ex = B[0] - A[0], ey = B[1] - A[1], l = Math.hypot(ex, ey), nx = ey / l, ny = -ex / l;
      const C = V[(e + 2) % k], fx = C[0] - B[0], fy = C[1] - B[1], m = Math.hypot(fx, fy), mx = fy / m, my = -fx / m;
      if (e === 0) ctx.moveTo(A[0] + r * nx, A[1] + r * ny);
      ctx.lineTo(B[0] + r * nx, B[1] + r * ny);
      if (r > 1e-6) ctx.arc(B[0], B[1], r, Math.atan2(ny, nx), Math.atan2(my, mx), false);
    }
    ctx.closePath();
  }
  function frameAt(F, t) { // t in [0,1] -> interpolated frame
    const x = t * (F.length - 1), i = Math.min(F.length - 2, Math.floor(x)), w = x - i;
    return { A: F[i], B: F[i + 1], w, ph: (w < 0.5 ? F[i] : F[i + 1]).ph, L: F[i].L + (F[i + 1].L - F[i].L) * w,
      g: F[i].g + (F[i + 1].g - F[i].g) * w, u: F[i].u + (F[i + 1].u - F[i].u) * w };
  }
  function controls(el, onChange) {
    const btn = el.querySelector('button'), rng = el.querySelector('input');
    const st = { t: 0, playing: !reduce };
    btn.textContent = st.playing ? 'Pause' : 'Play';
    btn.onclick = () => { if (st.t >= 1) st.t = 0; st.playing = !st.playing; btn.textContent = st.playing ? 'Pause' : 'Play'; };
    rng.oninput = () => { st.t = rng.value / 1000; st.playing = false; btn.textContent = 'Play'; onChange && onChange(); };
    st.sync = () => { rng.value = Math.round(st.t * 1000); if (st.t >= 1 && st.playing) { st.playing = false; btn.textContent = 'Replay'; } };
    return st;
  }
  function mix(c1, c2, w) { const h = (c) => [1, 3, 5].map(k => parseInt(c.slice(k, k + 2), 16)); const a = h(c1), b = h(c2); return `rgb(${a.map((v, k) => Math.round(v + (b[k] - v) * w))})`; }

  function replay2d(el, D, opts) {
    opts = opts || {};
    const cv = el.querySelector('canvas'), hud = el.querySelector('.hud'), ctx = cv.getContext('2d');
    const P = piece(D.piece), st = controls(el.querySelector('.ctl'));
    let span = null;
    let alive = true;
    function draw() {
      const W = cv.clientWidth * devicePixelRatio; if (cv.width !== W) { cv.width = W; cv.height = W; }
      const f = frameAt(D.frames, st.t);
      const want = outerR(D.container, Math.max(f.L, D.record || 0)) * 1.08 + 0.3; span = span === null ? want : span + (want - span) * 0.15; // follow the container
      const sc = W / (2 * span); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, W); ctx.setTransform(sc, 0, 0, -sc, W / 2, W / 2);
      if (D.record) { ctx.save(); ctx.setLineDash([0.08, 0.06]); ctx.lineWidth = 1.2 / sc; ctx.strokeStyle = css('--ref'); containerPath(ctx, D.container, D.record); ctx.stroke(); ctx.restore(); }
      ctx.lineWidth = 2 / sc; ctx.strokeStyle = css('--ink'); containerPath(ctx, D.container, f.L); ctx.stroke();
      const blob = css('--blob'), hard = css('--sq');
      for (let i = 0; i < D.n; i++) {
        const a = f.A.p.slice(3 * i, 3 * i + 3), b = f.B.p.slice(3 * i, 3 * i + 3);
        const x = a[0] + (b[0] - a[0]) * f.w, y = a[1] + (b[1] - a[1]) * f.w, t = a[2] + (b[2] - a[2]) * f.w;
        piecePath(ctx, P, x, y, t, f.g, f.u);
        ctx.fillStyle = mix(hard, blob, Math.min(1, f.u)); ctx.globalAlpha = 0.88; ctx.fill(); ctx.globalAlpha = 1;
        ctx.lineWidth = 1 / sc; ctx.strokeStyle = css('--panel'); ctx.stroke();
      }
      hud.innerHTML = `<b>${f.ph}</b> · size <b>${f.L.toFixed(4)}</b>` + (D.record ? ` · best known ${D.record.toFixed(4)}` : '');
    }
    let last = performance.now();
    function tick(now) { if (!alive) return; const dt = Math.min(0.1, (now - last) / 1000); last = now; if (st.playing) st.t = Math.min(1, st.t + dt / (opts.seconds || 10)); st.sync(); draw(); requestAnimationFrame(tick); }
    requestAnimationFrame(tick);
    return { stop: () => { alive = false; } };
  }

  function replay3d(el, D) {
    const stage = el.querySelector('.stage'), hud = el.querySelector('.hud'), st = controls(el.querySelector('.ctl'));
    if (!window.THREE) { hud.textContent = 'The 3D viewer could not load.'; return { stop() {} }; }
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(2, devicePixelRatio || 1)); stage.appendChild(renderer.domElement);
    const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
    const oc = THREE.OrbitControls ? new THREE.OrbitControls(camera, renderer.domElement) : null;
    if (oc) { oc.enableDamping = true; oc.autoRotate = !reduce; oc.autoRotateSpeed = 0.7; oc.enableZoom = false; }
    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const l1 = new THREE.DirectionalLight(0xffffff, 0.75); l1.position.set(4, 7, 5); scene.add(l1);
    const fit = (D.record || 3) + 0.7; camera.position.set(fit * 1.5, fit * 1.1, fit * 1.8);
    const grp = new THREE.Group(); scene.add(grp);
    const geos = new Map();
    function geo(s, r) { // rounded box: core half-side s, radius r
      const key = Math.round(s * 40) + ':' + Math.round(r * 40); if (geos.has(key)) return geos.get(key);
      const G = new THREE.BoxGeometry(1, 1, 1, 8, 8, 8), p = G.attributes.position, v = new THREE.Vector3();
      for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const c = new THREE.Vector3(Math.max(-s, Math.min(s, v.x)), Math.max(-s, Math.min(s, v.y)), Math.max(-s, Math.min(s, v.z))); const d = v.clone().sub(c); if (d.length() > 1e-9) d.setLength(r); else d.set(0, 0, 0); c.add(d); p.setXYZ(i, c.x, c.y, c.z); }
      G.computeVertexNormals(); geos.set(key, G); return G;
    }
    const meshes = [];
    for (let i = 0; i < D.n; i++) { const m = new THREE.Mesh(geo(0, 0.5), new THREE.MeshStandardMaterial({ roughness: 0.55, metalness: 0.05 })); grp.add(m); meshes.push(m); }
    const edges = (L, color, dashed) => { const l = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(L, L, L)), dashed ? new THREE.LineDashedMaterial({ color, dashSize: 0.08, gapSize: 0.06 }) : new THREE.LineBasicMaterial({ color })); if (dashed) l.computeLineDistances(); return l; };
    if (D.record) grp.add(edges(D.record, new THREE.Color(css('--ref')), true));
    let box = null, alive = true;
    const qa = new THREE.Quaternion(), qb = new THREE.Quaternion();
    function resize() { const w = stage.clientWidth; renderer.setSize(w, w, false); camera.aspect = 1; camera.updateProjectionMatrix(); }
    resize(); new ResizeObserver(resize).observe(stage);
    let last = performance.now();
    function tick(now) {
      if (!alive) return;
      const dt = Math.min(0.1, (now - last) / 1000); last = now; if (st.playing) st.t = Math.min(1, st.t + dt / 12); st.sync();
      const f = frameAt(D.frames, st.t), s = 0.5 * f.g * (1 - f.u), r = 0.5 * f.g * f.u, G = geo(s, r);
      if (box) grp.remove(box); box = edges(f.L, new THREE.Color(css('--ink')), false); grp.add(box);
      const blob = new THREE.Color(css('--blob')), hard = new THREE.Color(css('--sq'));
      for (let i = 0; i < D.n; i++) {
        const a = f.A.p.slice(7 * i, 7 * i + 7), b = f.B.p.slice(7 * i, 7 * i + 7), m = meshes[i];
        m.geometry = G;
        m.position.set(a[0] + (b[0] - a[0]) * f.w, a[2] + (b[2] - a[2]) * f.w, a[1] + (b[1] - a[1]) * f.w); // sim (x,y,z) -> three (x,z,y)
        qa.set(-a[4], -a[6], -a[5], a[3]); qb.set(-b[4], -b[6], -b[5], b[3]); m.quaternion.copy(qa).slerp(qb, f.w);
        m.material.color.copy(hard).lerp(blob, Math.min(1, f.u));
      }
      hud.innerHTML = `<b>${f.ph}</b> · size <b>${f.L.toFixed(4)}</b>` + (D.record ? ` · best known ${D.record.toFixed(4)}` : '');
      if (oc) oc.update(); renderer.render(scene, camera); requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
    return { stop: () => { alive = false; renderer.dispose(); stage.innerHTML = '<div class="hud"></div>'; } };
  }

  // ---------- verifier: same checks as verify.py (2D) ----------
  function verify2d(c) {
    const P = piece(c.piece), s = c.s_full, k = P.k;
    const V = c.pieces.map(([x, y, t]) => k ? P.g.map(([a, b]) => [x + a * Math.cos(t) - b * Math.sin(t), y + a * Math.sin(t) + b * Math.cos(t)]) : [[x, y]]);
    const pad = k ? 0 : 0.5; let wall = Infinity, pair = Infinity;
    const N = c.container === 'square' ? [[1, 0, .5], [0, 1, .5], [-1, 0, .5], [0, -1, .5]] : c.container === 'triangle' ? [-Math.PI / 2, Math.PI / 6, 5 * Math.PI / 6].map(a => [Math.cos(a), Math.sin(a), 1 / (2 * Math.sqrt(3))]) : null;
    for (const Q of V) for (const v of Q) {
      if (!N) wall = Math.min(wall, s - pad - Math.hypot(v[0], v[1]));
      else for (const [ax, ay, b] of N) wall = Math.min(wall, b * s - pad - (ax * v[0] + ay * v[1]));
    }
    const axes = (Q) => Q.map((v, i) => { const w = Q[(i + 1) % Q.length]; const ux = w[1] - v[1], uy = -(w[0] - v[0]), l = Math.hypot(ux, uy); return [ux / l, uy / l]; });
    for (let i = 0; i < V.length; i++) for (let j = i + 1; j < V.length; j++) {
      let g;
      if (!k) g = Math.hypot(V[i][0][0] - V[j][0][0], V[i][0][1] - V[j][0][1]) - 1;
      else { g = -Infinity; for (const [ux, uy] of axes(V[i]).concat(axes(V[j]))) { const pa = V[i].map(v => ux * v[0] + uy * v[1]), pb = V[j].map(v => ux * v[0] + uy * v[1]); g = Math.max(g, Math.min(...pb) - Math.max(...pa), Math.min(...pa) - Math.max(...pb)); } }
      pair = Math.min(pair, g);
    }
    return { n: V.length, s, wall, pair, ok: wall > 0 && pair > 0 };
  }
  // cubes: same as verify3.py
  function verify3d(c) {
    const s = c.s_full, dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2], cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
    const cubes = c.pieces.map(p => { const [w0, x0, y0, z0] = p.slice(3), n = Math.hypot(w0, x0, y0, z0), w = w0 / n, x = x0 / n, y = y0 / n, z = z0 / n;
      const R = [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]];
      const ax = [0, 1, 2].map(k => [R[0][k], R[1][k], R[2][k]]), V = [];
      for (const a of [-.5, .5]) for (const b of [-.5, .5]) for (const d of [-.5, .5]) V.push([0, 1, 2].map(i => p[i] + a * ax[0][i] + b * ax[1][i] + d * ax[2][i]));
      return { ax, V }; });
    let wall = Infinity, pair = Infinity;
    for (const { V } of cubes) for (const v of V) for (let i = 0; i < 3; i++) wall = Math.min(wall, v[i], s - v[i]);
    for (let i = 0; i < cubes.length; i++) for (let j = i + 1; j < cubes.length; j++) {
      const A = cubes[i], B = cubes[j], axes = [...A.ax, ...B.ax];
      for (const a of A.ax) for (const b of B.ax) { const w = cross(a, b); if (dot(w, w) > 1e-18) axes.push(w); }
      let g = -Infinity;
      for (const u0 of axes) { const l = Math.sqrt(dot(u0, u0)), u = u0.map(v => v / l), pa = A.V.map(v => dot(u, v)), pb = B.V.map(v => dot(u, v)); g = Math.max(g, Math.min(...pb) - Math.max(...pa), Math.min(...pa) - Math.max(...pb)); }
      pair = Math.min(pair, g);
    }
    return { n: cubes.length, s, wall, pair, ok: wall > 0 && pair > 0 };
  }

  window.SiteViewers = { replay2d, replay3d, verify2d, verify3d, piece, piecePath, containerPath };
})();
