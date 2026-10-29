"""29/10/2026: Provas em cartões (exame/provas/), piloto com a Prova 639, 1.ª fase, 2026, versão 2.

Pedido do docente: os exames passam a lições em cartões, uma por grupo da prova; os itens de resposta escrita
desmontam-se em cartões e a resposta completa escreve-se no caderno, com a grelha à vista. Aqui confere-se, sem
navegador, que:
- os três grupos passam em validate_cards (o tipo «item», os itens de escolha múltipla do Grupo II com as quatro
  opções da prova, valida-se como «escolha») e usam só os campos do motor;
- o texto da prova (linhas numeradas, versos, notas) é igual à transcrição conferida em
  tests/fixtures/prova-639-2026-1f-v2.json, e cada item da prova tem o seu enunciado e cartões de preparação;
- as chaves de escolha múltipla são as da versão 2 dos critérios de classificação;
- cada lição cita a fonte (prova, fase, ano, versão, IAVE, as cópias públicas e as fontes dos textos);
- não há código da Sala de aula nem chaves que choquem com as das lições;
- as ligações internas existem;
- o texto que escrevemos (fora do texto da prova e dos critérios) cumpre as regras de escrita;
- (revisão de 29/10) a ordem dos cartões: nos itens de resposta escrita, os exemplos completos e os tópicos dos critérios só
  depois do cartão «Escreve no caderno»; nos itens de escolha, o item da prova antes dos cartões «Porquê?»; o que adaptamos diz
  «adaptado»; o feedback das escolhas não aponta opções pela posição (o motor baralha-as).
O percurso no navegador está em tests/browser_provas_cartoes.py.
"""
import html
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import TYPES, lesson_cards, validate_cards  # noqa: E402

FX = json.loads((ROOT / 'tests/fixtures/prova-639-2026-1f-v2.json').read_text('utf-8'))
PROVAS = ROOT / 'exame/provas'
SECCAO = PROVAS / 'index.html'
GRUPOS = {1: 'grupo-i', 2: 'grupo-ii', 3: 'grupo-iii'}
PAGINAS = {g: PROVAS / '2026-1f' / slug / 'index.html' for g, slug in GRUPOS.items()}
ASSETS = [ROOT / 'assets/exame/provas-licao.js', ROOT / 'assets/exame/provas-licao.css',
          ROOT / 'assets/exame/provas.js', ROOT / 'assets/exame/provas.css']
URL_ENUNCIADO = 'https://www.examesnacionais.com.pt/exames-nacionais/12ano/2026-1fase/Portugues.pdf'
URL_CRITERIOS = 'https://www.examesnacionais.com.pt/exames-nacionais/12ano/2026-1fase/Portugues_Criterios.pdf'

# Chaves da versão 2, tal como estão nos critérios de classificação (Grupo I, pp. 7 e 11; Grupo II, p. 13).
CHAVES_II = {1: 'B', 2: 'C', 3: 'A', 4: 'D', 5: 'B', 6: 'C', 7: 'D'}
CHAVE_I3 = {'a': 1, 'b': 2}
CHAVE_I6 = {'I', 'III', 'IV'}

# Campos que o motor (jogo.js e rever-frase.js) e o tipo «item» (assets/exame/provas-licao.js) leem.
CAMPOS = {'t', 'rot', 'titulo', 'html', 'escuro', 'p', 'p2', 'o', 'c', 'f', 'fe', 'cita', 'l', 'g', 'v', 'pares',
          'frase', 'lacunas', 'passos', 'linhas', 'palavras', 'certas', 'apoio', 'trecho', 'liga', 'ver', 'voc'}
# Rótulo dos cartões com o item tal como está na prova; o que está adaptado ao ecrã diz «adaptado» e lê-se como texto nosso.
OFICIAL = re.compile(r'\bItem \d+ da prova\b(?! \(adaptado)')
PALAVRAS_PROIBIDAS = re.compile(r'—|–|‒|·|\bprofessor|\bjog|\bficha|\bfolha', re.I)
SALA = ('ntfy', 'EventSource', 'BroadcastChannel', 'EPISala', 'aoEvento', 'enviarSala', 'data-sala', 'epi-sala',
        'painel-sala-', 'id="liga-sala"', '<div class="sala"', 'data-fechar-sala', 'Código da sala', 'id="faixa-pausa"',
        'id="sobre"', 'sala-cod', 'data-placar', 'Nova sala')


def ler(p):
    return p.read_text('utf-8')


def cartoes(g):
    return lesson_cards(PAGINAS[g])


def plano(s):
    """Texto simples: sem etiquetas, sem a marcação dos dados (_itálico_, **negrito**, [^n]), espaços normalizados."""
    s = re.sub(r'<sup>\d+</sup>', '', s)
    s = re.sub(r'</?(?:i|b|em|strong|span|a|sub|small|cite)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\[\^\d+\]', '', s).replace('**', '')
    s = re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def textos(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from textos(y)
    elif isinstance(x, dict):
        for k, y in x.items():
            if not k.startswith('_') and 'nossa' not in k:
                yield from textos(y)


CORPUS = ' \n '.join(plano(t) for t in textos({k: v for k, v in FX.items() if k != '_sobre'}))


def oficial(trecho):
    t = plano(trecho)
    return bool(t) and t in CORPUS


def linhas_da_prova():
    """{chave data-l: texto da linha na transcrição}, como as lições as numeram (Grupo I parte B com «v»)."""
    g1, g2, _ = FX['grupos']
    out = {1: {}, 2: {}}
    for parte in g1['partes']:
        for t in parte.get('textos', []):
            for linha in t.get('linhas', []):
                out[1][str(linha['n'])] = linha['t']
            for estrofe in t.get('estrofes', []):
                for v in estrofe:
                    out[1]['v%d' % v['v']] = v['t']
    for linha in g2['textos'][0]['linhas']:
        out[2][str(linha['n'])] = linha['t']
    return out


def linha_html(s):
    """Uma linha dos dados no formato das lições: _x_ em <i>, [^n] em <sup>n</sup>."""
    s = html.escape(s, quote=False)
    s = re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'<i>\1</i>', s)
    return re.sub(r'\[\^(\d+)\]', r'<sup>\1</sup>', s)


def linhas_na_licao(cards):
    """(data-l, HTML da linha só com <i> e <sup>) de cada span.ln com data-l."""
    out = []
    for c in cards:
        if c['t'] != 'ler':
            continue
        for m in re.finditer(r'<span class="ln(?: par)?" data-l="([^"]+)"><span class="n" aria-hidden="true">(\d*)</span>(.*?)</span>(?=<span class="ln|</div>)', c.get('html', '')):
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


FONTES = [t['fonte'] for p in FX['grupos'][0]['partes'] for t in p.get('textos', [])] + [FX['grupos'][1]['textos'][0]['fonte']]


def nosso(texto):
    """O texto que escrevemos: tira as referências dos textos, como a prova as dá, e as citações «…» que são da prova
    ou dos critérios (uma citação com «[…]» conta se cada pedaço for da prova)."""
    t = plano(texto)
    for f in FONTES:
        t = t.replace(plano(f).rstrip('.'), ' ')
    return re.sub(r'«([^«»]*)»', lambda m: ' ' if all(oficial(x) or not x.strip() for x in m.group(1).split('[…]')) else m.group(0), t)


def segmentos(h):
    """O HTML partido nos blocos (parágrafos, itens de lista, células, quebras): cada bloco lê-se sozinho."""
    return [x for x in re.split(r'<(?:/?(?:p|li|ul|ol|td|th|tr|table|div|details|summary|h\d)\b[^>]*|br\s*/?)>', h) if x.strip()]


def fora_das_regras(trecho):
    """As marcas proibidas que sobram num bloco, salvo quando o bloco inteiro é da prova ou dos critérios."""
    if oficial(trecho):
        return []
    return PALAVRAS_PROIBIDAS.findall(nosso(trecho))


class ProvasEmCartoes(unittest.TestCase):
    def test_os_tres_grupos_passam_em_validate_cards_com_os_campos_do_motor(self):
        for g in GRUPOS:
            cards = cartoes(g)
            with self.subTest(grupo=g):
                self.assertGreaterEqual(len(cards), 40)
                self.assertEqual(validate_cards([dict(c, t='escolha') if c.get('t') == 'item' else c for c in cards]), [])
                for k, c in enumerate(cards):
                    self.assertIn(c['t'], TYPES | {'item'}, k)
                    self.assertLessEqual(set(c), CAMPOS, (k, set(c) - CAMPOS))
                    if c['t'] == 'item':
                        self.assertEqual(g, 2)
                        self.assertEqual(len(c['o']), 4, k)
                        self.assertNotIn('p2', c)
                fazer = [c for c in cards if c['t'] != 'ler']
                self.assertGreaterEqual(len(fazer), 3 * len([c for c in cards if c['t'] == 'ler']) // 2)
                gs = [c.get('g') for c in fazer]
                self.assertEqual(len(gs), len(set(gs)), 'cada cartão de fazer tem o seu g, para a ordem da prova')
                self.assertNotIn(None, gs)

    def test_paginas_usam_o_motor_sem_a_sala_e_com_chaves_proprias(self):
        chaves = set()
        for g in GRUPOS:
            s = ler(PAGINAS[g])
            with self.subTest(grupo=g):
                m = re.search(r'var K="([^"]+)",CARTOES=', s)
                self.assertIsNotNone(m)
                self.assertEqual(m.group(1), f'prova-2026-1f-g{g}')
                chaves.add(m.group(1))
                for marca in ('variar:false', 'versao:"2026-10-29"', 'percurso:"../../#prova-2026-1f"',
                              'percursoRotulo:"Provas em cartões"', 'assets/pt-lessons/jogo.js?v=',
                              'assets/pt-lessons/casca.js', 'assets/exame/provas-licao.js?v=', 'assets/exame/provas-licao.css?v=',
                              '<style id="casca-pc">', '<style id="amp-css">', '<script id="amp-js">'):
                    self.assertIn(marca, s)
                for marca in ('epi-ultima', 'K+"-a1"', 'pistas:', 'data-unit-return', 'CARTAZ_DADOS', 'atlasEstado',
                              'abrirExtra'):
                    self.assertNotIn(marca, s)
                self.assertEqual(s.count('assets/pt-lessons/rever-frase.js'), 1 if any(c['t'] == 'rever' for c in cartoes(g)) else 0)
                if g < 3:
                    self.assertIn(f'seguinte:"../{GRUPOS[g + 1]}/",seguinteRotulo:"Grupo {"I" * (g + 1)}"', s)
                else:
                    self.assertIn('voltarRotulo:"Voltar às provas"', s)
                self.assertIn(f'<title>Prova 639, 1.ª fase, 2026: Grupo {"I" * g}</title>', s)
                self.assertIn('<b>Aprendes:</b>', s)
        self.assertEqual(len(chaves), 3)
        for p in ROOT.glob('m[1-9]/licao-*/index.html'):
            self.assertNotIn('prova-2026-1f-g', ler(p))

    def test_nenhum_codigo_da_sala(self):
        for p in list(PAGINAS.values()) + [SECCAO] + ASSETS:
            s = ler(p)
            for marca in SALA:
                self.assertNotIn(marca, s, f'{p.relative_to(ROOT)}: {marca}')
            self.assertIsNone(re.search(r'<button\b[^>]*>\s*Sala\b', s), p)

    def test_texto_da_prova_igual_a_transcricao(self):
        esperado = linhas_da_prova()
        for g in (1, 2):
            vistas = {}
            for dl, n, corpo in linhas_na_licao(cartoes(g)):
                with self.subTest(grupo=g, linha=dl):
                    self.assertNotIn(dl, vistas, 'cada linha da prova aparece numerada uma só vez')
                    self.assertEqual(corpo, linha_html(esperado[g][dl]))
                    numero = int(dl.lstrip('v'))
                    self.assertEqual(n, str(numero) if numero % 5 == 0 else '')
                    vistas[dl] = corpo
            self.assertEqual(set(vistas), set(esperado[g]), f'grupo {g}: linhas em falta')
        # notas: o texto exato de cada nota da prova
        g1, g2, _ = FX['grupos']
        notas = {1: [n for p in g1['partes'] for n in p.get('notas', [])], 2: g2['notas']}
        for g in (1, 2):
            gl = ' '.join(plano(m) for c in cartoes(g) if c['t'] == 'ler' for m in re.findall(r'<p class="gl">(.*?)</p>', c['html'], re.S))
            for nota in notas[g]:
                self.assertIn(plano(nota['texto']), gl, (g, nota['n']))

    def test_cada_item_da_prova_tem_o_enunciado_e_cartoes(self):
        g1, g2, g3 = FX['grupos']
        itens1 = {i['n']: i for p in g1['partes'] for i in p['itens']}
        self.assertEqual(sorted(itens1), [1, 2, 3, 4, 5, 6, 7])
        cards = cartoes(1)
        tudo = plano(' '.join(json.dumps(c, ensure_ascii=False) for c in cards).replace('\\"', '"'))
        for n, item in itens1.items():
            with self.subTest(grupo='I', item=n):
                prep = [c for c in cards if c['t'] != 'ler' and str(c.get('g', '')).startswith(str(n))]
                self.assertGreaterEqual(len(prep), 4)
                self.assertIn(plano(item['enunciado'][0]), tudo)
                if item['tipo'].startswith('construção'):
                    caderno = [c for c in cards if c['t'] == 'ler' and c.get('rot') == 'Escreve no caderno' and c['titulo'].startswith(f'Item {n} ')]
                    self.assertEqual(len(caderno), 1)
                    papel = plano(re.search(r'<p class="papel-q">(.*?)</p>', caderno[0]['html'], re.S).group(1))
                    for frase in item['enunciado']:
                        self.assertIn(plano(frase), papel)
                    self.assertIn('<table class="empilha grelha">', caderno[0]['html'], 'a grelha oficial à vista')
                    self.assertIn('<table class="cl">', caderno[0]['html'])
        cards = cartoes(2)
        for item in g2['itens']:
            n = item['n']
            with self.subTest(grupo='II', item=n):
                oficial_ = [c for c in cards if c['t'] == 'item' and c['g'] == f'{n}i']
                self.assertEqual(len(oficial_), 1)
                self.assertEqual(plano(oficial_[0]['p']), plano(' '.join(item['enunciado'])))
                self.assertTrue(oficial_[0]['rot'].startswith(f'Item {n} da prova'))
                self.assertEqual(oficial_[0]['rot'].endswith('✱'), item['obrigatorio'])
                prep = [c for c in cards if c['t'] != 'ler' and c['t'] != 'item' and str(c['g']).startswith(str(n))]
                self.assertGreaterEqual(len(prep), 2)
        cards = cartoes(3)
        item = g3['itens'][0]
        prova = [c for c in cards if c['t'] == 'ler' and c.get('rot') == 'A prova']
        caderno = [c for c in cards if c['t'] == 'ler' and c.get('rot') == 'Escreve no caderno']
        self.assertEqual((len(prova), len(caderno)), (1, 1))
        for c in prova + caderno:
            texto = plano(c['html'])
            for frase in item['enunciado'] + item['enunciado_lista']:
                self.assertIn(plano(frase), texto)
        self.assertIn('<table class="empilha grelha">', caderno[0]['html'])
        self.assertGreaterEqual(len([c for c in cards if c['t'] != 'ler']), 30)

    def test_exemplos_e_topicos_so_depois_da_escrita(self):
        """Nos itens de resposta escrita, a resposta completa de exemplo e os tópicos dos critérios vêm depois do caderno."""
        cards = cartoes(1)
        for n in (1, 2, 4, 5, 7):
            with self.subTest(grupo='I', item=n):
                k_cad = next(k for k, c in enumerate(cards) if c['t'] == 'ler' and c.get('titulo') == f'Item {n} ✱')
                cad = cards[k_cad]['html']
                self.assertNotIn('Tópicos de resposta', cad)
                self.assertNotIn('Confere a tua resposta', cad)
                self.assertIn('<summary>A grelha oficial, tal como está nos critérios</summary>', cad)
                self.assertIn('leitura nossa da grelha', cad)
                if n != 7:
                    self.assertIn('<summary>As linhas do item</summary>', cad)
                    k_cmp = [k for k, c in enumerate(cards) if c.get('rot') == 'Compara a tua resposta' and str(c.get('g', '')).startswith(str(n))]
                    self.assertEqual(k_cmp, [k_cad + 1], 'as respostas de exemplo logo depois do caderno')
                    antes = [c for c in cards[:k_cad] if str(c.get('g', '')).startswith(str(n))]
                    self.assertFalse([c for c in antes if c.get('rot') == 'Compara a tua resposta'])
                k_conf = next(k for k, c in enumerate(cards) if c['t'] == 'ler' and c.get('rot') == 'Confere com os critérios'
                              and c['titulo'].startswith(f'Item {n}:'))
                self.assertGreater(k_conf, k_cad)
                self.assertIn('Tópicos de resposta dos critérios', cards[k_conf]['html'])
        cards = cartoes(3)
        k_cad = next(k for k, c in enumerate(cards) if c.get('rot') == 'Escreve no caderno')
        k_auto = next(k for k, c in enumerate(cards) if c.get('rot') == 'Revê com a grelha')
        k_ex = next(k for k, c in enumerate(cards) if c.get('rot') == 'Compara com um exemplo')
        self.assertLess(k_cad, k_auto)
        self.assertEqual(k_ex, k_auto + 1)
        self.assertNotIn('Um exemplo nosso', cards[k_cad]['html'])
        self.assertFalse([c for c in cards[:k_cad] if 'Escreve no caderno' in (c.get('f') or '') and 'Um exemplo nosso' in (c.get('f') or '')])

    def test_itens_de_escolha_antes_dos_cartoes_porque(self):
        """O item da prova vem logo a seguir ao texto (tenta-se sozinho); os cartões que desmentem as opções vêm depois."""
        casos = {1: {'3': ['3i', '3j'], '6': ['6i']}, 2: {str(n): [f'{n}i'] for n in range(1, 6)}}
        for g, itens in casos.items():
            cards = cartoes(g)
            pos = {c.get('g'): k for k, c in enumerate(cards) if c.get('g')}
            for n, oficiais in itens.items():
                porques = [c['g'] for c in cards if c.get('rot', '').startswith('Porquê?') and c['g'].startswith(n)]
                with self.subTest(grupo=g, item=n):
                    self.assertTrue(porques)
                    self.assertLess(max(pos[o] for o in oficiais), min(pos[p] for p in porques))
                    for c in cards:
                        if c.get('rot', '').startswith('Porquê?'):
                            for t in textos({k: c.get(k) for k in ('p', 'p2', 'f', 'fe')}):
                                self.assertNotRegex(t, r'Lembra-te|te pede que verifiques|Repara em que coluna')

    def test_feedback_das_escolhas_nao_aponta_posicoes(self):
        """O motor baralha as opções das escolhas: o feedback nomeia-as pelo conteúdo, nunca por «a primeira» ou «a segunda»."""
        for g in GRUPOS:
            for k, c in enumerate(cartoes(g)):
                if c['t'] != 'escolha':
                    continue
                for t in textos({'f': c.get('f'), 'fe': c.get('fe')}):
                    with self.subTest(grupo=g, cartao=k + 1):
                        self.assertNotRegex(t, r'\*\*(A|O) (primeir|segund|terceir)[oa]\b|\b(A|O) (segund|terceir)[oa] (já|tem|é)\b|\bAs outras\b')

    def test_chaves_de_escolha_multipla_batem_com_os_criterios(self):
        g1, g2, _ = FX['grupos']
        for item in g2['itens']:
            n = item['n']
            with self.subTest(item=f'II.{n}'):
                self.assertEqual(item['chave_versao_2'], CHAVES_II[n])
                c = next(x for x in cartoes(2) if x['t'] == 'item' and x['g'] == f'{n}i')
                self.assertEqual([o['letra'] for o in item['opcoes']], list('ABCD'))
                self.assertEqual([plano(o) for o in c['o']], [plano(o['texto']) for o in item['opcoes']])
                self.assertEqual(c['c'], 'ABCD'.index(CHAVES_II[n]))
                self.assertIsNone(c['fe'][c['c']])
        itens1 = {i['n']: i for p in g1['partes'] for i in p['itens']}
        cards = cartoes(1)
        for espaco, chave in CHAVE_I3.items():
            with self.subTest(item=f'I.3 ({espaco})'):
                c = next(x for x in cards if x.get('rot') == f'Item 3 da prova, espaço ({espaco})')
                self.assertEqual(c['t'], 'escolha')
                opcoes = itens1[3]['opcoes'][espaco]
                self.assertEqual(sorted(plano(o) for o in c['o']), sorted(plano(f'({o["n"]}) {o["texto"]}') for o in opcoes))
                self.assertTrue(c['o'][c['c']].startswith(f'({chave}) '))
        self.assertEqual(set(itens1[6]['chave_versao_2']), CHAVE_I6)
        c = next(x for x in cards if x.get('rot', '').startswith('Item 6 da prova'))
        self.assertEqual(c['t'], 'emparelhar')
        # formato adaptado ao ecrã (duas colunas nossas): o rótulo e o feedback dizem-no
        self.assertEqual(c['rot'], 'Item 6 da prova (adaptado ao ecrã)')
        self.assertIn('adaptado ao ecrã', c['f'])
        colunas = {}
        for afirmacao, coluna in c['pares']:
            colunas.setdefault(coluna, set()).add(afirmacao.split('.', 1)[0])
        self.assertEqual(len(colunas), 2)
        certas = [v for k, v in colunas.items() if not k.startswith('não')]
        self.assertEqual(certas, [CHAVE_I6])
        for o in itens1[6]['opcoes']:
            self.assertIn(plano(f'{o["n"]}. {o["texto"]}'), [plano(a) for a, _ in c['pares']])

    def test_cada_licao_cita_a_fonte(self):
        g1, g2, g3 = FX['grupos']
        fontes = {1: [t['fonte'] for p in g1['partes'] for t in p.get('textos', [])], 2: [g2['textos'][0]['fonte']],
                  3: [g3['itens'][0]['imagem']['fonte']]}
        for g in GRUPOS:
            s = ler(PAGINAS[g])
            menu = plano(re.search(r'<div class="casca-menu".*?</div></div>', s, re.S).group(0))
            with self.subTest(grupo=g):
                for marca in ('Prova 639', '1.ª fase, 2026', 'versão 2', 'IAVE', 'EduQA', 'Instituto de Educação, Qualidade e Avaliação'):
                    self.assertIn(marca, menu)
                for url in (URL_ENUNCIADO, URL_CRITERIOS):
                    self.assertIn(f'href="{url}"', s)
                for f in fontes[g]:
                    self.assertIn(plano(f).rstrip('.'), menu)
                abre = cartoes(g)[0]
                self.assertEqual(abre.get('rot'), 'Abre')
                self.assertIn('IAVE', abre['html'])
                self.assertIn('versão 2', abre['html'])
        s = ler(SECCAO)
        for marca in ('Prova 639, 1.ª fase, 2026, versão 2', 'IAVE', 'EduQA', URL_ENUNCIADO, URL_CRITERIOS):
            self.assertIn(marca, s)

    def test_seccao_e_ligacoes_a_partir_do_exame(self):
        s = ler(SECCAO)
        self.assertIn('id="prova-2026-1f"', s)
        for g, slug in GRUPOS.items():
            versao = re.search(r'versao:"([^"]+)"', ler(PAGINAS[g])).group(1)
            m = re.search(rf'<li class="pv-grupo"><a href="2026-1f/{slug}/" data-chave="prova-2026-1f-g{g}" data-versao="{re.escape(versao)}" '
                          rf'aria-labelledby="pv-g{g}-n pv-g{g}-t pv-g{g}-e">.*?</a></li>', s)
            self.assertIsNotNone(m, slug)
            for ident in (f'pv-g{g}-n', f'pv-g{g}-t', f'pv-g{g}-e'):
                self.assertIn(f'id="{ident}"', m.group(0))
            fazer = len([c for c in cartoes(g) if c['t'] != 'ler'])
            self.assertIn(f'{len(cartoes(g))} cartões, {fazer} para responder.', m.group(0))
        seguir = re.search(r'<section class="pv-seguir".*?</section>', s, re.S).group(0)
        for prova in ('2026, 2.ª fase', '2025, 1.ª e 2.ª fases', '2024, 1.ª e 2.ª fases', '2023, 1.ª e 2.ª fases'):
            self.assertIn(prova, seguir)
        self.assertIsNone(re.search(r'\b(19|20)\d\d-\d\d|\b\d{1,2}/\d{1,2}/20\d\d|janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro', seguir), 'sem datas prometidas')
        exame = ler(ROOT / 'exame/index.html')
        self.assertEqual(exame.count('<a href="provas/">Provas em cartões</a>'), 1)
        self.assertEqual(exame.count('href="laboratorio/"'), 1)
        app = ler(ROOT / 'assets/exame/app.js')
        porta = re.search(r'<section class="provas-porta".*?</section>', app).group(0)
        self.assertIn('<a href="provas/">', porta)
        for proibido in ('session-card', 'catalogue-group', '<select', 'laboratorio/'):
            self.assertNotIn(proibido, porta)
        self.assertIn('<a href="../provas/">Provas em cartões</a>', ler(ROOT / 'exame/laboratorio/index.html'))
        self.assertIn('.site-head nav{flex-wrap:wrap;row-gap:0}', ler(ROOT / 'assets/exame/exame.css'))

    def test_ligacoes_internas_existem(self):
        sessoes = {x['id'] for x in json.loads(ler(ROOT / 'assets/exame/sessoes.json'))['sessions']}
        ids_seccao = set(re.findall(r'\bid="([^"]+)"', ler(SECCAO)))
        for p in list(PAGINAS.values()) + [SECCAO, ROOT / 'exame/index.html', ROOT / 'exame/laboratorio/index.html']:
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
        for g in GRUPOS:
            for c in cartoes(g):
                for l in c.get('liga', []):
                    alvo = (PAGINAS[g].parent / l['href'].split('#')[0]).resolve()
                    self.assertTrue((alvo / 'index.html' if alvo.is_dir() else alvo).is_file(), l['href'])

    def test_regras_de_escrita_no_texto_nosso(self):
        """«tu», «docente», sem «professor», «jogar», «ficha», «folha», «·» nem travessões no que escrevemos.

        O texto da prova e dos critérios fica como está (tem «folha de respostas», «folha branca» e travessões):
        os blocos que o reproduzem são conferidos com a transcrição noutros testes, e as citações «…» só ficam de
        fora quando são da prova ou dos critérios."""
        for g in GRUPOS:
            for k, c in enumerate(cartoes(g)):
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
                                self.assertTrue(oficial(re.sub(r'^\(?[IV\d]+[.)]\s*', '', t)) or oficial(t.split('\n')[0]) or not PALAVRAS_PROIBIDAS.search(t), (g, k, t))
                    partes += [t for campo in campos for t in textos(c.get(campo))]
                with self.subTest(grupo=g, cartao=k):
                    self.assertEqual([m for p in partes if p for m in fora_das_regras(p)], [])
            # a moldura da página: título, menu, fim e avisos
            s = ler(PAGINAS[g])
            moldura = re.sub(r'<script>document\.addEventListener.*?</script>', ' ', s, flags=re.S)
            moldura = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', moldura, flags=re.S)
            depois = json.loads(re.search(r'depois:("(?:[^"\\]|\\.)*")', s).group(1))
            with self.subTest(grupo=g, parte='moldura'):
                self.assertEqual([m for p in segmentos(moldura + ' ' + depois) for m in fora_das_regras(p)], [])
        seccao = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', ler(SECCAO), flags=re.S)
        self.assertEqual([m for p in segmentos(seccao) for m in fora_das_regras(p)], [])
        porta = re.search(r'<section class="provas-porta".*?</section>', ler(ROOT / 'assets/exame/app.js')).group(0)
        self.assertIsNone(PALAVRAS_PROIBIDAS.search(plano(porta)))

    def test_blocos_oficiais_so_tem_texto_da_prova_ou_dos_criterios(self):
        """Os blocos que o teste das regras de escrita deixa de fora têm de ser mesmo da prova ou dos critérios."""
        cabecalhos = {'Nível', 'Descritor de desempenho', 'Pontuação', 'Número de erros do tipo B', 'Número de erros do tipo A',
                      'Parâmetro', 'Tabela da correção linguística', 'OU'}
        for g in GRUPOS:
            for k, c in enumerate(cartoes(g)):
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
                        self.assertTrue(oficial(t), t)


if __name__ == '__main__':
    unittest.main()
