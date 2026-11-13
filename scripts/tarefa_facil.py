"""Molde «mais fácil de fazer» das tarefas de unidade (12/11/2026: piloto na m3-u1, aprovado pelo docente nesse dia; a seguir,
o M3 inteiro, com a m3-u2).

Pedido do docente: «As tarefas de pt têm de ser mais fáceis de entender e os textos estudados têm de aparecer completos
para análise»; «as tarefas são para manter, mas é para ser mais fácil de fazer». A tarefa é a mesma (perguntas, temas,
números de palavras, grelha, aquecimento); muda a forma.

Só entra nas tarefas cujos dados (docs/pedagogia/tarefas-escolha/<slug>.json) têm a chave opcional «facil»; as outras
continuam a sair de scripts/tarefas_escolha.py, iguais byte a byte. Este módulo é chamado por esse gerador.

O que a chave «facil» traz (tudo texto público; nada da grelha nem da correção):
  kicker, fazer, modo, entregas, quadro, aquecer, perguntas, temas_titulo, temas_nota, temas, finais, verificar,
  entrega, rever, opcional_titulo e «textos» (os textos para análise, completos, com a origem em cada um).
O que continua a vir das chaves antigas: titulo, unidade, aquecer (ligação e minutos), exemplos (o exemplo das sílabas),
dossie e dossie_titulo, opcional, e a ligação à grelha, igual à de scripts/grelhas_tarefas.py.

Ordem de cada cartão de pergunta: o relógio de produção (só na primeira), o pedido, os exemplos com outros casos e, por
fim, os textos. Num tema, «figura» e «antes» ficam à vista antes dos passos; um passo {"t", "sub"} leva as suas condições.

M3 inteiro (12/11/2026, depois de o docente aprovar o piloto): uma pergunta pode ter «grupos» (cada um com a sua frase de
entrada e as suas alíneas; as letras continuam de um grupo para o outro) e «apoios» (um quadro copiado de uma lição, num
desdobrável fechado no ecrã que não sai em papel); no quadro de tempo e tamanho, uma célula de palavras também pode ocupar
várias linhas (a orientação que vale para as duas perguntas juntas). A m3-u1 não usa nenhuma destas chaves.

Quarta versão (achados de duas revisões): um modelo de divisão em sílabas à vista na pergunta 2; a letra do tema pede-se no
cartão do tema («temas_topo»), antes da verificação; no tema B, «dossiê» e «Texto 4» são ligações que abrem o desdobrável,
que fica antes do exemplo; em papel a fotografia sai larga, com uma só legenda (o crédito por extenso), e a nota da leitura
não fala dos exemplos; a descrição da página diz «duas perguntas».

Terceira versão (decisões do docente de 12/11/2026 e emagrecimento): «producao_minutos» dá a duração do relógio de produção;
«grelha_nota» fica por baixo da ligação à grelha; os exemplos ficam junto do pedido, num desdobrável fechado no ecrã que
não sai em papel (como as descrições do Kit); a verificação é uma só lista de perguntas de sim ou não; em papel sai só o que
é preciso para fazer a tarefa, sem páginas novas forçadas e sem partir um poema.

Textos: «estrofes» é uma lista de {"rotulo": opcional, "versos": [...]}; os versos numeram-se de «numerar» em «numerar»,
contando só versos (nunca rótulos como «Mote» e «Voltas»); «escolher» {"de", "ate", "frase"} marca com uma barra os versos
de onde se pode escolher. A fotografia («figura») lê-se da lição que a publica (chave «de»), para ser a mesma imagem.

M1 (13/11/2026, camada tarefas_faceis_m1_20261113: a m1-u1 e a m1-u2 no mesmo molde). Chaves novas, todas opcionais; as páginas
sem elas (a m3-u1 e a m3-u2) saem iguais, byte a byte:
  * um texto em prosa: «paragrafos», uma lista de {"n": "[1]", "t": texto, "partes": [...]} em vez de «estrofes» (os parágrafos
    numerados como nas lições; «partes» diz os pedaços das lições de que o parágrafo é feito, e junta-os só com espaço ou vírgula);
  * «folha_versao»: a versão da folha assets/task-textos.css que a página pede (a folha ganhou regras para a prosa e para as imagens;
    as páginas do M3 continuam a pedir a versão de antes);
  * numa pergunta, «intro»: uma frase antes das alíneas;
  * no cartão dos temas: «temas_figuras» (imagens que servem aos dois temas, numeradas, lidas pelo caminho que a lição usa, com o
    crédito completo atrás do «i»), «temas_comum» (o que o texto leva nos dois temas, um pedido por linha, com exemplos) e
    «temas_material» (textos que servem aos dois temas, num desdobrável fechado no ecrã e aberto em papel).

M5 (13/11/2026, camada tarefas_faceis_m5_20261113: a m5-u1 e a m5-u2 no mesmo molde, com passos de romances). Duas chaves novas,
opcionais; as páginas sem elas (as do M3 e as do M1) saem iguais, byte a byte:
  * num parágrafo de um texto em prosa, «html»: o mesmo parágrafo com os itálicos da lição (só <i>…</i>: o assento que Camilo
    transcreve, as palavras estrangeiras de Eça); tirados os itálicos, é o texto de «t», letra a letra;
  * num texto em prosa, «longo»: o texto pode passar de uma página em papel (parte-se só entre parágrafos, nunca dentro de um);
  * «nao_partir_dossie»: nos factos do dossiê (que vêm da chave antiga, igual à de antes), «1803 a 1805» e «cap. VI» não se partem.

M6 (13/11/2026, camada tarefas_faceis_m6_20261113: a m6-u1 e a m6-u2 no mesmo molde, com sonetos de Antero e as partes de «O Sentimento
dum Ocidental», de Cesário). Duas chaves novas, opcionais; as páginas sem elas (as do M3, do M1 e do M5) saem iguais, byte a byte:
  * num texto em verso, um verso pode ser {"falta": "[…]", "conta": n} em vez de uma linha: o que as lições não dão. Com «conta» 1,
    é um verso que falta e entra na numeração (o v. 13 de «A um poeta»); com «conta» 0, é um corte sem número (as quadras que a lição
    de «Ao Gás» salta). Nada se copia de fora: a linha de fonte do texto diz o que falta;
  * num texto em verso, «pagina»: uma parte longa do poema (44 versos) que em papel sai inteira numa só página, em letra mais pequena.
Revisão de 13/11/2026 (M6), mais duas, opcionais; as páginas sem elas saem iguais, byte a byte:
  * num texto em verso, «numerar» 0: os versos não levam número (os excertos de «Ao Gás»: com estrofes saltadas, um número contado
    por cima dos cortes não seria o número do verso na parte);
  * «juntos_em_papel»: em papel, os passos de um tema não se partem entre duas páginas, nem os factos do dossiê (classe tf-juntos).
"""
import re
from html import escape

LIGACAO = '<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>\n'
V_FACIL = '20261112-facil-7'
FOLHAS = ('<link rel="stylesheet" href="../../assets/info-i.css?v=20261105">'
          f'<link rel="stylesheet" href="../../assets/task-textos.css?v={V_FACIL}">'
          '<script defer src="../../assets/info-i.js?v=20261105"></script>')
MAIN = '<main class="task-page task-choice-page" data-task-compact data-task-choice>'
MAIN_FACIL = ('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil '
              'data-task-opening="Começar" data-task-index="nomes">')
DESCRICAO = ('aquecimento, núcleo comum e um tema à escolha', 'aquecimento, duas perguntas e um tema à escolha')
CURTO = 24  # até aqui, o texto sai inteiro numa página em papel (não se parte entre estrofes)
IMPRIMIR = ('<script>document.querySelectorAll("[data-task-print]").forEach(function(b){b.hidden=false;'
            'b.onclick=function(){window.print()}})</script>\n')


def lista(itens, tag='ol', cls='', inicio=1):
    """Uma lista. Um item {"t": texto, "sub": [...]} leva por baixo as condições desse passo (lista sem números)."""
    def item(x):
        return x if isinstance(x, str) else x['t'] + '<ul class="tf-cond">' + ''.join(f'<li>{y}</li>' for y in x['sub']) + '</ul>'
    return f'<{tag}{" class=" + chr(34) + cls + chr(34) if cls else ""}{f" start={chr(34)}{inicio}{chr(34)}" if inicio != 1 else ""}>' + ''.join(f'<li>{item(x)}</li>' for x in itens) + f'</{tag}>'


def quadro(q):
    """Um só quadro de tempo e tamanho. Uma célula {"t": texto, "linhas": n} ocupa n linhas (o tempo de escrita)."""
    cab = ''.join(f'<th scope="col">{c}</th>' for c in q['colunas'])
    corpo = []
    for linha in q['linhas']:
        cels = []
        for k, c in enumerate(linha):
            if c is None:
                continue
            span = ''
            if isinstance(c, dict):
                span, c = f' rowspan="{c["linhas"]}"', c['t']
            cels.append(f'<th scope="row{"group" if span else ""}"{span}>{c}</th>' if k == 0 else f'<td{span}>{c}</td>')
        corpo.append('<tr>' + ''.join(cels) + '</tr>')
    notas = ''.join(f'<p class="tf-nota">{n}</p>' for n in q.get('notas', []))
    return (f'<table class="tf-quadro"><caption>{q["titulo"]}</caption><thead><tr>{cab}</tr></thead>'
            f'<tbody>{"".join(corpo)}</tbody></table>{notas}')


def bloco_texto(t):
    """O texto para análise, completo e contínuo: título, versos numerados, vocabulário das lições e linha de fonte."""
    passo, esc, n, partes = t.get('numerar', 5), t.get('escolher'), 0, []
    if 'paragrafos' in t:
        # 13/11/2026 (M1): prosa. Os parágrafos numerados como nas lições ([1], [2]…), inteiros e seguidos.
        for x in t['paragrafos']:
            resto = x['t']
            for parte in x['partes']:  # o parágrafo é feito destes pedaços das lições, pela ordem, juntos só com espaço ou vírgula
                assert resto.lstrip(' ,').startswith(parte), (t['id'], x['n'], parte[:40])
                resto = resto.lstrip(' ,')[len(parte):]
            assert not resto.strip(), (t['id'], x['n'], resto)
            # 13/11/2026 (M5): com «html», o parágrafo sai com os itálicos da lição; sem os itálicos, é o texto de «t».
            assert 'html' not in x or re.sub(r'</?i>', '', x['html']) == escape(x['t'], quote=False), (t['id'], x['n'])
        corpo = '\n'.join(f'<p class="tt-par"><span class="tt-pn">{x["n"]}</span> {x.get("html") or escape(x["t"], quote=False)}</p>' for x in t['paragrafos'])
        gloss = ('<div class="tt-gloss"><p><b>Vocabulário</b></p><ul>'
                 + ''.join(f'<li><b>{p}</b>: {s}</li>' for p, s in t['glossario']) + '</ul></div>') if t.get('glossario') else ''
        return (f'<section class="tt-texto {"tt-longo" if t.get("longo") else "tt-curto"}" id="{t["id"]}" aria-labelledby="{t["id"]}-titulo">'
                f'<h3 id="{t["id"]}-titulo"><span class="tt-num">{t["rotulo"]}</span> {t["titulo"]}</h3>\n'
                f'<div class="tt-prosa">\n{corpo}\n</div>\n{gloss}'
                f'<p class="tt-fonte">{t["fonte"]}</p></section>\n')
    for e in t['estrofes']:
        if e.get('rotulo'):
            partes.append(f'<p class="tt-rotulo">{e["rotulo"]}</p>')
        versos = []
        for v in e['versos']:
            if isinstance(v, dict):
                # 13/11/2026 (M6): o que as lições não dão. Um verso que falta conta para a numeração; um corte não conta.
                assert set(v) == {'falta', 'conta'} and v['conta'] in (0, 1), (t['id'], v)
                n += v['conta']
                versos.append(f'<span class="tt-v tt-falta"><span class="tt-n">{n if v["conta"] and passo and n % passo == 0 else ""}</span>'
                              f'<span class="tt-l">{escape(v["falta"], quote=False)}</span></span>')
                continue
            n += 1
            marca = ' tt-esc' if esc and esc['de'] <= n <= esc['ate'] else ''
            versos.append(f'<span class="tt-v{marca}"><span class="tt-n">{n if passo and n % passo == 0 else ""}</span>'
                          f'<span class="tt-l">{escape(v, quote=False)}</span></span>')
        partes.append('<p class="tt-estrofe">' + '\n'.join(versos) + '</p>')
    frase = f'<p class="tt-escolher">{esc["frase"]}</p>' if esc and esc.get('frase') else ''
    gloss = ('<div class="tt-gloss"><p><b>Vocabulário</b></p><ul>'
             + ''.join(f'<li><b>{p}</b>: {s}</li>' for p, s in t['glossario']) + '</ul></div>') if t.get('glossario') else ''
    return (f'<section class="tt-texto{" tt-curto" if n <= CURTO else ""}{" tt-pagina" if t.get("pagina") else ""}" id="{t["id"]}" aria-labelledby="{t["id"]}-titulo">'
            f'<h3 id="{t["id"]}-titulo"><span class="tt-num">{t["rotulo"]}</span> {t["titulo"]}</h3>\n'
            f'{frase}<div class="tt-versos">\n' + '\n'.join(partes) + f'\n</div>\n{gloss}'
            f'<p class="tt-fonte">{t["fonte"]}</p></section>\n')


def onde_esta(o):
    """Texto protegido: não se copia; diz-se onde está e dá-se só o que as lições já publicam em citação curta.
    À vista ficam só os nomes («nomes»); as descrições das lições («lista») ficam num desdobrável, que não sai em papel."""
    return (f'<section class="tt-onde" id="{o["id"]}" aria-labelledby="{o["id"]}-titulo"><h3 id="{o["id"]}-titulo">{o["titulo"]}</h3>'
            + ''.join(f'<p class="tf-p">{p}</p>' for p in o['frases'])
            + (f'<p class="tf-p tf-ordem">{o["ordem"]}</p>' if o.get('ordem') else '')
            + f'<p class="tf-p"><b>{o["nomes_titulo"]}</b></p>' + lista(o['nomes'], 'ul', 'tt-nomes')
            + f'<details class="tf-so-tema tf-mais tf-so-ecra"><summary>{o["lista_titulo"]}</summary><div>{lista(o["lista"], "ul")}</div></details>'
            + f'<p class="tt-fonte">{o["fonte"]}</p></section>\n')


def alineas(p):
    """As alíneas de uma pergunta. Com «grupos», cada grupo tem a sua frase de entrada e as letras continuam (a, b, c; d, e)."""
    if not p.get('grupos'):
        return lista(p['alineas'], 'ol', 'tf-alineas')
    out, n = '', 1
    for g in p['grupos']:
        out += f'<p class="tf-p tf-grupo">{g["intro"]}</p>' + lista(g['alineas'], 'ol', 'tf-alineas', n)
        n += len(g['alineas'])
    return out


def apoios(xs):
    """Apoio copiado de uma lição (um quadro), num desdobrável fechado no ecrã que não sai em papel."""
    out = ''
    for x in xs:
        q = x['quadro']
        cab = ''.join(f'<th scope="col">{c}</th>' for c in q['colunas'])
        corpo = ''.join('<tr>' + ''.join(f'<th scope="row">{c}</th>' if k == 0 else f'<td>{c}</td>' for k, c in enumerate(l)) + '</tr>' for l in q['linhas'])
        out += (f'<details class="tf-so-tema tf-mais tf-so-ecra"><summary>{x["titulo"]}</summary><div>'
                f'<table class="tf-tabela"><caption>{q["titulo"]}</caption><thead><tr>{cab}</tr></thead><tbody>{corpo}</tbody></table>'
                + ''.join(f'<p class="tf-p">{n}</p>' for n in x.get('notas', [])) + '</div></details>\n')
    return out


def exemplos(xs, titulos):
    """Exemplos com outros casos, num desdobrável fechado no ecrã («Ver um exemplo com outro caso»), que não sai em papel. «contexto» diz de onde vem o caso; um parágrafo {"al": rótulo, "t": texto} diz a que
    alínea ou passo corresponde (o rótulo fica fora do texto copiado)."""
    def par(p):
        return f'<p class="tf-p">{p}</p>' if isinstance(p, str) else f'<p class="tf-p"><span class="tf-al">{p["al"]}</span> {p["t"]}</p>'
    if not xs:
        return ''
    return (f'<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>{titulos[min(len(xs), len(titulos)) - 1]}</summary><div>'
            + ''.join(f'<aside class="tf-exemplo"><h4>{x["titulo"]}</h4>'
                   + (f'<p class="tf-contexto">{x["contexto"]}</p>' if x.get('contexto') else '')
                   + (x.get('html') or ''.join(par(p) for p in x['paragrafos'])) + '</aside>\n' for x in xs) + '</div></details>\n')


def figura(f, raiz):
    """A fotografia é a que a lição publica (lê-se do ficheiro da lição, pelo texto alternativo), com o crédito completo
    atrás do «i» (peça assets/info-i.*, como no mapa do módulo) e a legenda à vista."""
    fonte = (raiz / f['de']).read_text('utf-8')
    if f.get('src'):
        # 13/11/2026 (M1): a imagem que a lição publica como ficheiro (img/fontes/…), pelo mesmo caminho e com o mesmo texto
        # alternativo; numerada («Imagem 1»), porque os passos dos temas se referem a ela, também em papel.
        assert f'<img src=\\"{f["src"]}\\" alt=\\"{f["alt"]}\\"' in fonte, (f['de'], f['src'])
        assert (raiz / 'tarefas' / 'x' / f['src']).resolve().is_file(), f['src']
        return (f'<figure class="tf-fig tf-fig-n" id="{f["id"]}"><p class="tf-fig-rotulo"><span class="tt-num">{f["rotulo"]}</span> {f["nome"]}</p>'
                f'<img src="{f["src"]}" alt="{f["alt"]}" width="{f["largura"]}" height="{f["altura"]}" loading="lazy">'
                f'<details class="info-i info-i--linha" name="info-i"><summary aria-label="{f["credito_rotulo"]}">'
                f'<span aria-hidden="true">i</span></summary><p class="info-i-texto">{f["credito"]}</p></details>'
                f'<figcaption>{f["legenda"]}</figcaption></figure>\n')
    m = re.search(r'<img src=\\"(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+)\\" alt=\\"' + re.escape(f['alt']) + r'\\"', fonte)
    assert m, f['de']
    return (f'<figure class="tf-fig"><img src="{m.group(1)}" alt="{f["alt"]}" width="{f["largura"]}" height="{f["altura"]}">'
            f'<details class="info-i info-i--linha" name="info-i"><summary aria-label="{f["credito_rotulo"]}">'
            f'<span aria-hidden="true">i</span></summary><p class="info-i-texto">{f["credito"]}</p></details>'
            f'<figcaption>{f["legenda"]}</figcaption></figure>\n')


def prender(texto):
    """13/11/2026 (M5): as referências de um facto do dossiê que não se partem (U+00A0): «1803 a 1805», «cap. VI». Fora das etiquetas.
    13/11/2026 (M6): também «verso 6» e «parte II» (os dossiês do M5 não têm nenhuma destas: as páginas do M5 saem iguais)."""
    partes = re.split(r'(<[^>]+>)', texto)
    for i in range(0, len(partes), 2):
        partes[i] = re.sub(r'\b(cap\.|capítulo) (?=[IVXLC]+\b)', '\\1\xa0', re.sub(r'(\d) (a|e|ou) (?=\d)', '\\1\xa0\\2\xa0', partes[i]))
        # 13/11/2026 (M6): e «verso 6» e «parte II», nos factos dos dossiês da m6-u1 e da m6-u2.
        partes[i] = re.sub(r'\b(versos?|parte) (?=\d|[IVXLC]+\b)', '\\1\xa0', partes[i])
    return ''.join(partes)


def dossie(titulo, factos, preso=False, juntos=False):
    li = ''.join(f'<li>{prender(x["facto"]) if preso else x["facto"]}<span class="tf-origem">Fonte: <a href="{x["href"]}">{x["fonte"]}</a></span></li>' for x in factos)
    return f'<section class="task-dossier tf-dossie{" tf-juntos" if juntos else ""}" aria-labelledby="dossie"><h4 id="dossie">{titulo}</h4><ol>{li}</ol></section>\n'


def opcoes(items):
    out = []
    for x in items:
        assert '"' not in x['resposta'] and '<' not in x['resposta'], x['resposta']
        out.append(f'<button type="button" aria-pressed="false" data-correct="{"true" if x["certa"] else "false"}" '
                   f'data-response="{x["resposta"]}"><span class="task-letter">{x["letra"]}<span class="sr-only">:</span></span> {x["texto"]}</button>')
    return ('<div class="task-options">' + ''.join(out)
            + '</div><p class="task-feedback" data-task-feedback role="status" aria-live="polite" hidden></p>')


def pagina(d, com_grelha, head, foot, raiz):
    """Devolve o HTML completo da página. head e foot são os de scripts/tarefas_escolha.py, já preenchidos."""
    f, slug, a = d['facil'], d['slug'], d['aquecer']
    textos = {t['id']: t for t in f['textos']}
    assert head.count(MAIN) == 1 and head.count('<link rel="stylesheet" href="../../assets/appearance.css') == 1, slug
    folhas = FOLHAS if not f.get('folha_versao') else FOLHAS.replace(f'task-textos.css?v={V_FACIL}', f'task-textos.css?v={f["folha_versao"]}')
    assert folhas.count('task-textos.css?v=') == 1, slug
    head = head.replace(MAIN, MAIN_FACIL).replace('<link rel="stylesheet" href="../../assets/appearance.css', folhas + '<link rel="stylesheet" href="../../assets/appearance.css')
    assert head.count('assets/task-reader.js?v=') == 1, slug
    head = re.sub(r'assets/task-reader\.js\?v=[^"]+', 'assets/task-reader.js?v=' + V_FACIL, head)
    # A descrição da página usa as palavras do enunciado novo («duas perguntas», não «núcleo comum»).
    assert head.count(DESCRICAO[0]) == 1, slug
    head = head.replace(*DESCRICAO)

    # Cartão 1, «Começar»: o que se faz (o passo 1 é o aquecimento e leva a única ligação), o relógio do aquecimento,
    # o que se entrega e o quadro.
    e = f['entregas']
    fazer = [f['fazer'][0] + f'<span class="task-aquecer tf-abrir"><a href="{a["cartoes"]}">{a["ligacao"]}</a></span>'] + f['fazer'][1:]
    comecar = (f'<header><p class="task-kicker">{f["kicker"]}</p><h1>{d["titulo"]}</h1>\n'
               f'<h2 class="task-part">O que vais fazer</h2>{lista(fazer, "ol", "tf-fazer")}<p class="tf-p">{f["modo"]}</p>\n'
               f'<section class="task-warmup tf-aquecer" id="aquecer" aria-labelledby="aquecer-title" data-task-warm="cartoes">'
               f'<h2 class="task-part" id="aquecer-title">{f["aquecer"]["titulo"]}</h2>\n'
               f'<div class="task-relogio" data-relogio data-max="{a["minutos"]}" data-passo="1" data-rotulo="Aquecimento" data-chave="pt-relogio:tarefas/{slug}:aquecimento"></div>\n'
               f'</section>\n'
               f'<h2 class="task-part">O que entregas</h2><p class="tf-p">{e["intro"]}</p>{lista(e["itens"], "ul") if e.get("itens") else ""}\n'
               f'<h2 class="task-part">{f["quadro"]["titulo"]}</h2>{quadro(f["quadro"])}\n'
               + ((LIGACAO + (f'<p class="tf-nota tf-grelha-nota">{f["grelha_nota"]}</p>\n' if f.get('grelha_nota') else '')) if com_grelha else '')
               + '<p class="tf-imprimir"><button type="button" data-task-print hidden>Imprimir o enunciado</button></p>\n'
               '</header>\n')

    # Cartões das perguntas: o relógio de produção no cimo da primeira; o pedido (um por alínea) e «Como citar»; logo a seguir
    # os exemplos com outros casos; depois os textos da pergunta, completos.
    perguntas = ''
    for k, p in enumerate(f['perguntas'], 1):
        ident = 'produzir' if k == 1 else f'pergunta-{k}'
        relogio = (f'<p class="tf-nota tf-relogio-nota">{p["relogio"]}</p><div class="task-relogio" data-relogio data-max="{f.get("producao_minutos", 60)}" data-passo="5" '
                   f'data-rotulo="Produção em papel" data-chave="pt-relogio:tarefas/{slug}:producao"></div>\n') if k == 1 else ''
        exs = [x for x in p['exemplos']]
        for x in exs:
            if x.get('de') == 'exemplos':  # o exemplo resolvido que a página já tinha (chave antiga «exemplos»)
                ps = re.findall(r'<p>.*?</p>', d['exemplos'][x['n']]['html'])  # «desde» e «ate»: só alguns parágrafos (os casos resolvidos)
                x['titulo'], x['html'] = d['exemplos'][x['n']]['titulo'], ''.join(ps[x.get('desde', 0):x.get('ate')]).replace('<p>', '<p class="tf-p">')
        perguntas += (f'<section class="task-section tf-pergunta" id="{ident}" data-task-card-name="Pergunta {k}" aria-labelledby="pergunta-{k}-titulo">'
                      f'<h2 id="pergunta-{k}-titulo"><span class="tf-n">Pergunta\xa0{k}</span> {p["titulo"]}</h2>\n'
                      f'<p class="tf-meta">{p["meta"]}</p>\n{relogio}'
                      + f'<div class="tf-pedido"><h3>{p["pedido_titulo"]}</h3>'
                      + (f'<p class="tf-p tf-intro">{p["intro"]}</p>' if p.get('intro') else '')
                      + (f'<p class="tf-p">{p["antes"]}</p>' + lista(p['escolhas'], 'ul') if p.get('escolhas') else '')
                      + (f'<p class="tf-p">{p["barra"]}</p>' if p.get('barra') else '')
                      + (f'<p class="tf-p">{p["para_cada"]}</p>' if p.get('para_cada') else '')
                      + alineas(p)
                      + ''.join(f'<p class="tf-ajuda">{x}</p>' for x in p.get('ajudas', []))
                      + (f'<p class="tf-citar"><b>Como citar.</b> {p["citar"]}</p>' if p.get('citar') else '') + '</div>\n'
                      + exemplos(exs, f['exemplo_titulo']) + apoios(p.get('apoios', []))
                      + (f'<p class="tf-p tf-ler">{p["ler"]}</p>\n' if p.get('ler') else '')
                      + ''.join(bloco_texto(textos[i]) for i in p['textos'])
                      + (onde_esta(p['onde_esta']) if p.get('onde_esta') else '') + '</section>\n')

    # Cartão «Tema A ou B»: a fotografia do tema (se houver), as remissões e os passos à vista; logo a seguir, o material
    # que é só de um tema (desdobrável fechado no ecrã, aberto em papel; as ligações dos passos abrem-no) e o exemplo
    # (desdobrável que não sai em papel).
    temas = ''
    for t in f['temas']:
        m = t['material']
        dentro = ((dossie(d['dossie_titulo'].replace('tema B', 'tema\xa0B'), d['dossie'], bool(f.get('nao_partir_dossie')), bool(f.get('juntos_em_papel'))) if m.get('dossie') else '')  # a referência não se parte
                  + ''.join(bloco_texto(textos[i]) for i in m.get('textos', []))
                  + ''.join(f'<p class="tf-p">{x}</p>' for x in m.get('notas', [])))
        temas += (f'<article class="task-theme" data-task-theme="{t["letra"]}" aria-labelledby="tema-{t["letra"]}">'
                  f'<h3 id="tema-{t["letra"]}"><span><span class="sr-only">Tema </span>{t["letra"]}</span> {t["nome"]}</h3>'
                  + (f'<p class="tf-resumo">{t["resumo"]}</p>' if t.get('resumo') else '') + f'<p class="tf-p">{t["intro"]}</p>'
                  + (figura(t['figura'], raiz) if t.get('figura') else '')
                  + ''.join(f'<p class="tf-p tf-antes">{x}</p>' for x in t.get('antes', []))
                  + f'{lista(t["passos"], "ol", "tf-passos tf-juntos" if f.get("juntos_em_papel") else "tf-passos")}'  # 13/11/2026 (M6)
                  + (f'<details class="tf-so-tema"><summary>{m["titulo"]}</summary><div>{dentro}</div></details>' if dentro else '')
                  + exemplos(m.get('exemplos', []), f['exemplo_titulo']) + '</article>')
    # 13/11/2026 (M1): o que serve aos dois temas. As imagens ficam à vista antes dos temas; depois dos temas, o que o texto leva nos
    # dois (um pedido por linha, com exemplos em desdobrável que não sai em papel) e os textos que servem aos dois (desdobrável
    # fechado no ecrã e aberto em papel; as ligações dos passos abrem-no).
    figs = f.get('temas_figuras')
    figuras = (f'<div class="tf-figs" id="imagens" role="group" aria-labelledby="imagens-titulo"><h3 id="imagens-titulo">{figs["titulo"]}</h3>'
               + ''.join(f'<p class="tf-p">{x}</p>' for x in figs.get('notas', []))
               + ''.join(figura(x, raiz) for x in figs['itens']) + '</div>\n') if figs else ''
    com = f.get('temas_comum')
    comum = (f'<div class="tf-comum" id="comum" role="group" aria-labelledby="comum-titulo"><h3 id="comum-titulo">{com["titulo"]}</h3>'
             + (f'<p class="tf-p">{com["intro"]}</p>' if com.get('intro') else '') + lista(com['passos'], 'ol', 'tf-passos')
             + exemplos(com.get('exemplos', []), f['exemplo_titulo']) + '</div>\n') if com else ''
    mat = f.get('temas_material')
    material = (f'<details class="tf-so-tema tf-dois-temas"><summary>{mat["titulo"]}</summary><div>'
                + ''.join(f'<p class="tf-p">{x}</p>' for x in mat.get('notas', []))
                + ''.join(bloco_texto(textos[i]) for i in mat['textos']) + '</div></details>\n') if mat else ''
    tema = (f'<section class="task-section tf-tema" id="tema" data-task-card-name="Tema A ou B" aria-labelledby="tema-titulo">'
            f'<h2 id="tema-titulo">{f["temas_titulo"]}</h2><p class="tf-meta">{f["temas_nota"]}</p>'
            + (f'<p class="tf-p tf-topo">{f["temas_topo"]}</p>' if f.get('temas_topo') else '') + '\n' + figuras
            + f'<div class="task-themes">{temas}</div>' + comum + material + '</section>\n')

    # Cartão «Fechar e entregar»: duas linhas finais, verificação (uma só lista de perguntas de sim ou não), entrega em passos.
    fi = f['finais']
    grupos = ('<fieldset class="task-checklist" aria-labelledby="entregar-title">'
              + ''.join(f'<label><input type="checkbox"> <span>{x}</span></label>' for x in f['verificar']) + '</fieldset>')
    fechar = (f'<section class="task-section" id="entregar" data-task-card-name="Fechar e entregar" aria-labelledby="entregar-title">'
              f'<h2 id="finais-titulo">{fi["titulo"]}</h2>' + (f'<p class="tf-p">{fi["texto"]}</p>' if fi.get('texto') else '') + f'{lista(fi["passos"], "ol", "tf-passos")}\n'
              f'<h2 id="entregar-title">{f["verificar_titulo"]}</h2><p class="tf-p" id="criterios">{f["verificar_texto"]}</p>\n{grupos}\n'
              f'<h2>{f["entrega_titulo"]}</h2>{lista(f["entrega"], "ol", "tf-passos")}</section>\n')

    # Cartão «Rever a matéria» (não sai em papel): uma linha por pergunta ou tema e a pergunta opcional de sempre.
    op = d['opcional']
    rever = (f'<section class="task-section tf-rever" id="apoios" data-task-card-name="Rever a matéria" aria-labelledby="preparacao">'
             f'<h2 id="preparacao">{f["rever_titulo"]}</h2><p class="tf-p">{f["rever_texto"]}</p>'
             + lista([f'<b>{x["para"]}.</b> {x["texto"]}' for x in f['rever']], 'ul', 'tf-rever-lista') + '\n'
             f'<details data-task-optional-preparation><summary>{f["opcional_titulo"]}</summary><div class="task-quiz" aria-label="Uma pergunta opcional">\n'
             f'<article class="task-question" data-task-question="1" aria-labelledby="q1"><h3 id="q1">{op["pergunta"]}</h3>{opcoes(op["opcoes"])}</article>\n'
             f'<p data-task-status role="status">Respostas exploradas: 0 de 1. Podes rever qualquer escolha.</p></div></details>\n'
             f'</section>\n')
    assert foot.count('</main>\n') == 1, slug
    return head + comecar + perguntas + tema + fechar + rever + foot.replace('</main>\n', '</main>\n' + IMPRIMIR)
