"""Score C06-tune-best by its pre-registered rule: per method and setting, mean over instances of the lowest
legal size of the 16 runs relative to the best known value; tie-break: mean fraction of runs within 1e-4
relative. Writes methods/<method>-best.json with --write."""
import glob, json, os, statistics as S, sys
from collections import defaultdict
ROOT = os.path.join(os.path.dirname(__file__), '..'); C = 'C06-tune-best'
rows = [json.loads(l) for f in glob.glob(f'{ROOT}/campaigns/{C}/runs*.jsonl') for l in open(f) if l.strip()]
plan = json.load(open(f'{ROOT}/campaigns/{C}/plan.json'))
params = {(m, cf['name']): cf['params'] for m, cfs in plan['configs'].items() for cf in cfs}
g = defaultdict(lambda: defaultdict(list))
for r in rows: g[(r['method'], r['config'])][(r['family'], r['n'])].append(r['L'] / r['record'] - 1)
for m in plan['methods']:
    sc = sorted((S.mean(min(v) for v in I.values()), -S.mean(sum(x < 1e-4 for x in v) / len(v) for v in I.values()), cf) for (mm, cf), I in g.items() if mm == m)
    best = sc[0]
    print(f'{m:7s} winner {best[2]:20s} mean lowest relgap {best[0]:.5f}  hit-frac {-best[1]:.3f}   runner-up {sc[1][2]} {sc[1][0]:.5f}')
    if '--write' in sys.argv:
        json.dump({'method': m, 'params': params[(m, best[2])], 'tuned_by': f'{C}/{best[2]}', 'tuning_score': {'mean_lowest_relgap': best[0], 'mean_hit_fraction_1e-4': -best[1]}},
                  open(f'{ROOT}/methods/{m}-best.json', 'w'), indent=1)
