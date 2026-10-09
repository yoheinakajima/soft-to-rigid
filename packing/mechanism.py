"""Mechanism measurements from replays (descriptive): what pieces do while their shape changes.

    python3 -m packing.mechanism    # -> analysis/mechanism.json, paper/figures/mechanism.pdf, paper/mechanism.tex

For the best run (lowest legalised size, before tightening) of harden and rigid on every C07 instance (its replay), with polygons k = 3, 4, 6:
  move    mean net displacement of a piece's centre from the end of compression to the end of the run (unit side)
  turn    mean net |change of orientation| between the same two frames, modulo the piece's symmetry 2pi/k (degrees)
  order   orientational order |mean exp(i k theta)| at the middle recorded frame of the morph phase (the same step of the
          schedule for every path; for hardening tau is about 0.5 there)
  tilt    share of pieces in the final packing with no edge within 2 degrees of parallel to a container edge
          (square and triangle containers only)
"""
import glob, json, math, os, statistics as S
from collections import defaultdict
from .ledger import ROOT

K = {'triangle': 3, 'square': 4, 'hexagon': 6}
CONT_EDGES = {'square': [0.0, math.pi / 2], 'triangle': [0.0, math.pi / 3, 2 * math.pi / 3]}
FAMS = ['squ-in-squ', 'squ-in-cir', 'squ-in-tri', 'tri-in-tri', 'tri-in-squ', 'hex-in-squ']


def piece_edge_dirs(k, th):
    a = [-math.pi / 2 - math.pi / k + 2 * math.pi * i / k + th for i in range(k)]
    V = [(math.cos(x), math.sin(x)) for x in a]
    return [math.atan2(V[(i + 1) % k][1] - V[i][1], V[(i + 1) % k][0] - V[i][0]) for i in range(k)]


def adiff(a, b, period):
    d = (a - b) % period
    return min(d, period - d)


def measure(R):
    k = K.get(R['piece'])
    if not k:
        return None
    F = R['frames']; n = R['n']
    comp = [f for f in F if f['ph'] == 'compress']
    sett = [f for f in F if f['ph'] == 'settle']
    if not comp or not sett:
        return None
    a, b = comp[-1]['p'], sett[-1]['p']
    move = S.mean(math.hypot(b[3 * i] - a[3 * i], b[3 * i + 1] - a[3 * i + 1]) for i in range(n))
    sym = 2 * math.pi / k
    turn = math.degrees(S.mean(adiff(b[3 * i + 2], a[3 * i + 2], sym) for i in range(n)))
    order = None
    morph = [f for f in F if f['ph'] == 'morph']
    if morph:
        p = morph[len(morph) // 2]['p']
        c = sum(math.cos(k * p[3 * i + 2]) for i in range(n)) / n; s = sum(math.sin(k * p[3 * i + 2]) for i in range(n)) / n
        order = math.hypot(c, s)
    tilt = None
    if R['container'] in CONT_EDGES:
        fin = F[-1]['p']; tilted = 0
        for i in range(n):
            ds = [adiff(e, c, math.pi) for e in piece_edge_dirs(k, fin[3 * i + 2]) for c in CONT_EDGES[R['container']]]
            tilted += min(ds) > math.radians(2)
        tilt = tilted / n
    return {'move': move, 'turn': turn, 'order': order, 'tilt': tilt}


def main():
    cells = {c['cell']: c for c in json.load(open(os.path.join(ROOT, 'site', 'data', 'cells.json')))}
    out = defaultdict(dict)
    for f in glob.glob(os.path.join(ROOT, 'campaigns', 'C07-breadth-best', 'replays', '*.json')):
        R = json.load(open(f)); m = R['method'].replace('-best', '')
        if m not in ('harden', 'rigid') or R['family'] not in FAMS or R['n'] < 6:
            continue
        x = measure(R)
        if x:
            c = cells.get(f"C07-breadth-best/{R['family']}/n{R['n']}/{R['method']}/B1/default", {})
            x['sole'] = bool(c.get('sole_lowest')); x['lowest'] = bool(c.get('is_lowest'))
            out[(R['family'], R['n'])][m] = x
    summ = {}
    for fam in FAMS:
        for m in ('harden', 'rigid'):
            xs = [v[m] for (f, n), v in out.items() if f == fam and m in v]
            if xs:
                summ[f'{fam}/{m}'] = {k: round(S.median([x[k] for x in xs if x[k] is not None]), 3) if any(x[k] is not None for x in xs) else None for k in ('move', 'turn', 'order', 'tilt')}
    sole = {f'{f}/n{n}': v['harden'] for (f, n), v in out.items() if 'harden' in v and v['harden']['sole']}
    json.dump({'median': summ, 'harden_sole_wins': sole, 'per_instance': {f'{f}/n{n}': v for (f, n), v in out.items()}}, open(os.path.join(ROOT, 'analysis', 'mechanism.json'), 'w'), indent=1)
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.size': 7, 'axes.spines.top': False, 'axes.spines.right': False})
    lab = {'squ-in-squ': 'sq/sq', 'squ-in-cir': 'sq/cir', 'squ-in-tri': 'sq/tri', 'tri-in-tri': 'tri/tri', 'tri-in-squ': 'tri/sq', 'hex-in-squ': 'hex/sq'}
    col = {'harden': '#d17a22', 'rigid': '#2f5d8a'}
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 1.9))
    for ax, key, ttl in zip(axs, ('move', 'turn', 'tilt'), ('net displacement after compression\n(unit sides)', 'net rotation after compression (deg)', 'share of tilted pieces, final')):
        for j, fam in enumerate(FAMS):
            for d, m in ((-0.18, 'harden'), (0.18, 'rigid')):
                ys = [(v[m][key], v[m]['sole']) for (f, n), v in out.items() if f == fam and m in v and v[m][key] is not None]
                if not ys:
                    continue
                ax.scatter([j + d] * len(ys), [y for y, s in ys], s=[14 if s else 4 for y, s in ys], c=col[m], alpha=0.6, lw=0, label=m if j == 0 else None)
        ax.set_xticks(range(len(FAMS))); ax.set_xticklabels([lab[f] for f in FAMS], fontsize=6); ax.set_title(ttl, fontsize=7)
    axs[0].legend(fontsize=6, frameon=False)
    fig.tight_layout(pad=0.3)
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(ROOT, 'paper', 'figures', f'mechanism.{ext}'), dpi=220)
    nums = []
    mac = {'squ-in-squ': 'SquSqu', 'tri-in-tri': 'TriTri', 'tri-in-squ': 'TriSqu', 'hex-in-squ': 'HexSqu', 'squ-in-cir': 'SquCir', 'squ-in-tri': 'SquTri'}
    for k2, v in summ.items():
        fam, m = k2.split('/')
        for q in ('move', 'turn', 'tilt', 'order'):
            if v[q] is not None:
                val = f"{v[q]:.2f}" if q != 'turn' else f"{v[q]:.0f}"
                nums.append(rf'\newcommand{{\Mech{mac[fam]}{m.capitalize()}{q.capitalize()}}}{{{val}}}')
    sw = [(v['harden']['tilt'], v['rigid']['tilt']) for (f, n), v in out.items() if f == 'squ-in-squ' and 'harden' in v and 'rigid' in v and v['harden']['sole']]
    tf = [(v['harden']['move'], v['rigid']['move']) for (f, n), v in out.items() if f == 'tri-in-tri' and 'harden' in v and 'rigid' in v and v['rigid']['sole']]
    nums += [rf'\newcommand{{\MechSoleN}}{{{len(sw)}}}', rf'\newcommand{{\MechSoleTiltH}}{{{S.median(a for a, b in sw):.2f}}}', rf'\newcommand{{\MechSoleTiltR}}{{{S.median(b for a, b in sw):.2f}}}',
             rf'\newcommand{{\MechSoleMore}}{{{sum(a > b for a, b in sw)}}}',
             rf'\newcommand{{\MechTriFailN}}{{{len(tf)}}}', rf'\newcommand{{\MechTriFailMoveH}}{{{S.median(a for a, b in tf):.2f}}}', rf'\newcommand{{\MechTriFailMoveR}}{{{S.median(b for a, b in tf):.2f}}}']
    open(os.path.join(ROOT, 'paper', 'mechanism.tex'), 'w').write('\n'.join(nums) + '\n')
    print(json.dumps(summ, indent=1)); print('harden sole wins:', json.dumps(sole, indent=0)[:1500])


if __name__ == '__main__':
    main()
