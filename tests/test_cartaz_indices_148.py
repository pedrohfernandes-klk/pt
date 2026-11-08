"""06/11/2026: decisão 148. O desenho do índice do M4 (#166) nos nove índices do Português.

Confere a camada literal cartaz_indices_148_20261106 (fechada, com contagens, reversível e a mais recente) e o desenho que ela
dá aos nove índices, o mesmo para todos: a palavra do módulo à vista, «Recursos do módulo» no fluxo, o título de cada unidade
na banda, a prova junto da pergunta, a imagem documental mais pequena a seguir às unidades e os botões flutuantes de sempre
(modo noturno e acesso do docente) fora dos recursos. Nada do conteúdo se perde: ligações, âncoras, ids, chaves de progresso,
dados do motor, imagens e textos ficam todos.
"""
import glob
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from auditoria_20261028 import undo_cartaz_148_0611
# 07/11/2026: por cima desta camada ficam os acertos da decisão 173 (camada indices_acertos_20261107).
from auditoria_20261028 import undo_acertos_0711
# 07/11/2026: por cima de tudo ficam os créditos atrás de um «i» do pedido pt-1 (camada creditos_i_pt1_20261107).
from auditoria_20261028 import undo_creditos_i_pt1_0711

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/cartaz_indices_148_20261106.json'
MANIFESTO = ROOT / 'tests/fixtures/cartaz-indices-148-edits-20261106.json'
NOVE = [f'm{n}/index.html' for n in range(1, 10)]
# Textos que só o piloto M4 tinha posto (não são do módulo) e que saem com os botões que voltam a flutuar.
SO_DO_PILOTO_M4 = ['Neste aparelho', 'Materiais do docente']


def ler(rel):
    return (ROOT / rel).read_text('utf-8')


class Inventario(HTMLParser):
    """Ids, ligações, imagens, dados, scripts e textos visíveis de uma página, pela ordem do documento."""

    def __init__(self, texto):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.imgs, self.dados, self.scripts, self.textos = [], [], [], [], [], []
        self._script = None
        self._estilo = False
        self.feed(texto)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if 'href' in a:
            self.hrefs.append(a['href'])
        if tag == 'img':
            self.imgs.append(tuple(sorted(a.items())))
        self.dados += [(k, v) for k, v in attrs if k.startswith('data-') and k not in ('data-cz-indice', 'data-m4-piloto')]
        if tag == 'script':
            self._script = [a.get('src', ''), '']
            self.scripts.append(self._script)
        if tag == 'style':
            self._estilo = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self._script = None
        if tag == 'style':
            self._estilo = False

    def handle_data(self, data):
        if self._script is not None:
            self._script[1] += data
        elif not self._estilo and data.strip():
            self.textos.append(re.sub(r'\s+', ' ', data.strip()))


class Camada148(unittest.TestCase):
    def test_camada_mais_recente_fechada_e_reversivel(self):
        # A camada mais recente confere-se sem nada por cima, com as contagens exatas do manifesto.
        # 07/11/2026: por cima dela ficam os acertos da decisão 173 (indices_acertos_20261107), que se desfazem primeiro, com a
        # mesma exigência; as contagens e a reversibilidade desta camada conferem-se como antes.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', str(CAMADA.relative_to(ROOT)), '--manifesto',
                            str(MANIFESTO.relative_to(ROOT)), '--verificar',
                            # 07/11/2026 (fusão do main 29441e6b no pedido #182): por cima de tudo, a decisão 152 no M1; desfaz-se primeiro, com a mesma exigência.
                            # 07/11/2026: os créditos atrás de um «i» na entrada, nos índices e no Atlas (creditos_i_pt1_20261107, pedido pt-1) passam a camada mais recente, por cima da decisão 152 no M1; desfazem-se primeiro, com a mesma exigência.
                            # 08/11/2026: o cartaz «Ler a cidade» na entrada e o nome novo da secção nas páginas publicadas (cidade_cartaz_20261108) passam a camada mais recente, por cima dos créditos atrás de um «i» do pedido pt-1 (e mudam páginas desta cadeia: a entrada, os índices e a frase da sugestão «continua»); desfazem-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M2 (cuidado_m2_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M2, incluindo o índice do módulo) passa a camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M3 (cuidado_m3_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M3, incluindo o índice, o guia e o mapa do módulo) passa a camada mais recente, por cima da decisão 152 no M2; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M4 (cuidado_m4_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M4, incluindo o índice, o guia, o mapa e o portefólio do módulo) passa a camada mais recente, por cima da decisão 152 no M3; desfaz-se primeiro, com a mesma exigência.
                            '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cidade-cartaz-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/creditos-i-pt1-edits-20261107.json', '--desfazer-antes', 'tests/fixtures/cuidado-m1-edits-20261106.json',
                            '--desfazer-antes', 'tests/fixtures/indices-acertos-edits-20261107.json'],  # 07/11/2026: acertos por cima.
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('92 trocas em 9 ficheiros: 92 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        manifesto = json.loads(MANIFESTO.read_text('utf-8'))
        self.assertEqual(sorted(manifesto['files']), NOVE)
        self.assertEqual(manifesto['base_commit'], '8dbcb41967ea1676bc8befbacbc0144ee47caadd')
        trocas = json.loads(CAMADA.read_text('utf-8'))
        self.assertEqual(Counter(t['ficheiro'] for t in trocas),
                         Counter({'m1/index.html': 10, 'm2/index.html': 10, 'm3/index.html': 10, 'm4/index.html': 9,
                                  'm5/index.html': 10, 'm6/index.html': 10, 'm7/index.html': 13, 'm8/index.html': 10,
                                  'm9/index.html': 10}))
        self.assertTrue(all(t['ocorrencias'] == 1 for t in trocas))
        for rel in NOVE:
            atual = ler(rel)
            base = undo_cartaz_148_0611(rel, atual)
            edits = manifesto['files'][rel]['edits']
            # Reaplicar as trocas sobre a base devolve a página publicada, letra a letra.
            refeito = base
            for e in edits:
                self.assertEqual(refeito.count(e['old']), e['occurrences'], (rel, e['location']))
                refeito = refeito.replace(e['old'], e['new'])
            # 07/11/2026: a página publicada com os acertos da decisão 173 desfeitos (a camada por cima desta), letra a letra.
            self.assertEqual(refeito, undo_acertos_0711(rel, atual), rel)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('cartaz_indices_148', ROOT / 'scripts/cartaz_indices_148_20261106.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.construir(), json.loads(CAMADA.read_text('utf-8')))

    def test_registada_como_a_primeira_camada(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 07/11/2026: os acertos da decisão 173 ficam por cima (primeira camada); esta passa a segunda, logo por baixo deles.
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): por cima dos acertos fica a decisão 152 no M1; os acertos passam a segundos e esta camada a terceira.
        # 07/11/2026: por cima da decisão 152 no M1 ficam os créditos atrás de um «i» do pedido pt-1; a ordem ganha uma posição e
        # esta camada passa a quarta.
        # 08/11/2026: por cima dos créditos do pedido pt-1 fica o cartaz «Ler a cidade» e o nome novo da secção
        # (cidade_cartaz_20261108); a ordem ganha mais uma posição e esta camada passa a quinta.
        # 08/11/2026: por cima do cartaz «Ler a cidade» fica a decisão 152 no M2 (cuidado_m2_20261108); a ordem ganha mais uma
        # posição e esta camada passa a sexta.
        # 08/11/2026: por cima da decisão 152 no M2 fica a decisão 152 no M3 (cuidado_m3_20261108); a ordem ganha mais uma posição.
        # 08/11/2026: por cima da decisão 152 no M3 fica a decisão 152 no M4 (cuidado_m4_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cuidado_m3_20261108', 'cuidado-m3-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('cuidado_m2_20261108', 'cuidado-m2-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cidade_cartaz_20261108', 'cidade-cartaz-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('creditos_i_pt1_20261107', 'creditos-i-pt1-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cuidado_m1_20261106', 'cuidado-m1-edits-20261106'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('indices_acertos_20261107', 'indices-acertos-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cartaz_indices_148_20261106', 'cartaz-indices-148-edits-20261106'))
        self.assertEqual(verificar_camadas.LAYERS[8], ('creditos_i_20261105', 'creditos-i-edits-20261105'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_creditos_i_0511'):]
        self.assertLess(corpo.index('undo_cartaz_148_0611(path, text)'), corpo.index('_CREDITOS_I_0511.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cartaz-indices-148-edits-20261106.json'), sala.index('creditos-i-edits-20261105.json'))
        # Em cada cadeia dos workflows, o desenho comum desfaz-se antes dos créditos atrás de um «i».
        cadeias = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if '--desfazer-antes tests/fixtures/creditos-i-edits-20261105.json' in linha:
                    cadeias += 1
                    self.assertIn('--desfazer-antes tests/fixtures/cartaz-indices-148-edits-20261106.json --desfazer-antes '
                                  'tests/fixtures/creditos-i-edits-20261105.json', linha, wf)
        self.assertEqual(cadeias, 13)

    def test_nada_do_conteudo_se_perde(self):
        for rel in NOVE:
            with self.subTest(indice=rel):
                atual = ler(rel)
                # 07/11/2026: o «depois» desta camada é a página com os acertos da decisão 173 desfeitos (o que eles mudam confere-se
                # em tests/test_indices_acertos_20261107.py).
                antes, depois = Inventario(undo_cartaz_148_0611(rel, atual)), Inventario(undo_acertos_0711(rel, atual))
                self.assertEqual(antes.ids, depois.ids)
                estilos = ('cartaz-indices.css', 'cartaz-m4-piloto.css', 'cartaz-indice-comum.css')
                self.assertEqual(Counter(x for x in antes.hrefs if x.split('?')[0].rsplit('/', 1)[-1] not in estilos),
                                 Counter(x for x in depois.hrefs if x.split('?')[0].rsplit('/', 1)[-1] not in estilos))
                self.assertEqual(antes.imgs, depois.imgs)
                # No M4 sai só o lugar do modo noturno dentro dos recursos (o botão volta a flutuar, decisão 148).
                self.assertEqual(Counter(antes.dados) - Counter(depois.dados),
                                 Counter({('data-appearance-control', ''): 1}) if rel == 'm4/index.html' else Counter())
                self.assertEqual(Counter(depois.dados) - Counter(antes.dados), Counter())
                # Os scripts (dados do motor, chaves de progresso, rota do adaptador) ficam iguais; só muda o dos recursos.
                tira = ('cartaz-indice-comum.js', 'cartaz-m4-piloto.js')
                self.assertEqual([s for s in antes.scripts if not s[0].split('?')[0].endswith(tira)],
                                 [s for s in depois.scripts if not s[0].split('?')[0].endswith(tira)])
                self.assertEqual(re.findall(r'localStorage\.[\s\S]{0,150}', undo_cartaz_148_0611(rel, atual)),
                                 re.findall(r'localStorage\.[\s\S]{0,150}', atual))
                # Os textos são os mesmos (o título da unidade passa do cabeçalho do grupo para a banda, onde já estava).
                perdidos = Counter(antes.textos) - Counter(depois.textos)
                ganhos = Counter(depois.textos) - Counter(antes.textos)
                if rel == 'm4/index.html':
                    self.assertEqual(sorted(perdidos.elements()), sorted(SO_DO_PILOTO_M4))
                else:
                    # Só sai a segunda cópia do título de cada unidade (estava na banda e no cabeçalho do grupo).
                    titulos = re.findall(r'<h2 class="cz-fold-t" id="unidade-pedagogica-\d+">(.*?)</h2>', atual)
                    esperados = Counter()
                    for t in titulos:
                        esperados += Counter(Inventario(t).textos)
                        self.assertEqual(atual.count(f'>{t}</h2>'), 1)
                    self.assertEqual(perdidos, esperados)
                # Só entra o nome dos recursos, como no M4 (que já o tinha).
                self.assertEqual(ganhos, Counter() if rel == 'm4/index.html' else Counter({'Recursos do módulo': 1}))

    def test_o_mesmo_desenho_nos_nove(self):
        for n, rel in enumerate(NOVE, 1):
            s = ler(rel)
            with self.subTest(indice=rel):
                main = s[s.index('<main'):s.index('</main>')]
                self.assertEqual(s.count('<main data-cartaz="2" class="cz-index" data-cz-indice="20261106">'), 1)
                # 07/11/2026: o CSS comum na versão dos acertos da decisão 173 (camada indices_acertos_20261107).
                self.assertEqual(s.count('<link rel="stylesheet" href="../assets/cartaz-indice-comum.css?v=20261107">'), 1)
                self.assertEqual(s.count('<script src="../assets/cartaz-indice-comum.js?v=20261106"></script></body>'), 1)
                for antigo in ('cartaz-indices.css', 'cartaz-m4-piloto', 'data-m4-piloto', 'm4-recursos', 'm4-unit-body',
                               'm4-device', 'm4-resource-links', '<span class="cz-fold-t">', 'data-appearance-control'):
                    self.assertNotIn(antigo, s)
                # A palavra do módulo: a mesma da frase lida pelos leitores de ecrã.
                palavra = re.search(r'<span (?:class="agua" aria-hidden="true"|aria-hidden="true" class="agua")>([^<]+)</span>',
                                    main).group(1)
                self.assertIn(f'<span class="vh">A palavra do módulo é {palavra}. </span>', main)
                # Recursos do módulo logo a seguir ao cabeçalho, só com o mapa e a regra.
                recursos = re.search(r'</header><details class="cz-recursos"><summary>Recursos do módulo</summary>'
                                     r'(<div class="mod-sec"><nav class="ligas"><a href="\./mapa-do-modulo-m%d/">Mapa do módulo'
                                     r'</a></nav><details class="regra">.*?</details></div>)</details>' % n, main, re.S)
                self.assertIsNotNone(recursos)
                self.assertNotIn('<figure', recursos.group(1))
                self.assertNotIn('teacher-access', recursos.group(1))
                # Cada unidade: banda com o <h2> e a âncora; corpo com a pergunta e a prova, depois o percurso.
                units = json.JSONDecoder().raw_decode(s.split('var U=', 1)[1])[0]
                secoes = re.findall(r'<section\b[^>]*class="unidade-pedagogica".*?</section></div></details></section>', main, re.S)
                self.assertEqual(len(secoes), len(units))
                for k, sec in enumerate(secoes, 1):
                    self.assertRegex(sec, r'<summary><span class="cz-fold-k">Unidade %d</span><h2 class="cz-fold-t" '
                                          r'id="unidade-pedagogica-%d">[^<]*(?:<em>[^<]*</em>[^<]*)*</h2><span class="cz-index-fold-state">'
                                          r'</span></summary><div class="cz-unit-body"><header class="grupo-topo"><p class="grupo-etq">'
                                          r'[^<]*</p><p class="grupo-pergunta">[^<]*</p><p class="prova-esperada">.*?</p></header>'
                                          r'<section class="unidade" data-u="%d">' % (k, k, k))
                    self.assertTrue(sec.endswith('</section></div></details></section>'))
                    self.assertEqual(sec.count('<h2'), 1)
                # A imagem documental: uma, fora de qualquer details, logo a seguir à última unidade.
                self.assertEqual(main.count('<figure class="doc">'), 1)
                fim = main.rindex('</section></div></details></section>') + len('</section></div></details></section>')
                self.assertTrue(main[fim:].startswith('<figure class="doc">'), main[fim:fim + 80])
                # 07/11/2026: o crédito da imagem passa para trás de um «i» (camada creditos_i_pt1_20261107, por cima desta, que
                # tests/test_creditos_i_pt1.py confere); a imagem documental desta camada confere-se como antes, letra a letra, na
                # página com essa camada desfeita.
                antes_pt1 = undo_creditos_i_pt1_0711(rel, s)
                main_pt1 = antes_pt1[antes_pt1.index('<main'):antes_pt1.index('</main>')]
                fim_pt1 = main_pt1.rindex('</section></div></details></section>') + len('</section></div></details></section>')
                self.assertRegex(main_pt1[fim_pt1:], r'^<figure class="doc">.*?<figcaption class="cz-credit">.*?'
                                                     r'(Domínio público|CC BY-SA 2\.0)\.</figcaption></figure>')
                # O acesso do docente flutua, fora do <main>, como sempre: um só, com os quatro materiais.
                # 06/11/2026: decisão 173, no HTML continua fora do <main> (e assim fica sem JavaScript); abaixo de 640 px é
                # cartaz-indice-comum.js que o põe no menu «Recursos do módulo» (ver test_estilos_e_script_comuns).
                fora = s[s.index('</main>'):]
                self.assertEqual(s.count('class="route-teacher-tools"'), 1)
                self.assertEqual(fora.count('<details class="route-teacher-tools"><summary class="teacher-access" '
                                            'aria-label="Abrir materiais do docente" title="Para o docente">'), 1)
                # 07/11/2026: acertos da decisão 173, o lugar flutuante do menu (position:fixed;left:12px;bottom:64px) passou do style
                # do HTML para o CSS comum (ver test_estilos_e_script_comuns e tests/test_indices_acertos_20261107.py).
                self.assertIn('<nav aria-label="Materiais do docente" style="z-index:1001;max-width:calc(100vw - 24px);', fora)
                self.assertNotIn('position:fixed', re.search(r'<nav aria-label="Materiais do docente" style="([^"]*)"', fora).group(1))
                self.assertEqual(len(re.findall(r'<nav aria-label="Materiais do docente".*?</nav>', fora, re.S)[0]
                                     .split('<p><a ')), 5)

    def test_estilos_e_script_comuns(self):
        css = ler('assets/cartaz-indice-comum.css')
        js = ler('assets/cartaz-indice-comum.js')
        self.assertNotIn('!important', css)
        self.assertNotRegex(js, r'(?:localStorage|sessionStorage)|MutationObserver|innerHTML')
        self.assertNotIn('data-m4-piloto', css)
        # A palavra do módulo vê-se (o piloto escondia-a); a frase das unidades também.
        self.assertRegex(css, r'\.cabm>\.agua\{display:block;')
        self.assertNotRegex(css, r'\.agua\{display:none')
        self.assertRegex(css, r'\.unit-index>span\{display:block;')
        # A imagem mais pequena a seguir às unidades: 200 px de altura, com o crédito ao lado (por baixo no telemóvel).
        self.assertIn('>figure.doc img{display:block;height:200px;max-height:200px;', css)
        # Os botões flutuantes de sempre, com 48 px; nenhum lugar para eles dentro dos recursos.
        self.assertIn('body:has(main[data-cz-indice]) .teacher-access{width:48px;height:48px;}', css)
        self.assertNotIn('.cz-recursos .teacher-access', css)
        # 06/11/2026: decisão 173. Abaixo de 640 px, o script muda de sítio os dois botões que já existem (o modo noturno para a
        # barra de cima, nav.migalhas; o acesso do docente para .cz-docente, dentro de «Recursos do módulo») e devolve-os ao
        # sítio de sempre a partir de 640 px, onde voltam a flutuar; o CSS desses lugares é só para o ecrã (a impressão não muda).
        # 06/11/2026: decisão 173, revisão de 6/11: o telemóvel é o que não cumpre (min-width: 640px), o mesmo limite do CSS (com
        # max-width: 639px, 639,2 px a 125 % de zoom não cumpria nenhum dos dois e os botões flutuavam por cima do texto).
        self.assertIn("const desktop = window.matchMedia('(min-width: 640px)');", js)
        self.assertIn('function phone() { return !desktop.matches; }', js)
        self.assertNotIn("matchMedia('(max-width", js)
        self.assertIn("bar.appendChild(slot)", js)
        self.assertIn("slot.setAttribute('data-appearance-floating', '')", js)
        self.assertIn("holder.className = 'cz-docente'", js)
        self.assertIn('resources.appendChild(holder)', js)
        # 06/11/2026: decisão 173, revisão de 6/11: limites que se completam no CSS (sem max-width:639px, 359px nem 1279px, que
        # deixavam sem regra as larguras fracionárias do zoom); as regras do ecrã abaixo de 640 px ficam dentro de @media screen.
        self.assertIn('@media screen{\n@media not all and (min-width:640px){\n', css)
        self.assertIn('@media screen{\n@media not all and (min-width:360px){\n', css)
        self.assertIn('@media not all and (min-width:640px){\nbody.pt-module-layout main.cz-index[data-cz-indice]{padding:24px 16px 48px;}', css)
        self.assertIn('@media not all and (min-width:360px){\nbody.pt-module-layout main.cz-index[data-cz-indice] .cz-fold>summary{padding:.5rem 0;}', css)
        self.assertIn('@media (min-width:640px){\n@media not all and (min-width:1280px){\nbody.pt-module-layout main.cz-index[data-cz-indice]{padding-inline:72px;}', css)
        self.assertNotRegex(css, r'@media[^{]*max-width:\s*(?:639|359|1279)(?:\.\d+)?px')
        # 06/11/2026: decisão 173, revisão de 6/11: em projeção, abaixo de 880 px, «Neste módulo» com três unidades numa unidade por
        # linha (em três colunas, «leitura/preparação,» saía da coluna e passava por baixo do modo noturno, no M4 e no M7); fora
        # da projeção, o mesmo abaixo de 720 px («Heterónimos:» saía da segunda coluna do M7).
        self.assertIn('@media not all and (min-width:720px){\nbody.pt-module-layout main.cz-index[data-cz-indice] .unit-index '
                      'ol:has(>li:nth-child(3)){grid-auto-flow:row;grid-template-columns:1fr;gap:0;}', css)
        self.assertIn('@media not all and (min-width:880px){\nhtml:has(main[data-cz-indice].cz-sala) body.pt-module-layout '
                      'main.cz-index[data-cz-indice] .unit-index ol:has(>li:nth-child(3)){grid-auto-flow:row;'
                      'grid-template-columns:1fr;gap:0;}', css)
        # 06/11/2026: decisão 173, revisão de 6/11: cada { tem o seu } (as regras novas estão aninhadas em @media).
        self.assertEqual(css.count('{'), css.count('}'))
        self.assertIn('body:has(main[data-cz-indice]) nav.migalhas>[data-appearance-control]>.epi-appearance-toggle{width:48px;'
                      'height:48px;min-width:48px;min-height:48px;margin:0;border-color:transparent;}', css)
        self.assertIn('@media screen{\n/* 06/11/2026: decisão 173, o acesso do docente dentro dos recursos', css)
        self.assertIn('main.cz-index[data-cz-indice] .cz-docente summary.teacher-access{position:relative;', css)
        # 07/11/2026: acertos da decisão 173, o lugar flutuante do menu dos materiais no fim do <body> (era o style do HTML) e,
        # sem JavaScript abaixo de 640 px, o menu no fluxo.
        self.assertIn('body:has(main[data-cz-indice])>details.route-teacher-tools>summary.teacher-access+nav{position:fixed;left:12px;'
                      'bottom:64px;}', css)
        self.assertIn('body:has(main[data-cz-indice])>details.route-teacher-tools>summary.teacher-access+nav{position:static;}', css)
        self.assertNotIn('m4-device', css)
        # A camada do piloto continua a poder desfazer-se: os ficheiros dele ficam como estavam.
        self.assertTrue((ROOT / 'assets/cartaz-m4-piloto.css').is_file())
        self.assertTrue((ROOT / 'assets/cartaz-indices.css').is_file())


if __name__ == '__main__':
    unittest.main()
