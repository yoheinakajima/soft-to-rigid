"""Post-hoc check for C16: tighten the best run of every method at the instances only hardening reached (n = 17, 19, 26, 29),
regardless of the tightening gate, and print each method's gap to the best known value.  python3 scripts/c16_equal_tighten.py"""
import glob, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from multiprocessing import Pool
from packing.polish import polish_row, polished_path
from packing.stats import catalog_tol
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
rows = {}
for f in glob.glob(f'{ROOT}/campaigns/C16-squares-long/runs*.jsonl'):
    for l in open(f):
        if l.strip():
            r = json.loads(l); rows.setdefault((r['n'], r['method'][:-5]), []).append(r)
todo = []
for n in (17, 19, 26, 29):
    for m in ('harden', 'grow', 'rigid', 'sa', 'pc'):
        b = min(rows[(n, m)], key=lambda r: r['L'])
        if not os.path.exists(polished_path(b['id'])): todo.append(b)
print('to tighten', len(todo), flush=True)
with Pool(2) as p:
    for x in p.imap_unordered(polish_row, todo): print(x, flush=True)
for n in (17, 19, 26, 29):
    rec, tol = catalog_tol('squ-in-squ', n)
    out = {}
    for m in ('harden', 'grow', 'rigid', 'sa', 'pc'):
        b = min(rows[(n, m)], key=lambda r: r['L'])
        t = json.load(open(polished_path(b['id'])))['L']
        out[m] = round(min(t, b['L']) - rec, 5)
    print(n, out)
