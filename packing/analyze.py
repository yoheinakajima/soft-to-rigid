"""Analyses quoted in the paper, computed from the ledger's cells (never from hand-copied numbers).

    python3 -m packing.analyze            # writes analysis/*.json, paper/numbers.tex, paper/tables/*.tex

Pre-registered tests (C04): one-sided sign test of harden vs each other method over instances solved by
exactly one of the two. Everything else here is descriptive.
"""
import json, math, os, statistics as S
from collections import defaultdict
from .project import load, cell_status
from .ledger import ROOT

METHODS = ['harden', 'grow', 'rigid', 'sa', 'pc']


def sign_test(a_only, b_only):
    """one-sided P(X >= a_only) for X ~ Bin(a_only + b_only, 1/2)."""
    n = a_only + b_only
    if n == 0:
        return 1.0
    return sum(math.comb(n, k) for k in range(a_only, n + 1)) / 2 ** n


def breadth(st, cid='C04-breadth', methods=None):
    cells = [dict(c, method=c['method'].replace('-best', '')) for c in st.values() if c['campaign'] == cid]
    if not cells:
        return None
    fams = sorted({c['family'] for c in cells})
    inst = sorted({(c['family'], c['n']) for c in cells})
    by = {(c['family'], c['n'], c['method']): c for c in cells}
    out = {'campaign': cid, 'instances': len(inst), 'families': fams, 'per_family': {}, 'totals': {}, 'sign_tests': {}, 'unique': {}}
    for f in fams + ['all']:
        I = [i for i in inst if f == 'all' or i[0] == f]
        row = {}
        for m in METHODS:
            cs = [by[(i[0], i[1], m)] for i in I if (i[0], i[1], m) in by]
            if not cs:
                continue
            rel = [c['median_gap'] / c['record'] for c in cs if c['median_gap'] is not None]
            row[m] = {'instances': len(cs), 'solved': sum(c['solved'] for c in cs), 'below': sum(c['below'] for c in cs),
                      'lowest': sum(c['is_lowest'] for c in cs), 'sole_lowest': sum(c['sole_lowest'] for c in cs),
                      'raw_hits': sum(c['hits_1e3'] for c in cs), 'runs': sum(c['runs'] for c in cs),
                      'median_relgap': S.median(rel) if rel else None, 'ms_mean': S.mean(c['ms_mean'] for c in cs)}
        out['per_family' if f != 'all' else 'totals'][f] = row
    for m in METHODS[1:]:
        a = b = 0
        for i in inst:
            h, o = by.get((i[0], i[1], 'harden')), by.get((i[0], i[1], m))
            if not h or not o:
                continue
            a += h['solved'] and not o['solved']
            b += o['solved'] and not h['solved']
        out['sign_tests'][m] = {'harden_only': a, 'other_only': b, 'p_harden_better': sign_test(a, b), 'p_other_better': sign_test(b, a)}
    for i in inst:
        solvers = [m for m in METHODS if by.get((i[0], i[1], m), {}).get('solved')]
        key = solvers[0] if len(solvers) == 1 else ('none' if not solvers else None)
        if key:
            out['unique'].setdefault(key, []).append(f'{i[0]}/n{i[1]}')
    # per-n difficulty: how many methods solve each instance, by family
    out['solved_by_count'] = {f'{i[0]}/n{i[1]}': sum(by.get((i[0], i[1], m), {}).get('solved', False) for m in METHODS) for i in inst}
    return out


FAMS = ['squ-in-squ', 'squ-in-cir', 'squ-in-tri', 'tri-in-tri', 'tri-in-squ', 'hex-in-squ', 'cir-in-squ']
FAMNAME = {'squ-in-squ': 'squares in square', 'squ-in-cir': 'squares in circle', 'squ-in-tri': 'squares in triangle',
           'tri-in-tri': 'triangles in triangle', 'tri-in-squ': 'triangles in square', 'hex-in-squ': 'hexagons in square',
           'cir-in-squ': 'circles in square (control)'}


def table_lowest(b, label, caption):
    """LaTeX table: per family, for each method 'lowest (only)'; last row totals; plus solved row."""
    L = [r'\begin{table}[t]\centering\small', r'\begin{tabular}{lr' + 'c' * len(METHODS) + '}', r'\toprule',
         'family & $N$ & ' + ' & '.join(r'\textbf{%s}' % m for m in METHODS) + r' \\', r'\midrule']
    for f in FAMS:
        row = b['per_family'].get(f)
        if not row:
            continue
        N = row['harden']['instances']
        best = max(row[m]['lowest'] for m in METHODS)
        cells = []
        for m in METHODS:
            v = row[m]
            t = f"{v['lowest']}" + (f" ({v['sole_lowest']})" if v['sole_lowest'] else '')
            cells.append(r'\textbf{%s}' % t if v['lowest'] == best else t)
        L.append(f'{FAMNAME[f]} & {N} & ' + ' & '.join(cells) + r' \\')
    T = b['totals']['all']; best = max(T[m]['lowest'] for m in METHODS)
    L.append(r'\midrule')
    L.append(f"all & {b['instances']} & " + ' & '.join((r'\textbf{%s}' if T[m]['lowest'] == best else '%s') % (f"{T[m]['lowest']} ({T[m]['sole_lowest']})") for m in METHODS) + r' \\')
    L.append(f"reached best known & & " + ' & '.join(str(T[m]['solved']) for m in METHODS) + r' \\')
    L += [r'\bottomrule', r'\end{tabular}', r'\caption{' + caption + '}', r'\label{' + label + '}', r'\end{table}']
    return '\n'.join(L) + '\n'


def macros(prefix, b):
    out = []
    T = b['totals']['all']
    for m in METHODS:
        M = m.capitalize()
        out.append(rf'\newcommand{{\{prefix}{M}Lowest}}{{{T[m]["lowest"]}}}')
        out.append(rf'\newcommand{{\{prefix}{M}Sole}}{{{T[m]["sole_lowest"]}}}')
        out.append(rf'\newcommand{{\{prefix}{M}Solved}}{{{T[m]["solved"]}}}')
    for m, t in b['sign_tests'].items():
        M = m.capitalize()
        out.append(rf'\newcommand{{\{prefix}Sign{M}}}{{{t["harden_only"]} vs {t["other_only"]}}}')
        p = min(t['p_harden_better'], t['p_other_better'])
        out.append(rf'\newcommand{{\{prefix}SignP{M}}}{{{p:.2g}}}')
    out.append(rf'\newcommand{{\{prefix}Instances}}{{{b["instances"]}}}')
    out.append(rf'\newcommand{{\{prefix}Unsolved}}{{{len(b["unique"].get("none", []))}}}')
    for f in FAMS:
        row = b['per_family'].get(f)
        if row:
            F = ''.join(w.capitalize() for w in f.split('-'))
            for m in ('harden', 'rigid', 'grow'):
                out.append(rf'\newcommand{{\{prefix}{F}{m.capitalize()}Lowest}}{{{row[m]["lowest"]}}}')
                out.append(rf'\newcommand{{\{prefix}{F}{m.capitalize()}Sole}}{{{row[m]["sole_lowest"]}}}')
            out.append(rf'\newcommand{{\{prefix}{F}N}}{{{row["harden"]["instances"]}}}')
    return out


def main():
    camps, cells, cands, finds, claims, nev = load()
    st = cell_status(cells, cands)
    os.makedirs(os.path.join(ROOT, 'analysis'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'paper', 'tables'), exist_ok=True)
    import time as _t
    nums = [r'\newcommand{\builtdate}{%s}' % _t.strftime('%-d %B %Y'), r'\newcommand{\totalruns}{%s}' % f"{sum(c['runs'] for c in st.values()):,}".replace(',', '{,}'),
            r'\newcommand{\ncampaigns}{%d}' % len(camps)]
    for cid, prefix, cap in (('C04-breadth', 'Cfour', 'Settings tuned by median gap (C04). Same layout as Table~\\ref{tab:main}.'),
                             ('C07-breadth-best', 'Cseven', 'Lowest point by family (C07; every method tuned for its lowest point, 32 runs per instance, equal budget). Each cell: number of instances on which the method\\textquotesingle s lowest tightened size is the lowest of all five methods; in brackets, on how many it is the only method that low. Bold: most per family.')):
        b = breadth(st, cid)
        if not b:
            continue
        json.dump(b, open(os.path.join(ROOT, 'analysis', cid + '.json'), 'w'), indent=1)
        T = b['totals']['all']
        print(cid, {m: (T[m]['lowest'], T[m]['sole_lowest'], T[m]['solved']) for m in T}, b['sign_tests'])
        nums += macros(prefix, b)
        open(os.path.join(ROOT, 'paper', 'tables', cid + '.tex'), 'w').write(
            table_lowest(b, 'tab:main' if cid.startswith('C07') else 'tab:median', cap.replace('\\\\', '\\')))
    cub = [c for c in st.values() if c['campaign'] == 'C05-cubes']
    if cub:
        ns = sorted({c['n'] for c in cub}); cfgs = ['original', 'tuned2d']; ms = ['harden', 'grow', 'rigid']
        by = {(c['n'], c['method'], c['config']): c for c in cub}
        L = [r'\begin{table}[t]\centering\small', r'\begin{tabular}{rr' + 'r' * 6 + '}', r'\toprule',
             r' & & \multicolumn{3}{c}{original settings} & \multicolumn{3}{c}{2D-tuned settings}\\',
             r'$n$ & best known & ' + ' & '.join(ms + ms) + r'\\', r'\midrule']
        for n in ns:
            rec = next(c['record'] for c in cub if c['n'] == n)
            vals = [by.get((n, m, cf)) for cf in cfgs for m in ms]
            lo = min(v['lowest'] for v in vals if v)
            cells = []
            for v in vals:
                if not v: cells.append(''); continue
                t = f"{v['lowest']:.5f}"
                cells.append((r'\textbf{%s}' % t if v['lowest'] <= lo * (1 + 1e-9) else t) + ('$^*$' if v['below'] else ''))
            L.append(f'{n} & {rec:.5f} & ' + ' & '.join(cells) + r'\\')
        L += [r'\bottomrule', r'\end{tabular}', r'\caption{Cubes in a cube (C05): lowest side over 32 runs at the record budget, after tightening. Bold: lowest in the row; $^*$: below the best known value.}', r'\label{tab:cubes}', r'\end{table}']
        open(os.path.join(ROOT, 'paper', 'tables', 'C05-cubes.tex'), 'w').write('\n'.join(L) + '\n')
        below = sorted({(c['n'], c['method'], c['config']) for c in cub if c['below']})
        def best(m):
            return min((c['lowest'] for c in cub if c['n'] == 12 and c['method'] == m), default=float('nan'))
        nums.append(r'\newcommand{\CubesHardenTwelve}{%.6f}' % best('harden'))
        nums.append(r'\newcommand{\CubesRigidTwelve}{%.6f}' % best('rigid'))
        nums.append(r'\newcommand{\CubesGrowTwelve}{%.6f}' % best('grow'))
        nums.append(r'\newcommand{\CubesBelow}{%s}' % (', '.join(f'n = {n} ({m}, {cf})' for n, m, cf in below) or 'none'))
    nums += extra_campaigns(st)
    open(os.path.join(ROOT, 'paper', 'numbers.tex'), 'w').write('\n'.join(nums) + '\n')


if __name__ == '__main__':
    main()


def extra_campaigns(st):
    """C08 (start shape), C09 (budget), C10 (portfolio): tables and macros."""
    nums = []
    tabdir = os.path.join(ROOT, 'paper', 'tables')
    # ---- C08: which tau0 reaches the lowest size, per family
    c8 = [c for c in st.values() if c['campaign'] == 'C08-start-shape']
    if c8:
        taus = ['tau1', 'tau0.5', 'tau0.25', 'tau0']
        groups = defaultdict(dict)
        for c in c8:
            groups[(c['family'], c['n'])][c['config']] = c['lowest']
        fams = [f for f in FAMS if any(k[0] == f for k in groups)]
        cnt = {f: {t: 0 for t in taus} for f in fams}
        for (f, n), d in groups.items():
            lo = min(d.values())
            for t in taus:
                if t in d and d[t] <= lo * (1 + 1e-9):
                    cnt[f][t] += 1
        L = [r'\begin{table}[t]\centering\small', r'\begin{tabular}{lrrrrr}', r'\toprule',
             r'family & instances & $\tau_0=1$ (harden) & $0.5$ & $0.25$ & $0$ (rigid)\\', r'\midrule']
        tot = {t: 0 for t in taus}; ni = 0
        for f in fams:
            k = sum(1 for g in groups if g[0] == f); ni += k
            L.append(f'{FAMNAME[f]} & {k} & ' + ' & '.join(str(cnt[f][t]) for t in taus) + r'\\')
            for t in taus: tot[t] += cnt[f][t]
        L += [r'\midrule', f'all & {ni} & ' + ' & '.join(str(tot[t]) for t in taus) + r'\\', r'\bottomrule', r'\end{tabular}',
              r'\caption{How soft the start must be (C08): on the 40 most contested instances of C07, the number of instances where each starting softness $\tau_0$ reaches the lowest size (32 runs each, all other settings equal; ties counted for every tied value).}',
              r'\label{tab:tau}', r'\end{table}']
        open(os.path.join(tabdir, 'C08-start-shape.tex'), 'w').write('\n'.join(L) + '\n')
        for t in taus:
            nums.append(r'\newcommand{\Ctau%s}{%d}' % (t.replace('tau', '').replace('.', 'p').replace('1', 'One').replace('0p5', 'Half').replace('0p25', 'Quarter').replace('0', 'Zero'), tot[t]))
        nums.append(r'\newcommand{\CtauN}{%d}' % ni)
        sq = cnt.get('squ-in-squ'); tri = {t: cnt.get('tri-in-squ', {}).get(t, 0) + cnt.get('tri-in-tri', {}).get(t, 0) for t in taus}
        if sq: nums.append(r'\newcommand{\CtauSquares}{%s}' % ', '.join(f'{cnt["squ-in-squ"][t]}' for t in taus))
        nums.append(r'\newcommand{\CtauTriangles}{%s}' % ', '.join(str(tri[t]) for t in taus))
    # ---- C09: budget
    c9 = [c for c in st.values() if c['campaign'] == 'C09-budget']
    c7 = {(c['family'], c['n'], c['method']): c for c in st.values() if c['campaign'] == 'C07-breadth-best'}
    if c9:
        insts = sorted({(c['family'], c['n']) for c in c9})
        rows = []
        for B in (1, 3, 10):
            h = r = solvedH = solvedR = 0
            for f, n in insts:
                if B == 1:
                    ch, cr = c7.get((f, n, 'harden-best')), c7.get((f, n, 'rigid-best'))
                else:
                    ch = next((c for c in c9 if c['family'] == f and c['n'] == n and c['budget'] == B and c['method'] == 'harden-best'), None)
                    cr = next((c for c in c9 if c['family'] == f and c['n'] == n and c['budget'] == B and c['method'] == 'rigid-best'), None)
                if not ch or not cr:
                    continue
                lo = min(ch['lowest'], cr['lowest'])
                h += ch['lowest'] <= lo * (1 + 1e-9); r += cr['lowest'] <= lo * (1 + 1e-9)
                solvedH += ch['solved']; solvedR += cr['solved']
            rows.append((B, h, r, solvedH, solvedR))
            nums.append(r'\newcommand{\Cbudget%sHarden}{%d}\newcommand{\Cbudget%sRigid}{%d}' % ({1: 'One', 3: 'Three', 10: 'Ten'}[B], h, {1: 'One', 3: 'Three', 10: 'Ten'}[B], r))
        L = [r'\begin{table}[t]\centering\small', r'\begin{tabular}{rrrrr}', r'\toprule',
             r'budget & harden lowest & rigid lowest & harden reaches best known & rigid reaches best known\\', r'\midrule']
        L += [f'{B}$\times$ & {h} & {r} & {a} & {b}' + r'\\' for B, h, r, a, b in rows]
        L += [r'\bottomrule', r'\end{tabular}', r'\caption{Longer schedules (C09) on the 20 most contested instances: number of instances where each path reaches the lower of the two lowest sizes (ties counted for both), and where it reaches the best known value. Budget 1 is C07 (32 runs); budgets 3 and 10 use 16 runs.}', r'\label{tab:budget}', r'\end{table}']
        open(os.path.join(tabdir, 'C09-budget.tex'), 'w').write('\n'.join(L) + '\n')
        nums.append(r'\newcommand{\CbudgetN}{%d}' % len(insts))
    # ---- C10: portfolio
    c10 = {(c['family'], c['n']): c for c in st.values() if c['campaign'] == 'C10-portfolio'}
    if c10:
        insts = sorted(c10)
        def solved(f, n, m): return c7[(f, n, m)]['solved']
        r64 = sum(solved(f, n, 'rigid-best') or c10[(f, n)]['solved'] for f, n in insts)
        rh = sum(solved(f, n, 'rigid-best') or solved(f, n, 'harden-best') for f, n in insts)
        rg = sum(solved(f, n, 'rigid-best') or solved(f, n, 'grow-best') for f, n in insts)
        a = sum((solved(f, n, 'rigid-best') or solved(f, n, 'harden-best')) and not (solved(f, n, 'rigid-best') or c10[(f, n)]['solved']) for f, n in insts)
        b = sum((solved(f, n, 'rigid-best') or c10[(f, n)]['solved']) and not (solved(f, n, 'rigid-best') or solved(f, n, 'harden-best')) for f, n in insts)
        p = sign_test(a, b)
        nums += [r'\newcommand{\PortRigidSixtyFour}{%d}' % r64, r'\newcommand{\PortRigidHarden}{%d}' % rh, r'\newcommand{\PortRigidGrow}{%d}' % rg,
                 r'\newcommand{\PortSign}{%d vs %d}' % (a, b), r'\newcommand{\PortP}{%.2g}' % p]
        json.dump({'rigid64': r64, 'rigid32+harden32': rh, 'rigid32+grow32': rg, 'mixed_only': a, 'rigid64_only': b, 'p': p},
                  open(os.path.join(ROOT, 'analysis', 'C10-portfolio.json'), 'w'), indent=1)
        print('C10', r64, rh, rg, a, b, p)
    return nums
