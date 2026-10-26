from pathlib import Path
import json,sys,unittest,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
class ExamAlignment(unittest.TestCase):
 def setUp(self):self.sessions=json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))['sessions']
 def test_recycled_answers_match_current_lessons(self):
  matches=0
  for s in self.sessions:
   # Authored video case studies have their own comprehension tests; they do not
   # recycle answers from a lesson bank. Existing recycled sessions stay checked.
   if s['source'].get('original'):continue
   cards=lesson_cards(ROOT/s['source']['url'].removeprefix('/pt/')/'index.html')
   for q in s['warmup']:
    for c in cards:
     if q['q'] not in [c.get('p'),c.get('p2')]:continue
     if c['t']=='escolha':answer=c['o'][c['c']]
     elif c['t']=='vf':answer='Verdadeiro' if c['v'] else 'Falso'
     else:continue
     self.assertEqual(q['options'][q['answer']],answer,q['id'])
     self.assertEqual(q['feedback'],c['f'].replace('**',''),q['id']);matches+=1
  self.assertGreaterEqual(matches,30)
 def test_support_targets_exist_and_cantigas_supply_mendinho(self):
  for s in self.sessions:
   for ref in [s['source']]+s['resources']:
    self.assertTrue((ROOT/ref['url'].removeprefix('/pt/')/'index.html').is_file(),(s['id'],ref))
  s=self.sessions[0]
  self.assertIn('Nom hei [eu] i barqueiro nem remador',s['source']['excerpt'])
  self.assertIn('morte consumada',s['source']['excerpt'])
  self.assertTrue(any('m1-f02' in r['url'] for r in s['resources']))
 def test_interpretation_limits_and_specific_terms(self):
  by={s['id']:s for s in self.sessions}
  self.assertNotIn('quem partiu descontente',by['s04']['warmup'][1]['q'])
  self.assertIn('não deve ser classificada como sinestesia',by['s11']['warmup'][2]['feedback'])
  self.assertIn('não é, por si só, um recuo',by['s19']['warmup'][1]['feedback'])
  self.assertTrue(all(any('diferente' in st['detail'] for st in s['correction']['steps']) for s in self.sessions))
if __name__=='__main__':unittest.main()
