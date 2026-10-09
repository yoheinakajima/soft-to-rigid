"""Ablations C11 (snap), C12 (grow-area) and C13 (clean budget study), computed from raw runs and the tightening
cache under the decision rules in their plans.

    python3 -m packing.ablations      # -> analysis/ablations.json, paper/ablations.tex, paper/tables/ablations.tex

A run's size is its tightened size if tightened, else its legalised size (as packing.stats). Reached = within the
catalogue tolerance of the best known value. All p-values are exact two-sided sign tests.
"""
import glob, json, os
from collections import defaultdict
from .ledger import ROOT
from .stats import tightened, catalog_tol
from .analyze import sign_test2

FAMS = ['squ-in-squ', 'squ-in-cir', 'squ-in-tri', 'tri-in-tri', 'tri-in-squ', 'hex-in-squ', 'cir-in-squ']
SHORT = {'squ-in-squ': 'squares in square', 'squ-in-cir': 'squares in circle', 'squ-in-tri': 'squares in triangle', 'tri-in-tri': 'triangles in triangle',
         'tri-in-squ': 'triangles in square', 'hex-in-squ': 'hexagons in square', 'cir-in-squ': 'disks in square'}
MAC = {'squ-in-squ': 'SquSqu', 'squ-in-cir': 'SquCir', 'squ-in-tri': 'SquTri', 'tri-in-tri': 'TriTri', 'tri-in-squ': 'TriSqu', 'hex-in-squ': 'HexSqu', 'cir-in-squ': 'CirSqu'}


def runs(cid):
    """(family, n, method, budget) -> {seed: size}"""
    out = defaultdict(dict)
    for f in glob.glob(os.path.join(ROOT, 'campaigns', cid, 'runs*.jsonl')):
        for line in open(f):
            if not line.strip():
                continue
            r = json.loads(line)
            if 'error' in r:
                continue
            t = tightened(r['id'])
            out[(r['family'], r['n'], r['method'].replace('-best', ''), r['budget'])][r['seed']] = min(r['L'], t) if t is not None else r['L']
    return out


def low(d, seeds=None):
    v = [x for s, x in d.items() if seeds is None or s in seeds]
    return min(v) if v else None


def pairwise(A, B, insts):
    """A, B: dict inst -> lowest. Returns (A lower, B lower, ties, A-only reached, B-only reached) and p-values."""
    al = bl = ti = ar = br = 0
    for f, n in insts:
        a, b = A[(f, n)], B[(f, n)]
        rec, tol = catalog_tol(f, n)
        if a < b * (1 - 1e-9): al += 1
        elif b < a * (1 - 1e-9): bl += 1
        else: ti += 1
        ra, rb = a <= rec + tol, b <= rec + tol
        ar += ra and not rb; br += rb and not ra
    return {'a_lower': al, 'b_lower': bl, 'ties': ti, 'p_lower': sign_test2(al, bl), 'a_only_reached': ar, 'b_only_reached': br, 'p_reached': sign_test2(ar, br)}


def ablation(cid, new):
    c7, cx = runs('C07-breadth-best'), runs(cid)
    insts = sorted({(f, n) for f, n, m, B in cx})
    H = {i: low(c7[(*i, 'harden', 1)]) for i in insts}
    R = {i: low(c7[(*i, 'rigid', 1)]) for i in insts}
    X = {i: low(cx[(*i, new, 1)]) for i in insts}
    res = {'all': {'harden_vs_' + new: pairwise(H, X, insts), new + '_vs_rigid': pairwise(X, R, insts)}, 'families': {}}
    for fam in FAMS:
        I = [i for i in insts if i[0] == fam]
        if I:
            res['families'][fam] = {'N': len(I), 'harden_vs_' + new: pairwise(H, X, I), new + '_vs_rigid': pairwise(X, R, I)}
    return res


def budget():
    c7, c13 = runs('C07-breadth-best'), runs('C13-budget-clean')
    insts = sorted({(f, n) for f, n, m, B in c13})
    if not insts:
        return None
    S32 = set(range(1, 33))
    arm = {}
    for m in ('harden', 'rigid'):
        arm[(m, '1x32')] = {i: low(c7[(*i, m, 1)], S32) for i in insts}
        arm[(m, '3x32')] = {i: low(c13[(*i, m, 3)]) for i in insts}
        arm[(m, '1x96')] = {i: min(low(c7[(*i, m, 1)], S32), low(c13[(*i, m, 1)])) for i in insts}
    out = {'instances': len(insts)}
    for a in ('1x32', '3x32', '1x96'):
        out[a] = pairwise(arm[('harden', a)], arm[('rigid', a)], insts)
        for m in ('harden', 'rigid'):
            out[a][m + '_reached'] = sum(arm[(m, a)][i] <= sum(catalog_tol(*i)) for i in insts)
    for m in ('harden', 'rigid'):
        out[m + '_longer_vs_more'] = pairwise(arm[(m, '3x32')], arm[(m, '1x96')], insts)
        out[m + '_longer_vs_base'] = pairwise(arm[(m, '3x32')], arm[(m, '1x32')], insts)
    return out


def done(cid):
    """a campaign counts once all its runs are in and tightened (scripts/queue.sh logs 'done <cid>')."""
    q = os.path.join(ROOT, 'campaigns', 'queue.log')
    return os.path.exists(q) and any(l.split()[-1] == cid for l in open(q) if l.strip())


def fmt_p(p):
    return '1' if p >= 0.995 else f'{p:.2g}'


def main():
    res = {}
    nums, rows = [], []
    for cid, new, key in (('C11-snap', 'snap', 'Snap'), ('C12-grow-area', 'grow-area', 'Area')):
        if not done(cid):
            continue
        r = ablation(cid, new); res[cid] = r
        hv, xr = r['all']['harden_vs_' + new], r['all'][new + '_vs_rigid']
        nums += [rf'\newcommand{{\{key}HLower}}{{{hv["a_lower"]}}}', rf'\newcommand{{\{key}XLower}}{{{hv["b_lower"]}}}', rf'\newcommand{{\{key}Ties}}{{{hv["ties"]}}}',
                 rf'\newcommand{{\{key}P}}{{{fmt_p(hv["p_lower"])}}}', rf'\newcommand{{\{key}HOnly}}{{{hv["a_only_reached"]}}}', rf'\newcommand{{\{key}XOnly}}{{{hv["b_only_reached"]}}}',
                 rf'\newcommand{{\{key}PReached}}{{{fmt_p(hv["p_reached"])}}}',
                 rf'\newcommand{{\{key}RXLower}}{{{xr["a_lower"]}}}', rf'\newcommand{{\{key}RRLower}}{{{xr["b_lower"]}}}', rf'\newcommand{{\{key}RP}}{{{fmt_p(xr["p_lower"])}}}']
        for fam, v in r['families'].items():
            a = v['harden_vs_' + new]; b = v[new + '_vs_rigid']
            nums += [rf'\newcommand{{\{key}{MAC[fam]}}}{{{a["a_lower"]}--{a["b_lower"]}}}', rf'\newcommand{{\{key}R{MAC[fam]}}}{{{b["a_lower"]}--{b["b_lower"]}}}']
    b = budget() if done('C13-budget-clean') else None
    if b:
        res['C13-budget-clean'] = b
        for a, k in (('1x32', 'One'), ('3x32', 'Three'), ('1x96', 'More')):
            nums += [rf'\newcommand{{\Bud{k}H}}{{{b[a]["a_lower"]}}}', rf'\newcommand{{\Bud{k}R}}{{{b[a]["b_lower"]}}}', rf'\newcommand{{\Bud{k}P}}{{{fmt_p(b[a]["p_lower"])}}}',
                     rf'\newcommand{{\Bud{k}HReached}}{{{b[a]["harden_reached"]}}}', rf'\newcommand{{\Bud{k}RReached}}{{{b[a]["rigid_reached"]}}}']
        for m, k in (('harden', 'H'), ('rigid', 'R')):
            lv, lb = b[m + '_longer_vs_more'], b[m + '_longer_vs_base']
            nums += [rf'\newcommand{{\BudLvML{k}}}{{{lv["a_lower"]}}}', rf'\newcommand{{\BudLvMM{k}}}{{{lv["b_lower"]}}}', rf'\newcommand{{\BudLMP{k}}}{{{fmt_p(lv["p_lower"])}}}',
                     rf'\newcommand{{\BudGain{k}}}{{{lb["a_lower"]}}}', rf'\newcommand{{\BudLoss{k}}}{{{lb["b_lower"]}}}']
        nums.append(rf'\newcommand{{\BudN}}{{{b["instances"]}}}')
    # table: per family, harden vs snap, snap vs rigid, harden vs grow-area (instances where the first / second is lower)
    if 'C11-snap' in res:
        hdr = ['family', '$N$', 'harden : snap', 'snap : rigid'] + (['harden : grow-area', 'grow-area : rigid'] if 'C12-grow-area' in res else [])
        L = [r'\begin{table}[t]\centering\small', r'\begin{tabular}{lr' + 'c' * (len(hdr) - 2) + '}', r'\toprule', ' & '.join(hdr) + r' \\', r'\midrule']
        for fam in FAMS:
            v = res['C11-snap']['families'].get(fam)
            if not v:
                continue
            cells = [SHORT[fam], str(v['N']), '{a_lower} : {b_lower}'.format(**v['harden_vs_snap']), '{a_lower} : {b_lower}'.format(**v['snap_vs_rigid'])]
            if 'C12-grow-area' in res:
                w = res['C12-grow-area']['families'][fam]
                cells += ['{a_lower} : {b_lower}'.format(**w['harden_vs_grow-area']), '{a_lower} : {b_lower}'.format(**w['grow-area_vs_rigid'])]
            L.append(' & '.join(cells) + r' \\')
        tot = [r'\midrule all', str(sum(v['N'] for v in res['C11-snap']['families'].values())),
               '{a_lower} : {b_lower}'.format(**res['C11-snap']['all']['harden_vs_snap']), '{a_lower} : {b_lower}'.format(**res['C11-snap']['all']['snap_vs_rigid'])]
        if 'C12-grow-area' in res:
            tot += ['{a_lower} : {b_lower}'.format(**res['C12-grow-area']['all']['harden_vs_grow-area']), '{a_lower} : {b_lower}'.format(**res['C12-grow-area']['all']['grow-area_vs_rigid'])]
        L += [' & '.join(tot) + r' \\', r'\bottomrule', r'\end{tabular}',
              r'\caption{Which part of hardening matters (C11, C12; harden and rigid from C07, same seeds, settings and budget). Each cell $a:b$ counts the instances on which the first method\textquotesingle s lowest size is lower than the second\textquotesingle s, and the reverse; the rest are ties. \emph{snap} compresses disks as hardening does, then switches to polygons at once; \emph{grow-area} keeps rigid polygons whose area follows hardening\textquotesingle s.}',
              r'\label{tab:ablate}', r'\end{table}']
        open(os.path.join(ROOT, 'paper', 'tables', 'ablations.tex'), 'w').write('\n'.join(L) + '\n')
    json.dump(res, open(os.path.join(ROOT, 'analysis', 'ablations.json'), 'w'), indent=1)
    open(os.path.join(ROOT, 'paper', 'ablations.tex'), 'w').write('\n'.join(nums) + '\n')
    print(json.dumps(res, indent=1)[:4000])


if __name__ == '__main__':
    main()
