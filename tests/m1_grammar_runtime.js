/* No browser: parse every edited inline script and exercise real task-90 callbacks. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const files = ['m1/licao-m1-f05/index.html', 'm1/gram-fonologia/index.html',
  'tarefas/m1-u1/index.html', 'tarefas/m1-u2/index.html'];
const decode = text => text.replace(/&#x([\da-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
  .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
  .replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const attrs = text => Object.fromEntries([...text.matchAll(/([\w-]+)="([^"]*)"/g)].map(m => [m[1], decode(m[2])]));
let compiled = 0;
for (const file of files) {
  const source = fs.readFileSync(path.join(root, file), 'utf8');
  for (const script of source.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (/\bsrc=/.test(script[1])) continue;
    if (/application\/json/.test(script[1])) JSON.parse(script[2]);
    else new vm.Script(script[2], {filename: file});
    compiled++;
  }
  if (!file.startsWith('tarefas/')) continue;
  const status = {textContent: ''};
  // 28/10/2026 (PR #122): no formato com escolha, a pergunta do aquecimento é um <div class="task-question">
  // dentro da máquina 02 e a opcional continua num <article>; cada grupo vai até ao seu parágrafo de feedback.
  const groups = [...source.matchAll(/<(?:article|div) class="task-question"([^>]*)>([\s\S]*?data-task-feedback[^>]*>)/g)].map(match => {
    const attributes = attrs(match[1]);
    const feedback = {textContent: '', dataset: {}, hidden: true};
    const buttons = [...match[2].matchAll(/<button\b([^>]*)>/g)].map(button => {
      const a = attrs(button[1]), listeners = {};
      return {getAttribute: k => a[k], setAttribute: (k, v) => { a[k] = v; },
        addEventListener: (type, callback) => { listeners[type] = callback; },
        click: () => listeners.click(), attributes: a};
    });
    return {getAttribute: k => attributes[k], querySelector: () => feedback,
      querySelectorAll: () => buttons, buttons, feedback};
  });
  assert.equal(groups.length, 2);
  const document = {querySelector: () => status, querySelectorAll: () => groups};
  // No storage or network globals: any unexpected access fails this context.
  vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/task-90.js'), 'utf8'), {document});
  groups.forEach((group, index) => {
    const correct = group.buttons.find(b => b.getAttribute('data-correct') === 'true');
    const wrong = group.buttons.find(b => b.getAttribute('data-correct') === 'false');
    wrong.click();
    assert.equal(group.feedback.dataset.answer, 'retry');
    assert.equal(group.feedback.textContent, wrong.getAttribute('data-response'));
    assert.equal(group.feedback.hidden, false);
    assert.match(status.textContent, new RegExp(`: ${index + 1} de ${groups.length}`));
    correct.click();
    assert.equal(group.feedback.dataset.answer, 'supported');
    assert.equal(group.feedback.textContent, correct.getAttribute('data-response'));
    assert.equal(correct.getAttribute('aria-pressed'), 'true');
    assert.equal(wrong.getAttribute('aria-pressed'), 'false');
    assert.match(status.textContent, new RegExp(`: ${index + 1} de ${groups.length}`));
  });
  groups[0].buttons[0].click();
  assert.match(status.textContent, /: 2 de 2/);
}
console.log(`M1 grammar: ${compiled} inline scripts parsed; 4 MC support/retry/revisit flows passed.`);
