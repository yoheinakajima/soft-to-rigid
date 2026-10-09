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
  const S = D.summary || {};
  const nCamps = Object.keys(D.ledger.campaigns).length;
  document.getElementById('nums').innerHTML = [
    [D.totalRuns.toLocaleString(), 'runs in ' + nCamps + ' planned experiments'],
    [inst.size, 'instances in the main comparison, 7 families'],
    [S.C15 ? S.C15.N : '—', 'instances in 4 held-out families'],
    ['5', 'searches, matched budget and tuning'],
  ].map(([b, s]) => `<div><b>${b}</b><span>${s}</span></div>`).join('');
  // the answer
  const J = (c, t) => `<a class="mono" href="journal.html#${c}">${c.split('-')[0]}</a> ${t}`;
  const ans = [];
  if (S.C07) ans.push(`<b>Not a better default.</b> Tuned with comparable effort, rigid starts reach the lowest container size on ${S.C07.lowest.rigid} of ${S.C07.instances} instances, hardening on ${S.C07.lowest.harden}. ` + J('C07-breadth-best', ''));
  if (S.C07 && S.C16) ans.push(`<b>A different search.</b> On squares in a square hardening is lowest on ${S.C07.squ.harden_lowest} of ${S.C07.squ.N} instances and the only search that low on ${S.C07.squ.harden_sole}, including Trump's n = 11 and Wainwright's n = 19; at ten times the budget it alone reaches the best known packing for n = ${S.C16.harden_only.filter(n => !S.C16.repeats.includes(n)).join(' and ')} (and ${S.C16.harden_only.filter(n => S.C16.repeats.includes(n)).join(', ')}, repeating an earlier experiment). ` + J('C07-breadth-best', '') + ' ' + J('C16-squares-long', ''));
  if (S.C11 && S.C12) ans.push(`<b>Consistent with the gradual rounding, not proven.</b> Compressing disks then switching to polygons at once, or growing rigid polygons along hardening's area schedule, shows no detectable difference from rigid starts (${S.C11.snap_vs_rigid.a_lower}:${S.C11.snap_vs_rigid.b_lower} and ${S.C12.area_vs_rigid.a_lower}:${S.C12.area_vs_rigid.b_lower} instances lower); the pre-registered test on squares is inconclusive. ` + J('C11-snap', '') + ' ' + J('C12-grow-area', ''));
  if (S.C15) ans.push(`<b>It has a cost.</b> On four families held out from development, hardening is lower than rigid starts on ${S.C15.harden_vs_rigid.a_lower} instances and higher on ${S.C15.harden_vs_rigid.b_lower}; a pilot that picks the path per instance does no better than always starting rigid. ` + J('C15-heldout-decision', ''));
  document.getElementById('answer').innerHTML = ans.map(a => `<li>${a}</li>`).join('');
  // paired replays
  const PW = document.getElementById('pairs'), lab = { 'squ-in-squ': 'squares · square', 'tri-in-tri': 'triangles · triangle', 'pen-in-squ': 'pentagons · square' };
  for (const p of (S.pairs || [])) {
    const fig = document.createElement('figure'); fig.className = 'pair';
    fig.innerHTML = `<figcaption><b>${lab[p.family] || p.family} · n = ${p.n}</b> ${p.why} <a class="mono" href="journal.html#${p.campaign}">${p.campaign.split('-')[0]}</a></figcaption><div class="wall two"></div>`;
    PW.appendChild(fig);
    SiteViewers.wall(fig.querySelector('.wall'), [
      { file: p.harden, family: p.family, n: p.n, method: 'best of its runs', dim: 2, label: 'hardening', href: `families.html#${p.family}` },
      { file: p.rigid, family: p.family, n: p.n, method: 'best of its runs', dim: 2, label: 'rigid start', href: `families.html#${p.family}` }], { seconds: 10, sync: true });
  }
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
  document.getElementById('matrixcap').textContent = `Campaign ${main}: every method tuned for its lowest point, 32 runs per instance, matched budget, sizes after tightening. Each cell counts the instances where the method's lowest size is the lowest of all five; in brackets, where it is the only one that low. Held-out families and the ten-times-budget squares campaign are in the journal and on the family pages.`;
  const order = ['C00-reproduce', 'C05-cubes', 'C07-breadth-best', 'C16-squares-long', 'C11-snap', 'C12-grow-area', 'C15-heldout-decision', 'C13-budget-clean', 'C14-equal-refine', 'C10-portfolio', 'C08-start-shape'];
  document.getElementById('findings').innerHTML = order.map(c => D.ledger.findings.findLast(f => f.campaign === c && !f.text.startsWith('Precision note'))).filter(Boolean).map(f => `<li><a class="mono" href="journal.html#${f.campaign}">${f.campaign}</a> <i>${((D.ledger.campaigns[f.campaign] || {}).title || '').replace(/[.?]$/, m => m === '?' ? '?' : '')}</i> ${f.text}</li>`).join('');
  // path illustrations
  const P = SiteViewers.piece('square'), paths = [
    ['harden', 'γ = 1, τ: 1 → 0', (u) => [1, 1 - u]], ['grow', 'τ = 0, γ: 0.2 → 1', (u) => [0.2 + 0.8 * u, 0]],
    ['rigid', 'γ = 1, τ = 0, same schedule', () => [1, 0]], ['sa', 'rigid; Metropolis moves', () => [1, 0]], ['pc', 'rigid; shrink, relax, perturb', () => [1, 0]],
    ['snap (ablation)', 'disks, then polygons at once', (u) => [1, u < 0.5 ? 1 : 0]], ['grow-area (ablation)', 'rigid, area as in hardening', (u) => [Math.sqrt(1 - 0.215 * (1 - u) * (1 - u)), 0]]];
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
