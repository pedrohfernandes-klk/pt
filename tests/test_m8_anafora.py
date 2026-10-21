"""Reference tasks retain saved-answer meaning and avoid punctuation heuristics."""
from pathlib import Path
import json
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links = []; self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.links.append(dict(attrs))


class Anafora(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT/'m8/anafora-catafora/index.html').read_text('utf-8')
        start = self.text.index('var E={"pasta"') + 6
        self.data = json.JSONDecoder().raw_decode(self.text[start:])[0]

    def test_existing_progress_keeps_its_meaning(self):
        p = self.data['passos']
        self.assertEqual(self.data['id'], 'anafora-catafora')
        self.assertEqual([s['tipo'] for s in p], ['leitura','classificar','unica','lacuna','julgar','unica'])
        self.assertEqual([s['nivel'] for s in p], [1,1,1,2,2,3])
        self.assertEqual([x[1] for x in p[1]['itens']], [0,1,0,1])
        self.assertEqual([o[1] for o in p[2]['opcoes']], ['cuidado','cuidado','certo'])
        self.assertEqual([v['opcoes'][0] for v in p[3]['versos']], ['Isto','Ela'])
        self.assertEqual([c[1] for c in p[4]['casos']], [True,False,True,False])
        self.assertEqual([o[1] for o in p[5]['opcoes']], ['cuidado','certo','cuidado'])

    def test_targets_and_reference_are_distinct_from_direction(self):
        p = self.data['passos']
        for item in p[1]['itens']: self.assertIn('Analisa', item[0])
        self.assertIn('ambíguo', p[1]['retorno'])
        self.assertIn('ambos aparecem antes', p[1]['retorno'])
        self.assertIn('retoma especificamente «a carta»', p[3]['pergunta'])
        self.assertEqual(p[3]['versos'][1]['opcoes'], ['Ela','Ele','Elas'])
        self.assertIn('não dos dois pontos', p[3]['retorno'])
        self.assertNotIn('Antes dos dois pontos, aponta-se', p[3]['retorno'])

    def test_model_help_and_transfer_are_available(self):
        p=self.data['passos']
        self.assertIn('<details>', p[0]['html'])
        self.assertIn('Substitui', p[0]['html'])
        self.assertIn('oralmente ou no caderno', p[5]['opcoes'][1][2])
        self.assertIn('Assinala o referente', p[5]['opcoes'][1][2])

    def test_optional_navigation_does_not_add_required_activity(self):
        lesson=(ROOT/'m8/licao-m8-f06/index.html').read_text('utf-8')
        url='https://pedrohfernandes-klk.github.io/pt/m8/anafora-catafora/'
        links=[a for a in Links(lesson).links if a.get('href')==url]
        self.assertEqual(len(links),1)
        self.assertNotIn('data-ativ',links[0])
        self.assertIn('A2ID="gramatica-aspeto"',lesson)
        self.assertTrue(any(a.get('href','').endswith('/m8/licao-m8-f06/') for a in Links(self.text).links))


if __name__ == '__main__': unittest.main()
