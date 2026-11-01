import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards,validate_cards
from sync_teacher_labels import expected_cards

class RetomasClaras(unittest.TestCase):
    def test_review_moves_from_identification_to_disambiguation(self):
        c=lesson_cards(ROOT/'m8/licao-m8-f12/index.html')
        self.assertEqual(validate_cards(c),[])
        self.assertEqual(len(c),22)
        self.assertEqual(c[9]['t'],'vf');self.assertFalse(c[9]['v'])
        self.assertIn('poeta',c[9]['p']);self.assertIn('editora',c[9]['p2'])
        self.assertIn('inventado',c[1]['html'])
        self.assertEqual([x['c'] for x in c[19]['lacunas']],[0,0])
        self.assertEqual(c[19]['lacunas'][0]['o'][0],'A editora')
        self.assertEqual(c[19]['lacunas'][1]['o'][0],'a poeta ou a editora')
        self.assertIn('a poeta',c[21]['html']);self.assertIn('conserves quem conversou',c[21]['html'])
        self.assertIn('Li o conto',lesson_cards(ROOT/'m8/licao-m8-f06/index.html')[18]['p'])

    def test_pool_and_panel_do_not_restore_the_old_review_question(self):
        path=ROOT/'m8/licao-m8-f12/index.html';c=lesson_cards(path)
        s=(ROOT/'m8/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
        copies=[x for unit in u for x in unit['pool'] if x.get('_l')=='m8-f12' and x.get('p')==c[9]['p']]
        self.assertEqual(len(copies),1)
        for k in ('p','v','f','fe'):self.assertEqual(copies[0][k],c[9][k])
        s=(ROOT/'m8/painel-m8-f12/index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
        self.assertEqual(panel,expected_cards(path))

if __name__=='__main__':unittest.main()
