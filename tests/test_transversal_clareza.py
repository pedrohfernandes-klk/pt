from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(p):return json.JSONDecoder().raw_decode(p.read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class TransversalClareza(unittest.TestCase):
 def test_comparison_layout_has_explicit_two_columns(self):
  for key,k in [('m7-f02',15),('m7-f13',18),('m7-f14',16)]:
   p=ROOT/'m7'/('licao-'+key)/'index.html';c=bank(p);self.assertIn('duas-colunas',c[k]['html']);self.assertIn('comparacoes.css',p.read_text('utf-8'))
 def test_source_matching_challenge_answers_agree(self):
  matched=0
  for m in range(1,10):
   questions={}
   for p in (ROOT/f'm{m}').glob('licao-*/index.html'):
    if 'CARTOES=' not in p.read_text('utf-8'):continue
    for x in bank(p):
     if x['t']=='escolha' and x.get('p'):questions[(p.parent.name.replace('licao-',''),x['p'])]=x
   s=(ROOT/f'm{m}/index.html').read_text('utf-8');units=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
   for unit in units:
    for x in unit.get('pool',[]):
     c=questions.get((x.get('_l'),x.get('p')))
     if not c or x['t']!='escolha':continue
     expected=c['o'][c['c']]
     if expected in x['o']:matched+=1;self.assertEqual(x['o'][x['c']],expected,(x['_l'],x['p']))
  self.assertGreaterEqual(matched,188)
 def test_teaching_and_language_distinction(self):
  c=bank(ROOT/'m3/licao-m3-f11/index.html');self.assertEqual(len(c),20);self.assertIn('Exemplo escrito para esta lição',c[2]['html']);self.assertIn('Nota fiel e seletiva',c[2]['html']);self.assertIn('O tétum não é uma variedade',c[2]['html']);self.assertFalse(c[11]['v']);self.assertIn('registo',c[16]['p']);self.assertIn('sem voltar ao modelo',c[19]['html'])
 def test_challenge_does_not_restore_old_examples(self):
  s=(ROOT/'m3/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for unit in u:
   for x in unit.get('pool',[]):
    if x.get('_l')=='m3-f11':
     t=json.dumps(x,ensure_ascii=False);self.assertNotIn('tem vinte',t);self.assertNotIn('continua a mandar',t);self.assertNotIn('o «tu» é de Portugal',t)
 def test_teacher_prompts_follow_lesson(self):
  c=bank(ROOT/'m3/licao-m3-f11/index.html');s=(ROOT/'m3/painel-m3-f11/index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
  for x in panel:self.assertEqual(x['p'],c[x['k']].get('p',c[x['k']].get('frase','')))
if __name__=='__main__':unittest.main()
