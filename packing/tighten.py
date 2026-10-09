"""Exact tightening of a 2D packing.

Minimise the container size L over piece poses and one separating line per nearby pair:
  - every vertex of every piece inside the container (square / triangle: half-planes; circle: radius);
  - for each nearby pair (i, j) a line u(phi)·p = c with i's vertices on one side and j's on the other
    (circles: centre distance >= 1).
SLSQP with analytic Jacobians, in outer iterations with a trust region; the pair list and the line
initialisation are rebuilt each iteration, and a step is kept only if the independently legalised size
(geom.legalize: separating-axis test, tolerance 1e-12) goes down.
"""
import math
import numpy as np
from scipy.optimize import minimize
from . import geom


def _init_line(VA, VB):
    best = None
    for ux, uy in geom.edge_normals(VA) + geom.edge_normals(VB):
        for s in (1, -1):
            a = math.atan2(s * uy, s * ux)
            vx, vy = math.cos(a), math.sin(a)
            mi = max(vx * p[0] + vy * p[1] for p in VA)
            mj = min(vx * p[0] + vy * p[1] for p in VB)
            if best is None or mj - mi > best[0]:
                best = (mj - mi, a, (mi + mj) / 2)
    return best[1], best[2]


def solve(piece_name, container_name, poses, outer=20, trust=0.03, verbose=False):
    if piece_name == 'cube':
        from . import tighten3
        return tighten3.solve_poses(poses)
    P, C = geom.piece(piece_name), geom.container(container_name)
    L0, _, poses = geom.legalize(P, C, poses)
    best = (L0, poses)
    n, k = len(poses), P['k']
    G = np.array(P['g']) if k else np.zeros((0, 2))
    circ = C.get('circle', False)
    hist = [L0]
    fails = 0
    for it in range(outer):
        X = np.array([p[0] for p in best[1]]); Y = np.array([p[1] for p in best[1]]); T = np.array([p[2] for p in best[1]])
        L = best[0]
        cut = 2 * P['R'] + 4 * trust + 0.05
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if math.hypot(X[i] - X[j], Y[i] - Y[j]) < cut]
        Pn = len(pairs)
        pi_ = np.array([p[0] for p in pairs], int); pj_ = np.array([p[1] for p in pairs], int)
        lines = []
        if k:
            V = [geom.verts(P, X[i], Y[i], T[i]) for i in range(n)]
            lines = [_init_line(V[i], V[j]) for i, j in pairs]
        nl = Pn if k else 0
        iL = 3 * n
        nv = 3 * n + 1 + 2 * nl
        z0 = np.concatenate([X, Y, T, [L], [l[0] for l in lines], [l[1] for l in lines]])

        def unpack(z):
            return z[:n], z[n:2 * n], z[2 * n:3 * n], z[iL], z[iL + 1:iL + 1 + nl], z[iL + 1 + nl:]

        def vert_arrays(x, y, t):
            if not k:
                return x[:, None], y[:, None], np.zeros((n, 1)), np.zeros((n, 1))
            ct, st = np.cos(t)[:, None], np.sin(t)[:, None]
            A, B = G[:, 0][None, :], G[:, 1][None, :]
            return x[:, None] + A * ct - B * st, y[:, None] + A * st + B * ct, -A * st - B * ct, A * ct - B * st

        def cons(z):
            x, y, t, Lz, ph, c = unpack(z)
            vx, vy, _, _ = vert_arrays(x, y, t)
            g = []
            pad = 0.5 if not k else 0.0
            if circ:
                g.append(((Lz - pad) ** 2 - vx ** 2 - vy ** 2).ravel())
            else:
                for (ax, ay), b in zip(C['normals'], C['beta']):
                    g.append((b * Lz - pad - ax * vx - ay * vy).ravel())
            if Pn:
                if k:
                    ux, uy = np.cos(ph)[:, None], np.sin(ph)[:, None]
                    g.append((c[:, None] - ux * vx[pi_] - uy * vy[pi_]).ravel())
                    g.append((ux * vx[pj_] + uy * vy[pj_] - c[:, None]).ravel())
                else:
                    g.append((x[pi_] - x[pj_]) ** 2 + (y[pi_] - y[pj_]) ** 2 - 1.0)
            return np.concatenate(g)

        def jac(z):
            x, y, t, Lz, ph, c = unpack(z)
            vx, vy, dxt, dyt = vert_arrays(x, y, t)
            m = vx.shape[1]
            rows = []
            pad = 0.5 if not k else 0.0
            ii = np.repeat(np.arange(n), m)
            if circ:
                J = np.zeros((n * m, nv)); r = np.arange(n * m)
                J[r, ii] = -2 * vx.ravel(); J[r, n + ii] = -2 * vy.ravel()
                J[r, 2 * n + ii] = -2 * (vx * dxt + vy * dyt).ravel(); J[r, iL] = 2 * (Lz - pad)
                rows.append(J)
            else:
                for (ax, ay), b in zip(C['normals'], C['beta']):
                    J = np.zeros((n * m, nv)); r = np.arange(n * m)
                    J[r, ii] = -ax; J[r, n + ii] = -ay; J[r, 2 * n + ii] = -(ax * dxt + ay * dyt).ravel(); J[r, iL] = b
                    rows.append(J)
            if Pn:
                if k:
                    ux, uy = np.cos(ph)[:, None], np.sin(ph)[:, None]
                    for side, idx in ((1, pi_), (-1, pj_)):
                        J = np.zeros((Pn * m, nv)); r = np.arange(Pn * m)
                        pp = np.repeat(np.arange(Pn), m); pc = idx[pp]
                        # side=1: c - u·v_i ; side=-1: u·v_j - c
                        J[r, pc] = -side * np.repeat(ux[:, 0], m)
                        J[r, n + pc] = -side * np.repeat(uy[:, 0], m)
                        J[r, 2 * n + pc] = -side * (ux * dxt[idx] + uy * dyt[idx]).ravel()
                        J[r, iL + 1 + pp] = -side * (-np.sin(ph)[:, None] * vx[idx] + np.cos(ph)[:, None] * vy[idx]).ravel()
                        J[r, iL + 1 + nl + pp] = side
                        rows.append(J)
                else:
                    J = np.zeros((Pn, nv)); r = np.arange(Pn)
                    dx, dy = x[pi_] - x[pj_], y[pi_] - y[pj_]
                    J[r, pi_] = 2 * dx; J[r, pj_] = -2 * dx; J[r, n + pi_] = 2 * dy; J[r, n + pj_] = -2 * dy
                    rows.append(J)
            return np.vstack(rows)

        bounds = [(v - trust, v + trust) for v in np.concatenate([X, Y])] + [(v - 3 * trust, v + 3 * trust) for v in T] + [(0, None)] + [(None, None)] * (2 * nl)
        try:
            res = minimize(lambda z: z[iL], z0, jac=lambda z: np.eye(nv)[iL], constraints=[{'type': 'ineq', 'fun': cons, 'jac': jac}],
                           bounds=bounds, method='SLSQP', options={'maxiter': 300, 'ftol': 1e-15})
            z = res.x
        except Exception as e:  # recorded, not raised
            if verbose:
                print('slsqp error', e)
            break
        x, y, t, _, _, _ = unpack(z)
        Lnew, _, Q = geom.legalize(P, C, list(zip(x, y, t)))
        if Lnew < best[0] - 1e-13:
            gain = best[0] - Lnew
            best = (Lnew, Q)
            if gain < 1e-11:
                break
            hist.append(Lnew)
            if verbose:
                print(it, Lnew)
            fails = 0
        else:
            trust *= 0.5
            fails += 1
            if trust < 1e-7 or fails >= 4:
                break
    return dict(L=best[0], poses=[list(map(float, q)) for q in best[1]], history=hist, L0=L0)
