#!/usr/bin/env python3
"""Fix Notion explainer embeds: insert missing /PersonalSkillUp/ path segment,
and add embeds to pages whose explainer file exists but has no embed."""
import json,os,re,time,urllib.request,ssl,sys
AI=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def slug(t):
    s=t.split(":")[0].split("(")[0].strip().lower(); s=re.sub(r"[^a-z0-9]+","_",s).strip("_"); return re.sub(r"_+","_",s)[:48] or "topic"
ids=json.load(open(os.path.join(AI,"topic_page_ids.json"))); topics=list(ids.keys())
TOK=os.environ["NOTION_API_TOKEN"]; ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
H={"Authorization":f"Bearer {TOK}","Notion-Version":"2022-06-28","Content-Type":"application/json"}
BASE="https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/"
WRONG="https://jayitsaha.github.io/AI/explainers/"
def api(method,url,body=None):
    for k in range(5):
        try:
            data=json.dumps(body).encode() if body is not None else None
            req=urllib.request.Request(url,data=data,headers=H,method=method)
            return json.loads(urllib.request.urlopen(req,timeout=40,context=ctx).read())
        except urllib.error.HTTPError as e:
            if e.code in(429,409,502,503,504) and k<4: time.sleep(2*(k+1)); continue
            raise
        except Exception:
            if k<4: time.sleep(1.5); continue
            raise
START=int(sys.argv[1]) if len(sys.argv)>1 else 0
END=int(sys.argv[2]) if len(sys.argv)>2 else len(topics)
fixed_url=added=already=nofile=err=0
for i in range(START,END):
    t=topics[i]; pid=ids[t]; sg=slug(t)
    correct=f"{BASE}{sg}_explainer.html"
    file_ok=os.path.exists(os.path.join(AI,"AI","explainers",f"{sg}_explainer.html"))
    try:
        results=[]; cur=None
        while True:  # paginate ALL blocks (pages can exceed 100) so we never miss an existing embed
            u=f"https://api.notion.com/v1/blocks/{pid}/children?page_size=100"+(f"&start_cursor={cur}" if cur else "")
            r=api("GET",u); results+=r["results"]
            if not r.get("has_more"): break
            cur=r["next_cursor"]
        r={"results":results}
    except Exception as e:
        err+=1; continue
    emb=[b for b in r["results"] if b["type"]=="embed" and "explainer" in (b.get("embed",{}).get("url") or "")]
    if emb:
        for b in emb:
            u=b["embed"]["url"]
            if u.startswith(WRONG):
                newu=u.replace(WRONG,BASE)
                try: api("PATCH",f"https://api.notion.com/v1/blocks/{b['id']}",{"embed":{"url":newu}}); fixed_url+=1
                except Exception: err+=1
            else:
                already+=1
    else:
        if file_ok:
            try:
                api("PATCH",f"https://api.notion.com/v1/blocks/{pid}/children",
                    {"children":[{"type":"embed","embed":{"url":correct}}]}); added+=1
            except Exception: err+=1
        else:
            nofile+=1
    if (i-START)%25==0: print(f"[{i}] fixed_url={fixed_url} added={added} already_ok={already} nofile={nofile} err={err}",flush=True)
    time.sleep(float(os.environ.get("SLEEP","0.34")))  # ~3 req/s Notion limit
print(f"DONE range {START}-{END}: fixed_url={fixed_url} added={added} already_ok={already} nofile(no embed,no file)={nofile} err={err}",flush=True)
