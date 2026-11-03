/* 03/11/2026: recolhe os acessos existentes sem alterar destinos, motores ou progresso. */
(function () {
  'use strict';
  const script=document.currentScript;
  if(!script || document.querySelector('[data-apoios-paginas]'))return;
  const root=new URL('../',script.src);
  function candidates(){return [...document.querySelectorAll('a[href]')].filter(a=>!a.closest('.cz-dock,[data-apoios-paginas]')&&(a.closest('details')?.querySelector(':scope>summary.teacher-access')||a.classList.contains('teacher-access')||a.getAttribute('href').includes('/docente/')||/^Para o docente(?:\s|:|$)/i.test(a.textContent.trim())));}
  function mount(){
    const links=candidates();if(!links.length)return;
    const dock=document.createElement('details');dock.className='pt-apoios';dock.setAttribute('data-apoios-paginas','');
    dock.innerHTML='<summary aria-label="Abrir apoios"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m5.6 5.6 3.6 3.6m5.6 5.6 3.6 3.6m0-12.8-3.6 3.6m-5.6 5.6-3.6 3.6"/></svg></summary><nav aria-label="Apoios"></nav>';
    const nav=dock.querySelector('nav');
    const oldMenus=[...document.querySelectorAll('details')].filter(e=>e.querySelector(':scope>summary.teacher-access'));
    links.forEach(a=>{a.classList.remove('teacher-access');if(!a.textContent.trim())a.appendChild(document.createTextNode(a.getAttribute('aria-label')||'Materiais do docente'));nav.appendChild(a);});
    oldMenus.forEach(e=>{e.hidden=true;e.open=false;});
    const print=document.createElement('button');print.type='button';print.textContent='Imprimir';print.addEventListener('click',()=>window.print());nav.appendChild(print);
    const help=document.createElement('a');help.href=new URL('como/',root).href;help.textContent='Como usar o sítio';nav.appendChild(help);
    const area=document.createElement('div');area.className='pt-apoios-area';
    [...document.body.children].filter(e=>!['SCRIPT','STYLE','LINK'].includes(e.tagName)).forEach(e=>area.appendChild(e));
    document.body.classList.add('pt-com-apoios');document.body.append(area,dock);
    dock.addEventListener('keydown',e=>{if(e.key==='Escape'){dock.open=false;dock.querySelector('summary').focus();e.preventDefault();e.stopPropagation();}});
  }
  const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('assets/apoios-paginas.css?v=20261103-1',root).href;
  css.addEventListener('load',mount,{once:true});document.head.appendChild(css);
}());
