#!/usr/bin/env python3
"""Dedupe explainer embeds. Pages with >100 blocks got duplicate embeds because the
add-branch only inspected the first 100 blocks. Paginate ALL blocks, keep exactly one
correct (/PersonalSkillUp/) explainer embed per page, delete the rest.
  python3 dedup_embeds.py [START] [END]   env: SLEEP (default 0.34)
"""
import json,os,sys,ssl,time,urllib.request,urllib.error
AI=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOK=os.environ["NOTION_API_TOKEN"]; ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
ids=json.load(open(os.path.join(AI,"topic_page_ids.json"))); topics=list(ids.keys())
WRONG="https://jayitsaha.github.io/AI/explainers/"
BASE ="https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/"
START=int(sys.argv[1]) if len(sys.argv)>1 else 0
END  =int(sys.argv[2]) if len(sys.argv)>2 else len(topics)
SLEEP=float(os.environ.get("SLEEP","0.34"))
H={"Authorization":f"Bearer {TOK}","Notion-Version":"2022-06-28","Content-Type":"application/json"}

def api(method,url,body=None):
    for k in range(6):
        try:
            data=json.dumps(body).encode() if body is not None else None
            req=urllib.request.Request(url,data=data,method=method,headers=H)
            return json.loads(urllib.request.urlopen(req,timeout=40,context=ctx).read())
        except urllib.error.HTTPError as e:
            if e.code in(429,409,502,503,504) and k<5: time.sleep(2*(k+1)); continue
            raise
        except Exception:
            if k<5: time.sleep(1.5); continue
            raise

def all_kids(pid):
    out=[]; cur=None
    while True:
        u=f"https://api.notion.com/v1/blocks/{pid}/children?page_size=100"+(f"&start_cursor={cur}" if cur else "")
        r=api("GET",u); out+=r["results"]
        if not r.get("has_more"): break
        cur=r["next_cursor"]; time.sleep(0.15)
    return out

def eurl(b):
    return (b.get("embed",{}).get("url") or "") if b.get("type")=="embed" else ""

deduped=urlfixed=clean=err=0; pages_hit=0
for i in range(START,END):
    pid=ids[topics[i]]
    try:
        bs=all_kids(pid)
        embs=[b for b in bs if "explainer" in eurl(b).lower()]
        if len(embs)<=1:
            # ensure the single one is correct
            if embs and eurl(embs[0]).startswith(WRONG):
                api("PATCH",f"https://api.notion.com/v1/blocks/{embs[0]['id']}",
                    {"embed":{"url":eurl(embs[0]).replace(WRONG,BASE)}}); urlfixed+=1
            else: clean+=1
            continue
        # >1 embed: pick keeper = first correct one, else first (and fix its url)
        keeper=next((b for b in embs if eurl(b).startswith(BASE)), None)
        if keeper is None:
            keeper=embs[0]
            if eurl(keeper).startswith(WRONG):
                api("PATCH",f"https://api.notion.com/v1/blocks/{keeper['id']}",
                    {"embed":{"url":eurl(keeper).replace(WRONG,BASE)}}); urlfixed+=1
        for b in embs:
            if b["id"]==keeper["id"]: continue
            try: api("DELETE",f"https://api.notion.com/v1/blocks/{b['id']}"); deduped+=1
            except Exception: err+=1
        pages_hit+=1
    except Exception: err+=1
    if (i-START)%25==0: print(f"[{i}] pages_with_dupes={pages_hit} deleted={deduped} urlfixed={urlfixed} clean={clean} err={err}",flush=True)
    time.sleep(SLEEP)
print(f"DONE {START}-{END}: pages_with_dupes={pages_hit} embeds_deleted={deduped} urlfixed={urlfixed} clean_single={clean} err={err}",flush=True)
