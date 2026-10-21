from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(path):return json.JSONDecoder().raw_decode((ROOT/path).read_text('utf-8').split('CARTOES=',1)[1])[0]
class CadernoCampo(unittest.TestCase):
 def test_model_precedes_questions(self):
  c=bank('m8/licao-m8-f11/index.html');self.assertEqual(len(c),20);self.assertIn('A cadeira estava ali para o guarda',c[2]['html']);self.assertIn('cinco minutos',c[2]['html']);self.assertIn('Hipótese',c[2]['html']);self.assertIn('Invenção narrativa',c[2]['html'])
 def test_answers_respect_observation(self):
  c=bank('m8/licao-m8-f11/index.html');self.assertIn('cinco minutos',c[15]['o'][c[15]['c']]);self.assertTrue(c[16]['o'][c[16]['c']].startswith('Talvez'));self.assertIn('não conclusões comprovadas',c[7]['f']);self.assertIn('oração seguinte',c[18]['f'])
 def test_independent_route_and_recovery(self):
  c=bank('m8/licao-m8-f11/index.html');self.assertIn('não disponíveis',c[2]['html']);self.assertIn('oralmente ou no caderno',c[19]['html']);self.assertIn('verso ou passo',c[19]['html'])
 def test_panel_synchronized(self):
  c=bank('m8/licao-m8-f11/index.html')
  for x in bank('m8/painel-m8-f11/index.html'):self.assertEqual(x['p'],c[x['k']].get('p',''))
if __name__=='__main__':unittest.main()
