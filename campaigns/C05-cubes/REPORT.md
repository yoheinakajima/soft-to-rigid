# C05-cubes: Cubes in a cube: three paths, two settings

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** The n = 12 cube record came from hardening balls into cubes with the original (untuned) schedule. In 3D, at n = 9 to 14, how do harden, grow and rigid compare at the record's budget, with the original settings and with each method's 2D-tuned settings?

**Hypothesis.** harden is the only path that gets below 2.93277 at n = 12 under either setting; at n = 9 all three reach Friedman's packing.

**Decision rule (pre-registered 2026-10-08).** Same 'solved' metric as C04 (tightened run within 1e-9 of the best known value, 1e-5 if truncated, or below it). Report per n, method and setting. sa and pc are not implemented in 3D; the comparison is limited to the three gradient paths. If a tightened run beats a catalogue value it is certified as in C04.

**Status.** closed — **decision:** Hypothesis partly supported: harden is the lowest path for n = 11-13 under both settings, but nothing went below 2.93277 in 32 seeds. Reported as a 3D replication of the family pattern, not as a new record.

## Findings

- Cubes, 32 runs per method at the record's budget. harden has the lowest side of the three paths at n = 11, 12 and 13 under both settings; all three reach Friedman's n = 9 packing; with 2D-tuned settings harden and rigid also reach his n = 10 packing (2 + 1/sqrt 2), which the original schedule never reached. At n = 13 tuned harden tightens to 2.956145, consistent with Friedman's 2.956+ to the printed precision. No run went below a catalogue value: the n = 12 record (2.9315185) came from seed 52, outside this campaign's seeds 1-32; the best here is 2.942809. Rigid starts end at the trivial side 3 for n >= 12.

## Results

Per instance and method: **solved** (✓ = a tightened run matches or beats the best known value), raw hits (raw gap < 1e-3) / runs, best raw gap, median raw gap. Gaps are in container units.

### budget 3, setting `original`

| instance | best known | harden | grow | rigid |
|---|---|---|---|---|
| cub-in-cub n=9 | 2.707107 | ✓ 7/32 · 3.0e-08 · 0.0607 | ✓ 9/32 · 3.5e-08 · 0.0607 | ✓ 5/32 · 2.4e-08 · 0.2929 |
| cub-in-cub n=10 | 2.707107 | 0/32 · 0.0607 · 0.1743 | 0/32 · 0.0607 · 0.2929 | 0/32 · 0.1873 · 0.2929 |
| cub-in-cub n=11 | 2.882953 | 0/32 · 0.0131 · 0.0608 | 0/32 · 0.0344 · 0.1170 | 0/32 · 0.0360 · 0.1170 |
| cub-in-cub n=12 | 2.932772 | 0/32 · 0.0126 · 0.0672 | 0/32 · 0.0531 · 0.0672 | 0/32 · 0.0672 · 0.0672 |
| cub-in-cub n=13 | 2.956000 | 0/32 · 0.0390 · 0.0500 | 0/32 · 0.0440 · 0.0440 | 0/32 · 0.0440 · 0.0440 |
| cub-in-cub n=14 | 2.989949 | 0/32 · 0.0101 · 0.0151 | 0/32 · 0.0101 · 0.0101 | 0/32 · 0.0101 · 0.0101 |

### budget 3, setting `tuned2d`

| instance | best known | harden | grow | rigid |
|---|---|---|---|---|
| cub-in-cub n=9 | 2.707107 | ✓ 14/32 · 7.8e-08 · 0.0383 | ✓ 13/32 · 4.2e-08 · 0.0607 | ✓ 21/32 · 5.2e-08 · 9.1e-08 |
| cub-in-cub n=10 | 2.707107 | ✓ 4/32 · 1.7e-07 · 0.0609 | 0/32 · 0.0607 · 0.2929 | ✓ 2/32 · 1.4e-07 · 0.2929 |
| cub-in-cub n=11 | 2.882953 | 0/32 · 0.0295 · 0.0599 | 0/32 · 0.0303 · 0.1170 | 0/32 · 0.0599 · 0.1170 |
| cub-in-cub n=12 | 2.932772 | 0/32 · 0.0100 · 0.0526 | 0/32 · 0.0156 · 0.0672 | 0/32 · 0.0672 · 0.0672 |
| cub-in-cub n=13 | 2.956000 | ✓ 1/32 · 1.7e-04 · 0.0440 | 0/32 · 0.0440 · 0.0440 | 0/32 · 0.0440 · 0.0440 |
| cub-in-cub n=14 | 2.989949 | 0/32 · 0.0101 · 0.0103 | 0/32 · 0.0101 · 0.0101 | 0/32 · 0.0101 · 0.0101 |

