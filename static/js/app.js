let currentDFAResult = {states:[],alpha:[],start:"",finals:[],trans:[]};
let currentNFAResult = null;
let nfaLayoutTree = null;

function switchTab(tabId, el) {
  document.querySelectorAll(".nav-link").forEach(x => x.classList.remove("activeTab"));
  document.querySelectorAll(".panel").forEach(x => x.classList.remove("activeTab"));
  el.classList.add("activeTab");
  document.getElementById(tabId).classList.add("activeTab");
  setTimeout(() => Object.keys(automataGraphs).forEach(fitGraph), 50);
}
function parseInputList(value){return value.split(",").map(x=>x.trim()).filter(Boolean)}
function esc(value){return String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}

function buildMatrix(prefix, states, alpha, containerId) {
  const container=document.getElementById(containerId);
  if(!states.length||!alpha.length){container.innerHTML='<p class="text-muted">Enter states and alphabet first.</p>';return}
  let html='<table class="trans-table"><thead><tr><th>State</th>';
  alpha.forEach(a=>html+=`<th>Input ${esc(a)}</th>`);
  html+='</tr></thead><tbody>';
  states.forEach((state,i)=>{
    html+=`<tr><td><strong>${esc(state)}</strong></td>`;
    alpha.forEach((_symbol,j)=>html+=`<td><input class="table-input" id="${prefix}_${i}_${j}" list="${prefix}_states" placeholder="state"></td>`);
    html+='</tr>';
  });
  html+=`</tbody></table><datalist id="${prefix}_states">${states.map(s=>`<option value="${esc(s)}">`).join("")}</datalist>`;
  container.innerHTML=html;
}
function collectMatrix(prefix, states, alpha, generator){
  const missing=states.some((_s,i)=>alpha.some((_a,j)=>!document.getElementById(`${prefix}_${i}_${j}`)));
  if(missing) generator();
  const transitions=[];
  states.forEach((state,i)=>alpha.forEach((symbol,j)=>{
    const input=document.getElementById(`${prefix}_${i}_${j}`);
    const target=input?input.value.trim():"";
    if(target) transitions.push({state,symbol,target});
  }));
  return transitions;
}
function config(ids,prefix,generator){
  const states=parseInputList(document.getElementById(ids.states).value);
  const alpha=parseInputList(document.getElementById(ids.alpha).value);
  return {states,alpha,start:document.getElementById(ids.start).value.trim(),finals:parseInputList(document.getElementById(ids.finals).value),trans:collectMatrix(prefix,states,alpha,generator)};
}
function generateDFAMatrix(){buildMatrix("dfa_t",parseInputList(dfa_states.value),parseInputList(dfa_alpha.value),"dfa_trans_container")}
function getDFAConfig(){return config({states:"dfa_states",alpha:"dfa_alpha",start:"dfa_start",finals:"dfa_final"},"dfa_t",generateDFAMatrix)}
function updateDFADiagram(){currentDFAResult=getDFAConfig();drawAutomata("diagram-container",currentDFAResult.states,currentDFAResult.alpha,currentDFAResult.start,currentDFAResult.finals,currentDFAResult.trans)}

async function postJSON(url,body){
  const response=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const data=await response.json();
  if(!response.ok||!data.success)throw new Error(data.message||`HTTP ${response.status}`);
  return data;
}
async function testDFAResult(){
  updateDFADiagram();
  const inputStr=dfa_input_str.value;
  try{
    const data=await postJSON("/api/dfa/test",{...currentDFAResult,input_str:inputStr});
    dfa_result.style.display="block";
    dfa_result.className=`result-box-dynamic ${data.accepted?"r-accept":"r-reject"}`;
    dfa_result.innerHTML=`<strong>${data.accepted?"DITERIMA":"DITOLAK"}</strong><br>State akhir: <code>${esc(data.final_state)}</code>`;
    dfa_trace.innerHTML=data.trace.map((step,index)=>{
      const previous=index?data.trace[index-1].state:null;
      const symbol=(step.info.match(/δ\([^,]+,\s*([^)]+)\)/)||[])[1];
      const attrs=previous&&step.state&&symbol?`onmouseenter="highlightDFA('${esc(previous)}','${esc(step.state)}','${esc(symbol)}')" onmouseleave="updateDFADiagram()"`:"";
      return `<div class="trace-step step-${step.type}" ${attrs}>${esc(step.info)}</div>`;
    }).join("");
    drawAutomata("diagram-container",currentDFAResult.states,currentDFAResult.alpha,currentDFAResult.start,currentDFAResult.finals,currentDFAResult.trans,data.final_state);
  }catch(error){alert("Gagal menguji DFA: "+error.message)}
}
function highlightDFA(from,to,symbol){drawAutomata("diagram-container",currentDFAResult.states,currentDFAResult.alpha,currentDFAResult.start,currentDFAResult.finals,currentDFAResult.trans,to,{from,to,symbol})}

function transitionTarget(transitions,state,symbol){
  const item=(transitions||[]).find(x=>x.state===state&&x.symbol===symbol);
  return item?item.target:null;
}
async function convertRegexNFA(){
  const regex=document.getElementById("regex-input").value.trim();
  if(!regex)return;
  try{
    const data=await postJSON("/api/regex/to-nfa",{regex});
    currentNFAResult=data.nfa;nfaLayoutTree=data.nfa.layoutTree;
    const headers=[...data.nfa.alpha,"E"];
    let html='<table class="trans-table"><thead><tr><th>State</th>'+headers.map(x=>`<th>${x==="E"?"ε":esc(x)}</th>`).join("")+'</tr></thead><tbody>';
    data.nfa.states.forEach(state=>{
      html+=`<tr><td><strong>${esc(state)}</strong></td>`;
      headers.forEach(symbol=>{const target=transitionTarget(data.nfa.trans,state,symbol);html+=`<td>${target&&target.length?`{ ${target.map(esc).join(", ")} }`:"∅"}</td>`});
      html+="</tr>";
    });
    document.getElementById("nfa-trans-table").innerHTML=html+"</tbody></table>";
    drawAutomata("diagram2-container",data.nfa.states,data.nfa.alpha,data.nfa.start,data.nfa.finals,data.nfa.trans);
  }catch(error){alert(error.message)}
}
async function testNFA() {
    const inputStr = document.getElementById('nfa_input_str').value;
    const resultDiv = document.getElementById('nfa_result');

    if (!currentNFAResult) return alert("Harap konstruksi NFA terlebih dahulu.");

    // PERBAIKAN: Format ulang transisi NFA agar sesuai dengan standar tuple (|||) 
    // yang diminta oleh normalizer di backend nfa.py milikmu
    let cleanTrans = {};
    for (let key in currentNFAResult.trans) {
        // Thompson dari backend mengembalikan transisi dalam format string 'q0|||a'
        cleanTrans[key] = currentNFAResult.trans[key];
    }

    const payload = {
        states: currentNFAResult.states,
        alpha: currentNFAResult.alpha,
        start: currentNFAResult.start,
        finals: currentNFAResult.finals,
        trans: cleanTrans,
        input_str: inputStr
    };

    try {
        const response = await fetch('/api/nfa/test', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        resultDiv.style.display = 'block';
        if (data.accepted) {
            resultDiv.className = 'result-box-dynamic r-accept';
            resultDiv.innerHTML = `<strong>DITERIMA</strong><br>Final active state set mencakup final state: { <code>${data.final_set.join(', ')}</code> }`;
        } else {
            resultDiv.className = 'result-box-dynamic r-reject';
            resultDiv.innerHTML = `<strong>DITOLAK</strong><br>Active state set akhir: { <code>${data.final_set.join(', ') || '∅'}</code> }`;
        }
    } catch (err) {
        alert(err.message);
    }
}

function generateMinMatrix(){buildMatrix("min_t",parseInputList(min_states.value),parseInputList(min_alpha.value),"min_trans_container")}
function getMinConfig(){return config({states:"min_states",alpha:"min_alpha",start:"min_start",finals:"min_final"},"min_t",generateMinMatrix)}
async function minimizeDFA(){
  const dfa=getMinConfig();drawAutomata("diagram3-container",dfa.states,dfa.alpha,dfa.start,dfa.finals,dfa.trans);
  try{
    const data=await postJSON("/api/dfa/minimize",dfa),m=data.minimized;
    min_result.innerHTML=`<strong>Mereduksi ${m.reduced_count} state</strong><br>${m.mapping.map(x=>`{ ${x.group.map(esc).join(", ")} } → ${esc(x.name)}`).join("<br>")}`;
    drawAutomata("diagram4-container",m.states,m.alpha,m.start,m.finals,m.trans);
  }catch(error){alert(error.message)}
}

function generateEquivMatrix(num){buildMatrix(`eq${num}_t`,parseInputList(document.getElementById(`eq${num}_states`).value),parseInputList(document.getElementById(`eq${num}_alpha`).value),`eq${num}_trans_container`)}
function getEqConfig(num){return config({states:`eq${num}_states`,alpha:`eq${num}_alpha`,start:`eq${num}_start`,finals:`eq${num}_final`},`eq${num}_t`,()=>generateEquivMatrix(num))}
async function checkEquivalence(){
  const dfa1=getEqConfig(1),dfa2=getEqConfig(2);
  drawAutomata("diagram5a-container",dfa1.states,dfa1.alpha,dfa1.start,dfa1.finals,dfa1.trans);
  drawAutomata("diagram5b-container",dfa2.states,dfa2.alpha,dfa2.start,dfa2.finals,dfa2.trans);
  try{
    const data=await postJSON("/api/dfa/equivalence",{dfa1,dfa2});
    equiv_result_card.style.display="block";
    equiv_result.innerHTML=data.equivalent?'<div class="equiv-big">≡</div><strong>EKUIVALEN</strong>':`<div class="equiv-big" style="color:var(--rose)">≢</div><strong>TIDAK EKUIVALEN</strong><div>Counterexample: <code>${esc(data.counterexample)}</code></div>`;
  }catch(error){alert(error.message)}
}
