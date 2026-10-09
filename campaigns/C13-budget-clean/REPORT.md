# C13-budget-clean: Longer runs or more runs? A clean budget study

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** C09 changed run length and restart count together and used instances selected for disagreement. Here, on 28 instances fixed in advance (n = 11, 17, 23, 29 per family; hexagons n = 8, 12, 16, 20), harden-best and rigid-best get (a) budget 3 with seeds 1-32, compared with C07 at budget 1 with the same 32 seeds, and (b) budget 1 with seeds 33-96, so that 96 short runs can be compared with 32 runs three times as long at equal total cost.

**Hypothesis.** Both paths improve with longer runs; hardening improves more, as in C09.

**Decision rule (pre-registered 2026-10-09).** Metric: lowest tightened size over the stated runs, per instance. Report, per budget arm, counts of instances where each path is lowest and solved, and the two-sided sign test of harden vs rigid; and, at equal total cost, 3x32 vs 1x96 per path. Tightening policy as C07.

**Status.** closed — **decision:** Per the rule: no arm separates harden and rigid (two-sided sign tests p = 0.18, 1, 0.29). The hypothesis that hardening improves more with longer runs is not supported; the paper withdraws the C09 claim and reports C09 only in the appendix as confounded.

## Findings

- On 28 instances fixed in advance, harden vs rigid lower: 7 vs 2 with 32 base runs, 4 vs 3 with 32 runs at 3x budget, 6 vs 2 with 96 base runs (all p >= 0.18). Longer runs improved rigid (5 lower, 0 higher than base) more than harden (4 vs 3). At equal cost, 3x longer and 3x more runs did about equally (harden 3 vs 3, rigid 3 vs 2). C09's indication that hardening gains more from longer runs does not replicate.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 1, setting `default`

| instance | best known | harden-best | rigid-best |
|---|---|---|---|
| cir-in-squ n=11 | 3.511255 | ✓ 64/64 · 3.0e-06 · 3.0e-06 | ✓ 64/64 · 3.0e-06 · 3.0e-06 |
| cir-in-squ n=17 | 4.266330 | ✓ 58/64 · 3.9e-06 · 3.9e-06 | ✓ 58/64 · 3.9e-06 · 3.9e-06 |
| cir-in-squ n=23 | 4.863703 | ✓ 6/64 · 1.1e-06 · 0.0757 | ✓ 6/64 · 1.1e-06 · 0.0757 |
| cir-in-squ n=29 | 5.407560 | ✓ 0/64 · 0.0010 · 0.0015 | ✓ 0/64 · 0.0010 · 0.0015 |
| hex-in-squ n=8 | 5.196152 | ✓ 63/64 · 5.6e-07 · 1.0e-06 | ✓ 61/64 · 5.7e-07 · 1.0e-06 |
| hex-in-squ n=12 | 6.387355 | ✓ 27/64 · 1.7e-06 · 0.0078 | ✓ 22/64 · 1.7e-06 · 0.0078 |
| hex-in-squ n=16 | 7.311304 | ✓ 20/64 · 1.8e-06 · 0.0501 | ✓ 22/64 · 1.8e-06 · 0.0339 |
| hex-in-squ n=20 | 7.948954 | ✓ 22/64 · 3.8e-06 · 0.0175 | ✓ 26/64 · 3.8e-06 · 0.0175 |
| squ-in-cir n=11 | 2.213860 | ✓ 13/64 · 2.4e-04 · 0.0079 | ✓ 11/64 · 2.4e-04 · 0.0019 |
| squ-in-cir n=17 | 2.676870 | 1/64 · 9.8e-04 · 0.0147 | 3/64 · 7.4e-04 · 0.0136 |
| squ-in-cir n=23 | 3.067380 | 0/64 · 0.0013 · 0.0255 | 0/64 · 0.0065 · 0.0405 |
| squ-in-cir n=29 | 3.393090 | 0/64 · 0.0044 · 0.1457 | 0/64 · 0.0048 · 0.1053 |
| squ-in-squ n=11 | 3.877084 | ✓ 2/64 · 6.8e-06 · 0.0202 | 0/64 · 0.0136 · 0.1229 |
| squ-in-squ n=17 | 4.675530 | 0/64 · 0.0046 · 0.0336 | 0/64 · 0.0316 · 0.0317 |
| squ-in-squ n=23 | 5.000000 | ✓ 57/64 · 1.7e-06 · 3.1e-06 | ✓ 64/64 · 1.1e-06 · 2.4e-06 |
| squ-in-squ n=29 | 5.933833 | ✓ 2/64 · 7.6e-04 · 0.0664 | 0/64 · 0.0662 · 0.0662 |
| squ-in-tri n=11 | 6.154701 | ✓ 64/64 · 9.0e-07 · 3.4e-06 | ✓ 58/64 · 1.1e-06 · 3.1e-06 |
| squ-in-tri n=17 | 7.301000 | 0/64 · 0.0084 · 0.0084 | 0/64 · 0.0084 · 0.0084 |
| squ-in-tri n=23 | 8.301000 | 0/64 · 0.0084 · 0.0084 | 0/64 · 0.0084 · 0.0084 |
| squ-in-tri n=29 | 9.154701 | ✓ 63/64 · 4.5e-06 · 9.6e-06 | ✓ 57/64 · 4.5e-06 · 8.3e-06 |
| tri-in-squ n=11 | 2.490000 | ✓ 0/64 · 0.0015 · 0.0331 | ✓ 0/64 · 0.0031 · 0.0388 |
| tri-in-squ n=17 | 2.982000 | 0/64 · 0.0157 · 0.1275 | 0/64 · 0.0157 · 0.0612 |
| tri-in-squ n=23 | 3.431100 | 0/64 · 0.0092 · 0.1117 | 0/64 · 0.0077 · 0.0644 |
| tri-in-squ n=29 | 3.817110 | 0/64 · 0.0210 · 0.1401 | 0/64 · 0.0187 · 0.1147 |
| tri-in-tri n=11 | 3.722971 | ✓ 0/64 · 0.0050 · 0.0050 | 0/64 · 0.0050 · 0.0050 |
| tri-in-tri n=17 | 4.465000 | 0/64 · 0.0350 · 0.0350 | 0/64 · 0.0350 · 0.0350 |
| tri-in-tri n=23 | 5.000000 | ✓ 30/64 · 5.5e-06 · 0.2789 | ✓ 54/64 · 5.1e-06 · 7.8e-06 |
| tri-in-tri n=29 | 5.666667 | 0/64 · 0.0774 · 0.2827 | ✓ 8/64 · 5.8e-06 · 0.1620 |

### budget 3, setting `default`

| instance | best known | harden-best | rigid-best |
|---|---|---|---|
| cir-in-squ n=11 | 3.511255 | ✓ 32/32 · 2.9e-06 · 2.9e-06 | ✓ 32/32 · 2.9e-06 · 2.9e-06 |
| cir-in-squ n=17 | 4.266330 | ✓ 32/32 · 3.5e-06 · 3.5e-06 | ✓ 32/32 · 3.5e-06 · 3.5e-06 |
| cir-in-squ n=23 | 4.863703 | ✓ 2/32 · 1.1e-06 · 0.0629 | ✓ 2/32 · 1.1e-06 · 0.0629 |
| cir-in-squ n=29 | 5.407560 | ✓ 32/32 · 8.9e-06 · 9.0e-06 | ✓ 32/32 · 8.9e-06 · 9.0e-06 |
| hex-in-squ n=8 | 5.196152 | ✓ 32/32 · 4.2e-07 · 8.7e-07 | ✓ 32/32 · 4.7e-07 · 8.7e-07 |
| hex-in-squ n=12 | 6.387355 | ✓ 13/32 · 1.5e-06 · 0.0078 | ✓ 18/32 · 1.6e-06 · 1.8e-06 |
| hex-in-squ n=16 | 7.311304 | ✓ 19/32 · 1.7e-06 · 1.9e-06 | ✓ 18/32 · 1.8e-06 · 1.9e-06 |
| hex-in-squ n=20 | 7.948954 | ✓ 21/32 · 1.3e-06 · 1.5e-06 | ✓ 16/32 · 1.2e-06 · 0.0087 |
| squ-in-cir n=11 | 2.213860 | ✓ 10/32 · 7.5e-05 · 0.0014 | ✓ 3/32 · 7.5e-05 · 0.0019 |
| squ-in-cir n=17 | 2.676870 | 0/32 · 0.0011 · 0.0101 | 2/32 · 7.4e-04 · 0.0076 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0047 · 0.1296 | 0/32 · 0.0039 · 0.0132 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0016 · 0.0359 | 0/32 · 0.0020 · 0.0362 |
| squ-in-squ n=11 | 3.877084 | ✓ 2/32 · 2.9e-06 · 0.0101 | 0/32 · 0.0101 · 0.1229 |
| squ-in-squ n=17 | 4.675530 | ✓ 1/32 · 1.1e-05 · 0.0316 | 0/32 · 0.0316 · 0.3245 |
| squ-in-squ n=23 | 5.000000 | ✓ 32/32 · 2.2e-06 · 3.3e-06 | ✓ 32/32 · 1.0e-06 · 2.4e-06 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0230 · 0.0662 | 0/32 · 0.0662 · 0.0662 |
| squ-in-tri n=11 | 6.154701 | ✓ 32/32 · 1.0e-06 · 2.1e-06 | ✓ 32/32 · 1.3e-06 · 2.2e-06 |
| squ-in-tri n=17 | 7.301000 | 0/32 · 0.0084 · 0.0084 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=23 | 8.301000 | 0/32 · 0.0084 · 0.0084 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=29 | 9.154701 | ✓ 31/32 · 2.3e-06 · 5.9e-06 | ✓ 29/32 · 2.8e-06 · 6.1e-06 |
| tri-in-squ n=11 | 2.490000 | ✓ 2/32 · 9.6e-04 · 0.0331 | ✓ 1/32 · 9.6e-04 · 0.0144 |
| tri-in-squ n=17 | 2.982000 | 0/32 · 0.0157 · 0.0942 | 0/32 · 0.0157 · 0.0462 |
| tri-in-squ n=23 | 3.431100 | 0/32 · 0.0197 · 0.0571 | 0/32 · 0.0109 · 0.0432 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0158 · 0.0898 | 0/32 · 0.0020 · 0.0507 |
| tri-in-tri n=11 | 3.722971 | ✓ 0/32 · 0.0040 · 0.0040 | ✓ 0/32 · 0.0040 · 0.0040 |
| tri-in-tri n=17 | 4.465000 | 0/32 · 0.0350 · 0.0350 | 0/32 · 0.0350 · 0.0350 |
| tri-in-tri n=23 | 5.000000 | ✓ 24/32 · 5.9e-06 · 6.8e-06 | ✓ 31/32 · 5.2e-06 · 7.1e-06 |
| tri-in-tri n=29 | 5.666667 | ✓ 2/32 · 5.5e-06 · 0.2163 | ✓ 13/32 · 4.7e-06 · 0.0423 |

