const assert=require('node:assert/strict'),fs=require('node:fs');
const src=fs.readFileSync('assets/pt-lessons/jogo.js','utf8');
const a=src.indexOf(' function deckDe()'),b=src.indexOf(' function novoBaralho()',a);
const deck=new Function('TODOS','cfg','st','baralhar','Math',src.slice(a,b)+';return deckDe();');
const items=[{t:'ler',html:'Texto A'},{t:'escolha',g:'unico',id:0},...Array.from({length:12},(_,i)=>({t:'escolha',g:'outros',id:i+1}))];
const state={},math=Object.create(Math);math.random=()=>0;
const run=()=>deck(items,{},state,a=>a.slice(),math);
const first=run(),second=run();
assert(second.some(x=>x.g==='unico'),'A segunda tentativa perdeu o único exercício de um bloco de leitura');
assert.notDeepEqual(first.filter(x=>x.t!=='ler').map(x=>x.id).sort(),second.filter(x=>x.t!=='ler').map(x=>x.id).sort());
console.log('PASS coverage and different repeat deck');
// Prioritise previously unseen items while keeping every pedagogical group.
const counts={},seen=new Set();state.exposicoes=counts;delete state.ult;
for(let attempt=0;attempt<4;attempt++){
 const selected=run();
 assert(selected.some(x=>x.g==='unico'));
 for(const x of selected.filter(x=>x.t!=='ler')){const k=items.indexOf(x);counts[k]=(counts[k]||0)+1;seen.add(x.id);}
 if(attempt===1)assert.equal(seen.size,13,'All 13 items should have appeared after two completed attempts');
}
assert.equal(run().filter(x=>x.t==='ler').length,1);
const fixed=deck(items,{variar:false},{},a=>a.slice(),math);
assert.equal(fixed.length,items.length,'Explicitly fixed banks stay complete');
console.log('PASS unseen-item priority, reading preservation and fixed banks');
