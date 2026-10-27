from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,unittest
from task_source_contract import historical_task_source

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.sections=[];self.task_sections=[];self.links=[];self.ids=set();self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='section':self.sections.append(a.get('aria-labelledby',a.get('id')))
  if t=='li' and a.get('id')=='tarefa-unidade-2':self.task_sections.append(list(self.sections))
  if t=='a':self.links.append(a.get('href',''))
  if 'id' in a:self.ids.add(a['id'])
 def handle_endtag(self,t):
  if t=='section':self.sections.pop()

class M7Task(unittest.TestCase):
 def test_existing_assignment_and_full_rubric_are_preserved(self):
  baseline=json.loads((ROOT/'tests/fixtures/m7-u2-task-original.json').read_text('utf-8'))['task']
  guide=(ROOT/'m7/guia-da-tarefa-m7/index.html').read_text('utf-8-sig')
  tasks,_=json.JSONDecoder().raw_decode(guide[guide.index('T=[{')+2:])
  self.assertEqual(tasks[0],baseline)
  page=historical_task_source(ROOT/'tarefas/m7-u2/index.html')
  self.assertIn(baseline['encomenda'],page)
  for criterion in baseline['criterios']:self.assertIn(criterion,page)
  self.assertIn('100 a 150 palavras',page);self.assertIn('dois minutos',page)
  self.assertIn('responde a uma pergunta',page)

 def test_access_is_at_end_of_unit_two_without_changing_steps(self):
  source=(ROOT/'m7/index.html').read_text('utf-8');page=Page(source)
  # 26/10: the task is the last classroom row inside the unit, not an appended aside.
  self.assertEqual(len(page.task_sections),1)
  self.assertEqual(page.task_sections[0][0],'unidade-pedagogica-2')
  self.assertGreater(source.index('id="tarefa-unidade-2"'),source.index('id="m7-quatro-vozes-um-problema"'))
  self.assertNotIn('id="sintese-unidade-2"',source)
  self.assertIn('duas linhas de síntese',historical_task_source(ROOT/'tarefas/m7-u2/index.html'))
  self.assertIn('../tarefas/m7-u2/',page.links)
  self.assertIn('../../tarefas/m7-u2/',(ROOT/'m7/guia-da-tarefa-m7/index.html').read_text('utf-8'))

 def test_consultation_recovery_transfer_and_submission(self):
  path=ROOT/'tarefas/m7-u2/index.html';source=historical_task_source(path);page=Page(source)
  self.assertIn('durante toda a tarefa',source)
  times=list(map(int,re.findall(r'<b>(\d+) min</b>',re.search(r'<ol class="task-clock".*?</ol>',source,re.S)[0])))
  self.assertEqual(times,[10,10,60,10])
  self.assertEqual(source.count('data-task-question='),4)
  self.assertIn('Exemplo inventado para esta tarefa',source)
  for anchor in ['rever-caeiro','rever-reis','rever-campos']:
   self.assertIn(anchor,page.ids);self.assertIn('#'+anchor,page.links)
  for href in page.links:
   if href.startswith('#'):self.assertIn(href[1:],page.ids)
   elif not urlsplit(href).scheme:
    target=(path.parent/unquote(urlsplit(href).path)).resolve()
    self.assertTrue((target/'index.html').exists() if target.is_dir() else target.exists(),href)
  self.assertIn('fotografias legíveis',source);self.assertIn('Teams no início desta aula',source)
  self.assertNotIn('localStorage',source);self.assertNotIn('fetch(',source)

if __name__=='__main__':unittest.main()
