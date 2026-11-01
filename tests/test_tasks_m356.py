"""31/10/2026: decisões 20 a 25 nas tarefas e nos guias do M3, M5 e M6."""
from pathlib import Path
import json
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TasksM356(unittest.TestCase):
    def test_extras_sem_exemplos_e_quatro_blocos(self):
        for m in (3, 5, 6):
            s = (ROOT / f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
            extras, _ = json.JSONDecoder().raw_decode(s.split('T=', 1)[1])
            self.assertTrue(extras)
            for extra in extras:
                self.assertTrue(extra['extra'])
                self.assertFalse({'exemplo', 'fraco'} & extra.keys())
            blocks, _ = json.JSONDecoder().raw_decode(s.split('BLOCOS=', 1)[1])
            self.assertEqual([x[0] for x in blocks], [10, 5, 60, 15])
            self.assertIn('Extras sem nota', s)

    def test_pesos_coerentes_e_entregas_das_duas_unidades(self):
        for m in (3, 5, 6):
            for path in (f'm{m}/index.html', f'm{m}/guia-da-tarefa-m{m}/index.html', f'm{m}/mapa-do-modulo-m{m}/index.html'):
                s = (ROOT / path).read_text('utf-8')
                weights = re.search(r'<p class="avaliacao-tarefas">(.*?)</p>', s)[1]
                self.assertEqual(re.findall(r'(\d+) %', weights), ['30', '30', '10', '30'])
                self.assertIn('mesma grelha /20', weights)
            portfolio = (ROOT / f'm{m}/portefolio-do-modulo-m{m}/index.html').read_text('utf-8')
            for u in (1, 2):
                self.assertIn(f'../../tarefas/m{m}-u{u}/', portfolio)
            self.assertNotIn(f'M{m}_Tarefa3', portfolio)

    # 01/11/2026: nenhum texto entre a barra e header.topo no percurso do módulo.
    def test_abertura_e_guias_sem_corrupcao_css(self):
        for m in (3, 5, 6):
            s = (ROOT / f'm{m}/index.html').read_text('utf-8')
            self.assertGreater(s.find('class="avaliacao-tarefas"'), s.find('<h1'))
            self.assertIn('Cada unidade termina na sua aula de tarefa', s)
            guia = (ROOT / f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
            for errado in ('#5c5a60', '#607a24', 'rgba(260,260,260,.15)', '.bloco.feito{opacity:.60}'):
                self.assertNotIn(errado, guia)
            self.assertIn('#arquivo-producoes>summary{min-height:44px', guia)
            self.assertIn('#arquivo-producoes>summary{min-height:88px', guia)

    def test_camada_literal_aplicada_e_reversivel(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py',
                            'scripts/tarefas_m356_20261031.json', '--manifesto',
                            'tests/fixtures/tarefas-m356-edits-20261031.json', '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main()
