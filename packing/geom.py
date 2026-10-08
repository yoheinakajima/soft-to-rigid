"""2D geometry shared by tightening, certification and projections.

Pieces are regular k-gons with unit side about their incenter (k = 0: unit-diameter circle).
Containers are centred at the origin with size L: square (side), triangle (equilateral, side), circle (radius).
Mirrors engine/engine2d.js so that a pose means the same thing in both.
"""
import math

PIECES = {'circle': 0, 'triangle': 3, 'square': 4, 'pentagon': 5, 'hexagon': 6, 'octagon': 8}


def piece(name):
    k = PIECES[name]
    if k == 0:
        return dict(k=0, g=[], rho=0.5, R=0.5)
    rho, R = 1 / (2 * math.tan(math.pi / k)), 1 / (2 * math.sin(math.pi / k))
    g = [(R * math.cos(-math.pi / 2 - math.pi / k + 2 * math.pi * i / k), R * math.sin(-math.pi / 2 - math.pi / k + 2 * math.pi * i / k)) for i in range(k)]
    return dict(k=k, g=g, rho=rho, R=R)


def container(name):
    if name == 'square':
        return dict(type=name, normals=[(1, 0), (0, 1), (-1, 0), (0, -1)], beta=[0.5] * 4)
    if name == 'triangle':
        b = 1 / (2 * math.sqrt(3))
        return dict(type=name, normals=[(math.cos(a), math.sin(a)) for a in (-math.pi / 2, math.pi / 6, 5 * math.pi / 6)], beta=[b] * 3)
    if name == 'circle':
        return dict(type=name, circle=True)
    raise ValueError(name)


def verts(P, x, y, t):
    c, s = math.cos(t), math.sin(t)
    return [(x + gx * c - gy * s, y + gx * s + gy * c) for gx, gy in P['g']]


def edge_normals(V):
    k = len(V)
    out = []
    for e in range(k):
        ex, ey = V[(e + 1) % k][0] - V[e][0], V[(e + 1) % k][1] - V[e][1]
        l = math.hypot(ex, ey)
        out.append((ey / l, -ex / l))
    return out


def pair_gap(P, a, b):
    """Separation of two rigid pieces: > 0 gap along the best separating axis (a lower bound on the
    distance), < 0 minus the penetration depth. a, b = (x, y, t)."""
    if P['k'] == 0:
        return math.hypot(a[0] - b[0], a[1] - b[1]) - 1
    VA, VB = verts(P, *a), verts(P, *b)
    best = -math.inf
    for ux, uy in edge_normals(VA) + edge_normals(VB):
        pa = [ux * p[0] + uy * p[1] for p in VA]
        pb = [ux * p[0] + uy * p[1] for p in VB]
        best = max(best, min(pb) - max(pa), min(pa) - max(pb))
    return best


def wall_gap(P, C, L, pose):
    """Smallest distance from the piece to the container boundary (negative = outside)."""
    x, y, t = pose
    pts = [(x, y)] if P['k'] == 0 else verts(P, x, y, t)
    pad = 0.5 if P['k'] == 0 else 0
    if C.get('circle'):
        return min(L - math.hypot(*p) - pad for p in pts)
    return min(b * L - (ax * p[0] + ay * p[1]) - pad for (ax, ay), b in zip(C['normals'], C['beta']) for p in pts)


def min_enclosing_circle(pts):
    c, r = list(pts[0]), 0.0

    def inside(p):
        return math.hypot(p[0] - c[0], p[1] - c[1]) <= r + 1e-14
    for i in range(1, len(pts)):
        if inside(pts[i]):
            continue
        c, r = list(pts[i]), 0.0
        for j in range(i):
            if inside(pts[j]):
                continue
            c = [(pts[i][0] + pts[j][0]) / 2, (pts[i][1] + pts[j][1]) / 2]
            r = math.hypot(pts[i][0] - c[0], pts[i][1] - c[1])
            for m in range(j):
                if inside(pts[m]):
                    continue
                a, b, q = pts[i], pts[j], pts[m]
                bx, by, cx, cy = b[0] - a[0], b[1] - a[1], q[0] - a[0], q[1] - a[1]
                D = 2 * (bx * cy - by * cx)
                if abs(D) < 1e-300:
                    continue
                ux = (cy * (bx * bx + by * by) - by * (cx * cx + cy * cy)) / D
                uy = (bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by)) / D
                c, r = [a[0] + ux, a[1] + uy], math.hypot(ux, uy)
    return c, r


def tight_container(P, C, poses):
    """Smallest container (translation free, orientation fixed) holding all pieces: (L, cx, cy)."""
    pts = []
    for p in poses:
        pts += [(p[0], p[1])] if P['k'] == 0 else verts(P, *p)
    pad = 0.5 if P['k'] == 0 else 0
    if C.get('circle'):
        c, r = min_enclosing_circle(pts)
        return r + pad, c[0], c[1]
    h = [max(ax * q[0] + ay * q[1] for q in pts) + pad for ax, ay in C['normals']]
    if C['type'] == 'square':
        return max(h[0] + h[2], h[1] + h[3]), (h[0] - h[2]) / 2, (h[1] - h[3]) / 2
    b = C['beta'][0]
    L = sum(h) / (3 * b)
    (a0x, a0y), (a1x, a1y) = C['normals'][0], C['normals'][1]
    r0, r1 = h[0] - b * L, h[1] - b * L
    det = a0x * a1y - a0y * a1x
    return L, (r0 * a1y - a0y * r1) / det, (a0x * r1 - r0 * a1x) / det


def legalize(P, C, poses, tol=1e-12):
    """Scale centres apart about their mean until no pair overlaps by more than tol; return the tight
    container size and the poses re-centred on it."""
    n = len(poses)
    mx, my = sum(p[0] for p in poses) / n, sum(p[1] for p in poses) / n
    cut = 2 * P['R'] + 1e-9

    def placed(s):
        return [(mx + s * (p[0] - mx), my + s * (p[1] - my), p[2]) for p in poses]

    def ok(s):
        Q = placed(s)
        for i in range(n):
            for j in range(i + 1, n):
                if math.hypot(Q[i][0] - Q[j][0], Q[i][1] - Q[j][1]) <= cut and pair_gap(P, Q[i], Q[j]) < -tol:
                    return False
        return True
    lo = hi = 1.0
    if not ok(1.0):
        hi = 1.0001
        while not ok(hi):
            hi = 1 + (hi - 1) * 2
        for _ in range(60):
            m = (lo + hi) / 2
            if ok(m):
                hi = m
            else:
                lo = m
    Q = placed(hi)
    L, cx, cy = tight_container(P, C, Q)
    return L, hi, [(q[0] - cx, q[1] - cy, q[2]) for q in Q]
