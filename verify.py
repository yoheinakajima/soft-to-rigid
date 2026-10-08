"""Check a claim file: python3 verify.py claims/<claim>/claim.json   (standard library only; exit 1 on failure)
Piece: regular k-gon with unit side (k=0: circle of diameter 1); vertex i at R*(cos a_i, sin a_i), a_i = -pi/2 - pi/k + 2*pi*i/k,
rotated by theta about (x, y). Container centred at the origin: square (side s), triangle (side s, one side down), circle (radius s)."""
import json, math, sys
c = json.load(open(sys.argv[1])); s, k = c['s_full'], {'circle': 0, 'triangle': 3, 'square': 4, 'hexagon': 6}[c['piece']]
R = 0.5 if k == 0 else 1 / (2 * math.sin(math.pi / k))
def verts(x, y, t):
    if k == 0: return [(x, y)]
    a = [-math.pi / 2 - math.pi / k + 2 * math.pi * i / k for i in range(k)]
    return [(x + R * math.cos(b + t), y + R * math.sin(b + t)) for b in a]
def axes(V):
    return [((V[(i + 1) % len(V)][1] - V[i][1]), -(V[(i + 1) % len(V)][0] - V[i][0])) for i in range(len(V))]
V = [verts(*p) for p in c['pieces']]; pad = 0.5 if k == 0 else 0.0
if c['container'] == 'circle': walls = [s - pad - math.hypot(*v) for P in V for v in P]
else:
    N = {'square': [(1, 0, .5), (0, 1, .5), (-1, 0, .5), (0, -1, .5)],
         'triangle': [(math.cos(a), math.sin(a), 1 / (2 * math.sqrt(3))) for a in (-math.pi / 2, math.pi / 6, 5 * math.pi / 6)]}[c['container']]
    walls = [b * s - pad - (ax * v[0] + ay * v[1]) for ax, ay, b in N for P in V for v in P]
gaps = []
for i in range(len(V)):
    for j in range(i + 1, len(V)):
        if k == 0: gaps.append(math.dist(V[i][0], V[j][0]) - 1); continue
        g = -math.inf
        for ux, uy in axes(V[i]) + axes(V[j]):
            l = math.hypot(ux, uy); pa = [(ux * p[0] + uy * p[1]) / l for p in V[i]]; pb = [(ux * p[0] + uy * p[1]) / l for p in V[j]]
            g = max(g, min(pb) - max(pa), min(pa) - max(pb))
        gaps.append(g)
ok = min(walls) > 0 and min(gaps) > 0
print(f"{c['problem']}  n = {len(V)}  s = {s!r}\nmin wall gap = {min(walls):.12e}\nmin pair gap = {min(gaps):.12e}\n{'VALID' if ok else 'INVALID'}")
sys.exit(0 if ok else 1)
