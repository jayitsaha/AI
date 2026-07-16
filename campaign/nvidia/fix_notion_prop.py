#!/usr/bin/env python3
"""Fix the 'Explainer URL' page property: rewrite broken /AI/explainers/ -> /PersonalSkillUp/AI/explainers/.
Only rewrites URLs starting with the wrong prefix; correct ones are left untouched.
  python3 fix_notion_prop.py [START] [END]   env: SLEEP (default 0.34)
"""
import json,os,sys,ssl,time,urllib.request
AI=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOK=os.environ["NOTION_API_TOKEN"]; ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
ids=json.load(open(os.path.join(AI,"topic_page_ids.json"))); topics=list(ids.keys())
WRONG="https://jayitsaha.github.io/AI/explainers/"
BASE ="https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/"
PROP="Explainer URL"
START=int(sys.argv[1]) if len(sys.argv)>1 else 0
END  =int(sys.argv[2]) if len(sys.argv)>2 else len(topics)
SLEEP=float(os.environ.get("SLEEP","0.34"))

def api(method,url,body=None):
    for k in range(6):
        try:
            data=json.dumps(body).encode() if body is not None else None
            req=urllib.request.Request(url,data=data,method=method,
                headers={"Authorization":f"Bearer {TOK}","Notion-Version":"2022-06-28","Content-Type":"application/json"})
            return json.load(urllib.request.urlopen(req,context=ctx,timeout=20))
        except urllib.error.HTTPError as e:
            if e.code in(429,409,502,503,504) and k<5: time.sleep(2*(k+1)); continue
            raise
        except Exception:
            if k<5: time.sleep(1.5); continue
            raise

fixed=already=nourl=noprop=err=0
for i in range(START,END):
    pid=ids[topics[i]]
    try:
        p=api("GET",f"https://api.notion.com/v1/pages/{pid}")
        prop=p.get("properties",{}).get(PROP)
        if not prop or prop.get("type")!="url":
            noprop+=1
        else:
            u=prop.get("url") or ""
            if u.startswith(WRONG):
                newu=u.replace(WRONG,BASE)
                api("PATCH",f"https://api.notion.com/v1/pages/{pid}",{"properties":{PROP:{"url":newu}}})
                fixed+=1
            elif u.startswith(BASE): already+=1
            else: nourl+=1
    except Exception: err+=1
    if (i-START)%25==0: print(f"[{i}] fixed={fixed} already={already} nourl/other={nourl} noprop={noprop} err={err}",flush=True)
    time.sleep(SLEEP)
print(f"DONE range {START}-{END}: fixed={fixed} already_ok={already} nourl/other={nourl} noprop={noprop} err={err}",flush=True)
