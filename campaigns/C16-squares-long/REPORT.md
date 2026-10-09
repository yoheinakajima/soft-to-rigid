# C16-squares-long: Squares in a square at ten times the budget

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Hardening's clearest advantage is on squares in a square, and the hardest instances are n >= 17. Here all five tuned methods get ten times the base budget (sa and pc matched to a hardening run at that budget, as in C07) on n = 17..30, 16 runs each, to see whether hardening reaches packings none of the others reach when every method has more time.

**Hypothesis.** Hardening is the only method to reach the lowest size on at least one instance; no run goes below a catalogue value.

**Decision rule (pre-registered 2026-10-09).** Same metric and tightening policy as C07. Report per method the instances where its lowest size is the lowest of all five and where it is the only one that low, reached counts, and the exact two-sided sign test of harden vs rigid on instances where exactly one is lower. Any tightened packing below a catalogue value is certified (float and exact) before it is mentioned.

**Status.** closed — **decision:** Hypothesis confirmed: hardening is the only method to reach the lowest size on five instances (17, 19, 26, 28, 29); no run went below a catalogue value, so nothing to certify. Harden vs rigid 6 vs 0, p = 0.031.

## Findings

- Squares in a square, n = 17-30, ten times the base budget, 16 runs per method. Lowest of all five: harden 13 of 14, sa 9, rigid 8, grow 7, pc 6; harden is the only method that low on n = 17, 19, 26, 28, 29 (sa alone on 27). Best known value reached: harden 12, sa 9, rigid 8, grow 7, pc 6. Harden vs rigid lower 6 vs 0 (two-sided p = 0.031). No run below a catalogue value.
- Disclosure (after independent check): C16's harden-best and rigid-best runs at n = 19, 28 and 29 (budget 10, seeds 1-16) are identical to C09's, because runs are deterministic in seed and budget; they repeat C09 rather than add evidence at those instances. C16 was planned after C07 and C09 to confirm an advantage already seen on squares in a square. New evidence in C16 is n = 17 and 26 (hardening alone reaches the best known packing) and the three other methods at every n.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

| instance | best known | grow-best | harden-best | pc-best | rigid-best | sa-best |
|---|---|---|---|---|---|---|
| squ-in-squ n=17 | 4.675530 | 0/16 · 0.3245 · 0.3245 | ✓ 2/16 · 4.1e-06 · 0.0316 | 0/16 · 0.0940 · 0.3283 | 0/16 · 0.0316 · 0.3245 | 0/16 · 0.0352 · 0.3285 |
| squ-in-squ n=18 | 4.822876 | 0/16 · 0.1771 · 0.1771 | ✓ 2/16 · 1.1e-05 · 0.0057 | 0/16 · 0.0189 · 0.1798 | ✓ 1/16 · 3.3e-06 · 0.1771 | ✓ 0/16 · 0.0079 · 0.1802 |
| squ-in-squ n=19 | 4.885618 | 0/16 · 0.1144 · 0.1144 | 12/16 · 2.9e-05 · 3.0e-05 | 0/16 · 0.1146 · 0.1215 | 0/16 · 0.1144 · 0.1144 | 0/16 · 0.1157 · 0.1201 |
| squ-in-squ n=20 | 5.000000 | ✓ 16/16 · 2.4e-07 · 1.4e-06 | ✓ 16/16 · 1.3e-06 · 3.9e-06 | ✓ 0/16 · 0.0016 · 0.0174 | ✓ 16/16 · 8.6e-07 · 3.1e-06 | ✓ 0/16 · 0.0035 · 0.0069 |
| squ-in-squ n=21 | 5.000000 | ✓ 16/16 · 9.1e-07 · 1.5e-06 | ✓ 15/16 · 2.8e-06 · 3.3e-06 | ✓ 0/16 · 0.0063 · 0.3538 | ✓ 16/16 · 2.2e-06 · 3.8e-06 | ✓ 0/16 · 0.0061 · 0.0126 |
| squ-in-squ n=22 | 5.000000 | ✓ 16/16 · 1.0e-06 · 1.3e-06 | ✓ 16/16 · 2.6e-06 · 7.7e-06 | ✓ 0/16 · 0.0046 · 0.4827 | ✓ 16/16 · 2.0e-06 · 2.7e-06 | ✓ 0/16 · 0.0065 · 0.0177 |
| squ-in-squ n=23 | 5.000000 | ✓ 16/16 · 7.3e-07 · 1.2e-06 | ✓ 16/16 · 2.2e-06 · 2.8e-06 | ✓ 0/16 · 0.0065 · 0.9480 | ✓ 16/16 · 1.4e-06 · 2.4e-06 | ✓ 0/16 · 0.0071 · 0.0124 |
| squ-in-squ n=24 | 5.000000 | ✓ 16/16 · 6.9e-07 · 7.9e-07 | ✓ 16/16 · 1.6e-06 · 2.1e-06 | ✓ 0/16 · 0.0119 · 0.9264 | ✓ 16/16 · 1.5e-06 · 1.7e-06 | ✓ 0/16 · 0.0070 · 0.0106 |
| squ-in-squ n=25 | 5.000000 | ✓ 16/16 · 6.0e-07 · 6.7e-07 | ✓ 16/16 · 1.3e-06 · 1.4e-06 | 0/16 · 0.7557 · 1.0062 | ✓ 16/16 · 1.2e-06 · 1.4e-06 | ✓ 0/16 · 0.0080 · 0.0105 |
| squ-in-squ n=26 | 5.621320 | 0/16 · 0.3787 · 0.3787 | ✓ 10/16 · 5.8e-06 · 6.7e-06 | 0/16 · 0.2077 · 0.3877 | 0/16 · 0.3787 · 0.3787 | 0/16 · 0.0898 · 0.2515 |
| squ-in-squ n=27 | 5.707107 | 0/16 · 0.2929 · 0.2929 | 0/16 · 0.0989 · 0.1173 | 0/16 · 0.2939 · 0.3037 | 0/16 · 0.1386 · 0.2929 | ✓ 0/16 · 0.0056 · 0.2981 |
| squ-in-squ n=28 | 5.824445 | 0/16 · 0.1756 · 0.1756 | 0/16 · 0.0426 · 0.0441 | 0/16 · 0.1791 · 0.2014 | 0/16 · 0.0735 · 0.1756 | 0/16 · 0.1779 · 0.1821 |
| squ-in-squ n=29 | 5.933833 | 0/16 · 0.0662 · 0.0662 | 2/16 · 2.5e-05 · 0.0564 | 0/16 · 0.0694 · 0.5358 | 0/16 · 0.0662 · 0.0662 | 0/16 · 0.0686 · 0.0730 |
| squ-in-squ n=30 | 6.000000 | ✓ 16/16 · 7.1e-07 · 1.7e-06 | ✓ 16/16 · 1.8e-06 · 1.6e-05 | ✓ 0/16 · 0.0085 · 0.1760 | ✓ 16/16 · 2.7e-06 · 4.6e-06 | ✓ 0/16 · 0.0046 · 0.0071 |

