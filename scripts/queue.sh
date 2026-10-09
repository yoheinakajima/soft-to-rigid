#!/bin/bash
# Run campaigns one after another, each on two workers, then tighten its candidates. Logs in each campaign folder.
cd "$(dirname "$0")/.."
for C in "$@"; do
  node engine/run.js campaigns/$C/plan.json --worker 0 --of 2 > /dev/null 2> campaigns/$C/w0.log &
  node engine/run.js campaigns/$C/plan.json --worker 1 --of 2 > /dev/null 2> campaigns/$C/w1.log &
  wait
  python3 -m packing.polish $C --workers 2 > campaigns/$C/polish.log 2>&1
  echo "$(date -u +%FT%TZ) done $C" >> campaigns/queue.log
done
