#!/bin/bash
# Bank NVIDIA Notion pages for K waves; defer HTML explainers (tracked in pending_html.tsv).
# Usage: bash campaign/nvidia/run_notion_waves.sh [K]   (default K=5, 20 topics/wave)
set -u
cd /Users/jayitsaha/Downloads/PersonalSkillUp/AI
K=${1:-5}
MODEL="nvidia/nemotron-3-super-120b-a12b"
PENDING=campaign/pending_html.tsv
touch "$PENDING"

for i in $(seq 1 "$K"); do
  echo "===== NOTION WAVE $i/$K  $(date '+%H:%M:%S') ====="
  python3 campaign/fastqueue.py --limit 20 >/dev/null
  n=$(grep -c '|' campaign/next.txt)
  if [ "$n" -eq 0 ]; then echo "queue empty — stopping"; break; fi
  # record (pageid<TAB>topic<TAB>slug) for later HTML building
  python3 campaign/nvidia/build_topic.py --print-slugs >> "$PENDING"
  # build the Notion pages only (HTML deferred)
  python3 campaign/nvidia/build_topic.py --model "$MODEL" --notion-only --concurrency 4 2>&1 \
    | grep -E "Notion:y|ERROR|built in"
done

# de-duplicate the pending list (by slug, keep first)
python3 - <<'PY'
seen=set(); out=[]
for line in open("campaign/pending_html.tsv"):
    p=line.rstrip("\n").split("\t")
    if len(p)>=3 and p[2] not in seen:
        seen.add(p[2]); out.append(line if line.endswith("\n") else line+"\n")
open("campaign/pending_html.tsv","w").writelines(out)
print("pending unique HTML topics:", len(out))
PY

python3 campaign/fastqueue.py --reconcile
echo "===== DONE: $K notion waves banked. HTML deferred (campaign/pending_html.tsv). ====="
