from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, unittest
from task_source_contract import historical_task_source
ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.ids=[];self.links=[];self.questions=[];self.buttons=[];self.text=[];self.feedback=0;self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t in ('a','link','script'):self.links.append(a.get('href',a.get('src','')))
  if 'data-task-question' in a:self.questions.append(a['data-task-question'])
  if t=='button':self.buttons.append(a)
  if 'data-task-feedback' in a:self.feedback+=1
 def handle_data(self,d):self.text.append(d)

class RemainingM7Tasks(unittest.TestCase):
 def page(self,n):
  p=ROOT/f'tarefas/m7-u{n}/index.html';s=historical_task_source(p);return p,s,Page(s)
 def test_links_and_shared_quiz_contract(self):
  for n in (1,3):
   with self.subTest(unit=n):
    p,s,page=self.page(n)
    self.assertEqual(page.questions,['1','2','3','4']);self.assertEqual(page.feedback,4)
    self.assertEqual(len(page.ids),len(set(page.ids)));self.assertEqual(len(page.buttons),12)
    for i in range(4):
     options=page.buttons[3*i:3*i+3]
     self.assertEqual(sum(o.get('data-correct')=='true' for o in options),1)
     self.assertEqual(len({o['data-response'] for o in options}),3)
     for o in options:
      self.assertEqual(o['type'],'button');self.assertEqual(o['aria-pressed'],'false')
      self.assertGreater(len(o['data-response']),50)
    for href in page.links:
     u=urlsplit(href)
     if u.scheme:continue
     if u.path:
      target=(p.parent/unquote(u.path)).resolve()
      if target.is_dir():target=target/'index.html'
      self.assertTrue(target.is_file(),href)
      if u.fragment:self.assertIn(f'id="{u.fragment}"',target.read_text('utf-8-sig'))
     elif u.fragment:self.assertIn(u.fragment,page.ids)
    for asset in ('task-90.js','task-90.css'):
     version='20261027-tarefas-1' if asset.endswith('.css') else '20261026.1'
     self.assertIn('../../assets/'+asset+'?v='+version,page.links)
    self.assertIn('aria-live="polite"',s)
    for forbidden in ('localStorage','fetch(','<textarea','Tarefa Final','href="#sintese'):
     self.assertNotIn(forbidden,s)
 def test_lesson_clock_paper_synthesis_and_delivery(self):
  for n in (1,3):
   with self.subTest(unit=n):
    _,s,p=self.page(n)
    clock=re.search(r'<ol class="task-clock".*?</ol>',s,re.S)[0]
    self.assertEqual(re.findall(r'<b>(\d+) min</b>',clock),['10','10','60','10'])
    production=s.split('id="produzir"')[1].split('id="entregar"')[0]
    self.assertEqual(sum(map(int,re.findall(r'<h3>\d+\. (\d+) min</h3>',production))),60)
    self.assertIn('duas linhas',production)
    for required in ('nas tuas folhas','durante toda a tarefa','fotografias legíveis','Teams no início desta aula',f'Aula de tarefa · Unidade {n} · 90 min'):
     self.assertIn(required,s)
 def test_original_criteria_and_products(self):
  g=(ROOT/'m7/guia-da-tarefa-m7/index.html').read_text('utf-8-sig')
  tasks,_=json.JSONDecoder().raw_decode(g[g.index('T=[{')+2:])
  _,_,p=self.page(1);t=''.join(p.text)
  for level in tasks[0]['rubrica'][4]['niveis']:self.assertIn(level,t)
  for required in ('não são uma nova cotação','80 a 120 palavras','Quem sou ao menos sinta','É em nós que é tudo','não transformes os versos num relato da vida'):
   self.assertIn(required,t)
  _,_,p=self.page(3);t=''.join(p.text)
  for criterion in tasks[1]['criterios']:self.assertIn(criterion,t)
  for rubric in tasks[1]['rubrica']:
   for level in rubric['niveis']:self.assertIn(level,t)
  for required in ('duas aulas','objeto preparado','150 a 200 palavras','três minutos','perguntas','três propostas','três mudanças','intenção, versos de partida, decisões formais, abandonos e o que falta','até quatro projetos','restantes defesas','sem nota','M7_Tarefa2_Objeto','M7_Tarefa2_Memoria'):
   self.assertIn(required,t)

if __name__=='__main__':unittest.main()
