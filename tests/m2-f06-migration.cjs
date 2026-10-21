const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const code=fs.readFileSync('assets/pt-lessons/m2-f06-bank-migration.js','utf8');
let stored=JSON.stringify({lida:true,melhor:12,totalMelhor:12,tentativas:3,xp:125,t:100,exposicoes:{11:3,15:2,23:1},ult:'11,15,23'});
const context=vm.createContext({localStorage:{getItem:()=>stored,setItem:(k,v)=>{assert.equal(k,'licao-m2-f06');stored=v;}}});
vm.runInContext(code,context);const result=JSON.parse(stored);assert.deepEqual(result.exposicoes,{'17':3,'10':2,'23':1});assert.equal(result.ult,'10,17,23');
for(const [key,value] of Object.entries({lida:true,melhor:12,totalMelhor:12,tentativas:3,xp:125,t:100}))assert.equal(result[key],value);
const once=stored;vm.runInContext(code,context);assert.equal(stored,once);stored=null;vm.runInContext(code,context);assert.equal(JSON.parse(stored).banco,'m2-f06-20261021');
console.log('PASS F06 chronology migration, exposure mapping, scores and idempotence');
