from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(key):return json.JSONDecoder().raw_decode((ROOT/'m6'/('licao-'+key)/'index.html').read_text('utf-8').split('CARTOES=',1)[1])[0]
class OracoesContexto(unittest.TestCase):
 def test_teaches_relation_and_limits(self):
  c=bank('m6-f04');self.assertEqual(len(c),24);self.assertIn('não é um teste seguro',c[1]['html']);self.assertIn('frases didáticas inventadas',c[4]['html']);self.assertIn('substantiva relativa',c[4]['html']);self.assertIn('gerundiva',c[4]['html']);self.assertIn('antecedente',c[12]['lacunas'][1]['o'])
 def test_pois_has_context_and_cause_is_not_contrast(self):
  c=bank('m6-f04');self.assertIn('E eu sigo',c[10]['p']);self.assertIn('M6-F07',c[4]['html']);self.assertIn('didático',c[19]['f']);self.assertIn('não estabelece',c[19]['f']);self.assertIn('coordenação',c[18]['p']);self.assertIn('sujeito subentendido',c[22]['f'])
 def test_companion_and_panel_match(self):
  d=bank('m6-f09');self.assertEqual(len(d),21);self.assertIn('Exemplo didático',d[13]['pares'][2][0]);self.assertIn('antecedente',d[13]['f'])
  for key in ['m6-f04','m6-f09']:
   c=bank(key);s=(ROOT/'m6'/('painel-'+key)/'index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
   for x in panel:self.assertEqual(x['p'],c[x['k']].get('p',c[x['k']].get('frase','')))
 def test_challenge_does_not_restore_unsafe_rules(self):
  s=(ROOT/'m6/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for unit in u:
   for x in unit.get('pool',[]):
    if x.get('_l') in ['m6-f04','m6-f09']:
     t=json.dumps(x,ensure_ascii=False);self.assertNotIn('teste «o qual se enche»',t);self.assertNotIn('«O qual dê a essa visão»',t);self.assertNotIn('«que» troca-se por «o qual»',t)
if __name__=='__main__':unittest.main()
