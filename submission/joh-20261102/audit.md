# Journal preparation audit

Observed 2026-11-02, America/Los_Angeles. Evidence base is `yoheinakajima/soft-to-rigid@07e3cbd3c4855e5e19344885fbf672c3d7a0f039`. This audit accompanies a distinct journal draft; it does not alter public v1, historical plans, run files, reports or the ledger. Computed audit results and fixed-input hashes are in `verification/report.json` and `verification/input-manifest.json`.

## Contribution and closest prior art

The supported contribution is an auditable finite-container study of shape continuation as a search path, including where it loses, under the actual tuning/budget design. It is not the invention of rounding, morphing, continuation or sphere-to-polyhedron evolution. Jin, Lu and Li already evolve periodic spherotetrahedron packings in both directions, including starting from sphere arrangements. The journal draft preserves that credit and removes the unverified “we have not found” priority claim. Prior formulation: [Scientific Reports 5, 15640](https://www.nature.com/articles/srep15640), DOI 10.1038/srep15640 (2015); the current manuscript bibliography already includes it. The primary article's inverse-evolution discussion was checked in the present audit.

The paper's support-function/area identities explain the path construction, not a new guarantee of escaping local minima. The distinctive evidence is which packings the specified searches reach, under finite budgets and in-house implementations. C10 and C15 do not validate generic portfolio utility; C11/C12 and selected replay statistics do not isolate an orientation cause. A mixed-result study can remain useful without setting records if these scope conditions are explicit. No acceptance or editorial-competitiveness prediction is made.

## External baseline compatibility: exact variants

Sources inspected: [Berthold et al. v1](https://arxiv.org/html/2605.04850v1), especially Sections 3, 4 and 6; [supplement repository](https://github.com/DominikKamp/Packing/tree/27f71632d8655ae4b6a049410a401976748b94e3), commit `27f71632d8655ae4b6a049410a401976748b94e3`; and [sparrow v4, Section 2](https://arxiv.org/html/2509.13329v4). These are comparison-design sources, not executed competitors.

Berthold's supplement stores regular inner m-gons of circumradius one inside regular outer l-gons, minimizing outer circumradius R, with continuous rotations modulo polygon symmetry. The finite polygon subset can match this study's unit-side pieces by multiplying coordinates by `1/(2 sin(pi/m))`. Container side then equals `R sin(pi/l)/sin(pi/m)`. Thus the geometry-compatible mappings are:

- squares in square: `(l,m)=(4,4)`, side `R`;
- squares in triangle: `(3,4)`, side `R sqrt(3/2)`;
- triangles in square: `(4,3)`, side `R sqrt(2/3)`;
- triangles in triangle: `(3,3)`, side `R`;
- hexagons in square: `(4,6)`, side `R sqrt(2)`;
- held-out hexagons in triangle: `(3,6)`, side `R sqrt(3)`;
- held-out pentagons in square: `(4,5)`, side `R sin(pi/4)/sin(pi/5)`.

The supplement indexes `l,m=3..7` and `n=1..30`; only the intersection with each source campaign's actual n-range is eligible. Octagons are outside that indexed set. Circle containers are not finite regular-polygon containers in this supplement; no circular-container comparison is silently inferred. Its square/rectangle circle results allow **variable radii and maximize their sum**. They do not match the study's congruent unit-diameter disks, even in a square. An equality-of-radii model restriction would be a changed benchmark. Cube-in-cube is a geometry-compatible 3D subset, after uniform scale conversion; C05 still lacks the two classical baseline methods and is not evidence for all five searches in 3D.

Sparrow minimizes variable strip length with fixed width. Although its shape/rotation machinery is relevant, minimizing finite square/triangle/circle container scale changes the objective and containment problem. A fixed-width strip incumbent is not a square-container optimum, and an outer bisection wrapper/adaptation is a new experiment. It is retained as related work, not a promised untouched baseline.

A geometric match is insufficient for a cost-matched empirical comparison: solver version/configuration, native termination budget, warm starts, machine, randomness, polishing, feasibility tolerance and retained incumbent/bounds must also match or be explicitly separated. Berthold's supplement is a solution archive; its inspected root contains README and solution directories, not a licensed complete experiment harness. GitHub reports no detected root license. No executable baseline, solver configuration, license entitlement or corresponding resource cost has been verified here. Solver-produced feasible incumbents are upper bounds; their reported global lower bounds and optimality gaps are distinct evidence and do not certify a locally produced solution's optimality.

**Implemented decision:** keep the present within-implementation comparison and remove general external competitiveness. No outside solver run is necessary to support that narrowed claim. A future external-performance sentence would require a new bounded, preregistered, explicitly approved comparison; it is not added as a hidden prerequisite.

## Tuning, budgets and tightening

C01–C03 tune median outcomes; C06 tunes lowest-of-16 outcomes on eight larger instances, with a single nine-configuration grid per method and no extension. The audit extracts every C06 axis and winner directly from plans and `methods/*-best.json`: **all five winners occupy a grid corner**. The exact ranges and selected values are in `verification/report.json::checks.C06_grid` and the generated SI tuning table. Equal grid effort is not evidence that each algorithm was well tuned across all families. Square-driven development and larger-than-test tuning instances limit generality; SA and pc remain these implementations/configurations.

Gradient paths share step counts, not pair-evaluation counts. SA/pc stop against a reference-hardening pair-evaluation allowance and overshoot it according to their iteration structure. The saved diagnostics distinguish this from simulator wall-clock time, which excludes tightening. The journal draft no longer infers equal end-to-end cost or general wall-time superiority. Historical host/Node/NumPy/SciPy/ActiveGraph versions are not fully recorded; current validation's environment cannot fill that historical gap. The recorded diagnostic times remain descriptive measurements with that limitation.

C14 tightens the best three legalised runs of each method, without the C07 eligibility gate, on a fixed 28-instance subset. Its conclusions apply to that subset, not all 188 instances. C16's equal-tightening check on four selected hardening-only instances is post hoc. The original report/projection is preserved; the journal draft replaces the claim that similar eligibility fractions “cannot explain” rigid/hardening ordering with the weaker supported observation. `packing.refine`, `packing.decision`, and post-hoc scripts can call numerical tightening on a missing cache, so none is used as a nominal read-only verifier.

## Inference and chronology

The saved-input verifier independently reconstructs C10 from serialized event objects and patches without instantiating the event runtime. It confirms mixed 139 versus doubled rigid 138 solved and discordants 4 versus 3. The registered one-sided tail is .5; the paper's two-sided value is 1. Neither provides an equivalence result. `interpretive-corrections.jsonl` records a new interpretive correction and native-finding proposal. Historical “as good as/no better” wording is retained as history and explicitly superseded in the new draft.

For C15, the verifier reads all 7,680 saved raw rows, applies the registered raw-pilot selection rule, selects the saved tightened best result for each policy, fails on cache absence and matches every policy/run/value/reached entry in `analysis/C15.json`. Pilot versus rigid is 2 versus 3 lower, 55 ties, p=1. Its 41 versus 40 reached counts are a different endpoint. Pre-plan n=8 seed-3 geometry smoke tests on each family/path qualify “never used”; they are disclosed in the draft. The tightened-pilot check remains post hoc. The additional families contain no aggregate hardening-favorable family, so this is not a test of finding such a family.

For C16, 96 harden/rigid rows at n=19,28,29 match C09's poses, objective, steps and pair evaluations exactly. They are not independent replications; the new-only 11-instance comparison remains 3 versus 0 lower, p=.25. New hardening-only best-known reaches are n=17,26. The targeted follow-up is not a randomly sampled family test.

Instances and shape families are designed, related benchmark units. Best-of-32 is a restart procedure observed once per cell, not a typical single run. Within-pool bootstrap omits possible unseen better runs and is a sensitivity analysis, not independent replication or future-population confidence. Numerous family/endpoint tests are descriptive and do not establish multiplicity-controlled general claims. The draft preserves failed/withdrawn C09 and C11 interpretations and labels mechanism measurements as descriptive.

## Witnesses, precision and code/data rights

There are no `claims/` entries at the pinned study tree; zero controlled-study below-catalogue certificates is the reported result. A catalogue-tolerance “reached” result is not exact equality, a new record or an optimum proof. The exact 2D checker accepts circles, triangles, squares and hexagons, not C15 pentagons/octagons. The earlier reported cube bound and its witness belong to the separately cited companion repository, not to a new C05 record.

Four decisive saved square outcomes (n=11,19 in C07 and n=17,26 in C16) were selected from fixed raw/cached outputs. For each, the verifier makes a **separate enlarged witness**: centers scaled by 1.000001 and container side set to `1.00001 * stored_side + 0.000001`. Both the native floating-point checker and exact rational checker pass. Exact input/output files and bounds are included. These certificates establish nearby feasible upper bounds, **not certification of the original contact objective or a record improvement**. No optimizer, new seed, tightening, record claim, or canonical witness cache is used or modified. Exact validation at all original contact values and for all families remains unestablished.

Root MIT is a software license. The public manuscript has its own CC BY 4.0 license; externally sourced catalogue/witness/figure rights are not automatically relicensed by the repository. This packet uses existing own-study figures and links to external datasets rather than redistributing external witnesses. Companion reuse permissions and any publisher agreement require author confirmation. External solver/software license acceptance is outside scope.

## Native-state boundary and residual scientific limits

The native finding CLI imports unavailable `activegraph`, opens/creates `ledger.sqlite`, emits the finding and runs behaviors. The work clone has an event export but no database; automatically rebuilding it would ingest campaigns and can launch polishing/certification. Therefore no native ledger command or global projection was run. The new correction record is explicitly **proposed**, outside `ledger/`, ready for later native application after a cache-complete stateful route is separately established. All historical reports, macro sources, event exports, raw files and registrations are preserved. The distinct journal draft uses copied native macro snapshots and an additional saved-output projection.

Residual limits are substantive and visible: no general external competitiveness, no equivalence/predictive-selector/causal-mechanism claim, incomplete historical environment identity, no exhaustive certification of every contact outcome, and unresolved author/rights/companion/exclusivity attestations. Existing evidence supports a reviewable narrowed draft; it does not establish journal submission readiness or acceptance.

## Public priority caveat added during manager review

The official [public build log](https://yohei.me/) entry dated October 8 states that novelty relative to Haowei Lin's arrangement remains disputed. The companion repository [README at efe7a920142350a4f0678633490c3e3dbed71fa0](https://github.com/yoheinakajima/soft-to-rigid-packing/blob/efe7a920142350a4f0678633490c3e3dbed71fa0/README.md) still describes an improvement over its July 2026 Hyra comparator. These public assertions do not resolve priority. A feasibility certificate proves a bound, not originality, chronology or attribution. The journal intro/story now use a prior reported feasible bound and dated catalogue comparators; no undisputed new-record/improvement claim is necessary to the controlled-study contribution. Priority/rights remain unresolved for author/editor disclosure. No companion repository, website or correspondence was changed.
