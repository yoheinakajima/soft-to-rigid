# Notes for AI agents working in this repository

Read `ARCHITECTURE.md` first. The short version:

- **Never edit results.** `campaigns/*/runs*.jsonl` are append-only; `ledger/` is written only by `packing/ledger.py`.
- **Plan before running.** A new experiment is a new folder `campaigns/Cxx-name/plan.json` (question, hypothesis, instances, methods, budgets, seeds, decision rule), committed before its first run. If a plan must change after runs started, add an entry to its `amendments` list; do not rewrite it.
- **Run:** `node engine/run.js campaigns/<C>/plan.json --worker 0 --of 2` (and `--worker 1`). Resumable; safe to kill.
- **Record:** `python3 -m packing.polish <C>` (exact tightening, parallel), then `python3 -m packing.ledger ingest <C>`.
  Add conclusions with `python3 -m packing.ledger finding "<text>" --evidence <cell ids> --campaign <C>` and
  `python3 -m packing.ledger close <C> "<decision taken, citing the decision rule>"`.
- **Project:** `python3 -m packing.project` regenerates README tables, `JOURNAL.md`, campaign reports, site data and paper numbers. Never type a number into those files by hand.
- **Claims:** any tightened packing strictly below a catalogue value becomes `claims/<family>-n<N>/` automatically, with `verify.py` (float) and `packing.certify` (exact) outputs. Check both before announcing anything.
- **Catalogue values** come from `scripts/build_catalog.py`, which cites its sources. Values marked `truncated` are lower bounds of the true record (Friedman's "+"), so beating them requires going below the printed digits.
