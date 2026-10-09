"""Fill the instance list of C08 and C09 from C07, by the rule pre-registered in C08's plan:
contested = harden-best and rigid-best lowest sizes differ by more than 1e-6 relative; at most 40, largest
relative differences first. Must run before the first C08/C09 run; records the list and its source in the plans.
    python3 scripts/contested.py
"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
from packing.project import load, cell_status

camps, cells, cands, finds, claims, _ = load()
st = cell_status(cells, cands)
low = {}
for c in st.values():
    if c['campaign'] == 'C07-breadth-best' and c['method'] in ('harden-best', 'rigid-best'):
        low[(c['family'], c['n'], c['method'])] = c['lowest']
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
for c in ('C08-start-shape', 'C09-budget'):
    p = os.path.join(ROOT, 'campaigns', c, 'plan.json')
    pl = json.load(open(p))
    pl['instances'] = inst
    pl['instances_source'] = f'scripts/contested.py over C07-breadth-best: {len(diffs)} contested, {len(chosen)} used (largest relative differences)'
    json.dump(pl, open(p, 'w'), indent=1)
