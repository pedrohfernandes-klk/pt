import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards,validate_cards
from sync_teacher_labels import expected_cards


class ObservarImaginar(unittest.TestCase):
    def test_observation_and_imagination_are_not_mutually_exclusive(self):
        c=lesson_cards(ROOT/'m6/licao-m6-f07/index.html')
        self.assertEqual(validate_cards(c),[])
        self.assertEqual(len(c),34)
        self.assertEqual(c[16]['t'],'escolha')
        self.assertEqual(c[16]['c'],0)
        self.assertEqual(len(c[16]['fe']),len(c[16]['o']))
        self.assertTrue(all(c[16]['fe'][i] for i in (1,2,3)))
        self.assertIn('mausoléos',c[16]['p'])
        self.assertIn('mausoléos',c[16]['p2'])
        self.assertIn('ponto de partida',c[28]['html'])
        self.assertIn('não torna a observação neutra',c[29]['f'])
        self.assertNotIn('não da imaginação',c[16]['f'])

    def test_hypallage_is_not_defined_by_word_order(self):
        c=lesson_cards(ROOT/'m6/licao-m6-f07/index.html')
        self.assertIn('ordem muda',c[30]['html'])
        self.assertIn('transferência',c[32]['f'])
        self.assertNotIn('hipálage está na ordem',c[32]['f'])
        self.assertIn('dois desenhos',c[33]['html'])
        self.assertIn('pormenor observado',c[33]['html'])

    def test_module_copy_and_teacher_labels_preserve_context(self):
        lesson=ROOT/'m6/licao-m6-f07/index.html'
        c=lesson_cards(lesson)
        s=(ROOT/'m6/index.html').read_text('utf-8')
        u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
        copies=[x for unit in u for x in unit['pool'] if x.get('_l')=='m6-f07' and x.get('p')==c[16]['p']]
        self.assertEqual(len(copies),1)
        for k in ('p','o','c','f','fe'):self.assertEqual(copies[0][k],c[16][k])
        self.assertNotIn('não da imaginação',s)
        s=(ROOT/'m6/painel-m6-f07/index.html').read_text('utf-8')
        panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
        self.assertEqual(panel,expected_cards(lesson))


if __name__=='__main__':unittest.main()
