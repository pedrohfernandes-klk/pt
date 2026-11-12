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
        # 06/11/2026: o desenho comum dos nove índices (decisão 148) é a camada mais recente, por cima dos créditos atrás de um «i»; desfaz-se primeiro, com a mesma exigência.
        # 07/11/2026: os três acertos dos índices deixados pela decisão 173 são a camada mais recente, por cima do desenho comum dos nove índices; desfazem-se primeiro, com a mesma exigência.
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): a decisão 152 no M1 (cuidado_m1_20261106) passa a camada mais recente, por cima dos acertos da decisão 173; desfaz-se primeiro, com a mesma exigência.
        # 07/11/2026: os créditos atrás de um «i» na entrada, nos índices e no Atlas (creditos_i_pt1_20261107, pedido pt-1) passam a camada mais recente, por cima da decisão 152 no M1; desfazem-se primeiro, com a mesma exigência.
        # 08/11/2026: o cartaz «Ler a cidade» na entrada e o nome novo da secção nas páginas publicadas (cidade_cartaz_20261108) passam a camada mais recente, por cima dos créditos atrás de um «i» do pedido pt-1 (e mudam páginas desta cadeia: a entrada, os índices e a frase da sugestão «continua»); desfazem-se primeiro, com a mesma exigência.
        # 08/11/2026: a decisão 152 no M2 (cuidado_m2_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M2, incluindo o índice do módulo) passa a camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção; desfaz-se primeiro, com a mesma exigência.
        # 08/11/2026: a decisão 152 no M3 (cuidado_m3_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M3, incluindo o índice, o guia e o mapa do módulo) passa a camada mais recente, por cima da decisão 152 no M2; desfaz-se primeiro, com a mesma exigência.
        # 08/11/2026: a decisão 152 no M4 (cuidado_m4_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M4, incluindo o índice, o guia, o mapa e o portefólio do módulo) passa a camada mais recente, por cima da decisão 152 no M3; desfaz-se primeiro, com a mesma exigência.
        # 08/11/2026: a decisão 152 no M5 (cuidado_m5_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M5, incluindo o índice, o guia, o mapa e o portefólio do módulo, e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M4; desfaz-se primeiro, com a mesma exigência.
        # 08/11/2026: a decisão 152 no M6 (cuidado_m6_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M6, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M5; desfaz-se primeiro, com a mesma exigência.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M9, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», as atividades e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        result = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cartaz_cabecalho_20261103.json', '--manifesto', str(MANIFEST), '--verificar', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m9-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m8-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m7-edits-20261111.json', '--desfazer-antes', 'tests/fixtures/cuidado-m6-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cidade-cartaz-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/creditos-i-pt1-edits-20261107.json', '--desfazer-antes', 'tests/fixtures/cuidado-m1-edits-20261106.json', '--desfazer-antes', 'tests/fixtures/indices-acertos-edits-20261107.json', '--desfazer-antes', 'tests/fixtures/cartaz-indices-148-edits-20261106.json', '--desfazer-antes', 'tests/fixtures/creditos-i-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/atlas-lote3-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/autonomia-154-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/exame-contexto-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/exame-licao-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/tabela-movimentos-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/revisao-edits-20261105.json'], cwd=ROOT, capture_output=True)
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
