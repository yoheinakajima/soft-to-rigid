"""Score tuning campaigns by the pre-registered rule (C01): per method and setting, mean over tuning
instances of the median relative gap (L / best known - 1) over seeds; ties by mean best relative gap.
Usage: python3 scripts/score_tuning.py C01-tune C02-tune-extend [--write]"""
import glob, json, os, statistics as S, sys
from collections import defaultdict
ROOT = os.path.join(os.path.dirname(__file__), '..')
camps = [a for a in sys.argv[1:] if not a.startswith('--')]
rows = [json.loads(l) for c in camps for f in glob.glob(f'{ROOT}/campaigns/{c}/runs*.jsonl') for l in open(f) if l.strip()]
g = defaultdict(lambda: defaultdict(list)); params = {}
for r in rows:
    g[(r['method'], r['campaign'], r['config'])][r['family']].append(r['L'] / r['record'] - 1)
for c in camps:
    for m, cfgs in json.load(open(f'{ROOT}/campaigns/{c}/plan.json'))['configs'].items():
        for cf in cfgs: params[(m, c, cf['name'])] = cf['params']
out = {}
for m in sorted({k[0] for k in g}):
    sc = []
    for (mm, c, cf), fams in g.items():
        if mm != m: continue
        sc.append((S.mean(S.median(v) for v in fams.values()), S.mean(min(v) for v in fams.values()), c, cf))
    sc.sort()
    out[m] = sc[0]
    print(f'{m:8s} winner {sc[0][2]}/{sc[0][3]}  median-relgap {sc[0][0]:.5f}  best-relgap {sc[0][1]:.6f}   (runner-up {sc[1][2]}/{sc[1][3]} {sc[1][0]:.5f})')
if '--write' in sys.argv:
    for m, (med, best, c, cf) in out.items():
        json.dump({'method': m, 'params': params[(m, c, cf)], 'tuned_by': f'{c}/{cf}',
                   'tuning_score': {'mean_median_relgap': med, 'mean_best_relgap': best}}, open(f'{ROOT}/methods/{m}.json', 'w'), indent=1)
    print('written methods/*.json')
