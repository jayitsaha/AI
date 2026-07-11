#!/bin/bash
# Tuned continuous Notion banker: bigger waves, higher concurrency across all NVIDIA keys.
set -u
cd /Users/jayitsaha/Downloads/PersonalSkillUp/AI
export NOTION_API_TOKEN="$(grep '^NOTION_API_TOKEN=' campaign/nvidia/.env | cut -d= -f2-)"
MODEL="nvidia/nemotron-3-super-120b-a12b"
CONC=${1:-9}; TARGET=${2:-2040}; LIMIT=${3:-30}
while true; do
  cur=$(cat campaign/cursor.txt)
  if [ "$cur" -ge "$TARGET" ]; then echo "=== REACHED TARGET $TARGET @$(date '+%H:%M:%S') ==="; break; fi
  echo "===== BANK WAVE @cursor=$cur conc=$CONC limit=$LIMIT $(date '+%H:%M:%S') ====="
  python3 campaign/fastqueue.py --limit "$LIMIT" >/dev/null
  grep -q '|' campaign/next.txt || { echo "queue empty"; break; }
  python3 campaign/nvidia/build_topic.py --model "$MODEL" --notion-only --concurrency "$CONC" 2>&1 | grep -E "built in|ERROR"
done
python3 campaign/fastqueue.py --reconcile
echo "===== BANKER FINISHED $(date '+%H:%M:%S') ====="
