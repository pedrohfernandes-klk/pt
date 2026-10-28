/* A task is a consultable lesson. This adapter moves the existing nodes; it never
   scores a task, writes progress or replaces the shared EPICasca controller. */
(function () {
 "use strict";
 var page=document.querySelector("main.task-page");
 if(!page||!window.EPICasca||document.querySelector("[data-task-reader]"))return;
 var compact=page.hasAttribute("data-task-compact");
 var original=Array.from(page.childNodes),parent=page.parentNode,next=page.nextSibling;
 var root=null,controller=null,updatingHash=false,returnQuestion=null,positions=[];
 function move(node,host){positions.push({node:node,parent:node.parentNode,next:node.nextSibling});host.appendChild(node);}
 function element(tag,cls,text){var el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el;}
 try {
  var cards=[],quiz=page.querySelector(".task-quiz"),questions=quiz?Array.from(quiz.querySelectorAll("[data-task-question]")):[],
      status=page.querySelector("[data-task-status]"),title=page.querySelector("h1"),nav=page.querySelector(".task-nav"),
      unit=nav&&nav.querySelector("a:last-of-type"),unitHref=unit?unit.getAttribute("href"):"../../";
  function card(label,nodes,kind){
   var box=element("article","task-reader-card");box.id="task-card-"+(cards.length+1);
   box.setAttribute("data-task-card",String(cards.length));box.setAttribute("aria-label",label);box.tabIndex=-1;
   nodes.forEach(function(node){move(node,box);});
   cards.push({el:box,label:label,kind:kind||"reading"});return box;
  }
  var opening=card(compact?"Enunciado":"A aula de tarefa",[]);
  var before=Array.from(page.children);
  before.forEach(function(node){
   if(node===nav||node.tagName==="HEADER"){move(node,opening);return;}
   if(node.matches("[data-task-status]"))return;
   var heading=node.querySelector("h2,h3,summary"),label=heading?heading.textContent.trim():"Outros apoios";
   if(!compact&&node.id==="preparacao"){
    card("Preparar · leitura e modelo",[node]);
    questions.forEach(function(question,i){card("Preparar · pergunta "+(i+1),[question],"question");});
   }else card(compact?(node.id==="aquecer"?"Aquecer":node.id==="apoios"?"Relembrar":node.id==="entregar"?"Verificar":label):label,[node],node.id==="aquecer"?"warmup":node.id==="apoios"?"support":node.id==="produzir"?"production":node.id==="entregar"?"delivery":"reading");
  });
  // 28/10/2026: nas tarefas com aquecimento, o aquecimento é o primeiro cartão; o enunciado vem a seguir.
  var warm=cards.findIndex(function(item){return item.kind==="warmup";});
  if(compact&&warm>0){
   cards.unshift(cards.splice(warm,1)[0]);
   cards.forEach(function(item,i){item.el.id="task-card-"+(i+1);item.el.setAttribute("data-task-card",String(i));});
  }
  if(quiz&&!compact)quiz.hidden=true; // Its original question nodes now have their own cards.
  page.replaceChildren();
  cards.forEach(function(item){page.appendChild(item.el);});
  root=element("div","casca task-reader");root.setAttribute("data-casca","");root.setAttribute("data-task-reader","");
  var top=element("header","casca-topo"),brand=element("a","c-marca",unit?unit.textContent:"Aula de tarefa");
  brand.href=unitHref;brand.setAttribute("aria-label","Voltar à unidade");
  var number=element("span","c-num");number.setAttribute("data-c-num","");
  var bar=element("button","c-barra");bar.type="button";bar.setAttribute("data-c-barra","");bar.setAttribute("aria-label","Índice dos cartões de consulta");
  bar.innerHTML='<svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg>';
  var mode=element("span","c-modo");mode.setAttribute("data-c-modo","");mode.hidden=true;
  var menu=element("button","c-ic","☰");menu.type="button";menu.setAttribute("data-c-menu","");
  menu.setAttribute("aria-label","Abrir o índice da aula");menu.setAttribute("aria-expanded","false");
  top.append(brand,number,bar,mode,menu);
  // 27/10/2026: o relógio do aluno fica no enunciado; o tempo que falta acompanha os outros cartões.
  var clock=page.querySelector("[data-relogio]");
  if(clock&&clock.relogio){var mini=element("span","relogio-mini");mini.setAttribute("aria-hidden","true");clock.relogio.espelhar(mini);top.insertBefore(mini,menu);}
  var body=element("div","casca-corpo");body.tabIndex=-1;body.appendChild(page);
  if(status&&!compact){status.classList.add("task-reader-status");move(status,body);}
  var actions=element("footer","casca-acoes");actions.setAttribute("data-c-acoes","");
  var feedback=element("section","casca-folha");feedback.setAttribute("data-c-folha","");feedback.hidden=true;
  var panel=element("div","casca-menu");panel.setAttribute("data-c-painel","");panel.hidden=true;
  var panelInner=element("div","c-menu-in");panelInner.setAttribute("role","dialog");panelInner.setAttribute("aria-label","Índice da aula");
  var panelHead=element("div","c-menu-cab"),close=element("button","c-ic","✕");
  close.type="button";close.setAttribute("data-c-fecha-menu","");close.setAttribute("aria-label","Fechar o índice");
  panelHead.append(element("p","",title?title.textContent:"Aula de tarefa"),close);
  var menuNav=element("nav","task-reader-index");menuNav.setAttribute("aria-label","Cartões da aula");
  panelInner.append(panelHead,element("p","task-reader-note","Consulta livre. A barra mostra onde estás; não dá uma nota."),menuNav);
  panel.appendChild(panelInner);root.append(top,body,actions,feedback,panel);
  parent.insertBefore(root,next);
  controller=EPICasca.pagina(root);
  var current=0,menuButtons=[];
  function show(index,opts){
   opts=opts||{};index=Math.max(0,Math.min(cards.length-1,index));current=index;
   cards.forEach(function(item,i){item.el.hidden=i!==index;});
   menuButtons.forEach(function(button,i){if(i===index)button.setAttribute("aria-current","page");else button.removeAttribute("aria-current");});
   controller.num(index+1,cards.length);
   controller.barra(cards.map(function(){return "ler";}),index,function(){controller.menu.abrir();},false);
   var item=cards[index],buttons=[
    {t:"← Anterior",cls:"sec",esq:true,disabled:index===0,attrs:{"data-task-reader-prev":""},onclick:function(){show(index-1);}}
   ];
   if(item.kind==="question"&&document.getElementById("apoios")){
    buttons.push({t:"Consultar apoios",cls:"sec",href:"#apoios",attrs:{"data-task-reader-support":""}});
   }else if(returnQuestion!==null&&index!==returnQuestion){
    buttons.push({t:"Voltar à pergunta",cls:"sec",attrs:{"data-task-reader-return":""},onclick:function(){var back=returnQuestion;returnQuestion=null;show(back);}});
   }
   buttons.push({t:index===cards.length-1?"Voltar ao início":"Seguinte →",cls:"prim",
    attrs:{"data-task-reader-next":""},onclick:function(){show(index===cards.length-1?0:index+1);}});
   controller.acoes(buttons);controller.rolarTopo();
   if(opts.hash!==false){
    updatingHash=true;
    try {history.replaceState(history.state,"","#"+item.el.id);window.dispatchEvent(new Event("hashchange"));} catch(_){}
    updatingHash=false;
   }
   if(opts.focus!==false)body.focus({preventScroll:true});
  }
  cards.forEach(function(item,i){
   var button=element("button","",String(i+1)+". "+item.label);button.type="button";
   button.setAttribute("data-task-reader-jump",String(i));
   button.addEventListener("click",function(){controller.menu.fechar();show(i);});
   menuNav.appendChild(button);menuButtons.push(button);
  });
  function reveal(hash){
   if(!hash)return false;
   var id;try{id=decodeURIComponent(hash.replace(/^#/,""));}catch(_){return false;}
   var target=document.getElementById(id),index=cards.findIndex(function(item){return target&&(item.el===target||item.el.contains(target));});
   if(index<0)return false;
   var ancestor=target;
   while(ancestor&&ancestor!==cards[index].el){if(ancestor.tagName==="DETAILS")ancestor.open=true;ancestor=ancestor.parentElement;}
   show(index,{hash:false,focus:false});
   requestAnimationFrame(function(){target.scrollIntoView({block:"start"});controller.sombra();});
   return true;
  }
  root.addEventListener("click",function(event){
   var link=event.target.closest&&event.target.closest('a[href^="#"]');
   if(!link)return;
   var hash=link.getAttribute("href"),id;try{id=decodeURIComponent(hash.slice(1));}catch(_){return;}
   var target=document.getElementById(id);
   if(!target||!cards.some(function(item){return item.el.contains(target)||item.el===target;}))return;
   if(cards[current].kind==="question")returnQuestion=current;
   event.preventDefault();
   if(location.hash===hash)reveal(hash);else location.hash=hash;
  });
  window.addEventListener("hashchange",function(){if(!updatingHash)reveal(location.hash);});
  document.addEventListener("keydown",function(event){
   if(event.altKey||event.ctrlKey||event.metaKey||!panel.hidden)return;
   var target=event.target;
   if(target&&target.closest&&target.closest("input,textarea,select,button,a,summary,[contenteditable]"))return;
   if(event.key==="ArrowRight"||event.key==="PageDown"){event.preventDefault();show(current+1);}
   else if(event.key==="ArrowLeft"||event.key==="PageUp"){event.preventDefault();show(current-1);}
  });
  var printDetails=[];
  window.addEventListener("beforeprint",function(){printDetails=Array.from(page.querySelectorAll("details")).map(function(el){var record={el:el,open:el.open};el.open=true;return record;});});
  window.addEventListener("afterprint",function(){printDetails.forEach(function(record){record.el.open=record.open;});printDetails=[];});
  root.classList.add("task-reader-ready");
  document.body.classList.add("task-reader-active");
  show(0,{hash:false,focus:false});reveal(location.hash);
  window.EPITaskReader={go:function(index){show(index);},reveal:reveal,current:function(){return current;},count:cards.length};
 } catch(error) {
  // A loading failure restores the original readable page with its original nodes.
  positions.reverse().forEach(function(pos){if(pos.parent)pos.parent.insertBefore(pos.node,pos.next&&pos.next.parentNode===pos.parent?pos.next:null);});
  page.replaceChildren.apply(page,original);
  if(quiz)quiz.hidden=false;
  if(parent){parent.insertBefore(page,root&&root.parentNode?root:next);}
  if(root&&root.parentNode)root.remove();
  document.documentElement.classList.remove("com-casca");
  document.body.classList.remove("task-reader-active");
  window.console&&console.warn("A aula continua disponível na página de leitura.",error);
 }
})();
