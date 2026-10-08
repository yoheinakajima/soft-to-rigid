#!/usr/bin/env python3
"""Verify a cubes-in-cube packing file. Usage: python3 verify.py file.json
Pieces are [x, y, z, qw, qx, qy, qz]: unit cube centred at (x,y,z), rotated by the unit quaternion q.
Checks every corner lies in [0, s]^3 and every pair is separated (15-axis separating-axis test).
Prints s, min wall gap, min pair gap (SAT separation, a lower bound on distance). Exits 1 on any failure."""
import json, sys, itertools
d = json.load(open(sys.argv[1])); s = float(d['s_full']); P = d['pieces']; ok = True
def rot(q):
    n = sum(v * v for v in q) ** 0.5
    if abs(n - 1) > 1e-12: print(f'note: quaternion normalized (|q| = {n:.15f})')
    w, x, y, z = (v / n for v in q)
    return [[1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)], [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)], [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]]
cubes = []
for p in P:
    R = rot(p[3:]); ax = [[R[0][k], R[1][k], R[2][k]] for k in range(3)]   # cube axes = columns of R
    V = [[p[i] + sum(g[k] * ax[k][i] for k in range(3)) for i in range(3)] for g in itertools.product((-.5, .5), repeat=3)]
    cubes.append((p[:3], ax, V))
wall = min(min(min(v[i], s - v[i]) for v in V for i in range(3)) for _, _, V in cubes)
if wall < 0: ok = False; print('FAIL: a corner lies outside [0, s]^3')
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
cross = lambda a, b: [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
pair = float('inf')
for (i, (ca, A, VA)), (j, (cb, B, VB)) in itertools.combinations(enumerate(cubes), 2):
    axes = A + B + [c for a in A for b in B for c in [cross(a, b)] if dot(c, c) > 1e-18]
    units = [[x / dot(u, u) ** .5 for x in u] for u in axes]
    gap = max(max(min(dot(u, v) for v in VB) - max(dot(u, v) for v in VA), min(dot(u, v) for v in VA) - max(dot(u, v) for v in VB)) for u in units)
    pair = min(pair, gap)
    if gap <= 0: ok = False; print(f'FAIL: pieces {i} and {j} overlap or touch (gap {gap:.3e})')
print(f'n = {len(P)}  s = {s:.16f}\nmin wall gap = {wall:.12e}\nmin pair gap = {pair:.12e}\n' + ('VALID' if ok else 'INVALID'))
sys.exit(0 if ok else 1)
