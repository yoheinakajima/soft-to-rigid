"""Uncertainty and diagnostics for the main comparison (C07), computed from raw runs and the tightening cache.

    python3 -m packing.stats            # -> analysis/stats.json, paper/tables/stats-*.tex, paper/figures/bestofk.pdf

1. Seed bootstrap: resample each cell's 32 runs with replacement (1000 times) and recount, per method, the
   instances where its lowest size is the lowest of the five. A run's size is its tightened size if it was
   tightened, else its legalised raw size (runs outside the tightening policy are never tightened, so the
   bootstrap slightly favours methods whose best runs were tightened; stated in the paper).
2. Best-of-k: for an instance with s successful runs out of N, the chance that k random runs include one is
   1 - C(N-s, k)/C(N, k). Success = size within the catalogue tolerance of the best known value.
3. Wins by n range (2-10, 11-20, 21-30).
4. Diagnostics for the baselines: how often each method's best run was eligible for tightening (within 2%),
   and simulated-annealing moves / perturbation-compression relaxation steps per run.
"""
import glob, json, math, os, random, statistics as S
from collections import defaultdict
from .ledger import ROOT

METHODS = ['harden', 'grow', 'rigid', 'sa', 'pc']
CID = 'C07-breadth-best'


def load_runs(cid):
    rows = []
    for f in glob.glob(os.path.join(ROOT, 'campaigns', cid, 'runs*.jsonl')):
        rows += [json.loads(l) for l in open(f) if l.strip()]
    return rows


def tightened(run_id):
    p = os.path.join(ROOT, 'ledger', 'polished', run_id.replace('/', '_') + '.json')
    return json.load(open(p))['L'] if os.path.exists(p) else None


def catalog_tol(fam, n):
    r = json.load(open(os.path.join(ROOT, 'catalog', fam + '.json')))['records'][str(n)]
    return r['value'], (r.get('tol') or 1e-5) if r.get('truncated') else 1e-9


def cells(cid=CID):
    by = defaultdict(list)
    for r in load_runs(cid):
        if 'error' in r:
            continue
        m = r['method'].replace('-best', '')
        t = tightened(r['id'])
        by[(r['family'], r['n'], m)].append(min(r['L'], t) if t is not None else r['L'])
    return by


def lowest_counts(by, pick):
    inst = sorted({(f, n) for f, n, m in by})
    cnt = {m: 0 for m in METHODS}
    for f, n in inst:
        lows = {m: pick(by[(f, n, m)]) for m in METHODS if (f, n, m) in by}
        lo = min(lows.values())
        for m, v in lows.items():
            if v <= lo * (1 + 1e-9) + 1e-12:
                cnt[m] += 1
    return cnt


def bootstrap(by, B=1000, seed=7):
    rng = random.Random(seed)
    samples = {m: [] for m in METHODS}
    for _ in range(B):
        c = lowest_counts(by, lambda v: min(rng.choice(v) for _ in range(len(v))))
        for m in METHODS:
            samples[m].append(c[m])
    out = {}
    for m in METHODS:
        s = sorted(samples[m])
        out[m] = {'lo95': s[int(0.025 * B)], 'hi95': s[int(0.975 * B) - 1], 'mean': S.mean(s)}
    # paired contrasts: difference of two methods' counts within the same resample
    for a, b in (('rigid', 'harden'), ('rigid', 'grow'), ('grow', 'harden')):
        d = sorted(x - y for x, y in zip(samples[a], samples[b]))
        out[f'{a}-{b}'] = {'lo95': d[int(0.025 * B)], 'hi95': d[int(0.975 * B) - 1], 'median': d[B // 2], 'share_positive': sum(x > 0 for x in d) / B}
    # how often each method has the most lowest-of-five instances
    return out


def best_of_k(vals, rec, tol, ks):
    N = len(vals); s = sum(v <= rec + tol for v in vals)
    return [1 - (math.comb(N - s, k) / math.comb(N, k) if k <= N - s else 0) for k in ks]


def by_range(by):
    out = {}
    for lo, hi in ((2, 10), (11, 20), (21, 30)):
        sub = {k: v for k, v in by.items() if lo <= k[1] <= hi}
        out[f'{lo}-{hi}'] = dict(lowest_counts(sub, min), instances=len({(f, n) for f, n, m in sub}))
    return out


def diagnostics(cid=CID):
    rows = load_runs(cid)
    best = {}
    for r in rows:
        k = (r['family'], r['n'], r['method'].replace('-best', ''))
        if k not in best or r['L'] < best[k]['L']:
            best[k] = r
    elig = {m: [] for m in METHODS}
    for (f, n, m), r in best.items():
        elig[m].append(r['L'] <= r['record'] * 1.02)
    steps = defaultdict(list)
    for r in rows:
        m = r['method'].replace('-best', '')
        if r['n'] in (10, 20, 30) and r['family'] == 'squ-in-squ':
            steps[(m, r['n'])].append((r['steps'], r['evals'], r['ms']))
    st = {f'{m}/n{n}': {'steps': round(S.mean(x[0] for x in v)), 'pair_evals': round(S.mean(x[1] for x in v)), 'ms': round(S.mean(x[2] for x in v))}
          for (m, n), v in sorted(steps.items())}
    return {'eligible_fraction': {m: round(sum(v) / len(v), 3) for m, v in elig.items()}, 'per_run': st}


def main():
    by = cells()
    res = {'point': lowest_counts(by, min), 'bootstrap95': bootstrap(by), 'by_n_range': by_range(by), 'diagnostics': diagnostics()}
    ks = [1, 2, 4, 8, 16, 32]
    sel = [('squ-in-squ', 11), ('squ-in-squ', 19), ('squ-in-squ', 18), ('squ-in-cir', 21), ('tri-in-squ', 18), ('tri-in-tri', 20)]
    curves = {}
    for f, n in sel:
        rec, tol = catalog_tol(f, n)
        curves[f'{f}/n{n}'] = {m: best_of_k(by[(f, n, m)], rec, tol, ks) for m in ('harden', 'rigid', 'grow') if (f, n, m) in by}
    res['best_of_k'] = {'k': ks, 'curves': curves}
    os.makedirs(os.path.join(ROOT, 'analysis'), exist_ok=True)
    json.dump(res, open(os.path.join(ROOT, 'analysis', 'stats.json'), 'w'), indent=1)
    # figure
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    col = {'harden': '#d17a22', 'grow': '#6a8e3a', 'rigid': '#2f5d8a'}
    fig, axs = plt.subplots(1, len(sel), figsize=(7.2, 1.55), sharey=True)
    for ax, (f, n) in zip(axs, sel):
        for m, ys in curves[f'{f}/n{n}'].items():
            ax.plot(ks, ys, 'o-', ms=2.5, lw=1, color=col[m], label=m)
        ax.set_xscale('log', base=2); ax.set_xticks(ks); ax.set_xticklabels([str(k) for k in ks], fontsize=5.5)
        ax.set_title(f"{f.replace('squ', 'sq').replace('-in-', ' in ')} n={n}", fontsize=6.5); ax.set_ylim(-0.03, 1.03)
        ax.tick_params(labelsize=6)
        for s in ('top', 'right'): ax.spines[s].set_visible(False)
    axs[0].set_ylabel('P(best of k\nreaches record)', fontsize=6.5); axs[len(sel) // 2].set_xlabel('runs k', fontsize=6.5)
    axs[-1].legend(fontsize=5.5, frameon=False, loc='lower right')
    fig.tight_layout(pad=0.3)
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(ROOT, 'paper', 'figures', f'bestofk.{ext}'), dpi=220)
    # macros
    b = res['bootstrap95']; d = res['diagnostics']; r = res['by_n_range']
    nums = [r'\newcommand{\Boot%s}{%d--%d}' % (m.capitalize(), b[m]['lo95'], b[m]['hi95']) for m in METHODS]
    for pair, key in (('rigid-harden', 'RH'), ('rigid-grow', 'RG'), ('grow-harden', 'GH')):
        v = b[pair]
        nums += [r'\newcommand{\BootD%s}{%d to %d}' % (key, v['lo95'], v['hi95']), r'\newcommand{\BootD%sMed}{%d}' % (key, v['median']),
                 r'\newcommand{\BootD%sPos}{%d\%%}' % (key, round(100 * v['share_positive']))]
    nums += [r'\newcommand{\Elig%s}{%d\%%}' % (m.capitalize(), round(100 * d['eligible_fraction'][m])) for m in METHODS]
    for rg, v in r.items():
        key = {'2-10': 'Small', '11-20': 'Mid', '21-30': 'Large'}[rg]
        nums += [r'\newcommand{\Range%s%s}{%d}' % (key, m.capitalize(), v[m]) for m in METHODS] + [r'\newcommand{\Range%sN}{%d}' % (key, v['instances'])]
    for k, v in d['per_run'].items():
        m, n = k.split('/')
        nums.append(r'\newcommand{\Steps%s%s}{%s}' % (m.capitalize(), {'n10': 'Ten', 'n20': 'Twenty', 'n30': 'Thirty'}[n], f"{v['steps']:,}".replace(',', '{,}')))
    open(os.path.join(ROOT, 'paper', 'stats.tex'), 'w').write('\n'.join(nums) + '\n')
    # diagnostics table
    pr = d['per_run']; f = lambda v: f"{v:,}".replace(',', '{,}')
    unit = {'harden': 'steps', 'grow': 'steps', 'rigid': 'steps', 'sa': 'moves', 'pc': 'steps'}
    rows = [rf"{m} & {f(pr[f'{m}/n20']['steps'])} & {f(pr[f'{m}/n30']['steps'])} & {f(pr[f'{m}/n20']['pair_evals'])} & {f(pr[f'{m}/n30']['pair_evals'])} & {f(pr[f'{m}/n20']['ms'])} & {f(pr[f'{m}/n30']['ms'])} & {round(100 * d['eligible_fraction'][m])}\% \\"
            for m in METHODS if f'{m}/n20' in pr]
    open(os.path.join(ROOT, 'paper', 'tables', 'diag.tex'), 'w').write(
        '\\begin{table}[ht]\\centering\\small\n\\begin{tabular}{lrrrrrrr}\n\\toprule\n'
        r'method & \multicolumn{2}{c}{steps (sa: moves) per run} & \multicolumn{2}{c}{pair evaluations per run} & \multicolumn{2}{c}{ms per run} & best run \\' '\n'
        r' & $n=20$ & $n=30$ & $n=20$ & $n=30$ & $n=20$ & $n=30$ & tightened \\' '\n\\midrule\n' + '\n'.join(rows) +
        '\n\\bottomrule\n\\end{tabular}\n\\caption{Work per run (C07, squares in a square, mean over 32 runs) wall-clock milliseconds per run on one core (Node.js), and the share of instances on which each method\'s best run was within 2\\% of the best known value and so was tightened (all families). Gradient paths are matched in steps; the baselines stop once they exceed a reference hardening run\'s pair evaluations.}\\label{tab:diag}\n\\end{table}\n')
    print(json.dumps({k: res[k] for k in ('point', 'bootstrap95', 'by_n_range', 'diagnostics')}, indent=1))


if __name__ == '__main__':
    main()
