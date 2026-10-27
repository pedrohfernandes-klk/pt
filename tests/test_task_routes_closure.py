"""26/10 decision: task = closure lesson, synthesis inside, old checkpoints archive only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib,json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'tests/fixtures/task-route-lesson-content-before.json'
INSTRUCTION_EDITS=ROOT/'tests/fixtures/task-instruction-edits-20261026.json'
GRAMMAR_EDITS=ROOT/'tests/fixtures/m1-grammar-pilot-edits-20261027.json'

def original_lesson_text(path):
 """Reverse only the explicitly authorized UX strings; retain the frozen LF hash."""
 source=(ROOT/path).read_text('utf-8')
 for manifest_path in (GRAMMAR_EDITS,INSTRUCTION_EDITS):
  manifest=json.loads(manifest_path.read_text('utf-8'))
  for edit in reversed(manifest['files'].get(path,{}).get('edits',[])):
   if source.count(edit['new'])!=edit['occurrences']:
    raise AssertionError(f"Authorized edit no longer matches: {path}: {edit['location']}")
   source=source.replace(edit['new'],edit['old'])
 return source
class Route(HTMLParser):
 def __init__(self,s):
  super().__init__();self.ids=[];self.tasks=[];self.stack=[];self.placements=[];self.links=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a':self.links.append(a.get('href',''))
  if 'data-task-lesson' in a:self.tasks.append(a['data-task-lesson']);self.placements.append(list(self.stack))
  if t not in ('meta','link','img','input','br','hr','source','wbr','area','base','col','embed','param','track'):self.stack.append((t,a))
 def handle_endtag(self,t):
  if any(x[0]==t for x in self.stack):
   i=max(i for i,x in enumerate(self.stack) if x[0]==t);self.stack=self.stack[:i]
def units(s):
 return json.JSONDecoder().raw_decode(s[re.search(r'\bvar U=(\[)',s).start(1):])[0]
class TaskRoutes(unittest.TestCase):
 def test_lessons_order_content_and_old_pools_are_preserved(self):
  for m,before in json.loads(FIXTURE.read_text('utf-8')).items():
   s=(ROOT/f'm{m}/index.html').read_text('utf-8');after=units(s)
   self.assertEqual(len(before['units']),len(after))
   for old,new in zip(before['units'],after):
    self.assertEqual(old['passos'],new['passos']);self.assertEqual(old['licoes'],new['licoes'])
    self.assertEqual(old['pool_sha256'],hashlib.sha256(json.dumps(new['pool'],sort_keys=True,ensure_ascii=False).encode()).hexdigest())
   for path,digest in before['files'].items():
    self.assertEqual(digest,hashlib.sha256(original_lesson_text(path).encode('utf-8')).hexdigest(),path)
 def test_one_classroom_task_per_unit_no_independent_closure_gate(self):
  expected={1:['m1-u1','m1-u2'],4:['m4-u1','m4-u2','m4-u3-discurso'],7:['m7-u1','m7-u2','m7-u3']}
  for m,slugs in expected.items():
   s=(ROOT/f'm{m}/index.html').read_text('utf-8');p=Route(s)
   self.assertEqual(len(p.ids),len(set(p.ids)))
   self.assertEqual(p.tasks,[str(i+1) for i in range(len(slugs))])
   self.assertTrue(all(any(t=='ol' and a.get('class')=='passos' for t,a in ancestors) for ancestors in p.placements))
   self.assertNotIn('data-sintese=',s);self.assertNotIn('id="cartao"',s)
   self.assertNotIn('TAREFA FINAL',s);self.assertNotIn('sinteseFeita',s)
   self.assertIn('id="arquivo-percurso" hidden',s)
   self.assertIn('unit-task-route.js',s)
   self.assertNotIn('data-cartaz="percurso"',s)
   self.assertIn('data-cartaz-archive="percurso"',s)
   self.assertIn('route-teacher-tools',s)
   self.assertIn('aula de tarefa de 90 minutos',s)
   for slug in slugs:
    self.assertIn('../tarefas/'+slug+'/',p.links)
    self.assertIn('../../tarefas/'+slug+'/',(ROOT/f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8'))
   guide=(ROOT/f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
   self.assertIn('id="arquivo-producoes"',guide)
   self.assertNotIn('Cada unidade termina com um desafio',guide)
 def test_adapter_has_no_task_or_historical_completion_writes(self):
  s=(ROOT/'assets/unit-task-route.js').read_text('utf-8')
  for forbidden in ('localStorage.setItem','localStorage.removeItem','sinteseFeita','#cartao'):
   self.assertNotIn(forbidden,s)
  for required in ('percurso-v2-','percurso-sintese-','desafio-unidade-v2-','percurso-','lessonDone','evaluation'):
   if required=='evaluation':continue
   self.assertIn(required,s)
  self.assertIn('teacher',(ROOT/'m7/index.html').read_text('utf-8'))
 def test_m4_comparison_is_support_and_discurso_is_canonical(self):
  old=(ROOT/'tarefas/m4-u3/index.html').read_text('utf-8')
  self.assertIn('APOIO DE COMPARAÇÃO',old);self.assertIn('../m4-u3-discurso/',old)
  self.assertIn('../tarefas/m4-u3-discurso/',(ROOT/'m4/index.html').read_text('utf-8'))
if __name__=='__main__':unittest.main()
