"""Turn a tightened packing into a claim folder: spread to a clearance, write the claim file, run both checks.

claims/<family>-n<N>/
  claim.json        container size at full precision, one [x, y, theta] pose per piece
  verify.txt        output of verify.py (floating point)
  certify.txt       output of packing.certify (exact rational)
"""
import json, math, os, subprocess, sys, time
from . import geom
from .certify import certify

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CLEAR = 1e-6


def spread(P, C, poses, clear=CLEAR):
    """Scale centres about the container centre until every pair is at least `clear` apart, then size the
    container so every piece is at least `clear` from the wall. Returns (s_full, poses)."""
    n = len(poses)

    def placed(f):
        return [(p[0] * f, p[1] * f, p[2]) for p in poses]

    def min_gap(Q):
        return min(geom.pair_gap(P, Q[i], Q[j]) for i in range(n) for j in range(i + 1, n))
    lo, hi = 1.0, 1.0 + 4 * clear
    while min_gap(placed(hi)) < clear:
        hi = 1 + (hi - 1) * 2
    for _ in range(60):
        m = (lo + hi) / 2
        if min_gap(placed(m)) >= clear:
            hi = m
        else:
            lo = m
    Q = placed(hi)
    L, cx, cy = geom.tight_container(P, C, Q)
    Q = [(q[0] - cx, q[1] - cy, q[2]) for q in Q]
    beta = 1.0 if C.get('circle') else min(C['beta'])
    s = L + clear / beta * (1 + 1e-6)
    s = math.ceil(s * 1e13) / 1e13
    return s, Q


def spread3(poses, clear=CLEAR):
    """cubes: scale centres about their mean until every pair is >= clear apart (15-axis SAT gap), then the
    tight bounding cube plus `clear` on every wall; returns (s_full, poses in [0, s]^3)."""
    import numpy as np
    from .tighten3 import quat_to_R
    C = np.array([p[:3] for p in poses]); R = [quat_to_R(p[3:]) for p in poses]; cen = C.mean(0); n = len(C)

    def gap(cA, RA, cB, RB):
        D = cB - cA; axs = [RA[:, k] for k in range(3)] + [RB[:, k] for k in range(3)]
        for i in range(3):
            for j in range(3):
                w = np.cross(RA[:, i], RB[:, j]); l = np.linalg.norm(w)
                if l > 1e-9: axs.append(w / l)
        return max(abs(u @ D) - 0.5 * np.abs(u @ RA).sum() - 0.5 * np.abs(u @ RB).sum() for u in axs)

    def mg(f):
        P = cen + f * (C - cen)
        return min(gap(P[i], R[i], P[j], R[j]) for i in range(n) for j in range(i + 1, n))
    lo, hi = 1.0, 1 + 4 * clear
    while mg(hi) < clear: hi = 1 + (hi - 1) * 2
    for _ in range(60):
        m = (lo + hi) / 2
        if mg(m) >= clear: hi = m
        else: lo = m
    P = cen + hi * (C - cen)
    h = np.array([[0.5 * np.abs(R[i][e, :]).sum() for e in range(3)] for i in range(n)])
    mn, mx = (P - h).min(0), (P + h).max(0)
    s = math.ceil((max(mx - mn) + 2 * clear * (1 + 1e-6)) * 1e13) / 1e13
    off = mn - (s - (mx - mn)) / 2
    return s, [list(map(float, P[i] - off)) + list(map(float, poses[i][3:])) for i in range(n)]


def make_claim(family, n, polished_path, found_by='Yohei Nakajima'):
    F = json.load(open(os.path.join(ROOT, 'catalog', family + '.json')))
    pol = json.load(open(polished_path))
    if F['piece'] == 'cube':
        return _make_claim3(F, family, n, pol, found_by)
    P, C = geom.piece(F['piece']), geom.container(F['container'])
    s, Q = spread(P, C, pol['poses'])
    rec = F['records'].get(str(n))
    folder = os.path.join('claims', f'{family}-n{n}')
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
    claim = {
        'problem': family, 'n': n, 'piece': F['piece'], 'container': F['container'], 'measure': F['measure'],
        's_full': s, 's': f'{math.floor(s * 1e5) / 1e5:.5f}+',
        'pieces': [[float(q[0]), float(q[1]), float(q[2])] for q in Q],
        'format': '[x, y, theta] per piece. Piece: regular k-gon with unit side (circle: diameter 1), vertex i at '
                  'R(cos a_i, sin a_i) with a_i = -pi/2 - pi/k + 2 pi i/k, rotated by theta about (x, y). '
                  'Container centred at the origin with size s (square: side; triangle: side, one side horizontal at the bottom; circle: radius).',
        'previous_record': rec['value'] if rec else None, 'previous_record_by': rec['finder'] if rec else None,
        'previous_record_truncated': rec.get('truncated') if rec else None,
        'improvement': (rec['value'] - s) if rec else None,
        'found_by': found_by, 'method': 'soft-to-rigid hardening + exact tightening (github.com/yoheinakajima/soft-to-rigid)',
        'source_run': pol['run'], 'date': time.strftime('%Y-%m-%d'),
        'clearance': {'pair_min': CLEAR, 'wall_min': CLEAR},
    }
    cp = os.path.join(ROOT, folder, 'claim.json')
    json.dump(claim, open(cp, 'w'), indent=1)
    v = subprocess.run([sys.executable, os.path.join(ROOT, 'verify.py'), cp], capture_output=True, text=True)
    open(os.path.join(ROOT, folder, 'verify.txt'), 'w').write(v.stdout + v.stderr)
    ok_c, why = certify(claim)
    open(os.path.join(ROOT, folder, 'certify.txt'), 'w').write(f"exact check: {why}\n{'CERTIFIED' if ok_c else 'NOT CERTIFIED'}\n")
    ok = v.returncode == 0 and ok_c and (rec is None or s < rec['value'])
    return {'ok': ok, 'family': family, 'n': n, 's_full': s, 'folder': folder,
            'reason': None if ok else f'verify rc={v.returncode}, certify={why}, s={s}, record={rec and rec["value"]}'}


def _make_claim3(F, family, n, pol, found_by):
    from .certify3 import certify as cert3
    s, Q = spread3(pol['poses'])
    rec = F['records'].get(str(n))
    folder = os.path.join('claims', f'{family}-n{n}')
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
    claim = {'problem': family, 'n': n, 'piece': 'cube', 'container': 'cube', 'measure': 'side', 's_full': s,
             's': f'{math.floor(s * 1e5) / 1e5:.5f}+', 'pieces': Q,
             'format': '[x, y, z, qw, qx, qy, qz] per piece; unit cube centred at (x, y, z) rotated by the unit quaternion q; container [0, s]^3',
             'previous_record': rec['value'] if rec else None, 'previous_record_by': rec['finder'] if rec else None,
             'improvement': (rec['value'] - s) if rec else None, 'found_by': found_by,
             'method': 'soft-to-rigid hardening + exact tightening (github.com/yoheinakajima/soft-to-rigid)',
             'source_run': pol['run'], 'date': time.strftime('%Y-%m-%d'), 'clearance': {'pair_min': CLEAR, 'wall_min': CLEAR}}
    cp = os.path.join(ROOT, folder, 'claim.json')
    json.dump(claim, open(cp, 'w'), indent=1)
    v = subprocess.run([sys.executable, os.path.join(ROOT, 'verify3.py'), cp], capture_output=True, text=True)
    open(os.path.join(ROOT, folder, 'verify.txt'), 'w').write(v.stdout + v.stderr)
    ok_c, why = cert3(claim)
    open(os.path.join(ROOT, folder, 'certify.txt'), 'w').write(f"exact check: {why}\n{'CERTIFIED' if ok_c else 'NOT CERTIFIED'}\n")
    ok = v.returncode == 0 and ok_c and (rec is None or s < rec['value'])
    return {'ok': ok, 'family': family, 'n': n, 's_full': s, 'folder': folder,
            'reason': None if ok else f'verify rc={v.returncode}, certify={why}, s={s}'}
