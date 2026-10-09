# C15-heldout-decision: Does choosing the path pay on families never used before?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** C07-C13 show that the better path depends on the family, but that was learned on seven families. Here four families never used to develop, tune or analyse any method (pentagons in a square, octagons in a square, hexagons in a triangle, triangles in a circle; n = 6..20; best known values parsed from Friedman's captions at a pinned commit) test a decision procedure rather than a description. Each instance gets 64 harden-best and 64 rigid-best runs at budget 1, with the frozen C06 settings, from which three policies of 64 runs each are formed: always-rigid (rigid seeds 1-64), always-harden (harden seeds 1-64), and pilot (harden seeds 1-8 and rigid seeds 1-8, then seeds 9-56 of the path whose pilot reached the lower legalised size; ties go to rigid).

**Hypothesis.** From the mechanism hypotheses in the paper (orientation matters late; odd and near-round pieces gain nothing): pentagons and triangles in a circle favour rigid starts or tie; octagons and hexagons in a triangle mostly tie. The pilot policy is at least as good as always-rigid.

**Decision rule (pre-registered 2026-10-09).** Primary: pilot vs always-rigid, counting instances where each policy's result is strictly lower (relative 1e-9); exact two-sided sign test. If the pilot is lower on more instances with p < 0.05, the paper reports path choice by pilot as a method that transfers to new families; if p >= 0.05, it reports no detected benefit (not equivalence); if always-rigid is lower with p < 0.05, it reports that the pilot costs more than it gains. Secondary, descriptive: per family, always-harden vs always-rigid counts, compared with the hypotheses above; the number of instances on which the pilot picked harden; reached counts per policy.

**Status.** closed — **decision:** Per the rule: pilot vs always-rigid 2 vs 3, p = 1 >= 0.05, so the paper reports no detected benefit from choosing the path by pilot on held-out families (not equivalence). Secondary hypotheses: pentagons favour rigid (confirmed, 1 vs 8); octagons and hexagons in a triangle mostly tie (12 and 13 ties of 15, remaining instances favour rigid); triangles in a circle rigid or tie (2 vs 4, 9 ties).

## Findings

- Held-out families (pentagons and octagons in a square, hexagons in a triangle, triangles in a circle; n = 6-20; 60 instances; 64 runs per policy). Pilot (8 harden + 8 rigid runs, then 48 on the pilot winner) vs always-rigid: lower on 2 vs 3 instances, 55 ties (two-sided p = 1). Always-harden vs always-rigid: 3 vs 17 (p = 0.0026); pentagons 1 vs 8. Pilot vs always-harden: 14 vs 2. Best known reached: rigid 40, harden 32, pilot 41. The pilot picked harden on 20 of 60 instances. Hardening helps on none of these families; the pilot avoids its losses but does not beat always-rigid.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

| instance | best known | harden-best | rigid-best |
|---|---|---|---|
| hex-in-tri n=6 | 6.898970 | ✓ 0/64 · 0.0254 · 0.0279 | ✓ 0/64 · 0.0260 · 0.0277 |
| hex-in-tri n=7 | 8.000000 | ✓ 64/64 · 8.8e-06 · 1.2e-05 | ✓ 64/64 · 1.6e-06 · 1.2e-05 |
| hex-in-tri n=8 | 8.333300 | 0/64 · 0.1308 · 0.1308 | ✓ 8/64 · 3.8e-05 · 0.1308 |
| hex-in-tri n=9 | 8.644940 | ✓ 0/64 · 0.0152 · 0.0153 | ✓ 0/64 · 0.0152 · 0.0153 |
| hex-in-tri n=10 | 8.660200 | ✓ 64/64 · 5.7e-05 · 5.9e-05 | ✓ 64/64 · 5.7e-05 · 5.9e-05 |
| hex-in-tri n=11 | 9.548230 | 0/64 · 0.0052 · 0.0052 | 0/64 · 0.0052 · 0.0052 |
| hex-in-tri n=12 | 9.964290 | ✓ 55/64 · 2.8e-05 · 2.8e-05 | ✓ 47/64 · 2.8e-05 · 2.9e-05 |
| hex-in-tri n=13 | 10.288570 | 0/64 · 0.0057 · 0.1037 | 0/64 · 0.0057 · 0.1037 |
| hex-in-tri n=14 | 10.392300 | ✓ 59/64 · 9.2e-06 · 1.3e-05 | ✓ 58/64 · 9.0e-06 · 1.3e-05 |
| hex-in-tri n=15 | 10.392300 | ✓ 64/64 · 9.2e-06 · 1.0e-05 | ✓ 64/64 · 9.1e-06 · 1.0e-05 |
| hex-in-tri n=16 | 11.363830 | ✓ 12/64 · 5.6e-04 · 0.1003 | ✓ 12/64 · 5.3e-04 · 0.1003 |
| hex-in-tri n=17 | 11.634530 | 0/64 · 0.1682 · 0.1685 | 0/64 · 0.1618 · 0.1720 |
| hex-in-tri n=18 | 11.914210 | 0/64 · 0.0405 · 0.0407 | 0/64 · 0.0407 · 0.0407 |
| hex-in-tri n=19 | 12.000000 | 0/64 · 0.1236 · 0.1244 | 0/64 · 0.1206 · 0.1244 |
| hex-in-tri n=20 | 12.124300 | ✓ 56/64 · 6.0e-05 · 6.2e-05 | ✓ 59/64 · 6.0e-05 · 6.2e-05 |
| oct-in-squ n=6 | 6.511260 | ✓ 55/64 · 1.1e-05 · 1.1e-05 | ✓ 45/64 · 1.1e-05 · 1.1e-05 |
| oct-in-squ n=7 | 7.035530 | ✓ 60/64 · 4.5e-06 · 4.7e-06 | ✓ 59/64 · 4.5e-06 · 4.7e-06 |
| oct-in-squ n=8 | 7.242640 | ✓ 64/64 · 1.1e-06 · 1.5e-06 | ✓ 64/64 · 1.2e-06 · 1.5e-06 |
| oct-in-squ n=9 | 7.242640 | ✓ 64/64 · 9.6e-07 · 1.2e-06 | ✓ 64/64 · 9.2e-07 · 1.2e-06 |
| oct-in-squ n=10 | 8.242640 | ✓ 64/64 · 2.1e-06 · 3.2e-06 | ✓ 64/64 · 2.0e-06 · 3.2e-06 |
| oct-in-squ n=11 | 8.575960 | 0/64 · 0.0202 · 0.0202 | 2/64 · 1.9e-05 · 0.0202 |
| oct-in-squ n=12 | 8.815860 | 0/64 · 0.0402 · 0.0525 | ✓ 44/64 · 4.5e-06 · 4.6e-06 |
| oct-in-squ n=13 | 9.199090 | 18/64 · 2.9e-04 · 0.0151 | 41/64 · 2.9e-04 · 2.9e-04 |
| oct-in-squ n=14 | 9.449740 | ✓ 5/64 · 9.8e-06 · 0.2071 | ✓ 7/64 · 9.8e-06 · 0.2071 |
| oct-in-squ n=15 | 9.656850 | ✓ 64/64 · 4.8e-06 · 5.3e-06 | ✓ 64/64 · 4.8e-06 · 5.3e-06 |
| oct-in-squ n=16 | 9.656850 | ✓ 63/64 · 4.6e-06 · 4.8e-06 | ✓ 62/64 · 4.6e-06 · 4.8e-06 |
| oct-in-squ n=17 | 10.449730 | 54/64 · 1.9e-05 · 1.9e-05 | 53/64 · 1.9e-05 · 1.9e-05 |
| oct-in-squ n=18 | 10.608320 | ✓ 35/64 · 6.7e-06 · 6.9e-06 | ✓ 32/64 · 6.7e-06 · 0.0822 |
| oct-in-squ n=19 | 10.966200 | 0/64 · 0.0126 · 0.0645 | 0/64 · 0.0113 · 0.0218 |
| oct-in-squ n=20 | 11.104930 | 0/64 · 0.0269 · 0.0463 | ✓ 9/64 · 9.6e-06 · 0.0315 |
| pen-in-squ n=6 | 3.882990 | ✓ 26/64 · 3.6e-06 · 0.0130 | ✓ 26/64 · 3.6e-06 · 0.0059 |
| pen-in-squ n=7 | 4.180370 | ✓ 38/64 · 2.2e-06 · 2.5e-06 | ✓ 11/64 · 2.2e-06 · 0.0016 |
| pen-in-squ n=8 | 4.381900 | 0/64 · 0.0022 · 0.0399 | ✓ 4/64 · 1.3e-05 · 0.0399 |
| pen-in-squ n=9 | 4.600320 | 0/64 · 0.0155 · 0.0214 | ✓ 12/64 · 1.4e-05 · 0.0175 |
| pen-in-squ n=10 | 4.905810 | 0/64 · 0.0022 · 0.0879 | 0/64 · 0.0016 · 0.0882 |
| pen-in-squ n=11 | 5.115550 | 27/64 · 1.6e-05 · 0.0067 | 39/64 · 1.5e-05 · 3.0e-05 |
| pen-in-squ n=12 | 5.232210 | ✓ 44/64 · 2.4e-04 · 2.4e-04 | ✓ 28/64 · 2.4e-04 · 0.0273 |
| pen-in-squ n=13 | 5.521020 | 0/64 · 0.0021 · 0.0282 | ✓ 0/64 · 0.0011 · 0.0083 |
| pen-in-squ n=14 | 5.696590 | 1/64 · 4.3e-04 · 0.0531 | 2/64 · 4.2e-04 · 0.0484 |
| pen-in-squ n=15 | 5.901180 | 0/64 · 0.0074 · 0.0158 | 0/64 · 0.0022 · 0.0112 |
| pen-in-squ n=16 | 6.064510 | 0/64 · 0.0559 · 0.0835 | 0/64 · 0.0339 · 0.0632 |
| pen-in-squ n=17 | 6.237610 | 0/64 · 0.0272 · 0.0346 | 0/64 · 0.0064 · 0.0415 |
| pen-in-squ n=18 | 6.325650 | ✓ 1/64 · 1.0e-05 · 0.0214 | ✓ 4/64 · 1.0e-05 · 0.0145 |
| pen-in-squ n=19 | 6.557810 | 0/64 · 0.0094 · 0.0306 | ✓ 1/64 · 3.2e-04 · 0.0245 |
| pen-in-squ n=20 | 6.661350 | 1/64 · 2.9e-04 · 0.0696 | ✓ 1/64 · 3.5e-04 · 0.0330 |
| tri-in-cir n=6 | 1.000000 | ✓ 9/64 · 3.5e-07 · 0.2269 | ✓ 43/64 · 3.4e-07 · 3.9e-07 |
| tri-in-cir n=7 | 1.152000 | 0/64 · 0.0743 · 0.1072 | ✓ 6/64 · 3.8e-04 · 0.0746 |
| tri-in-cir n=8 | 1.263000 | ✓ 35/64 · 3.7e-04 · 9.5e-04 | ✓ 44/64 · 3.6e-04 · 5.5e-04 |
| tri-in-cir n=9 | 1.314000 | ✓ 47/64 · 7.7e-04 · 7.7e-04 | ✓ 45/64 · 7.7e-04 · 7.7e-04 |
| tri-in-cir n=10 | 1.384680 | ✓ 23/64 · 8.8e-05 · 0.0109 | ✓ 29/64 · 9.4e-05 · 0.0010 |
| tri-in-cir n=11 | 1.466000 | ✓ 1/64 · 1.0e-03 · 0.0060 | ✓ 0/64 · 0.0010 · 0.0050 |
| tri-in-cir n=12 | 1.507000 | ✓ 26/64 · 2.1e-04 · 0.0018 | ✓ 20/64 · 3.1e-04 · 0.0042 |
| tri-in-cir n=13 | 1.527000 | ✓ 2/64 · 5.3e-04 · 0.0676 | ✓ 4/64 · 5.3e-04 · 0.0649 |
| tri-in-cir n=14 | 1.604480 | ✓ 6/64 · 2.4e-05 · 0.0282 | ✓ 7/64 · 2.4e-05 · 0.0265 |
| tri-in-cir n=15 | 1.636000 | ✓ 0/64 · 0.0012 · 0.0782 | 0/64 · 0.0013 · 0.0621 |
| tri-in-cir n=16 | 1.687000 | 0/64 · 0.0173 · 0.0579 | 0/64 · 0.0028 · 0.0521 |
| tri-in-cir n=17 | 1.730000 | 0/64 · 0.0111 · 0.0728 | ✓ 3/64 · 4.9e-04 · 0.0695 |
| tri-in-cir n=18 | 1.801760 | 0/64 · 0.0010 · 0.0399 | 0/64 · 0.0010 · 0.0360 |
| tri-in-cir n=19 | 1.825000 | ✓ 2/64 · 7.4e-04 · 0.0689 | 0/64 · 0.0216 · 0.0537 |
| tri-in-cir n=20 | 1.874000 | 0/64 · 0.0080 · 0.0710 | ✓ 1/64 · 3.9e-04 · 0.0541 |

