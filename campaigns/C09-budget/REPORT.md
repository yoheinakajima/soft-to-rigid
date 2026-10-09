# C09-budget: Does a longer schedule change which path finds the lowest point?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** On the contested instances, give harden-best and rigid-best 3x and 10x the budget (32 runs each). Does the gap between the paths close, persist, or reverse with more time, and does either path find a packing below a published value?

**Hypothesis.** More time lowers both paths' lowest points; the path that wins at budget 1 on an instance still wins at budget 10 on most instances.

**Decision rule (pre-registered 2026-10-08).** The 20 most contested of C08's instances (largest relative differences). Metric: lowest tightened size over 32 runs per instance, method and budget. Report the per-budget count of instances where each path is lowest, and certify anything below a catalogue value.

**Status.** closed — **decision:** Hypothesis partly supported: rigid's wins at budget 1 mostly persist, but harden closes the gap with more time (3 -> 9 instances lowest). Instances were chosen where the paths differed, mostly in rigid's favour, so part of the change may be regression toward even.

## Findings

- Longer schedules on the 20 most contested instances: harden is lowest on 3, 5 and 9 instances at budget 1, 3 and 10, rigid on 17, 16 and 16; harden reaches the best known value on 1, 2 and 6, rigid on 10, 10 and 9. Hardening gains more from time. At budget 10 harden reaches Schadt's squares-in-square n = 29 packing (5.933833) and Wainwright's n = 19 in 11 of 16 runs; both paths tighten to 3.1292935 for triangles in a square n = 19 (catalogue 3.12929+) and harden to 3.6726370 for n = 27 (3.6726+), both consistent with the catalogue to its printed precision. Nothing below a published value.
- Precision note on the C09 finding: at budget 10, 11 of 16 harden runs for squares-in-square n = 19 come within 1e-4 of Wainwright's value before tightening; the three that were tightened all match it to 1e-14. Both runs tightened at n = 29 match Schadt's 5.933833462677 to 1e-12.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 3, setting `default`

| instance | best known | harden-best | rigid-best |
|---|---|---|---|
| squ-in-cir n=5 | 1.581139 | 0/16 · 0.0567 · 0.0584 | ✓ 1/16 · 4.9e-07 · 0.0575 |
| squ-in-cir n=12 | 2.236068 | 0/16 · 0.0968 · 0.0996 | ✓ 1/16 · 3.4e-06 · 0.0980 |
| squ-in-cir n=19 | 2.801500 | 0/16 · 0.0269 · 0.0487 | 0/16 · 0.0425 · 0.0477 |
| squ-in-cir n=21 | 2.915476 | 0/16 · 0.1079 · 0.1140 | 0/16 · 0.1011 · 0.1098 |
| squ-in-squ n=19 | 4.885618 | ✓ 7/16 · 1.8e-04 · 0.0014 | 0/16 · 0.1144 · 0.1144 |
| squ-in-squ n=28 | 5.824445 | 0/16 · 0.0054 · 0.0564 | 0/16 · 0.1756 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | 0/16 · 0.0230 · 0.0662 | 0/16 · 0.0662 · 0.0662 |
| squ-in-tri n=24 | 8.309401 | ✓ 2/16 · 5.0e-06 · 0.1547 | ✓ 5/16 · 4.4e-06 · 0.1547 |
| tri-in-squ n=9 | 2.287000 | 0/16 · 0.0252 · 0.0588 | ✓ 2/16 · 5.1e-04 · 0.0065 |
| tri-in-squ n=16 | 2.900000 | 0/16 · 0.0530 · 0.1003 | 4/16 · 2.6e-04 · 0.0726 |
| tri-in-squ n=19 | 3.129290 | 0/16 · 0.0497 · 0.0979 | ✓ 3/16 · 1.8e-04 · 0.0695 |
| tri-in-squ n=24 | 3.467800 | 0/16 · 0.0509 · 0.1127 | 0/16 · 0.0150 · 0.0479 |
| tri-in-squ n=26 | 3.575000 | 0/16 · 0.0720 · 0.1726 | 0/16 · 0.0153 · 0.1061 |
| tri-in-squ n=27 | 3.672600 | 0/16 · 0.0435 · 0.1199 | ✓ 1/16 · 4.6e-05 · 0.0851 |
| tri-in-squ n=29 | 3.817110 | 0/16 · 0.0158 · 0.0789 | 0/16 · 0.0147 · 0.0507 |
| tri-in-squ n=30 | 3.866190 | 0/16 · 0.0610 · 0.1177 | 0/16 · 0.0346 · 0.0707 |
| tri-in-tri n=12 | 3.879385 | 0/16 · 0.0443 · 0.1144 | ✓ 4/16 · 1.2e-05 · 0.0062 |
| tri-in-tri n=25 | 5.000000 | 0/16 · 0.3544 · 0.4992 | ✓ 5/16 · 5.2e-06 · 0.3333 |
| tri-in-tri n=28 | 5.500000 | 0/16 · 0.1667 · 0.2485 | ✓ 3/16 · 5.7e-06 · 0.1667 |
| tri-in-tri n=30 | 5.750000 | 0/16 · 0.0972 · 0.2337 | ✓ 1/16 · 9.2e-06 · 0.1661 |

### budget 10, setting `default`

| instance | best known | harden-best | rigid-best |
|---|---|---|---|
| squ-in-cir n=5 | 1.581139 | 0/16 · 0.0567 · 0.0583 | 0/16 · 0.0567 · 0.0567 |
| squ-in-cir n=12 | 2.236068 | 0/16 · 0.0906 · 0.0998 | ✓ 1/16 · 6.2e-07 · 0.0977 |
| squ-in-cir n=19 | 2.801500 | 0/16 · 0.0269 · 0.0462 | 0/16 · 0.0075 · 0.0269 |
| squ-in-cir n=21 | 2.915476 | 0/16 · 0.1009 · 0.1081 | 0/16 · 0.1009 · 0.1090 |
| squ-in-squ n=19 | 4.885618 | ✓ 12/16 · 2.9e-05 · 3.0e-05 | 0/16 · 0.1144 · 0.1144 |
| squ-in-squ n=28 | 5.824445 | 0/16 · 0.0426 · 0.0441 | 0/16 · 0.0735 · 0.1756 |
| squ-in-squ n=29 | 5.933833 | ✓ 2/16 · 2.5e-05 · 0.0564 | 0/16 · 0.0662 · 0.0662 |
| squ-in-tri n=24 | 8.309401 | ✓ 1/16 · 5.1e-06 · 0.1547 | ✓ 10/16 · 4.4e-06 · 5.4e-06 |
| tri-in-squ n=9 | 2.287000 | 0/16 · 0.0290 · 0.0572 | ✓ 2/16 · 5.1e-04 · 0.0084 |
| tri-in-squ n=16 | 2.900000 | 1/16 · 2.4e-04 · 0.0892 | 10/16 · 2.4e-04 · 7.8e-04 |
| tri-in-squ n=19 | 3.129290 | ✓ 1/16 · 1.5e-05 · 0.0994 | ✓ 4/16 · 1.4e-05 · 0.0590 |
| tri-in-squ n=24 | 3.467800 | 0/16 · 0.0321 · 0.0649 | 0/16 · 0.0141 · 0.0401 |
| tri-in-squ n=26 | 3.575000 | 0/16 · 0.0066 · 0.0922 | 0/16 · 0.0021 · 0.0449 |
| tri-in-squ n=27 | 3.672600 | ✓ 3/16 · 4.6e-05 · 0.0693 | ✓ 5/16 · 4.5e-05 · 0.0291 |
| tri-in-squ n=29 | 3.817110 | 0/16 · 0.0155 · 0.0719 | 0/16 · 0.0086 · 0.0320 |
| tri-in-squ n=30 | 3.866190 | 0/16 · 0.0285 · 0.0584 | 0/16 · 0.0062 · 0.0432 |
| tri-in-tri n=12 | 3.879385 | 0/16 · 0.0062 · 0.0881 | ✓ 2/16 · 1.2e-05 · 0.0062 |
| tri-in-tri n=25 | 5.000000 | ✓ 2/16 · 5.3e-06 · 0.4085 | ✓ 12/16 · 4.8e-06 · 5.3e-06 |
| tri-in-tri n=28 | 5.500000 | 0/16 · 0.1602 · 0.1667 | ✓ 5/16 · 4.5e-06 · 0.1667 |
| tri-in-tri n=30 | 5.750000 | 0/16 · 0.0833 · 0.1869 | ✓ 11/16 · 8.3e-06 · 9.1e-06 |

