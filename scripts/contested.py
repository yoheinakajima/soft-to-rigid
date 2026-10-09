"""Fill the instance list of C08 and C09 from C07, by the rule pre-registered in C08's plan:
contested = harden-best and rigid-best lowest sizes differ by more than 1e-6 relative; at most 40, largest
relative differences first. Must run before the first C08/C09 run; records the list and its source in the plans.
    python3 scripts/contested.py
"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
import glob
from packing.ledger import _cells
# lowest tightened size per cell, computed from the raw runs and the tightening cache (same values the
# ledger holds; this avoids waiting for ingestion)
rows, files = [], {}
for f in glob.glob(os.path.join(ROOT, 'campaigns', 'C07-breadth-best', 'runs*.jsonl')):
    for line in open(f):
        if line.strip():
            r = json.loads(line); rows.append(r); files[r['id']] = f
low = {}
for c in _cells('C07-breadth-best', rows, files):
    if c['method'] not in ('harden-best', 'rigid-best'):
        continue
    v = c['best_L']
    for cand in c['candidates']:
        pp = os.path.join(ROOT, 'ledger', 'polished', cand['run'].replace('/', '_') + '.json')
        if os.path.exists(pp):
            v = min(v, json.load(open(pp))['L'])
    low[(c['family'], c['n'], c['method'])] = v
diffs = []
for (f, n, m), v in low.items():
    if m != 'harden-best' or (f, n, 'rigid-best') not in low:
        continue
    r = low[(f, n, 'rigid-best')]
    d = abs(v - r) / min(v, r)
    if d > 1e-6:
        diffs.append((d, f, n, 'harden' if v < r else 'rigid'))
diffs.sort(reverse=True)
chosen = diffs[:40]
by = {}
for d, f, n, w in chosen:
    by.setdefault(f, []).append(n)
inst = [{'family': f, 'ns': sorted(ns)} for f, ns in sorted(by.items())]
print(f'{len(diffs)} contested instances; using {len(chosen)}:', inst)
print('lower path:', {k: sum(1 for x in chosen if x[3] == k) for k in ('harden', 'rigid')})
def group(ch):
    by = {}
    for d, f, n, w in ch:
        by.setdefault(f, []).append(n)
    return [{'family': f, 'ns': sorted(ns)} for f, ns in sorted(by.items())]
for c, k in (('C08-start-shape', 40), ('C09-budget', 20)):
    p = os.path.join(ROOT, 'campaigns', c, 'plan.json')
    pl = json.load(open(p))
    pl['instances'] = group(diffs[:k])
    pl['instances_source'] = f'scripts/contested.py over C07-breadth-best: {len(diffs)} contested, {min(k, len(diffs))} used (largest relative differences)'
    json.dump(pl, open(p, 'w'), indent=1)
