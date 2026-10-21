/* Preserve F06 history when its reading blocks return to dramatic order. */
(function(){'use strict';
 var key='licao-m2-f06',version='m2-f06-20261021',order=[0,1,2,3,4,5,6,7,8,14,15,16,17,18,19,9,10,11,12,13,20,21,22,23,24,25,26,27,28,29,30,31,32,33];
 try{
  var state=JSON.parse(localStorage.getItem(key)||'null')||{};
  if(typeof state!=='object'||Array.isArray(state)||state.banco===version)return;
  function move(k){return order.indexOf(Number(k));}
  if(state.exposicoes&&typeof state.exposicoes==='object'){
   var mapped=Object.create(null);
   Object.keys(state.exposicoes).forEach(function(k){if(/^\d+$/.test(k)&&move(k)>=0)mapped[move(k)]=state.exposicoes[k];});
   state.exposicoes=mapped;
  }
  if(typeof state.ult==='string'&&/^\d+(,\d+)*$/.test(state.ult))state.ult=state.ult.split(',').map(move).filter(function(k){return k>=0;}).map(String).sort().join(',');
  state.banco=version;localStorage.setItem(key,JSON.stringify(state));
 }catch(error){/* Keep the lesson usable when browser storage is unavailable. */}
})();
