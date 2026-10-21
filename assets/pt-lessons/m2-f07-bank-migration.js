/* F07 now includes the three middle scenes before the grammar exercises.
   Old exercise indices >=3 move by three places; scores and completion stay intact. */
(function(){'use strict';
 var key='licao-m2-f07',version='m2-f07-20261021';
 try{
  var state=JSON.parse(localStorage.getItem(key)||'null')||{};
  if(typeof state!=='object'||Array.isArray(state)||state.banco===version)return;
  function move(k){return Number(k)>=3?Number(k)+3:Number(k);}
  if(state.exposicoes&&typeof state.exposicoes==='object'){
   var mapped=Object.create(null);
   Object.keys(state.exposicoes).forEach(function(k){if(/^\d+$/.test(k))mapped[move(k)]=state.exposicoes[k];});
   state.exposicoes=mapped;
  }
  if(typeof state.ult==='string'&&/^\d+(,\d+)*$/.test(state.ult))state.ult=state.ult.split(',').map(move).map(String).sort().join(',');
  state.banco=version;
  localStorage.setItem(key,JSON.stringify(state));
 }catch(error){/* Lessons remain usable when browser storage is unavailable. */}
})();
