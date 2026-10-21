import json,re,unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
def cards(n):return json.JSONDecoder().raw_decode((ROOT/f'm2/licao-m2-f{n}/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
def extra(name):
 s=(ROOT/f'm2/{name}/index.html').read_text('utf-8');return json.JSONDecoder().raw_decode(s[re.search(r'var E=(\{"pasta")',s).start(1):])[0]
class M2Balance(unittest.TestCase):
 def test_middle_scenes_precede_grammar_and_desfecho(self):
  a=cards('07');self.assertEqual(28,len(a))
  for pos,name in zip([2,3,4],['pero-visita','escudeiro-fala','janelas-pregadas']):
   self.assertEqual('ler',a[pos]['t']);self.assertIn(extra(name)['passos'][0]['html'],a[pos]['html'])
  self.assertEqual('escolha',a[5]['t']);self.assertIn('Está tu dissimulado',a[5]['f'])
  self.assertIn('Retomar a distinção',a[7]['html']);self.assertIn('Para o desfecho',a[-1]['html'])
 def test_complements_use_their_own_passages(self):
  for name in ['pero-visita','janelas-pregadas']:
   e=extra(name);cases=e['passos'][4]['casos'];self.assertEqual(4,len(cases))
   self.assertEqual({True,False},{c[1] for c in cases});self.assertTrue(all(c[2] for c in cases))
   for stranger in ['Alencar','Cohen','Ega','Carlos']:self.assertNotIn(stranger,json.dumps(cases))
  self.assertIn('não prova',extra('pero-visita')['passos'][4]['casos'][3][2])
 def test_no_external_visit_or_video_needed_for_initial_transfer(self):
  self.assertIn('Sem visita ao teatro',cards('10')[2]['html'])
  self.assertIn('efetivamente ao espetáculo',cards('10')[2]['html'])
  self.assertIn('individualmente',cards('09')[2]['html']);self.assertIn('não precisas de filmar',cards('09')[2]['html'])
  self.assertNotIn('castigo',json.dumps(cards('09'),ensure_ascii=False))
 def test_core_navigation_and_complement_returns(self):
  base='https://pedrohfernandes-klk.github.io/pt/m2/'
  for n,nxt in [('06','11'),('11','10'),('10','08'),('08','09')]:
   s=(ROOT/f'm2/licao-m2-f{n}/index.html').read_text('utf-8');self.assertIn('seguinte:"'+base+'licao-m2-f'+nxt+'/"',s)
  self.assertIn('seguinte:"../#desafio-unidade-2"',(ROOT/'m2/licao-m2-f09/index.html').read_text('utf-8'))
  for n,target in [('12','10'),('13','11')]:
   s=(ROOT/f'm2/licao-m2-f{n}/index.html').read_text('utf-8');self.assertIn('seguinte:"../licao-m2-f'+target+'/"',s)
   self.assertNotIn('Continuar para a lição seguinte',s)
if __name__=='__main__':unittest.main()
