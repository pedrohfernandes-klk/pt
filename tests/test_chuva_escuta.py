"""A leitura da parte VI tem apoio textual e corresponde ao painel da aula."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def cards(path):
    text = (ROOT / path).read_text(encoding='utf-8')
    return json.JSONDecoder().raw_decode(text.split('CARTOES=', 1)[1])[0]

class ChuvaEscuta(unittest.TestCase):
    def setUp(self):
        self.lesson = cards('m7/licao-m7-f34/index.html')

    def test_video_tem_texto_alternativo_da_parte_que_e_lida(self):
        reading = next(c for c in self.lesson if c.get('rot') == 'Escutar e ler · VI')
        self.assertIn('BX14TEVc76k', reading['html'])
        self.assertIn('com ou sem som', reading['html'])
        for proof in ('O maestro sacode a batuta', 'Todo o teatro é o meu quintal',
                      'a música cessa como um muro que desaba', '23621'):
            self.assertIn(proof, reading['html'])
        self.assertEqual(sum('data-yt="BX14TEVc76k"' in c.get('html', '')
                             for c in self.lesson), 1)

    def test_escuta_tem_recuperacao_analise_e_comparacao_com_feedback(self):
        activities = [c for c in self.lesson if str(c.get('g', '')).startswith('escuta-vi-')]
        self.assertEqual(len(activities), 3)
        self.assertEqual(len({c['g'] for c in activities}), 3) # três operações essenciais na seleção
        for c in activities:
            self.assertTrue(c['f'])
            self.assertEqual(len(c['o']), len(c['fe']))
            self.assertIsNone(c['fe'][c['c']])
            self.assertTrue(all(f for i, f in enumerate(c['fe']) if i != c['c']))
        self.assertIn('Compara I e VI', activities[-1]['p'])

    def test_painel_lanca_todas_as_perguntas_reais_da_ficha(self):
        panel = cards('m7/painel-m7-f34/index.html')
        expected = {i for i, c in enumerate(self.lesson) if c['t'] != 'ler'}
        self.assertEqual({c['k'] for c in panel}, expected)
        for c in panel:
            actual = self.lesson[c['k']]
            self.assertEqual(c['t'], actual['t'])
            # Textos antigos do painel podem ser abreviados; novos são completos.
            if str(actual.get('g', '')).startswith('escuta-vi-'):
                self.assertEqual(c['p'], actual['p'])
