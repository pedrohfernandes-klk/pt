import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_teacher_parity import audit,compare,digest

class TeacherParityAudit(unittest.TestCase):
    def setUp(self):
        self.cards=[{'t':'ler','html':'Leitura'}, {'t':'escolha','p':'Que prova?','o':['a','b'],'c':0,'f':'Porque a.'}]
        self.controls=[{'k':1,'t':'escolha','p':'Que prova?'}]

    def test_aligned_bank_preserves_answer_and_feedback_identity(self):
        r=compare(self.cards,self.controls)
        self.assertTrue(r['exact_bank']);self.assertEqual(r['statuses'],{'matched':1})
        self.assertEqual(r['rows'][0]['resolved']['answer']['c'],0)
        self.assertEqual(r['rows'][0]['resolved']['feedback']['f'],'Porque a.')
        altered={**self.cards[1],'c':1}
        self.assertNotEqual(digest(altered),digest(self.cards[1]))

    def test_reading_negative_and_out_of_range_are_distinct_from_label_drift(self):
        controls=[{'k':0,'t':'escolha','p':'Antiga'}, {'k':-1}, {'k':2}, {'k':1,'t':'vf','p':'Antiga'}]
        r=compare(self.cards,controls)
        self.assertEqual(r['statuses'],{'reading_target':1,'invalid_index':2,'different_question':1})
        self.assertEqual(r['uncovered_current'],self.controls)

    def test_missing_or_editorial_panel_is_not_silently_certified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'m4/licao-m4-f99/index.html';p.parent.mkdir(parents=True)
            p.write_text('var CARTOES='+json.dumps(self.cards),encoding='utf-8')
            before=p.read_bytes();r=audit(root)
            self.assertEqual(r['summary']['panels'],{'missing_panel':1})
            panel=root/'m4/painel-m4-f99/index.html';panel.parent.mkdir()
            panel.write_text('<p>Guiao editorial</p>',encoding='utf-8')
            r=audit(root);self.assertEqual(r['summary']['panels'],{'editorial_panel':1})
            self.assertEqual(r['summary']['unverified'],1);self.assertEqual(p.read_bytes(),before)

    def test_empty_module_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=audit(Path(tmp));self.assertEqual(r['missing_modules'],['m4'])
            self.assertEqual(r['summary']['unverified'],1)

if __name__=='__main__':unittest.main()
