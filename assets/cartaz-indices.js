/* 01/11/2026: apresentação dos índices. O motor existente continua a decidir o percurso.
 * Não escreve localStorage. Uma visita nunca é uma conclusão. */
(function(){
 'use strict';
 const main=document.querySelector('main.cz-index'),source=document.getElementById('cz-index-route');
 if(!main||!source||!window.EPICartaz||!window.EPIUnitTaskRoute)return;
 const units=JSON.parse(source.textContent),previous=new Map();let initialized=false,sequence=0;
 const read=key=>{try{return JSON.parse(localStorage.getItem(key)||'null')}catch{return null}};
 const date=value=>{if(!value)return null;const t=typeof value==='object'?value.t:null;if(typeof t!=='number'||!Number.isFinite(t))return null;const d=new Date(t);return Number.isFinite(d.getTime())?`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`:null};
 function completionDate(step){if(step.licao)return date(read('licao-'+step.licao));const longos=read('epi-pt-longos')||{};const ds=(step.exs||[]).map(id=>{const t=longos.feitas&&longos.feitas[id];return date(typeof t==='number'?{t}:read('epi-pt-'+id))});return ds.length&&ds.every(Boolean)?ds.sort().at(-1):null}
 function text(node,value){if(node&&node.textContent!==value)node.textContent=value}
 function anchor(){try{return document.getElementById(decodeURIComponent(location.hash.slice(1)))}catch{return null}}
 function paint(){
  const sala=new URLSearchParams(location.search).get('projetar')==='1'||document.documentElement.matches('.em-projecao,.epi-projection');
  main.classList.toggle('cz-sala',sala);
  let next=null,total=0,doneCount=0;
  for(const unit of units){
   const fold=main.querySelector('[data-cz-unit="'+unit.n+'"]');let doneUnit=0;
   for(const step of unit.passos){
    const row=document.getElementById(step.id);if(!row)continue;
    const done=EPIUnitTaskRoute.lessonDone(step),current=!next&&!done;if(current)next=row;
    total++;if(done){doneCount++;doneUnit++}
    const a=row.querySelector('a'),chip=row.querySelector('[data-chip]'),label=sala?'':EPICartaz.stateLabel({done,next:current,date:done?completionDate(step):null});
    a.classList.toggle('current',!sala&&current);a.toggleAttribute('data-cz-next',!sala&&current);
    if(chip){
     chip.className='chip cz-state'+(done?' done':current?' current':'');
     if(label){if(!chip.querySelector('[data-cz-state-text]'))chip.innerHTML='<span data-cz-point aria-hidden="true"></span><span data-cz-state-text></span>';text(chip.querySelector('[data-cz-state-text]'),label);const point=chip.querySelector('[data-cz-point]');point.classList.toggle('cz-motion-point',done);text(point,done?'✓':'');if(initialized&&previous.get(step.id)===false&&done)EPICartaz.motion.complete(point,{before:false,after:true,event:step.id+':'+(++sequence)});}
     else text(chip,'');
    }
    previous.set(step.id,done);
   }
   const here=next&&fold.contains(next);text(fold.querySelector('.cz-index-fold-state'),sala?'':here?'A seguir':doneUnit===unit.passos.length?'Passos feitos':'');
   fold.querySelector('.cz-index-fold-state').classList.toggle('feita',!sala&&!here&&doneUnit===unit.passos.length);
   if(sala)fold.open=true;else if(!initialized&&matchMedia('(max-width:639px)').matches&&!new URLSearchParams(location.search).has('projetar'))fold.open=!!(here||fold.contains(anchor()));else if(here||fold.contains(anchor()))fold.open=true;
  }
  // 02/11/2026: decisão 134. A linha de estado saiu com a caixa «A seguir»; se existir numa cópia antiga, continua a funcionar.
  const status=main.querySelector('.cz-index-status');if(status){status.hidden=sala;text(status,doneCount?`${doneCount} de ${total} passos feitos.`:'Ainda não há passos feitos.');}
  const label=main.querySelector('[data-module-next-label]');if(label&&!doneCount)text(label,label.textContent.replace(/^Continuar: /,'Começar: '));
  // Mantém o destino e o rótulo calculados pelo motor, bem como todos os contadores.
  main.querySelectorAll('[data-prog]').forEach(e=>text(e,e.textContent.replace(/ · /g,', ')));
  initialized=true;
 }
 paint();
 window.addEventListener('focus',paint);window.addEventListener('pageshow',paint);
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)paint()});
 document.fonts.ready.then(()=>EPICartaz.motion.play(main.querySelector('.cz-motion-title')));
 // A linha só anima quando chega ao ecrã; não atrasa nem desloca qualquer ação.
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){EPICartaz.motion.play(e.target);observer.unobserve(e.target)}},{threshold:.5});main.querySelectorAll('[data-cz-route-line]').forEach(e=>observer.observe(e));}
})();
