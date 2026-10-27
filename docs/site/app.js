/* Deterministic offline demo. No network calls, storage, analytics or user input HTML. */
(function(root){
'use strict';
const weights={narrow:[.75,.25],broad:[.25,.75]};
const probs={'archive-a':[.8,.1],'archive-b':[.7,.2],'north-field':[.9,.1],'south-field':[.1,.9]};
const joint={'000':21740,'001':17054,'010':3331,'011':1702,'100':5955,'101':45064,'110':229,'111':4925};
function audit(selected, independent){
 const groups=independent?selected.map(s=>[s]):(selected.length?[selected]:[]);
 const coverage={},rank=[];
 for(const [m,ws] of Object.entries(weights)){
  let lower=0,upper=0;
  ws.forEach((w,i)=>{let minMiss=1,maxMiss=1;groups.forEach(g=>{const ps=g.map(s=>probs[s][i]);minMiss*=1-Math.min(1,ps.reduce((a,b)=>a+b,0));maxMiss*=1-Math.max(...ps)});lower+=w*(1-maxMiss);upper+=w*(1-minMiss)});
  coverage[m]={lower,upper};
 }
 for(const name of ['north-field','south-field']){
  const gains={};
  for(const [m,ws] of Object.entries(weights)){
   let lower=0,upper=0;
   ws.forEach((w,i)=>{let l=probs[name][i],h=l;groups.forEach(g=>{const ps=g.map(s=>probs[s][i]);l*=1-Math.min(1,ps.reduce((a,b)=>a+b,0));h*=1-Math.max(...ps)});lower+=w*l;upper+=w*h});gains[m]={lower,upper};
  }
  rank.push({name,gains,worst:Math.min(...Object.values(gains).map(g=>g.lower))});
 }
 rank.sort((a,b)=>b.worst-a.worst||a.name.localeCompare(b.name));
 return {synthetic:true,selected,independent_archives:independent,coverage,rank,warning:'Invented toy inputs, not astronomical coverage or telescope recommendations.'};
}
function flagCount(indices){return Object.entries(joint).reduce((s,[key,n])=>s+(indices.some(i=>key[i]==='1')?n:0),0)}
if(typeof module!=='undefined')module.exports={audit,flagCount,joint};
if(typeof document==='undefined')return;
const $=id=>document.getElementById(id);let current;
const pct=x=>(100*x).toFixed(2)+'%';
function draw(){
 const selected=['archive-a','archive-b'].filter(s=>$(s).checked), independent=document.querySelector('input[name="dependence"]:checked').value==='independent';
 current=audit(selected,independent);
 $('coverage').replaceChildren();$('ranking').replaceChildren();
 for(const [m,v] of Object.entries(current.coverage)){
  const row=document.createElement('div');row.className='result-row';
  const title=document.createElement('div');title.className='row-head';
  const name=document.createElement('strong');name.textContent=m==='narrow'?'Narrow toy model':'Broad toy model';
  const value=document.createElement('span');value.textContent=pct(v.lower)+' to '+pct(v.upper);title.append(name,value);
  const bar=document.createElement('div');bar.className='bar';bar.setAttribute('aria-hidden','true');
  const hi=document.createElement('span');hi.className='interval';hi.style.width=100*v.upper+'%';
  const lo=document.createElement('span');lo.className='interval-known';lo.style.width=100*v.lower+'%';bar.append(hi,lo);row.append(title,bar);$('coverage').append(row);
 }
 current.rank.forEach((r,i)=>{
  const row=document.createElement('div');row.className='result-row'+(i===0?' winner':'');
  const title=document.createElement('div');title.className='row-head';
  const name=document.createElement('strong');name.textContent=(i+1)+'. '+r.name.replace('-',' ')+' (toy)';
  const val=document.createElement('span');val.className='rank-value';val.textContent=(100*r.worst).toFixed(2)+' pp minimum gain';title.append(name,val);row.append(title);$('ranking').append(row);
 });
}
function real(){const n=flagCount([...document.querySelectorAll('.survey:checked')].map(el=>Number(el.value)));$('real-fraction').textContent=(n/1000).toFixed(2)+'%';$('real-count').textContent=n.toLocaleString('en-US')+' of 100,000 model particles have at least one selected flag.';$('real-bar').style.width=(n/1000)+'%'}
document.querySelectorAll('.controls input').forEach(el=>el.addEventListener('change',draw));
document.querySelectorAll('.survey').forEach(el=>el.addEventListener('change',real));
$('reset').addEventListener('click',()=>{$('archive-a').checked=$('archive-b').checked=true;document.querySelector('input[value="shared"]').checked=true;draw()});
$('download').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(current,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='synthetic-p9-audit.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
draw();real();
})(typeof globalThis!=='undefined'?globalThis:this);
