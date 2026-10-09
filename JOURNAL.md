# Journal

*Generated from the ledger (`ledger/events.jsonl`, 18457 events) by `packing/project.py`. Do not edit.*

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

## C04-breadth — Equal-budget comparison of five paths across seven 2D families

*Planned 2026-10-08 · status: closed*

With every method tuned the same way (C01-C03) and given the same number of pair evaluations, which methods reach the best known packing, on which families, and how often?

- **Expected:** H1: after exact tightening, harden reaches the best known value on more instances than each of grow, rigid, sa and pc. H2 (control): on circles, where hardening changes nothing, harden and rigid differ only through their tuned schedule parameters, so any difference there measures parameters, not paths. H3 (exploratory): the gap to the best known value grows with n for every method.
- **Rule:** Primary metric: an instance is solved by a method if any of its 32 runs, after exact tightening, is within 1e-9 of the best known value (within 1e-5 when the catalogue value is truncated) or below it. Test H1 with a one-sided sign test over instances solved by exactly one of the two methods (alpha 0.05, per pair, no correction; reported with counts). If H1 fails against rigid, the paper does not claim that hardening is the better path in general; it reports where each path wins. Secondary metrics: raw hit rate (raw gap < 1e-3), median relative gap, time per run. Excludes the five tuning instances. Any run whose tightened size is below a catalogue value is certified and reported regardless of method. Tightening policy, identical for every method: in each cell (instance x method) the three best runs are tightened if their raw size is within 2% of the best known value, plus every run within 2e-3 of it, at most ten per cell.
- **Found:** Main comparison with median-tuned settings (188 instances, 32 runs each, equal budget, lowest point after exact tightening). Instances where each method's lowest size equals the lowest of all five: rigid 155, harden 142, grow 139, sa 72, pc 64; where it is the only method that low: rigid 23, harden 16, grow 11, sa 2, pc 0. Instances solved (best known value reached): rigid 132, harden 121, grow 119, sa 69, pc 63. Pre-registered sign test: rigid solves more instances than harden (18 only-rigid vs 7 only-harden, one-sided p = 0.02); harden vs grow is inconclusive (11 vs 9); harden beats sa (57 vs 5) and pc (59 vs 1). H1 fails against rigid. 46 instances were solved by no method; no packing below a published value was found.
- **Found:** The advantage depends on the family. Squares in a square: harden's lowest is the lowest of all methods on all 28 instances and the only one that low on 7 (it alone solves n = 11, 17, 26; rigid and grow solve none of these). Squares in a circle: split (harden only-lowest on 7 instances, rigid on 9). Triangles in a square or triangle, hexagons and squares in a triangle: rigid and grow are lower more often; harden is the only lowest on at most one instance per family. Circles (control, where hardening changes nothing): all three gradient paths are equivalent (27 or 28 of 29).
- **Decided:** By the pre-registered rule, the paper does not claim that hardening is the better path in general: tuned rigid starts solve significantly more instances overall. It reports where each path reaches the lowest point: hardening for squares in a square (and part of squares in a circle), rigid or grow for triangles and hexagons. Because settings were tuned by median, C07 repeats the comparison with settings tuned for the lowest point.

[Full report](campaigns/C04-breadth/REPORT.md)

## C06-tune-best — Re-tune every method for its lowest point, on harder held-out instances

*Planned 2026-10-08 · status: closed*

C01-C03 chose each method's settings by median gap, but the question that matters is which method is most likely to produce the lowest packing. On the C01 tuning instances nearly every setting reaches the best known value, so best-of scoring cannot separate settings there. Re-tune on eight harder instances above n = 30 that no other campaign uses.

- **Expected:** Best-of tuning favours stronger pressure for harden and weaker pressure for rigid and grow than median tuning did (as a re-scoring of C01-C03 suggests).
- **Rule:** For each method and setting: primary score = mean over the eight instances of the lowest legal size of 16 runs relative to the best known value (lowest is best); tie-break = mean fraction of runs within 1e-4 relative of the best known value. The winner is frozen into methods/<method>-best.json and used by C07. Every method gets one 3x3 grid; no extensions.
- **Found:** Tuned for their lowest point on eight held-out instances above n = 30, harden and rigid choose the same settings (strongest pressure and noise in the grid). With those settings rigid reaches the lower size on most of these instances (mean lowest gap 0.63% of the best known size, against 1.06% for harden, 1.71% grow, 5.5% sa, 5.7% pc); harden is worst among the gradient paths on triangles.
- **Decided:** Frozen by scripts/score_best.py into methods/*-best.json: harden and rigid both mu 0.16, noise x8 (identical settings, so C07 compares their paths alone); grow mu 0.08, gamma0 0.1; sa T0 1e-3, mu 0.02; pc kick 0.05, relax 19200. Several winners lie on a grid edge; as pre-registered, no extension.

[Full report](campaigns/C06-tune-best/REPORT.md)

