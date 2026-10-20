from pathlib import Path
import json,sys,unittest,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
class Synthesis(unittest.TestCase):
 def test_optional_notes_and_explicit_completion_all_modules(self):
  for m in range(1,10):
   s=(ROOT/f'm{m}/index.html').read_text('utf-8')
   self.assertIn('&&sinteseFeita(u.n)',s)
   self.assertNotIn('&&palavrasDe(resp(u.n))>=80',s)
   self.assertEqual(s.count('data-sintese-registar'),s.count('data-resp="'))
   self.assertIn('Notas no ecrã (opcional)',s)
 def test_interpretations_are_open_and_not_in_challenge_pool(self):
  plan=json.loads((ROOT/'docs/pedagogia/interpretacoes-abertas-20261020.json').read_text('utf-8'))
  for x in plan['unscored_cards']:
   m=x['module']; lesson=x['lesson']; card=lesson_cards(ROOT/f'{m}/licao-{m}-f{lesson}/index.html')[x['index']]
   src=(ROOT/f'{m}/index.html').read_text('utf-8')
   start=re.search(r'\bU\s*=\s*(\[)',src).start(1)
   units=json.JSONDecoder().raw_decode(src[start:])[0]
   self.assertFalse(any((c.get('p') or c.get('frase'))==x['former_prompt'] for u in units for c in u['pool']))
   self.assertEqual(card['t'],'ler');self.assertIn('<details>',card['html'])
   self.assertFalse(set(card)&{'c','v','pares','lacunas'})
 def test_objective_question_stays_objective(self):
  card=lesson_cards(ROOT/'m7/licao-m7-f14/index.html')[18]
  self.assertEqual(card['t'],'vf');self.assertIs(card['v'],False)
if __name__=='__main__': unittest.main()
