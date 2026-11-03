'use strict';
// 02/11/2026: propriedades da migração, independentes do DOM e do motor.
const assert = require('node:assert/strict');
const A = require('../assets/pt-lessons/acrescentos.js');
for (const novos of [[0], [1], [0, 1], [2, 5], [0, 3, 8, 11], [5, 2]]) {
  const original = {tentativas: 3, versao: 'v', lida: true, melhor: 5, banco: 'antigo', exposicoes: {}, ult: ''};
  for (let i = 0; i < 100; i++) original.exposicoes[i] = i + 1;
  original.ult = Object.keys(original.exposicoes).sort().join(',');
  const before = JSON.stringify(original), after = A.remapear(original, novos);
  const indices = Array.from({length: 100 + novos.length}, (_, i) => i).filter(i => !novos.includes(i));
  assert.deepEqual(after.exposicoes, Object.fromEntries(indices.map((k, i) => [k, i + 1])));
  assert.equal(after.ult, indices.map(String).sort().join(','));
  assert.equal(JSON.stringify(original), before);
  for (const k of ['tentativas', 'versao', 'lida', 'melhor', 'banco']) assert.deepEqual(after[k], original[k]);
}
for (const bad of [[], [-1], [1, 1], [0.5], [Infinity], '', '1,,2', '1,', 'a']) {
  assert.throws(() => A.remapear({exposicoes: {0: 1}}, bad));
}
const imported = {melhor: 5, exposicoes: {2: 8}, ult: '2'}, original = JSON.stringify(imported);
assert.deepEqual(A.protegerImportacao(imported, '["l1","l2"]', '["l1"]'), {melhor: 5});
assert.equal(JSON.stringify(imported), original);
assert.strictEqual(A.protegerImportacao(imported, '["l1"]', '["l1","l2"]'), imported);
console.log('PASS 600 correspondências de índices, campos preservados, entradas inválidas e importação sem mutação');
