"""28/10/2026: a Sala de aula em tempo real está desligada nas páginas publicadas.

Decisão do docente de 17/10/2026: a Sala enviava a alcunha, a lição e os pontos de cada aluno para tópicos
públicos do ntfy.sh. Aqui confere-se, sem navegador, que:
- nenhum ficheiro publicado (html, js) fala com o ntfy.sh nem abre os canais da Sala (EventSource,
  BroadcastChannel, window.EPISala), e não há botão nem formulário «Sala»;
- onde a Sala existia (as páginas listadas no manifesto) corre a limpeza única do que ela deixou no aparelho;
- os painéis do docente continuam a servir a aula no projetor (pedido, cronómetro, QR, pausa e relâmpago),
  sem placar, sem código de sala e sem gravar nada; 28/10/2026 (revisão): como já não há telemóveis do outro
  lado, o relâmpago mostra no projetor o material do cartão da lição, sem a solução, e a correção no fim do
  tempo; o «Quem sou eu?» dá uma pista por cada terço do tempo; «Voltar ao início» (I) e a tecla A funcionam;
- o manifesto literal desfaz-se e refaz-se, e scripts/desligar_sala.py já não tem nada por fazer.
O comportamento no navegador (sem pedidos para fora, limpeza a correr) está em tests/browser_sala_desligada.py.
"""
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
import unittest

from auditoria_20261028 import undo_sala

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('desligar_sala', ROOT / 'scripts/desligar_sala.py')
D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D)
MANIFESTO = json.loads((ROOT / 'tests/fixtures/sala-desligada-edits-20261028.json').read_text('utf-8'))
PAGINAS = MANIFESTO['paginas']
TODAS = sorted(p for lista in PAGINAS.values() for p in lista)


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def publicados():
    for rel, p in D.publicados():
        yield rel, p.read_bytes().decode('utf-8')


def texto_visivel(html):
    return re.sub(r'<[^>]+>', ' ', html)


def banco(texto, marca):
    i = texto.index(marca) + len(marca)
    return json.JSONDecoder().raw_decode(texto, i)[0]


def codigo_do_painel(texto):
    """O painel sem os dados das lições (CARTOES, MATERIAL e ATL), que citam os textos e podem dizer «na sala»."""
    i, j = texto.index('var ID="'), texto.index(',crono=null,tPistas=null;')
    texto = texto[:i] + texto[j:]
    a = texto.find('var ATL=')
    return texto if a < 0 else texto[:a] + texto[texto.index('\n', a):]


class SalaDesligada(unittest.TestCase):
    # mensagens curtas: as páginas têm centenas de KB e não se despejam no relatório
    def tem(self, marca, texto, onde):
        self.assertTrue(marca in texto, f'{onde}: falta {marca[:80]!r}')

    def nao_tem(self, marca, texto, onde):
        self.assertFalse(marca in texto, f'{onde}: ainda tem {marca[:80]!r}')

    def test_nenhum_ficheiro_publicado_tem_o_canal_nem_o_botao_ou_o_formulario(self):
        canal = ('ntfy', 'EventSource', 'BroadcastChannel', 'EPISala', 'aoEvento', 'enviarSala')
        formulario = ('id="liga-sala"', 'data-sala', '<div class="sala"', 'data-fechar-sala', 'Código da sala',
                      'A tua alcunha<input', 'id="faixa-pausa"', 'id="sobre"', 'sala-cod', 'data-placar', 'Nova sala')
        botao = re.compile(r'<button\b[^>]*>\s*Sala\b')
        n = 0
        for rel, texto in publicados():
            n += 1
            for marca in canal + formulario:
                self.nao_tem(marca, texto, rel)
            self.assertIsNone(botao.search(texto), rel)
        self.assertGreater(n, 700)

    def test_a_limpeza_corre_onde_a_sala_existia_e_so_ai(self):
        contagem = {tipo: len(lista) for tipo, lista in PAGINAS.items()}
        self.assertEqual(contagem, {'licao': 100, 'painel': 93, 'indice': 9, 'atlas': 1, 'mapa': 1, 'raiz': 1})
        for rel in TODAS:
            texto = ler(rel)
            with self.subTest(pagina=rel):
                self.assertEqual(texto.count(D.LIMPEZA_SCRIPT), 1)
                self.assertEqual(texto.count(D.SALA_LIMPAR_JS), 1)
        com_limpeza = sorted(rel for rel, texto in publicados() if 'painel-sala-' in texto or 'epi-sala' in texto)
        self.assertEqual(com_limpeza, TODAS)
        # as nove lições que nunca tiveram a Sala (ligam lesson.css) ficam como estavam
        licoes = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('m[1-9]/licao-*/index.html'))
        self.assertEqual(len(licoes), 109)
        sem_sala = sorted(set(licoes) - set(PAGINAS['licao']))
        self.assertEqual(len(sem_sala), 9)
        for rel in licoes:
            self.assertEqual('assets/pt-lessons/lesson.css' in ler(rel), rel in sem_sala, rel)

    def test_a_limpeza_e_a_das_fontes_e_apaga_so_o_que_a_sala_guardou(self):
        js = D.SALA_LIMPAR_JS
        self.assertEqual(re.findall(r'"(epi-[a-z-]+|painel-sala-)"', js), ['epi-sala', 'epi-sala-atlas', 'painel-sala-', 'epi-atlas-sala'])
        self.assertIn('localStorage.removeItem(k)', js)
        self.assertIn('sessionStorage.removeItem("epi-atlas-sala")', js)
        self.assertNotIn('clear()', js)
        self.assertNotIn('setItem', js)

    def test_pagina_inicial_limpa_antes_de_exportar_ou_repor_o_progresso(self):
        texto = ler('index.html')
        self.assertLess(texto.index(D.LIMPEZA_SCRIPT), texto.index(D.PROGRESSO_INICIO))
        self.assertEqual(texto.index(D.LIMPEZA_SCRIPT) + len(D.LIMPEZA_SCRIPT), texto.index(D.PROGRESSO_INICIO))

    def test_paineis_continuam_a_servir_a_aula_sem_placar_nem_codigo_de_sala(self):
        # 28/10/2026 (revisão): as instruções dos painéis com Atlas anunciam a tecla A; entram «Voltar ao início» (I),
        # o material do relâmpago (MATERIAL) e o QR grande no ecrã de abertura
        ficam = ('<h1 data-pedido>' + D.PAINEL_PEDIDO_NOVO + '</h1>', 'data-crono', '@keyframes pulsa',
                 '<div class="qr"><img src="data:image/png;base64,', 'CARTOES=', ',MATERIAL=', '<select data-r-k>',
                 'data-relampago', 'data-pausa', 'data-projetar', 'data-fecha', D.PAINEL_INICIO_NOVO, D.PAINEL_ESC_NOVO,
                 'function contar(seg,aoFim){', 'main.grelha{flex:1;display:grid;grid-template-columns:1fr;',
                 D.PAINEL_RELAMPAGO_JS, D.PAINEL_FECHA_INICIO_JS, D.PAINEL_TECLAS_JS, D.PAINEL_CSS_NOVO)
        saem = ('placar', 'data-cod', 'sala-cod', 'Nova sala', 'data-nova', 'data-limpar', 'data-sorteio',
                'data-votacao', 'data-codigo', 'data-add', 'data-canal', 'abrirSala', 'aoReceber', 'enviar(',
                'localStorage', 'sessionStorage', 'fetch(', 'alcunha', 'na sala', 'minmax(300px,34%)',
                'Fechar o cartão nos telemóveis', 'À espera das respostas')
        self.assertEqual(len(PAGINAS['painel']), 93)
        atlas = 0
        for rel in PAGINAS['painel']:
            texto = D.sem_limpeza(ler(rel))
            com_atlas = '<button type="button" data-atlas title="A">Quem sou eu?</button>' in texto
            atlas += com_atlas
            with self.subTest(painel=rel):
                for marca in ficam:
                    self.tem(marca, texto, rel)
                self.tem(D.PAINEL_COMO_NOVO_ATLAS if com_atlas else D.PAINEL_COMO_NOVO, texto, rel)
                if com_atlas:
                    self.tem(D.PAINEL_ATLAS_JS, texto, rel)
                codigo = codigo_do_painel(texto)
                for marca in saem:
                    self.nao_tem(marca, codigo, rel)
        self.assertEqual(atlas, 75)
        # os oito painéis estáticos (notas do docente, prolongamentos) nunca tiveram a Sala e ficam iguais
        estaticos = sorted(set(p.relative_to(ROOT).as_posix() for p in ROOT.glob('m[1-9]/painel-*/index.html')) - set(PAGINAS['painel']))
        self.assertEqual(len(estaticos), 8)
        for rel in estaticos:
            self.assertNotIn('CARTOES=', ler(rel))

    def test_relampago_mostra_o_material_da_licao_sem_a_solucao(self):
        # 28/10/2026 (revisão): antes, o telemóvel abria o cartão k da lição; agora o projetor mostra esse cartão:
        # o enunciado é o da lição, o material vem baralhado e sem a solução, e a correção (f) fica para o fim
        solucoes = {'c', 'v', 'certas', 'lacunas', 'pares', 'passos', 'linhas', 'fe'}
        n = 0
        for rel in PAGINAS['painel']:
            texto = ler(rel)
            P, MAT = banco(texto, 'CARTOES='), banco(texto, ',MATERIAL=')
            licao = rel.replace('/painel-', '/licao-')
            L = banco(ler(licao), 'CARTOES=')
            self.assertEqual(set(MAT), {str(c['k']) for c in P}, rel)
            for c in P:
                x, m = L[c['k']], MAT[str(c['k'])]
                n += 1
                with self.subTest(painel=rel, k=c['k']):
                    self.assertEqual(c['t'], x['t'])
                    self.assertEqual(D.normal(c['p']), D.normal(D.enunciado(x)))
                    self.assertFalse(solucoes & set(m), sorted(solucoes & set(m)))
                    self.assertEqual(m['f'], x['f'])
                    t = x['t']
                    if t in ('escolha', 'rever'):
                        self.assertEqual(sorted(m['o']), sorted(x['o']))
                    elif t in ('ordenar', 'versos', 'frase'):
                        certo = x['passos'] if t == 'ordenar' else x['linhas'] if t == 'versos' else x['palavras']
                        itens = m['palavras'] if t == 'frase' else m['itens']
                        self.assertEqual(sorted(itens), sorted(certo))
                        if len(set(certo)) > 1 and len(set(certo)) == len(certo):
                            self.assertNotEqual(itens, certo, 'a ordem mostrada é a solução')
                    elif t == 'emparelhar':
                        self.assertEqual(sorted(m['esq']), sorted(a for a, _ in x['pares']))
                        self.assertEqual(set(m['dir']), {b for _, b in x['pares']})
                        self.assertEqual(len(m['dir']), len(set(m['dir'])))
                    elif t == 'completar':
                        self.assertEqual(m['frase'], x['frase'])
                        self.assertEqual([sorted(o) for o in m['lac']], [sorted(l['o']) for l in x['lacunas']])
                    elif t == 'sublinhar':
                        self.assertEqual(m['frase'], x['frase'])
                    else:
                        self.assertEqual(t, 'vf')
        self.assertEqual(n, 1445)

    def test_licoes_sem_envio_com_o_cartao_extra_e_o_menu_que_fica(self):
        for rel in PAGINAS['licao']:
            texto = ler(rel)
            with self.subTest(licao=rel):
                for marca in ('evento:function(ev){aoEvento(ev)}', 'EPICasca.abrir({marca:"Relâmpago"', 'window.REL'):
                    self.nao_tem(marca, texto, rel)
                for marca in (D.LICAO_FIM_JS + D.LICAO_ESC + '})();', 'function abrirExtra(',
                              D.MENU_COMO + '<p class="c-menu-extra">', 'O que marcas fica só neste aparelho.'):
                    self.tem(marca, texto, rel)

    def test_indices_e_desafio_sem_envio(self):
        self.assertEqual(PAGINAS['indice'], [f'm{m}/index.html' for m in range(1, 10)])
        for m in range(1, 10):
            texto = ler(f'm{m}/index.html')
            with self.subTest(modulo=m):
                self.nao_tem('.casca-menu .sala{', texto, m)
                if m in (3, 5, 6, 8, 9):
                    self.tem('titulo:"Desafio da unidade "+u.n', texto, m)
                    self.tem('pintar();if(festa)surpresa(u);}})}});', texto, m)

    def test_atlas_sem_sala_e_mapa_da_turma_leva_ao_atlas(self):
        atlas = ler('atlas/index.html')
        self.nao_tem('.sala-f', atlas, 'atlas')
        self.tem('evento:function(ev){', atlas, 'atlas')  # o progresso das figuras no Atlas não é da Sala
        self.tem('// ── folhas: pessoa, todas as pessoas, passaporte, final', atlas, 'atlas')
        mapa = ler('atlas/sala/index.html')
        alvo = 'https://pedrohfernandes-klk.github.io/pt/atlas/'
        self.assertIn('<meta name="robots" content="noindex">', mapa)
        self.assertIn(f'<meta http-equiv="refresh" content="0;url={alvo}">', mapa)
        self.assertIn(f'<link rel="canonical" href="{alvo}">', mapa)
        self.assertIn(f'Esta página mudou de sítio: <a href="{alvo}">Atlas Lusófono</a>.', mapa)
        self.assertNotIn('mapa da turma', mapa)
        self.assertLess(len(mapa), 10000)

    def test_textos_novos_seguem_as_regras_de_escrita(self):
        # 28/10/2026 (revisão): entram as instruções com a tecla A, «Voltar ao início», as dicas do relâmpago,
        # o rótulo do «Quem sou eu?» e o rótulo «Correção»
        for texto in (D.PAINEL_COMO_NOVO, D.PAINEL_COMO_NOVO_ATLAS, D.PAINEL_INICIO_NOVO, D.PAINEL_PEDIDO_NOVO,
                      D.PAINEL_ESC_NOVO, D.PAINEL_TEMPO_NOVO, D.PAINEL_RELAMPAGO_NOVO, D.PAINEL_ATLAS_ROT,
                      D.LIMPEZA_COMENTARIO, D.LICAO_FIM_JS, D.PAINEL_RELAMPAGO_JS, *D.PAINEL_DICAS.values()):
            visivel = texto_visivel(texto)
            with self.subTest(texto=visivel[:40]):
                for proibido in ('—', '·', 'professor', 'ficha', 'folha'):
                    self.assertNotIn(proibido, visivel.lower())
                self.assertIsNone(re.search(r'(?i)\bjog', visivel))

    def test_manifesto_literal_desfaz_e_refaz_as_paginas_congeladas(self):
        files = MANIFESTO['files']
        # 28/10/2026 (revisão): as 61 páginas congeladas no dia do corte; uma página que se congele depois já é
        # congelada sem a Sala e fica fora do manifesto, por isso aqui confere-se só que o manifesto não sai daí
        self.assertLessEqual(set(files), set(TODAS) & D.congelados())
        self.assertEqual(len(files), 61)
        for rel, registo in files.items():
            atual = ler(rel)
            with self.subTest(pagina=rel):
                for edit in registo['edits']:
                    self.assertTrue(edit['new'])
                    self.assertEqual(edit['occurrences'], 1)
                antes = undo_sala(rel, atual)
                self.tem(D.EPISALA_SCRIPT, antes, rel)
                refeito = antes
                for edit in registo['edits']:
                    self.assertEqual(refeito.count(edit['old']), edit['occurrences'], (rel, edit['location']))
                    refeito = refeito.replace(edit['old'], edit['new'])
                self.assertTrue(refeito == atual, f'{rel}: refazer as trocas não dá a página atual')

    def test_script_reconhece_a_forma_e_falha_com_uma_desconhecida(self):
        rel = 'm1/licao-m1-f01/index.html'
        original = undo_sala(rel, ler(rel))
        novo, edits = D.aplicar(rel, original, D.trocas_licao(rel, original))
        self.assertTrue(novo == ler(rel), 'o script não reproduz a lição atual')
        self.assertEqual(edits, MANIFESTO['files'][rel]['edits'])
        alterado = original.replace('ligaSala()})();', 'ligaSala();})();')
        with self.assertRaises(D.FormaDesconhecida):
            D.aplicar(rel, alterado, D.trocas_licao(rel, alterado))
        self.assertIsNone(D.tipo_de('m1/m1-voz-emprestada/index.html'))

    def test_script_aceita_mudancas_fora_da_sala_nas_paginas_congeladas(self):
        # 28/10/2026 (revisão): uma troca literal posterior numa lição congelada, longe da Sala, não pode deixar o
        # script inutilizável; só um bloco que as trocas da Sala tocam dá o aviso, e esse aviso é o do manifesto
        rel = 'm2/licao-m2-f01/index.html'
        texto, reg = ler(rel), MANIFESTO['files'][rel]
        alterado = texto.replace('fica só neste aparelho.', 'fica só neste telemóvel.', 1)
        self.assertNotEqual(alterado, texto)
        D.confirmar_congelada(rel, 'licao', alterado, reg)
        estragado = texto.replace(D.LIMPEZA_SCRIPT, D.LIMPEZA_SCRIPT.replace('"epi-sala-atlas"', '"epi-sala-atlaz"'))
        with self.assertRaises(D.ManifestoDesatualizado):
            D.confirmar_congelada(rel, 'licao', estragado, reg)

    def test_script_nao_tem_nada_por_fazer(self):
        r = subprocess.run([sys.executable, str(ROOT / 'scripts/desligar_sala.py'), '--verificar'],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Nada a mudar', r.stdout)


if __name__ == '__main__':
    unittest.main()
