#!/bin/bash
# Persistent Gemini HTML build+QC+commit loop. Builds what quota allows each wave,
# QCs new files (headless Chrome), commits the clean ones, queues broken ones for
# repair, sleeps, repeats until nothing is missing. "Set and forget."
set -u
cd /Users/jayitsaha/Downloads/PersonalSkillUp/AI
export START_IDX=1374
QC=campaign/qc_headless.mjs
QUEUE=campaign/gemini_repair_queue.txt
LOG=campaign/gemini/logs/autoloop.log
touch "$QUEUE"
missing() {
python3 - <<'PY'
import json,os,re
def slug(t):
    s=t.split(":")[0].split("(")[0].strip().lower(); s=re.sub(r"[^a-z0-9]+","_",s).strip("_"); return re.sub(r"_+","_",s)[:48] or "topic"
t=list(json.load(open("topic_page_ids.json")).keys()); sk=set(json.load(open("campaign/html_skip_idx.json")))
print(sum(1 for i in range(1374,2040) if i not in sk and not os.path.exists(os.path.join("AI/explainers",f"{slug(t[i])}_explainer.html"))))
PY
}
while true; do
  M=$(missing)
  echo "===== WAVE $(date '+%F %T') | missing=$M =====" >> "$LOG"
  [ "$M" -le 0 ] && { echo "ALL BUILT $(date)" >> "$LOG"; break; }
  pkill -f "remote-debugging-port=9" 2>/dev/null; rm -rf /tmp/qc4_* 2>/dev/null
  # BUILD (quota-limited; auto-skips built + ethics)
  python3 campaign/gemini/parallel_html.py 2040 16 >> "$LOG" 2>&1
  # collect new untracked files NOT already queued as broken
  git status --porcelain AI/explainers/ | awk '/^\?\?/{print $2}' > /tmp/al_all.txt
  awk -F/ '{print $3}' /tmp/al_all.txt | sed 's/_explainer.html//' > /tmp/al_slugs.txt
  : > /tmp/al_new.txt
  while read -r p; do s=$(basename "$p" | sed 's/_explainer.html//'); grep -qxF "$s" "$QUEUE" || echo "$p" >> /tmp/al_new.txt; done < /tmp/al_all.txt
  if [ -s /tmp/al_new.txt ]; then
    node "$QC" /tmp/al_new.txt /tmp/al_qc.tsv >> "$LOG" 2>&1
    grep '^\.done' /tmp/al_qc.tsv | grep 'ok$' | cut -f2 | while read -r s; do git add "AI/explainers/${s}_explainer.html"; done
    git commit -q -m "Gemini autoloop: QC-passing explainers $(date '+%F %T')" >/dev/null 2>&1 && git push -q origin AI >/dev/null 2>&1
    grep '^FAULTY' /tmp/al_qc.tsv | cut -f2 >> "$QUEUE"; sort -u "$QUEUE" -o "$QUEUE"
    echo "  committed passing; repair-queue now $(wc -l < "$QUEUE")" >> "$LOG"
  fi
  sleep 10800   # 3h; quota is daily so wait for it to free
done
