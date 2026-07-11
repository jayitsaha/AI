import { spawn } from 'child_process';
import fs from 'fs';
const CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const files=fs.readFileSync(process.argv[2],'utf8').trim().split('\n').filter(Boolean);
const OUT=process.argv[3];
const CHUNK=5, PFCAP=6000, NAVWAIT=650;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const INJECT=`(async()=>{const hash=s=>{let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return h;};
 const sig=()=>{let p=[];document.querySelectorAll('canvas').forEach(c=>{try{p.push(hash(c.toDataURL()))}catch(e){p.push('t')}});document.querySelectorAll('svg').forEach(s=>p.push(hash(s.innerHTML)));p.push(hash((document.body.innerText||'').replace(/\\s+/g,' ').trim()));return p.join(',');};
 const isToggle=x=>{const oc=(x.getAttribute&&x.getAttribute('onclick')||'');const cl=(x.className||'')+'';return /toggle|collaps|accordion/i.test(oc)||/section-header|section-toggle|card-header|collaps/i.test(cl)||x.tagName==='DIV'||x.tagName==='SUMMARY';};
 const nb=()=>{
   // 1) explicit stepper button IDs
   for(const id of ['btnNext','nextBtn','btn-next','next-btn','nextStep','btn_next','stepNext','next']){const e=document.getElementById(id);if(e&&!e.disabled&&e.offsetParent!==null)return e;}
   // 2) real BUTTON/A elements (never toggles/divs) whose label says next
   const a=[...document.querySelectorAll('button, a[role=button], a.btn, .nav-btn')].filter(x=>!isToggle(x));
   return a.find(x=>/(^|[^a-z])next|→|»|›|forward|step\\s*\\+/i.test((x.textContent||'')+' '+(x.id||'')+' '+((x.getAttribute&&x.getAttribute('aria-label'))||''))&&!x.disabled&&x.offsetParent!==null);
 };
 const psleep=ms=>new Promise(r=>setTimeout(r,ms));for(let w=0;w<60&&document.readyState!=='complete';w++)await psleep(100);await psleep(400);await new Promise(r=>requestAnimationFrame(()=>setTimeout(r,300)));for(let w=0;w<40&&!nb();w++)await psleep(100);const st=[sig()];let clk=0,fb=false;
 for(let i=0;i<12;i++){const b=nb();if(!b)break;fb=true;b.click();clk++;await new Promise(r=>requestAnimationFrame(()=>setTimeout(r,200)));st.push(sig());}
 return JSON.stringify({fb,clk,uniq:new Set(st).size});})()`;
function cdp(ws){let id=0;const p=new Map();const s=new Map();return new Promise(res=>{ws.onmessage=m=>{const d=JSON.parse(m.data);if(d.id&&p.has(d.id)){p.get(d.id)(d);p.delete(d.id);}else if(d.method){const h=s.get(d.sessionId);if(h)h(d);}};res({send:(m,pa={},sid)=>new Promise(r=>{const i=++id;p.set(i,r);ws.send(JSON.stringify({id:i,method:m,params:pa,sessionId:sid}));}),on:(sid,fn)=>s.set(sid,fn)});});}
async function runChunk(chunk,port,out){
  const ch=spawn(CHROME,["--headless=new",`--remote-debugging-port=${port}`,"--no-first-run","--no-default-browser-check","--disable-gpu","--user-data-dir=/tmp/qc4_"+port+"_"+process.pid],{stdio:'ignore'});
  let ws;try{let url;for(let i=0;i<40;i++){try{url=(await(await fetch(`http://127.0.0.1:${port}/json/version`)).json()).webSocketDebuggerUrl;break;}catch(e){await sleep(250);}}
    ws=new WebSocket(url);await new Promise(r=>ws.onopen=r);const c=await cdp(ws);
    for(const f of chunk){let v;try{
      v=await Promise.race([(async()=>{
      const {result:{targetId}}=await c.send('Target.createTarget',{url:'about:blank'});
      const {result:{sessionId}}=await c.send('Target.attachToTarget',{targetId,flatten:true});
      const errs=[];c.on(sessionId,d=>{if(d.method==='Runtime.exceptionThrown'){const e=d.params.exceptionDetails;errs.push((e.exception&&e.exception.description||e.text||'exc').split('\n')[0].slice(0,90));}});
      await c.send('Runtime.enable',{},sessionId);await c.send('Page.enable',{},sessionId);
      await Promise.race([c.send('Page.navigate',{url:'file://'+process.cwd()+'/'+f},sessionId),sleep(4000)]);await sleep(NAVWAIT);
      const r=await Promise.race([c.send('Runtime.evaluate',{expression:INJECT,awaitPromise:true,returnByValue:true},sessionId),sleep(PFCAP).then(()=>({t:1}))]);
      let vv;if(r.t)vv={ok:false,why:'timeout'};else{const x=JSON.parse(r.result.result.value);const le=errs.filter(e=>!/favicon/i.test(e));
        if(le.length)vv={ok:false,why:'JSERR:'+le[0].slice(0,60)};else if(!x.fb)vv={ok:false,why:'NO-NEXT-BTN'};else if(x.uniq<=1)vv={ok:false,why:'DEAD-NAV'};else vv={ok:true};}
      await c.send('Target.closeTarget',{targetId},sessionId).catch(()=>{});
      return vv;})(), sleep(20000).then(()=>({ok:false,why:'hang'}))]);
    }catch(e){v={ok:false,why:'harness'};}
      const name=f.split('/').pop().replace('_explainer.html','');
      if(!v.ok)fs.appendFileSync(out,`FAULTY\t${name}\t${v.why}\n`);
      fs.appendFileSync(out,`.done\t${name}\t${v.ok?'ok':v.why}\n`);
    }
  }catch(e){}finally{try{ws&&ws.close();}catch(e){}ch.kill('SIGKILL');}
}
const main=async()=>{fs.writeFileSync(OUT,'');let port=9500;
  for(let i=0;i<files.length;i+=CHUNK){await runChunk(files.slice(i,i+CHUNK),port++,OUT);}
  const lines=fs.readFileSync(OUT,'utf8').split('\n');
  const faulty=lines.filter(l=>l.startsWith('FAULTY'));const done=lines.filter(l=>l.startsWith('.done'));
  fs.appendFileSync(OUT,`\nHEADLESS QC COMPLETE: checked=${done.length} FAULTY=${faulty.length}\n`);
};
main();
