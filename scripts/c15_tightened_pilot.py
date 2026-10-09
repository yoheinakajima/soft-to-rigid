"""Post-hoc check for C15: would the pilot have chosen differently if it compared the tightened sizes of the best
legalised run of each path's 8 pilot runs, instead of the untightened sizes?   python3 scripts/c15_tightened_pilot.py"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from multiprocessing import Pool
from packing.decision import load
from packing.polish import polish_row, polished_path
from packing.analyze import sign_test2

rows = load()
insts = sorted({(f, n) for f, n, m, s in rows})
best8 = {}
for f, n in insts:
    for m in ('harden', 'rigid'):
        best8[(f, n, m)] = min((rows[(f, n, m, s)] for s in range(1, 9)), key=lambda r: r['L'])
todo = [r for r in best8.values() if not os.path.exists(polished_path(r['id']))]
with Pool(2) as p:
    for _ in p.imap_unordered(polish_row, todo):
        pass
T = lambda r: min(r['L'], json.load(open(polished_path(r['id'])))['L'])
res = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'analysis', 'C15.json')))
changed, out = [], {}
for f, n in insts:
    raw_pick = res['instances'][f'{f}/n{n}']['pick']
    th, tr = T(best8[(f, n, 'harden')]), T(best8[(f, n, 'rigid')])
    t_pick = 'harden' if th < tr * (1 - 1e-9) else 'rigid'
    out[f'{f}/n{n}'] = t_pick
    if t_pick != raw_pick:
        changed.append(f'{f}/n{n}')
# score the tightened-selector policy: pilot seeds 1-8 each, then seeds 9-56 of the chosen path; best legalised run, tightened
al = bl = 0
for f, n in insts:
    pick = out[f'{f}/n{n}']
    pool = [rows[(f, n, 'harden', s)] for s in range(1, 9)] + [rows[(f, n, 'rigid', s)] for s in range(1, 9)] + [rows[(f, n, pick, s)] for s in range(9, 57)]
    b = min(pool, key=lambda r: r['L'])
    if not os.path.exists(polished_path(b['id'])):
        polish_row(b)
    x = T(b); y = res['instances'][f'{f}/n{n}']['always-rigid']['L']
    al += x < y * (1 - 1e-9); bl += y < x * (1 - 1e-9)
summary = {'instances': len(insts), 'picked_harden_tightened': sum(v == 'harden' for v in out.values()),
           'picked_harden_raw': res['picked_harden'], 'changed': changed, 'tightened_pilot_vs_rigid': [al, bl, sign_test2(al, bl)]}
json.dump(summary, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'analysis', 'C15_tightened_pilot.json'), 'w'), indent=1)
print(json.dumps(summary, indent=1))
