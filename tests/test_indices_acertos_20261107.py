"""07/11/2026: os três acertos dos índices do Português que a decisão 173 deixou para um pedido próprio (decisão 48).

Confere a camada literal indices_acertos_20261107 (fechada, com contagens, reversível até ao main 93907af1 letra a letra e a
mais recente) e cada acerto:

1. no M3, no M5 e no M6 sai a ligação repetida a.teacher-access, e o destino (os guiões do docente) continua no menu dos
   materiais da mesma página;
2. nenhuma legenda de «Neste módulo» tem «·» (no M8 e no M9, « · » passa a «, », como nos outros sete);
3. o lugar flutuante do menu dos materiais sai do style do HTML para assets/cartaz-indice-comum.css, que o mantém igual com
   JavaScript e a partir de 640 px e, sem JavaScript abaixo de 640 px, abre o menu no fluxo (o comportamento no navegador
   confere-se em tests/browser_cartaz_m4_interacoes.cjs).
"""
import glob
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

import test_cartaz_indices_148 as c148
from auditoria_20261028 import undo_acertos_0711
# 07/11/2026 (fusão do main 29441e6b no pedido #182): por cima dos acertos fica a decisão 152 no M1 (camada cuidado_m1_20261106).
from auditoria_20261028 import undo_cuidado_m1_0611

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/indices_acertos_20261107.json'
MANIFESTO = ROOT / 'tests/fixtures/indices-acertos-edits-20261107.json'
NOVE = [f'm{n}/index.html' for n in range(1, 10)]
GUIOES = 'https://pedrohfernandes-klk.github.io/lente/docente/#portugues'
# sha256 dos nove índices no main 93907af1 (git show 93907af1:mN/index.html | sha256sum): desfeita a camada, têm de dar o mesmo.
MAIN_93907AF1 = {
    'm1/index.html': '2d1a72a1a762aa8f1d9fd4337dbac95d11b163b7de5bbe749150d636fc0a5609',
    'm2/index.html': '44e5ae51c66f2e3f252edfc70717ca8d2afd84d313d734a3354752db3d1d3f6a',
    'm3/index.html': '50e5e3a82ff853110125f28700a673087521f6624316464ab1ac4a84063238fd',
    'm4/index.html': '8e2574ceec5bf2f46a1162e5a9b7f6d48d48d387b3493ac58dec47a03339d506',
    'm5/index.html': '2120843a6b0c23d74074e00b520077e5a93cea20aea1e6d90c42498e8c6afa78',
    'm6/index.html': '02260926b383d566a52c27825de4dceced5d9b3884c928211a4f34eb6074b090',
    'm7/index.html': '35cfc67367e70252d64a19029e8e3188530d920a9c0512fec4389e5c0a08e9e8',
    'm8/index.html': '65e268841168340dabc0bdace7a71f4ca9fb0661de605dd499e67ecb9ade7097',
    'm9/index.html': '80c270fbd249606868c8d73672f2e1dba0fdd9bd23f0e0dca422f046e664b105',
}
SELETOR_MENU = 'body:has(main[data-cz-indice])>details.route-teacher-tools>summary.teacher-access+nav'
ESTILO_MENU = ('z-index:1001;max-width:calc(100vw - 24px);padding:12px 16px;background:var(--papel,#fff);'
               'color:var(--tinta,#171715);border:1px solid currentColor')


def ler(rel):
    return (ROOT / rel).read_text('utf-8')


def ler_bytes(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def regras(css):
    """Cada regra do CSS, com os @media que a envolvem, pela ordem do ficheiro (sem comentários)."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    chaveta = re.compile(r'[{}]')
    pilha, saida, i = [], [], 0
    while True:
        m = chaveta.search(css, i)
        if not m:
            return saida
        cabeca = css[i:m.start()].strip()
        if m.group(0) == '}':
            if pilha:
                pilha.pop()
            i = m.end()
        elif cabeca.startswith('@') and not cabeca.startswith('@font-face'):
            pilha.append(cabeca)
            i = m.end()
        else:
            fim = css.index('}', m.end())
            saida.append((tuple(pilha), cabeca, css[m.end():fim].strip()))
            i = fim + 1


class Acertos0711(unittest.TestCase):
    def test_camada_mais_recente_fechada_e_reversivel(self):
        # A camada mais recente confere-se sem nada por cima, com as contagens exatas do manifesto.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', str(CAMADA.relative_to(ROOT)), '--manifesto',
                            str(MANIFESTO.relative_to(ROOT)), '--verificar',
                            # 07/11/2026 (fusão do main 29441e6b no pedido #182): a decisão 152 no M1 fica por cima; desfaz-se primeiro, com a mesma exigência.
                            # 07/11/2026: os créditos atrás de um «i» na entrada, nos índices e no Atlas (creditos_i_pt1_20261107, pedido pt-1) passam a camada mais recente, por cima da decisão 152 no M1; desfazem-se primeiro, com a mesma exigência.
                            # 08/11/2026: o cartaz «Ler a cidade» na entrada e o nome novo da secção nas páginas publicadas (cidade_cartaz_20261108) passam a camada mais recente, por cima dos créditos atrás de um «i» do pedido pt-1 (e mudam páginas desta cadeia: a entrada, os índices e a frase da sugestão «continua»); desfazem-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M2 (cuidado_m2_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M2, incluindo o índice do módulo) passa a camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção; desfaz-se primeiro, com a mesma exigência.
                            '--desfazer-antes', 'tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cidade-cartaz-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/creditos-i-pt1-edits-20261107.json', '--desfazer-antes', 'tests/fixtures/cuidado-m1-edits-20261106.json'], cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('25 trocas em 9 ficheiros: 25 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        manifesto = json.loads(MANIFESTO.read_text('utf-8'))
        self.assertEqual(sorted(manifesto['files']), NOVE)
        self.assertEqual(manifesto['base_commit'], '93907af1fb2481cb537df27ad6a777d0a87c3f8a')
        trocas = json.loads(CAMADA.read_text('utf-8'))
        self.assertEqual(Counter(t['ficheiro'] for t in trocas),
                         Counter({'m1/index.html': 2, 'm2/index.html': 2, 'm3/index.html': 3, 'm4/index.html': 2,
                                  'm5/index.html': 3, 'm6/index.html': 3, 'm7/index.html': 2, 'm8/index.html': 4,
                                  'm9/index.html': 4}))
        self.assertTrue(all(t['ocorrencias'] == 1 for t in trocas))
        for rel in NOVE:
            with self.subTest(indice=rel):
                atual = ler_bytes(rel)
                base = undo_acertos_0711(rel, atual)
                # Desfeita a camada, o índice é o do main 93907af1, letra a letra.
                self.assertEqual(hashlib.sha256(base.encode('utf-8')).hexdigest(), MAIN_93907AF1[rel])
                refeito = base
                for e in manifesto['files'][rel]['edits']:
                    self.assertEqual(refeito.count(e['old']), 1, (rel, e['location']))
                    self.assertEqual(refeito.count(e['new']), 0, (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                # 07/11/2026 (fusão do main 29441e6b no pedido #182): o «depois» desta camada é a página com a decisão 152 no M1 desfeita (a camada por cima), letra a letra.
                self.assertEqual(refeito, undo_cuidado_m1_0611(rel, atual), rel)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('indices_acertos', ROOT / 'scripts/indices_acertos_20261107.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.construir(), json.loads(CAMADA.read_text('utf-8')))

    def test_registada_como_a_primeira_camada(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): por cima dos acertos fica a decisão 152 no M1; os acertos passam a segundos, logo por baixo dela.
        # 07/11/2026: por cima da decisão 152 no M1 ficam os créditos atrás de um «i» do pedido pt-1; a ordem ganha uma posição e os
        # acertos passam a terceiros.
        # 08/11/2026: por cima dos créditos do pedido pt-1 fica o cartaz «Ler a cidade» e o nome novo da secção
        # (cidade_cartaz_20261108); a ordem ganha mais uma posição e os acertos passam a quartos.
        # 08/11/2026: por cima do cartaz «Ler a cidade» fica a decisão 152 no M2 (cuidado_m2_20261108); a ordem ganha mais uma
        # posição e os acertos passam a quintos.
        self.assertEqual(verificar_camadas.LAYERS[0], ('cuidado_m2_20261108', 'cuidado-m2-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cidade_cartaz_20261108', 'cidade-cartaz-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('creditos_i_pt1_20261107', 'creditos-i-pt1-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cuidado_m1_20261106', 'cuidado-m1-edits-20261106'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('indices_acertos_20261107', 'indices-acertos-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cartaz_indices_148_20261106', 'cartaz-indices-148-edits-20261106'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cartaz_148_0611'):]
        self.assertLess(corpo.index('undo_acertos_0711(path, text)'), corpo.index('_CARTAZ_148_0611.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('indices-acertos-edits-20261107.json'), sala.index('cartaz-indices-148-edits-20261106.json'))
        # Em cada cadeia dos workflows, os acertos desfazem-se antes do desenho comum (as mesmas 13 cadeias).
        cadeias = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if '--desfazer-antes tests/fixtures/cartaz-indices-148-edits-20261106.json' in linha:
                    cadeias += 1
                    self.assertIn('aplicar_trocas.py', linha, wf)
                    # 07/11/2026 (fusão do main 29441e6b no pedido #182): a decisão 152 no M1 desfaz-se antes de tudo, logo a seguir a --verificar.
                    # 07/11/2026: antes dela, logo a seguir a --verificar, os créditos atrás de um «i» do pedido pt-1 (a camada mais recente).
                    # 08/11/2026: e, antes deles, logo a seguir a --verificar, o cartaz «Ler a cidade» e o nome novo da secção
                    # (cidade_cartaz_20261108), a camada mais recente; a cadeia de baixo fica igual, sem nada pelo meio.
                    # 08/11/2026: e, antes do cartaz, logo a seguir a --verificar, a decisão 152 no M2 (cuidado_m2_20261108), a camada
                    # mais recente; a cadeia de baixo fica igual, sem nada pelo meio.
                    self.assertIn('--verificar --desfazer-antes tests/fixtures/cuidado-m2-edits-20261108.json --desfazer-antes tests/fixtures/cidade-cartaz-edits-20261108.json --desfazer-antes tests/fixtures/creditos-i-pt1-edits-20261107.json --desfazer-antes tests/fixtures/cuidado-m1-edits-20261106.json --desfazer-antes tests/fixtures/indices-acertos-edits-20261107.json --desfazer-antes '
                                  'tests/fixtures/cartaz-indices-148-edits-20261106.json', linha, wf)
        self.assertEqual(cadeias, 13)
        for wf in ('pt-tarefas-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + wf)
            for caminho in ('scripts/indices_acertos_20261107.*', 'tests/fixtures/indices-acertos-edits-20261107.json',
                            'tests/test_indices_acertos_20261107.py'):
                self.assertIn(f"'{caminho}'", texto, wf)
        # Nas cadeias dos testes, os acertos vêm logo antes do desenho comum, sem outra camada pelo meio.
        for rel in ('tests/test_cartaz_cabecalho.py', 'tests/test_cartaz_indices.py', 'tests/test_task_routes_closure.py',
                    'tests/test_tasks_m356.py', 'tests/test_tasks_m89.py', 'tests/test_variedade_f0.py',
                    'tests/test_autonomia_154.py', 'tests/test_cartaz_m4_piloto.py'):
            texto = ler(rel)
            posicoes = [m.start() for m in re.finditer(re.escape('indices-acertos-edits-20261107.json'), texto)]
            with self.subTest(teste=rel):
                self.assertTrue(posicoes)
                for p in posicoes:
                    seguinte = texto.index('cartaz-indices-148-edits-20261106.json', p)
                    self.assertNotIn('edits-2026', texto[p + len('indices-acertos-edits-20261107.json'):seguinte])
        # A conferência da camada do desenho comum desfaz primeiro os acertos (estão por cima dela).
        self.assertIn("'--desfazer-antes', 'tests/fixtures/indices-acertos-edits-20261107.json'", ler('tests/test_cartaz_indices_148.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            with self.subTest(teste=rel):
                self.assertLess(texto.index('((acertos['), texto.index('((comum148['))

    def test_um_so_acesso_do_docente_e_os_guioes_no_menu(self):
        for n, rel in enumerate(NOVE, 1):
            s, antes = ler(rel), undo_acertos_0711(rel, ler(rel))
            with self.subTest(indice=rel):
                # Um só acesso do docente, o botão dos materiais (sai a ligação repetida, que recebia o foco sem se ver).
                self.assertEqual(s.count('class="teacher-access"'), 1)
                self.assertEqual(s.count('<summary class="teacher-access" aria-label="Abrir materiais do docente"'), 1)
                self.assertNotIn('<a class="teacher-access"', s)
                self.assertNotIn('Guiões e materiais do docente', s)
                # Antes, a ligação repetida só existia no M3, no M5 e no M6, logo antes do menu.
                self.assertEqual(antes.count(f'<a class="teacher-access" href="{GUIOES}"'), 1 if n in (3, 5, 6) else 0)
                # O destino continua na página: no menu dos materiais do docente, com o mesmo endereço.
                menu = re.findall(r'<details class="route-teacher-tools"><summary class="teacher-access"[^>]*>.*?</summary>'
                                  r'<nav aria-label="Materiais do docente"[^>]*>(.*?)</nav></details>', s, re.S)
                self.assertEqual(len(menu), 1)
                self.assertIn(f'<p><a href="{GUIOES}">Guiões do docente</a></p>', menu[0])
                self.assertEqual(s.count(f'href="{GUIOES}"'), 1)

    def test_neste_modulo_sem_ponto_medio(self):
        for n, rel in enumerate(NOVE, 1):
            # 07/11/2026 (fusão do main 29441e6b no pedido #182): confere-se a página com a decisão 152 no M1 desfeita (a camada por cima, que põe espaços que não
            # quebram, como em «90 min»); o que a decisão 152 muda confere-se em tests/test_cuidado_m1.py.
            s, antes = undo_cuidado_m1_0611(rel, ler(rel)), undo_acertos_0711(rel, ler(rel))
            with self.subTest(indice=rel):
                lista = re.search(r'<nav (?:aria-label="Unidades do módulo" class="unit-index"|class="unit-index" '
                                  r'aria-label="Unidades do módulo")><p>Neste módulo</p>(.*?)</nav>', s, re.S).group(1)
                legendas = re.findall(r'<small>([^<]*)</small>', lista)
                self.assertEqual(len(legendas), 3 if n in (4, 7) else 2)
                for legenda in legendas:
                    self.assertRegex(legenda, r'^\d+ aulas de leitura/preparação, tarefa 90 min$')
                # Nenhum «·» em todo o índice (no M8 e no M9 só os havia nestas legendas).
                self.assertNotIn('·', s)
                # Os números não mudam.
                self.assertEqual(re.findall(r'<small>(\d+) aulas', lista), re.findall(r'<small>(\d+) aulas', antes))
                self.assertEqual(antes.count(' · tarefa 90 min</small>'), 2 if n in (8, 9) else 0)

    def test_menu_dos_materiais_sem_lugar_no_html(self):
        for rel in NOVE:
            s = ler(rel)
            with self.subTest(indice=rel):
                estilos = re.findall(r'<nav aria-label="Materiais do docente" style="([^"]*)">', s)
                self.assertEqual(estilos, [ESTILO_MENU])
                self.assertNotRegex(estilos[0], r'(?:^|;)\s*(?:position|left|bottom|top|right|inset)\s*:')
                self.assertEqual(s.count('<link rel="stylesheet" href="../assets/cartaz-indice-comum.css?v=20261107">'), 1)
                self.assertNotIn('cartaz-indice-comum.css?v=20261106', s)
        css = ler('assets/cartaz-indice-comum.css')
        self.assertNotIn('!important', css)
        menu = [(i, medias, corpo) for i, (medias, seletor, corpo) in enumerate(regras(css)) if seletor == SELETOR_MENU]
        # Duas regras para o menu no fim do <body>: o lugar flutuante de sempre, sem @media (também na impressão), e, depois
        # dela, só no ecrã e abaixo de 640 px (sem JavaScript, porque com JavaScript o menu está dentro dos recursos), no fluxo.
        self.assertEqual([(m, c) for _, m, c in menu],
                         [((), 'position:fixed;left:12px;bottom:64px;'),
                          (('@media screen', '@media not all and (min-width:640px)'), 'position:static;')])
        self.assertLess(menu[0][0], menu[1][0])
        # Nenhuma outra regra do CSS muda o lugar deste menu.
        for medias, seletor, corpo in regras(css):
            if seletor != SELETOR_MENU and re.search(r'route-teacher-tools[^,{]*>\s*nav|teacher-access\+nav', seletor):
                self.assertNotRegex(corpo, r'(?:^|;)\s*(?:position|left|bottom|top|right|inset)\s*:', seletor)
                self.assertIn('.cz-docente', seletor)

    def test_nada_mais_muda(self):
        for n, rel in enumerate(NOVE, 1):
            s = ler(rel)
            # 07/11/2026 (fusão do main 29441e6b no pedido #182): o «depois» é a página com a decisão 152 no M1 desfeita (a camada por cima desta).
            antes, depois = c148.Inventario(undo_acertos_0711(rel, s)), c148.Inventario(undo_cuidado_m1_0611(rel, s))
            with self.subTest(indice=rel):
                self.assertEqual(antes.ids, depois.ids)
                self.assertEqual(antes.imgs, depois.imgs)
                self.assertEqual(antes.dados, depois.dados)
                self.assertEqual(antes.scripts, depois.scripts)
                sem_versao = lambda h: h.split('?')[0] if h.startswith('../assets/cartaz-indice-comum.css') else h
                perdidas = Counter(map(sem_versao, antes.hrefs)) - Counter(map(sem_versao, depois.hrefs))
                self.assertEqual(perdidas, Counter({GUIOES: 1}) if n in (3, 5, 6) else Counter())
                self.assertEqual(Counter(map(sem_versao, depois.hrefs)) - Counter(map(sem_versao, antes.hrefs)), Counter())
                perdidos = Counter(antes.textos) - Counter(depois.textos)
                ganhos = Counter(depois.textos) - Counter(antes.textos)
                self.assertEqual(sorted(ganhos.elements()), sorted(t.replace(' · ', ', ') for t in perdidos.elements()))
                self.assertEqual(len(list(perdidos.elements())), 2 if n in (8, 9) else 0)


if __name__ == '__main__':
    unittest.main()
