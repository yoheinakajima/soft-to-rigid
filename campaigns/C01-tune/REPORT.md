# C01-tune: Tune every method on held-out instances with the same effort

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Each method has two hyperparameters that matter. Give every method the same 3 x 3 grid on five tuning instances, pick its best setting by a fixed rule, and freeze it for all later campaigns.

**Hypothesis.** None; this is calibration so that later comparisons are not against untuned baselines.

**Decision rule (pre-registered 2026-10-08).** For each method, score each setting by the mean over tuning instances of (median legal size / best known - 1) over 16 seeds; ties broken by the mean of the best gap. The winning setting is written to methods/<method>.json and the tuning instances are excluded from headline comparisons.

**Status.** closed — **decision:** Scored with scripts/score_tuning.py. Winners on grid edges for harden, grow, rigid, sa and pc's relax; extended in C02 as the rule requires.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 1, setting `T0.0001_mu0.005`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 8/16 · 3.7e-04 · 0.0197 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 3/16 · 2.9e-04 · 0.0024 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 3/16 · 6.4e-04 · 0.2939 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0013 · 0.0355 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0077 · 0.0254 |  |

### budget 1, setting `T0.0001_mu0.02`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0018 · 0.0023 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 3/16 · 5.5e-04 · 0.0055 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0025 · 0.2947 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0030 · 0.0415 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0163 · 0.0301 |  |

### budget 1, setting `T0.0001_mu0.08`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0064 · 0.1220 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0012 · 0.0027 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0061 · 0.0766 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0215 · 0.0428 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0272 · 0.0511 |  |

### budget 1, setting `T0.001_mu0.005`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 7/16 · 5.8e-04 · 0.0197 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 6/16 · 4.7e-04 · 0.0013 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 1/16 · 6.5e-04 · 0.1891 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 1/16 · 5.6e-04 · 0.0293 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0150 · 0.0259 |  |

### budget 1, setting `T0.001_mu0.02`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0025 · 0.1890 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 5/16 · 4.4e-04 · 0.0014 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0027 · 0.0658 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0041 · 0.0340 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0184 · 0.0314 |  |

### budget 1, setting `T0.001_mu0.08`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0075 · 0.0094 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0012 · 0.0018 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0761 · 0.3041 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0057 · 0.0462 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0339 · 0.0677 |  |

### budget 1, setting `T0.01_mu0.005`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 2/16 · 8.5e-04 · 0.0036 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 2/16 · 3.7e-04 · 0.0018 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 2/16 · 8.6e-04 · 0.1882 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0192 · 0.0417 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0122 · 0.0338 |  |

### budget 1, setting `T0.01_mu0.02`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0028 · 0.1869 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 6/16 · 4.7e-04 · 0.0017 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0030 · 0.2956 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0049 · 0.0433 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0253 · 0.0399 |  |

### budget 1, setting `T0.01_mu0.08`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  | 0/16 · 0.0087 · 0.1087 |  |
| squ-in-cir n=8 | 1.978770 |  |  |  | 0/16 · 0.0015 · 0.0020 |  |
| squ-in-squ n=10 | 3.707107 |  |  |  | 0/16 · 0.0096 · 0.2992 |  |
| tri-in-squ n=5 | 1.803000 |  |  |  | 0/16 · 0.0075 · 0.0684 |  |
| tri-in-tri n=6 | 2.977082 |  |  |  | 0/16 · 0.0402 · 0.0646 |  |

### budget 1, setting `kick0.05_relax1200`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0525 · 0.2504 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0086 · 0.1311 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2938 · 0.3376 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0045 · 0.1054 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0062 · 0.0500 |

### budget 1, setting `kick0.05_relax300`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0750 · 0.3988 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0212 · 0.2024 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2929 · 0.5033 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0452 · 0.1747 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0229 · 0.2273 |

### budget 1, setting `kick0.05_relax600`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0750 · 0.2768 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0089 · 0.1673 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2931 · 0.4445 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0051 · 0.1504 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0178 · 0.1274 |

### budget 1, setting `kick0.15_relax1200`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0525 · 0.2504 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0086 · 0.1311 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2938 · 0.3376 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0045 · 0.1054 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0062 · 0.0500 |

### budget 1, setting `kick0.15_relax300`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0750 · 0.3988 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0212 · 0.2024 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2929 · 0.5033 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0452 · 0.1747 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0229 · 0.2196 |

### budget 1, setting `kick0.15_relax600`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0750 · 0.2768 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0089 · 0.1673 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2931 · 0.4445 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0051 · 0.1504 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0178 · 0.1274 |

### budget 1, setting `kick0.4_relax1200`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0525 · 0.2504 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0086 · 0.1311 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2938 · 0.3376 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0045 · 0.1054 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0062 · 0.0500 |

### budget 1, setting `kick0.4_relax300`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0750 · 0.3988 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0212 · 0.2024 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2929 · 0.5033 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0452 · 0.1415 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0229 · 0.2299 |

### budget 1, setting `kick0.4_relax600`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  |  |  |  | 0/16 · 0.0750 · 0.2768 |
| squ-in-cir n=8 | 1.978770 |  |  |  |  | 0/16 · 0.0089 · 0.1673 |
| squ-in-squ n=10 | 3.707107 |  |  |  |  | 0/16 · 0.2931 · 0.4445 |
| tri-in-squ n=5 | 1.803000 |  |  |  |  | 0/16 · 0.0051 · 0.1504 |
| tri-in-tri n=6 | 2.977082 |  |  |  |  | 0/16 · 0.0178 · 0.1274 |

### budget 1, setting `mu0.01_g0.2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 4/16 · 7.3e-08 · 0.1830 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0034 · 0.0092 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0892 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 0/16 · 0.0140 · 0.0334 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 1/16 · 4.4e-05 · 0.0229 |  |  |  |

### budget 1, setting `mu0.01_g0.35`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 3/16 · 7.3e-08 · 0.1897 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 0/16 · 0.0012 · 0.0087 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0854 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 1/16 · 2.3e-04 · 0.0336 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 1/16 · 2.8e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.01_g0.5`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 6/16 · 7.3e-08 · 0.1830 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 1/16 · 7.9e-04 · 0.0150 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0218 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 1/16 · 6.1e-04 · 0.0337 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 2/16 · 2.2e-06 · 0.0229 |  |  |  |

### budget 1, setting `mu0.01_nz0.5`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 4/16 · 7.3e-08 · 0.0545 |  | 2/16 · 7.3e-08 · 0.2032 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0116 · 0.0304 |  | 4/16 · 4.7e-04 · 0.0828 |  |  |
| squ-in-squ n=10 | 3.707107 | 0/16 · 0.0219 · 0.0931 |  | 0/16 · 0.0215 · 0.2929 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 2.9e-04 · 0.0353 |  | 1/16 · 3.4e-04 · 0.0480 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 4/16 · 1.4e-06 · 0.0229 |  |  |

### budget 1, setting `mu0.01_nz1`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 5/16 · 7.3e-08 · 0.0383 |  | 6/16 · 7.3e-08 · 0.1830 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0064 · 0.0206 |  | 3/16 · 2.9e-04 · 0.0081 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 5.8e-05 · 0.0617 |  | 1/16 · 1.5e-04 · 0.2929 |  |  |
| tri-in-squ n=5 | 1.803000 | 0/16 · 0.0140 · 0.0530 |  | 5/16 · 2.5e-04 · 0.0150 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 2/16 · 1.9e-06 · 0.0229 |  |  |

### budget 1, setting `mu0.01_nz2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 4/16 · 7.3e-08 · 0.1226 |  | 6/16 · 7.3e-08 · 0.1830 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0081 · 0.0281 |  | 1/16 · 6.7e-04 · 0.0180 |  |  |
| squ-in-squ n=10 | 3.707107 | 0/16 · 0.0256 · 0.0641 |  | 2/16 · 7.3e-05 · 0.1452 |  |  |
| tri-in-squ n=5 | 1.803000 | 0/16 · 0.0274 · 0.0415 |  | 2/16 · 2.1e-04 · 0.0333 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 2/16 · 2.4e-05 · 0.0229 |  |  |

### budget 1, setting `mu0.02_g0.2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 1/16 · 1.5e-07 · 0.2032 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 5/16 · 1.8e-04 · 0.0019 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 1/16 · 4.2e-07 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 3.7e-04 · 0.0140 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 1/16 · 6.0e-05 · 0.0229 |  |  |  |

### budget 1, setting `mu0.02_g0.35`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 6/16 · 1.5e-07 · 0.1830 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 4/16 · 9.6e-05 · 0.0037 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 0/16 · 0.0216 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 2.6e-04 · 0.0339 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 6/16 · 6.5e-05 · 0.0229 |  |  |  |

### budget 1, setting `mu0.02_g0.5`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 7/16 · 1.5e-07 · 0.1100 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 9/16 · 1.8e-05 · 7.3e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 1/16 · 3.5e-06 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 2.6e-04 · 0.0340 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 2/16 · 6.0e-05 · 0.0229 |  |  |  |

### budget 1, setting `mu0.02_nz0.5`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 3/16 · 1.5e-07 · 0.1100 |  | 4/16 · 1.5e-07 · 0.1830 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0035 · 0.0123 |  | 6/16 · 6.7e-06 · 0.0524 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 2.1e-07 · 0.0749 |  | 2/16 · 7.0e-07 · 0.2929 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 2.4e-04 · 0.0336 |  | 3/16 · 2.5e-04 · 0.0339 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 4/16 · 3.4e-05 · 0.0229 |  |  |

### budget 1, setting `mu0.02_nz1`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 6/16 · 1.5e-07 · 0.0370 |  | 7/16 · 1.5e-07 · 0.1100 |  |  |
| squ-in-cir n=8 | 1.978770 | 1/16 · 9.5e-04 · 0.0106 |  | 8/16 · 4.7e-05 · 8.7e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 0/16 · 0.0026 · 0.0614 |  | 4/16 · 5.9e-07 · 0.2043 |  |  |
| tri-in-squ n=5 | 1.803000 | 1/16 · 5.0e-04 · 0.0336 |  | 4/16 · 2.5e-04 · 0.0240 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 5/16 · 4.6e-05 · 0.0229 |  |  |

### budget 1, setting `mu0.02_nz2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 6/16 · 1.5e-07 · 0.0372 |  | 9/16 · 1.5e-07 · 1.5e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0024 · 0.0125 |  | 4/16 · 3.4e-06 · 0.0058 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 2.9e-06 · 0.0615 |  | 5/16 · 2.6e-07 · 0.0607 |  |  |
| tri-in-squ n=5 | 1.803000 | 3/16 · 1.8e-04 · 0.0337 |  | 3/16 · 2.5e-04 · 0.0339 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0229 |  | 6/16 · 2.9e-06 · 0.0229 |  |  |

### budget 1, setting `mu0.04_g0.2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 8/16 · 2.9e-07 · 0.1016 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 10/16 · 1.9e-06 · 6.7e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 4/16 · 5.0e-07 · 0.0931 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 3.8e-04 · 0.0341 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 3/16 · 1.6e-04 · 0.0233 |  |  |  |

### budget 1, setting `mu0.04_g0.35`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 8/16 · 2.9e-07 · 0.0915 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 15/16 · 7.2e-06 · 1.4e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 3/16 · 4.2e-07 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 3.8e-04 · 0.0341 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 3/16 · 1.4e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.04_g0.5`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 |  | 11/16 · 2.9e-07 · 2.9e-07 |  |  |  |
| squ-in-cir n=8 | 1.978770 |  | 13/16 · 1.1e-05 · 1.6e-04 |  |  |  |
| squ-in-squ n=10 | 3.707107 |  | 1/16 · 5.2e-07 · 0.2929 |  |  |  |
| tri-in-squ n=5 | 1.803000 |  | 2/16 · 3.8e-04 · 0.0341 |  |  |  |
| tri-in-tri n=6 | 2.977082 |  | 6/16 · 1.6e-04 · 0.0229 |  |  |  |

### budget 1, setting `mu0.04_nz0.5`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 5/16 · 2.9e-07 · 0.1100 |  | 2/16 · 2.9e-07 · 0.1226 |  |  |
| squ-in-cir n=8 | 1.978770 | 0/16 · 0.0011 · 0.0038 |  | 8/16 · 5.9e-06 · 0.0025 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 1.1e-05 · 0.0659 |  | 1/16 · 1.2e-06 · 0.1935 |  |  |
| tri-in-squ n=5 | 1.803000 | 0/16 · 0.0140 · 0.0341 |  | 2/16 · 3.7e-04 · 0.0240 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0234 |  | 3/16 · 1.8e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.04_nz1`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 8/16 · 2.9e-07 · 0.0915 |  | 7/16 · 2.9e-07 · 0.1830 |  |  |
| squ-in-cir n=8 | 1.978770 | 1/16 · 9.1e-04 · 0.0034 |  | 10/16 · 1.0e-06 · 1.4e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 1.1e-06 · 0.0609 |  | 5/16 · 6.0e-07 · 0.0607 |  |  |
| tri-in-squ n=5 | 1.803000 | 1/16 · 3.5e-04 · 0.0480 |  | 2/16 · 3.7e-04 · 0.0241 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0234 |  | 4/16 · 1.8e-04 · 0.0229 |  |  |

### budget 1, setting `mu0.04_nz2`

| instance | best known | harden | grow | rigid | sa | pc |
|---|---|---|---|---|---|---|
| hex-in-squ n=5 | 4.437822 | 10/16 · 2.9e-07 · 2.9e-07 |  | 10/16 · 2.9e-07 · 2.9e-07 |  |  |
| squ-in-cir n=8 | 1.978770 | 1/16 · 5.1e-04 · 0.0058 |  | 10/16 · 1.1e-04 · 3.1e-04 |  |  |
| squ-in-squ n=10 | 3.707107 | 1/16 · 4.6e-06 · 0.0609 |  | 9/16 · 3.9e-07 · 2.3e-04 |  |  |
| tri-in-squ n=5 | 1.803000 | 2/16 · 3.5e-04 · 0.0341 |  | 2/16 · 3.7e-04 · 0.0240 |  |  |
| tri-in-tri n=6 | 2.977082 | 0/16 · 0.0229 · 0.0232 |  | 10/16 · 9.0e-05 · 1.9e-04 |  |  |

