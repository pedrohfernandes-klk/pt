from pathlib import Path
import json,sys,unittest,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
class Synthesis(unittest.TestCase):
 def test_oral_or_notebook_synthesis_and_explicit_completion_all_modules(self):
  for m in range(1,10):
   s=(ROOT/f'm{m}/index.html').read_text('utf-8')
   self.assertIn('&&sinteseFeita(u.n)',s)
   self.assertNotIn('&&palavrasDe(resp(u.n))>=80',s)
   # 23/10/2026 (plano de melhoria, fase 0): a síntese faz-se oralmente ou no caderno; saíram a caixa
   # «Notas no ecrã (opcional)» e o botão «Copiar para o Teams». O teste deixa de exigir a caixa de notas
   # e passa a exigir um registo (oral / no caderno) por síntese e nenhum campo de escrita na síntese.
   self.assertEqual(s.count('data-sintese-registar'),s.count('<details class="fim"'))
   self.assertEqual(s.count('data-sintese-registar'),s.count('data-sintese="'))
   self.assertGreater(s.count('data-sintese-registar'),1)
   self.assertNotIn('data-resp="',s)
   self.assertNotIn('Notas no ecrã',s)
   self.assertNotIn('Copiar para o Teams',s)
   self.assertNotIn('data-copiar',s)
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
