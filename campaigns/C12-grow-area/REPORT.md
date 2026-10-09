# C12-grow-area: Is it the shape change or the area schedule?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Hardening also changes how much area each piece occupies over time. grow-area keeps pieces as rigid polygons but scales them so their area follows hardening's area schedule exactly, A(tau)/A = 1 - (1 - pi rho^2/A) tau^2, with the same settings, seeds and budget.

**Hypothesis.** On squares in a square, harden reaches lower sizes than grow-area (changing shape, not only size, matters).

**Decision rule (pre-registered 2026-10-09).** As C11, comparing harden with grow-area (and rigid, from C07).

**Status.** closed — **decision:** As C11's rule: squares in a square, instances solved by exactly one of harden and grow-area 2 vs 0 (p = 0.5), not separated by the pre-registered test; triangles in a triangle 0 vs 6 (p = 0.031) in grow-area's favour. Recorded together with the lower-size counts; the paper reports grow-area alongside snap as an ablation.

## Findings

- Grow-area (rigid polygons scaled so their area follows hardening's schedule) behaves like rigid starts: lower on 15 vs 14 instances, 159 ties. Hardening differs from it as from snap: squares in a square 5 vs 1, triangles in a triangle 1 vs 8, triangles in a square 5 vs 11. Neither the disk-compressed start (C11) nor the area schedule reproduces hardening's effect; the rounding of the pieces does.
- Correction (after review): grow-area shows no detectable difference from rigid starts (15 vs 14 lower); harden vs grow-area 20 vs 31 overall (p = 0.16), squares in a square 5 vs 1, triangles in a triangle 1 vs 8. Under C11's rule the squares-in-square test is inconclusive (2 vs 0). Neither ablation reproduces hardening's pattern, which makes rounding the likeliest explanation, but these experiments do not establish it.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

| instance | best known | grow-area-best |
|---|---|---|
| cir-in-squ n=2 | 1.707107 | ✓ 32/32 · 0 · 0 |
| cir-in-squ n=3 | 1.965926 | ✓ 0/32 · 0.0341 · 0.0341 |
| cir-in-squ n=4 | 2.000000 | ✓ 32/32 · 0 · 0 |
| cir-in-squ n=5 | 2.414214 | ✓ 25/32 · 0 · 0 |
| cir-in-squ n=6 | 2.664101 | ✓ 32/32 · 2.2e-06 · 2.2e-06 |
| cir-in-squ n=7 | 2.866025 | ✓ 32/32 · 5.4e-07 · 5.4e-07 |
| cir-in-squ n=8 | 2.931852 | ✓ 32/32 · 3.2e-07 · 3.2e-07 |
| cir-in-squ n=9 | 3.000000 | ✓ 32/32 · 0 · 0 |
| cir-in-squ n=10 | 3.373721 | 0/32 · 0.0064 · 0.0098 |
| cir-in-squ n=11 | 3.511255 | ✓ 32/32 · 3.0e-06 · 3.0e-06 |
| cir-in-squ n=12 | 3.572479 | ✓ 32/32 · 1.3e-06 · 1.3e-06 |
| cir-in-squ n=13 | 3.731524 | 28/32 · 4.3e-04 · 4.3e-04 |
| cir-in-squ n=14 | 3.866025 | 0/32 · 0.0067 · 0.0067 |
| cir-in-squ n=15 | 3.931852 | ✓ 32/32 · 8.0e-07 · 8.0e-07 |
| cir-in-squ n=16 | 4.000000 | ✓ 32/32 · 1.1e-08 · 1.1e-08 |
| cir-in-squ n=17 | 4.266330 | ✓ 30/32 · 3.9e-06 · 3.9e-06 |
| cir-in-squ n=18 | 4.328201 | ✓ 27/32 · 1.2e-06 · 1.2e-06 |
| cir-in-squ n=19 | 4.453730 | ✓ 26/32 · 6.9e-05 · 6.9e-05 |
| cir-in-squ n=20 | 4.489042 | ✓ 25/32 · 5.8e-06 · 5.8e-06 |
| cir-in-squ n=21 | 4.679010 | ✓ 20/32 · 8.9e-04 · 9.1e-04 |
| cir-in-squ n=22 | 4.731923 | 20/32 · 1.1e-04 · 1.3e-04 |
| cir-in-squ n=23 | 4.863703 | ✓ 2/32 · 1.1e-06 · 0.0847 |
| cir-in-squ n=24 | 4.931852 | ✓ 5/32 · 6.9e-07 · 0.0570 |
| cir-in-squ n=25 | 5.000000 | ✓ 28/32 · 1.9e-08 · 1.9e-08 |
| cir-in-squ n=26 | 5.188749 | 0/32 · 0.0022 · 0.0332 |
| cir-in-squ n=27 | 5.239992 | ✓ 0/32 · 0.0019 · 0.0571 |
| cir-in-squ n=28 | 5.337727 | ✓ 5/32 · 3.6e-04 · 0.0064 |
| cir-in-squ n=29 | 5.407560 | ✓ 1/32 · 1.0e-03 · 0.0015 |
| cir-in-squ n=30 | 5.454284 | ✓ 19/32 · 5.7e-06 · 5.7e-06 |
| hex-in-squ n=2 | 3.156597 | ✓ 32/32 · 6.5e-06 · 2.5e-05 |
| hex-in-squ n=3 | 3.491958 | ✓ 23/32 · 1.7e-06 · 1.8e-06 |
| hex-in-squ n=4 | 3.725003 | ✓ 25/32 · 8.4e-07 · 8.8e-07 |
| hex-in-squ n=6 | 4.813825 | ✓ 19/32 · 2.8e-06 · 3.1e-06 |
| hex-in-squ n=7 | 5.196152 | ✓ 32/32 · 8.9e-07 · 1.4e-06 |
| hex-in-squ n=8 | 5.196152 | ✓ 31/32 · 5.5e-07 · 9.6e-07 |
| hex-in-squ n=9 | 5.518154 | ✓ 24/32 · 1.3e-06 · 1.4e-06 |
| hex-in-squ n=10 | 6.104690 | 2/32 · 1.8e-04 · 0.0298 |
| hex-in-squ n=11 | 6.332180 | 0/32 · 0.0076 · 0.0076 |
| hex-in-squ n=12 | 6.387355 | ✓ 10/32 · 1.7e-06 · 0.0078 |
| hex-in-squ n=13 | 6.755490 | ✓ 14/32 · 2.2e-04 · 0.1727 |
| hex-in-squ n=14 | 6.928203 | ✓ 30/32 · 9.2e-07 · 1.5e-06 |
| hex-in-squ n=15 | 6.963670 | ✓ 32/32 · 3.4e-05 · 3.5e-05 |
| hex-in-squ n=16 | 7.311304 | ✓ 6/32 · 1.8e-06 · 0.0339 |
| hex-in-squ n=17 | 7.603830 | 0/32 · 0.0039 · 0.0224 |
| hex-in-squ n=18 | 7.702119 | ✓ 4/32 · 1.7e-06 · 0.0286 |
| hex-in-squ n=19 | 7.924682 | ✓ 12/32 · 2.9e-06 · 0.0103 |
| hex-in-squ n=20 | 7.948954 | ✓ 12/32 · 3.8e-06 · 0.0175 |
| squ-in-cir n=2 | 1.118034 | ✓ 32/32 · 1.8e-08 · 6.3e-08 |
| squ-in-cir n=3 | 1.288471 | ✓ 32/32 · 1.0e-07 · 1.6e-07 |
| squ-in-cir n=4 | 1.414214 | ✓ 32/32 · 1.4e-06 · 1.6e-06 |
| squ-in-cir n=5 | 1.581139 | 0/32 · 0.0567 · 0.0584 |
| squ-in-cir n=6 | 1.688000 | ✓ 16/32 · 5.4e-04 · 0.0064 |
| squ-in-cir n=7 | 1.802776 | ✓ 6/32 · 2.5e-07 · 0.0162 |
| squ-in-cir n=9 | 2.077596 | ✓ 26/32 · 1.1e-06 · 1.4e-06 |
| squ-in-cir n=10 | 2.121320 | ✓ 21/32 · 5.5e-07 · 8.3e-07 |
| squ-in-cir n=11 | 2.213860 | ✓ 9/32 · 2.3e-04 · 0.0019 |
| squ-in-cir n=12 | 2.236068 | ✓ 2/32 · 2.3e-05 · 0.1005 |
| squ-in-cir n=13 | 2.360700 | 11/32 · 2.8e-04 · 0.0065 |
| squ-in-cir n=14 | 2.500000 | 0/32 · 0.0050 · 0.0107 |
| squ-in-cir n=15 | 2.533000 | 0/32 · 0.0020 · 0.0083 |
| squ-in-cir n=16 | 2.623095 | 0/32 · 0.0091 · 0.0552 |
| squ-in-cir n=17 | 2.676870 | 0/32 · 0.0011 · 0.0156 |
| squ-in-cir n=18 | 2.741464 | ✓ 5/32 · 2.6e-06 · 0.0147 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0051 · 0.0496 |
| squ-in-cir n=20 | 2.893000 | ✓ 0/32 · 0.0021 · 0.0169 |
| squ-in-cir n=21 | 2.915476 | ✓ 1/32 · 1.1e-06 · 0.1161 |
| squ-in-cir n=22 | 3.032399 | 0/32 · 0.0032 · 0.0373 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0043 · 0.0886 |
| squ-in-cir n=24 | 3.109400 | 1/32 · 7.5e-04 · 0.0914 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0040 · 0.0372 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0306 · 0.0757 |
| squ-in-cir n=27 | 3.260500 | 0/32 · 0.0336 · 0.1105 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0111 · 0.0434 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0076 · 0.0686 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0127 · 0.0777 |
| squ-in-squ n=2 | 2.000000 | ✓ 32/32 · 3.4e-07 · 3.4e-07 |
| squ-in-squ n=3 | 2.000000 | ✓ 32/32 · 8.6e-07 · 1.4e-06 |
| squ-in-squ n=4 | 2.000000 | ✓ 32/32 · 8.4e-07 · 9.3e-07 |
| squ-in-squ n=5 | 2.707107 | ✓ 22/32 · 0 · 0 |
| squ-in-squ n=6 | 3.000000 | ✓ 32/32 · 6.7e-07 · 2.9e-06 |
| squ-in-squ n=7 | 3.000000 | ✓ 32/32 · 7.7e-07 · 2.5e-06 |
| squ-in-squ n=8 | 3.000000 | ✓ 32/32 · 8.6e-07 · 1.6e-06 |
| squ-in-squ n=9 | 3.000000 | ✓ 32/32 · 1.2e-06 · 1.4e-06 |
| squ-in-squ n=11 | 3.877084 | 0/32 · 0.0137 · 0.1229 |
| squ-in-squ n=12 | 4.000000 | ✓ 32/32 · 1.3e-06 · 3.8e-06 |
| squ-in-squ n=13 | 4.000000 | ✓ 32/32 · 2.1e-06 · 3.2e-06 |
| squ-in-squ n=14 | 4.000000 | ✓ 32/32 · 1.0e-06 · 2.4e-06 |
| squ-in-squ n=15 | 4.000000 | ✓ 32/32 · 1.2e-06 · 1.5e-06 |
| squ-in-squ n=16 | 4.000000 | ✓ 32/32 · 1.2e-06 · 1.4e-06 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0316 · 0.0923 |
| squ-in-squ n=18 | 4.822876 | ✓ 4/32 · 4.0e-05 · 0.1771 |
| squ-in-squ n=19 | 4.885618 | 0/32 · 0.0572 · 0.1144 |
| squ-in-squ n=20 | 5.000000 | ✓ 30/32 · 2.9e-06 · 6.0e-06 |
| squ-in-squ n=21 | 5.000000 | ✓ 31/32 · 2.4e-06 · 4.1e-06 |
| squ-in-squ n=22 | 5.000000 | ✓ 32/32 · 2.1e-06 · 3.0e-06 |
| squ-in-squ n=23 | 5.000000 | ✓ 32/32 · 9.4e-07 · 2.1e-06 |
| squ-in-squ n=24 | 5.000000 | ✓ 32/32 · 1.4e-06 · 1.7e-06 |
| squ-in-squ n=25 | 5.000000 | ✓ 32/32 · 1.2e-06 · 1.4e-06 |
| squ-in-squ n=26 | 5.621320 | ✓ 1/32 · 3.1e-04 · 0.1078 |
| squ-in-squ n=27 | 5.707107 | 0/32 · 0.1037 · 0.1639 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.0224 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0662 · 0.0662 |
| squ-in-squ n=30 | 6.000000 | ✓ 28/32 · 2.9e-06 · 6.3e-06 |
| squ-in-tri n=2 | 3.154701 | ✓ 32/32 · 1.7e-07 · 5.2e-07 |
| squ-in-tri n=3 | 3.232051 | ✓ 11/32 · 3.3e-06 · 0.0774 |
| squ-in-tri n=4 | 4.154701 | ✓ 32/32 · 1.6e-07 · 7.6e-07 |
| squ-in-tri n=5 | 4.309401 | ✓ 32/32 · 1.0e-06 · 1.8e-06 |
| squ-in-tri n=6 | 4.309401 | ✓ 30/32 · 2.7e-06 · 2.9e-06 |
| squ-in-tri n=7 | 5.154701 | ✓ 32/32 · 4.6e-07 · 1.7e-06 |
| squ-in-tri n=8 | 5.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=9 | 5.309401 | ✓ 18/32 · 3.7e-06 · 4.3e-06 |
| squ-in-tri n=10 | 5.464102 | ✓ 29/32 · 4.3e-06 · 4.9e-06 |
| squ-in-tri n=11 | 6.154701 | ✓ 28/32 · 1.2e-06 · 3.2e-06 |
| squ-in-tri n=12 | 6.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=13 | 6.309401 | ✓ 13/32 · 3.8e-06 · 0.1547 |
| squ-in-tri n=14 | 6.464102 | ✓ 26/32 · 6.3e-06 · 7.2e-06 |
| squ-in-tri n=15 | 6.464102 | ✓ 7/32 · 4.3e-06 · 0.1547 |
| squ-in-tri n=16 | 7.154701 | ✓ 29/32 · 2.8e-06 · 4.5e-06 |
| squ-in-tri n=17 | 7.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=18 | 7.309401 | ✓ 11/32 · 4.4e-06 · 0.1547 |
| squ-in-tri n=19 | 7.464102 | ✓ 17/32 · 7.1e-06 · 8.7e-06 |
| squ-in-tri n=20 | 7.616955 | 0/32 · 0.0019 · 0.0019 |
| squ-in-tri n=21 | 7.618802 | ✓ 16/32 · 6.4e-06 · 0.0194 |
| squ-in-tri n=22 | 8.154701 | ✓ 24/32 · 3.9e-06 · 6.9e-06 |
| squ-in-tri n=23 | 8.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=24 | 8.309401 | ✓ 8/32 · 4.6e-06 · 0.1547 |
| squ-in-tri n=25 | 8.464102 | ✓ 17/32 · 7.3e-06 · 1.0e-05 |
| squ-in-tri n=26 | 8.608050 | 0/32 · 0.0108 · 0.0108 |
| squ-in-tri n=27 | 8.618802 | ✓ 7/32 · 6.4e-06 · 0.1547 |
| squ-in-tri n=28 | 8.773503 | ✓ 24/32 · 7.7e-06 · 2.5e-05 |
| squ-in-tri n=29 | 9.154701 | ✓ 28/32 · 5.6e-06 · 9.8e-06 |
| squ-in-tri n=30 | 9.301000 | 0/32 · 0.0084 · 0.0084 |
| tri-in-squ n=2 | 1.224745 | ✓ 32/32 · 8.1e-08 · 4.1e-07 |
| tri-in-squ n=3 | 1.478398 | ✓ 32/32 · 1.2e-06 · 1.3e-06 |
| tri-in-squ n=4 | 1.577350 | ✓ 24/32 · 1.1e-06 · 1.1e-06 |
| tri-in-squ n=6 | 1.901924 | ✓ 9/32 · 2.7e-06 · 0.0180 |
| tri-in-squ n=7 | 2.000000 | ✓ 16/32 · 2.8e-06 · 0.0237 |
| tri-in-squ n=8 | 2.098076 | ✓ 12/32 · 1.4e-06 · 0.0573 |
| tri-in-squ n=9 | 2.287000 | ✓ 4/32 · 5.1e-04 · 0.0252 |
| tri-in-squ n=10 | 2.377000 | ✓ 11/32 · 2.6e-05 · 0.0240 |
| tri-in-squ n=11 | 2.490000 | 0/32 · 0.0013 · 0.0454 |
| tri-in-squ n=12 | 2.558000 | 0/32 · 0.0118 · 0.0360 |
| tri-in-squ n=13 | 2.595000 | ✓ 11/32 · 6.4e-04 · 0.0625 |
| tri-in-squ n=14 | 2.726000 | ✓ 5/32 · 2.0e-04 · 0.0707 |
| tri-in-squ n=15 | 2.829890 | ✓ 6/32 · 5.4e-05 · 0.0293 |
| tri-in-squ n=16 | 2.900000 | 1/32 · 8.9e-04 · 0.0686 |
| tri-in-squ n=17 | 2.982000 | ✓ 1/32 · 6.5e-04 · 0.0651 |
| tri-in-squ n=18 | 3.051000 | ✓ 1/32 · 9.8e-04 · 0.0629 |
| tri-in-squ n=19 | 3.129290 | ✓ 0/32 · 0.0014 · 0.0866 |
| tri-in-squ n=20 | 3.230500 | ✓ 0/32 · 0.0016 · 0.0555 |
| tri-in-squ n=21 | 3.311020 | 0/32 · 0.0082 · 0.0745 |
| tri-in-squ n=22 | 3.375700 | 0/32 · 0.0026 · 0.0587 |
| tri-in-squ n=23 | 3.431100 | 0/32 · 0.0119 · 0.0844 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0302 · 0.1074 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0367 · 0.1193 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0022 · 0.1354 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0270 · 0.1191 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0281 · 0.1070 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0158 · 0.1048 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0472 · 0.1167 |
| tri-in-tri n=2 | 2.000000 | ✓ 32/32 · 3.0e-06 · 3.0e-06 |
| tri-in-tri n=3 | 2.000000 | ✓ 32/32 · 2.3e-06 · 3.7e-06 |
| tri-in-tri n=4 | 2.000000 | ✓ 32/32 · 2.4e-06 · 2.5e-06 |
| tri-in-tri n=5 | 2.732051 | ✓ 32/32 · 1.0e-05 · 1.0e-05 |
| tri-in-tri n=7 | 3.000000 | ✓ 32/32 · 3.9e-06 · 5.2e-06 |
| tri-in-tri n=8 | 3.000000 | ✓ 31/32 · 3.3e-06 · 4.7e-06 |
| tri-in-tri n=9 | 3.000000 | ✓ 23/32 · 3.2e-06 · 3.5e-06 |
| tri-in-tri n=10 | 3.500000 | ✓ 29/32 · 3.5e-06 · 9.2e-06 |
| tri-in-tri n=11 | 3.722971 | ✓ 0/32 · 0.0050 · 0.0050 |
| tri-in-tri n=12 | 3.879385 | ✓ 6/32 · 1.3e-05 · 0.0864 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0061 · 0.0080 |
| tri-in-tri n=14 | 4.000000 | ✓ 32/32 · 4.9e-06 · 7.1e-06 |
| tri-in-tri n=15 | 4.000000 | ✓ 24/32 · 4.8e-06 · 6.2e-06 |
| tri-in-tri n=16 | 4.000000 | ✓ 15/32 · 4.5e-06 · 0.3660 |
| tri-in-tri n=17 | 4.465000 | 0/32 · 0.0350 · 0.0350 |
| tri-in-tri n=18 | 4.500000 | ✓ 22/32 · 5.6e-06 · 6.1e-06 |
| tri-in-tri n=19 | 4.666667 | ✓ 12/32 · 9.3e-06 · 0.1417 |
| tri-in-tri n=20 | 4.861485 | ✓ 0/32 · 0.0022 · 0.0625 |
| tri-in-tri n=21 | 4.923000 | ✓ 1/32 · 7.0e-04 · 0.0770 |
| tri-in-tri n=22 | 4.996000 | 0/32 · 0.0040 · 0.0040 |
| tri-in-tri n=23 | 5.000000 | ✓ 25/32 · 5.4e-06 · 7.8e-06 |
| tri-in-tri n=24 | 5.000000 | ✓ 8/32 · 5.9e-06 · 0.3212 |
| tri-in-tri n=25 | 5.000000 | ✓ 2/32 · 5.5e-06 · 0.4471 |
| tri-in-tri n=26 | 5.406000 | 0/32 · 0.0687 · 0.1631 |
| tri-in-tri n=27 | 5.500000 | ✓ 6/32 · 7.4e-06 · 0.1596 |
| tri-in-tri n=28 | 5.500000 | ✓ 3/32 · 5.3e-06 · 0.1683 |
| tri-in-tri n=29 | 5.666667 | ✓ 5/32 · 5.4e-06 · 0.1048 |
| tri-in-tri n=30 | 5.750000 | ✓ 3/32 · 1.0e-05 · 0.2160 |

