const box=document.getElementById('message');
const count=document.getElementById('count');
const button=document.getElementById('analyze');
const statusBox=document.getElementById('status');
const result=document.getElementById('result');
const empty=document.getElementById('empty-state');
box.addEventListener('input',()=>count.textContent=box.value.length+' / 1000');
document.querySelectorAll('.sample-btn').forEach(btn=>btn.addEventListener('click',()=>{box.value=btn.dataset.sample;box.dispatchEvent(new Event('input'));box.focus();}));
function addItems(list,items,fallback){list.replaceChildren();(items&&items.length?items:[fallback]).forEach(value=>{const li=document.createElement('li');li.textContent=value;list.appendChild(li);});}
button.addEventListener('click',async()=>{
  const text=box.value.trim();statusBox.textContent='';result.classList.add('hidden');
  if(!text){statusBox.textContent='Pehle ek sample message likhein.';return;}
  button.disabled=true;button.querySelector('span').textContent='Scanning...';
  try{
    const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
    const data=await response.json();if(!response.ok)throw new Error(data.error||'Analysis failed');
    const threat=!!data.threat_detected;const flagged=data.label==='potentially_harmful';const level=data.risk?.level||'low';
    const banner=document.querySelector('.result-banner');banner.className='result-banner'+(threat?' is-high':(!threat&&flagged?' is-review':''));
    document.getElementById('result-icon').textContent=threat?'⚠':(flagged?'◈':'✓');
    document.getElementById('result-title').textContent=data.result;
    const badge=document.getElementById('risk-badge');badge.textContent=threat?'HIGH PRIORITY':(flagged?'REVIEW':'LOW SIGNAL');
    document.getElementById('confidence').textContent=data.confidence===null?'N/A':data.confidence+'%';
    document.getElementById('confidence-bar').style.width=(data.confidence||0)+'%';
    addItems(document.getElementById('signals'),data.signals,'No extra phrase signal detected.');
    document.getElementById('risk-title').textContent=threat?'IMPORTANT — TAKE THESE STEPS':'SAFETY GUIDANCE';
    const riskBlock=document.querySelector('.risk-block');riskBlock.classList.toggle('urgent',threat);
    addItems(document.getElementById('risk-steps'),data.risk?.steps,'Talk to a trusted adult if you feel unsafe.');
    document.getElementById('result-note').textContent=data.note+' '+data.privacy;
    empty.classList.add('hidden');result.classList.remove('hidden');
    result.scrollIntoView({behavior:'smooth',block:'nearest'});
  }catch(error){statusBox.textContent=error.message;}
  finally{button.disabled=false;button.querySelector('span').textContent='Run AI analysis';}
});
