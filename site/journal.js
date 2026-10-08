(async function () {
  const D = await SiteData.load(), J = document.getElementById('journal');
  const esc = (s) => String(s ?? '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  J.innerHTML = Object.keys(D.ledger.campaigns).sort().map(cid => {
    const c = D.ledger.campaigns[cid], fs = D.ledger.findings.filter(f => f.campaign === cid);
    return `<article><div class="meta">${cid} · planned ${c.created} · ${c.status}</div><h3>${esc(c.title)}</h3><dl>
      <dt>Question</dt><dd>${esc(c.question)}</dd><dt>Expected</dt><dd>${esc(c.hypothesis || '—')}</dd><dt>Rule</dt><dd>${esc(c.decision_rule)}</dd>
      ${fs.map(f => `<dt>Found</dt><dd>${esc(f.text)}</dd>`).join('')}
      ${c.decision ? `<dt>Decided</dt><dd>${esc(c.decision)}</dd>` : ''}</dl>
      <p class="cap"><a href="{{REPO}}/blob/main/campaigns/${cid}/REPORT.md">report</a> · <a href="{{REPO}}/blob/main/campaigns/${cid}/plan.json">plan</a> · <a href="{{REPO}}/tree/main/campaigns/${cid}">raw runs</a></p></article>`;
  }).join('');
})();
