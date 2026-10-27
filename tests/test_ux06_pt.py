from pathlib import Path
from html.parser import HTMLParser
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
PLANS=json.loads((ROOT/'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))
class Tags(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
class UX06(unittest.TestCase):
 def test_module_entry_and_checkpoint_anchors(self):
  for plan in PLANS:
   m=plan['module'];s=(ROOT/f'm{m}/index.html').read_text('utf-8');tags=Tags(s)
   self.assertEqual(sum('data-module-next' in a for _,a in tags.nodes),1)
   self.assertIn('pt-module',next(a for t,a in tags.nodes if t=='body').get('class',''))
   ids={a['id'] for _,a in tags.nodes if 'id' in a}
   for u in plan['units']:
    self.assertIn('desafio-unidade-'+str(u['number']),ids)
    # 26/10: M1/M4/M7 use a task lesson instead of a separate synthesis checkpoint.
    if m in (1,4,7):
     self.assertIn('tarefa-unidade-'+str(u['number']),ids)
     self.assertNotIn('sintese-unidade-'+str(u['number']),ids)
    else:self.assertIn('sintese-unidade-'+str(u['number']),ids)
 def test_map_counts_match_the_route(self):
  for plan in PLANS:
   m=plan['module'];s=(ROOT/f'm{m}/mapa-do-modulo-m{m}/index.html').read_text('utf-8');start=s.index('<div class="numeros">');end=s.index('</header>',start)
   nums=list(map(int,re.findall(r'<b>(\d+)</b>',s[start:end])))
   self.assertEqual(nums[:3],[len(plan['units']),sum(len(u['lessons']) for u in plan['units']),len(plan['units'])])
   if m==2:self.assertEqual(nums[3],2)
 def test_lesson_return_matches_its_curricular_unit(self):
  mapping={lesson:(p['module'],u['number']) for p in PLANS for u in p['units'] for lesson in u['lessons']};mapping.update({'m2-f12':(2,2),'m2-f13':(2,2)})
  for p in ROOT.glob('m[1-9]/licao-*/index.html'):
   module,unit=mapping[p.parent.name.removeprefix('licao-')];tags=Tags(p.read_text('utf-8'));target='../#unidade-pedagogica-'+str(unit)
   body=next(a for t,a in tags.nodes if t=='body');brand=next(a for t,a in tags.nodes if t=='a' and 'c-marca' in a.get('class','').split())
   self.assertEqual(body['data-unit-return'],target);self.assertEqual(brand['href'],target)
   self.assertEqual(brand['aria-label'],f'Voltar à unidade {unit} do módulo {module}')
if __name__=='__main__':unittest.main()
