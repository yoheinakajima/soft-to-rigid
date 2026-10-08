"""Exact tightening for a campaign's candidates, in parallel, cached by run id.

    python -m packing.polish <campaign> [--workers 2]

Candidates are chosen by the same rule the ledger uses (packing.ledger._cells). Results go to
ledger/polished/<run id>.json; the ledger's polisher behavior reuses a cached file instead of recomputing.
"""
import argparse, glob, json, os, sys, time
from multiprocessing import Pool
from . import tighten
from .ledger import ROOT, _cells, catalog


def polished_path(run_id):
    return os.path.join(ROOT, 'ledger', 'polished', run_id.replace('/', '_') + '.json')


def polish_row(row):
    out_path = polished_path(row['id'])
    if os.path.exists(out_path):
        return row['id'], 'cached'
    F = catalog(row['family'])
    t0 = time.time()
    try:
        out = tighten.solve(F['piece'], F['container'], row['poses'])
    except Exception as e:
        return row['id'], 'error ' + repr(e)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump({'run': row['id'], 'family': row['family'], 'n': row['n'], 'L': out['L'], 'L_raw': row['L'],
               'poses': out['poses'], 'history': out['history'], 'seconds': round(time.time() - t0, 2)}, open(out_path, 'w'))
    return row['id'], 'ok %.1fs' % (time.time() - t0)


def main(campaign, workers):
    cdir = os.path.join(ROOT, 'campaigns', campaign)
    plan = json.load(open(os.path.join(cdir, 'plan.json')))
    rows, files = {}, {}
    for f in sorted(glob.glob(os.path.join(cdir, 'runs*.jsonl'))):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                rows[r['id']] = r
                files[r['id']] = os.path.relpath(f, ROOT)
    cells = _cells(campaign, list(rows.values()), files, plan.get('polish', True))
    todo = [rows[c['run']] for cell in cells for c in cell['candidates'] if not os.path.exists(polished_path(c['run']))]
    todo.sort(key=lambda r: r['n'])
    print(f'{campaign}: {sum(len(c["candidates"]) for c in cells)} candidates, {len(todo)} to polish', flush=True)
    with Pool(workers) as pool:
        for i, (rid, status) in enumerate(pool.imap_unordered(polish_row, todo)):
            if i % 25 == 0 or not status.startswith('ok'):
                print(i, rid, status, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('campaign'); ap.add_argument('--workers', type=int, default=2)
    a = ap.parse_args()
    main(a.campaign, a.workers)
