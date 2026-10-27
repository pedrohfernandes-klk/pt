from pathlib import Path
from html.parser import HTMLParser
import json,re,sys,unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
from test_task_routes_closure import original_lesson_text

class UnitPlacement(HTMLParser):
 def __init__(self,text):super().__init__();self.stack=[];self.tasks=[];self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='section':self.stack.append(a.get('aria-labelledby',a.get('id')))
  if t=='li' and a.get('id')=='tarefa-unidade-3':self.tasks.append(list(self.stack))
 def handle_endtag(self,t):
  if t=='section':self.stack.pop()

class TaskNinety(unittest.TestCase):
 def test_existing_prompt_and_assessment_are_preserved(self):
  # The original support retains its rubric; F11 only changes the surrounding UX.
  source=original_lesson_text('m4/licao-m4-f11/index.html')
  old=json.JSONDecoder().raw_decode(source[source.index('CARTOES=')+len('CARTOES='):])[0][15]['html']
  page=(ROOT/'tarefas/m4-u3/index.html').read_text('utf-8')
  self.assertIn(old.split('<details',1)[0],page)
  criteria=re.search(r'<summary>O que conta</summary><div>(<ol>.*?</ol>)',old,re.S).group(1)
  self.assertIn(criteria,page)
  self.assertIn('../../m4/licao-m4-f11/',page)
  self.assertIn('fotografias legíveis das folhas',page)
  self.assertIn('Teams no início desta aula',page)
  self.assertIn('Tarefa com consulta',page)
  self.assertIn('durante toda a tarefa',page)
  policy=json.loads((ROOT/'docs/pedagogia/tarefas-unidades-20261026.json').read_text('utf-8'))
  self.assertTrue(policy['consultation'].startswith('Always open-resource'))
  self.assertIn('several questions',policy['task_format'])

 def test_task_is_at_unit_three_end_without_changing_digital_steps(self):
  page=(ROOT/'m4/index.html').read_text('utf-8')
  placement=UnitPlacement(page)
  # 26/10: Discurso is the task lesson; comparison remains available only as support.
  self.assertEqual(len(placement.tasks),1)
  self.assertEqual(placement.tasks[0][0],'unidade-pedagogica-3')
  start=page.index('id="tarefa-unidade-3"')
  self.assertGreater(start,page.index('id="m4-f11"'))
  self.assertNotIn('id="sintese-unidade-3"',page)
  self.assertIn('../tarefas/m4-u3-discurso/',page)
  # Snapshot explícito da base; funciona também no checkout reduzido da CI.
  baseline=json.loads((ROOT/'tests/fixtures/task90-m4-units-before.json').read_text('utf-8'))
  def contract(s):
   match=re.search(r'<script[^>]*id="epi-unidades-pedagogicas"[^>]*>(.*?)</script>',s,re.S)
   return json.loads(match[1])
  current=contract(page)
  self.assertTrue(all(u['task']['minutes']==90 and u['task']['evaluation']=='teacher' for u in current))
  self.assertEqual(baseline['units'],[{k:v for k,v in u.items() if k!='task'} for u in current])

 def test_preparation_is_short_and_paper_has_the_majority_of_time(self):
  page=(ROOT/'tarefas/m4-u3/index.html').read_text('utf-8')
  clock=re.search(r'<ol class="task-clock".*?</ol>',page,re.S).group()
  times=list(map(int,re.findall(r'<b>(\d+) min</b>',clock)))
  self.assertEqual(times,[10,10,60,10]);self.assertEqual(sum(times),90)
  questions=re.findall(r'<article class="task-question".*?</article>',page,re.S)
  self.assertEqual(len(questions),4)
  for q in questions:self.assertEqual(q.count('data-correct="true"'),1)
  self.assertIn('href="#produzir"',page)
  script=(ROOT/'assets/task-90.js').read_text('utf-8')
  for identifier in ['localStorage','sessionStorage','fetch(','XMLHttpRequest']:
   self.assertNotIn(identifier,script)

 def test_teacher_guides_move_to_buoy_but_student_resources_remain(self):
  for module in range(1,10):
   source=(ROOT/f'm{module}/index.html').read_text('utf-8')
   self.assertIn('class="teacher-access"',source)
   self.assertIn('lente/docente/#portugues',source)
   self.assertIn(f'guia-da-tarefa-m{module}/',source)
  for module in [1,4]:
   source=(ROOT/f'm{module}/index.html').read_text('utf-8')
   self.assertNotIn('Guiões das aulas (docente)',source)
   self.assertTrue((ROOT/f'm{module}/aulas/index.html').is_file())

if __name__=='__main__':unittest.main()
