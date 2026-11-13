"""02/11/2026: F0 acrescenta ajuda e protege a importação, sem alterar os bancos."""
import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from auditoria_20261028 import undo_variedade_f0, undo_cabecalho

ROOT=Path(__file__).resolve().parents[1]


class F0(unittest.TestCase):
    def test_vinte_aquecimentos_mesmos_cartoes_chaves_e_versoes(self):
        data=list((ROOT/'docs/pedagogia/aquecimentos').glob('*.json'))
        self.assertEqual(len(data),20)
        for source in data:
            rel=f'tarefas/{source.stem}/aquecimento/index.html'
            now=(ROOT/rel).read_text('utf-8');before=undo_variedade_f0(rel,now)
            button='<button type="button" class="c-ic" data-c-como aria-label="Como se faz" title="Como se faz" hidden><span class="c-roda">?</span></button>'
            self.assertEqual(now.count(button),1,rel)
            self.assertEqual(now.replace(button,''),before,rel)
            self.assertEqual(re.findall(r'\b(?:chave|versao):[^,}]+',before),re.findall(r'\b(?:chave|versao):[^,}]+',now),rel)

    def test_manifesto_reversivel_e_ambito_exato(self):
        m=json.loads((ROOT/'tests/fixtures/variedade-f0-edits-20261102.json').read_text('utf-8'))
        expected={'index.html'}|{f'tarefas/{p.stem}/aquecimento/index.html' for p in (ROOT/'docs/pedagogia/aquecimentos').glob('*.json')}
        self.assertEqual(set(m['files']),expected)
        self.assertEqual(sum(len(r['edits']) for r in m['files'].values()),24)
        for rel,r in m['files'].items():
            # 03/11/2026: retirar só a ligação visual antes de conferir os mesmos SHA da F0.
            now=undo_cabecalho(rel,(ROOT/rel).read_text('utf-8'))
            self.assertEqual(hashlib.sha256(now.encode()).hexdigest(),r['after_sha256_lf'],rel)
            self.assertEqual(hashlib.sha256(undo_variedade_f0(rel,now).encode()).hexdigest(),r['base_sha256_lf'],rel)

    def test_verificador_confere_a_camada(self):
        # 05/11/2026: a revisão de 5/11 desfaz-se primeiro; as conferências ficam iguais.
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
        # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M9, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», as atividades e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: as duas tarefas do M1 mais fáceis de fazer e «tudo junto» no M1 (tarefas_faceis_m1_20261113: os enunciados, as grelhas e as correções da m1-u1 e da m1-u2, os seus dados, e o guia, o índice e o portefólio do M1) passam a camada mais recente, por cima das tarefas do M3 mais fáceis de fazer; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: as duas tarefas do M5 mais fáceis de fazer e «tudo junto» no M5, com dois acertos do M3 (tarefas_faceis_m5_20261113: os enunciados, as grelhas, as correções e os aquecimentos da m5-u1 e da m5-u2, os seus dados, o guia, o índice, o mapa e o portefólio do M5, o portefólio do M3 e o tema B da m3-u2) passam a camada mais recente, por cima das tarefas do M1 mais fáceis de fazer; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        r=subprocess.run([sys.executable,'scripts/aplicar_trocas.py','scripts/variedade_f0_20261102.json','--manifesto','tests/fixtures/variedade-f0-edits-20261102.json','--verificar','--desfazer-antes','tests/fixtures/tarefas-faceis-m7-edits-20261113.json','--desfazer-antes','tests/fixtures/tarefas-faceis-m6-edits-20261113.json','--desfazer-antes','tests/fixtures/tarefas-faceis-m5-edits-20261113.json','--desfazer-antes','tests/fixtures/tarefas-faceis-m1-edits-20261113.json','--desfazer-antes','tests/fixtures/tarefas-faceis-m3-edits-20261112.json','--desfazer-antes','tests/fixtures/exame-provas-oficial-edits-20261112.json','--desfazer-antes','tests/fixtures/exame-ligacao-treinos-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-exame-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-m9-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-m8-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-m7-edits-20261111.json','--desfazer-antes','tests/fixtures/cuidado-m6-edits-20261108.json','--desfazer-antes','tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes','tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes','tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes','tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes','tests/fixtures/cidade-cartaz-edits-20261108.json', '--desfazer-antes','tests/fixtures/creditos-i-pt1-edits-20261107.json', '--desfazer-antes','tests/fixtures/cuidado-m1-edits-20261106.json', '--desfazer-antes','tests/fixtures/indices-acertos-edits-20261107.json','--desfazer-antes','tests/fixtures/cartaz-indices-148-edits-20261106.json','--desfazer-antes','tests/fixtures/creditos-i-edits-20261105.json','--desfazer-antes','tests/fixtures/atlas-lote3-edits-20261105.json','--desfazer-antes','tests/fixtures/autonomia-154-edits-20261105.json','--desfazer-antes','tests/fixtures/exame-contexto-edits-20261105.json','--desfazer-antes','tests/fixtures/exame-licao-edits-20261105.json','--desfazer-antes','tests/fixtures/tabela-movimentos-edits-20261105.json','--desfazer-antes','tests/fixtures/revisao-edits-20261105.json','--desfazer-antes','tests/fixtures/cartaz-cabecalho-edits-20261103.json'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)


if __name__=='__main__':unittest.main()
