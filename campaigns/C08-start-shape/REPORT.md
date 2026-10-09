# C08-start-shape: How soft must the start be? A dose-response on the starting shape

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** With every other setting fixed at the shared best-of setting of harden and rigid (mu 0.16, noise x8), vary only how rounded the pieces start: tau0 = 1 (inscribed disk, harden), 0.5, 0.25 and 0 (rigid). Does the lowest point move monotonically with tau0, and does the answer depend on the family?

**Hypothesis.** On instances whose best known packing tilts pieces against each other (squares n = 11, 17-19, 26-29 in a square), softer starts reach lower sizes; on triangles and slack grids the reverse.

**Decision rule (pre-registered 2026-10-08).** Instances: the contested instances of C07, defined as those where the lowest sizes of harden-best and rigid-best differ by more than 1e-6 relative, capped at 40 by taking the largest relative differences. Metric: lowest tightened size over 32 runs per instance and tau0 (same tightening policy as C04). Report, per family, the number of instances where each tau0 attains the lowest size; test monotonicity descriptively (no significance test).

**Status.** closed — **decision:** Hypothesis supported for its two named cases (soft for squares in a square, rigid for triangles); no monotone rule across families. A half-rounded start is reported as a reasonable default when the family is unknown.

## Findings

- Starting softness on the 40 most contested instances of C07 (all other settings equal): tau0 = 1, 0.5, 0.25, 0 reach the lowest size on 7, 15, 18 and 17 instances. Squares in a square favour soft starts (3, 4, 2, 0); triangles favour rigid or slightly rounded ones (2, 7, 8, 10). Partly rounded starts (0.25-0.5) are never far from the best choice. The contested set leans to instances where rigid won in C07 (28 of 40), which favours small tau0.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 1, setting `tau0`

| instance | best known | harden-tau |
|---|---|---|
| hex-in-squ n=10 | 6.104690 | 1/32 · 1.8e-04 · 0.0298 |
| squ-in-cir n=5 | 1.581139 | ✓ 2/32 · 5.0e-07 · 0.0584 |
| squ-in-cir n=12 | 2.236068 | ✓ 3/32 · 2.3e-05 · 0.0987 |
| squ-in-cir n=17 | 2.676870 | 0/32 · 0.0013 · 0.0139 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0075 · 0.0479 |
| squ-in-cir n=20 | 2.893000 | 0/32 · 0.0051 · 0.0107 |
| squ-in-cir n=21 | 2.915476 | ✓ 4/32 · 8.6e-07 · 0.1125 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0107 · 0.0736 |
| squ-in-cir n=24 | 3.109400 | 1/32 · 5.5e-04 · 0.0906 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0258 · 0.0369 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0262 · 0.0925 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0069 · 0.0419 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0136 · 0.0902 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0196 · 0.0783 |
| squ-in-squ n=11 | 3.877084 | 0/32 · 0.0136 · 0.1229 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0316 · 0.0427 |
| squ-in-squ n=19 | 4.885618 | 0/32 · 0.1144 · 0.1144 |
| squ-in-squ n=27 | 5.707107 | 0/32 · 0.0607 · 0.2929 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.1026 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0662 · 0.0662 |
| squ-in-tri n=24 | 8.309401 | ✓ 10/32 · 4.6e-06 · 0.1547 |
| tri-in-squ n=9 | 2.287000 | ✓ 2/32 · 5.1e-04 · 0.0292 |
| tri-in-squ n=16 | 2.900000 | 2/32 · 7.3e-04 · 0.0729 |
| tri-in-squ n=18 | 3.051000 | ✓ 2/32 · 8.6e-04 · 0.0835 |
| tri-in-squ n=19 | 3.129290 | ✓ 0/32 · 0.0014 · 0.0965 |
| tri-in-squ n=22 | 3.375700 | 0/32 · 0.0039 · 0.0707 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0151 · 0.1071 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0067 · 0.0957 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0127 · 0.1440 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0062 · 0.1247 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0263 · 0.1104 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0228 · 0.0913 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0391 · 0.1277 |
| tri-in-tri n=12 | 3.879385 | ✓ 7/32 · 1.3e-05 · 0.0270 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0063 · 0.0080 |
| tri-in-tri n=21 | 4.923000 | ✓ 0/32 · 0.0024 · 0.0769 |
| tri-in-tri n=25 | 5.000000 | ✓ 3/32 · 6.2e-06 · 0.4501 |
| tri-in-tri n=26 | 5.406000 | 0/32 · 0.0226 · 0.0940 |
| tri-in-tri n=28 | 5.500000 | ✓ 2/32 · 5.9e-06 · 0.1667 |
| tri-in-tri n=30 | 5.750000 | ✓ 1/32 · 1.0e-05 · 0.1637 |

### budget 1, setting `tau0.25`

| instance | best known | harden-tau |
|---|---|---|
| hex-in-squ n=10 | 6.104690 | 2/32 · 1.8e-04 · 0.0297 |
| squ-in-cir n=5 | 1.581139 | 0/32 · 0.0567 · 0.0584 |
| squ-in-cir n=12 | 2.236068 | ✓ 1/32 · 2.3e-05 · 0.1005 |
| squ-in-cir n=17 | 2.676870 | 1/32 · 9.5e-04 · 0.0130 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0058 · 0.0538 |
| squ-in-cir n=20 | 2.893000 | ✓ 0/32 · 0.0012 · 0.0104 |
| squ-in-cir n=21 | 2.915476 | ✓ 2/32 · 8.4e-07 · 0.1176 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0079 · 0.0403 |
| squ-in-cir n=24 | 3.109400 | 1/32 · 7.7e-04 · 0.0895 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0230 · 0.0383 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0282 · 0.0522 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0261 · 0.0447 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0024 · 0.0427 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0145 · 0.0786 |
| squ-in-squ n=11 | 3.877084 | 0/32 · 0.0136 · 0.0951 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0047 · 0.0317 |
| squ-in-squ n=19 | 4.885618 | ✓ 0/32 · 0.0024 · 0.1144 |
| squ-in-squ n=27 | 5.707107 | 0/32 · 0.0220 · 0.1354 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.0569 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0524 · 0.0662 |
| squ-in-tri n=24 | 8.309401 | ✓ 6/32 · 4.4e-06 · 0.1547 |
| tri-in-squ n=9 | 2.287000 | ✓ 6/32 · 5.1e-04 · 0.0383 |
| tri-in-squ n=16 | 2.900000 | 3/32 · 7.2e-04 · 0.0833 |
| tri-in-squ n=18 | 3.051000 | ✓ 2/32 · 9.7e-04 · 0.0845 |
| tri-in-squ n=19 | 3.129290 | 0/32 · 0.0348 · 0.0870 |
| tri-in-squ n=22 | 3.375700 | 0/32 · 0.0034 · 0.0840 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0226 · 0.1081 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0187 · 0.1053 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0022 · 0.1625 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0398 · 0.1294 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0254 · 0.0967 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0084 · 0.1242 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0239 · 0.1434 |
| tri-in-tri n=12 | 3.879385 | ✓ 4/32 · 1.3e-05 · 0.0862 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0063 · 0.0080 |
| tri-in-tri n=21 | 4.923000 | 0/32 · 0.0321 · 0.0746 |
| tri-in-tri n=25 | 5.000000 | ✓ 1/32 · 5.8e-06 · 0.4899 |
| tri-in-tri n=26 | 5.406000 | 0/32 · 0.0227 · 0.0946 |
| tri-in-tri n=28 | 5.500000 | ✓ 1/32 · 6.2e-06 · 0.1828 |
| tri-in-tri n=30 | 5.750000 | 0/32 · 0.0834 · 0.2122 |

### budget 1, setting `tau0.5`

| instance | best known | harden-tau |
|---|---|---|
| hex-in-squ n=10 | 6.104690 | 0/32 · 0.0297 · 0.0298 |
| squ-in-cir n=5 | 1.581139 | 0/32 · 0.0567 · 0.0584 |
| squ-in-cir n=12 | 2.236068 | ✓ 1/32 · 2.3e-05 · 0.0999 |
| squ-in-cir n=17 | 2.676870 | 0/32 · 0.0019 · 0.0136 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0271 · 0.0585 |
| squ-in-cir n=20 | 2.893000 | 0/32 · 0.0011 · 0.0109 |
| squ-in-cir n=21 | 2.915476 | 0/32 · 0.0980 · 0.1178 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0045 · 0.0239 |
| squ-in-cir n=24 | 3.109400 | 1/32 · 7.5e-04 · 0.0948 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0138 · 0.0389 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0391 · 0.0874 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0090 · 0.0423 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0097 · 0.0442 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0228 · 0.0784 |
| squ-in-squ n=11 | 3.877084 | ✓ 1/32 · 7.1e-06 · 0.0137 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0076 · 0.0317 |
| squ-in-squ n=19 | 4.885618 | ✓ 1/32 · 3.2e-04 · 0.1144 |
| squ-in-squ n=27 | 5.707107 | 0/32 · 0.0643 · 0.1391 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.0096 · 0.1169 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0049 · 0.0662 |
| squ-in-tri n=24 | 8.309401 | ✓ 3/32 · 5.2e-06 · 0.1547 |
| tri-in-squ n=9 | 2.287000 | ✓ 1/32 · 5.1e-04 · 0.0383 |
| tri-in-squ n=16 | 2.900000 | ✓ 4/32 · 4.9e-04 · 0.1009 |
| tri-in-squ n=18 | 3.051000 | 0/32 · 0.0210 · 0.0981 |
| tri-in-squ n=19 | 3.129290 | 0/32 · 0.0149 · 0.1113 |
| tri-in-squ n=22 | 3.375700 | 0/32 · 0.0107 · 0.0775 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0082 · 0.1145 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0315 · 0.1391 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0127 · 0.1657 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0716 · 0.1547 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0386 · 0.1102 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0508 · 0.1126 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0400 · 0.1373 |
| tri-in-tri n=12 | 3.879385 | 0/32 · 0.0257 · 0.0944 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0061 · 0.0080 |
| tri-in-tri n=21 | 4.923000 | 0/32 · 0.0351 · 0.0770 |
| tri-in-tri n=25 | 5.000000 | ✓ 1/32 · 6.0e-06 · 0.4914 |
| tri-in-tri n=26 | 5.406000 | ✓ 1/32 · 8.9e-04 · 0.0948 |
| tri-in-tri n=28 | 5.500000 | 0/32 · 0.1594 · 0.2500 |
| tri-in-tri n=30 | 5.750000 | ✓ 1/32 · 1.0e-05 · 0.2328 |

### budget 1, setting `tau1`

| instance | best known | harden-tau |
|---|---|---|
| hex-in-squ n=10 | 6.104690 | 0/32 · 0.0297 · 0.0297 |
| squ-in-cir n=5 | 1.581139 | 0/32 · 0.0567 · 0.0584 |
| squ-in-cir n=12 | 2.236068 | 0/32 · 0.0910 · 0.1057 |
| squ-in-cir n=17 | 2.676870 | 0/32 · 0.0041 · 0.0164 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0408 · 0.0587 |
| squ-in-cir n=20 | 2.893000 | 0/32 · 0.0016 · 0.0104 |
| squ-in-cir n=21 | 2.915476 | 0/32 · 0.1121 · 0.1229 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0091 · 0.0279 |
| squ-in-cir n=24 | 3.109400 | 0/32 · 0.0110 · 0.0968 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0141 · 0.0391 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0265 · 0.0913 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0091 · 0.0451 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0044 · 0.0407 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0127 · 0.0790 |
| squ-in-squ n=11 | 3.877084 | ✓ 2/32 · 6.5e-06 · 0.0136 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0021 · 0.0317 |
| squ-in-squ n=19 | 4.885618 | ✓ 3/32 · 3.2e-04 · 0.0572 |
| squ-in-squ n=27 | 5.707107 | 0/32 · 0.0689 · 0.1233 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.0266 · 0.0793 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0186 · 0.0664 |
| squ-in-tri n=24 | 8.309401 | 0/32 · 0.1547 · 0.1547 |
| tri-in-squ n=9 | 2.287000 | 0/32 · 0.0252 · 0.0419 |
| tri-in-squ n=16 | 2.900000 | 0/32 · 0.0362 · 0.1141 |
| tri-in-squ n=18 | 3.051000 | 0/32 · 0.0210 · 0.1197 |
| tri-in-squ n=19 | 3.129290 | 0/32 · 0.0532 · 0.1207 |
| tri-in-squ n=22 | 3.375700 | ✓ 1/32 · 6.4e-04 · 0.0988 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0647 · 0.1603 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0318 · 0.1540 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0500 · 0.1945 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0656 · 0.1680 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0183 · 0.1076 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0649 · 0.1482 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0877 · 0.1537 |
| tri-in-tri n=12 | 3.879385 | 0/32 · 0.0356 · 0.1206 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0080 · 0.0080 |
| tri-in-tri n=21 | 4.923000 | 0/32 · 0.0357 · 0.0770 |
| tri-in-tri n=25 | 5.000000 | 0/32 · 0.3814 · 0.5009 |
| tri-in-tri n=26 | 5.406000 | 0/32 · 0.0328 · 0.1768 |
| tri-in-tri n=28 | 5.500000 | 0/32 · 0.1667 · 0.2978 |
| tri-in-tri n=30 | 5.750000 | 0/32 · 0.0500 · 0.2503 |

