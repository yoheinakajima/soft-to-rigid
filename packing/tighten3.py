"""Exact-contact tightening for unit-cube packings (3D).

Minimize the container side L subject to hard constraints:
  - every vertex of every cube lies in [0, L]^3
  - for every nearby pair (i, j) a separating plane u·p = c has all vertices of i on one side
    and all vertices of j on the other.
Cube orientation is R_i = Rod(phi_i) R0_i with phi re-based each outer iteration; plane normals are
parameterized in the tangent plane of the current normal. SLSQP, trust region, pair list rebuilt
each outer iteration. Results are certified independently (15-axis SAT, tolerance 1e-12, centres
scaled apart if needed, tight bounding cube measured).
"""
import json, math, sys, time
import numpy as np
from scipy.optimize import minimize

G = np.array([[a, b, c] for a in (1, -1) for b in (1, -1) for c in (1, -1)], float) * 0.5  # 8x3 local corners


def quat_to_R(q):
    w, x, y, z = q
    # columns = local axes (matches sim3.js axes(): rows there are axes; here R[:,k] = axis k)
    a0 = [1 - 2 * (y * y + z * z), 2 * (x * y + w * z), 2 * (x * z - w * y)]
    a1 = [2 * (x * y - w * z), 1 - 2 * (x * x + z * z), 2 * (y * z + w * x)]
    a2 = [2 * (x * z + w * y), 2 * (y * z - w * x), 1 - 2 * (x * x + y * y)]
    return np.array([a0, a1, a2]).T


def rod(phi):
    th = np.linalg.norm(phi)
    if th < 1e-14:
        return np.eye(3)
    k = phi / th
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + math.sin(th) * K + (1 - math.cos(th)) * K @ K


def overlap(cA, RA, cB, RB, tol=1e-12):
    D = cB - cA
    axs = [RA[:, k] for k in range(3)] + [RB[:, k] for k in range(3)]
    for i in range(3):
        for j in range(3):
            w = np.cross(RA[:, i], RB[:, j]); l = np.linalg.norm(w)
            if l > 1e-9: axs.append(w / l)
    for u in axs:
        rA = 0.5 * np.abs(u @ RA).sum(); rB = 0.5 * np.abs(u @ RB).sum()
        if rA + rB - abs(u @ D) <= tol:
            return False
    return True


def certify(C, R):
    C = np.array(C, float); n = len(C); cen = C.mean(0)

    def ok(k):
        P = cen + k * (C - cen)
        for i in range(n):
            for j in range(i + 1, n):
                if np.sum((P[i] - P[j]) ** 2) > 3.0001: continue
                if overlap(P[i], R[i], P[j], R[j]): return False
        return True

    lo = hi = 1.0
    if not ok(1.0):
        hi = 1.0001
        while not ok(hi): hi = 1 + (hi - 1) * 2
        for _ in range(70):
            m = (lo + hi) / 2
            if ok(m): hi = m
            else: lo = m
    P = cen + hi * (C - cen)
    V = np.concatenate([P[i] + G @ R[i].T for i in range(n)])
    mn, mx = V.min(0), V.max(0)
    side = float((mx - mn).max())
    off = mn - (side - (mx - mn)) / 2
    return side, hi, P - off


def init_plane(cA, RA, cB, RB):
    VA = cA + G @ RA.T; VB = cB + G @ RB.T
    axs = [RA[:, k] for k in range(3)] + [RB[:, k] for k in range(3)]
    for i in range(3):
        for j in range(3):
            w = np.cross(RA[:, i], RB[:, j]); l = np.linalg.norm(w)
            if l > 1e-9: axs.append(w / l)
    best = None
    for u in axs:
        for sgn in (1, -1):
            v = sgn * u
            g = (VB @ v).min() - (VA @ v).max()
            if best is None or g > best[0]: best = (g, v, ((VB @ v).min() + (VA @ v).max()) / 2)
    return best[1], best[2]


def tangent_basis(u):
    a = np.array([1.0, 0, 0]) if abs(u[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(u, a); e1 /= np.linalg.norm(e1)
    e2 = np.cross(u, e1)
    return e1, e2


def solve(C, R, L, outer=40, trust=0.03, verbose=False):
    C = np.array(C, float); R = [np.array(r) for r in R]; n = len(C)
    hist = []
    for it in range(outer):
        lim = (math.sqrt(3) + 4 * trust + 0.05) ** 2
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if np.sum((C[i] - C[j]) ** 2) < lim]
        P = len(pairs)
        U0, E1, E2, c0 = [], [], [], []
        for i, j in pairs:
            u, c = init_plane(C[i], R[i], C[j], R[j]); e1, e2 = tangent_basis(u)
            U0.append(u); E1.append(e1); E2.append(e2); c0.append(c)
        U0, E1, E2 = np.array(U0).reshape(P, 3), np.array(E1).reshape(P, 3), np.array(E2).reshape(P, 3)
        nv = 6 * n + 1 + 3 * P
        iL = 6 * n
        z0 = np.concatenate([C.ravel(), np.zeros(3 * n), [L], np.zeros(2 * P), c0])
        pi = np.array([p[0] for p in pairs], int); pj = np.array([p[1] for p in pairs], int)
        LG = [G @ R[i].T for i in range(n)]  # local corner offsets in world frame at phi=0

        def verts(z):
            Cz = z[:3 * n].reshape(n, 3); Ph = z[3 * n:6 * n].reshape(n, 3)
            return np.stack([Cz[i] + LG[i] @ rod(Ph[i]).T for i in range(n)])  # n x 8 x 3

        def cons(z):
            V = verts(z); Lz = z[iL]
            g = [V.ravel(), (Lz - V).ravel()]
            if P:
                ab = z[iL + 1:iL + 1 + 2 * P].reshape(P, 2); c = z[iL + 1 + 2 * P:]
                U = U0 + ab[:, :1] * E1 + ab[:, 1:] * E2
                U = U / np.linalg.norm(U, axis=1, keepdims=True)
                sA = np.einsum('pkd,pd->pk', V[pi], U); sB = np.einsum('pkd,pd->pk', V[pj], U)
                g += [(c[:, None] - sA).ravel(), (sB - c[:, None]).ravel()]
            return np.concatenate(g)

        bounds = ([(v - trust, v + trust) for v in C.ravel()] + [(-3 * trust, 3 * trust)] * (3 * n) +
                  [(L - 0.2, L + 0.01)] + [(-0.3, 0.3)] * (2 * P) + [(None, None)] * P)
        res = minimize(lambda z: z[iL], z0, jac=lambda z: np.eye(nv)[iL], method='SLSQP', bounds=bounds,
                       constraints=[{'type': 'ineq', 'fun': cons}], options={'maxiter': 300, 'ftol': 1e-15})
        z = res.x
        Cn = z[:3 * n].reshape(n, 3); Ph = z[3 * n:6 * n].reshape(n, 3)
        Rn = [rod(Ph[i]) @ R[i] for i in range(n)]
        side, k, Cc = certify(Cn, Rn)
        viol = -min(0.0, cons(z).min())
        hist.append((it, float(z[iL]), side, viol, P, res.status))
        if verbose: print(f'  it {it} L {z[iL]:.12f} certified {side:.12f} viol {viol:.1e} pairs {P} status {res.status}', flush=True)
        if side < L - 1e-13:
            imp = L - side
            C, R, L = Cc, Rn, side
            if imp < 1e-12: break
        else:
            trust *= 0.5
            if trust < 1e-4: break
    return float(L), C, R, hist



def R_to_quat(R):
    """rotation matrix (columns = cube axes) -> unit quaternion [w, x, y, z] (inverse of quat_to_R)."""
    R = np.asarray(R)
    # quat_to_R builds columns a_k; the matrix with rows a_k is the standard rotation of q. Undo the transpose.
    M = R.T
    t = M[0, 0] + M[1, 1] + M[2, 2]
    if t > 0:
        S = math.sqrt(t + 1) * 2; w = S / 4; x = (M[1, 2] - M[2, 1]) / S; y = (M[2, 0] - M[0, 2]) / S; z = (M[0, 1] - M[1, 0]) / S
    elif M[0, 0] > M[1, 1] and M[0, 0] > M[2, 2]:
        S = math.sqrt(1 + M[0, 0] - M[1, 1] - M[2, 2]) * 2; w = (M[1, 2] - M[2, 1]) / S; x = S / 4; y = (M[0, 1] + M[1, 0]) / S; z = (M[0, 2] + M[2, 0]) / S
    elif M[1, 1] > M[2, 2]:
        S = math.sqrt(1 + M[1, 1] - M[0, 0] - M[2, 2]) * 2; w = (M[2, 0] - M[0, 2]) / S; x = (M[0, 1] + M[1, 0]) / S; y = S / 4; z = (M[1, 2] + M[2, 1]) / S
    else:
        S = math.sqrt(1 + M[2, 2] - M[0, 0] - M[1, 1]) * 2; w = (M[0, 1] - M[1, 0]) / S; x = (M[0, 2] + M[2, 0]) / S; y = (M[1, 2] + M[2, 1]) / S; z = S / 4
    q = np.array([w, x, y, z]); return list(q / np.linalg.norm(q))


def solve_poses(poses, outer=40):
    """poses: [x, y, z, qw, qx, qy, qz] (any origin). Returns dict(L, poses) with poses in [0, L]^3."""
    C = [p[:3] for p in poses]
    R = [quat_to_R(p[3:]) for p in poses]
    L0, _, Cc = certify(C, R)
    L, C2, R2, hist = solve(Cc, R, L0, outer=outer)
    return dict(L=L, L0=L0, poses=[list(map(float, c)) + R_to_quat(r) for c, r in zip(C2, R2)], history=[h[2] for h in hist])
