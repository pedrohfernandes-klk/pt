import json,re,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import validate_cards
def bank(path):return json.JSONDecoder().raw_decode(path.read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class RevisionActivities(unittest.TestCase):
 def test_revision_requires_evidence_and_unique_fragment(self):
  for n in ['08','09']:
   a=bank(ROOT/f'm2/licao-m2-f{n}/index.html');revisions=[c for c in a if c['t']=='rever'];self.assertEqual(1,len(revisions));self.assertEqual([],validate_cards(a))
   x=revisions[0]
   for invalid in [dict(x,trecho='ausente'),dict(x,apoio=''),dict(x,c=99)]:self.assertTrue(validate_cards([invalid]))
   self.assertEqual(len(x['o']),len(x['fe']))
 def test_no_extra_cards_or_delivery_rules_removed(self):
  a,b=bank(ROOT/'m2/licao-m2-f08/index.html'),bank(ROOT/'m2/licao-m2-f09/index.html')
  self.assertEqual([22,20],[len(a),len(b)]);self.assertIn('180–240',a[4]['html']);self.assertIn('etapa 2',a[4]['html']);self.assertIn('Encomenda por curso',b[2]['html'])
  self.assertEqual('sublinhar',a[6]['t']);self.assertEqual('emparelhar',a[11]['t']);self.assertEqual('ordenar',b[12]['t']);self.assertIn('não uma receita única',b[12]['f'])
 def test_panels_match_current_lesson_indices(self):
  for n in ['08','09']:
   a=bank(ROOT/f'm2/licao-m2-f{n}/index.html');rows=bank(ROOT/f'm2/painel-m2-f{n}/index.html')
   self.assertEqual([i for i,c in enumerate(a) if c['t']!='ler'],[r['k'] for r in rows])
   for row in rows:self.assertEqual(a[row['k']]['t'],row['t']);self.assertEqual(a[row['k']].get('p',a[row['k']].get('frase','')),row['p'])
 def test_revision_plugin_available_in_lesson_and_challenge(self):
  for path in ['m2/index.html','m2/licao-m2-f08/index.html','m2/licao-m2-f09/index.html']:
   self.assertIn('rever-frase.js?v=20261021',(ROOT/path).read_text('utf-8'))
 def test_challenge_has_the_same_revision_cards(self):
  s=(ROOT/'m2/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s[re.search(r'\bU\s*=\s*(\[)',s).start(1):])[0]
  for n in ['08','09']:
   lesson=next(c for c in bank(ROOT/f'm2/licao-m2-f{n}/index.html') if c['t']=='rever');copy=next(c for unit in u for c in unit['pool'] if c.get('_l')=='m2-f'+n and c['t']=='rever')
   for field in ['p','apoio','frase','trecho','o','c','f','fe']:self.assertEqual(lesson[field],copy[field])
if __name__=='__main__':unittest.main()
