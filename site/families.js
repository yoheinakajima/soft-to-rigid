(async function () {
  const D = await SiteData.load(), meths = ['harden', 'grow', 'rigid', 'sa', 'pc'];
  const famList = Object.keys(D.families).filter(f => D.cells.some(c => c.family === f));
  let cur = null;
  const chips = document.getElementById('chips');
  chips.innerHTML = famList.map(f => `<button type="button" data-f="${f}">${D.families[f].title}</button>`).join('');
  chips.onclick = (e) => { const b = e.target.closest('button'); if (b) { location.hash = b.dataset.f; } };
  window.onhashchange = () => show(location.hash.slice(1) || famList[0]);
  show(location.hash.slice(1) || famList[0]);
  function show(f) {
    if (!D.families[f]) f = famList[0];
    const F = D.families[f];
    chips.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.f === f));
    document.getElementById('ftitle').textContent = F.title;
    document.getElementById('flede').innerHTML = `Container size is the ${F.measure}. Best known values from ${F.sources.map(s => `<a href="${s}">${new URL(s).hostname}</a>`).join(', ')}.`;
    const camps = [...new Set(D.cells.filter(c => c.family === f).map(c => c.campaign))].sort();
    const camp = camps.includes(D.mainCampaign) ? D.mainCampaign : camps[camps.length - 1];
    document.getElementById('camp').textContent = camp;
    const cs = D.cells.filter(c => c.family === f && c.campaign === camp);
    const ns = [...new Set(cs.map(c => c.n))].sort((a, b) => a - b);
    let h = '<tr><th>n</th><th>best known</th>' + meths.map(m => `<th>${m}</th>`).join('') + '</tr>';
    for (const n of ns) {
      const row = cs.filter(c => c.n === n), rec = row[0].record;
      h += `<tr><td>${n}</td><td>${rec.toFixed(5)}</td>` + meths.map(m => {
        const c = row.find(x => x.method === m); if (!c) return '<td></td>';
        const file = SiteData.replayFile(D, c), g = c.best_gap;
        const gap = Math.abs(g) < 1e-9 ? '0' : Math.abs(g) < 1e-3 ? g.toExponential(1) : g.toFixed(4);
        return `<td><span class="${c.solved ? 'ok' : 'no'}">${c.below ? '★' : c.solved ? '✓' : '·'}</span> ${c.hits_1e3}/${c.runs} ${gap} ${file ? `<button type="button" data-file="${file}" aria-label="replay ${m} n=${n}">▶</button>` : ''}</td>`;
      }).join('') + '</tr>';
    }
    const T = document.getElementById('inst'); T.innerHTML = h;
    T.onclick = (e) => { const b = e.target.closest('button'); if (!b) return; T.querySelectorAll('tr').forEach(r => r.classList.remove('sel')); b.closest('tr').classList.add('sel'); play(b.dataset.file); };
    const firstHarden = T.querySelector('button'); if (firstHarden && cur === null) {}
  }
  let handle = null;
  async function play(file) {
    const R = await fetch(file).then(r => r.json());
    if (handle) handle.stop();
    const el = document.getElementById('viewer');
    if (R.piece === 'cube') { el.querySelector('.stage').innerHTML = '<div class="hud"></div>'; handle = SiteViewers.replay3d(el, R); }
    else { el.querySelector('.stage').innerHTML = '<canvas></canvas><div class="hud"></div>'; handle = SiteViewers.replay2d(el, R); }
    document.getElementById('vcap').textContent = `${R.method}, seed ${R.seed}: legal size ${R.L.toFixed(6)}` + (R.record ? ` (best known ${R.record.toFixed(6)})` : '') + '.';
    cur = file;
  }
})();
