"""01/11/2026: 27 aquecimentos extensos, com opções e proveniência verificáveis."""
import json
from pathlib import Path
import re
import sys
import unittest
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import exame_aquecimentos as G


class AquecimentosExame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sessions = json.loads((ROOT / 'assets/exame/sessoes.json').read_text('utf-8'))['sessions']
        cls.banks = {p.stem: json.loads(p.read_text('utf-8')) for p in (ROOT / 'docs/pedagogia/exame-aquecimentos').glob('s*.json')}

    def test_todas_as_sessoes_com_doze_e_variedade(self):
        self.assertEqual(set(self.banks), {s['id'] for s in self.sessions})
        for sid, bank in self.banks.items():
            with self.subTest(sessao=sid):
                self.assertEqual([], G.validar(bank))
                for c in bank['cartoes']:
                    rel = c['recycledFrom'].removeprefix('/pt/')
                    self.assertTrue((ROOT / rel / 'index.html').is_file(), rel)

    def test_as_tres_perguntas_anteriores_estao_presentes(self):
        for session in self.sessions:
            old = {c['legacyId']: c for c in self.banks[session['id']]['cartoes'] if 'legacyId' in c}
            self.assertEqual(set(old), {q['id'] for q in session['warmup']})
            for q in session['warmup']:
                # 01/11/2026: preserva as perguntas e explicações, permitindo apenas a marcação de itálico.
                self.assertEqual(G.limpa(old[q['id']]['p']), G.limpa(q['q']))
                self.assertEqual(G.limpa(old[q['id']]['f']), G.limpa(q['feedback']))

    def test_paginas_atualizadas_e_motor_partilhado(self):
        for sid, d in self.banks.items():
            actual = (ROOT / 'exame/aquecimentos' / sid / 'index.html').read_text('utf-8')
            self.assertEqual(actual, G.pagina(d))
            self.assertIn('assets/pt-lessons/jogo.js', actual)
            self.assertIn('data-c-como', actual)
            self.assertNotRegex(actual, r'data-s=|class="gt"|class="gl"')

    def test_ajudas_existentes(self):
        for name in ('escolher', 'verdadeiro-falso', 'ligar-pares', 'ligar-lados', 'ordenar', 'tocar-palavras', 'completar'):
            self.assertTrue((ROOT / 'como' / (name + '.mp4')).is_file(), name)

    def test_textos_autorais_da_sessao_consultaveis_nos_cartoes(self):
        # 01/11/2026: uma pergunta que remete para o apoio tem o texto também na página própria.
        for s in self.sessions:
            if s['source'].get('excerpt'):
                html = ''.join(c.get('html', '') for c in self.banks[s['id']]['cartoes'] if c['t'] == 'ler')
                self.assertIn(s['source']['excerpt'], unescape(html))

    def test_tempos_e_chaves(self):
        for s in self.sessions:
            self.assertEqual(s['durationMinutes'], 50)
            self.assertEqual(10 + 8 + s['writing']['minutes'] + 27 - s['writing']['minutes'] + 5, 50)
        js = (ROOT / 'assets/exame/aquecimento.js').read_text('utf-8')
        self.assertIn("'aquecimento-exame-' + d.sessao", js)
        self.assertIn('projetado ? null', js)
        self.assertNotIn('localStorage.setItem', js)


if __name__ == '__main__':
    unittest.main()
