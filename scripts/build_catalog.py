"""Build catalog/<family>.json from the best-known values below.

Every value was copied from the caption text of Erich Friedman's Packing Center pages
(source repo github.com/erich-friedman/erich-friedman.github.io, commit of 2026-10-07),
from the Squares Project witnesses (github.com/jlevy/squares), from Packomania (csq), or
from Hyra-results. Truncated values (Friedman's "+") are stored as their decimal with
"truncated": true; closed forms are evaluated in full precision.
Run: python3 scripts/build_catalog.py
"""
import json, math, os
r2, r3, r5 = math.sqrt(2), math.sqrt(3), math.sqrt(5)
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalog')
FR = 'https://erich-friedman.github.io/packing/'

class TF(float):
    """a truncated catalogue value, remembering how many decimals were printed"""
    dec = None


def rec(v, who, trunc=False, coords=None, expr=None):
    d = {'value': float(v), 'finder': who, 'truncated': trunc}
    if trunc:
        dec = getattr(v, 'dec', None)
        d['decimals'] = dec
        d['tol'] = 10.0 ** -dec if dec else 1e-5
    if coords: d['coords'] = coords
    if expr: d['expr'] = expr
    return d

def T(s):  # truncated decimal string, e.g. '2.9000' -> value 2.9 with 4 printed decimals
    x = TF(s); x.dec = len(s.split('.')[1]); return x

fams = {}

# ---------- squares in square (side s), Squares Project witnesses ----------
sq = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2 + r2 / 2, 6: 3, 7: 3, 8: 3, 9: 3, 10: 3 + r2 / 2, 11: 3.87708359002281,
      12: 4, 13: 4, 14: 4, 15: 4, 16: 4, 17: 4.67553009360455, 18: 3.5 + math.sqrt(7) / 2, 19: 3 + 4 * r2 / 3,
      20: 5, 21: 5, 22: 5, 23: 5, 24: 5, 25: 5, 26: 3.5 + 1.5 * r2, 27: 5 + r2 / 2, 28: 5.82444461667405,
      29: 5.93383346267692, 30: 6}
who = {5: 'Göbel 1979', 10: 'Göbel 1979', 11: 'Trump 1979', 17: 'Bidwell 1998', 18: 'Hämäläinen 1980',
       19: 'Wainwright 1979', 26: 'Friedman 1997', 27: 'Göbel 1979', 28: 'Ellsworth 2025', 29: 'Schadt 2025'}
fams['squ-in-squ'] = dict(
    title='Unit squares in a square', dim=2, piece='square', container='square', measure='side',
    sources=['https://jlevy.github.io/squares/', 'https://kingbird.myphotos.cc/packing/squares_in_squares.html'],
    records={n: rec(v, who.get(n, 'trivial or classical'), coords='squares-project') for n, v in sq.items()})

# ---------- squares in circle (radius r), Friedman squincir ----------
sc = {1: (1 / r2, 'Trivial'), 2: (r5 / 2, 'Trivial'), 3: (5 * math.sqrt(17) / 16, 'Vu-Le 2026 (proved)'),
      4: (r2, 'proved 2026'), 5: (math.sqrt(10) / 2, 'Vu-Le 2026 (proved)'), 6: (T('1.688'), 'Ellsworth 2023, proved Vu-Le 2026', True),
      7: (math.sqrt(13) / 2, 'Vu-Le 2026 (proved)'), 8: (T('1.97877'), 'Cantrell 2002', True), 9: (math.sqrt(1105) / 16, 'Friedman 1997'),
      10: (3 / r2, 'Friedman 1997'), 11: (T('2.21386'), 'Kovacic 2006', True), 12: (r5, 'Friedman 1997'),
      13: (T('2.3607'), 'Cantrell 2010', True), 14: (2.5, 'Friedman 1997'), 15: (T('2.533'), 'Cantrell 2002', True),
      16: (math.sqrt(11009) / 40, 'Friedman 1997'), 17: (T('2.67687'), 'Kovacic 2026', True), 18: (math.sqrt(481) / 8, 'Cantrell 2002'),
      19: (T('2.80150'), 'Kovacic 2026', True), 20: (T('2.893'), 'Cantrell 2002', True), 21: (math.sqrt(34) / 2, 'Friedman 1997'),
      22: (3.032399268543576, 'H. Lin 2026 (Hyra)'), 23: (T('3.06738'), 'Kovacic 2026', True), 24: (T('3.10940'), 'Kovacic 2026', True),
      25: (3.174503223133547, 'H. Lin 2026 (Hyra)'), 26: (math.sqrt(41) / 2, 'Friedman 1997'), 27: (T('3.26050'), 'Kovacic 2026', True),
      28: (T('3.33147'), 'Kovacic 2026', True), 29: (T('3.39309'), 'Kovacic 2026', True), 30: (T('3.45962'), 'Kovacic 2026', True)}
fams['squ-in-cir'] = dict(title='Unit squares in a circle', dim=2, piece='square', container='circle', measure='radius',
    sources=[FR + 'squincir/'], records={n: rec(v[0], v[1], len(v) > 2) for n, v in sc.items()})

# ---------- triangles in triangle (side s), Friedman triintri ----------
tt = {1: 1, 2: 2, 3: 2, 4: 2, 5: 1 + r3, 6: 13 / 8 + 3 * math.sqrt(13) / 8, 7: 3, 8: 3, 9: 3, 10: 3.5,
      11: 9 / 4 + 9 * math.sqrt(21) / 28, 12: 2 + 2 * math.cos(math.pi / 9), 13: T('3.992'), 14: 4, 15: 4, 16: 4,
      17: T('4.465'), 18: 4.5, 19: 14 / 3, 20: 33 / 8 + 9 * math.sqrt(21) / 56, 21: T('4.923'), 22: T('4.996'),
      23: 5, 24: 5, 25: 5, 26: T('5.406'), 27: 5.5, 28: 5.5, 29: 17 / 3, 30: 23 / 4}
twho = {5: 'Friedman 1997 (proved)', 6: 'Morandi 2008', 10: 'Friedman 1997', 11: 'Friedman 1997', 12: 'Cantrell 2007',
        13: 'Morandi 2008', 17: 'Morandi 2008', 18: 'Friedman 1997', 19: 'Morandi 2008', 20: 'Morandi 2008', 21: 'Morandi 2008',
        22: 'Morandi 2008', 26: 'Frenzley 2026', 27: 'Friedman 1997', 28: 'Friedman 1997', 29: 'Cantrell 2007', 30: 'Morandi 2008'}
fams['tri-in-tri'] = dict(title='Unit equilateral triangles in an equilateral triangle', dim=2, piece='triangle', container='triangle',
    measure='side', sources=[FR + 'triintri/'],
    records={n: rec(v, twho.get(n, 'Trivial'), n in (13, 17, 21, 22, 26)) for n, v in tt.items()})

# ---------- triangles in square (side s), Friedman triinsqu ----------
ts = {1: ((r2 + math.sqrt(6)) / 4, 'Trivial'), 2: (math.sqrt(6) / 2, 'Trivial'), 3: (r3 / 2 + math.sqrt(6) / 4, 'Friedman 1996'),
      4: (1 + 1 / r3, 'Friedman 1996'), 5: (T('1.803'), 'Friedman 1996', True), 6: (4.5 - 1.5 * r3, 'Friedman 1996'),
      7: (2, 'Friedman 1996'), 8: (1.5 * r3 - 0.5, 'Friedman 1996'), 9: (T('2.287'), 'Morandi 2008', True),
      10: (T('2.377'), 'Cantrell 2002', True), 11: (T('2.490'), 'Morandi 2008', True), 12: (T('2.558'), 'Kamp 2026', True),
      13: (T('2.595'), 'Cantrell 2002', True), 14: (T('2.726'), 'Cantrell 2002', True), 15: (T('2.82989'), 'Loyd 2026', True),
      16: (T('2.9000'), 'Watson 2026', True), 17: (T('2.982'), 'Morandi 2008', True), 18: (T('3.051'), 'Morandi 2008', True),
      19: (T('3.12929'), 'Loyd 2026', True), 20: (T('3.2305'), 'Watson 2026', True), 21: (T('3.31102'), 'Schadt 2026', True),
      22: (T('3.3757'), 'Watson 2026', True), 23: (T('3.4311'), 'Watson 2026', True), 24: (T('3.46780'), 'Schadt 2026', True),
      25: (T('3.537'), 'Cantrell 2012', True), 26: (T('3.575'), 'Morandi 2008', True), 27: (T('3.6726'), 'Watson 2026', True),
      28: (T('3.75707'), 'Loyd 2026', True), 29: (T('3.81711'), 'Loyd 2026', True), 30: (T('3.86619'), 'Loyd 2026', True)}
fams['tri-in-squ'] = dict(title='Unit equilateral triangles in a square', dim=2, piece='triangle', container='square', measure='side',
    sources=[FR + 'triinsqu/'], records={n: rec(v[0], v[1], len(v) > 2) for n, v in ts.items()})

# ---------- squares in triangle (side s), Friedman squintri ----------
st = {1: 1 + 2 / r3, 2: 2 + 2 / r3, 3: 1.5 + r3, 4: 3 + 2 / r3, 5: 2 + 4 / r3, 6: 2 + 4 / r3, 7: 4 + 2 / r3, 8: T('5.301'),
      9: 3 + 4 / r3, 10: 2 + 2 * r3, 11: 5 + 2 / r3, 12: T('6.301'), 13: 4 + 4 / r3, 14: 3 + 2 * r3, 15: 3 + 2 * r3,
      16: 6 + 2 / r3, 17: T('7.301'), 18: 5 + 4 / r3, 19: 4 + 2 * r3, 20: 7.616954722204242, 21: 3 + 8 / r3,
      22: 7 + 2 / r3, 23: T('8.301'), 24: 6 + 4 / r3, 25: 5 + 2 * r3, 26: T('8.60805'), 27: 4 + 8 / r3, 28: 3 + 10 / r3,
      29: 8 + 2 / r3, 30: T('9.301')}
swho = {8: 'Cantrell 2002', 12: 'Cantrell 2002', 17: 'Cantrell 2002', 20: 'H. Lin 2026 (Hyra)', 23: 'Cantrell 2002',
        26: 'Wolk 2026', 30: 'Cantrell 2002'}
fams['squ-in-tri'] = dict(title='Unit squares in an equilateral triangle', dim=2, piece='square', container='triangle', measure='side',
    sources=[FR + 'squintri/'],
    records={n: rec(v, swho.get(n, 'Trivial' if n <= 2 else 'Friedman 1997'), n in (8, 12, 17, 23, 26, 30)) for n, v in st.items()})

# ---------- hexagons (side 1) in square, Friedman hexinsqu ----------
hs = {1: ((1 + r3) / r2, 'Trivial'), 2: ((1 + 2 * r3) / r2, 'Trivial'), 3: (9 * (6 - r3) / 11, 'Morandi 2026'),
      4: ((7 - r3) / r2, 'Morandi 2026'), 5: (3.5 * (3 - r3), 'Morandi 2026'), 6: (20 * (9 - 2 * r3) / 23, 'Morandi 2026'),
      7: (3 * r3, 'Trivial'), 8: (3 * r3, 'Trivial'), 9: ((13 - 3 * r3) / r2, 'Morandi 2026'), 10: (T('6.10469'), 'Viquerat 2026', True),
      11: (T('6.33218'), 'Jankowski 2026', True), 12: (43 * (5 - r3) / 22, 'Morandi 2026'), 13: (T('6.75549'), 'Berthold et al. 2026', True),
      14: (4 * r3, 'Trivial'), 15: (T('6.96367'), 'Jankowski 2026', True), 16: ((19 - 5 * r3) / r2, 'Morandi 2026'),
      17: (T('7.60383'), 'Jankowski 2026', True), 18: (32 * (9 - 2 * r3) / 23, 'Morandi 2026'), 19: (25 * (3 - r3) / 4, 'Morandi 2026'),
      20: (74 * (21 - 4 * r3) / 131, 'Morandi 2026')}
fams['hex-in-squ'] = dict(title='Unit regular hexagons in a square', dim=2, piece='hexagon', container='square', measure='side',
    sources=[FR + 'hexinsqu/'], records={n: rec(v[0], v[1], len(v) > 2) for n, v in hs.items()})

# ---------- circles (diameter 1) in square: control. Packomania radius r in unit square -> side 1/(2r) ----------
cr = [0.5, 0.292893218813, 0.254333095030, 0.25, 0.207106781187, 0.187680601147, 0.174457630187, 0.170540688701,
      0.166666666667, 0.148204322565, 0.142399237696, 0.139958844038, 0.133993513499, 0.129331793710, 0.127166547515,
      0.125, 0.117196742783, 0.115521432464, 0.112265437571, 0.111382347512, 0.106860212352, 0.105665296757,
      0.102802323380, 0.101381800432, 0.1, 0.096362339010, 0.095420001748, 0.093672833833, 0.092463144040, 0.091671057986]
fams['cir-in-squ'] = dict(title='Unit-diameter circles in a square (control: no orientation)', dim=2, piece='circle',
    container='square', measure='side', sources=['http://www.packomania.com/csq/csq.html'],
    records={i + 1: rec(1 / (2 * r), 'Packomania (csq)', coords='packomania') for i, r in enumerate(cr)})

# ---------- cubes in cube (side s), Friedman cubincub ----------
cc = {n: (math.ceil(n ** (1 / 3) - 1e-9), 'Trivial') for n in range(1, 34)}
cc.update({9: (2 + 1 / r2, 'Friedman 1998'), 10: (2 + 1 / r2, 'Friedman 1998'), 11: (2.8829529104956513, 'H. Lin 2026 (Hyra)'),
           12: (2.9327717687048653, 'H. Lin 2026 (Hyra)'), 13: (T('2.956'), 'Friedman 1998', True), 14: (2 + 7 * r2 / 10, 'Friedman 1998')})
for n in range(28, 34): cc[n] = (3 + 1 / r2, 'Friedman 1998')
fams['cub-in-cub'] = dict(title='Unit cubes in a cube', dim=3, piece='cube', container='cube', measure='side',
    sources=[FR + 'cubincub/', 'https://github.com/Tencent-Hunyuan/Hyra-results'],
    records={n: rec(v[0], v[1], len(v) > 2) for n, v in cc.items()},
    note='Our n = 12 packing (2.9315185094797, 8 Oct 2026, github.com/yoheinakajima/soft-to-rigid-packing) is the input to this study, not a catalogue entry.')

# ---------- held-out tuning instances above n = 30 (used only by C06-tune-best) ----------
# squares in square: Squares Project witnesses n-031/037/038; others: Friedman captions (source repo commit of 2026-10-07)
fams['squ-in-squ']['records'].update({31: rec(6, 'trivial'), 37: rec(6.59861960924436011617837046268, 'Squares Project witness', coords='squares-project'),
                                       38: rec(6 + r2 / 2, 'Squares Project witness', coords='squares-project')})
fams['squ-in-cir']['records'].update({31: rec(T('3.52279'), 'D. Lu 2026', True), 33: rec(3.6001082, 'H. Lin 2026 (Hyra; Friedman lists 3.60010+)')})
fams['tri-in-squ']['records'].update({31: rec(T('3.93107'), 'Loyd 2026', True), 32: rec(T('3.97880'), 'Loyd 2026', True)})
fams['tri-in-tri']['records'].update({31: rec(T('5.90751'), 'Gomes 2026', True)})

os.makedirs(OUT, exist_ok=True)
for k, f in fams.items():
    f['family'] = k
    f['records'] = {str(n): r for n, r in sorted(f['records'].items())}
    json.dump(f, open(os.path.join(OUT, k + '.json'), 'w'), indent=1)
    print(k, len(f['records']))
