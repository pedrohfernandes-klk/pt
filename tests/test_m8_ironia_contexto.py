from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(p):return json.JSONDecoder().raw_decode((ROOT/p).read_text('utf-8').split('CARTOES=',1)[1])[0]
class IroniaContexto(unittest.TestCase):
 def test_teaching_before_application(self):
  c=bank('m8/licao-m8-f05/index.html');self.assertEqual(len(c),24);s=c[6]['html'];self.assertIn('não são versos do poema',s);self.assertIn('nove e cinquenta',s);self.assertIn('chega às onze',s);self.assertIn('nem todo',s);self.assertNotIn('dizer uma coisa para dar a entender outra',s)
 def test_application_uses_context(self):
  c=bank('m8/licao-m8-f05/index.html');self.assertEqual(c[15]['lacunas'][0]['o'][c[15]['lacunas'][0]['c']],'ironia');self.assertIn('hora de chegada',c[18]['o'][c[18]['c']]);self.assertIn('oralmente ou no caderno',c[23]['html'])
 def test_panel_and_challenge(self):
  c=bank('m8/licao-m8-f05/index.html')
  for x in bank('m8/painel-m8-f05/index.html'):self.assertEqual(x['p'],c[x['k']].get('p',''))
  s=(ROOT/'m8/index.html').read_text('utf-8');units=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for u in units:
   for x in u.get('pool',[]):
    if x.get('_l')=='m8-f05':self.assertNotIn('dizer uma coisa para dar a entender outra',x.get('f',''))
if __name__=='__main__':unittest.main()
