/* Preparação formativa; não escreve progresso, classificação ou dados pessoais. */
(function(){'use strict';
 var explored=new Set(),status=document.querySelector('[data-task-status]'),groups=Array.from(document.querySelectorAll('[data-task-question]'));
 groups.forEach(function(group){
  var feedback=group.querySelector('[data-task-feedback]');
  group.querySelectorAll('button[data-response]').forEach(function(button){
   button.addEventListener('click',function(){
    group.querySelectorAll('button[data-response]').forEach(function(other){other.setAttribute('aria-pressed',String(other===button))});
    feedback.textContent=button.getAttribute('data-response');
    feedback.dataset.answer=button.getAttribute('data-correct')==='true'?'supported':'retry';
    feedback.hidden=false;explored.add(group.getAttribute('data-task-question'));
    if(status)status.textContent='Respostas exploradas: '+explored.size+' de '+groups.length+'. Podes rever qualquer escolha.';
   });
  });
 });
})();
