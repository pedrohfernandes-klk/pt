from pathlib import Path
import json,sys,unittest,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
class ExamAlignment(unittest.TestCase):
 def setUp(self):self.sessions=json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))['sessions']
 def test_recycled_answers_match_current_lessons(self):
  matches=0
  for s in self.sessions:
   # Authored video case studies have their own comprehension tests; they do not
   # recycle answers from a lesson bank. Existing recycled sessions stay checked.
   if s['source'].get('original'):continue
   cards=lesson_cards(ROOT/s['source']['url'].removeprefix('/pt/')/'index.html')
   for q in s['warmup']:
    for c in cards:
     if q['q'] not in [c.get('p'),c.get('p2')]:continue
     if c['t']=='escolha':answer=c['o'][c['c']]
     elif c['t']=='vf':answer='Verdadeiro' if c['v'] else 'Falso'
     else:continue
     self.assertEqual(q['options'][q['answer']],answer,q['id'])
     self.assertEqual(q['feedback'],c['f'].replace('**',''),q['id']);matches+=1
  self.assertGreaterEqual(matches,30)
 def test_s18_q1_conserva_a_resposta_da_licao(self):
  # 07/11/2026: o enunciado de s18-q1 passou a nomear o conto e a autora (pt #155, achado 41) e deixou de ser igual ao da
  # lição m8-f08, por isso o teste anterior já não o conferia (48 perguntas em vez de 49). Confere-se aqui pela pergunta
  # da lição: a resposta, na pergunta e na verificação «Depois da revisão», tem de ser a mesma; a explicação fica de fora,
  # porque mudou de propósito (a da lição remete para o resumo-modelo, que não está no exame).
  s=next(x for x in self.sessions if x['id']=='s18')
  cards=lesson_cards(ROOT/s['source']['url'].removeprefix('/pt/')/'index.html')
  licao=[c for c in cards if c.get('p')=='O que acontece em «George»?' and c['t']=='escolha']
  self.assertEqual(len(licao),1)
  resposta=licao[0]['o'][licao[0]['c']]
  q=next(x for x in s['warmup'] if x['id']=='s18-q1')
  self.assertEqual(q['q'],'O que acontece em «George», conto de Maria Judite de Carvalho?')
  self.assertEqual(q['options'][q['answer']],resposta)
  check=s['correction']['check']
  self.assertEqual(check['q'],'Depois da revisão: '+q['q'])
  self.assertEqual(check['options'][check['answer']],resposta)
 def test_support_targets_exist_and_cantigas_supply_mendinho(self):
  for s in self.sessions:
   for ref in [s['source']]+s['resources']:
    self.assertTrue((ROOT/ref['url'].removeprefix('/pt/')/'index.html').is_file(),(s['id'],ref))
  s=self.sessions[0]
  # 27/10/2026: o recorte achatado passou a textos compostos (versos, notas, crédito); ver test_exame_textos.py.
  mendinho=s['source']['passages'][2]
  self.assertIn('Nom hei [eu] i barqueiro nem remador',[l for st in mendinho['stanzas'] for l in st])
  self.assertIn('morte consumada',mendinho['note'])
  self.assertTrue(any('m1-f02' in r['url'] for r in s['resources']))
 def test_interpretation_limits_and_specific_terms(self):
  by={s['id']:s for s in self.sessions}
  self.assertNotIn('quem partiu descontente',by['s04']['warmup'][1]['q'])
  self.assertIn('não deve ser classificada como sinestesia',by['s11']['warmup'][2]['feedback'])
  self.assertIn('não é, por si só, um recuo',by['s19']['warmup'][1]['feedback'])
  self.assertTrue(all(any('diferente' in st['detail'] for st in s['correction']['steps']) for s in self.sessions))
if __name__=='__main__':unittest.main()
