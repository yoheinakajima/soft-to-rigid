# Paper outline (target: 8 pages + appendix)

Working title: **Soft-to-Rigid: Packing Congruent Shapes by Hardening Disks into Polygons**

The paper tells one story in order: it worked in 2D, then in 3D, so we tested it widely, and here is where it holds and where it does not. Every table and number is generated from the ledger (`paper/numbers.tex`, `paper/tables/*.tex`).

1. **Introduction** (0.75 p). Packing n congruent shapes in the smallest container. Most searches move rigid pieces. We change the pieces instead: start from the inscribed disk and harden. Contributions: the method; a study across families with equal budgets against four alternatives; new records (if any) with certificates; a repository where every run can be replayed and every claim verified.

2. **Method** (1.25 p). Rounded shapes (core = shape scaled about its incenter, plus a disk), energy, pressure, schedule; legalization; exact tightening with separating lines/planes; exact certificate. One figure: a replay strip for one run.

3. **From squares to cubes** (1 p). Squares in a square: recovers published records and beats rigid starts at n = 11. Cubes in a cube: n = 12 record (cite the Geombinatorics note). Short, because the earlier work is already public.

4. **A wider test** (2.5 p). Families, methods, budgets, pre-registration. Main table: per family, hit rate and best gap for each method at equal budget. Records found. Figure: gap to record vs n for each method.

5. **What we learned** (1.5 p). When the hardening path helps and when it does not (slack vs full packings, orientation-sensitive containers, n). Ablations: start shape, schedule, noise timing. Cost.

6. **Limitations and open directions** (0.5 p). Search, not proof. Families not tried. Non-convex shapes, mixed shapes, larger n.

**Appendix.** Catalogue sources, per-instance tables, claim coordinates.

Everything else lives in the repository and site: the journal of every campaign, all replays, and the verifiers.
