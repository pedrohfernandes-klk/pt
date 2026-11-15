"""15/11/2026: a fila final, camada fila_final_20261115 (assets/exame/app.js, assets/exame/sessoes.json e m3/licao-m3-f05/index.html).

Confere:
- no Exame, que o alvo de cada sessão é «Meta da sessão» e não limite do exame (a linha da sessão e a versão para imprimir), e que a
  página «Programa e fontes» diz que a Informação-Prova de 2027 ainda não está disponível (os dados continuam com referenceYear 2026);
- nas sessões, que o critério da sessão 20 diz «Cheguei à meta de treino de 80 a 100 palavras.» e não «Respeitei as 80 a 100
  palavras.», que o prompt da sessão 20 diz que é um treino de síntese e não um item do exame, e que o da sessão 23 diz que a extensão é
  a meta da sessão e distingue-a do item I.7 de 2026 (as expressões que scripts/exame_treinos_dados/exposicao.py confere por assert
  ficam);
- na lição M3-F05, que os números 5 e 10 dos versos de «Descalça vai para a fonte» estão no quinto e no décimo verso (e não no rótulo
  «Voltas» nem no oitavo verso);
- que os 20 rótulos «Item N da prova» ficam com espaço normal (o motor e os testes dependem disso);
- que a camada é fechada (só os 3 ficheiros, uma ocorrência por troca, o JSON das trocas igual ao manifesto, o script dá o mesmo JSON),
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

CAMADA_REL = 'scripts/fila_final_20261115.json'
MANIFESTO_REL = 'tests/fixtures/fila-final-edits-20261115.json'
SINTESE_REL = 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'
MAIN = '4f4135bf679176c6c8e4abda543837632aad7325'
APP = 'assets/exame/app.js'
SESSOES = 'assets/exame/sessoes.json'
F05 = 'm3/licao-m3-f05/index.html'
FICHEIROS = [APP, SESSOES, F05]
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
        self.assertIn("minutos. Meta da sessão: '+e(session.writing.target)+'. Não é um limite do exame.</p>", app)
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

    def test_f05_os_numeros_dos_versos(self):
        texto = ler(F05)
        n = lambda l: re.search(r'data-l=\\"0-%d\\"><span class=\\"n\\">(\d*)</span>' % l, texto).group(1)
        # Linha 0: «Mote»; 1 a 3: os três versos do mote; 4: em branco; 5: «Voltas»; 6 a 12: os sete versos da volta.
        self.assertEqual({l: n(l) for l in range(0, 13) if l != 4}, {0: '', 1: '', 2: '', 3: '', 5: '', 6: '', 7: '5', 8: '', 9: '', 10: '',
                                                                      11: '', 12: '10'})
        self.assertIn('data-l=\\"0-7\\"><span class=\\"n\\">5</span>O <b class=\\"gt\\" data-s=\\"tampa\\">testo</b> nas mãos de prata,', texto)
        self.assertIn('data-l=\\"0-12\\"><span class=\\"n\\">10</span>Vai formosa, e não segura.</span>', texto)
        self.assertIn('Traz a <b class=\\"gt\\" data-s=\\"saia de uso diário\\">vasquinha de cote</b>,', texto)

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
        self.assertEqual(len(TROCAS), 10)
        self.assertEqual(MANIFESTO['base_commit'], MAIN)
        for t in TROCAS:
            self.assertEqual(t['ocorrencias'], 1)
            self.assertTrue(t['achado'].startswith('15/11/2026: fila final'))
            for palavra in ('professor', 'jogar', 'jogo', 'ficha', 'folha', '—'):
                self.assertNotIn(palavra, t['novo'].lower())
        for rel in FICHEIROS:
            mine = [(t['antigo'], t['novo']) for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual([(e['old'], e['new']) for e in MANIFESTO['files'][rel]['edits']], mine, rel)
            self.assertTrue(all(e['occurrences'] == 1 for e in MANIFESTO['files'][rel]['edits']))
            self.assertEqual(sha_lf(ler(rel)), MANIFESTO['files'][rel]['after_sha256_lf'], rel)

    def test_reversivel_ate_ao_main_letra_a_letra(self):
        for rel in FICHEIROS:
            texto = ler(rel)
            for e in reversed(MANIFESTO['files'][rel]['edits']):
                self.assertEqual(texto.count(e['new']), e['occurrences'], rel)
                texto = texto.replace(e['new'], e['old'])
            main = subprocess.run(['git', 'show', f'{MAIN}:{rel}'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')
            self.assertEqual(texto, main, rel)
            self.assertEqual(sha_lf(main), MANIFESTO['files'][rel]['base_sha256_lf'], rel)
            self.assertEqual(undo_fila_final_1115(rel, ler(rel)), main, rel)
            self.assertEqual(undo_fila_final_1115(rel, main), main, rel)

    def test_o_script_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('fila_final_20261115', ROOT / 'scripts/fila_final_20261115.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.trocas(), TROCAS)

    def test_aplicar_trocas_verifica_esta_e_a_anterior(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar'],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/sintese_duas_linhas_20261115.json', '--manifesto', SINTESE_REL,
                            '--verificar', '--desfazer-antes', MANIFESTO_REL], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_no_topo_da_pilha(self):
        self.assertEqual(verificar_camadas.LAYERS[0], ('fila_final_20261115', 'fila-final-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('sintese_duas_linhas_20261115', 'sintese-duas-linhas-edits-20261115'))
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
