"""03/11/2026: contrato da camada visual da entrada, acima dos créditos publicados."""
from pathlib import Path
import hashlib
import json
import re
from collections import Counter
import subprocess
import sys
import unittest
# 05/11/2026: a revisão de 5/11 está por cima do cabeçalho.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditoria_20261028 import undo_revisao_0511

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/cartaz-cabecalho-edits-20261103.json'


class CabecalhoCartaz(unittest.TestCase):
    # 03/11/2026: três trocas fechadas; retirada autorizada e destinos preservados em Mais.
    def test_camada_reversivel_e_destinos_preservados(self):
        manifest = json.loads(MANIFEST.read_text('utf-8'))
        self.assertEqual(set(manifest['files']), {'index.html'})
        record = manifest['files']['index.html']
        self.assertEqual(len(record['edits']), 3)
        # 05/11/2026: a revisão de 5/11 (por cima) desfaz-se primeiro, com contagem estrita; o resto fica igual.
        current = undo_revisao_0511('index.html', (ROOT / 'index.html').read_text('utf-8'))
        original = current
        for edit in reversed(record['edits']):
            self.assertEqual(original.count(edit['new']), edit['occurrences'])
            original = original.replace(edit['new'], edit['old'])
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), record['base_sha256_lf'])
        rebuilt = original
        for edit in record['edits']:
            self.assertEqual(rebuilt.count(edit['old']), edit['occurrences'])
            rebuilt = rebuilt.replace(edit['old'], edit['new'])
        self.assertEqual(current, rebuilt)
        self.assertEqual(Counter(re.findall(r'<a\b[^>]*href="([^"]+)"', current)),
                         Counter(re.findall(r'<a\b[^>]*href="([^"]+)"', original)))
        self.assertNotIn('<aside class="ed-sugestao"', current)
        self.assertNotIn('data-reabrir', current)
        self.assertIn('id="ed-sugestao-titulo"', current)
        self.assertIn('Grafismo gerado com recurso a IA', original)

    def test_gerador_idempotente(self):
        # 05/11/2026: a revisão de 5/11 (por cima) desfaz-se antes de conferir o cabeçalho; a conferência fica igual.
        # 05/11/2026: a tabela dos seis movimentos é a camada mais recente; desfaz-se antes da revisão, com a mesma exigência.
        # 05/11/2026: o Laboratório do exame (lição, não «leitura de apoio») é a camada mais recente; desfaz-se antes da tabela dos seis movimentos.
        # 05/11/2026: o contexto de cada sessão do Laboratório do exame (lição e excerto, não «recorte») é a camada mais recente; desfaz-se antes da ligação e das notas do Laboratório do exame.
        # 05/11/2026: a decisão 154 (os exercícios fazem-se sozinho; nada no texto do aluno depende do docente) é a camada mais recente; desfaz-se antes do contexto do Laboratório do exame, com a mesma exigência.
        # 06/11/2026: o lote 3 do Atlas fica por cima da decisão 154 depois de juntar o main; desfaz-se primeiro, com a mesma exigência.
        # 06/11/2026: os créditos atrás de um «i» (decisão 153, pedido pt-2) são a camada mais recente, por cima do lote 3 do Atlas e da decisão 154 (junção com o main); desfazem-se primeiro, com a mesma exigência.
        result = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cartaz_cabecalho_20261103.json', '--manifesto', str(MANIFEST), '--verificar', '--desfazer-antes', 'tests/fixtures/creditos-i-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/atlas-lote3-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/autonomia-154-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/exame-contexto-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/exame-licao-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/tabela-movimentos-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/revisao-edits-20261105.json'], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_css_sem_motor_novo_nem_imposicoes(self):
        css = (ROOT / 'assets/cartaz-cabecalho.css').read_text('utf-8')
        self.assertNotIn('!important', css)
        self.assertNotIn('@keyframes', css)
        self.assertIn('body[data-site="pt"] .raiz', css)
        self.assertIn('html.epi-projection', css)
        self.assertIn('@media print', css)
        self.assertFalse((ROOT / 'assets/cartaz-cabecalho.js').exists())


if __name__ == '__main__':
    unittest.main()
