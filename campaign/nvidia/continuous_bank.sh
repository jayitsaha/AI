#!/bin/bash
# Continuously bank NVIDIA Notion pages (120B) until cursor reaches the §33 target.
# Won't stop until done. Usage: bash continuous_bank.sh [concurrency] [target]
set -u
cd /Users/jayitsaha/Downloads/PersonalSkillUp/AI
MODEL="nvidia/nemotron-3-super-120b-a12b"
CONC=${1:-8}
TARGET=${2:-1318}

while true; do
  cur=$(cat campaign/cursor.txt)
  if [ "$cur" -ge "$TARGET" ]; then echo "=== REACHED TARGET $TARGET @$(date '+%H:%M:%S') ==="; break; fi
  echo "===== BANK WAVE @cursor=$cur $(date '+%H:%M:%S') ====="
  python3 campaign/fastqueue.py --limit 20 >/dev/null
  grep -q '|' campaign/next.txt || { echo "queue empty"; break; }
  python3 campaign/nvidia/build_topic.py --model "$MODEL" --notion-only --concurrency "$CONC" 2>&1 \
    | grep -E "built in|ERROR"
done
python3 campaign/fastqueue.py --reconcile
echo "===== BANKER FINISHED $(date '+%H:%M:%S') ====="
