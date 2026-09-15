#!/usr/bin/env bash
# nightly-swarm.sh
# Takes the first unchecked question from research/QUEUE.md, runs it through
# Claude Code as a research swarm (split -> fan out -> skeptic -> file), then
# ticks the queue line. One question per run. Safe to call from cron.
#
# Requires: the `claude` CLI, logged in. Run from anywhere; it cds to the repo root.
# Cron example (2am daily):
#   0 2 * * *  cd ~/founder-research-swarms && ./scripts/nightly-swarm.sh >> logs/nightly.log 2>&1

set -euo pipefail
cd "$(dirname "$0")/.."

QUEUE="research/QUEUE.md"
Q="$(grep -m1 '^- \[ \] ' "$QUEUE" | sed 's/^- \[ \] //' || true)"
if [ -z "$Q" ]; then
  echo "$(date '+%F %T') queue empty"
  exit 0
fi

DATE="$(date +%F)"
SLUG="$(printf '%s' "$Q" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\{1,\}/-/g; s/^-//; s/-$//' | cut -c1-48)"
OUT="research/$DATE-$SLUG.md"

PROMPT_FILE="${PROMPT_FILE:-PROMPT.md}"   # set PROMPT_FILE=PROMPT-DEEP.md for the deep method
PROMPT="$(sed "s|\[one question from this page\]|$Q|; s|\[one question; see README for the eight worth asking\]|$Q|; s|YYYY-MM-DD-<slug>|$DATE-$SLUG|g" "$PROMPT_FILE")"

echo "$(date '+%F %T') start: $Q"
claude -p "$PROMPT" \
  --permission-mode acceptEdits \
  --allowedTools "Agent,WebSearch,WebFetch,Read,Write,Edit,Glob,Grep"

if [ -f "$OUT" ]; then
  # portable in-place edit (macOS and Linux sed differ on -i)
  tmp="$(mktemp)"
  awk -v q="$Q" -v out="$OUT" '
    !done && index($0, "- [ ] " q) == 1 { print "- [x] " q "  (" out ")"; done=1; next }
    { print }
  ' "$QUEUE" > "$tmp" && mv "$tmp" "$QUEUE"
  echo "$(date '+%F %T') wrote $OUT"
else
  echo "$(date '+%F %T') no file written for: $Q (left in queue)"
  exit 1
fi
