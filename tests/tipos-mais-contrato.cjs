'use strict';
// 02/11/2026: compatibilidade do contrato comum com o motor e isolamento do banco.
const assert = require('node:assert/strict'), fs = require('node:fs'), vm = require('node:vm'), path = require('node:path');
const root = path.resolve(__dirname, '..');
const motor = fs.readFileSync(path.join(root, 'assets/pt-lessons/jogo.js'), 'utf8');
const norm = motor.match(/^function norm\(.*$/m)[0], pista = motor.match(/^function pistaPara\(.*$/m)[0];
const referencia = new Function(norm + '\n' + pista + '\nreturn pistaPara;')();
const sandbox = {window: {}, location: {search: ''}, document: {documentElement: {classList: {contains: () => false}}}};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(root, 'assets/pt-lessons/tipos-mais.js'), 'utf8'), sandbox);
const T = sandbox.window.EPITiposMais;
const pistas = ['Relê o nome da personagem.', 'A oposição distingue as duas leituras.', 'Conta os versos e as sílabas.', 'A oposição repete uma palavra.'];
for (const x of [{p:'Que oposição distingue as leituras?'}, {p:'Conta as sílabas',frase:'A personagem repete o nome'}, {p:'OPOSIÇÃO; oposição!'}, {p:'a'}, {}, {p:'uma palavra palavra'}]) {
  assert.equal(T.pistaPara(x, pistas), referencia(x, pistas));
}
assert.equal(T.pistaPara({}, []), referencia({}, []));
let ctx, seen;
T.registar('teste', {rot:'Teste',como:'teste',criar(x,api,c){
  ctx=c;
  return {html:()=>'',ligar(){},confirmar:()=>({ok:false,certas:0,total:1,erros:['Confundes o tema. Relê o indício.'],falhas:[2]}),revelar:()=>({ok:true,certas:1,total:1,erros:[],falhas:[]})};
}});
assert.throws(()=>T.registar('teste',{rot:'Outro',como:'outro',criar(){}}));
const x={t:'teste',id:'n106-ensaio-1',p:'Indício',f:'Explicação.',fe:['Original.'],texto:'A palavra, outra.'};
const before=JSON.stringify(x), api={estado:{},cfg:{chave:'K',itens:[x],aula:true},el:{querySelectorAll:()=>[],querySelector:()=>null},fecha(){seen=[x.f,x.fe];throw Error('sentinela')}};
const P=sandbox.window.EPITipos.teste;
P.html(x,api);
assert.equal(ctx.repeticao,false);
assert.equal(JSON.stringify(ctx.partes()),JSON.stringify(['A','palavra,','outra.']));
const indices=[0,1,2,3,4,5], order=ctx.ordem(indices);
assert.equal(JSON.stringify(order),JSON.stringify(ctx.ordem(indices)));
assert.deepEqual(indices,[0,1,2,3,4,5]);
assert.deepEqual(Array.from(order).sort(),indices);
assert.throws(()=>P.acoes(x,api).at(-1).onclick(),/sentinela/);
assert.deepEqual(seen,['Acertaste 0 de 1. Explicação.','Confundes o tema. Relê o indício.']);
assert.equal(JSON.stringify(x),before);
const clone=JSON.parse(JSON.stringify(x));
P.html(clone,{...api,estado:{}});
assert.equal(ctx.repeticao,true);
assert.equal(JSON.stringify(ctx.falhas),'[2]');
ctx.falhas.push(9);
P.html(clone,{...api,estado:{}});
assert.equal(JSON.stringify(ctx.falhas),'[2]');
console.log('PASS contrato v1: pista do motor, sessão/variante, ordem estável, banco reposto mesmo com erro e memória isolada');
