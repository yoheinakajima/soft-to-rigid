# C02-tune-extend: Extend the tuning grid where C01's winner sat on its edge

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** In C01 the winning setting of every method except pc's kick lay on the edge of its grid (harden, rigid: mu 0.04 and noise x2; grow: mu 0.04, gamma0 0.2; sa: mu 0.005; pc: relax 1200). Extend each grid past that edge on the same five tuning instances and seeds.

**Hypothesis.** Stronger pressure and noise help every gradient method on these small instances; the C01 result that tuned rigid beats tuned harden on median gap (0.0027 vs 0.0092) may persist.

**Decision rule (pre-registered 2026-10-08).** Same scoring rule as C01. The overall winner across C01 and C02 for each method is frozen into methods/<method>.json. If a winner is again on an outer edge, run one more extension (at most two in total), then freeze regardless.

**Status.** closed — **decision:** Scored over C01+C02. grow (mu 0.04, gamma0 0.2) and rigid (mu 0.04, noise x2) are now interior and frozen. harden (mu 0.08, noise x8), sa (T0 3e-3, mu 0.0025) and pc (relax 4800) are still on an edge: extended once more in C03.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 1, setting `T0.0003_mu0.00125`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0021 · 0.2036 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0064 · 0.0191 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0165 · 0.0808 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 1/16 · 7.4e-04 · 0.0344 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0041 · 0.0240 |  |

### budget 1, setting `T0.0003_mu0.0025`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 4/16 · 4.6e-05 · 0.0375 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0049 · 0.0100 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0086 · 0.3137 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0145 · 0.0420 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0024 · 0.0240 |  |

### budget 1, setting `T0.0003_mu0.005`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 7/16 · 3.0e-04 · 0.1106 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 1/16 · 7.0e-04 · 0.0063 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 1/16 · 6.0e-04 · 0.1906 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0012 · 0.0336 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0058 · 0.0261 |  |

### budget 1, setting `T0.001_mu0.00125`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 2/16 · 4.5e-04 · 0.0248 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0067 · 0.0199 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0256 · 0.0961 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 1/16 · 7.8e-04 · 0.0229 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0102 · 0.0237 |  |

### budget 1, setting `T0.001_mu0.0025`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 10/16 · 5.4e-05 · 3.8e-04 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0031 · 0.0102 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0146 · 0.3000 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 1/16 · 8.9e-04 · 0.0269 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0132 · 0.0245 |  |

### budget 1, setting `T0.001_mu0.005`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 7/16 · 3.9e-04 · 0.0203 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0014 · 0.0063 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0018 · 0.0639 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 1/16 · 9.8e-04 · 0.0350 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0041 · 0.0261 |  |

### budget 1, setting `T0.003_mu0.00125`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 2/16 · 5.5e-04 · 0.0078 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0064 · 0.0157 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0440 · 0.3156 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0145 · 0.0326 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0109 · 0.0249 |  |

### budget 1, setting `T0.003_mu0.0025`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 5/16 · 9.1e-05 · 0.0047 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0040 · 0.0126 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0115 · 0.0575 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 2/16 · 7.0e-04 · 0.0355 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0154 · 0.0247 |  |

### budget 1, setting `T0.003_mu0.005`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 4/16 · 3.1e-04 · 0.1837 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 1/16 · 5.1e-04 · 0.0071 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0012 · 0.0680 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0012 · 0.0212 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0078 · 0.0281 |  |

### budget 1, setting `kick0.05_relax1200`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0556 · 0.2561 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0128 · 0.1327 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2954 · 0.3431 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0055 · 0.1056 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0115 · 0.0510 |

### budget 1, setting `kick0.05_relax2400`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0216 · 0.2534 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.3054 · 0.3332 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0084 · 0.0926 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.05_relax4800`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0440 · 0.2526 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0084 · 0.0994 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.15_relax1200`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0556 · 0.2561 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0128 · 0.1327 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2954 · 0.3431 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0055 · 0.1056 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0115 · 0.0510 |

### budget 1, setting `kick0.15_relax2400`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0216 · 0.2534 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.3054 · 0.3332 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0084 · 0.0926 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.15_relax4800`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0440 · 0.2526 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0084 · 0.0994 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.4_relax1200`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0556 · 0.2561 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0128 · 0.1327 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2954 · 0.3431 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0055 · 0.1056 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0115 · 0.0510 |

### budget 1, setting `kick0.4_relax2400`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0216 · 0.2534 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.3054 · 0.3332 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0084 · 0.0926 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `kick0.4_relax4800`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0440 · 0.2526 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0056 · 0.1295 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.0695 · 0.3054 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0084 · 0.0994 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0079 · 0.0384 |

### budget 1, setting `mu0.04_g0.1`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 15/16 · 2.9e-07 · 2.9e-07 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 11/16 · 2.0e-05 · 5.6e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0606 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 1/16 · 3.8e-04 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 5/16 · 1.7e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.04_g0.2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 8/16 · 2.9e-07 · 0.1016 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 10/16 · 1.9e-06 · 6.7e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 4/16 · 5.0e-07 · 0.0931 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 3.8e-04 · 0.0341 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 3/16 · 1.6e-04 · 0.0233 |  |  |  |

### budget 1, setting `mu0.04_g0.3`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 7/16 · 2.9e-07 · 0.1931 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 16/16 · 5.2e-06 · 9.8e-05 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 1/16 · 4.8e-07 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 1/16 · 3.8e-04 · 0.0341 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 3/16 · 1.5e-04 · 0.0233 |  |  |  |

### budget 1, setting `mu0.04_nz2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 10/16 · 2.9e-07 · 2.9e-07 |  | 10/16 · 2.9e-07 · 2.9e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 1/16 · 5.1e-04 · 0.0058 |  | 10/16 · 1.1e-04 · 3.1e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 4.6e-06 · 0.0609 |  | 9/16 · 3.9e-07 · 2.3e-04 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 3.5e-04 · 0.0341 |  | 2/16 · 3.7e-04 · 0.0240 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0232 |  | 10/16 · 9.0e-05 · 1.9e-04 |  |  |

### budget 1, setting `mu0.04_nz4`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 7/16 · 2.9e-07 · 0.1830 |  | 7/16 · 2.9e-07 · 0.1830 |  |  |
| squ-in-cir n=8 | 1.978770 | 1/16 · 6.8e-04 · 0.0055 |  | 13/16 · 1.7e-05 · 4.3e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 0/16 · 0.0049 · 0.0612 |  | 7/16 · 5.4e-07 · 0.0412 |  |  |
| tri-in-squ n=5 | 1.803000 | 6/16 · 3.5e-04 · 0.0240 |  | 3/16 · 3.7e-04 · 0.0140 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 9/16 · 5.2e-05 · 4.3e-04 |  |  |

### budget 1, setting `mu0.04_nz8`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 8/16 · 2.9e-07 · 0.0915 |  | 7/16 · 2.9e-07 · 0.0370 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0011 · 0.0066 |  | 3/16 · 3.1e-04 · 0.0044 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 5.4e-05 · 0.0612 |  | 2/16 · 5.8e-07 · 0.0608 |  |  |
| tri-in-squ n=5 | 1.803000 | 7/16 · 3.5e-04 · 0.0140 |  | 3/16 · 4.3e-04 · 0.0341 |  |  |
| tri-in-tri n=6 | 2.977082 | 2/16 · 4.3e-04 · 0.0229 |  | 1/16 · 3.7e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.08_g0.1`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 11/16 · 5.8e-07 · 5.8e-07 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 11/16 · 3.3e-05 · 2.6e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0607 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 6/16 · 2.2e-04 · 0.0208 |  |  |  |

### budget 1, setting `mu0.08_g0.2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 10/16 · 5.8e-07 · 5.8e-07 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 15/16 · 2.4e-05 · 1.1e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0607 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 6/16 · 2.1e-04 · 0.0218 |  |  |  |

### budget 1, setting `mu0.08_g0.3`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 8/16 · 5.8e-07 · 0.1016 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 16/16 · 3.6e-05 · 9.8e-05 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 1/16 · 1.3e-06 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 5/16 · 2.1e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.08_nz2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 9/16 · 5.8e-07 · 5.8e-07 |  | 8/16 · 5.8e-07 · 0.0915 |  |  |
| squ-in-cir n=8 | 1.978770 | 5/16 · 3.2e-04 · 0.0013 |  | 12/16 · 7.1e-05 · 1.4e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 2/16 · 1.8e-06 · 0.0607 |  | 9/16 · 8.9e-07 · 4.1e-05 |  |  |
| tri-in-squ n=5 | 1.803000 | 3/16 · 5.1e-04 · 0.0341 |  | 1/16 · 5.1e-04 · 0.0341 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0234 |  | 1/16 · 2.2e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.08_nz4`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 7/16 · 5.8e-07 · 0.1830 |  | 9/16 · 5.8e-07 · 5.8e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 9/16 · 6.4e-05 · 7.1e-04 |  | 16/16 · 1.6e-06 · 1.1e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 2.8e-06 · 0.0607 |  | 8/16 · 9.1e-07 · 0.1465 |  |  |
| tri-in-squ n=5 | 1.803000 | 7/16 · 5.1e-04 · 0.0341 |  | 1/16 · 5.1e-04 · 0.0140 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0234 |  | 3/16 · 1.9e-04 · 0.0208 |  |  |

### budget 1, setting `mu0.08_nz8`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 10/16 · 5.8e-07 · 5.8e-07 |  | 10/16 · 5.8e-07 · 5.8e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 8/16 · 1.2e-04 · 9.9e-04 |  | 13/16 · 8.8e-06 · 3.0e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 6/16 · 1.5e-06 · 0.0412 |  | 7/16 · 8.1e-07 · 0.0607 |  |  |
| tri-in-squ n=5 | 1.803000 | 9/16 · 5.1e-04 · 5.1e-04 |  | 4/16 · 5.1e-04 · 0.0140 |  |  |
| tri-in-tri n=6 | 2.977082 | 1/16 · 2.8e-04 · 0.0234 |  | 5/16 · 2.2e-04 · 0.0207 |  |  |

### budget 1, setting `mu0.16_g0.1`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 9/16 · 1.2e-06 · 1.2e-06 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 15/16 · 1.5e-04 · 2.9e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.2929 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0341 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 4/16 · 3.2e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.16_g0.2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 10/16 · 1.2e-06 · 1.2e-06 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 11/16 · 1.4e-04 · 5.7e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.2929 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 5/16 · 3.2e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.16_g0.3`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 9/16 · 1.2e-06 · 1.2e-06 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 15/16 · 1.4e-04 · 2.9e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.2929 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 11/16 · 3.2e-04 · 3.3e-04 |  |  |  |

### budget 1, setting `mu0.16_nz2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 9/16 · 1.2e-06 · 1.2e-06 |  | 8/16 · 1.2e-06 · 0.1016 |  |  |
| squ-in-cir n=8 | 1.978770 | 16/16 · 7.5e-05 · 8.9e-05 |  | 10/16 · 3.0e-04 · 4.3e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 4/16 · 4.8e-06 · 0.0611 |  | 7/16 · 2.1e-06 · 0.2929 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 5.1e-04 · 0.0341 |  | 0/16 · 0.0140 · 0.0341 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0234 · 0.0234 |  | 4/16 · 3.2e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.16_nz4`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 10/16 · 1.2e-06 · 1.2e-06 |  | 9/16 · 1.2e-06 · 1.2e-06 |  |  |
| squ-in-cir n=8 | 1.978770 | 16/16 · 5.8e-06 · 8.6e-05 |  | 15/16 · 1.2e-04 · 2.9e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 10/16 · 1.7e-06 · 2.9e-04 |  | 4/16 · 1.6e-06 · 0.2929 |  |  |
| tri-in-squ n=5 | 1.803000 | 0/16 · 0.0341 · 0.0341 |  | 0/16 · 0.0140 · 0.0140 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0234 |  | 10/16 · 3.2e-04 · 3.3e-04 |  |  |

### budget 1, setting `mu0.16_nz8`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 12/16 · 1.2e-06 · 1.2e-06 |  | 12/16 · 1.2e-06 · 1.2e-06 |  |  |
| squ-in-cir n=8 | 1.978770 | 15/16 · 3.0e-06 · 1.0e-04 |  | 16/16 · 2.1e-05 · 2.3e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 9/16 · 1.8e-06 · 2.1e-04 |  | 10/16 · 1.7e-06 · 7.8e-05 |  |  |
| tri-in-squ n=5 | 1.803000 | 3/16 · 5.1e-04 · 0.0341 |  | 0/16 · 0.0140 · 0.0341 |  |  |
| tri-in-tri n=6 | 2.977082 | 3/16 · 3.3e-04 · 0.0232 |  | 11/16 · 3.1e-04 · 3.3e-04 |  |  |

