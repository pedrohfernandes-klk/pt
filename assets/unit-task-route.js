/* Opt-in routes for M1, M2, M4 and M7: teacher assessment stays in Teams. */
(function () {
 "use strict";
 function read(key) { try { return JSON.parse(localStorage.getItem(key) || "null"); } catch (_) { return null; } }
 function raw(key) { try { return localStorage.getItem(key) || ""; } catch (_) { return ""; } }
 function exercise(id) {
  var all=read("epi-pt-longos");
  if(all&&all.feitas&&all.feitas[id])return true;
  var state=read("epi-pt-"+id)||{};
  return !!(state.fim||(state.n&&state.i>=state.n));
 }
 function lessonDone(step) {
  if(step.licao)return !!(read("licao-"+step.licao)||{}).lida;
  return !!(step.exs&&step.exs.length&&step.exs.every(exercise));
 }
 function challengeKey(module,n) { return (module==="M4"?"desafio-":"desafio-unidade-v2-")+module+"-u"+n; }
 function historicalKeys(module,n) {
  return ["percurso-"+module+"-u"+n,"percurso-v2-"+module+"-u"+n,
   "percurso-sintese-"+module+"-u"+n,"desafio-"+module+"-u"+n,
   "desafio-unidade-v2-"+module+"-u"+n];
 }
 // At least one question from each lesson of the unit, then the rest at random (the M2 rule before 27/10).
 function pick(unit) {
  var pool=EPIJogo.baralhar(unit.pool.slice()),chosen=[];
  (unit.licoes||[]).forEach(function(id){
   var item=pool.find(function(x){return x._l===id&&chosen.indexOf(x)<0;});
   if(item&&chosen.length<8)chosen.push(item);
  });
  pool.forEach(function(x){if(chosen.length<8&&chosen.indexOf(x)<0)chosen.push(x);});
  return EPIJogo.baralhar(chosen);
 }
 function mount(options) {
  if(!options||!["M1","M2","M4","M7"].includes(options.module))return;
  var units=options.units,module=options.module;
  function paint() {
   var next=null;
   units.forEach(function(unit){
    var section=document.querySelector('.unidade[data-u="'+unit.n+'"]');
    if(!section)return;
    var count=0;
    unit.passos.forEach(function(step){
     var done=lessonDone(step),li=section.querySelector('li[data-passo="'+step.id+'"]');
     if(done)count++;
     if(li){
      var chip=li.querySelector("[data-chip]");
      if(chip){chip.textContent=done?"feito":"por fazer";chip.className="chip"+(done?" feito":"");}
      var detail=li.querySelector("[data-k]");
      if(detail&&step.licao)detail.textContent=done?"lição feita":"lição por fazer";
      if(!next&&!done)next=li.querySelector("a");
     }
    });
    var progress=section.querySelector("[data-prog]");
    if(progress)progress.textContent=count+" de "+unit.passos.length+" lições feitas · tarefa individual com consulta";
    var bar=section.querySelector("[data-barra]");
    if(bar)bar.style.width=Math.round(count/Math.max(1,unit.passos.length)*100)+"%";
    var ok=section.querySelector("[data-ok]");
    if(ok)ok.hidden=true; // No automatic completion or quality claim for the task.
   });
   var entry=document.querySelector("[data-module-next]"),label=document.querySelector("[data-module-next-label]");
   if(entry&&label){
    if(next){entry.setAttribute("href",next.getAttribute("href"));label.textContent="Continuar: "+next.querySelector(".t").textContent;}
    else {entry.setAttribute("href","#tarefa-unidade-1");label.textContent="Consultar as aulas de tarefa";}
   }
   document.querySelectorAll("[data-desafio-estado]").forEach(function(node){
    var state=read(challengeKey(module,node.dataset.desafioEstado))||{};
    node.textContent=state.tentativas?"Registo do arquivo: melhor "+(state.melhor||0)+" de "+(state.total||8):"Sem tentativas guardadas neste arquivo.";
   });
  }
  var archive=document.getElementById("arquivo-percurso");
  if(archive&&new URLSearchParams(location.search).get("arquivo")==="1"){
   archive.hidden=false;
   archive.querySelectorAll("[data-cartaz-archive]").forEach(function(slot){slot.setAttribute("data-cartaz",slot.getAttribute("data-cartaz-archive"));});
   if(window.EPICartaz)window.EPICartaz.montar(archive);
   var host=archive.querySelector("[data-route-history]");
   if(host){
    var found=false;
    // Read every historic stage, including those merged when units were reorganised.
    for(var n=1;n<=Math.max(units.length,module==="M7"?5:module==="M2"?4:module==="M1"?3:units.length);n++){
     historicalKeys(module,n).forEach(function(key){
      var value=raw(key);
      if(!value)return;
      found=true;var title=document.createElement("h3"),text=document.createElement("pre");
      title.textContent="Registo guardado · "+key;text.textContent=value;text.style.whiteSpace="pre-wrap";text.style.overflowWrap="anywhere";
      host.appendChild(title);host.appendChild(text);
     });
    }
    ["percurso-"+module,"percurso-"+module+"-antes-unidades"].forEach(function(key){
     var value=raw(key);if(!value)return;
     found=true;var title=document.createElement("h3"),text=document.createElement("pre");
     title.textContent="Resumo anterior · "+key;text.textContent=value;text.style.whiteSpace="pre-wrap";text.style.overflowWrap="anywhere";host.appendChild(title);host.appendChild(text);
    });
    if(!found){var p=document.createElement("p");p.textContent="Não há registos anteriores neste aparelho.";host.appendChild(p);}
   }
  }
  // Optional practice uses the old pool and key. It never completes a unit or task.
  document.querySelectorAll("[data-desafio]").forEach(function(button){
   button.addEventListener("click",function(){
    var unit=units.find(function(u){return String(u.n)===button.dataset.desafio;});
    if(!unit||!unit.pool.length||!window.EPIJogo)return;
    var key=challengeKey(module,unit.n);
    var questions=pick(unit);
    EPIJogo.montar({marca:"Arquivo · Unidade "+unit.n,itens:questions,chave:key,titulo:"Perguntas do arquivo",mostrarAnterior:false,fim:paint});
   });
  });
  paint();
  // 28/10/2026: a âncora antiga #desafio-unidade-N (fim da lição M2-F09, congelada) aponta para o arquivo escondido;
  // fora do arquivo, leva à aula de tarefa da mesma unidade, à vista e assinalada.
  function oldChallengeAnchor() {
   var match=/^#desafio-unidade-(\d+)$/i.exec(location.hash||"");
   if(!match)return;
   var old=document.getElementById("desafio-unidade-"+match[1]),task=document.getElementById("tarefa-unidade-"+match[1]);
   if(!task||(old&&!old.closest("[hidden]")))return;
   try{history.replaceState(history.state,"","#tarefa-unidade-"+match[1]);}catch(_){}
   task.classList.add("aqui");
   setTimeout(function(){task.scrollIntoView({block:"center"});},50);
  }
  oldChallengeAnchor();
  window.addEventListener("hashchange",oldChallengeAnchor);
  window.addEventListener("focus",paint);window.addEventListener("pageshow",paint);
  document.addEventListener("visibilitychange",function(){if(!document.hidden)paint();});
 }
 window.EPIUnitTaskRoute={mount:mount,lessonDone:lessonDone,historicalKeys:historicalKeys,pick:pick};
})();
