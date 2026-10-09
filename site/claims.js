(async function () {
  const D = await SiteData.load(), S = document.getElementById('claims');
  if (!D.ledger.claims.length) { S.innerHTML = '<p>No run in this study went below a published value; the best known values it reached are marked ✓ on the <a href="families.html">family pages</a>. The study is about which search finds which packings, not about records.</p><p>The packing that started it, 12 unit cubes in a cube of side 2.9315185 (below the 2.9327718 then best known), is certified in the earlier repository: <a href="https://github.com/yoheinakajima/soft-to-rigid-packing">soft-to-rigid-packing</a> (doi:10.5281/zenodo.23248095).</p>'; return; }
  S.innerHTML = D.ledger.claims.map((c, i) => `<div class="math"><div><b>${D.families[c.family].title}, n = ${c.n}</b></div>
    <div class="mono">s = ${c.s_full} · previous ${c.record} · improvement ${(c.record - c.s_full).toExponential(3)}</div>
    <div><a href="${c.folder}/claim.json">claim.json</a> · <a href="${c.folder}/verify.txt">verify.txt</a> · <a href="${c.folder}/certify.txt">certify.txt</a></div>
    <div><button class="runbtn" type="button" data-i="${i}">Check in this page</button></div><div class="out" id="o${i}"></div></div>`).join('');
  S.onclick = async (e) => { const b = e.target.closest('button'); if (!b) return; const c = D.ledger.claims[+b.dataset.i], o = document.getElementById('o' + b.dataset.i);
    const cl = await fetch(c.folder + '/claim.json').then(r => r.json()), r = cl.piece === 'cube' ? SiteViewers.verify3d(cl) : SiteViewers.verify2d(cl);
    o.innerHTML = `n = ${r.n}  s = ${r.s}\nmin wall gap = ${r.wall.toExponential(9)}\nmin pair gap = ${r.pair.toExponential(9)}\n<span class="${r.ok ? 'ok' : 'bad'}">${r.ok ? 'VALID' : 'INVALID'}</span>`; };
})();
