"""Paper figures, drawn from the ledger projection (site/data/cells.json) and replay files.

    python3 scripts/figures.py      # -> paper/figures/*.pdf and *.png
"""
import json, math, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
from packing import geom

OUT = os.path.join(ROOT, 'paper', 'figures'); os.makedirs(OUT, exist_ok=True)
METHODS = ['harden', 'grow', 'rigid', 'sa', 'pc']
COL = {'harden': '#d17a22', 'grow': '#6a8e3a', 'rigid': '#2f5d8a', 'sa': '#8a5aa8', 'pc': '#9a9a9a'}
MK = {'harden': 'o', 'grow': '^', 'rigid': 's', 'sa': 'D', 'pc': 'x'}
plt.rcParams.update({'font.family': 'serif', 'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False})
cells = json.load(open(os.path.join(ROOT, 'site', 'data', 'cells.json')))
fams = json.load(open(os.path.join(ROOT, 'site', 'data', 'families.json')))


def best_gap(c):
    g = c['best_gap'] if c.get('best_polished') is None else min(c['best_gap'], c['best_polished'] - c['record'])
    return max(g, 0) / c['record']


def fig_gaps(cid='C04-breadth'):
    cs = [c for c in cells if c['campaign'] == cid]
    fl = [f for f in ['squ-in-squ', 'squ-in-cir', 'squ-in-tri', 'tri-in-tri', 'tri-in-squ', 'hex-in-squ', 'cir-in-squ'] if any(c['family'] == f for c in cs)]
    if not fl:
        return
    cols = 4; rows = math.ceil(len(fl) / cols)
    fig, axs = plt.subplots(rows, cols, figsize=(7.2, 1.75 * rows), sharey=True, squeeze=False)
    for ax, f in zip(axs.flat, fl):
        for m in METHODS:
            pts = sorted((c['n'], best_gap(c)) for c in cs if c['family'] == f and c['method'] == m)
            if not pts:
                continue
            xs = [p[0] for p in pts]; ys = [max(p[1], 1e-7) for p in pts]
            ax.plot(xs, ys, MK[m], color=COL[m], ms=2.6, mew=0.8, label=m, alpha=0.9, mfc='none' if m in ('rigid', 'sa') else COL[m])
        ax.set_yscale('log'); ax.set_ylim(5e-8, 1); ax.set_title(fams[f]['title'].replace('Unit ', '').replace('equilateral ', '').replace('regular ', ''), fontsize=7.5)
        ax.axhline(1e-6, color='#bbb', lw=0.5); ax.set_xlabel('n', labelpad=1)
    for ax in axs.flat[len(fl):]:
        ax.axis('off')
    axs[0][0].set_ylabel('best gap / best known')
    h, l = axs[0][0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower right', ncol=5, frameon=False, bbox_to_anchor=(0.98, 0.02))
    fig.text(0.01, 0.005, 'Points at the bottom (below the grey line) reach the best known value.', fontsize=6.5, color='#555')
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(OUT, f'gaps.{ext}'), dpi=200)
    plt.close(fig)


def draw_packing(ax, piece, container, L, poses, color='#2f5d8a'):
    P, C = geom.piece(piece), geom.container(container)
    if container == 'circle':
        ax.add_patch(Circle((0, 0), L, fill=False, lw=0.8))
    elif container == 'square':
        ax.add_patch(Polygon([(-L / 2, -L / 2), (L / 2, -L / 2), (L / 2, L / 2), (-L / 2, L / 2)], fill=False, lw=0.8))
    else:
        rc = L / math.sqrt(3)
        ax.add_patch(Polygon([(rc * math.cos(a), rc * math.sin(a)) for a in (math.pi / 2, 7 * math.pi / 6, 11 * math.pi / 6)], fill=False, lw=0.8))
    for x, y, t in poses:
        if P['k'] == 0:
            ax.add_patch(Circle((x, y), 0.5, color=color, alpha=0.85, lw=0))
        else:
            ax.add_patch(Polygon(geom.verts(P, x, y, t), closed=True, color=color, alpha=0.85, lw=0.3, ec='white'))
    s = L * 0.62 if container != 'circle' else L * 1.05
    ax.set_xlim(-s, s); ax.set_ylim(-s, s); ax.set_aspect('equal'); ax.axis('off')


def fig_strip(replay_path, name, k=6):
    """k frames of one replay, from disks to the final packing."""
    R = json.load(open(replay_path))
    F = R['frames']; idx = [round(i * (len(F) - 1) / (k - 1)) for i in range(k)]
    fig, axs = plt.subplots(1, k, figsize=(7.2, 7.2 / k + 0.25))
    P = geom.piece(R['piece'])
    for ax, i in zip(axs, idx):
        f = F[i]; g, u = f['g'], f['u']
        L = f['L']
        if R['container'] == 'circle':
            ax.add_patch(Circle((0, 0), L, fill=False, lw=0.8))
        elif R['container'] == 'square':
            ax.add_patch(Polygon([(-L / 2, -L / 2), (L / 2, -L / 2), (L / 2, L / 2), (-L / 2, L / 2)], fill=False, lw=0.8))
        else:
            rc = L / math.sqrt(3); ax.add_patch(Polygon([(rc * math.cos(a), rc * math.sin(a)) for a in (math.pi / 2, 7 * math.pi / 6, 11 * math.pi / 6)], fill=False, lw=0.8))
        for j in range(R['n']):
            x, y, t = f['p'][3 * j:3 * j + 3]
            if P['k'] == 0 or g * (1 - u) < 1e-6:
                ax.add_patch(Circle((x, y), g * (u * P['rho'] if P['k'] else 0.5), color=COL['harden'], alpha=0.85, lw=0))
            else:
                # rounded polygon: sample the Minkowski sum boundary
                s, r = g * (1 - u), g * u * P['rho']
                V = [(x + s * (a * math.cos(t) - b * math.sin(t)), y + s * (a * math.sin(t) + b * math.cos(t))) for a, b in P['g']]
                pts = []
                for e in range(len(V)):
                    A, B, Cn = V[e], V[(e + 1) % len(V)], V[(e + 2) % len(V)]
                    n1 = math.atan2(-(B[0] - A[0]), B[1] - A[1]); n2 = math.atan2(-(Cn[0] - B[0]), Cn[1] - B[1])
                    while n2 < n1: n2 += 2 * math.pi
                    pts += [(B[0] + r * math.cos(n1 + (n2 - n1) * q / 6), B[1] + r * math.sin(n1 + (n2 - n1) * q / 6)) for q in range(7)]
                col = COL['harden'] if u > 0.5 else COL['rigid']
                ax.add_patch(Polygon(pts, closed=True, color=col, alpha=0.85, lw=0.3, ec='white'))
        sp = (L * 0.62 if R['container'] != 'circle' else L * 1.05)
        ax.set_xlim(-sp, sp); ax.set_ylim(-sp, sp); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(f"{f['ph']}  τ={u:.2f}\nsize {L:.3f}", fontsize=6.5)
    fig.tight_layout(pad=0.3)
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(OUT, f'{name}.{ext}'), dpi=220)
    plt.close(fig)


if __name__ == '__main__':
    fig_gaps()
    for a in sys.argv[1:]:
        p, name = a.split('=')
        fig_strip(p, name)
    print('figures in', OUT)
