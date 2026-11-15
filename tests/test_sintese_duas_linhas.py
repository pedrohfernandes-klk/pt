"""15/11/2026: «duas linhas finais» em vez de «síntese integrada» (decisão do docente) nos índices, nos portefólios, nos mapas e no
guia da tarefa do M1, do M3, do M5, do M6, do M7 e do M8, na camada sintese_duas_linhas_20261115.

Confere:
- que nenhuma página do âmbito (os índices, os portefólios, os mapas e os guias da tarefa do M1, do M3, do M4, do M5, do M6, do M7 e
  do M8) diz «síntese integrada», «síntese simples integrada», «integra a síntese» nem «A síntese integra»;
- que as páginas mudadas dizem «duas linhas finais» e que os outros usos de «síntese» ficam (as perguntas de escolha das lições,
  «a síntese oral ou no caderno» do desafio, a chave interna «synthesis» do JSON das unidades);
- que a camada é fechada (só os 18 ficheiros, uma ocorrência por troca, o JSON das trocas igual ao manifesto, o script dá o mesmo
  JSON), reversível até ao main de partida letra a letra e está no topo da pilha, por cima de tarefa_m4u2_tema_b_20261115;
- que as camadas de baixo a desfazem primeiro (auditoria, desligar_sala, a leitura histórica e as leituras dos scripts das camadas).

A reversão até ao main lê o commit de partida com git: o fluxo que corre este teste faz o checkout com fetch-depth: 0.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
import verificar_camadas  # noqa: E402
from auditoria_20261028 import undo_fila_final_1115, undo_sintese_duas_linhas_1115  # noqa: E402

CAMADA_REL = 'scripts/sintese_duas_linhas_20261115.json'
MANIFESTO_REL = 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'
FILA_REL = 'tests/fixtures/fila-final-edits-20261115.json'
M4U2_REL = 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json'
MAIN = '4f4135bf679176c6c8e4abda543837632aad7325'

INDICES = [f'm{m}/index.html' for m in (1, 3, 5, 6, 7, 8)]
PORTEFOLIOS = [f'm{m}/portefolio-do-modulo-m{m}/index.html' for m in (1, 3, 5, 6, 7, 8)]
MAPAS = [f'm{m}/mapa-do-modulo-m{m}/index.html' for m in (1, 3, 5, 6, 7)]
GUIAS = ['m1/guia-da-tarefa-m1/index.html']
FICHEIROS = INDICES + PORTEFOLIOS + MAPAS + GUIAS
# As páginas do âmbito: as quatro de cada módulo da decisão, e as do M4, que a camada anterior já mudou.
# 15/11/2026: o M2 também (a fila final, fila_final_20261115, fez o resto da decisão do docente: o M2 passa a dizer «duas linhas finais»
# nos quatro ficheiros do âmbito); nenhuma página do M2 diz «síntese integrada».
AMBITO = [f'm{m}/{p}' for m in (1, 2, 3, 4, 5, 6, 7, 8)
          for p in ('index.html', f'portefolio-do-modulo-m{m}/index.html', f'mapa-do-modulo-m{m}/index.html',
                    f'guia-da-tarefa-m{m}/index.html')]
ANTIGAS = ('síntese integrada', 'síntese simples integrada', 'integra a síntese', 'síntese integra', 'Síntese integra')


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def ler_sem_fila(rel):
    # 15/11/2026: a fila final fica por cima desta camada (partilham o portefólio do M8): a página desta camada é a da árvore com ela desfeita.
    return undo_fila_final_1115(rel, ler(rel))


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


TROCAS = json.loads(ler(CAMADA_REL))
MANIFESTO = json.loads(ler(MANIFESTO_REL))


class SinteseDuasLinhas(unittest.TestCase):
    def test_nenhuma_pagina_do_ambito_diz_sintese_integrada(self):
        for rel in AMBITO:
            texto = ler(rel)
            for velho in ANTIGAS:
                self.assertNotIn(velho, texto, f'{rel}: «{velho}»')

    def test_as_paginas_mudadas_dizem_duas_linhas_finais(self):
        for rel in FICHEIROS:
            self.assertIn('duas linhas finais', ler(rel), rel)
        for m in (1, 7):
            self.assertIn('Cada unidade termina na sua aula de tarefa, com as duas linhas finais.', ler(f'm{m}/index.html'))
            self.assertIn('produção em papel, duas linhas finais e fotografias no Teams.', ler(f'm{m}/index.html'))
            for rel in (f'm{m}/portefolio-do-modulo-m{m}/index.html', f'm{m}/mapa-do-modulo-m{m}/index.html'):
                self.assertIn('uma aula de tarefa, que integra as duas linhas finais;', ler(rel))
            portefolio = ler(f'm{m}/portefolio-do-modulo-m{m}/index.html')
            self.assertIn('Reúne os trabalhos e as duas linhas finais já entregues.', portefolio)
            self.assertIn('Recupera as duas linhas finais da aula de tarefa.', portefolio)
            self.assertNotIn('Recupera a síntese', portefolio)
            self.assertNotIn('outra síntese', portefolio)
            self.assertIn('As duas linhas finais ficam no papel do trabalho:', ler(f'm{m}/mapa-do-modulo-m{m}/index.html'))
            self.assertEqual(ler(f'm{m}/mapa-do-modulo-m{m}/index.html').count('min · duas linhas finais</a>'), 2 if m == 1 else 3)
        for m in (3, 5, 6, 8):
            self.assertIn('As duas linhas finais fazem parte da produção.', ler(f'm{m}/index.html'))
        for m in (3, 5, 6):
            self.assertIn('/20 e duas linhas finais.</p>', ler(f'm{m}/portefolio-do-modulo-m{m}/index.html'))
            mapa = ler(f'm{m}/mapa-do-modulo-m{m}/index.html')
            for u in (1, 2):
                self.assertIn(f'Aula de tarefa da unidade {u}, com duas linhas finais</a>', mapa)
        m7 = ler('m7/portefolio-do-modulo-m7/index.html')
        self.assertIn('Recuperas as duas linhas finais da aula de tarefa, já fotografadas; não escreves outras.', m7)
        self.assertIn('As fotografias do trabalho e das duas linhas finais, ou a ligação', m7)
        self.assertNotIn('da síntese', m7)
        self.assertEqual(ler('m8/portefolio-do-modulo-m8/index.html').count('As duas linhas finais ficam na tarefa da unidade.'), 2)
        self.assertIn('escreves duas linhas finais no trabalho', ler('m1/guia-da-tarefa-m1/index.html'))

    def test_os_outros_usos_de_sintese_ficam(self):
        # As perguntas de escolha das lições, «a síntese oral ou no caderno» do desafio e a chave interna do JSON das unidades.
        self.assertIn('Qual das sínteses usa os três recortes', ler('m3/index.html'))
        for m in (3, 5, 6):
            self.assertEqual(ler(f'm{m}/portefolio-do-modulo-m{m}/index.html').count('Síntese oral ou no caderno, com duas passagens'), 2)
            self.assertIn('a síntese oral ou no caderno pede duas passagens', ler(f'm{m}/mapa-do-modulo-m{m}/index.html'))
        for rel in INDICES:
            self.assertIn('"synthesis":"integrated"', ler(rel), rel)
        # 15/11/2026: «sem síntese adicional obrigatória» (portefólio do M8) passou a «sem linhas a mais obrigatórias» na fila final, que está por cima.
        self.assertEqual(ler_sem_fila('m8/portefolio-do-modulo-m8/index.html').count('sem síntese adicional obrigatória.'), 2)
        self.assertEqual(ler('m8/portefolio-do-modulo-m8/index.html').count('sem linhas a mais obrigatórias.'), 2)

    def test_camada_fechada(self):
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(MANIFESTO['base_commit'], MAIN)
        for t in TROCAS:
            self.assertEqual(t['ocorrencias'], 1)
            self.assertTrue(t['achado'].startswith('15/11/2026: Decisão do docente'))
            for velho in ANTIGAS:
                self.assertNotIn(velho, t['novo'])
            for palavra in ('professor', 'jogar', 'jogo', 'ficha', 'folha', '—'):
                self.assertNotIn(palavra, t['novo'].lower())
        for rel in FICHEIROS:
            mine = [(t['antigo'], t['novo']) for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual([(e['old'], e['new']) for e in MANIFESTO['files'][rel]['edits']], mine, rel)
            self.assertTrue(all(e['occurrences'] == 1 for e in MANIFESTO['files'][rel]['edits']))
            self.assertEqual(sha_lf(ler_sem_fila(rel)), MANIFESTO['files'][rel]['after_sha256_lf'], rel)

    def test_reversivel_ate_ao_main_letra_a_letra(self):
        for rel in FICHEIROS:
            texto = ler_sem_fila(rel)
            for e in reversed(MANIFESTO['files'][rel]['edits']):
                self.assertEqual(texto.count(e['new']), e['occurrences'], rel)
                texto = texto.replace(e['new'], e['old'])
            main = subprocess.run(['git', 'show', f'{MAIN}:{rel}'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')
            self.assertEqual(texto, main, rel)
            self.assertEqual(sha_lf(main), MANIFESTO['files'][rel]['base_sha256_lf'], rel)
            self.assertEqual(undo_sintese_duas_linhas_1115(rel, ler(rel)), main, rel)  # desfaz a fila final primeiro
            self.assertEqual(undo_sintese_duas_linhas_1115(rel, main), main, rel)
            for velho in ('síntese integrada', 'integra a síntese', 'síntese integra', 'Síntese de duas linhas', 'Recupera a síntese',
                          'síntese de duas linhas', 'as sínteses já'):
                if velho in main:
                    break
            else:
                self.fail(f'{rel}: o main não dizia nenhuma das frases antigas')

    def test_o_script_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('sintese_duas_linhas_20261115', ROOT / 'scripts/sintese_duas_linhas_20261115.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        todas, _ = modulo.construir()
        self.assertEqual(todas, TROCAS)

    def test_aplicar_trocas_verifica_esta_e_a_anterior(self):
        # 15/11/2026: a fila final fica por cima (partilha o portefólio do M8 e o do M4): desfaz-se primeiro, nas duas verificações.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar',
                            '--desfazer-antes', FILA_REL], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/tarefa_m4u2_tema_b_20261115.json', '--manifesto', M4U2_REL,
                            '--verificar', '--desfazer-antes', FILA_REL, '--desfazer-antes', MANIFESTO_REL], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_no_topo_da_pilha(self):
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertEqual(verificar_camadas.LAYERS[0], ('fila_final_20261115', 'fila-final-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('sintese_duas_linhas_20261115', 'sintese-duas-linhas-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefa_m4u2_tema_b_20261115', 'tarefa-m4u2-tema-b-edits-20261115'))
        self.assertEqual(len(set(verificar_camadas.LAYERS)), len(verificar_camadas.LAYERS))

    def test_as_camadas_de_baixo_a_desfazem_primeiro(self):
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertRegex(auditoria, r'def undo_tarefa_m4u2_1115\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_sintese_duas_linhas_1115\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('sintese-duas-linhas-edits-20261115.json'), sala.index('tarefa-m4u2-tema-b-edits-20261115.json'))
        historico = ler('scripts/tarefas_claras_historico.py')
        self.assertLess(historico.index('por_cima = SINTESE_DUAS_LINHAS.get(rel)'), historico.index('por_cima = TAREFA_M4U2.get(rel)'))
        for nome in ('tarefas_faceis_m1_20261113', 'tarefas_faceis_m3_20261112', 'tarefas_faceis_m5_20261113', 'tarefas_faceis_m6_20261113',
                     'tarefas_faceis_m7_20261113', 'tarefas_faceis_m8_20261113', 'tarefas_faceis_m9_20261114', 'tarefa_m4u2_tema_b_20261115',
                     'cartaz_indices_148_20261106'):
            leitura = ler(f'scripts/{nome}.py')
            self.assertIn('sintese-duas-linhas-edits-20261115.json', leitura, nome)
        # Nas cadeias de --desfazer-antes dos testes e dos fluxos, esta camada vem logo antes da tarefa m4-u2, sem nada pelo meio.
        cadeia = re.compile(r'--desfazer-antes[ \',]+tests/fixtures/tarefa-m4u2-tema-b-edits-20261115\.json')
        junta = re.compile(r'--desfazer-antes[ \',]+tests/fixtures/sintese-duas-linhas-edits-20261115\.json[ \',]+'
                           r'--desfazer-antes[ \',]+tests/fixtures/tarefa-m4u2-tema-b-edits-20261115\.json')
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            texto = p.read_text('utf-8')
            self.assertEqual(len(cadeia.findall(texto)), len(junta.findall(texto)), p.name)


if __name__ == '__main__':
    unittest.main()
