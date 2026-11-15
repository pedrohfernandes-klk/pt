"""15/11/2026: a fila final, camada fila_final_20261115 (assets/exame/app.js, assets/exame/sessoes.json, m3/licao-m3-f05/index.html e, no
fim do dia, o resto da decisão do docente «síntese integrada» → «duas linhas finais»: 14 ficheiros do M1, do M2, do M4, do M7 e do M8).

Confere:
- no Exame, que o alvo de cada sessão é «Meta da sessão: …» (a linha da sessão e a versão para imprimir) sem a frase «Não é um limite do exame.» na origem única (falsa nas sessões 24 e 25), e que a
  página «Programa e fontes» diz que a Informação-Prova de 2027 ainda não está disponível (os dados continuam com referenceYear 2026);
- nas sessões, que o critério da sessão 20 diz «Cheguei à meta de treino de 80 a 100 palavras.» e não «Respeitei as 80 a 100
  palavras.», que o prompt da sessão 20 diz que é um treino de síntese e não um item do exame, e que o da sessão 23 diz que a extensão é
  a meta da sessão e distingue-a do item I.7 de 2026 (as expressões que scripts/exame_treinos_dados/exposicao.py confere por assert
  ficam);
- na lição M3-F05, que os números 5 e 10 dos versos de «Descalça vai para a fonte» estão no quinto e no décimo verso (e não no rótulo
  «Voltas» nem no oitavo verso);
- que nenhuma página do M2 (índice, portefólio, mapa e guia da tarefa) diz «síntese integrada» (15/11/2026, decisão do docente), que as
  peças soltas (todos do M1 e do M7, lição M1-F11, planos das aulas de tarefa do M1 e do M4, portefólios do M4 e do M8) dizem «duas
  linhas finais», e que os outros usos de «síntese» ficam (perguntas de escolha, «síntese oral ou no caderno», chave «synthesis»);
- que os 20 rótulos «Item N da prova» ficam com espaço normal (o motor e os testes dependem disso);
- que a camada é fechada (só os 17 ficheiros, uma ocorrência por troca, o JSON das trocas igual ao manifesto, o script dá o mesmo JSON),
  reversível até ao main de partida letra a letra e está no topo da pilha, por cima de sintese_duas_linhas_20261115;
- que as camadas de baixo a desfazem primeiro (auditoria, desligar_sala, a leitura histórica e a leitura dos scripts que partilham
  ficheiros).

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
from auditoria_20261028 import undo_fila_final_1115  # noqa: E402
# 15/11/2026: por cima desta camada fica a revisão geral (revisao_geral_20261115), que partilha com ela assets/exame/sessoes.json (a
# sessão 27): os testes desta camada leem cada ficheiro como ela o deixou, com a revisão geral desfeita primeiro, com contagem estrita.
from auditoria_20261028 import undo_revisao_geral_1115  # noqa: E402

CAMADA_REL = 'scripts/fila_final_20261115.json'
MANIFESTO_REL = 'tests/fixtures/fila-final-edits-20261115.json'
SINTESE_REL = 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'
REVISAO_REL = 'tests/fixtures/revisao-geral-edits-20261115.json'  # 15/11/2026: a revisão geral, a camada mais recente, por cima desta
MAIN = '4f4135bf679176c6c8e4abda543837632aad7325'
APP = 'assets/exame/app.js'
SESSOES = 'assets/exame/sessoes.json'
F05 = 'm3/licao-m3-f05/index.html'
EXAME = [APP, SESSOES, F05]
# 15/11/2026: o resto da decisão «duas linhas finais» em vez de «síntese integrada» (os 14 ficheiros que a camada sintese_duas_linhas_20261115 não tocou).
M2 = ['m2/index.html', 'm2/portefolio-do-modulo-m2/index.html', 'm2/mapa-do-modulo-m2/index.html', 'm2/guia-da-tarefa-m2/index.html']
TODOS = ['m1/todos/index.html', 'm7/todos/index.html']
AULAS = ['m1/aulas/aula-06/index.html', 'm1/aulas/aula-14/index.html', 'm4/aulas/aula-08/index.html', 'm4/aulas/aula-15/index.html',
         'm4/aulas/aula-18/index.html']
SOLTAS = TODOS + ['m1/licao-m1-f11/index.html'] + AULAS + ['m4/portefolio-do-modulo-m4/index.html', 'm8/portefolio-do-modulo-m8/index.html']
FICHEIROS = EXAME + M2 + SOLTAS
ANTIGAS = ('síntese integrada', 'síntese simples integrada', 'integra a síntese', 'síntese integra', 'Síntese integra',
           'integram a aula de tarefa')
NBSP = ' '
WJ = '⁠'


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


TROCAS = json.loads(ler(CAMADA_REL))
MANIFESTO = json.loads(ler(MANIFESTO_REL))


class FilaFinal(unittest.TestCase):
    def test_exame_o_alvo_e_meta_da_sessao_e_nao_limite_do_exame(self):
        app = ler(APP)
        self.assertIn("minutos. Meta da sessão: '+e(session.writing.target)+'.</p>", app)
        # 15/11/2026: a frase «Não é um limite do exame.» é falsa nas sessões 24 e 25 (200 a 350 palavras é o limite do Grupo III):
        # não está na origem única das 27 sessões; só os prompts das sessões 20 e 23 a dizem.
        self.assertNotIn('Não é um limite do exame', app)
        self.assertIn("<p>Meta da sessão: '+e(s.writing.target)+'.</p>", app)
        self.assertNotIn("minutos · '+e(session.writing.target)", app)
        self.assertNotIn("<p>'+e(s.writing.target)+'</p>", app)

    def test_exame_a_informacao_prova_de_2027_ainda_nao_esta_disponivel(self):
        app = ler(APP)
        self.assertEqual(app.count('indicadas pela DGE. A Informação-Prova de 2027 ainda não está disponível.'), 1)
        self.assertRegex(app, r'Informação-Prova[ \u00a0]639[ \u00a0]de[ \u00a0]2026')
        dados = json.loads(ler(SESSOES))
        self.assertEqual(dados['referenceYear'], 2026)

    def test_sessoes_20_e_23(self):
        dados = json.loads(ler(SESSOES))
        por_id = {s.get('id'): s for s in dados['sessions']}
        w = por_id['s20']['writing']
        self.assertIn('Cheguei à meta de treino de 80' + '–' + WJ + '100' + NBSP + 'palavras.', w['criteria'])
        self.assertFalse([c for c in w['criteria'] if c.startswith('Respeitei as 80')])
        self.assertTrue(w['prompt'].endswith('Não acrescentes opiniões nem exemplos teus. Isto é um treino de síntese, não um item do exame.'))
        p = por_id['s23']['writing']['prompt'].replace(NBSP, ' ')
        self.assertTrue(p.endswith('Define um eixo, explica-o e apoia-o em exemplos pertinentes. A extensão é a meta desta sessão, não uma '
                                   'regra do exame: no exame, a breve exposição do item I.7 não tem limite de palavras e pede uma só obra.'))
        # As expressões que scripts/exame_treinos_dados/exposicao.py confere por assert ficam.
        self.assertIn('texto expositivo de 200 a 350 palavras', p)
        self.assertIn('em duas obras estudadas', p)
        self.assertIn('texto expositivo de 200 a 350 palavras', ler('scripts/exame_treinos_dados/exposicao.py'))
        self.assertIn('em duas obras estudadas', ler('scripts/exame_treinos_dados/exposicao.py'))

    def test_sessoes_24_e_25_nao_dizem_que_o_alvo_nao_e_limite_do_exame(self):
        # 15/11/2026: o alvo de 200 a 350 palavras é o limite real do Grupo III (nas duas fases).
        dados = json.loads(ler(SESSOES))
        por_id = {s.get('id'): s for s in dados['sessions']}
        for sid in ('s24', 's25'):
            w = por_id[sid]['writing']
            self.assertIn('200', w['target'])
            self.assertIn('350', w['target'])
            self.assertNotIn('limite do exame', json.dumps(w, ensure_ascii=False))
        self.assertNotIn('Não é um limite do exame', ler(APP))

    def test_f05_os_numeros_dos_versos(self):
        texto = ler(F05)
        n = lambda l: re.search(r'data-l=\\"0-%d\\"><span class=\\"n\\">(\d*)</span>' % l, texto).group(1)
        # Linha 0: «Mote»; 1 a 3: os três versos do mote; 4: em branco; 5: «Voltas»; 6 a 12: os sete versos da volta.
        self.assertEqual({l: n(l) for l in range(0, 13) if l != 4}, {0: '', 1: '', 2: '', 3: '', 5: '', 6: '', 7: '5', 8: '', 9: '', 10: '',
                                                                      11: '', 12: '10'})
        self.assertIn('data-l=\\"0-7\\"><span class=\\"n\\">5</span>O <b class=\\"gt\\" data-s=\\"tampa\\">testo</b> nas mãos de prata,', texto)
        self.assertIn('data-l=\\"0-12\\"><span class=\\"n\\">10</span>Vai formosa, e não segura.</span>', texto)
        self.assertIn('Traz a <b class=\\"gt\\" data-s=\\"saia de uso diário\\">vasquinha de cote</b>,', texto)

    def test_o_m2_nao_diz_sintese_integrada(self):
        # 15/11/2026: decisão do docente: no M2, como no M1, «síntese integrada» e «síntese simples integrada» passam a «duas linhas finais».
        for rel in M2:
            texto = ler(rel)
            for velho in ANTIGAS:
                self.assertNotIn(velho, texto, f'{rel}: «{velho}»')
            self.assertIn('duas linhas finais', texto, rel)
        indice = ler('m2/index.html')
        self.assertIn('produção em papel, duas linhas finais e fotografias no Teams.', indice)
        self.assertIn('Cada unidade termina na sua aula de tarefa, com as duas linhas finais.', indice)
        self.assertEqual(indice.count('trabalho em papel, duas linhas finais e fotografias no Teams.'), 2)
        portefolio = ler('m2/portefolio-do-modulo-m2/index.html')
        self.assertIn('uma aula de tarefa, que integra as duas linhas finais;', portefolio)
        self.assertIn('Reúne os trabalhos e as duas linhas finais já entregues.', portefolio)
        self.assertEqual(portefolio.count('Recupera as duas linhas finais da aula de tarefa.'), 2)
        self.assertEqual(portefolio.count('As duas linhas finais, no papel da aula de tarefa, fotografadas com o trabalho. Recupera essa entrega, sem escrever outras.'), 2)
        self.assertNotIn('Recupera a síntese', portefolio)
        mapa = ler('m2/mapa-do-modulo-m2/index.html')
        self.assertEqual(mapa.count('min · duas linhas finais</a>'), 2)
        self.assertIn('As duas linhas finais ficam no papel do trabalho:', mapa)
        guia = ler('m2/guia-da-tarefa-m2/index.html')
        self.assertIn('com duas linhas finais; as retomas', guia)
        self.assertIn('escreves duas linhas finais no trabalho', guia)

    def test_pecas_soltas_dizem_duas_linhas_finais(self):
        for rel in TODOS:
            texto = ler(rel)
            self.assertIn('com consulta e duas linhas finais.', texto, rel)
            self.assertNotIn('síntese simples integrada', texto, rel)
        self.assertIn('As duas linhas finais ficam na Tarefa da Unidade 2.', ler('m1/licao-m1-f11/index.html'))
        self.assertNotIn('A síntese integra a Tarefa da Unidade 2.', ler('m1/licao-m1-f11/index.html'))
        for rel in AULAS:
            texto = ler(rel)
            self.assertIn('O fecho e as duas linhas finais fazem parte da aula de tarefa.', texto, rel)
            self.assertNotIn('O fecho e a síntese integram a aula de tarefa.', texto, rel)
        m4 = ler('m4/portefolio-do-modulo-m4/index.html')
        self.assertIn('já fotografadas; não escreves outras.', m4)
        self.assertNotIn('já fotografada; não escreves outra', m4)
        m8 = ler('m8/portefolio-do-modulo-m8/index.html')
        # 15/11/2026: revisão geral antes de publicar: «sem linhas a mais obrigatórias» lia-se mal; fica «sem outra escrita obrigatória».
        self.assertEqual(m8.count('sem outra escrita obrigatória.'), 2)
        self.assertNotIn('sem linhas a mais obrigatórias', m8)
        # 15/11/2026: revisão geral antes de publicar: «sozinho» marca o género de quem lê e sai dos planos das aulas 06 do M1 e 15
        # do M4; a última «síntese» da lição M1-F11 passa a «duas linhas finais», como no resto da lição.
        for rel in ('m1/aulas/aula-06/index.html', 'm4/aulas/aula-15/index.html'):
            self.assertIn('refazer o exercício no telemóvel, sem ajuda, ao teu ritmo', ler(rel), rel)
            self.assertNotIn('sozinho', ler(rel), rel)
        self.assertIn('Serve às duas linhas finais da unidade 2, não a este plano.', ler('m1/licao-m1-f11/index.html'))
        self.assertNotIn('Serve à síntese da unidade 2', ler('m1/licao-m1-f11/index.html'))
        self.assertNotIn('sem síntese adicional obrigatória', m8)

    def test_os_outros_usos_de_sintese_ficam(self):
        # 15/11/2026: ficam as perguntas de escolha das lições, «síntese oral ou no caderno» e a chave interna «synthesis».
        self.assertIn('Qual das sínteses usa os três recortes', ler('m3/index.html'))
        for m in (3, 5, 6):
            self.assertIn('a síntese oral ou no caderno pede duas passagens', ler(f'm{m}/mapa-do-modulo-m{m}/index.html'))
        for m in (1, 2, 3, 5, 6, 7, 8):
            self.assertIn('"synthesis":"integrated"', ler(f'm{m}/index.html'), m)

    def test_item_n_da_prova_fica_com_espaco_normal(self):
        rotulos = 0
        for prova in ('2026-1f', '2026-2f'):
            for grupo in ('grupo-i', 'grupo-ii'):
                texto = ler(f'exame/provas/{prova}/{grupo}/index.html')
                self.assertFalse(re.search(r'Item' + NBSP + r'\d+ da prova', texto), (prova, grupo))
                rotulos += len(re.findall(r'Item \d+ da prova', texto))
        self.assertGreaterEqual(rotulos, 20)

    def test_camada_fechada(self):
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        # 15/11/2026: revisão geral antes de publicar: mais 3 trocas («sozinho» nas aulas 06 do M1 e 15 do M4 e a «síntese» da M1-F11).
        self.assertEqual(len(TROCAS), 38)
        self.assertEqual(sum(1 for t in TROCAS if t['ficheiro'] in EXAME), 10)
        self.assertEqual(MANIFESTO['base_commit'], MAIN)
        for t in TROCAS:
            self.assertEqual(t['ocorrencias'], 1)
            self.assertTrue(t['achado'].startswith(('15/11/2026: fila final', '15/11/2026: Decisão do docente')))
            for velho in ANTIGAS:
                self.assertNotIn(velho, t['novo'])
            for palavra in ('professor', 'jogar', 'jogo', 'ficha', 'folha', '—'):
                self.assertNotIn(palavra, t['novo'].lower())
        for rel in FICHEIROS:
            mine = [(t['antigo'], t['novo']) for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual([(e['old'], e['new']) for e in MANIFESTO['files'][rel]['edits']], mine, rel)
            self.assertTrue(all(e['occurrences'] == 1 for e in MANIFESTO['files'][rel]['edits']))
            # 15/11/2026: com a revisão geral (revisao_geral_20261115) desfeita primeiro: é o ficheiro como esta camada o deixou.
            self.assertEqual(sha_lf(undo_revisao_geral_1115(rel, ler(rel))), MANIFESTO['files'][rel]['after_sha256_lf'], rel)

    def test_reversivel_ate_ao_main_letra_a_letra(self):
        # 15/11/2026: os 3 ficheiros do Exame e da M3-F05 voltam ao main; os 14 da decisão «duas linhas finais» voltam à base do manifesto
        # (as páginas como as deixou o commit anterior, que já trazia as camadas de baixo).
        for rel in FICHEIROS:
            # 15/11/2026: a partir do ficheiro como esta camada o deixou (com a revisão geral, por cima, desfeita primeiro).
            texto = undo_revisao_geral_1115(rel, ler(rel))
            for e in reversed(MANIFESTO['files'][rel]['edits']):
                self.assertEqual(texto.count(e['new']), e['occurrences'], rel)
                texto = texto.replace(e['new'], e['old'])
            main = subprocess.run(['git', 'show', f'{MAIN}:{rel}'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8') if rel in EXAME else None
            if rel in EXAME:
                self.assertEqual(texto, main, rel)
                self.assertEqual(sha_lf(main), MANIFESTO['files'][rel]['base_sha256_lf'], rel)
                self.assertEqual(undo_fila_final_1115(rel, ler(rel)), main, rel)
                self.assertEqual(undo_fila_final_1115(rel, main), main, rel)
            else:
                self.assertEqual(sha_lf(texto), MANIFESTO['files'][rel]['base_sha256_lf'], rel)
                self.assertEqual(undo_fila_final_1115(rel, ler(rel)), texto, rel)
                self.assertEqual(undo_fila_final_1115(rel, texto), texto, rel)
                self.assertTrue(any(v in texto for v in ANTIGAS + ('Síntese de duas linhas', 'síntese adicional', 'já fotografada;')), rel)

    def test_o_script_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('fila_final_20261115', ROOT / 'scripts/fila_final_20261115.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.trocas(), TROCAS)

    def test_aplicar_trocas_verifica_esta_e_a_anterior(self):
        # 15/11/2026: por cima desta camada fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a
        # mesma exigência, sem nada pelo meio.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar',
                            '--desfazer-antes', REVISAO_REL], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/sintese_duas_linhas_20261115.json', '--manifesto', SINTESE_REL,
                            '--verificar', '--desfazer-antes', REVISAO_REL, '--desfazer-antes', MANIFESTO_REL], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_no_topo_da_pilha(self):
        # 15/11/2026: por cima desta camada fica a revisão geral (revisao_geral_20261115), a camada mais recente: esta passa à segunda
        # posição, logo por baixo dela, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('revisao_geral_20261115', 'revisao-geral-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('fila_final_20261115', 'fila-final-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('sintese_duas_linhas_20261115', 'sintese-duas-linhas-edits-20261115'))
        self.assertEqual(len(set(verificar_camadas.LAYERS)), len(verificar_camadas.LAYERS))

    def test_as_camadas_de_baixo_a_desfazem_primeiro(self):
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertRegex(auditoria, r'def undo_sintese_duas_linhas_1115\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_fila_final_1115\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('fila-final-edits-20261115.json'), sala.index('sintese-duas-linhas-edits-20261115.json'))
        historico = ler('scripts/tarefas_claras_historico.py')
        self.assertLess(historico.index('por_cima = FILA_FINAL.get(rel)'), historico.index('por_cima = SINTESE_DUAS_LINHAS.get(rel)'))
        for nome in ('cuidado_exame_20261112', 'cidade_cartaz_20261108'):
            self.assertIn('fila-final-edits-20261115.json', ler(f'scripts/{nome}.py'), nome)
        # 15/11/2026: e as que partilham o M2, o M4 ou o M8 com o resto da decisão «duas linhas finais» (as tarefas mais fáceis de fazer,
        # a tarefa m4-u2, o índice da decisão 148 e a própria camada das duas linhas finais).
        for nome in ('tarefas_faceis_m1_20261113', 'tarefas_faceis_m3_20261112', 'tarefas_faceis_m5_20261113', 'tarefas_faceis_m6_20261113',
                     'tarefas_faceis_m7_20261113', 'tarefas_faceis_m8_20261113', 'tarefas_faceis_m9_20261114', 'tarefa_m4u2_tema_b_20261115',
                     'cartaz_indices_148_20261106', 'sintese_duas_linhas_20261115'):
            self.assertIn('fila-final-edits-20261115.json', ler(f'scripts/{nome}.py'), nome)
        # Nas cadeias de --desfazer-antes dos testes e dos fluxos, esta camada vem logo antes das duas linhas finais, sem nada pelo meio.
        cadeia = re.compile(r'--desfazer-antes[ \',]+tests/fixtures/sintese-duas-linhas-edits-20261115\.json')
        junta = re.compile(r'--desfazer-antes[ \',]+tests/fixtures/fila-final-edits-20261115\.json[ \',]+'
                           r'--desfazer-antes[ \',]+tests/fixtures/sintese-duas-linhas-edits-20261115\.json')
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_fila_final_20261115.py':
                continue
            texto = p.read_text('utf-8')
            self.assertEqual(len(cadeia.findall(texto)), len(junta.findall(texto)), p.name)


if __name__ == '__main__':
    unittest.main()
