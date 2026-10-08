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


def breadth(st, cid='C04-breadth'):
    cells = [c for c in st.values() if c['campaign'] == cid]
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


def main():
    camps, cells, cands, finds, claims, nev = load()
    st = cell_status(cells, cands)
    os.makedirs(os.path.join(ROOT, 'analysis'), exist_ok=True)
    b = breadth(st)
    if b:
        json.dump(b, open(os.path.join(ROOT, 'analysis', 'C04-breadth.json'), 'w'), indent=1)
        T = b['totals']['all']
        print('C04 totals:', {m: (T[m]['solved'], T[m]['instances']) for m in T})
        print('sign tests:', b['sign_tests'])
        print('unique solvers:', {k: len(v) for k, v in b['unique'].items()})


if __name__ == '__main__':
    main()
