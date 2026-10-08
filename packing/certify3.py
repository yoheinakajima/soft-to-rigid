"""Exact certificate for a cubes-in-cube claim (pieces [x, y, z, qw, qx, qy, qz], container [0, s]^3).

Every float is converted to an exact rational. Each quaternion q (not assumed unit) gives the exact rotation
R = H(q)/|q|^2, which is exactly orthogonal for any q != 0. Corners c + R g, g in {±1/2}^3, are exact rationals.
Checked with no rounding: (1) every corner lies in [0, s]^3; (2) every pair is strictly separated by an explicit
rational plane (a linear program proposes the normal; the check max_A u.p < min_B u.p is exact).
Ported from soft-to-rigid-packing/certify_exact.py (the n = 12 record certificate).
"""
import itertools, json, sys
from fractions import Fraction as Fr
from scipy.optimize import linprog


def _H(q):
    w, x, y, z = (Fr(v) for v in q); n = w * w + x * x + y * y + z * z
    M = [[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)], [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)], [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]
    return [[e / n for e in row] for row in M]


def certify(d):
    s = Fr(d['s_full']); V = []
    for p in d['pieces']:
        c = [Fr(v) for v in p[:3]]; R = _H(p[3:])
        V.append([[c[i] + sum(R[i][k] * g[k] for k in range(3)) for i in range(3)] for g in itertools.product((Fr(-1, 2), Fr(1, 2)), repeat=3)])
    wall = min(min(v[i], s - v[i]) for Vi in V for v in Vi for i in range(3))
    if wall <= 0:
        return False, 'a corner lies outside [0, s]^3'
    worst = None
    for i, j in itertools.combinations(range(len(V)), 2):
        fa = [[float(x) for x in v] for v in V[i]]; fb = [[float(x) for x in v] for v in V[j]]
        A = [[*a, -1, 1] for a in fa] + [[-b[0], -b[1], -b[2], 1, 1] for b in fb]
        res = linprog([0, 0, 0, 0, -1], A_ub=A, b_ub=[0] * 16, bounds=[(-1, 1)] * 3 + [(None, None), (None, 1)], method='highs')
        u = [Fr(x).limit_denominator(10 ** 14) for x in res.x[:3]]
        gap = min(sum(u[k] * v[k] for k in range(3)) for v in V[j]) - max(sum(u[k] * v[k] for k in range(3)) for v in V[i])
        worst = gap if worst is None or gap < worst else worst
        if gap <= 0:
            return False, f'pair {i},{j}: no strictly separating plane found'
    return True, f'exact min wall gap {float(wall):.6e}; min plane margin {float(worst):.6e}; all corners inside, every pair strictly separated'


if __name__ == '__main__':
    ok, why = certify(json.load(open(sys.argv[1])))
    print(why); print('CERTIFIED' if ok else 'NOT CERTIFIED'); sys.exit(0 if ok else 1)
