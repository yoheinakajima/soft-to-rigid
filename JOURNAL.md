# Journal

*Generated from the ledger (`ledger/events.jsonl`, 57389 events) by `packing/project.py`. Do not edit.*

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

## C05-cubes — Cubes in a cube: three paths, two settings

*Planned 2026-10-08 · status: closed*

The n = 12 cube record came from hardening balls into cubes with the original (untuned) schedule. In 3D, at n = 9 to 14, how do harden, grow and rigid compare at the record's budget, with the original settings and with each method's 2D-tuned settings?

- **Expected:** harden is the only path that gets below 2.93277 at n = 12 under either setting; at n = 9 all three reach Friedman's packing.
- **Rule:** Same 'solved' metric as C04 (tightened run within 1e-9 of the best known value, 1e-5 if truncated, or below it). Report per n, method and setting. sa and pc are not implemented in 3D; the comparison is limited to the three gradient paths. If a tightened run beats a catalogue value it is certified as in C04.
- **Found:** Cubes, 32 runs per method at the record's budget. harden has the lowest side of the three paths at n = 11, 12 and 13 under both settings; all three reach Friedman's n = 9 packing; with 2D-tuned settings harden and rigid also reach his n = 10 packing (2 + 1/sqrt 2), which the original schedule never reached. At n = 13 tuned harden tightens to 2.956145, consistent with Friedman's 2.956+ to the printed precision. No run went below a catalogue value: the n = 12 record (2.9315185) came from seed 52, outside this campaign's seeds 1-32; the best here is 2.942809. Rigid starts end at the trivial side 3 for n >= 12.
- **Decided:** Hypothesis partly supported: harden is the lowest path for n = 11-13 under both settings, but nothing went below 2.93277 in 32 seeds. Reported as a 3D replication of the family pattern, not as a new record.

[Full report](campaigns/C05-cubes/REPORT.md)

## C06-tune-best — Re-tune every method for its lowest point, on harder held-out instances

*Planned 2026-10-08 · status: closed*

C01-C03 chose each method's settings by median gap, but the question that matters is which method is most likely to produce the lowest packing. On the C01 tuning instances nearly every setting reaches the best known value, so best-of scoring cannot separate settings there. Re-tune on eight harder instances above n = 30 that no other campaign uses.

- **Expected:** Best-of tuning favours stronger pressure for harden and weaker pressure for rigid and grow than median tuning did (as a re-scoring of C01-C03 suggests).
- **Rule:** For each method and setting: primary score = mean over the eight instances of the lowest legal size of 16 runs relative to the best known value (lowest is best); tie-break = mean fraction of runs within 1e-4 relative of the best known value. The winner is frozen into methods/<method>-best.json and used by C07. Every method gets one 3x3 grid; no extensions.
- **Found:** Tuned for their lowest point on eight held-out instances above n = 30, harden and rigid choose the same settings (strongest pressure and noise in the grid). With those settings rigid reaches the lower size on most of these instances (mean lowest gap 0.63% of the best known size, against 1.06% for harden, 1.71% grow, 5.5% sa, 5.7% pc); harden is worst among the gradient paths on triangles.
- **Decided:** Frozen by scripts/score_best.py into methods/*-best.json: harden and rigid both mu 0.16, noise x8 (identical settings, so C07 compares their paths alone); grow mu 0.08, gamma0 0.1; sa T0 1e-3, mu 0.02; pc kick 0.05, relax 19200. Several winners lie on a grid edge; as pre-registered, no extension.

[Full report](campaigns/C06-tune-best/REPORT.md)

## C07-breadth-best — The breadth comparison again, with every method tuned for its lowest point

*Planned 2026-10-08 · status: closed*

Repeat C04 exactly (same 188 instances, 32 seeds, budget, tightening policy) with the settings chosen by C06. Which method is most likely to produce the lowest packing on each instance?

- **Expected:** As in C04: harden reaches the best known value where it needs tilted pieces (e.g. squares n = 11, 17-19, 26-29), and rigid or grow where the best packing is a grid with spare room. Best-of tuning should not reverse that split.
- **Rule:** Headline metric (pre-registered): per instance, each method's lowest tightened size over 32 runs; an instance is solved by a method if that lowest size is within 1e-9 of the best known value (within the printed precision when the catalogue value is truncated) or below it. Report, per family and overall, the number of instances where each method attains the lowest size among the five (ties counted for all tied methods), and the number solved. One-sided sign test of harden vs each method on instances solved by exactly one of the two. Medians are reported only as secondary information. Same tightening policy as C04.
- **Found:** Main comparison with every method tuned for its lowest point (188 instances, 32 runs each, equal budget, after exact tightening). Instances where the method's lowest size is the lowest of all five: rigid 155, grow 144, harden 142, sa 125, pc 72; the only method that low: rigid 16, harden 13, grow 9, sa 6, pc 1. Best known value reached: rigid 133, grow 129, harden 125, sa 115, pc 71. Sign tests (instances solved by exactly one of the pair): rigid vs harden 14 vs 6 (one-sided p = 0.058), grow vs harden 13 vs 9, harden vs sa 21 vs 11, harden vs pc 59 vs 5. Best-of tuning helped sa most (69 to 115 instances solved). No packing below a published value; 43 instances unsolved by every method.
- **Found:** The family pattern survives re-tuning. Squares in a square: harden's lowest is the lowest of all methods on 27 of 28 instances and the only one that low on 5; with identical settings, rigid is lowest on 23. harden alone reaches Wainwright's n = 19 packing (and Trump's n = 11). Triangles in a square and in a triangle: rigid is lowest on 22 and 26 instances against harden's 14 and 18. Run as a pair, harden and rigid together solve 139 instances, more than any pair without harden (rigid and grow: 137), though with twice the runs.
- **Found:** Correction to wording (after review): budgets are matched in steps for the gradient paths and in reference pair evaluations for sa and pc (pc overshoots up to 1.8x); tightening is constrained numerical optimisation, not exact; p-values in the paper are exact two-sided (rigid vs harden 14 vs 6, p = 0.12). The counts above are unchanged. Rigid's lead is about the width of the seed-bootstrap 95% intervals (rigid 139-153, harden 126-140, grow 123-138).
- **Decided:** Same conclusion as C04 under lowest-point tuning: no general superiority for hardening (rigid solves more, p = 0.058); hardening is the path for squares in a square, rigid or grow for triangles. Next: C08 (how soft the start must be, on the 40 most contested instances), C09 (longer budgets on 20 of them) and C10 (does adding hardening runs beat adding more rigid runs).

[Full report](campaigns/C07-breadth-best/REPORT.md)

## C08-start-shape — How soft must the start be? A dose-response on the starting shape

*Planned 2026-10-08 · status: closed*

With every other setting fixed at the shared best-of setting of harden and rigid (mu 0.16, noise x8), vary only how rounded the pieces start: tau0 = 1 (inscribed disk, harden), 0.5, 0.25 and 0 (rigid). Does the lowest point move monotonically with tau0, and does the answer depend on the family?

- **Expected:** On instances whose best known packing tilts pieces against each other (squares n = 11, 17-19, 26-29 in a square), softer starts reach lower sizes; on triangles and slack grids the reverse.
- **Rule:** Instances: the contested instances of C07, defined as those where the lowest sizes of harden-best and rigid-best differ by more than 1e-6 relative, capped at 40 by taking the largest relative differences. Metric: lowest tightened size over 32 runs per instance and tau0 (same tightening policy as C04). Report, per family, the number of instances where each tau0 attains the lowest size; test monotonicity descriptively (no significance test).
- **Found:** Starting softness on the 40 most contested instances of C07 (all other settings equal): tau0 = 1, 0.5, 0.25, 0 reach the lowest size on 7, 15, 18 and 17 instances. Squares in a square favour soft starts (3, 4, 2, 0); triangles favour rigid or slightly rounded ones (2, 7, 8, 10). Partly rounded starts (0.25-0.5) are never far from the best choice. The contested set leans to instances where rigid won in C07 (28 of 40), which favours small tau0.
- **Decided:** Hypothesis supported for its two named cases (soft for squares in a square, rigid for triangles); no monotone rule across families. A half-rounded start is reported as a reasonable default when the family is unknown.

[Full report](campaigns/C08-start-shape/REPORT.md)

## C09-budget — Does a longer schedule change which path finds the lowest point?

*Planned 2026-10-08 · status: closed*

On the contested instances, give harden-best and rigid-best 3x and 10x the budget (32 runs each). Does the gap between the paths close, persist, or reverse with more time, and does either path find a packing below a published value?

- **Expected:** More time lowers both paths' lowest points; the path that wins at budget 1 on an instance still wins at budget 10 on most instances.
- **Rule:** The 20 most contested of C08's instances (largest relative differences). Metric: lowest tightened size over 32 runs per instance, method and budget. Report the per-budget count of instances where each path is lowest, and certify anything below a catalogue value.
- **Found:** Longer schedules on the 20 most contested instances: harden is lowest on 3, 5 and 9 instances at budget 1, 3 and 10, rigid on 17, 16 and 16; harden reaches the best known value on 1, 2 and 6, rigid on 10, 10 and 9. Hardening gains more from time. At budget 10 harden reaches Schadt's squares-in-square n = 29 packing (5.933833) and Wainwright's n = 19 in 11 of 16 runs; both paths tighten to 3.1292935 for triangles in a square n = 19 (catalogue 3.12929+) and harden to 3.6726370 for n = 27 (3.6726+), both consistent with the catalogue to its printed precision. Nothing below a published value.
- **Found:** Precision note on the C09 finding: at budget 10, 11 of 16 harden runs for squares-in-square n = 19 come within 1e-4 of Wainwright's value before tightening; the three that were tightened all match it to 1e-14. Both runs tightened at n = 29 match Schadt's 5.933833462677 to 1e-12.
- **Decided:** Hypothesis partly supported: rigid's wins at budget 1 mostly persist, but harden closes the gap with more time (3 -> 9 instances lowest). Instances were chosen where the paths differed, mostly in rigid's favour, so part of the change may be regression toward even.

[Full report](campaigns/C09-budget/REPORT.md)

## C10-portfolio — Is a second path worth more than more of the same path?

*Planned 2026-10-08 · status: closed*

Run together, harden and rigid solve more instances than either alone, but with twice the runs. Run rigid-best for 32 more seeds (33-64) on all 188 instances and compare rigid with 64 runs against rigid 32 + harden 32 (same total budget), and against rigid 32 + grow 32.

- **Expected:** Mixing paths beats doubling one path: rigid 32 + harden 32 solves more instances than rigid 64, because the paths fail on different instances (squares in a square vs triangles).
- **Rule:** Count instances solved (as in C07) by: rigid 64 (C07 seeds 1-32 + C10 seeds 33-64), rigid 32 + harden 32, rigid 32 + grow 32. One-sided sign test of the mixed portfolio against rigid 64 over instances solved by exactly one. Report lowest-point counts as in C07.
- **Found:** Portfolio at equal total budget: 32 rigid runs plus 32 harden runs solve 139 of 188 instances, 64 rigid runs 138, and 32 rigid plus 32 grow 137. Instances solved by exactly one of mixed vs doubled: 4 vs 3 (one-sided p = 0.5). A second path is worth about as much as doubling the runs of the best single path; it does not beat it.
- **Decided:** Hypothesis not supported: mixing paths (139) is no better than doubling rigid (138) at equal budget. The paper reports that the paths are complementary by family but that, without knowing the family's character in advance, extra rigid runs are as good as adding hardening runs.

[Full report](campaigns/C10-portfolio/REPORT.md)

## C11-snap — Is it the path or the starting configuration?

*Planned 2026-10-09 · status: closed*

Hardening differs from rigid starts in two ways: pieces are compressed as disks first, and they then harden gradually. snap compresses disks exactly as harden does and then switches to the full polygons at once, with the same settings, seeds and budget. Comparing harden, snap and rigid on all 188 instances separates the effect of the disk-compressed starting configuration from the effect of the gradual path.

- **Expected:** On squares in a square, harden reaches lower sizes than snap (the gradual path matters); on other families snap and rigid are similar.
- **Rule:** Same metric and tightening policy as C07. For each family, count instances where harden, snap and rigid (C07, same seeds and settings) attain the lowest of the three, and solved counts; report the two-sided exact sign test of harden vs snap over instances solved by exactly one. If harden and snap do not differ on squares in a square, the paper attributes hardening's advantage there to the disk-compressed start rather than to the path.
- **Found:** Snap (disks compressed as in hardening, then polygons at once) behaves like rigid starts: lower on 20 instances each, 148 ties. Hardening differs from snap by family: lower on 6 squares-in-square instances against 0, while snap is lower on 8 triangles-in-triangle instances against 0 and 14 vs 6 triangles in a square. Over all 188 instances harden vs snap lower 17 vs 36 (two-sided p = 0.013). The gradual change of shape, not the disk-compressed start, carries hardening's effect in both directions.
- **Found:** Correction (supersedes the wording of the C11 and C12 findings after an independent check): snap and grow-area show no detectable difference from rigid starts (20 vs 20 and 15 vs 14 instances lower); this is non-detection, not equivalence. Hardening differs from both in the same family-dependent directions (squares in a square in hardening's favour, triangles against), which suggests the gradual rounding is responsible, but the pre-registered tests on squares in a square are inconclusive (2 vs 0 solved-only discordant), so by the plans' rule the advantage there is attributed to the disk-compressed start. Treat the path explanation as post hoc.
- **Decided:** Per the pre-registered rule (two-sided sign test over instances solved by exactly one of harden and snap): squares in a square 2 vs 0, p = 0.5, not separated, so the pre-registered conclusion attributes hardening's advantage there to the disk-compressed start. Recorded with the caveat that the rule has no power at two discordant instances, and that the descriptive evidence (snap = rigid; harden lower than snap 6-0 on squares, higher 0-8 on triangles in a triangle) points to the gradual path. The paper reports both.

[Full report](campaigns/C11-snap/REPORT.md)

## C12-grow-area — Is it the shape change or the area schedule?

*Planned 2026-10-09 · status: closed*

Hardening also changes how much area each piece occupies over time. grow-area keeps pieces as rigid polygons but scales them so their area follows hardening's area schedule exactly, A(tau)/A = 1 - (1 - pi rho^2/A) tau^2, with the same settings, seeds and budget.

- **Expected:** On squares in a square, harden reaches lower sizes than grow-area (changing shape, not only size, matters).
- **Rule:** As C11, comparing harden with grow-area (and rigid, from C07).
- **Found:** Grow-area (rigid polygons scaled so their area follows hardening's schedule) behaves like rigid starts: lower on 15 vs 14 instances, 159 ties. Hardening differs from it as from snap: squares in a square 5 vs 1, triangles in a triangle 1 vs 8, triangles in a square 5 vs 11. Neither the disk-compressed start (C11) nor the area schedule reproduces hardening's effect; the rounding of the pieces does.
- **Found:** Correction (after review): grow-area shows no detectable difference from rigid starts (15 vs 14 lower); harden vs grow-area 20 vs 31 overall (p = 0.16), squares in a square 5 vs 1, triangles in a triangle 1 vs 8. Under C11's rule the squares-in-square test is inconclusive (2 vs 0). Neither ablation reproduces hardening's pattern, which makes rounding the likeliest explanation, but these experiments do not establish it.
- **Decided:** As C11's rule: squares in a square, instances solved by exactly one of harden and grow-area 2 vs 0 (p = 0.5), not separated by the pre-registered test; triangles in a triangle 0 vs 6 (p = 0.031) in grow-area's favour. Recorded together with the lower-size counts; the paper reports grow-area alongside snap as an ablation.

[Full report](campaigns/C12-grow-area/REPORT.md)

## C13-budget-clean — Longer runs or more runs? A clean budget study

*Planned 2026-10-09 · status: closed*

C09 changed run length and restart count together and used instances selected for disagreement. Here, on 28 instances fixed in advance (n = 11, 17, 23, 29 per family; hexagons n = 8, 12, 16, 20), harden-best and rigid-best get (a) budget 3 with seeds 1-32, compared with C07 at budget 1 with the same 32 seeds, and (b) budget 1 with seeds 33-96, so that 96 short runs can be compared with 32 runs three times as long at equal total cost.

- **Expected:** Both paths improve with longer runs; hardening improves more, as in C09.
- **Rule:** Metric: lowest tightened size over the stated runs, per instance. Report, per budget arm, counts of instances where each path is lowest and solved, and the two-sided sign test of harden vs rigid; and, at equal total cost, 3x32 vs 1x96 per path. Tightening policy as C07.
- **Found:** On 28 instances fixed in advance, harden vs rigid lower: 7 vs 2 with 32 base runs, 4 vs 3 with 32 runs at 3x budget, 6 vs 2 with 96 base runs (all p >= 0.18). Longer runs improved rigid (5 lower, 0 higher than base) more than harden (4 vs 3). At equal cost, 3x longer and 3x more runs did about equally (harden 3 vs 3, rigid 3 vs 2). C09's indication that hardening gains more from longer runs does not replicate.
- **Decided:** Per the rule: no arm separates harden and rigid (two-sided sign tests p = 0.18, 1, 0.29). The hypothesis that hardening improves more with longer runs is not supported; the paper withdraws the C09 claim and reports C09 only in the appendix as confounded.

[Full report](campaigns/C13-budget-clean/REPORT.md)

