from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank():return json.JSONDecoder().raw_decode((ROOT/'m6/licao-m6-f09/index.html').read_text('utf-8').split('CARTOES=',1)[1])[0]
class RecursosComparados(unittest.TestCase):
 def test_teaches_distinction_before_application(self):
  c=bank();self.assertEqual(len(c),21);self.assertIn('exemplo inventado',c[2]['html']);self.assertIn('domínios sensoriais',c[2]['html']);self.assertIn('não é, só por si',c[2]['html']);self.assertEqual(c[18]['lacunas'][0]['o'][0],'hipálage');self.assertEqual(c[18]['lacunas'][1]['o'][0],'moral')
 def test_avoids_exclusive_author_labels(self):
  c=bank();self.assertIn('não listas',c[1]['html']);self.assertIn('não reserva',c[10]['p']);self.assertIn('indícios',c[3]['f']);self.assertIn('hipótese de comparação',c[20]['html'])
 def test_evidence_choice_has_specific_feedback(self):
  c=bank()[14];self.assertEqual(c['c'],0);self.assertEqual(len(c['fe']),len(c['o']));self.assertTrue(all(c['fe'][i] for i in [1,2,3]));self.assertIn('sem consultar',bank()[20]['html'])
 def test_panel_and_challenge_consistency(self):
  c=bank();s=(ROOT/'m6/painel-m6-f09/index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
  for x in panel:self.assertEqual(x['p'],c[x['k']].get('p',c[x['k']].get('frase','')))
  s=(ROOT/'m6/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0];copies=[x for unit in u for x in unit.get('pool',[]) if x.get('_l')=='m6-f09'];self.assertTrue(any(x.get('p')==c[14]['p'] for x in copies))
  for x in copies:self.assertNotIn('hipálage ou sinestesia',json.dumps(x,ensure_ascii=False))
if __name__=='__main__':unittest.main()
