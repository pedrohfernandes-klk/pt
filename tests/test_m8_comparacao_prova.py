from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank():return json.JSONDecoder().raw_decode((ROOT/'m8/licao-m8-f10/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class ComparacaoComProva(unittest.TestCase):
 def test_identifies_both_works_and_limits(self):
  c=bank();self.assertEqual(len(c),22);self.assertIn('Carta a meus filhos',c[2]['html']);self.assertIn('1814',c[2]['html']);self.assertIn('1963',c[2]['html']);self.assertIn('um verso inicial não prova',c[2]['html']);self.assertIn('licao-m8-f03',c[2]['html']);self.assertIn('comparacao-prova',c[2]['html'])
 def test_unidentified_poem_no_longer_graded(self):
  for c in bank():
   if c['t']!='ler':self.assertNotIn('de verão',json.dumps(c,ensure_ascii=False))
  self.assertIn('investigar Hammershøi',bank()[2]['html'])
 def test_vocative_and_feedback(self):
  c=bank();self.assertEqual([c[7]['frase'].split()[i] for i in c[7]['certas']],['meus','filhos,']);self.assertEqual(len(c[18]['fe']),len(c[18]['o']));self.assertIn('hipótese a desenvolver',c[18]['f']);self.assertIn('semelhanças',c[11]['f'])
 def test_teacher_and_challenge_match(self):
  c=bank();s=(ROOT/'m8/painel-m8-f10/index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
  for item in panel:self.assertEqual(item['p'],c[item['k']].get('p',c[item['k']].get('frase','')))
  s=(ROOT/'m8/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for unit in u:
   for item in unit.get('pool',[]):
    if item.get('_l')=='m8-f10':
     self.assertNotIn('de verão',json.dumps(item,ensure_ascii=False))
     if item.get('p') in [c[i].get('p') for i in [8,10,11,12,18]]:self.assertTrue(any(all(v==card.get(k) for k,v in item.items() if not k.startswith('_')) for card in c))
if __name__=='__main__':unittest.main()
