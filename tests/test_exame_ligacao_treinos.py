"""12/11/2026: a ligação «Treinos» na navegação da página principal do Exame (exame/index.html).

A camada exame_ligacao_treinos_20261112 (scripts/exame_ligacao_treinos_20261112.py e .json; manifesto em
tests/fixtures/exame-ligacao-treinos-edits-20261112.json) fica por cima da decisão 152 no Exame e nas páginas transversais
(cuidado_exame_20261112). Confere-se aqui:
- a camada: fechada, com uma só troca num só ficheiro, aplicada, e que se desfaz letra a letra;
- só a ligação muda: a página é a base mais a ligação, e nada mais (nem a versão de cache de assets/exame/app.js, que
  tests/test_exame_licao.py fixa);
- a ligação resolve para uma página que existe (exame/treinos/index.html), que por sua vez volta à página principal do Exame;
- a ligação é igual à dos cabeçalhos de exame/provas/ e de exame/laboratorio/: o mesmo rótulo, o mesmo destino, sem classe nem
  atributos próprios, e na mesma ordem (logo a seguir a «Provas em cartões»);
- os registos (scripts/verificar_camadas.py, tests/auditoria_20261028.py, scripts/desligar_sala.py), as cadeias dos outros testes
  e dos fluxos (esta camada desfaz-se primeiro, sem nada pelo meio) e os caminhos dos fluxos que a conferem.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
import exame_ligacao_treinos_20261112 as L  # noqa: E402
import verificar_camadas  # noqa: E402
from auditoria_20261028 import undo_exame_ligacao_treinos_1112, undo_cuidado_exame_1112  # noqa: E402

CAMADA_REL = 'scripts/exame_ligacao_treinos_20261112.json'
MANIFESTO_REL = 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
EX = 'tests/fixtures/cuidado-exame-edits-20261112.json'
# 12/11/2026: o manifesto da camada que ficou por cima desta (as provas em cartões com os documentos oficiais).
PO = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
# 12/11/2026: o manifesto da camada que fica por cima dela (as duas tarefas do M3 mais fáceis de fazer).
TF = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
# 13/11/2026: por cima das tarefas do M3 ficam as tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
# 13/11/2026: por cima das tarefas do M1 ficam as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
# 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
T6 = 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'
T7 = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'  # 13/11/2026: a camada das tarefas do M7 mais fáceis de fazer, a mais recente
T5 = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
T1 = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
BASE_COMMIT = '927bab632a0aefb1d3cb090d655a0f4356e3f9f8'
PAGINA = 'exame/index.html'
LIGACAO = '<a href="treinos/">Treinos</a>'
# A navegação da página principal do Exame, por ordem: (destino, rótulo).
NAVEGACAO = [('#inicio', 'Sessões'), ('laboratorio/', 'Laboratório de respostas'), ('provas/', 'Provas em cartões'), ('treinos/', 'Treinos'),
             ('#cobertura', 'Programa e fontes'), ('#dossie', 'Dossiê')]
# Os cabeçalhos que já tinham a ligação (os treinos são de 11/11/2026).
MODELOS = ('exame/provas/index.html', 'exame/laboratorio/index.html')


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def navegacao(rel):
    """As ligações da navegação do cabeçalho de uma página do Exame: [(a etiqueta de abertura, o destino, o rótulo)]."""
    cabeca = re.search(r'<header class="site-head[^"]*">.*?</header>', ler(rel), re.S).group(0)
    (nav,) = re.findall(r'<nav aria-label="[^"]*">(.*?)</nav>', cabeca, re.S)
    return [(m.group(1), m.group(2), m.group(3)) for m in re.finditer(r'(<a href="([^"]*)"[^>]*>)(.*?)</a>', nav, re.S)]


TROCAS = json.loads(ler(CAMADA_REL))
MANIFESTO = json.loads(ler(MANIFESTO_REL))


class ExameLigacaoTreinos(unittest.TestCase):
    def test_camada_fechada_aplicada_e_reversivel_letra_a_letra(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('1 trocas em 1 ficheiros: 1 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        self.assertEqual(len(TROCAS), 1)
        (t,) = TROCAS
        self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        self.assertEqual((t['ficheiro'], t['ocorrencias']), (PAGINA, 1))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('12/11/2026: a ligação «Treinos» na navegação da página principal do Exame'))
        self.assertIn('exame_ligacao_treinos_20261112', m['_nota'])
        self.assertEqual(list(m['files']), [PAGINA])
        registo = m['files'][PAGINA]
        self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
        self.assertEqual(registo['edits'], [{'location': t['local'], 'old': t['antigo'], 'new': t['novo'], 'occurrences': 1}])
        atual = ler(PAGINA)
        self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
        # Desfaz-se letra a letra: a base é a página do commit da base (o resumo é o desse ficheiro em 927bab63).
        b = undo_exame_ligacao_treinos_1112(PAGINA, atual)
        self.assertEqual(sha_lf(b), registo['base_sha256_lf'])
        self.assertEqual(registo['base_sha256_lf'], '7d48a0f9625320abd5eeb4712c4fd7615d3b79a43c87c8f8602b593bded69c28')
        self.assertEqual(b, atual.replace(t['novo'], t['antigo']))
        self.assertNotIn('treinos', b.lower())
        # Ida e volta: refazer a troca sobre a base devolve a página, letra a letra; o antigo não cabe dentro do novo.
        self.assertEqual(b.count(t['antigo']), 1)
        self.assertEqual(b.replace(t['antigo'], t['novo']), atual)
        self.assertEqual(atual.count(t['novo']), 1)
        self.assertEqual(atual.count(t['antigo']), 0)
        self.assertNotIn(t['antigo'], t['novo'])
        # A camada de baixo (a decisão 152 no Exame e nas páginas transversais) não toca nesta página e desfaz primeiro esta.
        self.assertNotIn(PAGINA, json.loads(ler(EX))['files'])
        self.assertEqual(undo_cuidado_exame_1112(PAGINA, atual), b)
        # As duas camadas de baixo que mexem nesta página continuam a conferir, com as de cima desfeitas (esta primeiro).
        for camada, manifesto in (('exame_contexto_20261105', 'exame-contexto-edits-20261105'), ('exame_licao_20261105', 'exame-licao-edits-20261105')):
            with self.subTest(camada=camada):
                self.assertIn(PAGINA, json.loads(ler(f'tests/fixtures/{manifesto}.json'))['files'])
                i = verificar_camadas.LAYERS.index((camada, manifesto))
                comando = [sys.executable, 'scripts/aplicar_trocas.py', f'scripts/{camada}.json', '--manifesto', f'tests/fixtures/{manifesto}.json',
                           '--verificar']
                for _, acima in verificar_camadas.LAYERS[:i]:
                    comando += ['--desfazer-antes', f'tests/fixtures/{acima}.json']
                r = subprocess.run(comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertIn('0 por aplicar; manifesto em dia.', r.stdout)

    def test_so_a_ligacao_muda(self):
        atual = ler(PAGINA)
        b = undo_exame_ligacao_treinos_1112(PAGINA, atual)
        # A página é a base com a ligação posta num só sítio: tirá-la devolve a base, letra a letra.
        self.assertEqual(atual.count(LIGACAO), 1)
        self.assertEqual(atual.replace(LIGACAO, ''), b)
        self.assertEqual(len(atual) - len(b), len(LIGACAO))
        (t,) = TROCAS
        self.assertEqual(t['novo'].replace(LIGACAO, ''), t['antigo'])
        # O único texto novo que se lê é o rótulo.
        visivel = lambda h: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))  # noqa: E731
        self.assertEqual(visivel(atual).replace('Provas em cartões Treinos Programa e fontes', 'Provas em cartões Programa e fontes'), visivel(b))
        # A navegação fica com as mesmas ligações de antes, pela mesma ordem, mais a nova.
        self.assertEqual([(d, r) for _, d, r in navegacao(PAGINA)], NAVEGACAO)
        # assets/exame/app.js não monta o cabeçalho nem fala dos treinos; a sua versão de cache fica a que tests/test_exame_licao.py fixa.
        app = ler('assets/exame/app.js')
        self.assertNotIn('treinos', app.lower())
        self.assertNotIn('site-head', app)
        self.assertEqual(re.findall(r'app\.js\?v=([^"]+)"', atual), ['20261105-licao-2'])
        self.assertEqual(re.findall(r'app\.js\?v=([^"]+)"', b), ['20261105-licao-2'])
        # Nada de palavras proibidas nem de sinais proibidos no que a camada escreve.
        for texto in (t['local'], t['achado'], t['novo'], MANIFESTO['_nota']):
            self.assertNotRegex(texto, r'—|·|(?i:\bprofessor|\bjog[oa]|\bfichas?\b|\bfolhas?\b)')

    def test_a_ligacao_resolve_para_uma_pagina_que_existe(self):
        (abertura, destino, rotulo), = [x for x in navegacao(PAGINA) if x[2] == 'Treinos']
        self.assertEqual(destino, 'treinos/')
        alvo = (ROOT / PAGINA).parent / destino / 'index.html'
        self.assertTrue(alvo.is_file(), alvo)
        self.assertEqual(alvo.resolve(), (ROOT / 'exame/treinos/index.html').resolve())
        # A entrada dos treinos é a do gerador (scripts/exame_treinos.py), apresenta-se como «Treinos» e volta à página do Exame.
        treinos = alvo.read_text('utf-8')
        self.assertIn('<span aria-current="page">Treinos</span>', treinos)
        self.assertIn('<a href="./" aria-current="page">Treinos</a>', treinos)
        self.assertIn('<a href="../">', treinos)

    def test_igual_a_dos_outros_cabecalhos(self):
        minha = navegacao(PAGINA)
        (abertura, destino, rotulo), = [x for x in minha if 'treinos' in x[1]]
        # Sem classe nem atributos: o aspeto é o das outras ligações da mesma navegação.
        self.assertEqual(abertura, '<a href="treinos/">')
        i = minha.index((abertura, destino, rotulo))
        self.assertEqual(minha[i - 1][2], 'Provas em cartões')
        self.assertEqual(minha[i - 1][0], '<a href="provas/">')
        for rel in MODELOS:
            with self.subTest(modelo=rel):
                outra = navegacao(rel)
                (a2, d2, r2), = [x for x in outra if 'treinos' in x[1]]
                # O mesmo rótulo, letra a letra, e a mesma etiqueta, só com o caminho relativo da página.
                self.assertEqual(r2, rotulo)
                self.assertEqual(a2, '<a href="../treinos/">')
                self.assertEqual(((ROOT / rel).parent / d2).resolve(), ((ROOT / PAGINA).parent / destino).resolve())
                # A mesma ordem: logo a seguir a «Provas em cartões».
                k = outra.index((a2, d2, r2))
                self.assertEqual(outra[k - 1][2], 'Provas em cartões')
                # E, nas ligações que as duas navegações têm em comum, a ordem relativa é a mesma.
                comuns = [r for _, _, r in outra if r in {x[2] for x in minha}]
                self.assertEqual(comuns, [r for _, _, r in minha if r in comuns])
        self.assertIn('.site-head nav{flex-wrap:wrap;row-gap:0}', ler('assets/exame/exame.css'))

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        # No topo das camadas, por cima da decisão 152 no Exame e nas páginas transversais.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima das provas em cartões com os documentos oficiais ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M3 mais fáceis de fazer ficam as duas tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 mais fáceis de fazer ficam as duas tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        # 12/11/2026: com as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112), as camadas passam a ser mais uma.
        # 12/11/2026: com as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112) no topo, as camadas passam de 46 a 47, todas diferentes.
        # 13/11/2026: com a camada das tarefas do M1 mais fáceis de fazer, são 48.
        # 13/11/2026: mais uma camada, as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): 49 em vez de 48.
        # 13/11/2026: mais uma camada, a das tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): 50.
        # 13/11/2026: mais uma camada, a das tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113): 51.
        self.assertEqual(len(verificar_camadas.LAYERS), 51)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 51)
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('exame-ligacao-treinos-edits-20261112.json'), sala.index('cuidado-exame-edits-20261112.json'))
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_exame_ligacao_treinos_1112(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_cuidado_exame_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_exame_ligacao_treinos_1112\(path, text\)\n')
        # As camadas de baixo que mexem na mesma página não têm gerador (só o JSON): não há gerador a desfazer esta camada.
        for camada in ('exame_licao_20261105', 'exame_contexto_20261105'):
            self.assertFalse((ROOT / f'scripts/{camada}.py').exists(), camada)
        # Nos fluxos e nos outros testes, a cadeia de desfazer começa por esta camada, sem nada entre ela e a do Exame.
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_exame_ligacao_treinos.py':
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + EX), plano.count(f'--desfazer-antes {meu} --desfazer-antes {EX}'))
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes {ex}'), plano.count('--desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex}'))
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes {EX}'), plano.count('--desfazer-antes {T7} --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {LT} --desfazer-antes {EX}'))
                # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça (os testes que conferem as cadeias com frases
                # partidas em várias linhas ficam de fora desta conta, como nos testes das outras camadas).
                # 12/11/2026: por cima desta camada ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112),
                # que não tocam em exame/index.html: a cabeça da cadeia passa a ser essa camada e esta vem logo a seguir, sem nada pelo
                # meio (nos fluxos e, agora também, nos testes).
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--desfazer-antes {T7} --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {meu}'))
                if p.suffix == '.yml':
                    # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--verificar --desfazer-antes {T7} --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {meu}'))
                cadeias += plano.count(f'--desfazer-antes {meu} --desfazer-antes {EX}')
        self.assertGreater(cadeias, 40)
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        exame = ler('.github/workflows/pt-exame-laboratorio-qa.yml')
        # 12/11/2026: esta camada já não é a mais recente: confere-se com a de cima (as provas em cartões com os documentos oficiais)
        # desfeita primeiro, com a mesma exigência.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        proprio = f'python scripts/aplicar_trocas.py scripts/exame_ligacao_treinos_20261112.json --manifesto {meu} --verificar --desfazer-antes {T7} --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO}\n'
        self.assertIn(proprio, tarefas)
        self.assertIn(proprio, exame)
        # 12/11/2026: e a decisão 152 no Exame confere-se com as duas de cima desfeitas, a mais recente primeiro.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_exame_20261112.json --manifesto {EX} --verificar --desfazer-antes {T7} --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {meu}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_exame_ligacao_treinos.py' -v", tarefas)
        # No fluxo do Exame, o teste corre com os outros do exame e o teste de navegador a seguir ao da hierarquia.
        self.assertIn("python -m unittest discover -s tests -p 'test_exame*.py' -v", exame)
        self.assertIn('          python tests/browser_exame_ligacao_treinos.py\n', exame)
        self.assertLess(exame.index('python tests/browser_exame_hierarquia.py'), exame.index('python tests/browser_exame_ligacao_treinos.py'))
        self.assertTrue((ROOT / 'tests/browser_exame_ligacao_treinos.py').is_file())
        # Os fluxos que conferem ou desfazem esta camada arrancam quando ela muda: o script, o JSON e o manifesto nos caminhos dos
        # quatro fluxos (no do cartaz, nos dois blocos e com a linha datada no cabeçalho).
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/exame_ligacao_treinos_20261112.*', meu):
                self.assertIn(f"'{caminho}'", texto, nome)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        blocos = re.findall(r'^    paths: (\[.*\])$', cartaz, re.M)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0], blocos[1])
        for caminho in ('scripts/exame_ligacao_treinos_20261112.*', meu):
            self.assertIn(f"'{caminho}'", blocos[0])
        self.assertRegex(cartaz.split('\non:')[0], r'\n# 12/11/2026: a ligação «Treinos» na página principal do Exame, a camada exame_ligacao_treinos_20261112 ')

        # Nos fluxos que correm o teste desta camada, a página que ela muda, o script, o JSON, o manifesto e os testes estão nos
        # caminhos do pedido (conferido com os padrões do fluxo, um a um).
        def padrao(glob):
            partes = re.split(r'(\*\*|\*|\[[^\]]+\])', glob)
            return re.compile(''.join('.*' if x == '**' else '[^/]*' if x == '*' else x if x.startswith('[') else re.escape(x)
                                      for x in partes) + '$')
        da_camada = [PAGINA, 'scripts/exame_ligacao_treinos_20261112.py', CAMADA_REL, meu, 'tests/test_exame_ligacao_treinos.py',
                     'tests/browser_exame_ligacao_treinos.py']
        for texto in (tarefas, exame):
            cabeca = texto[texto.index('  pull_request:\n    paths:\n'):texto.index('\npermissions:')]
            padroes = [padrao(g) for g in re.findall(r"^      - '([^']+)'$", cabeca, re.M)]
            self.assertGreater(len(padroes), 50)
            for rel in da_camada:
                self.assertTrue(any(q.match(rel) for q in padroes), rel)

    def test_gerador_da_o_mesmo_json(self):
        trocas, b, final = L.construir()
        self.assertEqual(trocas, TROCAS)
        self.assertEqual(final, ler(PAGINA))
        self.assertEqual(sha_lf(b), MANIFESTO['files'][PAGINA]['base_sha256_lf'])
        self.assertEqual(ler(CAMADA_REL), json.dumps(trocas, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    unittest.main()
