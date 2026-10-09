(async function () {
  const D = await SiteData.load();
  // the wall
  const short = { 'squ-in-squ': 'squares · square', 'squ-in-cir': 'squares · circle', 'squ-in-tri': 'squares · triangle', 'tri-in-tri': 'triangles · triangle', 'tri-in-squ': 'triangles · square', 'hex-in-squ': 'hexagons · square', 'cir-in-squ': 'disks · square', 'cub-in-cub': 'cubes · cube' };
  const W = SiteViewers.wall(document.getElementById('wall'), D.wall.map(w => Object.assign({}, w, { label: short[w.family] || w.family, method: `n=${w.n} · ${w.method}`, href: `families.html#${w.family}` })));
  document.getElementById('walltitle').textContent = `${D.wall.length} searches at once`;
  const wb = document.getElementById('wallbtn'); wb.textContent = W.paused ? 'Play' : 'Pause'; wb.onclick = () => { wb.textContent = W.toggle() ? 'Play' : 'Pause'; };
  const main = D.mainCampaign, cells = D.cells.filter(c => c.campaign === main).map(c => Object.assign({}, c, { method: c.method.replace('-best', '') }));
  const meths = ['harden', 'grow', 'rigid', 'sa', 'pc'];
  const fams = [...new Set(cells.map(c => c.family))];
  const inst = new Set(cells.map(c => c.family + '/' + c.n));
  document.getElementById('nums').innerHTML = [
    [D.totalRuns.toLocaleString(), 'runs in ' + Object.keys(D.ledger.campaigns).length + ' pre-registered campaigns'],
    [inst.size, 'instances in ' + fams.length + ' 2D families (main comparison)'],
    [meths.length, 'paths, tuned with the same effort'],
    [D.ledger.claims.length, 'certified packings below a published value'],
  ].map(([b, s]) => `<div><b>${b}</b><span>${s}</span></div>`).join('');
  // matrix: solved instances per family x method
  const T = document.getElementById('matrix');
  let h = '<tr><th>family</th>' + meths.map(m => `<th>${m}</th>`).join('') + '<th>instances</th></tr>';
  for (const f of fams) {
    const fc = cells.filter(c => c.family === f), ni = new Set(fc.map(c => c.n)).size;
    h += `<tr><td><a href="families.html#${f}">${D.families[f].title}</a></td>` + meths.map(m => {
      const s = fc.filter(c => c.method === m && c.is_lowest).length, u = fc.filter(c => c.method === m && c.sole_lowest).length, w = s / ni;
      return `<td><span class="cellv" style="background:color-mix(in srgb, var(--good) ${Math.round(w * 55)}%, transparent)">${s}${u ? ` <small>(${u})</small>` : ''}</span></td>`; }).join('') + `<td>${ni}</td></tr>`;
  }
  const tot = meths.map(m => [cells.filter(c => c.method === m && c.is_lowest).length, cells.filter(c => c.method === m && c.sole_lowest).length]);
  h += '<tr><th>all</th>' + tot.map(t => `<th>${t[0]} <small>(${t[1]})</small></th>`).join('') + `<th>${inst.size}</th></tr>`;
  T.innerHTML = h;
  document.getElementById('matrixcap').textContent = `Campaign ${main}. For each instance, the lowest container size each method reached in 32 runs (after exact tightening). Cells count the instances where the method's lowest is the lowest of all five methods; in brackets, where it is the only one that low.`;
  const order = ['C07-breadth-best', 'C10-portfolio', 'C09-budget', 'C08-start-shape', 'C05-cubes', 'C03-tune-extend2'];
  document.getElementById('findings').innerHTML = order.map(c => D.ledger.findings.find(f => f.campaign === c && !f.text.startsWith('Precision note'))).filter(Boolean).map(f => `<li><span class="mono">${f.campaign}</span> ${f.text}</li>`).join('');
  // path illustrations
  const P = SiteViewers.piece('square'), paths = [
    ['harden', 'γ = 1, τ: 1 → 0', (u) => [1, 1 - u]], ['grow', 'τ = 0, γ: 0.2 → 1', (u) => [0.2 + 0.8 * u, 0]],
    ['rigid', 'γ = 1, τ = 0, same schedule', () => [1, 0]], ['sa', 'rigid; Metropolis moves', () => [1, 0]], ['pc', 'rigid; shrink, relax, perturb', () => [1, 0]]];
  const wrap = document.getElementById('paths');
  for (const [name, cap, fn] of paths) {
    const fig = document.createElement('figure'); fig.innerHTML = `<canvas></canvas><figcaption><b>${name}</b> · ${cap}</figcaption>`; wrap.appendChild(fig);
    const cv = fig.querySelector('canvas'), ctx = cv.getContext('2d');
    const draw = () => { const W = cv.clientWidth * devicePixelRatio, H = W / 3; if (cv.width !== W) { cv.width = W; cv.height = H; }
      const sc = H / 1.4; ctx.setTransform(sc, 0, 0, -sc, 0, H / 2); ctx.clearRect(0, -1, W / sc, 2);
      for (let i = 0; i < 5; i++) { const u = i / 4, [g, t] = fn(u); SiteViewers.piecePath(ctx, P, 0.6 + i * 0.95 * (W / sc - 1.2) / 3.8, 0, 0.3 * u, g, t);
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue(t > 0.5 ? '--blob' : '--sq'); ctx.globalAlpha = 0.85; ctx.fill(); ctx.globalAlpha = 1; } };
    draw(); new ResizeObserver(draw).observe(cv);
  }
})();
