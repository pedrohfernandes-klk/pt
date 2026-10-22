"""Core author orientation is distinct from optional contexts and performance."""
from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(path,marker='CARTOES='):
 return json.JSONDecoder().raw_decode((ROOT/path).read_text('utf8').split(marker,1)[1])[0]

class AuthorContext(unittest.TestCase):
 def setUp(self):self.c=bank('m8/licao-m8-f01/index.html');self.u=bank('m8/index.html','var U=')
 def test_timeline_follows_three_central_voices(self):
  timeline=self.c[1]['html']
  self.assertNotIn('Ângelo',timeline);self.assertNotIn('Orpheu',timeline)
  self.assertEqual(re.findall(r'<b>(\d{4}) ·',timeline),['1919','1923','1948','1956','1959','2019'])
  for name in ['Jorge de Sena','Eugénio de Andrade','Ana Luísa Amaral']:
   self.assertRegex(timeline,r'<b>[^<]*'+name+r'</b>')
  for name in ['Jorge de Sena','Eugénio de Andrade','Ana Luísa Amaral']:self.assertIn(name,timeline)
  self.assertIn('As Mãos e os Frutos',timeline);self.assertIn('Ágora',timeline)
 def test_optional_author_is_preserved_without_ghost_exercise(self):
  for i in [0,1,2,23]:self.assertNotIn('Ângelo',self.c[i]['html'])
  context=self.c[5]['html']
  self.assertIn('Outra geração · Ângelo de Lima',context)
  self.assertIn('../../atlas/#figura-angelo-de-lima',context)
  self.assertIn('Não integra as três vozes centrais',context)
  self.assertNotIn('O exercício «Estes versos antigos»',context)
  for c in self.c:
   if c['t']!='ler':self.assertNotIn('Ângelo',json.dumps(c,ensure_ascii=False))
  for x in self.u[0]['pool']:
   if x.get('_l')=='m8-f01':self.assertNotIn('Ângelo',json.dumps(x,ensure_ascii=False))
 def test_authorship_and_performance_are_explicit(self):
  opening=self.c[0]['html']
  self.assertIn('Poema de Adília Lopes · leitura de Fernando Alvim',opening)
  self.assertIn('poeta portuguesa',opening);self.assertIn('Mário Cesariny</b> foi poeta e pintor',opening)
  self.assertIn('Goya é o pintor',opening)
  self.assertIn('Emily Dickinson foi uma poeta norte-americana',self.c[3]['html'])
 def test_context_leads_to_observation_and_proof(self):
  for name in ['Jorge de Sena','Eugénio de Andrade','Ana Luísa Amaral']:self.assertIn(name,self.c[5]['html'])
  self.assertEqual(self.c[5]['html'].count('<b>Experimenta:</b>'),3)
  words=self.c[8]['frase'].split()
  self.assertEqual([words[i] for i in self.c[8]['certas']],['carta','aos','filhos.'])
  self.assertIn('confirma-a.',self.c[22]['palavras'])
  self.assertNotIn('depois da guerra',json.dumps(self.c,ensure_ascii=False))
 def test_counts_keys_and_panel_remain_coherent(self):
  self.assertEqual(len(self.c),24);self.assertEqual(len(self.u[0]['pool']),94)
  self.assertEqual(self.c[11]['lacunas'][0]['c'],1)
  self.assertEqual(self.c[11]['lacunas'][0]['o'][1],'José Fontinhas')
  panel=bank('m8/painel-m8-f01/index.html')
  self.assertEqual(panel,[{'k':i,'t':x['t'],'p':x.get('p',x.get('frase',''))} for i,x in enumerate(self.c) if x['t']!='ler'])

if __name__=='__main__':unittest.main()
