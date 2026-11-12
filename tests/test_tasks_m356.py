# 03/11/2026: desfaz piloto M4, F0, créditos publicados e lote 2; asserções intactas.
# 02/11/2026: desfaz o lote 2 antes da base publicada; mesmas asserções.
# 01/11/2026: verificar as tarefas após desfazer índices e conteúdos.
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
                # 08/11/2026: decisão 152 no M5 (achados 0, 1 e 12): no M5, os pesos passam também a uma tabela de apoio, como no M3, com
                # a mesma exigência.
                if m in (3, 5):
                    # 08/11/2026: decisão 152 no M3 (achados 18, 19 e 20): no M3, os pesos passam a uma tabela de apoio logo antes do
                    # parágrafo, com espaço que não quebra entre o número e o «%»; o parágrafo fica com o resto. A mesma exigência: os
                    # quatro pesos, por esta ordem e com o componente certo, e nenhum peso fora da tabela.
                    tabela = re.search(r'<table class="apoio-tabela"[^>]*>((?:(?!</table>).)*)</table><p class="avaliacao-tarefas">', s)[1]
                    self.assertEqual(re.findall(r'<th scope="row"[^>]*>([^<]*)</th><td[^>]*>(\d+)\xa0%</td>', tabela),
                                     [('Tarefa da Unidade 1', '30'), ('Tarefa da Unidade 2', '30'), ('Provas rápidas', '10'),
                                      ('Prova escrita', '30')])
                    self.assertNotIn('%', weights)
                else:
                    # 08/11/2026: decisão 152 no M6 (achados 32, 33 e 34): no M6, os pesos ficam no parágrafo, com espaço que não quebra
                    # entre o número e o «%» e entre «grelha» e «/20» (U+00A0); a mesma exigência: os quatro pesos, por esta ordem, e
                    # nenhum com espaço normal.
                    sep = '\xa0' if m == 6 else ' '
                    self.assertEqual(re.findall(r'(\d+)' + sep + '%', weights), ['30', '30', '10', '30'])
                    if m == 6:
                        self.assertNotRegex(weights, r'\d %|grelha /20')
                self.assertIn('mesma grelha' + ('\xa0' if m == 6 else ' ') + '/20', weights)
            portfolio = (ROOT / f'm{m}/portefolio-do-modulo-m{m}/index.html').read_text('utf-8')
            for u in (1, 2):
                self.assertIn(f'../../tarefas/m{m}-u{u}/', portfolio)
            self.assertNotIn(f'M{m}_Tarefa3', portfolio)

    # 01/11/2026: nenhum texto entre a barra e header.topo no percurso do módulo.
    def test_abertura_e_guias_sem_corrupcao_css(self):
        # 01/11/2026: o M8 e o M9 entram com a mesma regra da dobra do arquivo (achado 2 do pt 145), sem tirar nenhum módulo.
        for m in (3, 5, 6, 8, 9):
            s = (ROOT / f'm{m}/index.html').read_text('utf-8')
            self.assertGreater(s.find('class="avaliacao-tarefas"'), s.find('<h1'))
            self.assertIn('Cada unidade termina na sua aula de tarefa', s)
            guia = (ROOT / f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
            for errado in ('#5c5a60', '#607a24', 'rgba(260,260,260,.15)', '.bloco.feito{opacity:.60}'):
                self.assertNotIn(errado, guia)
            # 01/11/2026: 44 px é o alvo do sistema; 88 px abria uma faixa vazia
            self.assertIn('#arquivo-producoes>summary{display:flex;gap:.6rem;align-items:center;list-style:none;'
                          'cursor:pointer;padding:.75rem 0;min-height:44px;font:700 .9rem/1.4 Arial,sans-serif}'
                          '#arquivo-producoes>summary::-webkit-details-marker{display:none}', guia)
            self.assertNotIn('min-height:88px', guia)

    # 01/11/2026: o número de aulas do «Neste módulo» conta os passos da unidade, como no M1 e no M7.
    def test_neste_modulo_conta_os_passos(self):
        for m in (3, 5, 6):
            s = (ROOT / f'm{m}/index.html').read_text('utf-8')
            U, _ = json.JSONDecoder().raw_decode(s[s.find('U=[') + 2:])
            aulas = [int(n) for n in re.findall(r'<small>(\d+) aulas de leitura/preparação', s)]
            self.assertEqual(aulas, [len(u['passos']) for u in U])

    # 01/11/2026: o número de aulas do índice é o número de li[data-passo] da unidade
    def test_neste_modulo_igual_aos_passos_do_percurso_m1_a_m7(self):
        for m in range(1, 8):
            s = (ROOT / f'm{m}/index.html').read_text('utf-8')
            aulas = [int(n) for n in re.findall(r'<small>(\d+) aulas de leitura/preparação', s)]
            passos = []
            for u in range(1, len(aulas) + 1):
                inicio = s.index(f'<section class="unidade" data-u="{u}">')
                fim = s.index('</ol>', s.index('<ol class="passos">', inicio))
                passos.append(len(re.findall(r'<li\b[^>]*\bdata-passo=', s[inicio:fim])))
            self.assertTrue(aulas, m)
            self.assertNotIn(f'<section class="unidade" data-u="{len(aulas) + 1}">', s)
            self.assertEqual(aulas, passos, f'M{m}')

    # 01/11/2026: o <style> dos nove guias é idêntico
    def test_estilo_dos_nove_guias_identico(self):
        estilos = []
        for m in range(1, 10):
            guia = (ROOT / f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
            estilos.append(re.search(r'<style>(.*?)</style>', guia, re.S)[1])
        self.assertEqual(len(estilos), 9)
        self.assertEqual(len(set(estilos)), 1)

    def test_camada_literal_aplicada_e_reversivel(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py',
                            'scripts/tarefas_m356_20261031.json', '--manifesto',
                            # 05/11/2026: a revisão de 5/11 desfaz-se primeiro; as conferências ficam iguais.
                            # 05/11/2026: a tabela dos seis movimentos é a camada mais recente; desfaz-se antes da revisão, com a mesma exigência.
                            # 05/11/2026: o Laboratório do exame (lição, não «leitura de apoio») é a camada mais recente; desfaz-se antes da tabela dos seis movimentos.
                            # 05/11/2026: o contexto de cada sessão do Laboratório do exame (lição e excerto, não «recorte») é a camada mais recente; desfaz-se antes da ligação e das notas do Laboratório do exame.
                            # 05/11/2026: a decisão 154 (os exercícios fazem-se sozinho; nada no texto do aluno depende do docente) é a camada mais recente; desfaz-se antes do contexto do Laboratório do exame, com a mesma exigência.
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
                            'tests/fixtures/tarefas-m356-edits-20261031.json', '--verificar', '--desfazer-antes', 'tests/fixtures/cuidado-m8-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m7-edits-20261111.json', '--desfazer-antes', 'tests/fixtures/cuidado-m6-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cidade-cartaz-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/creditos-i-pt1-edits-20261107.json', '--desfazer-antes', 'tests/fixtures/cuidado-m1-edits-20261106.json', '--desfazer-antes', 'tests/fixtures/indices-acertos-edits-20261107.json', '--desfazer-antes', 'tests/fixtures/cartaz-indices-148-edits-20261106.json', '--desfazer-antes', 'tests/fixtures/creditos-i-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/autonomia-154-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/exame-contexto-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/exame-licao-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/tabela-movimentos-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/revisao-edits-20261105.json', '--desfazer-antes', 'tests/fixtures/cartaz-cabecalho-edits-20261103.json', '--desfazer-antes', 'tests/fixtures/cartaz-m4-piloto-edits-20261102.json', '--desfazer-antes', 'tests/fixtures/variedade-f0-edits-20261102.json', '--desfazer-antes', 'tests/fixtures/creditos-grafismos-ia-edits-20261102.json', '--desfazer-antes', 'tests/fixtures/conteudos-lote2-edits-20261101.json', '--desfazer-antes', 'tests/fixtures/varredura-formatacao-edits-20261101.json', '--desfazer-antes', 'tests/fixtures/calcada-mar-edits-20261102.json', '--desfazer-antes', 'tests/fixtures/tarefas-individuais-edits-20261102.json', '--desfazer-antes', 'tests/fixtures/cartaz-indices-edits-20261101.json',  '--desfazer-antes', 'tests/fixtures/licoes-m16-edits-20261101.json', '--desfazer-antes', 'tests/fixtures/licoes-m89-edits-20261101.json', '--desfazer-antes', 'tests/fixtures/tarefas-m89-edits-20261101.json'], # 01/11/2026: verificar o predecessor por baixo das duas camadas de lições e da camada M8/M9. 02/11/2026: e das tarefas individuais.
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main()
