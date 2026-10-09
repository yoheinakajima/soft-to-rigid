# C10-portfolio: Is a second path worth more than more of the same path?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Run together, harden and rigid solve more instances than either alone, but with twice the runs. Run rigid-best for 32 more seeds (33-64) on all 188 instances and compare rigid with 64 runs against rigid 32 + harden 32 (same total budget), and against rigid 32 + grow 32.

**Hypothesis.** Mixing paths beats doubling one path: rigid 32 + harden 32 solves more instances than rigid 64, because the paths fail on different instances (squares in a square vs triangles).

**Decision rule (pre-registered 2026-10-08).** Count instances solved (as in C07) by: rigid 64 (C07 seeds 1-32 + C10 seeds 33-64), rigid 32 + harden 32, rigid 32 + grow 32. One-sided sign test of the mixed portfolio against rigid 64 over instances solved by exactly one. Report lowest-point counts as in C07.

**Status.** closed — **decision:** Hypothesis not supported: mixing paths (139) is no better than doubling rigid (138) at equal budget. The paper reports that the paths are complementary by family but that, without knowing the family's character in advance, extra rigid runs are as good as adding hardening runs.

## Findings

- Portfolio at equal total budget: 32 rigid runs plus 32 harden runs solve 139 of 188 instances, 64 rigid runs 138, and 32 rigid plus 32 grow 137. Instances solved by exactly one of mixed vs doubled: 4 vs 3 (one-sided p = 0.5). A second path is worth about as much as doubling the runs of the best single path; it does not beat it.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

| instance | best known | rigid-best |
|---|---|---|
| cir-in-squ n=2 | 1.707107 | ✓ 32/32 · 0 · 0 |
| cir-in-squ n=3 | 1.965926 | ✓ 0/32 · 0.0341 · 0.0341 |
| cir-in-squ n=4 | 2.000000 | ✓ 32/32 · 0 · 0 |
| cir-in-squ n=5 | 2.414214 | ✓ 16/32 · 0 · 0.0656 |
| cir-in-squ n=6 | 2.664101 | ✓ 32/32 · 2.2e-06 · 2.2e-06 |
| cir-in-squ n=7 | 2.866025 | ✓ 32/32 · 5.4e-07 · 5.4e-07 |
| cir-in-squ n=8 | 2.931852 | ✓ 32/32 · 3.2e-07 · 3.2e-07 |
| cir-in-squ n=9 | 3.000000 | ✓ 32/32 · 0 · 0 |
| cir-in-squ n=10 | 3.373721 | 0/32 · 0.0064 · 0.0098 |
| cir-in-squ n=11 | 3.511255 | ✓ 32/32 · 3.0e-06 · 3.0e-06 |
| cir-in-squ n=12 | 3.572479 | ✓ 32/32 · 1.3e-06 · 1.3e-06 |
| cir-in-squ n=13 | 3.731524 | 27/32 · 4.3e-04 · 4.3e-04 |
| cir-in-squ n=14 | 3.866025 | ✓ 3/32 · 1.6e-06 · 0.0067 |
| cir-in-squ n=15 | 3.931852 | ✓ 31/32 · 8.0e-07 · 8.0e-07 |
| cir-in-squ n=16 | 4.000000 | ✓ 32/32 · 1.1e-08 · 1.1e-08 |
| cir-in-squ n=17 | 4.266330 | ✓ 30/32 · 3.9e-06 · 3.9e-06 |
| cir-in-squ n=18 | 4.328201 | ✓ 27/32 · 1.2e-06 · 1.2e-06 |
| cir-in-squ n=19 | 4.453730 | ✓ 24/32 · 6.9e-05 · 6.9e-05 |
| cir-in-squ n=20 | 4.489042 | ✓ 28/32 · 5.8e-06 · 5.8e-06 |
| cir-in-squ n=21 | 4.679010 | ✓ 22/32 · 9.0e-04 · 9.1e-04 |
| cir-in-squ n=22 | 4.731923 | 21/32 · 1.1e-04 · 1.3e-04 |
| cir-in-squ n=23 | 4.863703 | 0/32 · 0.0090 · 0.0843 |
| cir-in-squ n=24 | 4.931852 | ✓ 4/32 · 6.9e-07 · 0.0570 |
| cir-in-squ n=25 | 5.000000 | ✓ 30/32 · 1.9e-08 · 1.9e-08 |
| cir-in-squ n=26 | 5.188749 | 0/32 · 0.0023 · 0.0429 |
| cir-in-squ n=27 | 5.239992 | ✓ 0/32 · 0.0018 · 0.0591 |
| cir-in-squ n=28 | 5.337727 | ✓ 10/32 · 3.6e-04 · 0.0011 |
| cir-in-squ n=29 | 5.407560 | ✓ 0/32 · 0.0011 · 0.0015 |
| cir-in-squ n=30 | 5.454284 | ✓ 20/32 · 5.7e-06 · 5.7e-06 |
| hex-in-squ n=2 | 3.156597 | ✓ 32/32 · 6.3e-06 · 2.8e-05 |
| hex-in-squ n=3 | 3.491958 | ✓ 22/32 · 1.7e-06 · 1.8e-06 |
| hex-in-squ n=4 | 3.725003 | ✓ 22/32 · 8.4e-07 · 9.2e-07 |
| hex-in-squ n=6 | 4.813825 | ✓ 20/32 · 2.8e-06 · 3.0e-06 |
| hex-in-squ n=7 | 5.196152 | ✓ 32/32 · 7.0e-07 · 1.7e-06 |
| hex-in-squ n=8 | 5.196152 | ✓ 29/32 · 5.8e-07 · 9.9e-07 |
| hex-in-squ n=9 | 5.518154 | ✓ 24/32 · 1.3e-06 · 1.4e-06 |
| hex-in-squ n=10 | 6.104690 | 0/32 · 0.0013 · 0.0298 |
| hex-in-squ n=11 | 6.332180 | 0/32 · 0.0076 · 0.0076 |
| hex-in-squ n=12 | 6.387355 | ✓ 10/32 · 1.7e-06 · 0.0078 |
| hex-in-squ n=13 | 6.755490 | ✓ 17/32 · 2.1e-04 · 3.6e-04 |
| hex-in-squ n=14 | 6.928203 | ✓ 31/32 · 7.3e-07 · 1.6e-06 |
| hex-in-squ n=15 | 6.963670 | ✓ 32/32 · 3.5e-05 · 3.5e-05 |
| hex-in-squ n=16 | 7.311304 | ✓ 9/32 · 1.8e-06 · 0.0339 |
| hex-in-squ n=17 | 7.603830 | 0/32 · 0.0039 · 0.0203 |
| hex-in-squ n=18 | 7.702119 | ✓ 5/32 · 1.7e-06 · 0.1913 |
| hex-in-squ n=19 | 7.924682 | ✓ 11/32 · 3.0e-06 · 0.0103 |
| hex-in-squ n=20 | 7.948954 | ✓ 10/32 · 7.6e-06 · 0.0175 |
| squ-in-cir n=2 | 1.118034 | ✓ 32/32 · 1.8e-08 · 4.1e-08 |
| squ-in-cir n=3 | 1.288471 | ✓ 32/32 · 1.2e-07 · 1.6e-07 |
| squ-in-cir n=4 | 1.414214 | ✓ 32/32 · 1.4e-06 · 1.6e-06 |
| squ-in-cir n=5 | 1.581139 | ✓ 2/32 · 5.1e-07 · 0.0585 |
| squ-in-cir n=6 | 1.688000 | ✓ 15/32 · 5.4e-04 · 0.0122 |
| squ-in-cir n=7 | 1.802776 | ✓ 8/32 · 2.0e-07 · 0.0162 |
| squ-in-cir n=9 | 2.077596 | ✓ 20/32 · 1.0e-06 · 1.5e-06 |
| squ-in-cir n=10 | 2.121320 | ✓ 23/32 · 5.3e-07 · 6.4e-07 |
| squ-in-cir n=11 | 2.213860 | ✓ 6/32 · 2.5e-04 · 0.0019 |
| squ-in-cir n=12 | 2.236068 | 0/32 · 0.0910 · 0.1006 |
| squ-in-cir n=13 | 2.360700 | 6/32 · 2.8e-04 · 0.0081 |
| squ-in-cir n=14 | 2.500000 | 0/32 · 0.0045 · 0.0099 |
| squ-in-cir n=15 | 2.533000 | ✓ 1/32 · 8.6e-04 · 0.0079 |
| squ-in-cir n=16 | 2.623095 | 0/32 · 0.0093 · 0.0540 |
| squ-in-cir n=17 | 2.676870 | 2/32 · 7.4e-04 · 0.0136 |
| squ-in-cir n=18 | 2.741464 | ✓ 5/32 · 2.7e-06 · 0.0163 |
| squ-in-cir n=19 | 2.801500 | 0/32 · 0.0094 · 0.0519 |
| squ-in-cir n=20 | 2.893000 | 0/32 · 0.0049 · 0.0141 |
| squ-in-cir n=21 | 2.915476 | 0/32 · 0.0969 · 0.1134 |
| squ-in-cir n=22 | 3.032399 | 0/32 · 0.0063 · 0.0269 |
| squ-in-cir n=23 | 3.067380 | 0/32 · 0.0065 · 0.0459 |
| squ-in-cir n=24 | 3.109400 | 0/32 · 0.0026 · 0.0921 |
| squ-in-cir n=25 | 3.174503 | 0/32 · 0.0177 · 0.0400 |
| squ-in-cir n=26 | 3.201562 | 0/32 · 0.0260 · 0.0939 |
| squ-in-cir n=27 | 3.260500 | 0/32 · 0.0323 · 0.1102 |
| squ-in-cir n=28 | 3.331470 | 0/32 · 0.0112 · 0.0443 |
| squ-in-cir n=29 | 3.393090 | 0/32 · 0.0048 · 0.1431 |
| squ-in-cir n=30 | 3.459620 | 0/32 · 0.0128 · 0.0781 |
| squ-in-squ n=2 | 2.000000 | ✓ 32/32 · 3.4e-07 · 3.4e-07 |
| squ-in-squ n=3 | 2.000000 | ✓ 32/32 · 6.5e-07 · 1.3e-06 |
| squ-in-squ n=4 | 2.000000 | ✓ 32/32 · 8.5e-07 · 9.6e-07 |
| squ-in-squ n=5 | 2.707107 | ✓ 19/32 · 0 · 0 |
| squ-in-squ n=6 | 3.000000 | ✓ 32/32 · 5.6e-07 · 3.4e-06 |
| squ-in-squ n=7 | 3.000000 | ✓ 32/32 · 7.9e-07 · 2.3e-06 |
| squ-in-squ n=8 | 3.000000 | ✓ 32/32 · 9.0e-07 · 1.5e-06 |
| squ-in-squ n=9 | 3.000000 | ✓ 32/32 · 1.2e-06 · 1.3e-06 |
| squ-in-squ n=11 | 3.877084 | 0/32 · 0.0137 · 0.1229 |
| squ-in-squ n=12 | 4.000000 | ✓ 32/32 · 1.4e-06 · 4.0e-06 |
| squ-in-squ n=13 | 4.000000 | ✓ 31/32 · 1.7e-06 · 3.4e-06 |
| squ-in-squ n=14 | 4.000000 | ✓ 32/32 · 1.1e-06 · 2.3e-06 |
| squ-in-squ n=15 | 4.000000 | ✓ 32/32 · 1.2e-06 · 1.6e-06 |
| squ-in-squ n=16 | 4.000000 | ✓ 32/32 · 1.2e-06 · 1.4e-06 |
| squ-in-squ n=17 | 4.675530 | 0/32 · 0.0316 · 0.0317 |
| squ-in-squ n=18 | 4.822876 | ✓ 3/32 · 5.1e-05 · 0.1771 |
| squ-in-squ n=19 | 4.885618 | 0/32 · 0.1144 · 0.1144 |
| squ-in-squ n=20 | 5.000000 | ✓ 31/32 · 2.1e-06 · 4.6e-06 |
| squ-in-squ n=21 | 5.000000 | ✓ 32/32 · 2.4e-06 · 3.7e-06 |
| squ-in-squ n=22 | 5.000000 | ✓ 32/32 · 2.1e-06 · 3.3e-06 |
| squ-in-squ n=23 | 5.000000 | ✓ 32/32 · 1.5e-06 · 2.5e-06 |
| squ-in-squ n=24 | 5.000000 | ✓ 32/32 · 1.5e-06 · 1.7e-06 |
| squ-in-squ n=25 | 5.000000 | ✓ 31/32 · 1.2e-06 · 1.4e-06 |
| squ-in-squ n=26 | 5.621320 | ✓ 1/32 · 2.5e-04 · 0.1078 |
| squ-in-squ n=27 | 5.707107 | ✓ 1/32 · 1.8e-05 · 0.2601 |
| squ-in-squ n=28 | 5.824445 | 0/32 · 0.0572 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | 0/32 · 0.0662 · 0.0662 |
| squ-in-squ n=30 | 6.000000 | ✓ 29/32 · 3.5e-06 · 6.6e-06 |
| squ-in-tri n=2 | 3.154701 | ✓ 32/32 · 1.7e-07 · 4.9e-07 |
| squ-in-tri n=3 | 3.232051 | ✓ 13/32 · 3.3e-06 · 0.0774 |
| squ-in-tri n=4 | 4.154701 | ✓ 32/32 · 8.8e-08 · 6.1e-07 |
| squ-in-tri n=5 | 4.309401 | ✓ 32/32 · 1.0e-06 · 1.8e-06 |
| squ-in-tri n=6 | 4.309401 | ✓ 31/32 · 2.6e-06 · 3.0e-06 |
| squ-in-tri n=7 | 5.154701 | ✓ 32/32 · 8.6e-07 · 1.7e-06 |
| squ-in-tri n=8 | 5.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=9 | 5.309401 | ✓ 16/32 · 3.6e-06 · 0.0387 |
| squ-in-tri n=10 | 5.464102 | ✓ 31/32 · 4.2e-06 · 4.9e-06 |
| squ-in-tri n=11 | 6.154701 | ✓ 28/32 · 1.3e-06 · 3.4e-06 |
| squ-in-tri n=12 | 6.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=13 | 6.309401 | ✓ 14/32 · 3.9e-06 · 0.1160 |
| squ-in-tri n=14 | 6.464102 | ✓ 28/32 · 6.0e-06 · 7.1e-06 |
| squ-in-tri n=15 | 6.464102 | ✓ 8/32 · 3.9e-06 · 0.1547 |
| squ-in-tri n=16 | 7.154701 | ✓ 27/32 · 1.6e-06 · 5.1e-06 |
| squ-in-tri n=17 | 7.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=18 | 7.309401 | ✓ 11/32 · 4.4e-06 · 0.1547 |
| squ-in-tri n=19 | 7.464102 | ✓ 19/32 · 6.8e-06 · 9.0e-06 |
| squ-in-tri n=20 | 7.616955 | 0/32 · 0.0019 · 0.0019 |
| squ-in-tri n=21 | 7.618802 | ✓ 23/32 · 5.0e-06 · 7.6e-06 |
| squ-in-tri n=22 | 8.154701 | ✓ 27/32 · 3.2e-06 · 8.2e-06 |
| squ-in-tri n=23 | 8.301000 | 0/32 · 0.0084 · 0.0084 |
| squ-in-tri n=24 | 8.309401 | ✓ 6/32 · 4.6e-06 · 0.1547 |
| squ-in-tri n=25 | 8.464102 | ✓ 12/32 · 7.2e-06 · 0.1547 |
| squ-in-tri n=26 | 8.608050 | 0/32 · 0.0108 · 0.0108 |
| squ-in-tri n=27 | 8.618802 | ✓ 3/32 · 6.4e-06 · 0.1547 |
| squ-in-tri n=28 | 8.773503 | ✓ 19/32 · 9.1e-06 · 8.1e-05 |
| squ-in-tri n=29 | 9.154701 | ✓ 28/32 · 4.5e-06 · 8.6e-06 |
| squ-in-tri n=30 | 9.301000 | 0/32 · 0.0084 · 0.0084 |
| tri-in-squ n=2 | 1.224745 | ✓ 32/32 · 1.7e-07 · 4.8e-07 |
| tri-in-squ n=3 | 1.478398 | ✓ 32/32 · 1.2e-06 · 1.3e-06 |
| tri-in-squ n=4 | 1.577350 | ✓ 25/32 · 1.1e-06 · 1.1e-06 |
| tri-in-squ n=6 | 1.901924 | ✓ 5/32 · 2.6e-06 · 0.0180 |
| tri-in-squ n=7 | 2.000000 | ✓ 15/32 · 2.8e-06 · 0.0473 |
| tri-in-squ n=8 | 2.098076 | ✓ 13/32 · 1.2e-06 · 0.0621 |
| tri-in-squ n=9 | 2.287000 | ✓ 2/32 · 5.1e-04 · 0.0272 |
| tri-in-squ n=10 | 2.377000 | ✓ 4/32 · 2.6e-05 · 0.0271 |
| tri-in-squ n=11 | 2.490000 | ✓ 0/32 · 0.0051 · 0.0399 |
| tri-in-squ n=12 | 2.558000 | 0/32 · 0.0118 · 0.0191 |
| tri-in-squ n=13 | 2.595000 | ✓ 6/32 · 6.4e-04 · 0.0802 |
| tri-in-squ n=14 | 2.726000 | ✓ 5/32 · 2.0e-04 · 0.0678 |
| tri-in-squ n=15 | 2.829890 | ✓ 4/32 · 6.2e-05 · 0.0272 |
| tri-in-squ n=16 | 2.900000 | ✓ 4/32 · 5.4e-04 · 0.0720 |
| tri-in-squ n=17 | 2.982000 | 0/32 · 0.0157 · 0.0696 |
| tri-in-squ n=18 | 3.051000 | ✓ 2/32 · 8.6e-04 · 0.0797 |
| tri-in-squ n=19 | 3.129290 | ✓ 0/32 · 0.0014 · 0.0934 |
| tri-in-squ n=20 | 3.230500 | ✓ 0/32 · 0.0015 · 0.0753 |
| tri-in-squ n=21 | 3.311020 | 0/32 · 0.0100 · 0.0568 |
| tri-in-squ n=22 | 3.375700 | 0/32 · 0.0035 · 0.0482 |
| tri-in-squ n=23 | 3.431100 | 0/32 · 0.0119 · 0.0802 |
| tri-in-squ n=24 | 3.467800 | 0/32 · 0.0193 · 0.0910 |
| tri-in-squ n=25 | 3.537000 | 0/32 · 0.0016 · 0.0902 |
| tri-in-squ n=26 | 3.575000 | 0/32 · 0.0127 · 0.1381 |
| tri-in-squ n=27 | 3.672600 | 0/32 · 0.0311 · 0.1203 |
| tri-in-squ n=28 | 3.757070 | 0/32 · 0.0090 · 0.1049 |
| tri-in-squ n=29 | 3.817110 | 0/32 · 0.0471 · 0.1147 |
| tri-in-squ n=30 | 3.866190 | 0/32 · 0.0454 · 0.1134 |
| tri-in-tri n=2 | 2.000000 | ✓ 32/32 · 4.8e-07 · 3.0e-06 |
| tri-in-tri n=3 | 2.000000 | ✓ 32/32 · 2.3e-06 · 3.7e-06 |
| tri-in-tri n=4 | 2.000000 | ✓ 32/32 · 2.4e-06 · 2.5e-06 |
| tri-in-tri n=5 | 2.732051 | ✓ 32/32 · 1.0e-05 · 1.1e-05 |
| tri-in-tri n=7 | 3.000000 | ✓ 32/32 · 4.1e-06 · 5.6e-06 |
| tri-in-tri n=8 | 3.000000 | ✓ 29/32 · 3.4e-06 · 4.9e-06 |
| tri-in-tri n=9 | 3.000000 | ✓ 21/32 · 3.1e-06 · 3.5e-06 |
| tri-in-tri n=10 | 3.500000 | ✓ 31/32 · 3.5e-06 · 9.2e-06 |
| tri-in-tri n=11 | 3.722971 | ✓ 0/32 · 0.0050 · 0.0050 |
| tri-in-tri n=12 | 3.879385 | ✓ 3/32 · 1.3e-05 · 0.0275 |
| tri-in-tri n=13 | 3.992000 | 0/32 · 0.0063 · 0.0080 |
| tri-in-tri n=14 | 4.000000 | ✓ 32/32 · 5.2e-06 · 7.0e-06 |
| tri-in-tri n=15 | 4.000000 | ✓ 26/32 · 4.9e-06 · 6.2e-06 |
| tri-in-tri n=16 | 4.000000 | ✓ 16/32 · 4.5e-06 · 0.1830 |
| tri-in-tri n=17 | 4.465000 | 0/32 · 0.0350 · 0.0350 |
| tri-in-tri n=18 | 4.500000 | ✓ 19/32 · 5.3e-06 · 6.6e-06 |
| tri-in-tri n=19 | 4.666667 | ✓ 14/32 · 9.6e-06 · 0.0833 |
| tri-in-tri n=20 | 4.861485 | ✓ 0/32 · 0.0019 · 0.0313 |
| tri-in-tri n=21 | 4.923000 | 0/32 · 0.0311 · 0.0768 |
| tri-in-tri n=22 | 4.996000 | 0/32 · 0.0039 · 0.0040 |
| tri-in-tri n=23 | 5.000000 | ✓ 27/32 · 5.1e-06 · 7.5e-06 |
| tri-in-tri n=24 | 5.000000 | ✓ 19/32 · 5.9e-06 · 7.2e-06 |
| tri-in-tri n=25 | 5.000000 | ✓ 1/32 · 5.9e-06 · 0.4629 |
| tri-in-tri n=26 | 5.406000 | 0/32 · 0.0229 · 0.0951 |
| tri-in-tri n=27 | 5.500000 | ✓ 8/32 · 7.4e-06 · 0.1470 |
| tri-in-tri n=28 | 5.500000 | ✓ 2/32 · 5.9e-06 · 0.1679 |
| tri-in-tri n=29 | 5.666667 | ✓ 2/32 · 5.8e-06 · 0.1836 |
| tri-in-tri n=30 | 5.750000 | ✓ 2/32 · 9.1e-06 · 0.1705 |

