"""Contracts for the three M4 closing lessons; shared feedback is exercised in Node."""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['m4-u1', 'm4-u2', 'm4-u3-discurso']


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids, self.questions = [], [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if 'data-task-question' in attrs:
            self.questions.append({'id': attrs['data-task-question'], 'options': []})
        if tag == 'button' and 'data-response' in attrs:
            self.questions[-1]['options'].append(attrs)


class M4UnitTasks(unittest.TestCase):
    def setUp(self):
        self.pages = [(ROOT / f'tarefas/{name}/index.html') for name in PAGES]

    def test_complete_closing_lesson_and_existing_rubrics(self):
        guide = (ROOT / 'm4/guia-da-tarefa-m4/index.html').read_text('utf-8-sig')
        plain_guide = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', guide)))
        for path in self.pages:
            source = path.read_text('utf-8')
            with self.subTest(path=path):
                self.assertIn('AULA DE TAREFA', source)
                self.assertIn('aula de encerramento da unidade', source)
                self.assertIn('durante toda a tarefa', source)
                clock = re.search(r'<ol class="task-clock".*?</ol>', source, re.S)[0]
                self.assertEqual(re.findall(r'<b>(\d+) min</b>', clock), ['10', '10', '60', '10'])
                self.assertEqual(sum(map(int, re.findall(r'data-production-minutes="(\d+)"', source))), 60)
                rubric = re.search(r'<div class="task-criteria"><ol>(.*?)</ol>', source, re.S)[1]
                criteria = re.findall(r'<li>(.*?)</li>', rubric, re.S)
                self.assertEqual(len(criteria), 3)
                for criterion in criteria:
                    self.assertIn(unescape(criterion), plain_guide)
                self.assertIn('Origem:', source)
                self.assertIn('folha própria', source)
                self.assertIn('duas linhas', source)
                self.assertIn('fotografias legíveis', source)
                self.assertIn('Teams no início desta aula', source)
                self.assertNotIn('Tarefa Final', source)
                self.assertNotIn('<textarea', source)

    def test_links_anchors_and_shared_assets(self):
        for path in self.pages:
            source = path.read_text('utf-8')
            parsed = Page(source)
            with self.subTest(path=path):
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                for href in parsed.links:
                    url = urlsplit(href)
                    if href.startswith('#'):
                        self.assertIn(href[1:], parsed.ids)
                    elif not url.scheme:
                        target = (path.parent / unquote(url.path)).resolve()
                        if target.is_dir():
                            target /= 'index.html'
                        self.assertTrue(target.is_file(), href)
                        if url.fragment:
                            self.assertIn(f'id="{url.fragment}"', target.read_text('utf-8-sig'), href)
                for asset in ['task-90.css', 'task-90.js', 'appearance.css', 'appearance.js']:
                    self.assertIn('../../assets/' + asset, source)
                self.assertIn('class="teacher-access"', source)
                self.assertIn('aria-live="polite"', source)

    def test_product_specific_constraints(self):
        fish, critical, speech = [p.read_text('utf-8') for p in self.pages]
        for text in ['grupo de 2 ou 3', '150 a 200 palavras', 'três a quatro minutos', 'todos falam', 'três imagens', 'objeção']:
            self.assertIn(text, fish)
        for text in ['180 a 240 palavras', 'Raquel Castro', 'LU.CA', 'TPC: Frei Luís de Sousaaa', 'Se não foste ao teatro', 'ato I lida em voz alta', 'cenas idênticas', 'adolescentes']:
            self.assertIn(text, critical)
        for fabricated in ['o ator apontou para a plateia', 'a luz desceu sobre nós', 'o retrato não existia']:
            self.assertNotIn(fabricated, critical)
        for text in ['220 a 280 palavras', 'dois minutos', 'dois argumentos', 'apelo final', 'Apoio comparativo', 'href="../m4-u3/"']:
            self.assertIn(text, speech)
        self.assertNotIn('proposta adicional', speech.lower())
        self.assertNotIn('100 a 140 palavras', speech)

    def test_all_options_drive_the_shared_feedback_script(self):
        script = (ROOT / 'assets/task-90.js').read_text('utf-8')
        for path in self.pages:
            groups = Page(path.read_text('utf-8')).questions
            self.assertEqual(len(groups), 4)
            for group in groups:
                self.assertEqual(sum(o['data-correct'] == 'true' for o in group['options']), 1)
                self.assertEqual(len(group['options']), 3)
                self.assertTrue(all(o['data-response'].strip() for o in group['options']))
            harness = r'''
const assert=require('assert'), vm=require('vm');
const input=JSON.parse(require('fs').readFileSync(0,'utf8'));
const status={textContent:''};
const groups=input.groups.map(g=>{
  const feedback={dataset:{},hidden:true};
  const buttons=g.options.map(a=>({a:{...a},handlers:{},getAttribute(k){return this.a[k]},setAttribute(k,v){this.a[k]=v},addEventListener(k,cb){this.handlers[k]=cb}}));
  return {feedback,buttons,getAttribute(){return g.id},querySelector(){return feedback},querySelectorAll(){return buttons}};
});
vm.runInNewContext(input.script,{Set,document:{querySelector(){return status},querySelectorAll(){return groups}}});
groups.forEach(g=>g.buttons.forEach(b=>{
 b.handlers.click();
 assert.equal(g.feedback.hidden,false);
 assert.equal(g.feedback.textContent,b.a['data-response']);
 assert.equal(g.feedback.dataset.answer,b.a['data-correct']==='true'?'supported':'retry');
 g.buttons.forEach(other=>assert.equal(other.a['aria-pressed'],String(other===b)));
}));
assert.equal(status.textContent,'Respostas exploradas: 4 de 4. Podes rever qualquer escolha.');
'''
            result = subprocess.run(['node', '-e', harness], input=json.dumps({'script': script, 'groups': groups}), text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
