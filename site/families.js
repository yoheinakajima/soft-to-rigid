(async function () {
  const D = await SiteData.load(), meths = ['harden', 'grow', 'rigid', 'sa', 'pc'];
  const order = ['squ-in-squ', 'squ-in-cir', 'squ-in-tri', 'tri-in-tri', 'tri-in-squ', 'hex-in-squ', 'cir-in-squ', 'cub-in-cub', 'pen-in-squ', 'oct-in-squ', 'hex-in-tri', 'tri-in-cir'];
  const famList = Object.keys(D.families).filter(f => D.cells.some(c => c.family === f)).sort((a, b) => (order.indexOf(a) + 99) % 99 - (order.indexOf(b) + 99) % 99);
  let cur = null;
  const chips = document.getElementById('chips');
  chips.innerHTML = famList.map(f => `<button type="button" data-f="${f}">${D.families[f].title.replace(/^Unit (regular |equilateral )?/, '').replace('Unit-diameter circles', 'disks')}${D.families[f].heldout ? ' · held out' : ''}</button>`).join('');
  chips.onclick = (e) => { const b = e.target.closest('button'); if (b) { location.hash = b.dataset.f; } };
  const route = () => { const [f, c] = (location.hash.slice(1) || famList[0]).split('/'); show(f, c); };
  window.onhashchange = route;
  const CAMPNOTE = { 'C07-breadth-best': 'main comparison: 32 runs per method, base budget', 'C16-squares-long': 'ten times the budget, 16 runs per method',
    'C15-heldout-decision': 'held-out family: 64 harden and 64 rigid runs', 'C05-cubes': 'cubes: three gradient paths, 32 runs, two settings', 'C04-breadth': 'median-tuned settings (earlier comparison)' };
  function show(f, want) {
    if (!D.families[f]) f = famList[0];
    const F = D.families[f];
    chips.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.f === f));
    document.getElementById('ftitle').textContent = F.title;
    document.getElementById('flede').innerHTML = `Container size is the ${F.measure}. Best known values from ${F.sources.map(s => `<a href="${s}">${new URL(s).hostname}</a>`).join(', ')}.`;
    const camps = [...new Set(D.cells.filter(c => c.family === f).map(c => c.campaign))].sort();
    const pref = ['C07-breadth-best', 'C15-heldout-decision', 'C05-cubes', 'C16-squares-long', 'C04-breadth'];
    const shown = camps.filter(c => pref.includes(c));
    const camp = shown.includes(want) ? want : (pref.find(c => shown.includes(c)) || camps[camps.length - 1]);
    document.getElementById('camp').innerHTML = shown.map(c => c === camp ? `<b>${c}</b>` : `<a href="#${f}/${c}">${c}</a>`).join(' · ') + ` <span class="cap">(${CAMPNOTE[camp] || ''})</span>`;
    const cs = D.cells.filter(c => c.family === f && c.campaign === camp).map(c => Object.assign({}, c, { method: c.method.replace('-best', ''), rawMethod: c.method }));
    const ns = [...new Set(cs.map(c => c.n))].sort((a, b) => a - b);
    let h = '<tr><th>n</th><th>best known</th>' + meths.map(m => `<th>${m}</th>`).join('') + '</tr>';
    for (const n of ns) {
      const row = cs.filter(c => c.n === n), rec = row[0].record;
      h += `<tr><td>${n}</td><td>${rec.toFixed(5)}</td>` + meths.map(m => {
        const c = row.find(x => x.method === m); if (!c) return '<td></td>';
        const file = SiteData.replayFile(D, Object.assign({}, c, { method: c.rawMethod })), g = c.lowest - c.record;
        const gap = Math.abs(g) < 1e-9 ? '0' : Math.abs(g) < 1e-3 ? g.toExponential(1) : g.toFixed(4);
        return `<td><span class="${c.solved ? 'ok' : 'no'}">${c.below ? '★' : c.solved ? '✓' : '·'}</span> ${c.hits_1e3}/${c.runs} ${gap} ${file ? `<button type="button" data-file="${file}" aria-label="replay ${m} n=${n}">▶</button>` : ''}</td>`;
      }).join('') + '</tr>';
    }
    const T = document.getElementById('inst'); T.innerHTML = h;
    T.onclick = (e) => { const b = e.target.closest('button'); if (!b) return; T.querySelectorAll('tr').forEach(r => r.classList.remove('sel')); b.closest('tr').classList.add('sel'); play(b.dataset.file); };
    const first = [...T.querySelectorAll('button')].reverse().find(b => /harden/.test(b.dataset.file)) || T.querySelector('button');
    if (first) { T.querySelectorAll('tr').forEach(r => r.classList.remove('sel')); first.closest('tr').classList.add('sel'); play(first.dataset.file); }
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
  route();
})();
