"""Projections of the ledger: everything a reader sees is regenerated from it.

    python3 -m packing.project

Writes
  campaigns/<C>/REPORT.md      plan, decision, findings, per-instance table
  JOURNAL.md                   the research story in order: campaigns, decisions, findings, claims
  README.md                    the block between <!-- results:start --> and <!-- results:end -->
  site/data/*.json             data for the site (families, instances, cells, claims, replay index)
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
        o = out[c['cell']]
        o['lowest'] = min(o['best_L'], o['best_polished']) if o['best_polished'] is not None else o['best_L']
    # within each (campaign, family, n, budget): which methods attain the lowest size of all methods
    groups = defaultdict(list)
    for o in out.values():
        groups[(o['campaign'], o['family'], o['n'], o['budget'])].append(o)
    for g in groups.values():
        lo = min(o['lowest'] for o in g)
        for o in g:
            o['is_lowest'] = o['lowest'] <= lo * (1 + 1e-9) + 1e-12
            o['sole_lowest'] = o['is_lowest'] and sum(x['lowest'] <= lo * (1 + 1e-9) + 1e-12 for x in g) == 1
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
         'Every campaign was planned before it ran; amendments, exploratory analyses and post-hoc checks are marked as such. Each entry gives the question, what we expected, what happened, and what we decided. Later findings on a campaign correct or qualify earlier ones.', '']
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


def wall(rep, st):
    """The front-page grid of replays, chosen by a fixed rule (no hand picking):
    2D: from C07, per family the four largest n (two for the disk control) whose best harden run reached the best known value (fewer if
    not enough), shown as harden, plus the largest other such n for grow (not for disks); 3D: C05 cubes, harden n = 9..14 and grow
    n = 12, 13 (tuned2d settings). Order is a fixed shuffle so families mix."""
    import random
    best = {r['name']: r['file'] for r in rep if not r['hit']}
    reached = {}
    for c in st.values():
        if c.get('campaign') == 'C07-breadth-best':
            reached[(c['family'], c['n'], c['method'].replace('-best', ''))] = bool(c.get('solved'))
    out = []
    fams = sorted({f for f, n, m in reached})
    for f in fams:
        ns = sorted({n for (g, n, m), ok in reached.items() if g == f and m == 'harden' and ok}, reverse=True)
        ns = [n for n in ns if n >= 6][:2 if f == 'cir-in-squ' else 4]  # disks: hardening changes nothing, two suffice
        for n in ns:
            name = f'{f}_n{n}_harden-best_B1_default'
            if name in best:
                out.append({'file': best[name], 'family': f, 'n': n, 'method': 'harden', 'dim': 2})
        gs = sorted({n for (g, n, m), ok in reached.items() if g == f and m == 'grow' and ok and n not in ns[:1]}, reverse=True)
        for n in gs[:0 if f == 'cir-in-squ' else 1]:
            name = f'{f}_n{n}_grow-best_B1_default'
            if name in best:
                out.append({'file': best[name], 'family': f, 'n': n, 'method': 'grow', 'dim': 2})
    for n, m in [(9, 'harden'), (10, 'harden'), (11, 'harden'), (12, 'harden'), (13, 'harden'), (14, 'harden'), (12, 'grow'), (13, 'grow')]:
        name = f'cub-in-cub_n{n}_{m}_B3_tuned2d'
        if name in best:
            out.append({'file': best[name], 'family': 'cub-in-cub', 'n': n, 'method': m, 'dim': 3})
    random.Random(11).shuffle(out)
    return out


def summary(rep, st):
    """Front-page headline numbers (from analysis/*.json and the cells) and the paired replays."""
    A = lambda f: json.load(open(os.path.join(ROOT, 'analysis', f))) if os.path.exists(os.path.join(ROOT, 'analysis', f)) else {}
    c7 = [c for c in st.values() if c['campaign'] == 'C07-breadth-best']
    cnt = lambda fam, m, k: sum(1 for c in c7 if (fam is None or c['family'] == fam) and c['method'] == m + '-best' and c.get(k))
    ab, dec, ref = A('ablations.json'), A('C15.json'), A('C14.json')
    out = {'C07': {'instances': len({(c['family'], c['n']) for c in c7}), 'lowest': {m: cnt(None, m, 'is_lowest') for m in METHODS},
                   'squ': {'N': len({c['n'] for c in c7 if c['family'] == 'squ-in-squ'}), 'harden_lowest': cnt('squ-in-squ', 'harden', 'is_lowest'),
                           'harden_sole': cnt('squ-in-squ', 'harden', 'sole_lowest'), 'rigid_lowest': cnt('squ-in-squ', 'rigid', 'is_lowest')}}}
    if 'C16-squares-long' in ab:
        L = ab['C16-squares-long']
        out['C16'] = {'N': L['N'], 'harden_only': L['reached_only']['harden'], 'sa_only': L['reached_only']['sa'], 'repeats': [19, 28, 29],
                      'reached': L['reached'], 'lowest': L['lowest']}
    if 'C11-snap' in ab:
        out['C11'] = {k: ab['C11-snap']['families'][k]['harden_vs_snap'] for k in ('squ-in-squ', 'tri-in-tri')}
        out['C11']['snap_vs_rigid'] = ab['C11-snap']['all']['snap_vs_rigid']
    if 'C12-grow-area' in ab:
        out['C12'] = {'area_vs_rigid': ab['C12-grow-area']['all']['grow-area_vs_rigid']}
    if dec:
        out['C15'] = {'N': len(dec['instances']), 'harden_vs_rigid': dec['harden_vs_rigid'], 'pilot_vs_rigid': dec['pilot_vs_rigid'], 'reached': dec['reached']}
    if ref:
        out['C14'] = ref
    have = {r['name']: r['file'] for r in rep if not r['hit']}
    pairs = []
    for cid, f, n, B, why in [('C07-breadth-best', 'squ-in-squ', 19, 1, 'Wainwright\'s packing: only hardening reaches it'),
                              ('C16-squares-long', 'squ-in-squ', 26, 10, 'at 10x budget only hardening reaches the best known packing'),
                              ('C07-breadth-best', 'tri-in-tri', 12, 1, 'triangles: rigid starts reach the best known packing, hardening does not'),
                              ('C15-heldout-decision', 'pen-in-squ', 19, 1, 'held-out pentagons: rigid starts reach the best known packing, hardening does not')]:
        hf, rf = have.get(f'{f}_n{n}_harden-best_B{B}_default'), have.get(f'{f}_n{n}_rigid-best_B{B}_default')
        if hf and rf:
            pairs.append({'campaign': cid, 'family': f, 'n': n, 'why': why, 'harden': hf, 'rigid': rf})
    out['pairs'] = pairs
    return out


def site_data(camps, st, claims, finds):
    d = os.path.join(ROOT, 'site', 'data')
    os.makedirs(d, exist_ok=True)
    fams = {}
    for f in glob.glob(os.path.join(ROOT, 'catalog', '*.json')):
        F = json.load(open(f))
        fams[F['family']] = dict({k: F[k] for k in ('family', 'title', 'dim', 'piece', 'container', 'measure', 'sources')}, heldout=bool(F.get('heldout')))
    json.dump(fams, open(os.path.join(d, 'families.json'), 'w'), indent=1)
    json.dump(list(st.values()), open(os.path.join(d, 'cells.json'), 'w'))
    json.dump({'campaigns': camps, 'findings': finds, 'claims': claims}, open(os.path.join(d, 'ledger.json'), 'w'), indent=1)
    rep = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'campaigns', '*', 'replays', '*.json')) + glob.glob(os.path.join(ROOT, 'campaigns', '*', 'replays', 'hits', '*.json'))):
        rel = os.path.relpath(f, ROOT)
        m = re.match(r'campaigns/([^/]+)/replays/(hits/)?(.+)\.json', rel)
        rep.append({'campaign': m.group(1), 'hit': bool(m.group(2)), 'file': rel, 'name': m.group(3)})
    json.dump(rep, open(os.path.join(d, 'replays.json'), 'w'))
    json.dump(wall(rep, st), open(os.path.join(d, 'wall.json'), 'w'), indent=0)
    json.dump(summary(rep, st), open(os.path.join(d, 'summary.json'), 'w'), indent=1)
    total = 0
    for f in glob.glob(os.path.join(ROOT, 'campaigns', '*', 'runs*.jsonl')):
        total += sum(1 for line in open(f) if line.strip())
    main = 'C07-breadth-best' if 'C07-breadth-best' in camps else ('C04-breadth' if 'C04-breadth' in camps else sorted(camps)[-1])
    json.dump({'mainCampaign': main, 'totalRuns': total}, open(os.path.join(d, 'meta.json'), 'w'))


def readme_headline():
    S = json.load(open(os.path.join(ROOT, 'site', 'data', 'summary.json')))
    L = ['*(generated by `python3 -m packing.project`; do not edit)*', '']
    J = lambda c: f"[{c.split('-')[0]}](https://yoheinakajima.github.io/soft-to-rigid/journal.html#{c})"
    if 'C07' in S:
        c = S['C07']
        L.append(f"1. **Not a better default.** Tuned with comparable effort, rigid starts reach the lowest container size on {c['lowest']['rigid']} of {c['instances']} instances, hardening on {c['lowest']['harden']} ({J('C07-breadth-best')}).")
        if 'C16' in S:
            new = [n for n in S['C16']['harden_only'] if n not in S['C16']['repeats']]
            L.append(f"2. **A different search.** On squares in a square hardening is lowest on {c['squ']['harden_lowest']} of {c['squ']['N']} instances and the only search that low on {c['squ']['harden_sole']}, including Trump's n = 11 and Wainwright's n = 19; at ten times the budget it alone reaches the best known packing for n = {' and '.join(map(str, new))} ({J('C16-squares-long')}).")
    if 'C11' in S and 'C12' in S:
        a, b = S['C11']['snap_vs_rigid'], S['C12']['area_vs_rigid']
        L.append(f"3. **Consistent with the gradual rounding, not proven.** Compressing disks then switching to polygons at once ({J('C11-snap')}), or growing rigid polygons along hardening's area schedule ({J('C12-grow-area')}), shows no detectable difference from rigid starts ({a['a_lower']}:{a['b_lower']} and {b['a_lower']}:{b['b_lower']} instances lower); the pre-registered test on squares is inconclusive.")
    if 'C15' in S:
        h = S['C15']['harden_vs_rigid']
        L.append(f"4. **It has a cost.** On four families held out from development, hardening is lower than rigid starts on {h['a_lower']} instances and higher on {h['b_lower']}; a short pilot that picks the path per instance does no better than always starting rigid ({J('C15-heldout-decision')}).")
    rp = os.path.join(ROOT, 'README.md'); s = open(rp).read()
    if '<!-- headline:start -->' in s:
        a, z = s.index('<!-- headline:start -->') + len('<!-- headline:start -->'), s.index('<!-- headline:end -->')
        open(rp, 'w').write(s[:a] + '\n' + '\n'.join(L) + '\n' + s[z:])


def readme_block(st, claims):
    import json as _j
    p = os.path.join(ROOT, 'analysis', 'C07-breadth-best.json')
    if not os.path.exists(p):
        return
    b = _j.load(open(p)); T = b['totals']['all']
    L = ['*(generated by `python3 -m packing.project` from the ledger; do not edit)*', '',
         f"Main comparison (campaign C07, {b['instances']} instances, 32 runs per method, matched budget, every method tuned for its lowest point). "
         'For each method: instances where its lowest container size is the lowest of all five methods (in brackets: the only one that low), and instances where it reaches the best known value.', '',
         '| family | ' + ' | '.join(METHODS) + ' |', '|---|' + '---|' * len(METHODS)]
    for f, row in b['per_family'].items():
        L.append(f'| {f} | ' + ' | '.join(f"{row[m]['lowest']} ({row[m]['sole_lowest']})" for m in METHODS) + ' |')
    top = max(T[m]['lowest'] for m in METHODS)
    L.append('| **all, lowest** | ' + ' | '.join((f"**{T[m]['lowest']}**" if T[m]['lowest'] == top else str(T[m]['lowest'])) + f" ({T[m]['sole_lowest']})" for m in METHODS) + ' |')
    L.append('| **all, best known reached** | ' + ' | '.join(str(T[m]['solved']) for m in METHODS) + ' |')
    L += ['', f"Certified packings below a published value: {len(claims)}." + ('' if claims else ' (The n = 12 cube record is in the earlier repository.)')]
    rp = os.path.join(ROOT, 'README.md'); s = open(rp).read()
    a, z = s.index('<!-- results:start -->') + len('<!-- results:start -->'), s.index('<!-- results:end -->')
    open(rp, 'w').write(s[:a] + '\n' + '\n'.join(L) + '\n' + s[z:])


def planned_only(camps):
    """Campaigns that made no new runs (e.g. C14, tightening only) are never ingested; list them from their plans,
    with any decision recorded in ledger/notes.jsonl."""
    notes = [json.loads(l) for l in open(os.path.join(ROOT, 'ledger', 'notes.jsonl')) if l.strip()]
    for f in sorted(glob.glob(os.path.join(ROOT, 'campaigns', '*', 'plan.json'))):
        cid = os.path.basename(os.path.dirname(f))
        if cid in camps:
            continue
        p = json.load(open(f))
        dec = [n['decision'] for n in notes if n.get('type') == 'campaign.closed' and n.get('campaign') == cid]
        camps[cid] = {'cid': cid, 'title': p.get('title'), 'question': p.get('question'), 'hypothesis': p.get('hypothesis'),
                      'decision_rule': p.get('decision_rule'), 'created': p.get('created'),
                      'status': 'closed (analysis of existing runs, no new runs)' if dec else 'planned', 'decision': dec[-1] if dec else None}
        fs = [n['text'] for n in notes if n.get('type') == 'finding.recorded' and n.get('campaign') == cid]
        a = os.path.join('analysis', cid.split('-')[0] + '.json')
        open(os.path.join(ROOT, 'campaigns', cid, 'REPORT.md'), 'w').write('\n'.join(
            [f"# {cid}: {p.get('title')}", '', '*Generated by `packing/project.py`. This campaign made no new runs; it re-analyses existing ones.*', '',
             f"**Question.** {p.get('question')}", '', f"**Expected.** {p.get('hypothesis')}", '', f"**Rule.** {p.get('decision_rule')}", '']
            + [f"**Found.** {t}\n" for t in fs] + ([f"**Decided.** {dec[-1]}", ''] if dec else [])
            + ([f"Numbers: [`{a}`](../../{a})."] if os.path.exists(os.path.join(ROOT, a)) else [])) + '\n')
    return camps


def main():
    camps, cells, cands, finds, claims, nev = load()
    camps = planned_only(camps)
    st = cell_status(cells, cands)
    for cid, c in camps.items():
        if os.path.isdir(os.path.join(ROOT, 'campaigns', cid)) and any(x['campaign'] == cid for x in st.values()):
            campaign_report(cid, c, st, finds)
    journal(camps, finds, claims, nev)
    site_data(camps, st, claims, finds)
    readme_block(st, claims)
    readme_headline()
    print(f'projected {len(camps)} campaigns, {len(st)} cells, {len(finds)} findings, {len(claims)} claims')


if __name__ == '__main__':
    main()
