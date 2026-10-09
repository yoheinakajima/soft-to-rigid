"""C14: equal tightening. On the 28 instances fixed by C13, tighten the three runs with the lowest legalised size of
every method in C07 (no eligibility condition) and recompute the lowest-of-five comparison three ways.

    python3 -m packing.refine [--workers 2]   # -> campaigns/C14-equal-refine/tightened/, analysis/C14.json, paper/refine.tex

Tightening is deterministic, so a run the C07 policy already tightened is copied from ledger/polished.
"""
import argparse, glob, json, os, shutil, time
from multiprocessing import Pool
from .ledger import ROOT, catalog
from . import tighten

CID, SRC = 'C14-equal-refine', 'C07-breadth-best'
METHODS = ['harden', 'grow', 'rigid', 'sa', 'pc']
OUT = os.path.join(ROOT, 'campaigns', CID, 'tightened')


def path(rid):
    return os.path.join(OUT, rid.replace('/', '_') + '.json')


def work(row):
    p = path(row['id'])
    if os.path.exists(p):
        return row['id'], 'done'
    cached = os.path.join(ROOT, 'ledger', 'polished', row['id'].replace('/', '_') + '.json')
    if os.path.exists(cached):
        shutil.copy(cached, p); return row['id'], 'copied'
    F = catalog(row['family']); t0 = time.time()
    try:
        out = tighten.solve(F['piece'], F['container'], row['poses'])
    except Exception as e:
        return row['id'], 'error ' + repr(e)
    json.dump({'run': row['id'], 'L': out['L'], 'L_raw': row['L'], 'poses': out['poses'], 'seconds': round(time.time() - t0, 2)}, open(p, 'w'))
    return row['id'], 'ok %.1fs' % (time.time() - t0)


def lowest_counts(vals, insts):
    cnt = {m: 0 for m in METHODS}
    for i in insts:
        lo = min(vals[(i, m)] for m in METHODS)
        for m in METHODS:
            cnt[m] += vals[(i, m)] <= lo * (1 + 1e-9) + 1e-12
    return cnt


def main(workers=2):
    plan = json.load(open(os.path.join(ROOT, 'campaigns', CID, 'plan.json')))
    want = {(i['family'], n) for i in plan['instances'] for n in i['ns']}
    rows = {}
    for f in glob.glob(os.path.join(ROOT, 'campaigns', SRC, 'runs*.jsonl')):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                if 'error' not in r and (r['family'], r['n']) in want:
                    rows.setdefault(((r['family'], r['n']), r['method'].replace('-best', '')), []).append(r)
    top = {k: sorted(v, key=lambda r: r['L'])[:3] for k, v in rows.items()}
    os.makedirs(OUT, exist_ok=True)
    jobs = [r for v in top.values() for r in v]
    with Pool(workers) as pool:
        for rid, st in pool.imap_unordered(work, jobs):
            print(rid, st, flush=True)
    insts = sorted(want)
    raw = {k: min(r['L'] for r in v) for k, v in rows.items()}
    eq = {k: min([r['L'] for r in rows[k]] + [json.load(open(path(r['id'])))['L'] for r in top[k]]) for k in rows}
    pol = {}
    for k, v in rows.items():
        xs = []
        for r in v:
            c = os.path.join(ROOT, 'ledger', 'polished', r['id'].replace('/', '_') + '.json')
            xs.append(min(r['L'], json.load(open(c))['L']) if os.path.exists(c) else r['L'])
        pol[k] = min(xs)
    secs = {m: [json.load(open(path(r['id']))).get('seconds') for k, v in top.items() if k[1] == m for r in v] for m in METHODS}
    res = {'instances': len(insts), 'raw': lowest_counts(raw, insts), 'equal_top3': lowest_counts(eq, insts), 'c07_policy': lowest_counts(pol, insts),
           'tighten_seconds_mean': {m: round(sum(x for x in s if x) / max(1, sum(1 for x in s if x)), 1) for m, s in secs.items()}}
    json.dump(res, open(os.path.join(ROOT, 'analysis', 'C14.json'), 'w'), indent=1)
    nums = [rf'\newcommand{{\RefN}}{{{len(insts)}}}']
    for t, key in (('raw', 'Raw'), ('equal_top3', 'Eq'), ('c07_policy', 'Pol')):
        nums += [rf'\newcommand{{\Ref{key}{m.capitalize()}}}{{{res[t][m]}}}' for m in METHODS]
    open(os.path.join(ROOT, 'paper', 'refine.tex'), 'w').write('\n'.join(nums) + '\n')
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=2)
    main(ap.parse_args().workers)
