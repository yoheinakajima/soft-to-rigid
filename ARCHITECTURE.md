# How this repository works

One question runs through everything here: **does the path a piece takes through shape space change which packings a search finds?** The method under study, *hardening*, starts every piece as the disk (or ball) inscribed in it and deforms it into the real shape while the container is pushed inward. The other methods take other paths. Everything in the repo serves the comparison, and every number in the paper can be traced back to a run.

## Six nouns

| Noun | What it is | Where it lives |
|---|---|---|
| **family** | a shape and a container, e.g. `squ-in-cir` (unit squares in a circle) | `catalog/<family>.json`: geometry, best known values with sources |
| **instance** | a family at one n, e.g. `squ-in-cir/n11` | an entry inside the family file |
| **method** | a path through shape space plus a schedule, e.g. `harden`, `grow`, `rigid`, `sa`, `pc` | `methods/<method>.json` |
| **run** | one instance × method × seed × budget | one line in `campaigns/<C>/runs.jsonl` |
| **certificate** | a packing tightened, spread by a clearance, and checked exactly | `claims/<family>-n<N>/` |
| **finding** | a sentence we are willing to defend, linked to the runs that support it | the ledger, rendered in `JOURNAL.md` |

## Campaigns are pre-registered

A campaign is a folder `campaigns/Cxx-name/`. Its `plan.json` is committed **before** any run: the question, instances, methods, seeds, budget, and the decision rule ("if harden beats grow by more than X on Y of Z instances, then ..."). Results are appended to `runs.jsonl`, one JSON object per run, never edited. A run is identified by `instance/method/seed/budget`, so the runner skips anything already done and a killed machine loses at most the runs in flight. `REPORT.md` in each campaign is generated, never written by hand.

## The ledger

The ledger is an [ActiveGraph](https://pypi.org/project/activegraph/) event store (`ledger/ledger.sqlite`, exported to `ledger/events.jsonl`, which is committed). Ingesting a campaign turns every run into an event and an object in the graph. Behaviors react:

- `run.completed` within the polish threshold of the catalogue → `polish.requested`
- `polish.completed` below the catalogue → `certify.requested`
- `certify.passed` → a `claim` object, linked to its runs and family
- `campaign.closed` → summary objects (hit rates, best sides, timings)

Findings are added by the researcher with evidence relations to campaigns and runs. Everything that a reader sees (the README table, `JOURNAL.md`, campaign reports, the site, the numbers in the paper) is a **projection** of the ledger, rebuilt by `make project`. Replaying `events.jsonl` rebuilds the same state with no recomputation.

## Replays

The runner saves a decimated trajectory (shape softness, container size, every piece's pose, ~150 frames) for the best run of every instance × method, and for every hit. These live in `campaigns/<C>/replays/` and are what the site animates.

## Verification

Every claim folder holds the claim file (container size at full precision and one pose per piece, in the Hyra-results format), the output of `verify.py` (floating point, standard library, about 40 lines, exits non-zero on failure), and the output of `packing/certify.py` (exact rational arithmetic). Continuous integration re-runs both on every push.

## Code

```
engine/     JavaScript simulators (fast inner loop)
  geom2d.js       convex polygons: support, signed distance, separating axis
  engine2d.js     every 2D method: harden, grow, rigid, sa, pc, and ablations (snap, grow-area)
  engine3d.js     cubes (3D) with the same interface
  run.js          worker: reads a job list, appends to runs.jsonl
packing/    Python
  catalog.py      families and instances
  tighten.py      constrained numerical tightening (SLSQP, separating lines/planes)
  certify.py      exact rational certificate (incl. exact Q(sqrt 3) proof that the rational surrogate encloses the true polygon)
  ledger.py       ActiveGraph ledger: ingest, behaviors, findings
  project.py      projections: reports, journal, site data (incl. the front-page wall), paper numbers
  analyze.py      main tables and macros (exact two-sided sign tests)
  stats.py        bootstrap intervals, best-of-k curves, n-range table, work per run
  ablations.py    C11 snap, C12 grow-area, C13 clean budget study, repeated batches, C16
  decision.py     C15 held-out families: path-choice policies
  refine.py       C14 equal tightening (no new runs)
  mechanism.py    what pieces do after compression, from replays
campaigns/  pre-registered experiments and their raw results
claims/     certified packings
scripts/    queue.sh (run campaigns in order), figures.py (paper figures), catalogue builder,
            post-hoc checks (c15_tightened_pilot.py, c16_equal_tighten.py, reference_budget.js)
paper/      the paper; its numbers come from numbers.tex, stats.tex, ablations.tex (all generated)
site/       templates and viewers; built into _site/ by site/build.py and deployed by CI
```

## Rules

1. Nothing in a table is typed by hand. If a number appears, a projection produced it.
2. Raw results are append-only. Corrections are new runs.
3. A campaign's plan is committed before its first run.
4. Every claim is checked twice: floating point and exact.
5. Failures are recorded the same way as successes.
