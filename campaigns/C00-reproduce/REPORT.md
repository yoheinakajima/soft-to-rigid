# C00-reproduce: Does the new general engine reproduce the earlier squares results?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** The 2D engine was rewritten for any regular polygon and container. Before using it, check it against the earlier square-only simulator on the cases reported in soft-to-rigid-packing (squares in a square, n = 11 and 17).

**Hypothesis.** harden reaches Trump's n = 11 packing in a few percent of starts at budget 3 and the rigid control does not; neither reaches Bidwell's n = 17 at budget 1.

**Decision rule (pre-registered 2026-10-08).** Proceed if harden hits n = 11 (gap < 1e-3) in at least 2 of 80 starts at B = 3 and its median gap at n = 11 is below rigid's. Otherwise debug the engine before any other campaign.

**Status.** closed — **decision:** Decision rule met (4/80 >= 2; harden median gap 0.054 < rigid 0.123). Engine accepted.

## Findings

- The general 2D engine reproduces the earlier square-only results: at squares-in-square n = 11, harden reaches Trump's packing in 1/80 starts at budget 1 and 4/80 at budget 3 (all four tighten to the record within 1e-14); the untuned rigid control reaches it in 0/160. Neither reaches Bidwell's n = 17 at these budgets.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 1, setting `default`

| instance | best known | harden | rigid |
|---|---|---|---|
| squ-in-squ n=11 | 3.877084 | ✓ 1/80 · 7.9e-07 · 0.0637 | 0/80 · 0.0107 · 0.1229 |
| squ-in-squ n=17 | 4.675530 | 0/80 · 0.0097 · 0.0925 | 0/80 · 0.0316 · 0.3245 |

### budget 3, setting `default`

| instance | best known | harden | rigid |
|---|---|---|---|
| squ-in-squ n=11 | 3.877084 | ✓ 4/80 · 3.5e-07 · 0.0543 | 0/80 · 0.0099 · 0.1229 |
| squ-in-squ n=17 | 4.675530 | 0/80 · 0.0119 · 0.0533 | 0/80 · 0.0302 · 0.1217 |

