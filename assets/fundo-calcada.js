// 02/11/2026: decisão 125. O fundo «A calçada e o mar» só anda fora da projeção (a projeção abre a página numa moldura)
// e sem movimento reduzido, e pára quando sai do ecrã. Sem este script, o padrão fica parado.
(function(){
 var cab=document.querySelector('.raiz .p-cab');
 if(!cab||!window.matchMedia)return;
 var projetada=/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top;
 if(projetada||!matchMedia('(prefers-reduced-motion: no-preference)').matches)return;
 cab.classList.add('cf-anda');
 if('IntersectionObserver'in window)new IntersectionObserver(function(e){cab.classList.toggle('cf-fora',!e[e.length-1].isIntersecting);}).observe(cab);
})();
