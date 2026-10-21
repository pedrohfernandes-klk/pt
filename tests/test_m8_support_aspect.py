from pathlib import Path
import json, unittest
ROOT=Path(__file__).resolve().parents[1]
class SupportAspect(unittest.TestCase):
 def test_linked_support_does_not_reintroduce_false_rules(self):
  text=(ROOT/'m8/gramatica-aspeto/index.html').read_text('utf-8')
  start=text.index('var E={"pasta"')+6
  data=json.JSONDecoder().raw_decode(text[start:])[0]
  p=data['passos'];self.assertEqual(len(p),6)
  self.assertIn('não diz se parei',p[0]['html']);self.assertIn('sem exigir contagem exata',p[0]['html']);self.assertIn('podem coexistir',p[0]['html'])
  self.assertNotIn('interrompeu',p[3]['opcoes'][2][2]);self.assertIn('Não sabemos se parou',p[3]['opcoes'][2][2])
  self.assertIn('várias vezes',next(o[0] for o in p[4]['opcoes'] if o[1]=='certo'))
  self.assertIn('Não provam, por si sós',next(o[2] for o in p[5]['opcoes'] if o[1]=='certo'))
if __name__=='__main__':unittest.main()
