// Loads the projected ledger data shipped with the site.
window.SiteData = {
  async load() {
    if (this._d) return this._d;
    const get = (u) => fetch(u).then(r => r.json());
    const [families, cells, ledger, replays, meta] = await Promise.all([get('data/families.json'), get('data/cells.json'), get('data/ledger.json'), get('data/replays.json'), get('data/meta.json')]);
    this._d = { families, cells, ledger, replays, ...meta };
    return this._d;
  },
  replayFile(D, c) { // best-run replay for a cell
    const name = `${c.family}_n${c.n}_${c.method}_B${c.budget}_${c.config}`;
    const r = D.replays.find(x => x.campaign === c.campaign && !x.hit && x.name === name);
    return r ? r.file : null;
  },
};
