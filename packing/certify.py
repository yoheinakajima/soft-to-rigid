"""Exact certificate for a 2D claim file:  python3 -m packing.certify claims/<claim>/claim.json

Every number is converted to an exact rational and checked with no rounding:
  * rotations: t = tan(theta/2) is rationalised and cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2), which is an
    exact rotation; it differs from the stated theta by about 1e-13 rad.
  * pieces: each vertex is the float vertex of the unit polygon scaled by (1 + 1e-8), taken as an exact
    rational. enclosure() proves exactly, in Q(sqrt 3), that this polygon contains the true unit polygon with a
    margin of 1e-9, more than the rotation and rounding discrepancies (< 1e-12), so a valid packing of the
    inflated pieces is a valid packing of the true ones. Circles are inflated to radius (1 + 1e-8)/2.
  * container: the square is |x|, |y| < s/2; the circle x^2 + y^2 < s^2; the triangle's walls involve sqrt(3)
    and are checked as numbers a + b*sqrt(3) with rational a, b, whose sign is decided exactly.
  * pairs: for each pair, a rational direction u (from the best floating-point separating axis) is
    exhibited with max_{v in A} u.v < min_{w in B} u.v exactly (circles: squared centre distance).
"""
import json, math, sys
from fractions import Fraction as Fr

INFL = 1 + 1e-8


def sign_sqrt3(a, b):
    """sign of a + b*sqrt(3) for rationals a, b."""
    if a >= 0 and b >= 0:
        return 0 if a == 0 and b == 0 else 1
    if a <= 0 and b <= 0:
        return -1
    # opposite signs: compare a^2 with 3 b^2
    d = a * a - 3 * b * b
    if d == 0:
        return 0
    return (1 if d > 0 else -1) * (1 if a > 0 else -1)


# exact unit polygons, coordinates a + b*sqrt(3) stored as (a, b) with rational a, b
_H = Fr(1, 2)
EXACT = {
    4: [((-_H, 0), (-_H, 0)), ((_H, 0), (-_H, 0)), ((_H, 0), (_H, 0)), ((-_H, 0), (_H, 0))],
    3: [((-_H, 0), (0, Fr(-1, 6))), ((_H, 0), (0, Fr(-1, 6))), ((0, 0), (0, Fr(1, 3)))],
    6: [((-_H, 0), (0, -_H)), ((_H, 0), (0, -_H)), ((Fr(1), 0), (0, 0)), ((_H, 0), (0, _H)), ((-_H, 0), (0, _H)), ((Fr(-1), 0), (0, 0))],
}
ENC_EPS = Fr(1, 10 ** 9)


def enclosure(k, G):
    """Prove, exactly, that the unit regular k-gon (vertices in Q(sqrt 3)) dilated by ENC_EPS lies inside the
    rational surrogate polygon G used by the certificate: for every edge pq of G and every exact vertex v,
    cross(q - p, v - p) - ENC_EPS * |q - p|_upper >= 0, decided as the sign of a + b*sqrt(3).
    ENC_EPS (1e-9) exceeds every discrepancy between the claimed float rotation and the rational one used."""
    if k == 0:
        return True, 'circle pieces: radius inflated by 1e-8 exactly'
    V = EXACT[k]
    worst = None
    for e in range(k):
        (px, py), (qx, qy) = G[e], G[(e + 1) % k]
        ex, ey = qx - px, qy - py
        L2 = ex * ex + ey * ey
        Lup = Fr(math.sqrt(float(L2)) * (1 + 1e-12)).limit_denominator(10 ** 12)
        while Lup * Lup < L2:
            Lup *= Fr(1000001, 1000000)
        for (xa, xb), (ya, yb) in V:
            # cross = ex*(vy - py) - ey*(vx - px), with vx = xa + xb*s3, vy = ya + yb*s3
            a = ex * (ya - py) - ey * (xa - px) - ENC_EPS * Lup
            b = ex * yb - ey * xb
            if sign_sqrt3(a, b) <= 0:
                return False, f'vertex not enclosed by surrogate edge {e}'
            val = float(a) + float(b) * math.sqrt(3)
            worst = val if worst is None else min(worst, val)
    return True, f'unit {k}-gon + 1e-9 margin enclosed by the surrogate (worst slack {worst:.2e})'


def certify(claim):
    k = {'circle': 0, 'triangle': 3, 'square': 4, 'hexagon': 6}[claim['piece']]
    s = Fr(claim['s_full'])
    R = 0.5 if k == 0 else 1 / (2 * math.sin(math.pi / k))
    G = [(Fr(R * INFL * math.cos(a)), Fr(R * INFL * math.sin(a))) for a in
         [-math.pi / 2 - math.pi / k + 2 * math.pi * i / k for i in range(k)]] if k else []
    V, C = [], []
    for x, y, t in claim['pieces']:
        tt = Fr(math.tan(t / 2)).limit_denominator(10 ** 15)
        c, sn = (1 - tt * tt) / (1 + tt * tt), 2 * tt / (1 + tt * tt)
        X, Y = Fr(x), Fr(y)
        C.append((X, Y))
        V.append([(X + gx * c - gy * sn, Y + gx * sn + gy * c) for gx, gy in G] if k else [(X, Y)])
    ok_enc, why_enc = enclosure(k, G)
    if not ok_enc:
        return False, why_enc
    rad = Fr(INFL) / 2 if k == 0 else Fr(0)
    # container
    worst = None
    for P in V:
        for vx, vy in P:
            if claim['container'] == 'square':
                m = min(s / 2 - rad - vx, s / 2 - rad + vx, s / 2 - rad - vy, s / 2 - rad + vy)
                if m <= 0:
                    return False, 'outside square'
                worst = m if worst is None else min(worst, m)
            elif claim['container'] == 'circle':
                if (s - rad) <= 0 or vx * vx + vy * vy >= (s - rad) ** 2:
                    return False, 'outside circle'
            else:  # triangle, three walls multiplied by 2*sqrt(3): s - 2*sqrt(3)*rad + ... > 0
                for a, b in ((s + 0, 2 * vy), (s - 3 * vx, -vy), (s + 3 * vx, -vy)):
                    if sign_sqrt3(a, b - 2 * rad) <= 0:
                        return False, 'outside triangle'
    # pairs
    n = len(V)
    for i in range(n):
        for j in range(i + 1, n):
            if k == 0:
                if (C[i][0] - C[j][0]) ** 2 + (C[i][1] - C[j][1]) ** 2 <= (2 * rad) ** 2:
                    return False, f'circles {i},{j} overlap'
                continue
            best = None
            fV = [[(float(a), float(b)) for a, b in P] for P in (V[i], V[j])]
            for P in fV:
                for e in range(k):
                    ux, uy = P[(e + 1) % k][1] - P[e][1], -(P[(e + 1) % k][0] - P[e][0])
                    g = max(min(ux * q[0] + uy * q[1] for q in fV[1]) - max(ux * q[0] + uy * q[1] for q in fV[0]),
                            min(ux * q[0] + uy * q[1] for q in fV[0]) - max(ux * q[0] + uy * q[1] for q in fV[1]))
                    if best is None or g > best[0]:
                        best = (g, ux, uy)
            ux, uy = Fr(best[1]), Fr(best[2])
            pa = [ux * a + uy * b for a, b in V[i]]
            pb = [ux * a + uy * b for a, b in V[j]]
            if not (max(pa) < min(pb) or max(pb) < min(pa)):
                return False, f'pair {i},{j} not separated'
    return True, 'all pieces inside, every pair strictly separated; ' + why_enc


if __name__ == '__main__':
    cl = json.load(open(sys.argv[1]))
    ok, why = certify(cl)
    print(f"{cl['problem']} n = {len(cl['pieces'])} s = {cl['s_full']!r}\nexact check: {why}\n{'CERTIFIED' if ok else 'NOT CERTIFIED'}")
    sys.exit(0 if ok else 1)
