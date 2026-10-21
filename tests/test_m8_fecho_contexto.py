from pathlib import Path
import json, unittest
ROOT = Path(__file__).resolve().parents[1]
def bank(rel, marker='CARTOES='):
    return json.JSONDecoder().raw_decode((ROOT/rel).read_text('utf-8').split(marker,1)[1])[0]
class FechoContexto(unittest.TestCase):
    def test_irony_evidence_is_available_in_both_questions_and_panel(self):
        cards=bank('m8/licao-m8-f05/index.html')
        panel={c['k']:c for c in bank('m8/painel-m8-f05/index.html')}
        for i in (15,18):
            support=cards[i].get('cita','')
            for clue in ('não versos do poema','nove e cinquenta','chegada às onze','tom de censura'):
                self.assertIn(clue,support)
            self.assertEqual(panel[i]['cita'],support)
    def test_anaphoric_reference_has_antecedent_and_correct_agent(self):
        c=bank('m8/licao-m8-f06/index.html')
        self.assertIn('A personagem olhou o espelho. Nele viu outra mulher',c[2]['html'])
        self.assertIn('o que a personagem viu no espelho',c[20]['html'])
        self.assertEqual(dict(c[21]['pares'])['viu outra mulher'],'o que a personagem viu no espelho')
        self.assertIn('sujeito',c[21]['f'])
        self.assertNotIn('o que se diz do espelho',json.dumps(c,ensure_ascii=False))
    def test_generic_reading_and_retrieval_task_are_explicit(self):
        c=bank('m8/licao-m8-f06/index.html')
        self.assertIn('Em geral',next(x for x,y in c[17]['pares'] if y=='genérico'))
        self.assertIn('mecanismo de coesão',c[12]['p'])
    def test_standalone_challenge_supplies_the_antecedent(self):
        units=bank('m8/index.html','var U=')
        pairs=[pair for u in units for c in u.get('pool',[]) if c.get('_l')=='m8-f06' for pair in c.get('pares',[]) if 'viu outra mulher' in pair[0]]
        self.assertTrue(pairs)
        for pair in pairs:self.assertIn('A personagem olhou o espelho.',pair[0])
    def test_exam_comparison_does_not_require_a_third_author(self):
        s=next(s for s in json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))['sessions'] if s['id']=='s17')
        self.assertIn('dois poemas',s['writing']['prompt'])
        self.assertIn('dois poemas',s['writing']['criteria'][0])
        self.assertIn('Não é necessário acrescentar um terceiro autor',s['correction']['steps'][0]['detail'])
        self.assertEqual(len(s['resources']),3)
if __name__=='__main__':unittest.main()
