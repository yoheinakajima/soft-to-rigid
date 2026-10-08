"""Projections of the ledger: everything a reader sees is regenerated from it.

    python3 -m packing.project

Writes
  campaigns/<C>/REPORT.md      plan, decision, findings, per-instance table
  JOURNAL.md                   the research story in order: campaigns, decisions, findings, claims
  README.md                    the block between <!-- results:start --> and <!-- results:end -->
  docs/data/*.json             data for the site (families, instances, cells, claims, replay index)
  paper/numbers.tex            \\newcommand macros for every number quoted in the paper
"""
import glob, json, math, os, re, statistics as S
from collections import defaultdict
from .ledger import ROOT, open_ledger

METHODS = ['harden', 'grow', 'rigid', 'sa', 'pc']
SOLVED = ('matches record', 'below record')


def load():
    rt, G = open_ledger()
    camps = {o.data['cid']: o.data for o in G.objects('campaign')}
    cells = [o.data for o in G.objects('cell')]
    cands = [o.data for o in G.objects('candidate')]
    finds = [o.data for o in G.objects('finding')]
    claims = [o.data for o in G.objects('claim')]
    return camps, cells, cands, finds, claims, len(G.events)


def cell_status(cells, cands):
    by = defaultdict(list)
    for c in cands:
        by[c['cell']].append(c)
    out = {}
    for c in cells:
        cs = by.get(c['cell'], [])
        pol = [x for x in cs if x.get('L_polished') is not None]
        out[c['cell']] = dict(c, solved=any(x.get('verdict') in SOLVED for x in cs),
                              below=any(x.get('verdict') == 'below record' for x in cs),
                              best_polished=min((x['L_polished'] for x in pol), default=None),
                              tightened=len(pol))
    return out


def fmt_gap(g):
    if g is None:
        return ''
    if abs(g) < 1e-9:
        return '0'
    return f'{g:.1e}' if abs(g) < 1e-3 else f'{g:.4f}'


def campaign_report(cid, camp, st, finds):
    rows = [c for c in st.values() if c['campaign'] == cid]
    lines = [f"# {cid}: {camp['title']}", '', f"*Generated from the ledger by `packing/project.py`. Do not edit.*", '',
             f"**Question.** {camp['question']}", '', f"**Hypothesis.** {camp.get('hypothesis') or '—'}", '',
             f"**Decision rule (pre-registered {camp.get('created')}).** {camp['decision_rule']}", '',
             f"**Status.** {camp.get('status')}" + (f" — **decision:** {camp['decision']}" if camp.get('decision') else ''), '']
    fs = [f for f in finds if f.get('campaign') == cid]
    if fs:
        lines += ['## Findings', ''] + [f"- {f['text']}" for f in fs] + ['']
    insts = sorted({(c['family'], c['n']) for c in rows})
    meths = [m for m in METHODS if any(c['method'] == m for c in rows)] + sorted({c['method'] for c in rows} - set(METHODS))
    configs = sorted({c['config'] for c in rows})
    budgets = sorted({c['budget'] for c in rows})
    lines += ['## Results', '', 'Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.', '']
    for B in budgets:
        for cf in configs:
            sub = [c for c in rows if c['budget'] == B and c['config'] == cf]
            if not sub:
                continue
            if len(configs) > 1 or len(budgets) > 1:
                lines += [f'### budget {B}, setting `{cf}`', '']
            lines += ['| instance | best known | ' + ' | '.join(meths) + ' |', '|---|---|' + '---|' * len(meths)]
            for fam, n in insts:
                cs = {c['method']: c for c in sub if c['family'] == fam and c['n'] == n}
                if not cs:
                    continue
                rec = next(iter(cs.values())).get('record')
                cells_txt = []
                for m in meths:
                    c = cs.get(m)
                    if not c:
                        cells_txt.append('')
                        continue
                    mark = ('✓ ' if c['solved'] else '') + ('**below** ' if c['below'] else '')
                    cells_txt.append(f"{mark}{c['hits_1e3']}/{c['runs']} · {fmt_gap(c['best_gap'])} · {fmt_gap(c['median_gap'])}")
                lines.append(f"| {fam} n={n} | {rec:.6f} | " + ' | '.join(cells_txt) + ' |')
            lines.append('')
    open(os.path.join(ROOT, 'campaigns', cid, 'REPORT.md'), 'w').write('\n'.join(lines) + '\n')


def journal(camps, finds, claims, nevents):
    L = ['# Journal', '', '*Generated from the ledger (`ledger/events.jsonl`, ' + str(nevents) + ' events) by `packing/project.py`. Do not edit.*', '',
         'Every campaign was planned before it ran. Each entry gives the question, what we expected, what happened, and what we decided.', '']
    for cid in sorted(camps):
        c = camps[cid]
        L += [f"## {cid} — {c['title']}", '', f"*Planned {c.get('created')} · status: {c.get('status')}*", '',
              f"{c['question']}", '', f"- **Expected:** {c.get('hypothesis') or '—'}", f"- **Rule:** {c['decision_rule']}"]
        for f in finds:
            if f.get('campaign') == cid:
                L.append(f"- **Found:** {f['text']}")
        if c.get('decision'):
            L.append(f"- **Decided:** {c['decision']}")
        L += ['', f"[Full report](campaigns/{cid}/REPORT.md)", '']
    if claims:
        L += ['## Claims', ''] + [f"- {c['family']} n = {c['n']}: {c['s_full']} (previous {c['record']}), [{c['folder']}]({c['folder']}/)" for c in claims]
    open(os.path.join(ROOT, 'JOURNAL.md'), 'w').write('\n'.join(L) + '\n')


def site_data(camps, st, claims, finds):
    d = os.path.join(ROOT, 'docs', 'data')
    os.makedirs(d, exist_ok=True)
    fams = {}
    for f in glob.glob(os.path.join(ROOT, 'catalog', '*.json')):
        F = json.load(open(f))
        fams[F['family']] = {k: F[k] for k in ('family', 'title', 'dim', 'piece', 'container', 'measure', 'sources')}
    json.dump(fams, open(os.path.join(d, 'families.json'), 'w'), indent=1)
    json.dump(list(st.values()), open(os.path.join(d, 'cells.json'), 'w'))
    json.dump({'campaigns': camps, 'findings': finds, 'claims': claims}, open(os.path.join(d, 'ledger.json'), 'w'), indent=1)
    rep = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'campaigns', '*', 'replays', '*.json')) + glob.glob(os.path.join(ROOT, 'campaigns', '*', 'replays', 'hits', '*.json'))):
        rel = os.path.relpath(f, ROOT)
        m = re.match(r'campaigns/([^/]+)/replays/(hits/)?(.+)\.json', rel)
        rep.append({'campaign': m.group(1), 'hit': bool(m.group(2)), 'file': rel, 'name': m.group(3)})
    json.dump(rep, open(os.path.join(d, 'replays.json'), 'w'))


def main():
    camps, cells, cands, finds, claims, nev = load()
    st = cell_status(cells, cands)
    for cid, c in camps.items():
        if os.path.isdir(os.path.join(ROOT, 'campaigns', cid)):
            campaign_report(cid, c, st, finds)
    journal(camps, finds, claims, nev)
    site_data(camps, st, claims, finds)
    print(f'projected {len(camps)} campaigns, {len(st)} cells, {len(finds)} findings, {len(claims)} claims')


if __name__ == '__main__':
    main()
