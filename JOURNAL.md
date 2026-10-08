# Journal

*Generated from the ledger (`ledger/events.jsonl`, 1512 events) by `packing/project.py`. Do not edit.*

Every campaign was planned before it ran. Each entry gives the question, what we expected, what happened, and what we decided.

## C00-reproduce — Does the new general engine reproduce the earlier squares results?

*Planned 2026-10-08 · status: closed*

The 2D engine was rewritten for any regular polygon and container. Before using it, check it against the earlier square-only simulator on the cases reported in soft-to-rigid-packing (squares in a square, n = 11 and 17).

- **Expected:** harden reaches Trump's n = 11 packing in a few percent of starts at budget 3 and the rigid control does not; neither reaches Bidwell's n = 17 at budget 1.
- **Rule:** Proceed if harden hits n = 11 (gap < 1e-3) in at least 2 of 80 starts at B = 3 and its median gap at n = 11 is below rigid's. Otherwise debug the engine before any other campaign.
- **Found:** The general 2D engine reproduces the earlier square-only results: at squares-in-square n = 11, harden reaches Trump's packing in 1/80 starts at budget 1 and 4/80 at budget 3 (all four tighten to the record within 1e-14); the untuned rigid control reaches it in 0/160. Neither reaches Bidwell's n = 17 at these budgets.
- **Decided:** Decision rule met (4/80 >= 2; harden median gap 0.054 < rigid 0.123). Engine accepted.

[Full report](campaigns/C00-reproduce/REPORT.md)

## C01-tune — Tune every method on held-out instances with the same effort

*Planned 2026-10-08 · status: closed*

Each method has two hyperparameters that matter. Give every method the same 3 x 3 grid on five tuning instances, pick its best setting by a fixed rule, and freeze it for all later campaigns.

- **Expected:** None; this is calibration so that later comparisons are not against untuned baselines.
- **Rule:** For each method, score each setting by the mean over tuning instances of (median legal size / best known - 1) over 16 seeds; ties broken by the mean of the best gap. The winning setting is written to methods/<method>.json and the tuning instances are excluded from headline comparisons.
- **Decided:** Scored with scripts/score_tuning.py. Winners on grid edges for harden, grow, rigid, sa and pc's relax; extended in C02 as the rule requires.

[Full report](campaigns/C01-tune/REPORT.md)

## C02-tune-extend — Extend the tuning grid where C01's winner sat on its edge

*Planned 2026-10-08 · status: closed*

In C01 the winning setting of every method except pc's kick lay on the edge of its grid (harden, rigid: mu 0.04 and noise x2; grow: mu 0.04, gamma0 0.2; sa: mu 0.005; pc: relax 1200). Extend each grid past that edge on the same five tuning instances and seeds.

- **Expected:** Stronger pressure and noise help every gradient method on these small instances; the C01 result that tuned rigid beats tuned harden on median gap (0.0027 vs 0.0092) may persist.
- **Rule:** Same scoring rule as C01. The overall winner across C01 and C02 for each method is frozen into methods/<method>.json. If a winner is again on an outer edge, run one more extension (at most two in total), then freeze regardless.
- **Decided:** Scored over C01+C02. grow (mu 0.04, gamma0 0.2) and rigid (mu 0.04, noise x2) are now interior and frozen. harden (mu 0.08, noise x8), sa (T0 3e-3, mu 0.0025) and pc (relax 4800) are still on an edge: extended once more in C03.

[Full report](campaigns/C02-tune-extend/REPORT.md)

## C03-tune-extend2 — Second and last grid extension for methods whose winner is still on an edge

*Planned 2026-10-08 · status: closed*

After C01 and C02, the winners for harden (noise x8), sa (T0 = 3e-3) and pc (relax 4800) are on the outer edge of their grids. Grow and rigid winners are interior. Extend once more, as the C02 decision rule requires, then freeze all five methods.

- **Expected:** None (calibration).
- **Rule:** Same scoring rule as C01 over C01 + C02 + C03. Freeze the winner of each method into methods/<method>.json regardless of edges.
- **Found:** Tuning changes the comparison. With equal tuning effort on five small instances (n = 5 to 10), tuned rigid starts have the lowest median gap (0.27% of the best known size), ahead of harden (0.40%), sa (1.0%), grow (1.5%) and pc (5.4%). The earlier advantage of hardening over rigid starts (C00, n = 11) was measured against an untuned rigid control. Both gradient methods prefer much stronger noise than the original schedule (harden x8, rigid x2). harden never reached the n = 6 triangles-in-triangle record in 16 runs at any setting, while rigid and grow did.
- **Decided:** Frozen into methods/*.json (scripts/score_tuning.py over C01-C03): harden mu 0.08, noise x8; grow mu 0.04, gamma0 0.2; rigid mu 0.04, noise x2; sa T0 3e-3, mu 0.0025; pc kick 0.05, relax 19200. Repeated settings across campaigns reproduce bit-for-bit (same seeds, same results).

[Full report](campaigns/C03-tune-extend2/REPORT.md)

