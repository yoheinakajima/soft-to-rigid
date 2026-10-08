# C03-tune-extend2: Second and last grid extension for methods whose winner is still on an edge

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** After C01 and C02, the winners for harden (noise x8), sa (T0 = 3e-3) and pc (relax 4800) are on the outer edge of their grids. Grow and rigid winners are interior. Extend once more, as the C02 decision rule requires, then freeze all five methods.

**Hypothesis.** None (calibration).

**Decision rule (pre-registered 2026-10-08).** Same scoring rule as C01 over C01 + C02 + C03. Freeze the winner of each method into methods/<method>.json regardless of edges.

**Status.** closed — **decision:** Frozen into methods/*.json (scripts/score_tuning.py over C01-C03): harden mu 0.08, noise x8; grow mu 0.04, gamma0 0.2; rigid mu 0.04, noise x2; sa T0 3e-3, mu 0.0025; pc kick 0.05, relax 19200. Repeated settings across campaigns reproduce bit-for-bit (same seeds, same results).

## Findings

- Tuning changes the comparison. With equal tuning effort on five small instances (n = 5 to 10), tuned rigid starts have the lowest median gap (0.27% of the best known size), ahead of harden (0.40%), sa (1.0%), grow (1.5%) and pc (5.4%). The earlier advantage of hardening over rigid starts (C00, n = 11) was measured against an untuned rigid control. Both gradient methods prefer much stronger noise than the original schedule (harden x8, rigid x2). harden never reached the n = 6 triangles-in-triangle record in 16 runs at any setting, while rigid and grow did.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 1, setting `T0.003_mu0.00125`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 2/16 · 5.5e-04 · 0.0078 |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0064 · 0.0157 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0440 · 0.3156 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0145 · 0.0326 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0109 · 0.0249 |  |

### budget 1, setting `T0.003_mu0.0025`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 5/16 · 9.1e-05 · 0.0047 |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0040 · 0.0126 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0115 · 0.0575 |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 7.0e-04 · 0.0355 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0154 · 0.0247 |  |

### budget 1, setting `T0.003_mu0.005`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 4/16 · 3.1e-04 · 0.1837 |  |
| squ-in-cir n=8 | 1.978770 |  | 1/16 · 5.1e-04 · 0.0071 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0012 · 0.0680 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0012 · 0.0212 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0078 · 0.0281 |  |

### budget 1, setting `T0.01_mu0.00125`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 1/16 · 3.6e-04 · 0.1903 |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0049 · 0.0155 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0135 · 0.2161 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0056 · 0.0371 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0174 · 0.0264 |  |

### budget 1, setting `T0.01_mu0.0025`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 6/16 · 3.4e-05 · 0.0023 |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0014 · 0.0120 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0433 · 0.3030 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0049 · 0.0270 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0157 · 0.0248 |  |

### budget 1, setting `T0.01_mu0.005`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 4/16 · 4.2e-04 · 0.1109 |  |
| squ-in-cir n=8 | 1.978770 |  | 3/16 · 6.3e-04 · 0.0051 |  |
| squ-in-squ n=10 | 3.707107 |  | 1/16 · 6.6e-04 · 0.3021 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0050 · 0.0350 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0206 · 0.0320 |  |

### budget 1, setting `T0.03_mu0.00125`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 6/16 · 1.9e-04 · 0.0202 |  |
| squ-in-cir n=8 | 1.978770 |  | 1/16 · 5.9e-04 · 0.0220 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0290 · 0.1857 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0443 · 0.0556 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0259 · 0.0434 |  |

### budget 1, setting `T0.03_mu0.0025`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 8/16 · 6.7e-05 · 0.0016 |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0016 · 0.0141 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0067 · 0.2988 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0050 · 0.0526 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0213 · 0.0405 |  |

### budget 1, setting `T0.03_mu0.005`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 8/16 · 3.6e-04 · 0.0016 |  |
| squ-in-cir n=8 | 1.978770 |  | 1/16 · 5.2e-04 · 0.0062 |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0084 · 0.3031 |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0084 · 0.0582 |  |
| tri-in-tri n=6 | 2.977082 |  | 0/16 · 0.0261 · 0.0444 |  |

### budget 1, setting `kick0.05_relax19200`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2288 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1085 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0267 · 0.1021 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0688 |

### budget 1, setting `kick0.05_relax4800`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2526 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0084 · 0.0994 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.05_relax9600`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2288 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1085 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0267 · 0.1021 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0688 |

### budget 1, setting `kick0.15_relax19200`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2288 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1085 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0267 · 0.1021 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0688 |

### budget 1, setting `kick0.15_relax4800`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2526 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0084 · 0.0994 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.15_relax9600`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2288 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1085 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0267 · 0.1021 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0688 |

### budget 1, setting `kick0.4_relax19200`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2288 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1085 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0267 · 0.1021 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0688 |

### budget 1, setting `kick0.4_relax4800`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2526 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0084 · 0.0994 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.4_relax9600`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  | 0/16 · 0.0440 · 0.2288 |
| squ-in-cir n=8 | 1.978770 |  |  | 0/16 · 0.0056 · 0.1085 |
| squ-in-squ n=10 | 3.707107 |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  | 0/16 · 0.0267 · 0.1021 |
| tri-in-tri n=6 | 2.977082 |  |  | 0/16 · 0.0079 · 0.0688 |

### budget 1, setting `mu0.04_nz16`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 6/16 · 2.9e-07 · 0.1100 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0029 · 0.0137 |  |  |
| squ-in-squ n=10 | 3.707107 | 2/16 · 4.3e-05 · 0.0655 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 4.4e-04 · 0.0334 |  |  |
| tri-in-tri n=6 | 2.977082 | 1/16 · 9.6e-05 · 0.0229 |  |  |

### budget 1, setting `mu0.04_nz32`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 1/16 · 2.9e-07 · 0.8646 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 2.4944 · 7.0899 |  |  |
| squ-in-squ n=10 | 3.707107 | 0/16 · 4.7525 · 11.1744 |  |  |
| tri-in-squ n=5 | 1.803000 | 0/16 · 0.0476 · 1.5863 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 2.6782 |  |  |

### budget 1, setting `mu0.04_nz8`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 8/16 · 2.9e-07 · 0.0915 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0011 · 0.0066 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 5.4e-05 · 0.0612 |  |  |
| tri-in-squ n=5 | 1.803000 | 7/16 · 3.5e-04 · 0.0140 |  |  |
| tri-in-tri n=6 | 2.977082 | 2/16 · 4.3e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.08_nz16`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 7/16 · 5.8e-07 · 0.1830 |  |  |
| squ-in-cir n=8 | 1.978770 | 4/16 · 2.0e-04 · 0.0019 |  |  |
| squ-in-squ n=10 | 3.707107 | 4/16 · 7.2e-05 · 0.0607 |  |  |
| tri-in-squ n=5 | 1.803000 | 4/16 · 5.1e-04 · 0.0341 |  |  |
| tri-in-tri n=6 | 2.977082 | 3/16 · 1.5e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.08_nz32`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 9/16 · 5.8e-07 · 5.8e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0021 · 0.1325 |  |  |
| squ-in-squ n=10 | 3.707107 | 0/16 · 0.0625 · 0.2929 |  |  |
| tri-in-squ n=5 | 1.803000 | 3/16 · 4.4e-04 · 0.0332 |  |  |
| tri-in-tri n=6 | 2.977082 | 3/16 · 4.4e-05 · 0.0229 |  |  |

### budget 1, setting `mu0.08_nz8`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 10/16 · 5.8e-07 · 5.8e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 8/16 · 1.2e-04 · 9.9e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 6/16 · 1.5e-06 · 0.0412 |  |  |
| tri-in-squ n=5 | 1.803000 | 9/16 · 5.1e-04 · 5.1e-04 |  |  |
| tri-in-tri n=6 | 2.977082 | 1/16 · 2.8e-04 · 0.0234 |  |  |

### budget 1, setting `mu0.16_nz16`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 9/16 · 1.2e-06 · 1.2e-06 |  |  |
| squ-in-cir n=8 | 1.978770 | 12/16 · 2.5e-05 · 2.4e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 8/16 · 1.8e-06 · 0.0111 |  |  |
| tri-in-squ n=5 | 1.803000 | 3/16 · 5.1e-04 · 0.0240 |  |  |
| tri-in-tri n=6 | 2.977082 | 5/16 · 3.2e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.16_nz32`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 9/16 · 1.2e-06 · 1.2e-06 |  |  |
| squ-in-cir n=8 | 1.978770 | 7/16 · 2.5e-05 · 0.0018 |  |  |
| squ-in-squ n=10 | 3.707107 | 2/16 · 1.9e-06 · 0.0607 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 5.1e-04 · 0.0249 |  |  |
| tri-in-tri n=6 | 2.977082 | 3/16 · 3.0e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.16_nz8`

| instance | best known | harden | sa | pc |
|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 12/16 · 1.2e-06 · 1.2e-06 |  |  |
| squ-in-cir n=8 | 1.978770 | 15/16 · 3.0e-06 · 1.0e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 9/16 · 1.8e-06 · 2.1e-04 |  |  |
| tri-in-squ n=5 | 1.803000 | 3/16 · 5.1e-04 · 0.0341 |  |  |
| tri-in-tri n=6 | 2.977082 | 3/16 · 3.3e-04 · 0.0232 |  |  |

