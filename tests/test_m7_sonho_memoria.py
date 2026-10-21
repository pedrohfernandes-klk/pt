from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(n):return json.JSONDecoder().raw_decode((ROOT/f'm7/licao-m7-f{n}/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class SonhoMemoria(unittest.TestCase):
 def test_banks_and_evidence_limited_perception(self):
  a,b=bank('14'),bank('15');self.assertEqual([len(a),len(b)],[23,21]);self.assertIn('não prova',b[4]['f']);self.assertFalse('Tu não as vês' in b[0]['html'],'opening must not infer that the subject cannot see');self.assertIn('audic',b[4]['f'].replace('ç','c').replace('ã','a'))
 def test_biography_is_not_automatically_inferred(self):
  a=bank('15');self.assertEqual('rever',a[12]['t']);self.assertIn('voz do poema',a[12]['o'][0]);self.assertIn('memória e imaginação',a[12]['f']);self.assertIn('não comprova',a[10]['f'])
 def test_grammar_uses_distinct_invented_example(self):
  a=bank('15');self.assertEqual('escolha',a[18]['t']);self.assertIn('inventada',a[18]['p']);self.assertIn('onomatopeia',a[18]['f']);self.assertIn('não retirada do poema',a[18]['f']);self.assertIn('Como se formam palavras novas',a[11]['html'])
 def test_conclusion_can_remain_open_and_context_matters(self):
  a=bank('14');self.assertIn('terceira estrofe',a[17]['pares'][2][1]);self.assertIn('tensão entre ambos',a[22]['html']);self.assertIn('Não é uma reprodução do poema',a[0]['html']);self.assertIn('não exige supor',a[11]['f']);self.assertIn('Oralmente ou no caderno',a[22]['html'])
 def test_teacher_panels_and_challenge_match(self):
  s=(ROOT/'m7/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s[re.search(r'\bU\s*=\s*(\[)',s).start(1):])[0]
  for n in ['14','15']:
   a=bank(n);source=(ROOT/f'm7/painel-m7-f{n}/index.html').read_text('utf-8');rows=json.JSONDecoder().raw_decode(source.split('CARTOES=',1)[1].lstrip())[0]
   for row in rows:self.assertEqual(a[row['k']]['t'],row['t']);self.assertEqual(a[row['k']].get('p',a[row['k']].get('frase','')),row['p'])
   x=next(c for c in a if c['t']=='rever');copy=next(c for unit in u for c in unit['pool'] if c.get('_l')=='m7-f'+n and c['t']=='rever');self.assertEqual(x['frase'],copy['frase']);self.assertEqual(x['o'],copy['o'])
if __name__=='__main__':unittest.main()
