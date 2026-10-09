# C11-snap: Is it the path or the starting configuration?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Hardening differs from rigid starts in two ways: pieces are compressed as disks first, and they then harden gradually. snap compresses disks exactly as harden does and then switches to the full polygons at once, with the same settings, seeds and budget. Comparing harden, snap and rigid on all 188 instances separates the effect of the disk-compressed starting configuration from the effect of the gradual path.

**Hypothesis.** On squares in a square, harden reaches lower sizes than snap (the gradual path matters); on other families snap and rigid are similar.

**Decision rule (pre-registered 2026-10-09).** Same metric and tightening policy as C07. For each family, count instances where harden, snap and rigid (C07, same seeds and settings) attain the lowest of the three, and solved counts; report the two-sided exact sign test of harden vs snap over instances solved by exactly one. If harden and snap do not differ on squares in a square, the paper attributes hardening's advantage there to the disk-compressed start rather than to the path.

**Status.** closed — **decision:** Per the pre-registered rule (two-sided sign test over instances solved by exactly one of harden and snap): squares in a square 2 vs 0, p = 0.5, not separated, so the pre-registered conclusion attributes hardening's advantage there to the disk-compressed start. Recorded with the caveat that the rule has no power at two discordant instances, and that the descriptive evidence (snap = rigid; harden lower than snap 6-0 on squares, higher 0-8 on triangles in a triangle) points to the gradual path. The paper reports both.

## Findings

- Snap (disks compressed as in hardening, then polygons at once) behaves like rigid starts: lower on 20 instances each, 148 ties. Hardening differs from snap by family: lower on 6 squares-in-square instances against 0, while snap is lower on 8 triangles-in-triangle instances against 0 and 14 vs 6 triangles in a square. Over all 188 instances harden vs snap lower 17 vs 36 (two-sided p = 0.013). The gradual change of shape, not the disk-compressed start, carries hardening's effect in both directions.
- Correction (supersedes the wording of the C11 and C12 findings after an independent check): snap and grow-area show no detectable difference from rigid starts (20 vs 20 and 15 vs 14 instances lower); this is non-detection, not equivalence. Hardening differs from both in the same family-dependent directions (squares in a square in hardening's favour, triangles against), which suggests the gradual rounding is responsible, but the pre-registered tests on squares in a square are inconclusive (2 vs 0 solved-only discordant), so by the plans' rule the advantage there is attributed to the disk-compressed start. Treat the path explanation as post hoc.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

| instance | best known | snap-best |
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
| hex-in-squ n=2 | 3.156597 | ✓ 32/32 · 6.6e-06 · 2.7e-05 |
| hex-in-squ n=3 | 3.491958 | ✓ 23/32 · 1.7e-06 · 1.9e-06 |
| hex-in-squ n=4 | 3.725003 | ✓ 27/32 · 8.5e-07 · 8.9e-07 |
| hex-in-squ n=6 | 4.813825 | ✓ 16/32 · 2.8e-06 · 0.0050 |
| hex-in-squ n=7 | 5.196152 | ✓ 32/32 · 4.3e-07 · 1.2e-06 |
| hex-in-squ n=8 | 5.196152 | ✓ 31/32 · 6.0e-07 · 1.0e-06 |
| hex-in-squ n=9 | 5.518154 | ✓ 27/32 · 1.3e-06 · 1.4e-06 |
| hex-in-squ n=10 | 6.104690 | 0/32 · 0.0297 · 0.0298 |
| hex-in-squ n=11 | 6.332180 | 1/32 · 7.4e-04 · 0.0076 |
| hex-in-squ n=12 | 6.387355 | ✓ 10/32 · 1.8e-06 · 0.0078 |
| hex-in-squ n=13 | 6.755490 | ✓ 13/32 · 2.3e-04 · 0.1727 |
| hex-in-squ n=14 | 6.928203 | ✓ 30/32 · 8.7e-07 · 1.5e-06 |
| hex-in-squ n=15 | 6.963670 | ✓ 30/32 · 3.4e-05 · 3.5e-05 |
| hex-in-squ n=16 | 7.311304 | ✓ 11/32 · 1.8e-06 · 0.0339 |
| hex-in-squ n=17 | 7.603830 | 0/32 · 0.0039 · 0.0214 |
| hex-in-squ n=18 | 7.702119 | ✓ 4/32 · 1.7e-06 · 0.0200 |
| hex-in-squ n=19 | 7.924682 | ✓ 6/32 · 3.1e-06 · 0.0103 |
| hex-in-squ n=20 | 7.948954 | ✓ 12/32 · 5.1e-06 · 0.0175 |
| squ-in-cir n=2 | 1.118034 | ✓ 32/32 · 3.2e-08 · 4.1e-08 |
| squ-in-cir n=3 | 1.288471 | ✓ 32/32 · 1.3e-07 · 1.7e-07 |
| squ-in-cir n=4 | 1.414214 | ✓ 32/32 · 1.4e-06 · 1.5e-06 |
| squ-in-cir n=5 | 1.581139 | ✓ 1/32 · 4.9e-07 · 0.0584 |
| squ-in-cir n=6 | 1.688000 | ✓ 10/32 · 5.4e-04 · 0.0122 |
| squ-in-cir n=7 | 1.802776 | ✓ 14/32 · 2.2e-07 · 0.0162 |
| squ-in-cir n=9 | 2.077596 | ✓ 17/32 · 9.6e-07 · 1.9e-06 |
| squ-in-cir n=10 | 2.121320 | ✓ 24/32 · 5.8e-07 · 7.0e-07 |
| squ-in-cir n=11 | 2.213860 | ✓ 4/32 · 2.5e-04 · 0.0034 |
| squ-in-cir n=12 | 2.236068 | 0/32 · 0.0909 · 0.0995 |
| squ-in-cir n=13 | 2.360700 | ✓ 9/32 · 2.8e-04 · 0.0052 |
| squ-in-cir n=14 | 2.500000 | 0/32 · 0.0045 · 0.0098 |
| squ-in-cir n=15 | 2.533000 | ✓ 2/32 · 8.6e-04 · 0.0051 |
| squ-in-cir n=16 | 2.623095 | 0/32 · 0.0090 · 0.0559 |
| squ-in-cir n=17 | 2.676870 | 0/32 · 0.0015 · 0.0138 |
| squ-in-cir n=18 | 2.741464 | ✓ 4/32 · 5.4e-06 · 0.0162 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0094 · 0.0498 |
| squ-in-cir n=20 | 2.893000 | ✓ 0/32 · 0.0025 · 0.0159 |
| squ-in-cir n=21 | 2.915476 | ✓ 1/32 · 8.6e-07 · 0.1166 |
| squ-in-cir n=22 | 3.032399 | 0/32 · 0.0138 · 0.0462 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0094 · 0.0363 |
| squ-in-cir n=24 | 3.109400 | 0/32 · 0.0044 · 0.0872 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0206 · 0.0427 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0375 · 0.0950 |
| squ-in-cir n=27 | 3.260500 | 0/32 · 0.0329 · 0.1101 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0059 · 0.0449 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0040 · 0.0428 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0103 · 0.0785 |
| squ-in-squ n=2 | 2.000000 | ✓ 32/32 · 3.4e-07 · 3.4e-07 |
| squ-in-squ n=3 | 2.000000 | ✓ 32/32 · 8.4e-07 · 1.3e-06 |
| squ-in-squ n=4 | 2.000000 | ✓ 32/32 · 8.3e-07 · 9.6e-07 |
| squ-in-squ n=5 | 2.707107 | ✓ 20/32 · 0 · 0 |
| squ-in-squ n=6 | 3.000000 | ✓ 32/32 · 8.4e-07 · 3.0e-06 |
| squ-in-squ n=7 | 3.000000 | ✓ 32/32 · 1.3e-06 · 2.3e-06 |
| squ-in-squ n=8 | 3.000000 | ✓ 32/32 · 8.6e-07 · 1.5e-06 |
| squ-in-squ n=9 | 3.000000 | ✓ 32/32 · 1.2e-06 · 1.3e-06 |
| squ-in-squ n=11 | 3.877084 | 0/32 · 0.0136 · 0.1229 |
| squ-in-squ n=12 | 4.000000 | ✓ 31/32 · 1.4e-06 · 3.7e-06 |
| squ-in-squ n=13 | 4.000000 | ✓ 32/32 · 2.0e-06 · 3.5e-06 |
| squ-in-squ n=14 | 4.000000 | ✓ 32/32 · 1.1e-06 · 2.3e-06 |
| squ-in-squ n=15 | 4.000000 | ✓ 32/32 · 1.2e-06 · 1.6e-06 |
| squ-in-squ n=16 | 4.000000 | ✓ 32/32 · 1.3e-06 · 1.4e-06 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0316 · 0.0317 |
| squ-in-squ n=18 | 4.822876 | ✓ 5/32 · 6.1e-05 · 0.1771 |
| squ-in-squ n=19 | 4.885618 | 0/32 · 0.0176 · 0.1144 |
| squ-in-squ n=20 | 5.000000 | ✓ 31/32 · 2.3e-06 · 4.2e-06 |
| squ-in-squ n=21 | 5.000000 | ✓ 32/32 · 2.4e-06 · 3.9e-06 |
| squ-in-squ n=22 | 5.000000 | ✓ 32/32 · 1.9e-06 · 3.0e-06 |
| squ-in-squ n=23 | 5.000000 | ✓ 32/32 · 1.1e-06 · 2.3e-06 |
| squ-in-squ n=24 | 5.000000 | ✓ 32/32 · 1.3e-06 · 1.7e-06 |
| squ-in-squ n=25 | 5.000000 | ✓ 32/32 · 1.3e-06 · 1.4e-06 |
| squ-in-squ n=26 | 5.621320 | ✓ 2/32 · 2.9e-04 · 0.1078 |
| squ-in-squ n=27 | 5.707107 | 0/32 · 0.1164 · 0.2926 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.0706 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0662 · 0.0662 |
| squ-in-squ n=30 | 6.000000 | ✓ 27/32 · 2.6e-06 · 6.0e-06 |
| squ-in-tri n=2 | 3.154701 | ✓ 32/32 · 1.7e-07 · 4.8e-07 |
| squ-in-tri n=3 | 3.232051 | ✓ 15/32 · 3.3e-06 · 0.0774 |
| squ-in-tri n=4 | 4.154701 | ✓ 32/32 · 1.6e-07 · 5.8e-07 |
| squ-in-tri n=5 | 4.309401 | ✓ 32/32 · 1.0e-06 · 1.7e-06 |
| squ-in-tri n=6 | 4.309401 | ✓ 30/32 · 2.5e-06 · 2.8e-06 |
| squ-in-tri n=7 | 5.154701 | ✓ 31/32 · 6.8e-07 · 1.8e-06 |
| squ-in-tri n=8 | 5.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=9 | 5.309401 | ✓ 15/32 · 3.5e-06 · 0.1160 |
| squ-in-tri n=10 | 5.464102 | ✓ 29/32 · 4.1e-06 · 4.7e-06 |
| squ-in-tri n=11 | 6.154701 | ✓ 32/32 · 1.6e-06 · 3.4e-06 |
| squ-in-tri n=12 | 6.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=13 | 6.309401 | ✓ 17/32 · 3.9e-06 · 5.3e-06 |
| squ-in-tri n=14 | 6.464102 | ✓ 24/32 · 5.1e-06 · 7.1e-06 |
| squ-in-tri n=15 | 6.464102 | ✓ 10/32 · 4.1e-06 · 0.1547 |
| squ-in-tri n=16 | 7.154701 | ✓ 31/32 · 2.4e-06 · 4.3e-06 |
| squ-in-tri n=17 | 7.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=18 | 7.309401 | ✓ 4/32 · 4.4e-06 · 0.1547 |
| squ-in-tri n=19 | 7.464102 | ✓ 19/32 · 6.1e-06 · 8.0e-06 |
| squ-in-tri n=20 | 7.616955 | 0/32 · 0.0019 · 0.0019 |
| squ-in-tri n=21 | 7.618802 | ✓ 18/32 · 5.1e-06 · 9.1e-06 |
| squ-in-tri n=22 | 8.154701 | ✓ 32/32 · 3.8e-06 · 6.4e-06 |
| squ-in-tri n=23 | 8.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=24 | 8.309401 | ✓ 3/32 · 5.2e-06 · 0.1547 |
| squ-in-tri n=25 | 8.464102 | ✓ 18/32 · 6.9e-06 · 9.4e-06 |
| squ-in-tri n=26 | 8.608050 | 0/32 · 0.0108 · 0.0108 |
| squ-in-tri n=27 | 8.618802 | ✓ 1/32 · 1.0e-05 · 0.1547 |
| squ-in-tri n=28 | 8.773503 | ✓ 24/32 · 8.4e-06 · 2.5e-05 |
| squ-in-tri n=29 | 9.154701 | ✓ 31/32 · 3.2e-06 · 8.4e-06 |
| squ-in-tri n=30 | 9.301000 | 0/32 · 0.0084 · 0.0084 |
| tri-in-squ n=2 | 1.224745 | ✓ 32/32 · 1.6e-07 · 4.5e-07 |
| tri-in-squ n=3 | 1.478398 | ✓ 32/32 · 1.2e-06 · 1.3e-06 |
| tri-in-squ n=4 | 1.577350 | ✓ 28/32 · 1.1e-06 · 1.1e-06 |
| tri-in-squ n=6 | 1.901924 | 0/32 · 0.0175 · 0.0181 |
| tri-in-squ n=7 | 2.000000 | ✓ 17/32 · 2.7e-06 · 3.0e-06 |
| tri-in-squ n=8 | 2.098076 | ✓ 12/32 · 1.2e-06 · 0.0621 |
| tri-in-squ n=9 | 2.287000 | ✓ 2/32 · 5.1e-04 · 0.0292 |
| tri-in-squ n=10 | 2.377000 | ✓ 11/32 · 2.6e-05 · 0.0210 |
| tri-in-squ n=11 | 2.490000 | 0/32 · 0.0100 · 0.0420 |
| tri-in-squ n=12 | 2.558000 | 0/32 · 0.0104 · 0.0268 |
| tri-in-squ n=13 | 2.595000 | ✓ 9/32 · 6.4e-04 · 0.0650 |
| tri-in-squ n=14 | 2.726000 | ✓ 3/32 · 2.0e-04 · 0.0599 |
| tri-in-squ n=15 | 2.829890 | ✓ 7/32 · 6.1e-05 · 0.0324 |
| tri-in-squ n=16 | 2.900000 | ✓ 3/32 · 5.3e-04 · 0.0546 |
| tri-in-squ n=17 | 2.982000 | ✓ 2/32 · 6.5e-04 · 0.0579 |
| tri-in-squ n=18 | 3.051000 | ✓ 1/32 · 8.5e-04 · 0.0755 |
| tri-in-squ n=19 | 3.129290 | 0/32 · 0.0341 · 0.1026 |
| tri-in-squ n=20 | 3.230500 | 0/32 · 0.0074 · 0.0625 |
| tri-in-squ n=21 | 3.311020 | ✓ 0/32 · 0.0026 · 0.0527 |
| tri-in-squ n=22 | 3.375700 | 0/32 · 0.0026 · 0.0628 |
| tri-in-squ n=23 | 3.431100 | 0/32 · 0.0127 · 0.0699 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0194 · 0.1063 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0020 · 0.1197 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0414 · 0.1381 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0411 · 0.1169 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0320 · 0.1114 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0157 · 0.1087 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0214 · 0.1212 |
| tri-in-tri n=2 | 2.000000 | ✓ 32/32 · 3.0e-06 · 3.0e-06 |
| tri-in-tri n=3 | 2.000000 | ✓ 32/32 · 2.3e-06 · 3.7e-06 |
| tri-in-tri n=4 | 2.000000 | ✓ 30/32 · 2.4e-06 · 2.6e-06 |
| tri-in-tri n=5 | 2.732051 | ✓ 32/32 · 1.0e-05 · 1.0e-05 |
| tri-in-tri n=7 | 3.000000 | ✓ 32/32 · 3.9e-06 · 5.4e-06 |
| tri-in-tri n=8 | 3.000000 | ✓ 30/32 · 3.3e-06 · 4.6e-06 |
| tri-in-tri n=9 | 3.000000 | ✓ 10/32 · 3.2e-06 · 0.4574 |
| tri-in-tri n=10 | 3.500000 | ✓ 30/32 · 3.4e-06 · 9.2e-06 |
| tri-in-tri n=11 | 3.722971 | ✓ 0/32 · 0.0050 · 0.0050 |
| tri-in-tri n=12 | 3.879385 | ✓ 4/32 · 1.3e-05 · 0.0868 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0062 · 0.0080 |
| tri-in-tri n=14 | 4.000000 | ✓ 32/32 · 4.9e-06 · 6.9e-06 |
| tri-in-tri n=15 | 4.000000 | ✓ 24/32 · 4.6e-06 · 5.9e-06 |
| tri-in-tri n=16 | 4.000000 | ✓ 12/32 · 4.5e-06 · 0.4128 |
| tri-in-tri n=17 | 4.465000 | 0/32 · 0.0350 · 0.0350 |
| tri-in-tri n=18 | 4.500000 | ✓ 10/32 · 5.1e-06 · 0.1503 |
| tri-in-tri n=19 | 4.666667 | ✓ 5/32 · 9.4e-06 · 0.1209 |
| tri-in-tri n=20 | 4.861485 | ✓ 0/32 · 0.0019 · 0.0262 |
| tri-in-tri n=21 | 4.923000 | ✓ 1/32 · 7.0e-04 · 0.0764 |
| tri-in-tri n=22 | 4.996000 | 0/32 · 0.0040 · 0.0040 |
| tri-in-tri n=23 | 5.000000 | ✓ 28/32 · 4.8e-06 · 7.9e-06 |
| tri-in-tri n=24 | 5.000000 | ✓ 9/32 · 5.7e-06 · 0.3276 |
| tri-in-tri n=25 | 5.000000 | ✓ 5/32 · 5.7e-06 · 0.4349 |
| tri-in-tri n=26 | 5.406000 | 0/32 · 0.0317 · 0.0941 |
| tri-in-tri n=27 | 5.500000 | ✓ 10/32 · 8.4e-06 · 0.1498 |
| tri-in-tri n=28 | 5.500000 | ✓ 2/32 · 6.5e-06 · 0.2175 |
| tri-in-tri n=29 | 5.666667 | ✓ 6/32 · 5.2e-06 · 0.1769 |
| tri-in-tri n=30 | 5.750000 | ✓ 1/32 · 1.0e-05 · 0.1948 |

