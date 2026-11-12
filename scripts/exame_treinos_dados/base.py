"""11/11/2026: base comum dos treinos da preparação de exame (exame/treinos/).

Os textos oficiais vêm das transcrições tests/fixtures/prova-639-2026-*.json; o que é nosso está num módulo por treino
(interpretacao.py, gramatica.py, escrita.py, poesia_contemporanea.py, conto.py) e em indice.py. As páginas escrevem-se com
scripts/exame_treinos.py.

12/11/2026: os treinos passam a vir de uma só lista (TREINOS); a navegação, a contagem («Treino n de N») e o nome da
entrada («Os quatro treinos») saem dela. Para juntar um treino, acrescenta-se uma linha aqui e o módulo em exame_treinos.py.
12/11/2026: mais o treino da sessão 18 (conto.py); licao(), que lê os cartões de uma lição do M8 para conferir citações, passa
de poesia_contemporanea.py para aqui, porque serve os dois treinos de textos com direitos de autor.
"""
import json, re, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F1 = json.load(open(ROOT + '/tests/fixtures/prova-639-2026-1f-v2.json', encoding='utf-8'))
F2 = json.load(open(ROOT + '/tests/fixtures/prova-639-2026-2f-v2.json', encoding='utf-8'))
SESSOES = {s['id']: s for s in json.load(open(ROOT + '/assets/exame/sessoes.json', encoding='utf-8'))['sessions']}

# versões dos ficheiros partilhados (as mesmas das páginas vizinhas do exame) e dos dois ficheiros dos treinos
V_APARENCIA = '20261025-universal-1'
V_PROJETAR = '20261019.4'
V_TREINO = '20261111-treinos-2'

URL = {
    'e1': 'https://eduqa.pt/wp-content/uploads/2026/06/portugues_prova_639_v2_enunciado.pdf',
    'c1': 'https://eduqa.pt/wp-content/uploads/2026/07/portugues_prova_639_cc.pdf',
    'e2': 'https://eduqa.pt/wp-content/uploads/2026/07/EX-Port639-F2-2026-V2_net.pdf',
    'c2': 'https://eduqa.pt/wp-content/uploads/2026/07/EX-Port639-F2-2026-CC-VD_net.pdf',
}


def lig(k, texto):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (URL[k], texto)


def esc(s):
    return html.escape(s, quote=False)


def md(s):
    """Marcas da transcrição: _itálico_, **negrito**, [^n] chamada de nota."""
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w/])_(.+?)_(?![\w/])', r'<i>\1</i>', s)
    s = re.sub(r'\[\^(\d+)\]', r'<sup>\1</sup>', s)
    return s


def sessao(sid, titulo, exame='../../'):
    """Ligação à sessão da preparação; o título confere-se com assets/exame/sessoes.json."""
    assert SESSOES[sid]['title'] == titulo, (sid, SESSOES[sid]['title'])
    return '<a href="%s#%s">sessão %d («%s»)</a>' % (exame, sid, int(sid[1:]), esc(titulo))


def aquecimento(sid, exame='../../'):
    assert os.path.isfile('%s/exame/aquecimentos/%s/index.html' % (ROOT, sid)), sid
    return '<a href="%saquecimentos/%s/">aquecimento</a>' % (exame, sid)


def licao(fid):
    """Texto dos cartões da lição m8/licao-m8-<fid>/, sem marcas, com os espaços normalizados, e o HTML da página."""
    h = open('%s/m8/licao-m8-%s/index.html' % (ROOT, fid), encoding='utf-8').read()
    cartoes = json.JSONDecoder().raw_decode(h[h.index('CARTOES=[') + len('CARTOES='):])[0]

    def cadeias(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for v in o.values():
                yield from cadeias(v)
        elif isinstance(o, list):
            for v in o:
                yield from cadeias(v)
    t = ' '.join(re.sub(r'<[^>]+>', ' ', re.sub(r'<img[^>]*>|<svg.*?</svg>', ' ', s, flags=re.S)) for c in cartoes for s in cadeias(c))
    t = re.sub(r'\s+', ' ', html.unescape(t))
    return re.sub(r' ([:,.;])', r'\1', t), h


# (pasta em exame/treinos/, nome na navegação), pela ordem dos treinos
TREINOS = [('interpretacao', 'Interpretação'), ('gramatica', 'Gramática'), ('escrita', 'Escrita'), ('poesia-contemporanea', 'Poesia contemporânea'), ('conto', 'Conto')]
N_TREINOS = len(TREINOS)
POR_EXTENSO = {3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis'}[N_TREINOS]
OS_TREINOS = 'Os %s treinos' % POR_EXTENSO
NAV = [('', OS_TREINOS)] + [(p + '/', t) for p, t in TREINOS]


def ordem(pid):
    """Número do treino (1, 2, 3…), pela ordem de TREINOS."""
    return [p for p, _ in TREINOS].index(pid) + 1


def sobre(pid, nome):
    """Linha por cima do título de cada treino: «Treino n de N. Nome»."""
    return '<p class="sobre">Treino %d de %d. %s</p>' % (ordem(pid), N_TREINOS, nome)


def cabeca(raiz, titulo, descr, com_motor):
    """raiz: caminho relativo até à raiz do sítio (onde está assets/)."""
    a = raiz + 'assets/'
    return ('<!doctype html>\n<html lang="pt-PT" data-appearance-site="pt"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s">'
            '<link rel="preload" href="%sexame/fontes/fraunces-latin-normal.woff2" as="font" type="font/woff2" crossorigin>'
            '<link rel="preload" href="%sexame/fontes/ibm-plex-sans-latin-normal.woff2" as="font" type="font/woff2" crossorigin>'
            '<link rel="stylesheet" href="%sappearance.css?v=%s">'
            '<link rel="stylesheet" href="%sexame/treino.css?v=%s">'
            '<script src="%sappearance.js?v=%s"></script>%s'
            '<script defer src="%sprojection-launcher.js?v=%s" data-site="pt"></script></head>\n') % (
        esc(titulo), html.escape(descr), a, a, a, V_APARENCIA, a, V_TREINO, a, V_APARENCIA,
        ('<script defer src="%sexame/treino.js?v=%s"></script>' % (a, V_TREINO)) if com_motor else '', a, V_PROJETAR)


def topo(exame, treinos, atual, migalha):
    """exame: caminho até exame/; treinos: caminho até exame/treinos/ ('./' no índice); atual: entrada de NAV; migalha: nome da página, ou None no índice."""
    def para(h):
        return (treinos + h) if treinos != './' else (h or './')
    nav = ''.join('<a href="%s"%s>%s</a>' % (para(h), ' aria-current="page"' if h == atual else '', t) for h, t in NAV)
    if migalha:
        fim = '<li><a href="%s">Treinos</a></li><li><span aria-current="page">%s</span></li>' % (treinos, migalha)
    else:
        fim = '<li><span aria-current="page">Treinos</span></li>'
    return ('<body class="treino"><a class="skip" href="#conteudo">Ir para o conteúdo</a>'
            '<nav class="migalhas" aria-label="Onde estás"><ol><li><a href="%s../">Português</a></li><li><a href="%s">Preparação de exame</a></li>%s</ol></nav>'
            '<div class="envolve"><header class="site-head"><a class="wordmark" href="%s">Português<span>.</span><small>Preparação de exame</small></a>'
            '<nav aria-label="Navegação da preparação"><a href="%s">Sessões</a><a href="%slaboratorio/">Laboratório de respostas</a>'
            '<a href="%sprovas/">Provas em cartões</a><a href="%s"%s>Treinos</a></nav></header>'
            '<nav class="tr-nav" aria-label="%s">%s</nav>\n') % (
        exame, exame, fim, exame, exame, exame, exame, treinos, '' if migalha else ' aria-current="page"', OS_TREINOS, nav)


def rodape(exame, treinos, raiz, dentro):
    """dentro: o que vem antes das ligações (o estado da guarda e o botão de recomeçar, nos treinos)."""
    return ('<footer class="site-foot pe">%s<a href="%s">Sessões de preparação</a><a href="%s">%s</a>%s</footer></div>\n') % (
        dentro, exame, treinos, OS_TREINOS, CREDITOS % (raiz, raiz))


CREDITOS = ('<p class="creditos">Itens e critérios: Exame Final Nacional de Português, Prova 639, 2026, 1.ª e 2.ª fases, citados com a página; os PDF estão em eduqa.pt. '
            'Tipos de letra: Fraunces e IBM Plex Sans, com a licença SIL Open Font License 1.1 '
            '(<a href="%sassets/exame/fontes/Fraunces-OFL.txt">Fraunces</a>, <a href="%sassets/exame/fontes/IBM-Plex-Sans-OFL.txt">IBM Plex Sans</a>).</p>')


def pagina_treino(pid, atual, migalha, titulo, descr, cab_html, apoios, treino):
    """apoios: dict id -> html; treino: dict com passos. Devolve (caminho no repositório, página)."""
    ap = ''.join('<div data-apoio="%s" hidden>%s</div>' % (k, v) for k, v in apoios.items())
    corpo = (
        '<main id="conteudo" tabindex="-1">%s'
        '<p id="aviso-guarda" class="caixa nossa" role="status" hidden>Este navegador não deixa guardar as respostas. Podes fazer o treino, mas, se recarregares a página, perdes o que escreveste: copia o teu texto para o caderno.</p>'
        '<noscript><p class="caixa nossa">Ativa o JavaScript para fazeres os passos.</p></noscript>'
        '<ol class="passos" id="passos" aria-label="Passos do treino"></ol>'
        '<div class="area" id="area">'
        '<aside class="apoio" id="apoio" aria-label="Texto de apoio" hidden>'
        '<div class="apoio-cab"><p id="apoio-rot">Texto de apoio</p><button type="button" id="apoio-bt" aria-expanded="true" aria-controls="apoio-corpo">Recolher</button></div>'
        '<div class="apoio-corpo" id="apoio-corpo" tabindex="0" role="region" aria-labelledby="apoio-rot">%s</div></aside>'
        '<section class="passo" id="passo" aria-labelledby="passo-t"></section>'
        '</div></main>\n'
    ) % (cab_html, ap)
    pe = ('<span id="pe-guarda">As tuas respostas e as duas versões do teu texto ficam só neste dispositivo (localStorage). Nada é enviado.</span>'
          '<button type="button" id="recomecar">Recomeçar este treino</button>')
    dados = json.dumps(treino, ensure_ascii=False).replace('</', '<\\/')
    out = (cabeca('../../../', titulo, descr, True) + topo('../../', '../', atual, migalha) + corpo + rodape('../../', '../', '../../../', pe) +
           '<script type="application/json" id="treino-dados">%s</script>\n</body></html>\n' % dados)
    return 'exame/treinos/%s/index.html' % pid, out


ETQ = {'oficial': 'Item oficial', 'adaptado': 'Item adaptado', 'treino': 'Exercício de treino'}


def etq(t):
    return '<span class="etq %s">%s</span>' % (t, ETQ[t])


LEGENDA = ('<ul class="legenda">'
           '<li>' + etq('oficial') + 'Texto dos documentos de 2026, com a página. O enunciado, as opções, a cotação, os critérios e o que vem entre aspas estão como no original; os títulos e as frases de ligação são nossos.</li>'
           '<li>' + etq('adaptado') + 'Parte de um item oficial; diz sempre o que mudou.</li>'
           '<li>' + etq('treino') + 'Feito por nós. Não vem de nenhuma prova.</li></ul>')


# ---------- tabelas oficiais ----------
def tabela_niveis(niveis, legenda):
    linhas = ''
    for n in niveis:
        alts = []
        for alt in n['descritores']:
            if len(alt) > 1 and alt[0].rstrip().endswith(':'):
                alts.append('<p>%s</p><ul class="top">%s</ul>' % (md(alt[0]), ''.join('<li>%s</li>' % md(x) for x in alt[1:])))
            else:
                alts.append(''.join('<p>%s</p>' % md(x) for x in alt))
        linhas += '<tr><td class="c">%s</td><td>%s</td><td class="c">%s</td></tr>' % (n['nivel'], '<span class="ou">OU</span>'.join(alts), n['pontuacao'])
    return ('<div class="rolo" tabindex="0" role="region" aria-label="%s"><table><caption class="so-leitor">%s</caption>'
            '<thead><tr><th class="c">Nível</th><th>Descritor de desempenho</th><th class="c">Pontuação</th></tr></thead><tbody>%s</tbody></table></div>') % (esc(legenda), esc(legenda), linhas)


def tabela_cl(chave):
    t = F1['criterios']['tabelas_CL'][chave]
    assert t == F2['criterios']['tabelas_CL'][chave]
    maxa = max(int(k[1:]) for linha in t['erros_B'].values() for k in linha)
    cab = ''.join('<th class="c" scope="col">%d</th>' % a for a in range(maxa + 1))
    linhas = ''
    for b in sorted(t['erros_B'], key=int):
        cels = ''
        for a in range(maxa + 1):
            v = t['erros_B'][b].get('A%d' % a)
            if v is None:
                cels += '<td class="c vazia"></td>'
            else:
                cels += '<td class="c">%s</td>' % v
        linhas += '<tr><th class="c" scope="row">%s</th>%s</tr>' % (b, cels)
    leg = 'Tabela de correção linguística: linhas, número de erros do tipo B; colunas, número de erros do tipo A; valor, pontuação'
    return ('<div class="rolo" tabindex="0" role="region" aria-label="%s"><table class="cl"><caption class="so-leitor">%s</caption>'
            '<thead><tr><th class="c">Erros do tipo B ↓ / do tipo A →</th>%s</tr></thead><tbody>%s</tbody></table></div>') % (leg, leg, cab, linhas)


def lint(nome, texto_nosso):
    """Regras de língua sobre o texto que é nosso (fora das citações oficiais)."""
    probs = []
    for pal in ['professor', 'jogar', 'jogo', 'ficha', 'folha', '—', '·', 'sozinho', 'sozinha']:
        for m in re.finditer(re.escape(pal), texto_nosso, flags=re.I):
            probs.append((pal, texto_nosso[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')))
    for m in re.finditer(r'\bQual (?!das\b|dos\b|destas\b|destes\b|é\b|foi\b|delas\b|deles\b)\w+', texto_nosso):
        probs.append(('Qual+nome', texto_nosso[max(0, m.start() - 30):m.end() + 40]))
    # títulos de obras em itálico
    for m in re.finditer(r'(?<!<i>)Dicionário Terminológico', texto_nosso):
        probs.append(('título sem itálico', texto_nosso[max(0, m.start() - 30):m.end() + 30]))
    if probs:
        raise SystemExit('Regras de língua, %s: %r' % (nome, probs))
    return probs
