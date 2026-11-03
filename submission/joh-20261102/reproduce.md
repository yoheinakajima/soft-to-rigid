# Saved-evidence verification and build guide

This route checks fixed saved evidence. It is deliberately different from regenerating native operational state or running a campaign.

## Fixed inputs and bounded execution

Use study commit `07e3cbd3c4855e5e19344885fbf672c3d7a0f039` plus the journal-preparation PR. `verification/input-manifest.json` enumerates every source input consumed, with byte count and SHA256. The verifier uses Python 3 standard-library JSON, arithmetic and file reads. It writes only `submission/joh-20261102/verification/` and the new draft's evidence/tuning/witness tables. It does not import ActiveGraph, a numerical optimizer or a provider. It never fills missing caches.

One command performs the authorized verification route:

```sh
python3 scripts/verify_joh_packet.py
```

It reconstructs C10 from serialized event objects/patches as data; recomputes C15 policy selection and all stored policy outcomes from fixed raw rows and existing polishing caches; checks C16 deterministic reuse and new-only comparison; recomputes C14 fixed-subset tightening rankings from saved outputs; extracts C06 grid boundaries; and runs `verify.py` plus `packing.certify` on four explicitly enlarged saved square witnesses. It fails on absent inputs, duplicate run IDs, errors or discrepant results. Each native checker has a 30-second timeout. No solver or pipeline rebuild is needed. The input dataset is approximately tens of megabytes, not the full historical campaign/replay corpus.

The witness enlargement is deterministic arithmetic, not optimization: source centers are scaled by 1.000001; container side is `1.00001 * stored_side + 0.000001`. The resulting feasibility proof concerns that enlarged side, not the original contact objective. Both values, exact run IDs, inputs and native outputs are recorded. No below-catalogue record is asserted.

## Commands excluded from this route

Do not substitute `packing.ledger rebuild/ingest/finding`, `packing.polish`, `packing.refine`, `packing.decision`, the post-hoc tightening scripts or `engine/run.js`. The native analysis path imports a runtime and several modules may launch tightening on cache miss. A source change needed for a read-only projection does not authorize canonical runtime mutation. No original `ledger/`, raw result, plan, generated result table, historical report or public-v1 artifact is written by the curated verifier.

The additive C10 interpretation record is a **native-finding proposal**, not an accepted ledger event. The native finding command requires ActiveGraph and a populated audited local database; automatically rebuilding the absent database is outside this route because it can trigger polishing/certification. Preserve the proposal and correct journal wording until that exact native application is separately reviewed.

## Compile the distinct journal sources

No app-native LaTeX compiler/editor tool was exposed in this worker's tool inventory. The existing Tectonic 0.16.9 installation and cached bundle were used; no TeX runtime, plugin, package or font was installed. This is a multi-file manuscript, not a standalone editor document.

```sh
tectonic --only-cached --keep-logs --keep-intermediates --untrusted paper/joh-20261102/main.tex
tectonic --only-cached --keep-logs --keep-intermediates --untrusted paper/joh-20261102/supplement.tex
```

The source specifies Times New Roman/Arial from the existing macOS font environment and cached scalable Computer Modern/AMS math fonts. `Y` denotes a reached catalogue value in the C16 table, replacing the original checkmark via a presentation macro. Fonts are embedded in the PDF; portability requires those fonts or an explicitly reviewed equivalent. The algorithm display uses ordinary LaTeX enumeration to avoid an unavailable optional style. These changes are journal-draft presentation only.

Historical study dependency versions/hardware were not fully recorded. The current verification environment is a new check environment and is not substituted for the original one. Building a PDF is distinct from reproducing an optimization campaign. The rendered-PDF QA receipt and the final artifact hashes are in the packet.

## Permissions and submission boundary

The public code license is MIT and the original arXiv manuscript is CC BY 4.0; third-party records retain their rights. Filled private author/companion answers do not belong in this Git package. Approve final public declarations and the exact candidate; accurately disclose the separate note's history and overlap, freshly attest exclusive consideration of the current JoH work, and check permissions only for actual applicable protected reuse. Mandatory closure, withdrawal or contact for the distinct note is not established by the inspected JoH policy. This guide authorizes no account, upload, editor/reviewer contact, fee, license agreement, arXiv replacement, public release, merge or deployment.
