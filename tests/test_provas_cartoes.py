"""Provas em cartões (exame/provas/): piloto de 29/10/2026 (Prova 639, 1.ª fase, 2026, versão 2); um caso por prova desde
30/10/2026.

Pedido do docente: os exames passam a lições em cartões, uma por grupo da prova; os itens de resposta escrita
desmontam-se em cartões e a resposta completa escreve-se no caderno, com a grelha à vista. Cada transcrição conferida
tests/fixtures/prova-639-AAAA-Nf-vN.json é um caso (tests/provas_casos.py) e dá uma classe de testes, que confere, sem
navegador, que:
- os três grupos passam em validate_cards (o tipo «item», os itens de escolha múltipla com as quatro opções da prova,
  valida-se como «escolha») e usam só os campos do motor;
- o texto da prova (linhas numeradas, versos, notas) é igual à transcrição, e cada item da prova tem o seu enunciado e
  cartões de preparação;
- as chaves de escolha múltipla são as da versão da prova, iguais no quadro dos critérios, no resumo dos itens e nos cartões;
- cada lição cita a fonte (prova, fase, ano, versão, IAVE, as cópias públicas e as fontes dos textos);
- não há código da Sala de aula nem chaves que choquem com as das lições;
- o texto que escrevemos (fora do texto da prova e dos critérios) cumpre as regras de escrita;
- a ordem dos cartões (revisão de 29/10): nos itens de resposta escrita, os exemplos completos e os tópicos dos critérios
  só depois do cartão «Escreve no caderno»; nos itens de escolha, o item da prova antes dos cartões «Porquê?»; o que
  adaptamos diz «adaptado»; o feedback das escolhas não aponta opções pela posição (o motor baralha-as);
- as opções das escolhas nossas têm comprimentos semelhantes (regra do docente de 29 e 30/10/2026, com a medição única do
  sítio, scripts/opcoes_equilibradas.py, por scripts/provas/opcoes.py): as provas feitas depois da regra cumprem-na, e as
  de antes têm uma catraca em prova.json que não pode subir;
- nenhuma página da prova reproduz uma imagem fora dos créditos e licenças dos parâmetros;
- o negrito e o itálico dos dados cabem no que o motor mostra (sem marcas cruas).
30/10/2026: nenhum teste saltado (regra do docente).
A classe SeccaoEGerador confere a secção (um bloco por prova, a mais recente primeiro, ids únicos, um nome próprio por bloco,
«O que vem a seguir»), as ligações a partir de /exame/, a medição única das opções e que scripts/provas/gerar.py dá, byte a
byte, as páginas que estão na árvore.
O percurso no navegador está em tests/browser_provas_cartoes.py.
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provas_casos import (DADOS, PROVAS, ROMANOS, ROOT, SECCAO, imagem_do_grupo, itens_do_grupo, plano,  # noqa: E402
                          textos, textos_do_grupo)
from audit_cards import TYPES, lesson_cards, validate_cards  # noqa: E402

sys.path.insert(0, str(ROOT / 'scripts/provas'))
import opcoes  # noqa: E402
from auditar_aquecimentos_m1 import auditar as auditar_aquecimentos  # noqa: E402

ASSETS = [ROOT / 'assets/exame/provas-licao.js', ROOT / 'assets/exame/provas-licao.css',
          ROOT / 'assets/exame/provas.js', ROOT / 'assets/exame/provas.css']
# Campos que o motor (jogo.js e rever-frase.js) e o tipo «item» (assets/exame/provas-licao.js) leem.
CAMPOS = {'t', 'rot', 'titulo', 'html', 'escuro', 'p', 'p2', 'o', 'c', 'f', 'fe', 'cita', 'l', 'g', 'v', 'pares',
          'frase', 'lacunas', 'passos', 'linhas', 'palavras', 'certas', 'apoio', 'trecho', 'liga', 'ver', 'voc'}
# Rótulo dos cartões com o item tal como está na prova; o que está adaptado ao ecrã diz «adaptado» e lê-se como texto nosso.
OFICIAL = re.compile(r'\bItem \d+ da prova\b(?! \(adaptado)')
PALAVRAS_PROIBIDAS = re.compile(r'—|–|‒|·|\bprofessor|\bjog|\bficha|\bfolha', re.I)
SALA = ('ntfy', 'EventSource', 'BroadcastChannel', 'EPISala', 'aoEvento', 'enviarSala', 'data-sala', 'epi-sala',
        'painel-sala-', 'id="liga-sala"', '<div class="sala"', 'data-fechar-sala', 'Código da sala', 'id="faixa-pausa"',
        'id="sobre"', 'sala-cod', 'data-placar', 'Nova sala')
SEM_DATAS = re.compile(r'\b(19|20)\d\d-\d\d|\b\d{1,2}/\d{1,2}/20\d\d|janeiro|fevereiro|março|abril|maio|junho|julho|agosto|'
                       r'setembro|outubro|novembro|dezembro')


def ler(p):
    return p.read_text('utf-8')


def linha_html(s):
    """Uma linha dos dados no formato das lições: _x_ em <i>, [^n] em <sup>n</sup>."""
    import html
    s = html.escape(s, quote=False)
    s = re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'<i>\1</i>', s)
    return re.sub(r'\[\^(\d+)\]', r'<sup>\1</sup>', s)


def linhas_na_licao(cards, atributo='data-l'):
    """(data-l, número do span.n, HTML da linha só com <i> e <sup>) de cada span.ln com data-l; com atributo='data-n', as
    linhas dos excertos repetidos (sem data-l), com o número que o gerador lhes dá."""
    out = []
    for c in cards:
        if c['t'] != 'ler':
            continue
        for m in re.finditer(r'<span class="ln(?: par)?(?: salto)?" ' + atributo + r'="([^"]+)"><span class="n" aria-hidden="true">(\d*)</span>(.*?)</span>(?=<span class="ln|</div>)', c.get('html', '')):
            corpo = re.sub(r'<(?!/?(?:i|sup)>)[^>]+>', '', m.group(3))
            out.append((m.group(1), m.group(2), corpo))
    return out


def sem_oficial(h):
    """O HTML de um cartão «ler» sem os blocos que reproduzem a prova ou os critérios (conferidos noutros testes)."""
    for padrao in (r'<div class="v prova-l[^"]*">.*?</div>', r'<p class="gl">.*?</p>', r'<p class="papel-q">.*?</p>',
                   r'<table class="(?:empilha grelha|cl)">.*?</table>', r'<ul class="(?:prova-lista|papel-l)">.*?</ul>',
                   r'<ol class="prova-obs">.*?</ol>'):
        h = re.sub(padrao, ' ', h, flags=re.S)
    return h


def segmentos(h):
    """O HTML partido nos blocos (parágrafos, itens de lista, células, quebras): cada bloco lê-se sozinho."""
    return [x for x in re.split(r'<(?:/?(?:p|li|ul|ol|td|th|tr|table|div|details|summary|h\d)\b[^>]*|br\s*/?)>', h) if x.strip()]


def imagens_reproduzidas(s):
    """O que uma página mostra como imagem: o nome do ficheiro de cada <img>, <image>, <source>, url(…) e caminho de imagem
    (também dentro dos dados dos cartões), «data:» para as imagens embutidas e «<svg>» para um desenho em linha que não seja
    um ícone decorativo (aria-hidden)."""
    s = s.replace('\\"', '"').replace('<\\/', '</')
    refs = (re.findall(r'<img\b[^>]*?\bsrc="([^"]*)"', s) + re.findall(r'<image\b[^>]*?\b(?:xlink:)?href="([^"]*)"', s)
            + [x.split()[0] for x in re.findall(r'\bsrcset="([^"]*)"', s) if x.strip()]
            + re.findall(r'url\(\s*[\'"]?([^\'")]+)', s) + re.findall(r'[\w./%-]+\.(?:jpe?g|png|gif|webp|avif|bmp|tiff?)\b', s, re.I))
    nomes = {'data:' if r.startswith('data:') else Path(r.split('?')[0].split('#')[0]).name for r in refs}
    if any('aria-hidden="true"' not in svg for svg in re.findall(r'<svg\b[^>]*>', s)):
        nomes.add('<svg>')
    if re.search(r'<(?:picture|canvas|video)\b', s):
        nomes.add('<picture, canvas ou video>')
    return nomes


def eh_selecao(item):
    return item['tipo'].startswith('seleção')


def eh_extensa(item):
    return item['tipo'].startswith('construção: resposta extensa')


def eh_restrita(item):
    return item['tipo'].startswith('construção') and not eh_extensa(item)


def rot_do_item(n):
    return re.compile(rf'^Item {n} da prova\b')


class CasoDeProva:
    """Os testes de uma prova (self.P, um caso de provas_casos). Cada fixture dá uma subclasse com unittest.TestCase."""
    P = None

    def fora_das_regras(self, trecho):
        """As marcas proibidas que sobram num bloco, salvo quando o bloco inteiro é da prova ou dos critérios."""
        if self.P.oficial(trecho):
            return []
        return PALAVRAS_PROIBIDAS.findall(self.P.nosso(trecho))

    def test_ha_dados_do_gerador_e_paginas(self):
        P = self.P
        self.assertIsNotNone(P.cfg, f'falta scripts/provas/dados/{P.pasta}/prova.json')
        self.assertEqual((str(P.cfg['prova']), P.cfg['ano'], P.cfg['fase'], P.cfg['versao']), (P.codigo, P.ano, P.fase, P.versao))
        meta = P.fx['prova']
        self.assertEqual((meta['codigo'], meta['ano'], meta['versao']), (P.codigo, P.ano, P.versao))
        self.assertTrue(meta['fase'].startswith(f'{P.fase}.ª'), meta['fase'])
        self.assertEqual(len(P.grupos), 3)
        for g, p in P.paginas.items():
            self.assertTrue(p.is_file(), p)

    def test_os_tres_grupos_passam_em_validate_cards_com_os_campos_do_motor(self):
        for g, gfx in enumerate(self.P.fx['grupos'], 1):
            cards = self.P.cartoes(g)
            quatro = {i['n'] for i, _ in itens_do_grupo(gfx) if isinstance(i.get('opcoes'), list) and i['opcoes']
                      and isinstance(i['opcoes'][0], dict) and [o.get('letra') for o in i['opcoes']] == list('ABCD')}
            with self.subTest(grupo=g):
                self.assertGreaterEqual(len(cards), 40)
                self.assertEqual(validate_cards([dict(c, t='escolha') if c.get('t') == 'item' else c for c in cards]), [])
                for k, c in enumerate(cards):
                    self.assertIn(c['t'], TYPES | {'item'}, k)
                    self.assertLessEqual(set(c), CAMPOS, (k, set(c) - CAMPOS))
                    if c['t'] == 'item':
                        self.assertIn(int(c['g'][:-1]), quatro, (k, 'o tipo «item» só para os itens de quatro opções'))
                        self.assertEqual(len(c['o']), 4, k)
                        self.assertNotIn('p2', c)
                fazer = [c for c in cards if c['t'] != 'ler']
                self.assertGreaterEqual(len(fazer), 3 * len([c for c in cards if c['t'] == 'ler']) // 2)
                gs = [c.get('g') for c in fazer]
                self.assertEqual(len(gs), len(set(gs)), 'cada cartão de fazer tem o seu g, para a ordem da prova')
                self.assertNotIn(None, gs)

    def test_paginas_usam_o_motor_sem_a_sala_e_com_chaves_proprias(self):
        P = self.P
        chaves = set()
        for g, slug in P.grupos.items():
            s = ler(P.paginas[g])
            with self.subTest(grupo=g):
                m = re.search(r'var K="([^"]+)",CARTOES=', s)
                self.assertIsNotNone(m)
                self.assertEqual(m.group(1), P.chave(g))
                chaves.add(m.group(1))
                for marca in ('variar:false', f'versao:"{P.versao_licao(g)}"', f'percurso:"../../#prova-{P.pasta}"',
                              'percursoRotulo:"Provas em cartões"', 'assets/pt-lessons/jogo.js?v=',
                              'assets/pt-lessons/casca.js', 'assets/exame/provas-licao.js?v=', 'assets/exame/provas-licao.css?v=',
                              '<style id="casca-pc">', '<style id="amp-css">', '<script id="amp-js">'):
                    self.assertIn(marca, s)
                for marca in ('epi-ultima', 'K+"-a1"', 'pistas:', 'data-unit-return', 'CARTAZ_DADOS', 'atlasEstado',
                              'abrirExtra'):
                    self.assertNotIn(marca, s)
                self.assertEqual(s.count('assets/pt-lessons/rever-frase.js'), 1 if any(c['t'] == 'rever' for c in P.cartoes(g)) else 0)
                if g < len(P.grupos):
                    self.assertIn(f'seguinte:"../{P.grupos[g + 1]}/",seguinteRotulo:"Grupo {ROMANOS[g]}"', s)
                else:
                    self.assertIn('voltarRotulo:"Voltar às provas"', s)
                self.assertIn(f'<title>{P.nome}: Grupo {ROMANOS[g - 1]}</title>', s)
                self.assertIn('<b>Aprendes:</b>', s)
        self.assertEqual(len(chaves), 3)
        for p in ROOT.glob('m[1-9]/licao-*/index.html'):
            self.assertNotIn(f'prova-{P.pasta}-g', ler(p))

    def test_nenhum_codigo_da_sala(self):
        for p in list(self.P.paginas.values()) + [SECCAO] + ASSETS:
            s = ler(p)
            for marca in SALA:
                self.assertNotIn(marca, s, f'{p.relative_to(ROOT)}: {marca}')
            self.assertIsNone(re.search(r'<button\b[^>]*>\s*Sala\b', s), p)

    def test_texto_da_prova_igual_a_transcricao(self):
        P = self.P
        esperado = P.linhas_da_prova()
        self.assertTrue(esperado, 'nenhum grupo com texto numerado')
        for g, linhas in esperado.items():
            vistas = {}
            for dl, n, corpo in linhas_na_licao(P.cartoes(g)):
                with self.subTest(grupo=g, linha=dl):
                    self.assertNotIn(dl, vistas, 'cada linha da prova aparece numerada uma só vez')
                    self.assertIn(dl, linhas, 'data-l que não é uma linha da prova')
                    self.assertEqual(corpo, linha_html(linhas[dl]))
                    numero = int(re.search(r'(\d+)$', dl).group(1))
                    self.assertEqual(n, str(numero) if numero % 5 == 0 else '')
                    vistas[dl] = corpo
            self.assertEqual(set(vistas), set(linhas), f'grupo {g}: linhas em falta')
            # os excertos repetidos (sem data-l): cada linha é a linha da prova com o número que mostra (data-n)
            prosa = {}
            for t in textos_do_grupo(P.fx['grupos'][g - 1]):
                for linha in t.get('linhas', []):
                    prosa.setdefault(str(linha['n']), []).append(linha_html(linha['t']))
            for dn, _, corpo in linhas_na_licao(P.cartoes(g), 'data-n'):
                with self.subTest(grupo=g, excerto=dn):
                    self.assertIn(corpo, prosa.get(dn, []), 'a linha do excerto não é a linha da prova com este número')
        # notas: o texto exato de cada nota da prova
        for g, gfx in enumerate(P.fx['grupos'], 1):
            notas = list(gfx.get('notas', [])) + [n for p in gfx.get('partes', []) for n in p.get('notas', [])]
            gl = ' '.join(plano(m) for c in P.cartoes(g) if c['t'] == 'ler' for m in re.findall(r'<p class="gl">(.*?)</p>', c['html'], re.S))
            for nota in notas:
                self.assertIn(plano(nota['texto']), gl, (g, nota['n']))

    def test_prosa_numerada_sem_linhas_coladas(self):
        """Prosa da prova em texto corrido (30/10/2026): cada linha da prosa tem o número à vista (data-l, ou data-n nos
        excertos repetidos), e uma linha que não segue a anterior tem a classe «salto» (começa numa linha nova do ecrã)."""
        linha = re.compile(r'<span class="(ln(?: par)?(?: salto)?)"(?: data-l="([^"]+)")?(?: data-n="(\d+)")?><span class="n"')
        prefixos = (self.P.cfg or {}).get('prefixos_data_l', {})
        for g in self.P.grupos:
            # 30/10/2026 (revisão técnica): cada linha começa parágrafo (classe «par») se e só se a transcrição o diz:
            # início de parágrafo, nome da personagem ou início de fala
            par_l, par_n = {}, {}
            for t in textos_do_grupo(self.P.fx['grupos'][g - 1]):
                for x in t.get('linhas', []):
                    v = bool(x.get('inicio_paragrafo') or x.get('personagem') or x.get('inicio_fala'))
                    par_l[prefixos.get(t.get('id'), '') + str(x['n'])] = v
                    par_n[str(x['n'])] = v if par_n.get(str(x['n']), v) == v else None
            for k, c in enumerate(self.P.cartoes(g), 1):
                if c['t'] != 'ler':
                    continue
                for bloco in re.findall(r'<div class="v prova-l">(.*?)</div>', c.get('html', ''), re.S):
                    anterior = None
                    for m in linha.finditer(bloco):
                        classe, dl, dn = m.groups()
                        with self.subTest(grupo=g, cartao=k, linha=dl or dn):
                            self.assertTrue(dl or dn, 'linha da prosa sem número')
                            n = int(re.search(r'(\d+)$', dl or dn).group(1))
                            seguida = anterior is None or n == anterior + 1
                            self.assertEqual('salto' in classe, not seguida, f'linha {n} depois da {anterior}')
                            esperado = par_l.get(dl) if dl else par_n.get(dn)
                            self.assertIsNotNone(esperado, 'linha da prosa que não está na transcrição')
                            self.assertEqual(' par' in classe, esperado, f'linha {n}: o início de parágrafo não bate com a transcrição')
                        anterior = n

    def test_cada_item_da_prova_tem_o_enunciado_e_cartoes(self):
        P = self.P
        for g, gfx in enumerate(P.fx['grupos'], 1):
            cards = P.cartoes(g)
            tudo = plano(' '.join(json.dumps(c, ensure_ascii=False) for c in cards).replace('\\"', '"'))
            for item, _ in itens_do_grupo(gfx):
                with self.subTest(grupo=g, item=item['numero']):
                    if eh_extensa(item):
                        prova = [c for c in cards if c['t'] == 'ler' and c.get('rot') == 'A prova']
                        caderno = [c for c in cards if c['t'] == 'ler' and c.get('rot') == 'Escreve no caderno']
                        self.assertEqual((len(prova), len(caderno)), (1, 1))
                        for c in prova + caderno:
                            texto = plano(c['html'])
                            for frase in item['enunciado'] + item.get('enunciado_lista', []):
                                self.assertIn(plano(frase), texto)
                        self.assertIn('<table class="empilha grelha">', caderno[0]['html'])
                        self.assertGreaterEqual(len([c for c in cards if c['t'] != 'ler']), 30)
                        continue
                    n = item['n']
                    self.assertIn(plano(item['enunciado'][0]), tudo)
                    if eh_restrita(item):
                        prep = [c for c in cards if c['t'] != 'ler' and str(c.get('g', '')).startswith(str(n))]
                        self.assertGreaterEqual(len(prep), 4)
                        caderno = [c for c in cards if c['t'] == 'ler' and c.get('rot') == 'Escreve no caderno'
                                   and (c['titulo'].startswith(f'Item {n} ') or c['titulo'] == f'Item {n}')]
                        self.assertEqual(len(caderno), 1)
                        papel = plano(re.search(r'<p class="papel-q">(.*?)</p>', caderno[0]['html'], re.S).group(1))
                        for frase in item['enunciado']:
                            self.assertIn(plano(frase), papel)
                        self.assertIn('<table class="empilha grelha">', caderno[0]['html'], 'a grelha oficial à vista')
                        self.assertIn('<table class="cl">', caderno[0]['html'])
                    elif eh_selecao(item):
                        prep = [c for c in cards if c['t'] not in ('ler', 'item') and str(c.get('g', '')).startswith(str(n))
                                and not rot_do_item(n).search(c.get('rot', ''))]
                        self.assertGreaterEqual(len(prep), 2)
                        da_prova = [c for c in cards if rot_do_item(n).search(c.get('rot', ''))]
                        self.assertTrue(da_prova, 'o item da prova tem um cartão com o rótulo «Item n da prova»')
                        if any(c['t'] == 'item' for c in da_prova):
                            oficial_ = [c for c in cards if c['t'] == 'item' and c['g'] == f'{n}i']
                            self.assertEqual(len(oficial_), 1)
                            self.assertEqual(plano(oficial_[0]['p']), plano(' '.join(item['enunciado'])))
                            self.assertEqual(oficial_[0]['rot'].endswith('✱'), item['obrigatorio'])
                    else:
                        self.fail(f'tipo de item sem conferência: {item["tipo"]}')

    def test_exemplos_e_topicos_so_depois_da_escrita(self):
        """Nos itens de resposta escrita, a resposta completa de exemplo e os tópicos dos critérios vêm depois do caderno."""
        P = self.P
        for g, gfx in enumerate(P.fx['grupos'], 1):
            cards = P.cartoes(g)
            for item, textos_ao_alcance in itens_do_grupo(gfx):
                if eh_restrita(item):
                    n = item['n']
                    with self.subTest(grupo=g, item=n):
                        titulo = f'Item {n} ✱' if item['obrigatorio'] else f'Item {n}'
                        k_cad = next(k for k, c in enumerate(cards) if c['t'] == 'ler' and c.get('titulo') == titulo)
                        cad = cards[k_cad]['html']
                        self.assertNotIn('Tópicos de resposta', cad)
                        self.assertNotIn('Confere a tua resposta', cad)
                        self.assertIn('<summary>A grelha oficial, tal como está nos critérios</summary>', cad)
                        self.assertIn('leitura nossa da grelha', cad)
                        if textos_ao_alcance:
                            self.assertIn('<summary>As linhas do item</summary>', cad)
                            k_cmp = [k for k, c in enumerate(cards) if c.get('rot') == 'Compara a tua resposta' and str(c.get('g', '')).startswith(str(n))]
                            self.assertEqual(k_cmp, [k_cad + 1], 'as respostas de exemplo logo depois do caderno')
                        k_conf = next(k for k, c in enumerate(cards) if c['t'] == 'ler' and c.get('rot') == 'Confere com os critérios'
                                      and c['titulo'].startswith(f'Item {n}:'))
                        self.assertGreater(k_conf, k_cad)
                        self.assertIn('Tópicos de resposta dos critérios', cards[k_conf]['html'])
                elif eh_extensa(item):
                    with self.subTest(grupo=g, item=item['numero']):
                        k_cad = next(k for k, c in enumerate(cards) if c.get('rot') == 'Escreve no caderno')
                        k_auto = next(k for k, c in enumerate(cards) if c.get('rot') == 'Revê com a grelha')
                        k_ex = next(k for k, c in enumerate(cards) if c.get('rot') == 'Compara com um exemplo')
                        self.assertLess(k_cad, k_auto)
                        self.assertEqual(k_ex, k_auto + 1)
                        self.assertNotIn('Um exemplo nosso', cards[k_cad]['html'])
                        self.assertFalse([c for c in cards[:k_cad] if 'Escreve no caderno' in (c.get('f') or '') and 'Um exemplo nosso' in (c.get('f') or '')])

    def test_itens_de_escolha_antes_dos_cartoes_porque(self):
        """O item da prova vem logo a seguir ao texto (tenta-se sozinho); os cartões que desmentem as opções vêm depois."""
        P = self.P
        for g, gfx in enumerate(P.fx['grupos'], 1):
            cards = P.cartoes(g)
            pos = {c.get('g'): k for k, c in enumerate(cards) if c.get('g')}
            selecao = [i for i, _ in itens_do_grupo(gfx) if eh_selecao(i)]
            com_porque = 0
            for item in selecao:
                n = str(item['n'])
                oficiais = [c['g'] for c in cards if rot_do_item(n).search(c.get('rot', ''))]
                porques = [c['g'] for c in cards if c.get('rot', '').startswith('Porquê?') and c['g'].startswith(n)]
                with self.subTest(grupo=g, item=n):
                    self.assertTrue(oficiais)
                    if porques:
                        com_porque += 1
                        self.assertLess(max(pos[o] for o in oficiais), min(pos[p] for p in porques))
            if selecao:
                self.assertGreaterEqual(com_porque, 1, f'grupo {g}: nenhum item de seleção com cartões «Porquê?»')
            for c in cards:
                if c.get('rot', '').startswith('Porquê?'):
                    for t in textos({k: c.get(k) for k in ('p', 'p2', 'f', 'fe')}):
                        self.assertNotRegex(t, r'Lembra-te|te pede que verifiques|Repara em que coluna')

    def test_feedback_das_escolhas_nao_aponta_posicoes(self):
        """O motor baralha as opções das escolhas: o feedback nomeia-as pelo conteúdo, nunca por «a primeira» ou «a segunda»."""
        for g in self.P.grupos:
            for k, c in enumerate(self.P.cartoes(g)):
                if c['t'] != 'escolha':
                    continue
                for t in textos({'f': c.get('f'), 'fe': c.get('fe')}):
                    with self.subTest(grupo=g, cartao=k + 1):
                        self.assertNotRegex(t, r'\*\*(A|O) (primeir|segund|terceir)[oa]\b|\b(A|O) (segund|terceir)[oa] (já|tem|é)\b|\bAs outras\b')

    def test_chaves_de_escolha_multipla_batem_com_os_criterios(self):
        P = self.P
        campo = f'chave_versao_{P.versao}'
        resumo = {r['item']: r for r in P.fx.get('resumo_itens', [])}
        for g, gfx in enumerate(P.fx['grupos'], 1):
            cards = P.cartoes(g)
            quadro = gfx.get('chaves_criterios_quadro')
            col = quadro['cabecalho'].index(f'VERSÃO {P.versao}') if quadro else None
            for item, _ in itens_do_grupo(gfx):
                if not eh_selecao(item):
                    continue
                n = item['n']
                with self.subTest(item=item['numero']):
                    chave = item.get(campo)
                    self.assertTrue(chave, f'{item["numero"]}: falta {campo} na transcrição')
                    if item['numero'] in resumo:
                        self.assertEqual(resumo[item['numero']].get(campo), chave, 'o resumo dos itens diz outra chave')
                    opcoes = item['opcoes']
                    if isinstance(opcoes, list) and opcoes and isinstance(opcoes[0], dict) and 'letra' in opcoes[0]:
                        if quadro:
                            linha = next(r for r in quadro['linhas'] if r[0] == f'{n}.')
                            self.assertEqual(linha[col], f'({chave})', 'o quadro das chaves dos critérios diz outra')
                        c = next(x for x in cards if x['t'] == 'item' and x['g'] == f'{n}i')
                        self.assertEqual([o['letra'] for o in opcoes], list('ABCD'))
                        self.assertEqual([plano(o) for o in c['o']], [plano(o['texto']) for o in opcoes])
                        self.assertEqual(c['c'], 'ABCD'.index(chave))
                        self.assertIsNone(c['fe'][c['c']])
                    elif isinstance(opcoes, dict):  # completamento: uma opção por espaço
                        for espaco, ch in chave.items():
                            c = next(x for x in cards if x.get('rot') == f'Item {n} da prova, espaço ({espaco})')
                            self.assertEqual(c['t'], 'escolha')
                            self.assertEqual(sorted(plano(o) for o in c['o']), sorted(plano(f'({o["n"]}) {o["texto"]}') for o in opcoes[espaco]))
                            self.assertTrue(c['o'][c['c']].startswith(f'({ch}) '))
                    elif isinstance(opcoes, list) and isinstance(chave, list):  # escolher várias afirmações
                        c = next(x for x in cards if rot_do_item(n).search(x.get('rot', '')))
                        self.assertEqual(c['t'], 'emparelhar')
                        # formato adaptado ao ecrã (duas colunas nossas): o rótulo e o feedback dizem-no
                        self.assertEqual(c['rot'], f'Item {n} da prova (adaptado ao ecrã)')
                        self.assertIn('adaptado ao ecrã', c['f'])
                        colunas = {}
                        for afirmacao, coluna in c['pares']:
                            colunas.setdefault(coluna, set()).add(afirmacao.split('.', 1)[0])
                        self.assertEqual(len(colunas), 2)
                        certas = [v for k, v in colunas.items() if not k.startswith('não')]
                        self.assertEqual(certas, [set(chave)])
                        for o in opcoes:
                            self.assertIn(plano(f'{o["n"]}. {o["texto"]}'), [plano(a) for a, _ in c['pares']])
                    else:
                        self.fail(f'{item["numero"]}: item de seleção sem conferência da chave ({item["tipo"]}); acrescenta-a aqui')

    def test_cada_licao_cita_a_fonte(self):
        P = self.P
        marcas = [f'Prova {P.codigo}', f'{P.fase}.ª fase, {P.ano}', f'versão {P.versao}', 'IAVE']
        if P.autor_nao_iave():
            marcas.append(P.autor_nao_iave())
        for g, gfx in enumerate(P.fx['grupos'], 1):
            s = ler(P.paginas[g])
            menu = plano(re.search(r'<div class="casca-menu".*?</div></div>', s, re.S).group(0))
            fontes = [t['fonte'] for t in textos_do_grupo(gfx)]
            if imagem_do_grupo(gfx):
                fontes.append(imagem_do_grupo(gfx)['fonte'])
            with self.subTest(grupo=g):
                sem_texto = P.cfg['grupos'][g - 1].get('sem_texto_da_prova', False)
                if not fontes:
                    # um grupo sem texto nem imagem da prova (o Grupo III de 2026-2f, um texto de opinião só com o
                    # enunciado) declara-se em prova.json (revisão técnica de 30/10/2026: antes, um grupo que perdesse o
                    # texto na transcrição passava calado); o menu cita a prova e não inventa a fonte de um texto
                    self.assertTrue(sem_texto, f'grupo {g}: sem texto nem imagem da prova; se a prova é assim, põe '
                                    '«sem_texto_da_prova»: true no grupo, em prova.json')
                    self.assertTrue(all(eh_extensa(i) for i, _ in itens_do_grupo(gfx)), 'só um grupo de escrita extensa fica sem texto')
                    self.assertNotRegex(menu, r'como a prova [oa]s? indica')
                else:
                    self.assertFalse(sem_texto, f'grupo {g}: tem texto ou imagem da prova, mas prova.json diz «sem_texto_da_prova»')
                for marca in marcas:
                    self.assertIn(marca, menu)
                for url in (P.url_enunciado, P.url_criterios):
                    self.assertIn(f'href="{url}"', s)
                for f in fontes:
                    self.assertIn(plano(f).rstrip('.'), menu)
                abre = P.cartoes(g)[0]
                self.assertEqual(abre.get('rot'), 'Abre')
                self.assertIn('IAVE', abre['html'])
                self.assertIn(f'versão {P.versao}', abre['html'])
        s = ler(SECCAO)
        bloco = re.search(rf'<section class="pv-prova" id="prova-{P.pasta}".*?</section>', s, re.S).group(0)
        for marca in [f'{P.nome}, versão {P.versao}', 'IAVE', P.url_enunciado, P.url_criterios] + marcas[4:]:
            self.assertIn(marca, bloco)

    def test_bloco_da_prova_na_seccao(self):
        P = self.P
        s = ler(SECCAO)
        self.assertEqual(s.count(f'id="prova-{P.pasta}"'), 1)
        bloco = re.search(rf'<section class="pv-prova" id="prova-{P.pasta}".*?</section>', s, re.S).group(0)
        self.assertIn(f'<h2 id="pv-{P.pasta}"><span class="pv-quando">{P.ano}, {P.fase}.ª fase</span> ', bloco)
        for g, slug in P.grupos.items():
            versao = re.search(r'versao:"([^"]+)"', ler(P.paginas[g])).group(1)
            self.assertEqual(versao, P.versao_licao(g))
            i = f'pv-{P.pasta}-g{g}'
            m = re.search(rf'<li class="pv-grupo"><a href="{P.pasta}/{slug}/" data-chave="{P.chave(g)}" data-versao="{re.escape(versao)}" '
                          rf'aria-labelledby="{i}-n {i}-t {i}-e">.*?</a></li>', bloco)
            self.assertIsNotNone(m, slug)
            for ident in (f'{i}-n', f'{i}-t', f'{i}-e'):
                self.assertIn(f'id="{ident}"', m.group(0))
            fazer = len([c for c in P.cartoes(g) if c['t'] != 'ler'])
            self.assertIn(f'{len(P.cartoes(g))} cartões, {fazer} para responder.', m.group(0))

    def test_ligacoes_internas_existem(self):
        P = self.P
        sessoes = {x['id'] for x in json.loads(ler(ROOT / 'assets/exame/sessoes.json'))['sessions']}
        ids_seccao = set(re.findall(r'\bid="([^"]+)"', ler(SECCAO)))
        for p in P.paginas.values():
            s = ler(p).replace('\\"', '"').replace('<\\/', '</')
            refs = re.findall(r'(?:href|src)="([^"]+)"', s)
            self.assertTrue(refs)
            for ref in refs:
                if re.match(r'^(https?:|mailto:|data:|#|javascript:)', ref) or '"+' in ref:
                    continue
                caminho, _, ancora = ref.partition('#')
                caminho = caminho.split('?')[0]
                alvo = (p.parent / caminho).resolve() if caminho else p
                if alvo.is_dir():
                    alvo = alvo / 'index.html'
                with self.subTest(pagina=p.relative_to(ROOT).as_posix(), ref=ref):
                    self.assertTrue(alvo.is_file(), alvo)
                    if ancora and alvo == SECCAO:
                        self.assertIn(ancora, ids_seccao)
                    if ancora and alvo == ROOT / 'exame/index.html' and ancora.startswith('s'):
                        self.assertIn(ancora.split('/')[0], sessoes)
        for g in P.grupos:
            for c in P.cartoes(g):
                for l in c.get('liga', []):
                    alvo = (P.paginas[g].parent / l['href'].split('#')[0]).resolve()
                    self.assertTrue((alvo / 'index.html' if alvo.is_dir() else alvo).is_file(), l['href'])

    def test_imagem_com_direitos_so_por_ligacao(self):
        """Uma imagem com direitos (o cartoon do Grupo III em 2026-1f) não se reproduz sem decisão do docente: liga-se ao PDF.
        Em todas as provas, nenhuma página reproduz uma imagem que não esteja nos créditos e licenças dos parâmetros
        («imagens_com_licenca», ou a imagem com direitos que o docente deixou reproduzir)."""
        # 30/10/2026: nenhum teste saltado (regra do docente). Antes, uma prova sem imagem com direitos declarada saltava
        # este teste; agora confere que nenhuma página da prova reproduz uma imagem fora dos créditos dos parâmetros.
        P = self.P
        img = P.imagem()
        licencas = P.cfg.get('imagens_com_licenca', [])
        for x in licencas:
            self.assertTrue(x.get('ficheiro') and x.get('credito') and x.get('licenca'), x)
            self.assertTrue((ROOT / x['ficheiro']).is_file(), x['ficheiro'])
        permitidas = {Path(x['ficheiro']).name for x in licencas}
        if img and img.get('reproduzir'):
            permitidas.add(Path(img['ficheiro']).name)
        bloco = re.search(rf'<section class="pv-prova" id="prova-{P.pasta}".*?</section>', ler(SECCAO), re.S).group(0)
        for onde, s in [(f'grupo {g}', ler(p)) for g, p in P.paginas.items()] + [('bloco da secção', bloco)]:
            with self.subTest(pagina=onde):
                self.assertEqual(imagens_reproduzidas(s) - permitidas, set(), 'imagem sem crédito e licença nos parâmetros')
        if not img:
            for g, gfx in enumerate(P.fx['grupos'], 1):
                self.assertIsNone(imagem_do_grupo(gfx), f'grupo {g}: a transcrição tem uma imagem; declara-a em prova.json («imagem»)')
            return
        g = img['grupo']
        s = ler(P.paginas[g])
        nome = Path(img['ficheiro']).name
        if img.get('reproduzir'):
            self.assertIn(nome, s)
            self.assertTrue((ROOT / img['ficheiro']).is_file())
            return
        self.assertNotIn(nome, s)
        url = f'{P.url_enunciado}#page={img["pagina_pdf"]}'
        vers = [c for c in P.cartoes(g) if 'ver' in c]
        self.assertTrue(vers)
        for c in vers:
            self.assertIn(f'href="{url}"', c['ver'])
            self.assertIn(f'p. {img["pagina_pdf"]} de {img["paginas_pdf"]}', c['ver'])
        self.assertNotIn('<figure class="fig inteiro cor">', s)

    def test_regras_de_escrita_no_texto_nosso(self):
        """«tu», «docente», sem «professor», «jogar», «ficha», «folha», «·» nem travessões no que escrevemos.

        O texto da prova e dos critérios fica como está (tem «folha de respostas», «folha branca» e travessões):
        os blocos que o reproduzem são conferidos com a transcrição noutros testes, e as citações «…» só ficam de
        fora quando são da prova ou dos critérios."""
        P = self.P
        for g in P.grupos:
            for k, c in enumerate(P.cartoes(g)):
                partes = []
                if c['t'] == 'ler':
                    partes += [c.get('titulo', ''), c.get('rot', '')] + segmentos(sem_oficial(c.get('html', '')))
                else:
                    campos = ['f', 'fe', 'cita', 'liga', 'rot']
                    if not OFICIAL.search(c.get('rot', '')):
                        campos += ['p', 'p2', 'o', 'pares', 'passos', 'frase', 'lacunas', 'apoio', 'trecho', 'linhas', 'palavras']
                    else:
                        for campo in ('p', 'o', 'pares'):
                            for t in textos(c.get(campo)):
                                self.assertTrue(P.oficial(re.sub(r'^\(?[IV\d]+[.)]\s*', '', t)) or P.oficial(t.split('\n')[0]) or not PALAVRAS_PROIBIDAS.search(t), (g, k, t))
                    partes += [t for campo in campos for t in textos(c.get(campo))]
                with self.subTest(grupo=g, cartao=k):
                    self.assertEqual([m for p in partes if p for m in self.fora_das_regras(p)], [])
            # a moldura da página: título, menu, fim e avisos
            s = ler(P.paginas[g])
            moldura = re.sub(r'<script>document\.addEventListener.*?</script>', ' ', s, flags=re.S)
            moldura = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', moldura, flags=re.S)
            depois = json.loads(re.search(r'depois:("(?:[^"\\]|\\.)*")', s).group(1))
            with self.subTest(grupo=g, parte='moldura'):
                self.assertEqual([m for p in segmentos(moldura + ' ' + depois) for m in self.fora_das_regras(p)], [])
        bloco = re.search(rf'<section class="pv-prova" id="prova-{P.pasta}".*?</section>', ler(SECCAO), re.S).group(0)
        self.assertEqual([m for p in segmentos(bloco) for m in self.fora_das_regras(p)], [])

    def test_blocos_oficiais_so_tem_texto_da_prova_ou_dos_criterios(self):
        """Os blocos que o teste das regras de escrita deixa de fora têm de ser mesmo da prova ou dos critérios."""
        cabecalhos = {'Nível', 'Descritor de desempenho', 'Pontuação', 'Número de erros do tipo B', 'Número de erros do tipo A',
                      'Parâmetro', 'Tabela da correção linguística', 'OU'}
        for g in self.P.grupos:
            for k, c in enumerate(self.P.cartoes(g)):
                if c['t'] != 'ler':
                    continue
                h = c['html']
                blocos = re.findall(r'<p class="papel-q">(.*?)</p>|<ul class="(?:prova-lista|papel-l)">(.*?)</ul>|<ol class="prova-obs">(.*?)</ol>', h, re.S)
                pedacos = []
                for trio in blocos:
                    for b in trio:
                        pedacos += re.split(r'<br>|</li>|<li>', b)
                for t in re.findall(r'<table class="(?:empilha grelha|cl)">(.*?)</table>', h, re.S):
                    pedacos += re.split(r'</t[dh]>|<br>|<li>|</li>', t)
                for pedaco in pedacos:
                    t = plano(pedaco)
                    t = re.sub(r'^✱\s*', '', t)
                    t = re.sub(r'^\d+\.\s+', '', t)
                    if not t or t.isdigit() or t in cabecalhos or re.fullmatch(r'[\d\sA-Z.,]+', t):
                        continue
                    with self.subTest(grupo=g, cartao=k, texto=t[:60]):
                        self.assertTrue(self.P.oficial(t), t)

    def test_opcoes_equilibradas_nas_escolhas_nossas(self):
        """Regra do docente de 29 e 30/10/2026: opções de comprimento semelhante (no máximo 20 % entre a mais curta e a mais
        longa; a certa nunca 25 % ou mais acima da maior errada; a certa a mais longa, empates incluídos, em não mais de 1 de
        cada k perguntas, para cada k). Medição única do sítio: scripts/opcoes_equilibradas.py."""
        # 30/10/2026: nenhum teste saltado (regra do docente). Antes, as provas feitas antes da regra (2026-1f) saltavam
        # este teste; agora têm uma catraca: prova.json guarda, por grupo, as perguntas com falhas e as vezes em que a certa
        # é a mais longa (opcoes_catraca, de python3 scripts/provas/opcoes.py --catraca), e o teste falha se piorarem. As
        # provas novas (opcoes_equilibradas: true) continuam com zero falhas.
        P = self.P
        antes_da_regra = P.cfg.get('opcoes_equilibradas', True) is False
        catraca = P.cfg.get('opcoes_catraca', {})
        if antes_da_regra:
            self.assertEqual(set(catraca), set(P.grupos.values()), 'opcoes_catraca: os números de cada grupo, em prova.json')
        else:
            self.assertEqual(catraca, {}, 'uma prova feita depois da regra cumpre-a inteira: sem catraca')
        for g, slug in P.grupos.items():
            m = opcoes.medir(P.cartoes(g))
            with self.subTest(grupo=g):
                if antes_da_regra:
                    self.assertEqual(opcoes.dentro_da_catraca(m, catraca[slug]), [], 'as opções pioraram em relação à catraca')
                else:
                    self.assertEqual([(x['cartao'], x['g'], x['falhas']) for x in m['falhas']], [])
                    self.assertFalse(m['mais_longa_acima_do_limite'], f'a certa é a mais longa em demasiadas perguntas: {m["por_k"]}')

    def test_negrito_e_italico_que_o_motor_mostra(self):
        """O motor (it() de jogo.js) só põe **x** em negrito até 80 carateres e _x_ em itálico até 100: acima disso, o aluno
        via as marcas cruas (revisão de 30/10/2026: três explicações do Grupo I de 2026-2f e uma de 2026-1f)."""
        for g in self.P.grupos:
            for k, c in enumerate(self.P.cartoes(g), 1):
                for campo, v in c.items():
                    if campo in ('html', 'rot', 'titulo', 'liga', 'ver', 'g', 'l', 't'):
                        continue
                    for t in textos(v):
                        with self.subTest(grupo=g, cartao=k, campo=campo):
                            # o que it() faz: troca **x** (até 80) e _x_ (até 100); o que sobra fica cru no ecrã
                            resto = re.sub(r'[*]{2}([^*]{1,80})[*]{2}', r'\1', t)
                            resto = re.sub(r'(^|[^0-9A-Za-zÀ-ÖØ-öø-ÿ_/])_([^_\n<>]{1,100}?)_(?![0-9A-Za-zÀ-ÖØ-öø-ÿ_])', r'\1\2', resto)
                            self.assertNotIn('**', resto, t[:90])
                            self.assertIsNone(re.search(r'(?<![\w/])_[^_\n<>]{101,}_(?!\w)', resto), t[:90])


class SeccaoEGerador(unittest.TestCase):
    """O que não é de uma só prova: a secção com todas, as ligações a partir de /exame/ e o gerador."""

    def test_ha_pelo_menos_uma_prova_e_cada_uma_tem_fixture_e_dados(self):
        self.assertTrue(PROVAS)
        com_dados = {p.parent.name for p in DADOS.glob('*/prova.json')}
        self.assertEqual(com_dados, {P.pasta for P in PROVAS}, 'cada prova com dados tem a sua fixture, e vice-versa')

    def test_seccao_um_bloco_por_prova_a_mais_recente_primeiro(self):
        s = ler(SECCAO)
        ordem = re.findall(r'<section class="pv-prova" id="prova-([0-9]{4}-[0-9]f)"', s)
        self.assertEqual(ordem, [P.pasta for P in PROVAS])
        ids = re.findall(r'\bid="([^"]+)"', s)
        self.assertEqual(len(ids), len(set(ids)), 'ids repetidos na secção')
        hrefs = re.findall(r'<li class="pv-grupo"><a href="([^"]+)"', s)
        self.assertEqual(hrefs, [f'{P.pasta}/{slug}/' for P in PROVAS for slug in P.grupos.values()])

    def test_cada_bloco_da_secao_tem_um_nome_proprio(self):
        """Revisão técnica de 30/10/2026: os blocos tinham o mesmo título e o mesmo nome de região («Exame Final Nacional de
        Português, Prova 639»); quem navega por títulos ou por regiões ouvia duas vezes a mesma coisa."""
        s = ler(SECCAO)
        nomes = {}
        for m in re.finditer(r'<section class="pv-prova" id="prova-([^"]+)" aria-labelledby="([^"]+)"', s):
            partes = []
            for i in m.group(2).split():
                el = re.search(rf'<(\w+)\b[^>]*\bid="{i}"[^>]*>(.*?)</\1>', s, re.S)
                self.assertIsNotNone(el, i)
                partes.append(plano(el.group(2)))
            nomes[m.group(1)] = ' '.join(partes)
        self.assertEqual(sorted(nomes), sorted(P.pasta for P in PROVAS))
        self.assertEqual(len(set(nomes.values())), len(nomes), nomes)
        titulos = [plano(x) for x in re.findall(r'<h2\b[^>]*>(.*?)</h2>', s, re.S)]
        self.assertEqual(len(titulos), len(set(titulos)), titulos)
        for P in PROVAS:
            self.assertTrue(nomes[P.pasta].startswith(f'{P.ano}, {P.fase}.ª fase '), nomes[P.pasta])

    def test_uma_so_medicao_das_opcoes(self):
        """Opções equilibradas: as provas (scripts/provas/opcoes.py) e os aquecimentos (scripts/auditar_aquecimentos_m1.py)
        medem com scripts/opcoes_equilibradas.py, sem tolerância e com os empates a contar (30/10/2026)."""
        cartoes = [{'t': 'escolha', 'g': '1', 'o': ['8', '11', '5'], 'c': 0},
                   {'t': 'escolha', 'g': '2', 'o': ['abc', 'abc', 'abc'], 'c': 1},
                   {'t': 'completar', 'g': '3', 'lacunas': [{'o': ['abcd', 'abc', 'abc'], 'c': 0}]},
                   {'t': 'escolha', 'g': '4', 'rot': 'Item 1 da prova', 'o': ['a', 'bbbbbbbb', 'c'], 'c': 1}]
        m = opcoes.medir(cartoes)
        self.assertEqual(m['perguntas'], 3, 'as opções oficiais (o item da prova) não contam')
        self.assertEqual([x['cartao'] for x in m['falhas']], [1, 3], 'sem tolerância para as opções curtas')
        self.assertEqual(m['certa_mais_longa'], 2, 'os empates contam, também com as opções todas iguais')
        self.assertTrue(m['mais_longa_acima_do_limite'])
        a = auditar_aquecimentos({'slug': 'controlo', 'cartoes': cartoes[:3]})
        self.assertEqual((a['certas_mais_longas'], len(a['erros'])), (m['certa_mais_longa'], len(m['falhas']) + 1))
        self.assertEqual(opcoes.dentro_da_catraca(m, {'falhas': 2, 'certa_mais_longa': 2}), [])
        self.assertTrue(opcoes.dentro_da_catraca(m, {'falhas': 1, 'certa_mais_longa': 2}))

    def test_o_que_vem_a_seguir(self):
        sec = json.loads(ler(DADOS / 'seccao.json'))
        feitas = {(P.ano, P.fase) for P in PROVAS}
        faltam = {}
        for ano, fase in sec['previstas']:
            if (ano, fase) not in feitas:
                faltam.setdefault(ano, []).append(fase)
        seguir = re.search(r'<section class="pv-seguir".*?</section>', ler(SECCAO), re.S).group(0)
        rotulos = re.findall(r'<li><b>([^<]+)</b>', seguir)
        esperado = []
        for ano in sorted(faltam, reverse=True):
            fs = sorted(faltam[ano])
            esperado.append(f'{ano}, {fs[0]}.ª fase' if len(fs) == 1 else f'{ano}, ' + ', '.join(f'{f}.ª' for f in fs[:-1]) + f' e {fs[-1]}.ª fases')
        self.assertEqual(rotulos, esperado)
        for P in PROVAS:
            self.assertNotIn(f'<b>{P.ano}, {P.fase}.ª fase</b>', seguir, 'uma prova publicada não está «em preparação»')
        self.assertIsNone(SEM_DATAS.search(seguir), 'sem datas prometidas')

    def test_chaves_diferentes_entre_provas(self):
        chaves = [P.chave(g) for P in PROVAS for g in P.grupos]
        self.assertEqual(len(chaves), len(set(chaves)))
        s = ler(SECCAO)
        self.assertEqual(sorted(re.findall(r'data-chave="([^"]+)"', s)), sorted(chaves))

    def test_ligacoes_a_partir_do_exame(self):
        exame = ler(ROOT / 'exame/index.html')
        self.assertEqual(exame.count('<a href="provas/">Provas em cartões</a>'), 1)
        self.assertEqual(exame.count('href="laboratorio/"'), 1)
        app = ler(ROOT / 'assets/exame/app.js')
        porta = re.search(r'<section class="provas-porta".*?</section>', app).group(0)
        self.assertIn('<a href="provas/">', porta)
        for proibido in ('session-card', 'catalogue-group', '<select', 'laboratorio/'):
            self.assertNotIn(proibido, porta)
        self.assertIsNone(PALAVRAS_PROIBIDAS.search(plano(porta)))
        self.assertIn('<a href="../provas/">Provas em cartões</a>', ler(ROOT / 'exame/laboratorio/index.html'))
        self.assertIn('.site-head nav{flex-wrap:wrap;row-gap:0}', ler(ROOT / 'assets/exame/exame.css'))

    def test_ligacoes_internas_da_seccao_e_do_exame(self):
        sessoes = {x['id'] for x in json.loads(ler(ROOT / 'assets/exame/sessoes.json'))['sessions']}
        ids_seccao = set(re.findall(r'\bid="([^"]+)"', ler(SECCAO)))
        for p in (SECCAO, ROOT / 'exame/index.html', ROOT / 'exame/laboratorio/index.html'):
            for ref in re.findall(r'(?:href|src)="([^"]+)"', ler(p)):
                if re.match(r'^(https?:|mailto:|data:|#|javascript:)', ref) or '"+' in ref:
                    continue
                caminho, _, ancora = ref.partition('#')
                alvo = (p.parent / caminho.split('?')[0]).resolve() if caminho else p
                if alvo.is_dir():
                    alvo = alvo / 'index.html'
                with self.subTest(pagina=p.relative_to(ROOT).as_posix(), ref=ref):
                    self.assertTrue(alvo.is_file(), alvo)
                    if ancora and alvo == SECCAO:
                        self.assertIn(ancora, ids_seccao)
                    if ancora and alvo == ROOT / 'exame/index.html' and ancora.startswith('s'):
                        self.assertIn(ancora.split('/')[0], sessoes)

    def test_regras_de_escrita_na_moldura_da_seccao(self):
        s = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', ler(SECCAO), flags=re.S)
        s = re.sub(r'<section class="pv-prova".*?</section>', ' ', s, flags=re.S)  # cada bloco confere-se no caso da prova
        self.assertEqual([m for p in segmentos(s) for m in PALAVRAS_PROIBIDAS.findall(plano(p))], [])

    def test_o_gerador_da_as_paginas_que_estao_na_arvore(self):
        """scripts/provas/gerar.py, com os dados e as fixtures, dá byte a byte as lições e a secção (nada escrito à mão)."""
        r = subprocess.run([sys.executable, '-B', 'scripts/provas/gerar.py', '--verificar'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, '-B', 'scripts/provas/gerar.py', '--saida', tmp], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            gerados = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('*.html'))
            esperados = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'exame/provas').rglob('*.html'))
            self.assertEqual(gerados, esperados, 'cada página de exame/provas/ sai do gerador')
            for rel in gerados:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())


# Um caso por fixture: Prova_2026_1f_v2, …
for _P in PROVAS:
    _nome = 'Prova_' + _P.id.replace('-', '_')
    globals()[_nome] = type(_nome, (CasoDeProva, unittest.TestCase), {'P': _P, '__doc__': f'{_P.nome}, versão {_P.versao}'})
del _P, _nome

if __name__ == '__main__':
    unittest.main()
