"""Protect the companion activity's stable scoring and contextualised prompts."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


def support():
    text=(ROOT/'m5/gram-dil/index.html').read_text(encoding='utf-8')
    start=text.index('{"pasta":"Ler-a-fundo"')
    return json.JSONDecoder().raw_decode(text[start:])[0]


class CompanionContext(unittest.TestCase):
    def test_structure_and_existing_scoring_remain_stable(self):
        data=support();steps=data['passos']
        self.assertEqual(data['id'],'gram-dil')
        self.assertEqual(len(steps),9)
        source=(ROOT/'m5/gram-dil/index.html').read_text(encoding='utf-8')
        self.assertEqual(source.count('<b>9</b><small>passos</small>'),1)
        self.assertEqual([(s['nivel'],s['tipo']) for s in steps],[
            (1,'leitura'),(1,'unica'),(1,'unica'),(2,'multi'),(2,'classificar'),
            (3,'unica'),(3,'unica'),(3,'multi'),(3,'unica')])
        self.assertEqual([[o[1] for o in s.get('opcoes',[])] for s in steps],[
            [],['cuidado','certo','cuidado'],['cuidado','cuidado','certo'],[5,5,5,0],[],
            ['cuidado','certo','cuidado'],['certo','cuidado','cuidado'],[5,-5,5,5,-5],
            ['cuidado','certo','cuidado']])
        self.assertEqual([i[1] for i in steps[4]['itens']],[0,1,2,2])

    def test_relating_and_reformulating_have_local_evidence(self):
        steps=support()['passos']
        self.assertIn('Ega mostrou-se impressionado',steps[1]['pergunta'])
        self.assertIn('emfim',steps[2]['pergunta'])
        for i in (5,7):
            self.assertIn('No dia seguinte',steps[i]['pergunta'])
            self.assertIn('sem o trabalho à vista',steps[i]['pergunta'])
        self.assertIn('ele não entregava',steps[8]['pergunta'])
        self.assertIn('mesmo momento e lugar',steps[0]['html'])
        self.assertIn('não chegam',steps[3]['opcoes'][1][2].lower())


if __name__=='__main__':unittest.main()
