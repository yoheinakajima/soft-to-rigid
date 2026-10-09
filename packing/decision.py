"""C15: score the pre-registered path-choice policies on held-out families.

    python3 -m packing.decision [--workers 2]   # -> analysis/C15.json, paper/decision.tex, paper/tables/C15.tex

Policies per instance (64 runs each), from 64 harden-best and 64 rigid-best runs at budget 1:
  always-rigid  rigid seeds 1-64
  always-harden harden seeds 1-64
  pilot         harden seeds 1-8 and rigid seeds 1-8, then seeds 9-56 of the path whose pilot reached the lower
                legalised size (ties -> rigid)
A policy's result is the tightened size of the run with the lowest legalised size in its set (one tightening per
policy and instance; cached in ledger/polished like every other tightening).
"""
import argparse, glob, json, os
from multiprocessing import Pool
from .ledger import ROOT
from .polish import polish_row, polished_path
from .stats import catalog_tol
from .analyze import sign_test2

CID = 'C15-heldout-decision'
FAMS = ['pen-in-squ', 'oct-in-squ', 'hex-in-tri', 'tri-in-cir']
SHORT = {'pen-in-squ': 'pentagons in square', 'oct-in-squ': 'octagons in square', 'hex-in-tri': 'hexagons in triangle', 'tri-in-cir': 'triangles in circle'}
MAC = {'pen-in-squ': 'PenSqu', 'oct-in-squ': 'OctSqu', 'hex-in-tri': 'HexTri', 'tri-in-cir': 'TriCir'}


def load():
    rows = {}
    for f in glob.glob(os.path.join(ROOT, 'campaigns', CID, 'runs*.jsonl')):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                if 'error' not in r:
                    rows[(r['family'], r['n'], r['method'].replace('-best', ''), r['seed'])] = r
    return rows


def policies(rows, f, n):
    H = {s: rows[(f, n, 'harden', s)] for s in range(1, 65) if (f, n, 'harden', s) in rows}
    R = {s: rows[(f, n, 'rigid', s)] for s in range(1, 65) if (f, n, 'rigid', s) in rows}
    ph, pr = min(H[s]['L'] for s in range(1, 9)), min(R[s]['L'] for s in range(1, 9))
    pick = 'harden' if ph < pr else 'rigid'
    chosen = H if pick == 'harden' else R
    pilot = [H[s] for s in range(1, 9)] + [R[s] for s in range(1, 9)] + [chosen[s] for s in range(9, 57)]
    best = lambda rs: min(rs, key=lambda r: r['L'])
    return {'always-rigid': best(list(R.values())), 'always-harden': best(list(H.values())), 'pilot': best(pilot)}, pick


def main(workers=2):
    rows = load()
    insts = sorted({(f, n) for f, n, m, s in rows})
    plan = {}
    for f, n in insts:
        plan[(f, n)] = policies(rows, f, n)
    todo = {r['id']: r for (P, pick) in plan.values() for r in P.values() if not os.path.exists(polished_path(r['id']))}
    if todo:
        with Pool(workers) as pool:
            for rid, st in pool.imap_unordered(polish_row, list(todo.values())):
                print(rid, st, flush=True)
    res = {'instances': {}, 'families': {}}
    for (f, n), (P, pick) in plan.items():
        rec, tol = catalog_tol(f, n)
        out = {}
        for k, r in P.items():
            L = json.load(open(polished_path(r['id'])))['L']
            out[k] = {'run': r['id'], 'L_raw': r['L'], 'L': min(L, r['L']), 'reached': min(L, r['L']) <= rec + tol}
        res['instances'][f'{f}/n{n}'] = {'pick': pick, 'record': rec, **out}

    def cmp(a, b, keys):
        al = bl = 0
        for k in keys:
            x, y = res['instances'][k][a]['L'], res['instances'][k][b]['L']
            if x < y * (1 - 1e-9): al += 1
            elif y < x * (1 - 1e-9): bl += 1
        return {'a_lower': al, 'b_lower': bl, 'ties': len(keys) - al - bl, 'p': sign_test2(al, bl)}

    allk = list(res['instances'])
    res['pilot_vs_rigid'] = cmp('pilot', 'always-rigid', allk)
    res['harden_vs_rigid'] = cmp('always-harden', 'always-rigid', allk)
    res['pilot_vs_harden'] = cmp('pilot', 'always-harden', allk)
    for f in FAMS:
        ks = [k for k in allk if k.startswith(f + '/')]
        if not ks:
            continue
        res['families'][f] = {'N': len(ks), 'pilot_vs_rigid': cmp('pilot', 'always-rigid', ks), 'harden_vs_rigid': cmp('always-harden', 'always-rigid', ks),
                              'picked_harden': sum(res['instances'][k]['pick'] == 'harden' for k in ks),
                              'reached': {p: sum(res['instances'][k][p]['reached'] for k in ks) for p in ('always-rigid', 'always-harden', 'pilot')}}
    res['reached'] = {p: sum(v[p]['reached'] for v in res['instances'].values()) for p in ('always-rigid', 'always-harden', 'pilot')}
    res['picked_harden'] = sum(v['pick'] == 'harden' for v in res['instances'].values())
    json.dump(res, open(os.path.join(ROOT, 'analysis', 'C15.json'), 'w'), indent=1)
    fp = lambda p: '1' if p >= 0.995 else f'{p:.2g}'
    pv, hv = res['pilot_vs_rigid'], res['harden_vs_rigid']
    nums = [rf'\newcommand{{\DecN}}{{{len(allk)}}}', rf'\newcommand{{\DecPilotLower}}{{{pv["a_lower"]}}}', rf'\newcommand{{\DecRigidLower}}{{{pv["b_lower"]}}}',
            rf'\newcommand{{\DecTies}}{{{pv["ties"]}}}', rf'\newcommand{{\DecP}}{{{fp(pv["p"])}}}', rf'\newcommand{{\DecHLower}}{{{hv["a_lower"]}}}',
            rf'\newcommand{{\DecHRLower}}{{{hv["b_lower"]}}}', rf'\newcommand{{\DecHP}}{{{fp(hv["p"])}}}', rf'\newcommand{{\DecPicked}}{{{res["picked_harden"]}}}']
    nums += [rf'\newcommand{{\DecReached{k}}}{{{res["reached"][p]}}}' for k, p in (('Rigid', 'always-rigid'), ('Harden', 'always-harden'), ('Pilot', 'pilot'))]
    tp = os.path.join(ROOT, 'analysis', 'C15_tightened_pilot.json')   # post-hoc check, scripts/c15_tightened_pilot.py
    if os.path.exists(tp):
        t = json.load(open(tp))
        nums += [rf'\newcommand{{\DecTPicked}}{{{t["picked_harden_tightened"]}}}', rf'\newcommand{{\DecTChanged}}{{{len(t["changed"])}}}',
                 rf'\newcommand{{\DecTLower}}{{{t["tightened_pilot_vs_rigid"][0]}}}', rf'\newcommand{{\DecTRLower}}{{{t["tightened_pilot_vs_rigid"][1]}}}']
    open(os.path.join(ROOT, 'paper', 'decision.tex'), 'w').write('\n'.join(nums) + '\n')
    L = [r'\begin{table}[t]\centering\small', r'\begin{tabular}{lrcccc}', r'\toprule',
         r'family & $N$ & harden : rigid & pilot : rigid & pilot chose harden & reached (r / h / p) \\', r'\midrule']
    for f, v in res['families'].items():
        L.append(f"{SHORT[f]} & {v['N']} & {v['harden_vs_rigid']['a_lower']} : {v['harden_vs_rigid']['b_lower']} & {v['pilot_vs_rigid']['a_lower']} : {v['pilot_vs_rigid']['b_lower']} & {v['picked_harden']} & "
                 f"{v['reached']['always-rigid']} / {v['reached']['always-harden']} / {v['reached']['pilot']} \\\\")
    L += [r'\midrule', f"all & {len(allk)} & {hv['a_lower']} : {hv['b_lower']} & {pv['a_lower']} : {pv['b_lower']} & {res['picked_harden']} & "
          f"{res['reached']['always-rigid']} / {res['reached']['always-harden']} / {res['reached']['pilot']} \\\\", r'\bottomrule', r'\end{tabular}',
          r'\caption{Held-out families (C15), $n=6$--$20$, 64 runs per policy. $a:b$ counts instances where the first policy\textquotesingle s result is lower than the second\textquotesingle s and the reverse. The pilot spends 8 runs on each path, then 48 on the one whose pilot went lower. Reached (r / h / p): instances where always-rigid, always-harden and the pilot reach the best known value.}',
          r'\label{tab:decision}', r'\end{table}']
    open(os.path.join(ROOT, 'paper', 'tables', 'C15.tex'), 'w').write('\n'.join(L) + '\n')
    print(json.dumps({k: res[k] for k in ('pilot_vs_rigid', 'harden_vs_rigid', 'pilot_vs_harden', 'reached', 'picked_harden')}, indent=1))
    print(json.dumps(res['families'], indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=2)
    main(ap.parse_args().workers)
