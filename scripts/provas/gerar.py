#!/usr/bin/env python3
"""Provas em cartões: gera as lições (uma por grupo da prova) e a secção exame/provas/ a partir dos dados.

Generaliza as ferramentas do piloto (Prova 639, 1.ª fase, 2026, versão 2; gerar_paginas.py, 29/10/2026), como pedia o
resumo do piloto, antes da segunda prova. Cada prova é uma pasta scripts/provas/dados/AAAA-Nf/ com:
* prova.json: prova, ano, fase e versao (daí saem a pasta AAAA-Nf, as chaves do progresso prova-AAAA-Nf-gN e a
  transcrição tests/fixtures/prova-639-AAAA-Nf-vN.json, que tem de dizer o mesmo), a versão da lição (versao_licao,
  gravada com o progresso), a autoria e as cópias, e por grupo as ligações aos módulos e às sessões e o texto do cartão
  na secção; opcionalmente, a imagem com direitos de um grupo (ver abaixo);
* grupo-i.json, grupo-ii.json, grupo-iii.json: título, «aprendes» e cartões (o desenho; é aqui que se editam os cartões).
A transcrição conferida (a fixture dos testes) dá as fontes dos textos, os endereços dos PDF, a duração e a cotação.
scripts/provas/dados/seccao.json dá as provas previstas, pela ordem do docente: as que já têm dados entram na secção
como blocos (a mais recente primeiro) e as outras ficam em «O que vem a seguir».

Saídas: exame/provas/AAAA-Nf/grupo-{i,ii,iii}/index.html e exame/provas/index.html.
O molde das lições é o do piloto: a forma leve (lesson.css, casca.js e jogo.js externos) com os blocos mg-css, amp-css,
casca-pc e amp-js copiados, em tempo de geração, da lição m5/licao-m5-f10 (já sem a Sala: falha se tiverem código dela).

Transformações gerais, para todas as provas (as duas primeiras são as do piloto):
* o número da linha da prova não se lê nos leitores de ecrã (span.n com aria-hidden);
* (30/10/2026) prosa em texto corrido: nos excertos repetidos (linhas sem data-l), cada linha leva o seu número em data-n,
  para se ver como nas outras (provas-licao.css), e a linha que não segue a anterior leva a classe «salto»;
* imagem com direitos (por exemplo, o cartoon do Grupo III): com «reproduzir»: false (por omissão), a figura dos cartões
  «ler» dá lugar a uma ligação para a página do enunciado em PDF, com a página escrita no texto (no telemóvel, o #page
  costuma ser ignorado), e cada campo «ver» passa a essa ligação; o cartão «Abre» troca a frase indicada em
  «abre_sem_imagem». Com «reproduzir»: true (ou --com-imagem), a figura fica e o ficheiro tem de estar no repositório.

Antes de escrever, cada grupo passa em scripts/audit_cards.validate_cards (o tipo «item» valida-se como «escolha»), cada
cartão de fazer tem o seu «g» e a página relida com audit_cards.lesson_cards dá os mesmos cartões.

Uso: python3 scripts/provas/gerar.py [--saida PASTA] [--verificar] [--com-imagem] [AAAA-Nf ...]
  sem pastas, gera todas as provas com dados; a secção gera-se sempre com todas;
  --saida escreve noutra raiz (os testes comparam assim, sem mexer na árvore);
  --verificar não escreve nada e sai com 1 se algum ficheiro gerado for diferente do que está na árvore.
Idempotente: só reescreve um ficheiro quando o conteúdo muda.
"""
import argparse
import copy
import html
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DADOS = Path(__file__).resolve().parent / 'dados'
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_cards as A  # noqa: E402

MOLDE = 'm5/licao-m5-f10/index.html'
ANO_LETIVO = '2026/2027'
R = '../../../../'  # das lições (exame/provas/AAAA-Nf/grupo-x/) à raiz do sítio
# Versões de cache dos ficheiros partilhados (mudam com os ficheiros, não com as provas).
V = {
    'provas-licao.css': '20261030-excertos-1', 'provas-licao.js': '20261029-provas-1', 'aula-clara.css': '20261023',
    'jogo.js': '20261021-ux06', 'rever-frase.js': '20261021', 'appearance.css-licao': '20261025-reading1',
    'appearance.js': '20261025-universal-1', 'projection-launcher.js': '20261019.4',
    'exame.css': '20261029-provas-1', 'appearance.css': '20261025-universal-1', 'oficina.css': '20261029-provas-1',
    'provas.css': '20261030-provas-2', 'provas.js': '20261029-provas-1',
}
ROMANOS = ['I', 'II', 'III', 'IV', 'V']
EXTENSO = {3: 'três'}
PROIBIDO_NO_MOLDE = ('ntfy', 'EventSource', 'BroadcastChannel', 'EPISala', 'epi-sala', 'painel-sala')


class Falha(Exception):
    pass


def it_html(s):
    """_itálico_ dos dados da transcrição para HTML (só nas fontes)."""
    return re.sub(r'_([^_]+)_', r'<i>\1</i>', html.escape(s, quote=False))


def textos_do_grupo(gfx):
    """Os textos de um grupo da transcrição, onde quer que estejam (no grupo ou nas partes), pela ordem da prova."""
    return list(gfx.get('textos', [])) + [t for p in gfx.get('partes', []) for t in p.get('textos', [])]


def imagem_do_grupo(gfx):
    for it in gfx.get('itens', []) + [i for p in gfx.get('partes', []) for i in p.get('itens', [])]:
        if it.get('imagem'):
            return it['imagem']
    return gfx.get('imagem')


class Prova:
    """Uma prova: os parâmetros (prova.json), a transcrição (fixture) e os grupos (desenhos)."""

    def __init__(self, pasta_dados, com_imagem=False):
        self.dados = pasta_dados
        self.cfg = json.loads((pasta_dados / 'prova.json').read_text('utf-8'))
        c = self.cfg
        self.codigo, self.ano, self.fase, self.versao = str(c['prova']), int(c['ano']), int(c['fase']), int(c['versao'])
        self.pasta = f'{self.ano}-{self.fase}f'
        if pasta_dados.name != self.pasta:
            raise Falha(f'{pasta_dados}: a pasta tem de se chamar {self.pasta} (ano {self.ano}, fase {self.fase})')
        self.fixture = ROOT / 'tests/fixtures' / f'prova-{self.codigo}-{self.pasta}-v{self.versao}.json'
        if not self.fixture.is_file():
            raise Falha(f'{self.pasta}: falta a transcrição conferida {self.fixture.relative_to(ROOT)}')
        self.fx = json.loads(self.fixture.read_text('utf-8'))
        p = self.fx['prova']
        if (str(p['codigo']), int(p['ano']), int(p['versao'])) != (self.codigo, self.ano, self.versao) or \
                not p['fase'].startswith(f'{self.fase}.ª'):
            raise Falha(f'{self.pasta}: a transcrição diz prova {p["codigo"]}, {p["fase"]}, {p["ano"]}, versão {p["versao"]}')
        self.fase_rot = f'{self.fase}.ª fase'
        self.nome = f'Prova {self.codigo}, {self.fase_rot}, {self.ano}'
        self.titulo_exame = p['titulo']
        f = p['fontes']
        self.url_enunciado, self.url_criterios = f['enunciado_url'], f['criterios_url']
        self.url_enunciado_orig, self.url_criterios_orig = f.get('enunciado_original_url'), f.get('criterios_original_url')
        self.n_grupos = len(self.fx['grupos'])
        if self.n_grupos != 3 or len(c['grupos']) != 3:
            raise Falha(f'{self.pasta}: a prova tem de ter três grupos, na transcrição e em prova.json')
        self.img = c.get('imagem')
        self.mostra_imagem = bool(self.img and (self.img.get('reproduzir') or com_imagem))
        self.grupos = []
        for g in range(1, self.n_grupos + 1):
            slug = 'grupo-' + ROMANOS[g - 1].lower()
            D = json.loads((pasta_dados / f'{slug}.json').read_text('utf-8'))
            gc = c['grupos'][g - 1]
            self.grupos.append({'g': g, 'nome': ROMANOS[g - 1], 'slug': slug, 'D': D, 'cfg': gc, 'fx': self.fx['grupos'][g - 1],
                                'chave': f'prova-{self.pasta}-g{g}', 'versao_licao': gc.get('versao_licao', c['versao_licao'])})

    # ---------- textos que se repetem ----------
    def autor(self, curto=False):
        nota = self.cfg.get('autoria', {}).get('nota')
        if curto:
            base = 'Autor: IAVE, como indica a página de onde vêm as cópias'
        else:
            base = ('Autor da prova e dos critérios de classificação: IAVE, como indica a página de onde vêm as cópias '
                    '(«documentos oficiais do IAVE»)')
        return base + (f'; {nota}' if nota else '') + '.'

    def ligacoes_pdf(self, curto=False):
        a = '" target="_blank" rel="noopener">'
        aut = self.cfg.get('autoria', {})
        host = re.sub(r'^www\.', '', re.match(r'https?://([^/]+)', self.url_enunciado).group(1))
        s = (f'Cópias públicas: <a href="{self.url_enunciado}{a}enunciado (PDF)</a> e '
             f'<a href="{self.url_criterios}{a}critérios (PDF)</a>' + ('' if curto else f', em {host}') + '.')
        if self.url_enunciado_orig and self.url_criterios_orig:
            onde = '' if curto or not aut.get('originais_em') else f' em {aut["originais_em"]}'
            s += (f' Originais{onde}: <a href="{self.url_enunciado_orig}{a}enunciado da versão {self.versao} (PDF)</a> e '
                  f'<a href="{self.url_criterios_orig}{a}critérios (PDF)</a>.')
        if not curto and aut.get('nota_copias'):
            s += ' ' + aut['nota_copias']
        return s

    def fontes_textos(self, G):
        fs = [t['fonte'] for t in textos_do_grupo(G['fx'])]
        partes = []
        if len(fs) == 1:
            partes.append('Texto, como a prova o indica: ' + it_html(fs[0]))
        elif fs:
            partes.append('Textos, como a prova os indica: ' + '; '.join(it_html(f.rstrip('.')) for f in fs) + '.')
        img = imagem_do_grupo(G['fx'])
        if img:
            partes.append(f'Imagem, como a prova a indica: {it_html(img["tipo"])} da autoria de {html.escape(img["autor"], quote=False)}; '
                          + html.escape(img['fonte'], quote=False))
        return ' '.join(partes)

    def pdf_pagina(self):
        return f'{self.url_enunciado}#page={self.img["pagina_pdf"]}'


# ---------- molde, sessões e lições ligadas ----------

def molde():
    s = (ROOT / MOLDE).read_text('utf-8')
    out = []
    for tag, ident in (('style', 'mg-css'), ('style', 'amp-css'), ('style', 'casca-pc'), ('script', 'amp-js')):
        m = re.findall(r'<%s id="%s">(.*?)</%s>' % (tag, ident, tag), s, re.S)
        if len(m) != 1:
            raise Falha(f'o molde mudou: <{tag} id="{ident}"> não aparece uma vez em {MOLDE}')
        for proibido in PROIBIDO_NO_MOLDE:
            if proibido in m[0]:
                raise Falha(f'o bloco {ident} de {MOLDE} tem código da Sala ({proibido})')
        out.append(m[0])
    return out


SESSOES = {s['id']: s for s in json.loads((ROOT / 'assets/exame/sessoes.json').read_text('utf-8'))['sessions']}


def titulo_de(rel):
    """O nome de uma página ligada no fim da lição, a partir do seu <title>, sem «·» (regra de escrita): «Lição M3-F09: …»
    dá «M3-F09: …»; «A lírica de Camões · As obras · Português» dá «As obras: A lírica de Camões»; as outras páginas dos
    módulos (30/10/2026), «Ler a fundo · X» dá «M3, ler a fundo: X» e «X · Português · Módulo 3» dá «M3: X»."""
    t = re.search(r'<title>([^<]*)</title>', (ROOT / rel / 'index.html').read_text('utf-8')).group(1)
    t = t.replace('Lição ', '')
    if ' · As obras' in t:
        return 'As obras: ' + t.split(' · ')[0]
    if ' · ' in t:
        partes = [x for x in t.split(' · ') if x != 'Português' and not re.fullmatch(r'Módulo \d+', x)]
        mod = re.match(r'm(\d)/', rel)
        if not mod:
            raise Falha(f'{rel}: título com «·» fora dos módulos e das obras ({t})')
        if partes[0] == 'Ler a fundo' and len(partes) == 2:
            return f'M{mod.group(1)}, ler a fundo: {partes[1]}'
        return f'M{mod.group(1)}: ' + ': '.join(partes)
    return t


# ---------- cartões ----------

BLOCO_PROSA = re.compile(r'(<div class="v prova-l">)(.*?)(</div>)', re.S)
LINHA = re.compile(r'<span class="(ln(?: par)?)"((?: data-l="[^"]*")?)><span class="n" aria-hidden="true">(\d*)</span>')


def numerar_excertos(h, onde):
    """Prosa da prova em texto corrido (provas-licao.css): cada linha mostra o seu número, que vem de data-l. Nos excertos
    repetidos (linhas sem data-l, como «As linhas do item»), o número vai para data-n, contado a partir das linhas com
    número (data-l, ou o número do span.n); uma linha que não segue a anterior (o excerto salta linhas) leva a classe
    «salto» e começa numa linha nova do ecrã, para não ficar colada à anterior como se fossem seguidas (30/10/2026)."""
    def bloco(m):
        linhas = list(LINHA.finditer(m.group(2)))
        conhecidos = []
        for x in linhas:
            dl = re.search(r'(\d+)"$', x.group(2)) if x.group(2) else None
            conhecidos.append(int(dl.group(1)) if dl else (int(x.group(3)) if x.group(3) else None))
        if all(n is None for n in conhecidos):
            return m.group(0)
        nums = list(conhecidos)
        k0 = next(k for k, n in enumerate(nums) if n is not None)
        for k in range(k0 - 1, -1, -1):  # antes do primeiro número: linhas seguidas
            nums[k] = nums[k + 1] - 1
        for k in range(k0 + 1, len(nums)):
            if nums[k] is None:
                nums[k] = nums[k - 1] + 1
        # um salto entre linhas sem número é ambíguo: o excerto tem de dar o número de todas as linhas (todos_numeros)
        for k in range(1, len(nums)):
            if conhecidos[k] is not None and nums[k - 1] + 1 != conhecidos[k] and conhecidos[k - 1] is None:
                raise Falha(f'{onde}: o excerto salta linhas ({nums[k - 1]} para {conhecidos[k]}) sem o número de cada linha')
        out, fim = [], 0
        for k, x in enumerate(linhas):
            classe, dl, n = x.group(1), x.group(2), x.group(3)
            if k and nums[k] != nums[k - 1] + 1:
                classe += ' salto'
            dn = '' if dl else f' data-n="{nums[k]}"'
            out.append(m.group(2)[fim:x.start()] + f'<span class="{classe}"{dl}{dn}><span class="n" aria-hidden="true">{n}</span>')
            fim = x.end()
        return m.group(1) + ''.join(out) + m.group(2)[fim:] + m.group(3)
    return BLOCO_PROSA.sub(bloco, h)


def preparar(P, G):
    """Os cartões do desenho com as transformações gerais (número da linha e imagem com direitos)."""
    cartoes = copy.deepcopy(G['D']['cartoes'])
    for k, c in enumerate(cartoes):
        if c.get('t') == 'ler' and 'html' in c:
            c['html'] = c['html'].replace('<span class="n">', '<span class="n" aria-hidden="true">')
            c['html'] = numerar_excertos(c['html'], f'{P.pasta} {G["slug"]} cartão {k + 1}')
    img = P.img
    if img and img['grupo'] == G['g']:
        nome_ficheiro = Path(img['ficheiro']).name
        if P.mostra_imagem:
            if not (ROOT / img['ficheiro']).is_file():
                raise Falha(f'{P.pasta}: para reproduzir a imagem, {img["ficheiro"]} tem de estar no repositório')
        else:
            pag, tot, url = img['pagina_pdf'], img['paginas_pdf'], P.pdf_pagina()
            ligacao = (f'<p class="prova-imagem">A imagem está na p. {pag} da prova: <a href="{url}" target="_blank" '
                       'rel="noopener">abre o enunciado (PDF) nessa página</a> e deixa-o aberto ao lado. Os cartões seguintes pedem-te '
                       'que olhes para ela.</p>')
            ligacao_caderno = (f'<p class="prova-imagem">A imagem: <a href="{url}" target="_blank" '
                               f'rel="noopener">enunciado da prova (PDF), p. {pag}</a>.</p>')
            ver = (f'<a class="ver-pdf" href="{url}" target="_blank" rel="noopener">'
                   f'Ver a imagem: enunciado da prova (PDF), p. {pag} de {tot}</a>')
            if img.get('abre_sem_imagem'):
                velho, novo = img['abre_sem_imagem']
                if cartoes[0]['html'].count(velho) != 1:
                    raise Falha(f'{P.pasta} {G["slug"]}: a frase de abre_sem_imagem não aparece uma vez no cartão «Abre»')
                cartoes[0]['html'] = cartoes[0]['html'].replace(velho, novo)
            fonte_img = imagem_do_grupo(G['fx'])['fonte']
            fig = re.compile(r'<figure class="fig inteiro cor">.*?</figure>', re.S)
            for k, c in enumerate(cartoes):
                if 'ver' in c:
                    c['ver'] = ver
                if c.get('t') == 'ler' and '<figure' in c.get('html', ''):
                    if len(fig.findall(c['html'])) != 1:
                        raise Falha(f'{P.pasta} {G["slug"]} cartão {k + 1}: mais de uma figura')
                    legenda = re.search(r'<figcaption>(.*?)</figcaption>', c['html'], re.S).group(1)
                    if legenda != fonte_img:
                        raise Falha(f'{P.pasta} {G["slug"]} cartão {k + 1}: a legenda da figura não é a fonte que a prova dá')
                    troca = ligacao if c.get('rot') == 'A prova' else ligacao_caderno
                    c['html'] = fig.sub(lambda _m: troca + f'<p class="fonte">Fonte da imagem, como a prova a indica: {legenda}</p>', c['html'])
            if nome_ficheiro in json.dumps(cartoes):
                raise Falha(f'{P.pasta} {G["slug"]}: a imagem {nome_ficheiro} continua nos cartões')
    erros = A.validate_cards([dict(c, t='escolha') if c.get('t') == 'item' else c for c in cartoes])
    if erros:
        raise Falha(f'{P.pasta} {G["slug"]}: ' + '; '.join(map(str, erros)))
    gs = [c.get('g') for c in cartoes if c['t'] != 'ler']
    if len(gs) != len(set(gs)) or None in gs:
        raise Falha(f'{P.pasta} {G["slug"]}: «g» repetido ou em falta nos cartões de fazer')
    return cartoes


# ---------- a página de cada grupo ----------

CASA = '<svg class="c-casa" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8.2 8 2.6l6 5.6M4 7v7h3v-4h2v4h3V7"/></svg>'
MG_CASA = '<svg viewBox="0 0 16 16" aria-hidden="true" class="mg-casa"><path d="M2 8.2 8 2.6l6 5.6M4 7v7h3v-4h2v4h3V7"/></svg>'
AO_DEPOIS = ('function(el){Array.prototype.forEach.call(el.querySelectorAll("a[data-licao]"),function(a){var s=null;'
             'try{s=JSON.parse(localStorage.getItem("licao-"+a.getAttribute("data-licao"))||"null")}catch(e){}'
             'var e=a.querySelector("[data-estado]");if(s&&s.lida){a.classList.add("feito");if(e)e.textContent="feita"}})}')


def depois_html(P, G):
    g, n = G['g'], P.n_grupos
    gr = P.grupos
    ant = f'<a href="../{gr[g - 2]["slug"]}/">← Grupo {gr[g - 2]["nome"]}</a>' if g > 1 else '<a href="../../">← Provas em cartões</a>'
    seg = f'<a href="../{gr[g]["slug"]}/">Grupo {gr[g]["nome"]} →</a>' if g < n else '<a href="../../">Provas em cartões →</a>'
    links = []
    for rel in G['cfg']['licoes']:
        dado = f' data-licao="{rel.split("/")[-1].replace("licao-", "")}"' if '/licao-' in rel else ''
        estado = '<span class="estado" data-estado></span>' if dado else ''
        links.append(f'<a class="pe-l" href="{R}{rel}/"{dado}><span class="pe-t">{html.escape(titulo_de(rel), quote=False)}</span>{estado}<span class="pe-s" aria-hidden="true">→</span></a>')
    sess = []
    for sid in G['cfg']['sessoes']:
        sess.append(f'<a class="pe-l" href="{R}exame/#{sid}"><span class="pe-t">Sessão {int(sid[1:])}: {html.escape(SESSOES[sid]["title"], quote=False)}</span><span class="pe-s" aria-hidden="true">→</span></a>')
    return (f'<div class="prox">{ant}{seg}</div>'
            f'<nav class="portas-ext" aria-label="Onde se estuda"><p class="pe-rot">Onde se estuda nos módulos</p>{"".join(links)}</nav>'
            f'<nav class="portas-ext" aria-label="Na preparação de exame"><p class="pe-rot">Na preparação de exame</p>{"".join(sess)}</nav>')


def pagina(P, G, cartoes, blocos):
    MG_CSS, AMP_CSS, CASCA_PC, AMP_JS = blocos
    g, nome, n = G['g'], G['nome'], P.n_grupos
    gr, D = P.grupos, G['D']
    ancora = f'../../#prova-{P.pasta}'
    titulo = f'{P.nome}: Grupo {nome}'
    h1 = f'{P.nome}, Grupo {nome}: {D["titulo"]}'
    aprendes = D['aprendes'] if D['aprendes'].startswith('Aprendes') else 'Aprendes ' + D['aprendes'][0].lower() + D['aprendes'][1:]
    desc = html.escape(re.sub(r'_([^_]+)_', r'\1', aprendes))
    vizinhos = []
    if g > 1:
        vizinhos.append(f'<a href="../{gr[g - 2]["slug"]}/">Grupo anterior: Grupo {gr[g - 2]["nome"]}</a>')
    if g < n:
        vizinhos.append(f'<a href="../{gr[g]["slug"]}/">Grupo seguinte: Grupo {gr[g]["nome"]}</a>')
    img_menu = ''
    if P.img and P.img['grupo'] == g and not P.mostra_imagem:
        img_menu = (f'<a href="{P.pdf_pagina()}" target="_blank" rel="noopener">A imagem do Grupo {nome} '
                    f'(enunciado, p. {P.img["pagina_pdf"]}, PDF)</a>')
    menu_links = ''.join(vizinhos) + (
        f'<a href="{ancora}">Os {EXTENSO[n]} grupos desta prova</a>' + img_menu
        + f'<a href="{P.url_enunciado}" target="_blank" rel="noopener">Enunciado da prova (PDF)</a>'
        f'<a href="{P.url_criterios}" target="_blank" rel="noopener">Critérios de classificação (PDF)</a>'
        f'<a href="{R}como/">Como se faz (vídeos)</a>')
    fonte_menu = (f'EPI, Escola Profissional de Imagem. Português {ANO_LETIVO}. Provas em cartões: Grupo {nome} do {P.titulo_exame}, '
                  f'{P.nome}, versão {P.versao}. {P.autor()} {P.ligacoes_pdf()} {P.fontes_textos(G)} '
                  'São nossos os cartões de preparação, as explicações e os exemplos; o que é da prova e dos critérios está dito '
                  'em cada cartão. O que marcas fica só neste aparelho.')
    aprendes_html = html.escape(aprendes, quote=False)
    aprendes_html = re.sub(r'_([^_]+)_', r'<i>\1</i>', aprendes_html)
    aprendes_html = re.sub(r'(?<![>\w])cartoon(?!\w)', '<i>cartoon</i>', aprendes_html)
    seguinte = (f',seguinte:"../{gr[g]["slug"]}/",seguinteRotulo:"Grupo {gr[g]["nome"]}"' if g < n
                else ',voltarRotulo:"Voltar às provas"')
    dados = json.dumps(cartoes, ensure_ascii=False).replace('</', '<\\/')
    if '</script' in dados.lower():
        raise Falha(f'{P.pasta} {G["slug"]}: </script dentro dos cartões')
    montar = (f'EPIJogo.montar({{casca:C,el:document.getElementById("baralho"),itens:CARTOES,chave:K,marca:"{P.codigo}",'
              f'titulo:"Grupo {nome}",variar:false,versao:"{G["versao_licao"]}",percurso:"{ancora}",'
              f'percursoRotulo:"Provas em cartões"{seguinte},depois:{json.dumps(depois_html(P, G), ensure_ascii=False)},'
              f'aoDepois:{AO_DEPOIS}}})')
    rever = (f'<script defer src="{R}assets/pt-lessons/rever-frase.js?v={V["rever-frase.js"]}"></script>'
             if any(c['t'] == 'rever' for c in cartoes) else '')
    menu_aprendes = aprendes_html[len("Aprendes "):] if aprendes_html.startswith("Aprendes ") else aprendes_html
    return f'''<!doctype html><html lang="pt-PT" data-appearance-site="pt" data-appearance-family="cards"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,interactive-widget=resizes-content"><title>{titulo}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Special+Elite&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/pt-lessons/lesson.css"><link rel="stylesheet" href="{R}assets/pt-lessons/aula-clara.css?v={V["aula-clara.css"]}"><link rel="stylesheet" href="{R}assets/exame/provas-licao.css?v={V["provas-licao.css"]}">
<style id="mg-css">{MG_CSS}</style><style id="amp-css">{AMP_CSS}</style><style id="casca-pc">{CASCA_PC}</style>
<script defer src="{R}assets/pt-lessons/casca.js"></script><script defer src="{R}assets/pt-lessons/jogo.js?v={V["jogo.js"]}"></script>{rever}<script defer src="{R}assets/exame/provas-licao.js?v={V["provas-licao.js"]}"></script>
<link rel="stylesheet" href="{R}assets/appearance.css?v={V["appearance.css-licao"]}"><script src="{R}assets/appearance.js?v={V["appearance.js"]}"></script></head><body>
<div class="casca" data-casca>
<header class="casca-topo"><a class="c-marca" href="{ancora}" aria-label="Voltar às provas em cartões">{CASA}{P.codigo}</a><span class="c-num" data-c-num></span><button type="button" class="c-barra" data-c-barra aria-label="Ver os cartões já feitos" disabled><svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg></button><span class="c-modo" data-c-modo hidden></span><button type="button" class="c-ic" data-c-como aria-label="Como se faz" title="Como se faz" hidden><span class="c-roda">?</span></button><button type="button" class="c-ic" data-c-som aria-pressed="false" aria-label="Som" title="Som ligado ou desligado"><span class="c-roda">♪</span></button><button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false" title="Menu"><span class="c-tres"></span></button></header>
<h1 class="c-sr">{html.escape(h1, quote=False)}</h1><main class="casca-corpo" id="casca-corpo" tabindex="-1"><div id="baralho" class="jogo-alvo"></div></main>
<footer class="casca-acoes" data-c-acoes></footer>
<section class="casca-folha" data-c-folha role="status" aria-live="polite" hidden></section>
<div class="casca-menu" data-c-painel hidden><div class="c-menu-in" role="dialog" aria-label="Menu"><div class="c-menu-cab"><p>{P.nome}<br>Grupo {nome} de {ROMANOS[n - 1]}</p><button type="button" class="c-ic" data-c-fecha-menu aria-label="Fechar o menu">✕</button></div><nav><ol class="c-migalhas" aria-label="Onde estás"><li style="--k:0"><a href="{R}">{MG_CASA}Página inicial</a></li><li style="--k:1"><a href="../../../">Preparação de exame</a></li><li style="--k:2"><a href="../../">Provas em cartões</a></li><li><span class="aqui" style="--k:3">Estás em: Grupo {nome}</span></li></ol>{menu_links}</nav><p class="c-menu-extra"><b>Aprendes:</b> {menu_aprendes}</p><p class="c-menu-extra">{fonte_menu}</p></div></div>
</div><div id="aviso" role="status"></div>
<noscript>Esta página precisa de JavaScript. <a href="../../">Voltar às provas em cartões</a>.</noscript>
<script>document.addEventListener("DOMContentLoaded",function(){{"use strict";var K="{G["chave"]}",CARTOES={dados};
var C=EPICasca.pagina();{montar};}});</script>
<script id="amp-js">{AMP_JS}</script>
<script defer src="{R}assets/projection-launcher.js?v={V["projection-launcher.js"]}" data-site="pt"></script></body></html>
'''


# ---------- a secção ----------

def bloco_prova(P, contagens):
    pv = P.pasta
    m = re.search(r'(\d+) minutos.*?Tolerância: (\d+) minutos', P.fx['prova']['duracao'])
    if not m:
        raise Falha(f'{pv}: a duração da transcrição não diz «N minutos… Tolerância: N minutos» ({P.fx["prova"]["duracao"]})')
    sobre = (f'Versão {P.versao} da prova. Na prova, {m.group(1)} minutos, mais {m.group(2)} de tolerância, para os '
             f'{EXTENSO[P.n_grupos]} grupos; {P.fx["cotacoes"]["total"]} pontos. Começa por qualquer grupo: cada um é uma lição.')
    lis = []
    for G in P.grupos:
        g, gc = G['g'], G['cfg']
        total, fazer = contagens[G['slug']]
        i = f'pv-{pv}-g{g}'
        lis.append(f'<li class="pv-grupo"><a href="{pv}/{G["slug"]}/" data-chave="{G["chave"]}" data-versao="{G["versao_licao"]}" '
                   f'aria-labelledby="{i}-n {i}-t {i}-e"><span class="pv-num" id="{i}-n">Grupo {G["nome"]}</span>'
                   f'<h3 id="{i}-t">{html.escape(G["D"]["titulo"], quote=False)}</h3><p class="pv-o-que">{gc["o_que"]}</p>'
                   f'<p class="pv-aprendes">{gc["aprendes"]}</p><p class="pv-meta">{total} cartões, {fazer} para responder. {gc["meta"]}<br>'
                   f'<span class="pv-estado" id="{i}-e" data-estado>Por fazer</span></p><span class="pv-abrir">Abrir o Grupo {G["nome"]} →</span></a></li>')
    fonte = (f'{P.titulo_exame}, {P.nome}, versão {P.versao}, e Critérios de Classificação da mesma prova. {P.autor(curto=True)} '
             f'{P.ligacoes_pdf(curto=True)} Textos da prova: {P.cfg["seccao"]["textos"]}. As referências completas estão em cada grupo.')
    # 30/10/2026: o ano e a fase dentro do título, para cada bloco (região e título) ter um nome diferente
    return (f'<section class="pv-prova" id="prova-{pv}" aria-labelledby="pv-{pv}"><div class="pv-cab">'
            f'<h2 id="pv-{pv}"><span class="pv-quando">{P.ano}, {P.fase_rot}</span> {P.titulo_exame}, Prova {P.codigo}</h2>'
            f'<p class="pv-sobre">{sobre}</p></div>\n'
            '<ol class="pv-grupos">\n' + '\n'.join(lis) + '\n</ol>\n'
            f'<p class="pv-fonte">{fonte}</p>\n</section>\n\n')


def seguir_html(provas, sec):
    feitas = {(P.ano, P.fase) for P in provas}
    por_ano = {}
    for ano, fase in sec['previstas']:
        if (ano, fase) not in feitas:
            por_ano.setdefault(ano, []).append(fase)
    itens = []
    for ano in sorted(por_ano, reverse=True):
        fases = sorted(por_ano[ano])
        rot = f'{ano}, {fases[0]}.ª fase' if len(fases) == 1 else f'{ano}, ' + ', '.join(f'{f}.ª' for f in fases[:-1]) + f' e {fases[-1]}.ª fases'
        itens.append(f'<li><b>{rot}</b>Em preparação.</li>')
    lista = f'<ol>{"".join(itens)}</ol>' if itens else ''
    return (f'<section class="pv-seguir" aria-labelledby="pv-seguir-titulo"><h2 id="pv-seguir-titulo">O que vem a seguir</h2>'
            f'{lista}<p>{sec["seguir"]}</p></section>\n\n')


def seccao(provas, contagens):
    sec = json.loads((DADOS / 'seccao.json').read_text('utf-8'))
    ordem = sorted(provas, key=lambda P: (P.ano, P.fase), reverse=True)
    blocos = ''.join(bloco_prova(P, contagens[P.pasta]) for P in ordem)
    return f'''<!doctype html>
<html lang="pt-PT" data-appearance-site="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Provas em cartões: Preparação de exame de Português</title><meta name="description" content="Os exames nacionais de Português (Prova 639) em cartões, grupo a grupo: o texto da prova com a numeração da prova, cada item desmontado em exercícios no ecrã e a resposta completa no caderno, com a grelha oficial à vista."><link rel="preload" href="../../assets/exame/fontes/fraunces-latin-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="../../assets/exame/fontes/ibm-plex-sans-latin-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="../../assets/exame/exame.css?v={V["exame.css"]}"><link rel="stylesheet" href="../../assets/appearance.css?v={V["appearance.css"]}"><link rel="stylesheet" href="../../assets/exame/oficina.css?v={V["oficina.css"]}"><link rel="stylesheet" href="../../assets/exame/provas.css?v={V["provas.css"]}"><script src="../../assets/appearance.js?v={V["appearance.js"]}"></script><script defer src="../../assets/exame/provas.js?v={V["provas.js"]}"></script><script defer src="../../assets/projection-launcher.js?v={V["projection-launcher.js"]}" data-site="pt"></script></head>
<body class="oficina"><a class="skip" href="#provas">Ir para as provas</a><nav class="migalhas" aria-label="Onde estás"><ol><li><a href="../../">Português</a></li><li><a href="../">Preparação de exame</a></li><li><span aria-current="page">Provas em cartões</span></li></ol></nav><header class="site-head of-cabeca"><a class="wordmark" href="../">Português<span>.</span><small>Preparação de exame</small></a><nav aria-label="Navegação da preparação"><a href="../">Sessões</a><a href="../laboratorio/">Laboratório de respostas</a><a href="./" aria-current="page">Provas em cartões</a></nav></header>
<main id="provas" tabindex="-1">
<section class="of-rosto" aria-labelledby="of-titulo"><h1 id="of-titulo">Provas em cartões</h1><p class="of-entrada">Os exames nacionais de Português, grupo a grupo. Lês o texto da prova com a numeração da prova e, a seguir a cada parte, fazes os cartões: o que pede o verbo, que linhas provam, o plano da resposta. A resposta completa escreve-se no caderno, com a grelha oficial à vista, e só depois a comparas com exemplos e com os critérios. Nos itens de escolha, tentas primeiro sozinho e depois vês porquê.</p><p class="of-estatuto-geral">Prova 639, 12.º ano, com os critérios de classificação</p></section>

{blocos}{seguir_html(provas, sec)}<section id="fontes" class="source of-colofao" aria-labelledby="fontes-titulo"><h2 id="fontes-titulo">O que é oficial e o que é nosso</h2><div class="of-colofao-texto"><p><strong>Oficial</strong>: o texto da prova, com a numeração das linhas e as notas, os enunciados, as opções, as chaves da versão indicada e as grelhas dos critérios, tal como estão na prova e nos critérios de classificação. Os cartões que os mostram dizem «da prova» ou «dos critérios».</p><p><strong>Nosso</strong>: os cartões de preparação, as explicações e as respostas de exemplo. Quando damos uma resposta possível, dizemos que é um exemplo e de onde vem. O sítio não corrige o que escreves no caderno: essa correção faz-se com a grelha oficial, por ti ou pelo docente.</p><p>O progresso de cada grupo fica só neste aparelho e viaja com o resto quando guardas o progresso num ficheiro na página inicial.</p></div></section>
</main>
<footer class="site-foot"><span>Português, EPI</span><a href="../">Sessões de preparação</a><a href="../laboratorio/">Laboratório de respostas</a><span>Os teus resultados ficam neste dispositivo.</span></footer></body></html>
'''


# ---------- principal ----------

def carregar(com_imagem=False):
    """Todas as provas com dados, da mais antiga para a mais recente."""
    provas = [Prova(p.parent, com_imagem) for p in sorted(DADOS.glob('*/prova.json'))]
    return sorted(provas, key=lambda P: (P.ano, P.fase))


def gerar(com_imagem=False, so=None):
    """{caminho relativo: conteúdo} de tudo o que o gerador escreve (as lições das provas pedidas e a secção)."""
    provas = carregar(com_imagem)
    blocos = molde()
    saida, contagens = {}, {}
    for P in provas:
        contagens[P.pasta] = {}
        for G in P.grupos:
            cartoes = preparar(P, G)
            contagens[P.pasta][G['slug']] = (len(cartoes), len([c for c in cartoes if c['t'] != 'ler']))
            if so and P.pasta not in so:
                continue
            rel = f'exame/provas/{P.pasta}/{G["slug"]}/index.html'
            saida[rel] = (pagina(P, G, cartoes, blocos), cartoes)
    if so:
        desconhecidas = set(so) - {P.pasta for P in provas}
        if desconhecidas:
            raise Falha('sem dados em scripts/provas/dados/: ' + ', '.join(sorted(desconhecidas)))
    saida['exame/provas/index.html'] = (seccao(provas, contagens), None)
    return saida, contagens


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--saida', help='raiz onde escrever (por omissão, a própria árvore)')
    ap.add_argument('--verificar', action='store_true', help='não escreve; sai com 1 se algum ficheiro for diferente')
    ap.add_argument('--com-imagem', action='store_true', help='reproduz as imagens com direitos (só com autorização do docente)')
    ap.add_argument('pastas', nargs='*', help='AAAA-Nf (por omissão, todas)')
    a = ap.parse_args(argv)
    try:
        saida, contagens = gerar(a.com_imagem, a.pastas or None)
    except Falha as e:
        print('ERRO:', e, file=sys.stderr)
        return 2
    raiz = Path(a.saida).resolve() if a.saida else ROOT
    diferentes = []
    with tempfile.TemporaryDirectory() as tmp:
        for rel, (conteudo, cartoes) in saida.items():
            alvo = raiz / rel
            atual = alvo.read_text('utf-8') if alvo.is_file() else None
            if atual != conteudo:
                diferentes.append(rel)
            if cartoes is not None:  # a página relida dá os mesmos cartões
                prova_lida = Path(tmp) / rel
                prova_lida.parent.mkdir(parents=True, exist_ok=True)
                prova_lida.write_text(conteudo, encoding='utf-8')
                if A.lesson_cards(prova_lida) != cartoes:
                    print(f'ERRO: {rel}: a página relida não dá os mesmos cartões', file=sys.stderr)
                    return 2
            if not a.verificar and atual != conteudo:
                alvo.parent.mkdir(parents=True, exist_ok=True)
                alvo.write_text(conteudo, encoding='utf-8')
    for pasta, grupos in contagens.items():
        print(pasta + ': ' + '; '.join(f'{slug} {t} cartões, {f} para responder' for slug, (t, f) in grupos.items()))
    if a.verificar:
        if diferentes:
            print('Diferentes do que está na árvore: ' + ', '.join(diferentes), file=sys.stderr)
            return 1
        print('Tudo igual ao que está na árvore.')
    else:
        print('Escritos: ' + (', '.join(diferentes) or 'nenhum (tudo igual)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
