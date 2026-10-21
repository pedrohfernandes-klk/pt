from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank():return json.JSONDecoder().raw_decode((ROOT/'m5/licao-m5-f14/index.html').read_text('utf-8').split('CARTOES=',1)[1])[0]
class AdaptacaoComProva(unittest.TestCase):
 def test_example_is_explicitly_invented(self):
  c=bank();self.assertEqual(len(c),21);self.assertIn('não descrevem planos do filme',c[2]['html']);self.assertIn('licao-m5-f10',c[2]['html']);self.assertIn('marca temporal',c[20]['html'])
 def test_voice_is_not_automatic_effect(self):
  c=bank();self.assertIn('analisados no excerto',c[1]['html']);self.assertIn('versão alargada',c[5]['f']);self.assertIn('Não tens de inventar uma perda',c[7]['f']);self.assertIn('ainda é preciso',c[16]['f']);self.assertEqual(len(c[6]['fe']),4);self.assertEqual(len(c[16]['fe']),4)
 def test_alternative_prompts_follow_revision(self):
  c=bank();self.assertIn('observação',c[6]['p2']);self.assertIn('observação',c[14]['p2']);self.assertIn('exemplo inventado',c[16]['p2'])
 def test_challenge_does_not_restore_generalization(self):
  s=(ROOT/'m5/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for unit in u:
   for x in unit.get('pool',[]):
    if x.get('_l')=='m5-f14':
     t=json.dumps(x,ensure_ascii=False);self.assertNotIn('a voz acrescenta a ironia',t);self.assertNotIn('e a sua ironia',t);self.assertNotIn('O que ganha, o que perde, o que decide',t)
 def test_teacher_and_revised_challenge_agree(self):
  c=bank();s=(ROOT/'m5/painel-m5-f14/index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
  for item in panel:self.assertEqual(item['p'],c[item['k']].get('p',c[item['k']].get('frase','')))
  s=(ROOT/'m5/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  copies=[x for unit in u for x in unit.get('pool',[]) if x.get('_l')=='m5-f14' and x.get('p')==c[16]['p']]
  self.assertEqual(len(copies),1);self.assertEqual(copies[0]['fe'],c[16]['fe']);self.assertIn('inventado',copies[0]['p2'])
if __name__=='__main__':unittest.main()
