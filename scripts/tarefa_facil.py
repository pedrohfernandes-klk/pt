"""Molde «mais fácil de fazer» das tarefas de unidade (12/11/2026, PILOTO na m3-u1, por aprovar pelo docente).

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

Textos: «estrofes» é uma lista de {"rotulo": opcional, "versos": [...]}; os versos numeram-se de «numerar» em «numerar»,
contando só versos (nunca rótulos como «Mote» e «Voltas»); «escolher» {"de", "ate", "frase"} marca com uma barra os versos
de onde se pode escolher. A fotografia («figura») lê-se da lição que a publica (chave «de»), para ser a mesma imagem.
"""
import re
from html import escape

LIGACAO = '<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>\n'
V_FACIL = '20261112-facil-1'
FOLHAS = ('<link rel="stylesheet" href="../../assets/info-i.css?v=20261105">'
          f'<link rel="stylesheet" href="../../assets/task-textos.css?v={V_FACIL}">'
          '<script defer src="../../assets/info-i.js?v=20261105"></script>')
MAIN = '<main class="task-page task-choice-page" data-task-compact data-task-choice>'
MAIN_FACIL = ('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil '
              'data-task-opening="Começar" data-task-index="nomes">')
IMPRIMIR = ('<script>document.querySelectorAll("[data-task-print]").forEach(function(b){b.hidden=false;'
            'b.onclick=function(){window.print()}})</script>\n')


def lista(itens, tag='ol', cls=''):
    return f'<{tag}{" class=" + chr(34) + cls + chr(34) if cls else ""}>' + ''.join(f'<li>{x}</li>' for x in itens) + f'</{tag}>'


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
            cels.append(f'<th scope="row{"group" if span else ""}"{span}>{c}</th>' if k == 0 else f'<td>{c}</td>')
        corpo.append('<tr>' + ''.join(cels) + '</tr>')
    notas = ''.join(f'<p class="tf-nota">{n}</p>' for n in q.get('notas', []))
    return (f'<table class="tf-quadro"><caption>{q["titulo"]}</caption><thead><tr>{cab}</tr></thead>'
            f'<tbody>{"".join(corpo)}</tbody></table>{notas}')


def bloco_texto(t):
    """O texto para análise, completo e contínuo: título, versos numerados, vocabulário das lições e linha de fonte."""
    passo, esc, n, partes = t.get('numerar', 5), t.get('escolher'), 0, []
    for e in t['estrofes']:
        if e.get('rotulo'):
            partes.append(f'<p class="tt-rotulo">{e["rotulo"]}</p>')
        versos = []
        for v in e['versos']:
            n += 1
            marca = ' tt-esc' if esc and esc['de'] <= n <= esc['ate'] else ''
            versos.append(f'<span class="tt-v{marca}"><span class="tt-n">{n if n % passo == 0 else ""}</span>'
                          f'<span class="tt-l">{escape(v, quote=False)}</span></span>')
        partes.append('<p class="tt-estrofe">' + '\n'.join(versos) + '</p>')
    frase = f'<p class="tt-escolher">{esc["frase"]}</p>' if esc else ''
    gloss = ('<div class="tt-gloss"><p><b>Vocabulário</b></p><ul>'
             + ''.join(f'<li><b>{p}</b>: {s}</li>' for p, s in t['glossario']) + '</ul></div>') if t.get('glossario') else ''
    return (f'<section class="tt-texto" id="{t["id"]}" aria-labelledby="{t["id"]}-titulo">'
            f'<h3 id="{t["id"]}-titulo"><span class="tt-num">{t["rotulo"]}</span> {t["titulo"]}</h3>\n'
            f'{frase}<div class="tt-versos">\n' + '\n'.join(partes) + f'\n</div>\n{gloss}'
            f'<p class="tt-fonte">{t["fonte"]}</p></section>\n')


def onde_esta(o):
    """Texto protegido: não se copia; diz-se onde está e dá-se só o que as lições já publicam em citação curta."""
    return (f'<section class="tt-onde" aria-labelledby="{o["id"]}-titulo"><h3 id="{o["id"]}-titulo">{o["titulo"]}</h3>'
            + ''.join(f'<p class="tf-p">{p}</p>' for p in o['frases'])
            + f'<p class="tf-p"><b>{o["lista_titulo"]}</b></p>' + lista(o['lista'], 'ul')
            + f'<p class="tt-fonte">{o["fonte"]}</p></section>\n')


def exemplos(xs):
    return ''.join(f'<aside class="tf-exemplo"><h4>{x["titulo"]}</h4>'
                   + (x.get('html') or ''.join(f'<p class="tf-p">{p}</p>' for p in x['paragrafos'])) + '</aside>\n' for x in xs)


def figura(f, raiz):
    """A fotografia é a que a lição publica (lê-se do ficheiro da lição, pelo texto alternativo), com o crédito completo
    atrás do «i» (peça assets/info-i.*, como no mapa do módulo) e a legenda à vista."""
    fonte = (raiz / f['de']).read_text('utf-8')
    m = re.search(r'<img src=\\"(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+)\\" alt=\\"' + re.escape(f['alt']) + r'\\"', fonte)
    assert m, f['de']
    return (f'<figure class="tf-fig"><img src="{m.group(1)}" alt="{f["alt"]}" width="{f["largura"]}" height="{f["altura"]}">'
            f'<details class="info-i info-i--linha" name="info-i"><summary aria-label="{f["credito_rotulo"]}">'
            f'<span aria-hidden="true">i</span></summary><p class="info-i-texto">{f["credito"]}</p></details>'
            f'<figcaption>{f["legenda"]}</figcaption></figure>\n')


def dossie(titulo, factos):
    li = ''.join(f'<li>{x["facto"]}<span class="tf-origem">Fonte: <a href="{x["href"]}">{x["fonte"]}</a></span></li>' for x in factos)
    return f'<section class="task-dossier tf-dossie" aria-labelledby="dossie"><h4 id="dossie">{titulo}</h4><ol>{li}</ol></section>\n'


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
    head = head.replace(MAIN, MAIN_FACIL).replace('<link rel="stylesheet" href="../../assets/appearance.css', FOLHAS + '<link rel="stylesheet" href="../../assets/appearance.css')
    assert head.count('assets/task-reader.js?v=') == 1, slug
    head = re.sub(r'assets/task-reader\.js\?v=[^"]+', 'assets/task-reader.js?v=' + V_FACIL, head)

    # Cartão 1, «Começar»: o que se faz, o que se entrega, o quadro e o aquecimento (uma só ligação).
    e = f['entregas']
    comecar = (f'<header><p class="task-kicker">{f["kicker"]}</p><h1>{d["titulo"]}</h1>\n'
               f'<h2 class="task-part">O que vais fazer</h2>{lista(f["fazer"], "ol", "tf-fazer")}<p class="tf-p">{f["modo"]}</p>\n'
               f'<h2 class="task-part">O que entregas</h2><p class="tf-p">{e["intro"]}</p>{lista(e["itens"], "ul")}\n'
               f'<h2 class="task-part">{f["quadro"]["titulo"]}</h2>{quadro(f["quadro"])}\n'
               + (LIGACAO if com_grelha else '')
               + '<p class="tf-imprimir"><button type="button" data-task-print hidden>Imprimir o enunciado</button></p>\n'
               f'<section class="task-warmup tf-aquecer" id="aquecer" aria-labelledby="aquecer-title" data-task-warm="cartoes">'
               f'<h2 class="task-part" id="aquecer-title">{f["aquecer"]["titulo"]}</h2><p class="tf-p">{f["aquecer"]["texto"]}</p>\n'
               f'<p class="task-aquecer"><a href="{a["cartoes"]}">{a["ligacao"]}</a></p>\n'
               f'<div class="task-relogio" data-relogio data-max="{a["minutos"]}" data-passo="1" data-rotulo="Aquecimento" data-chave="pt-relogio:tarefas/{slug}:aquecimento"></div>\n'
               f'</section></header>\n')

    # Cartões das perguntas: primeiro o pedido (um por alínea) e «Como citar»; logo a seguir os textos da pergunta, completos;
    # no fim, os exemplos com outros casos.
    perguntas = ''
    for k, p in enumerate(f['perguntas'], 1):
        ident = 'produzir' if k == 1 else f'pergunta-{k}'
        relogio = (f'<p class="tf-nota tf-relogio-nota">{p["relogio"]}</p><div class="task-relogio" data-relogio data-max="60" data-passo="5" '
                   f'data-rotulo="Produção em papel" data-chave="pt-relogio:tarefas/{slug}:producao"></div>\n') if k == 1 else ''
        exs = [x for x in p['exemplos']]
        for x in exs:
            if x.get('de') == 'exemplos':  # o exemplo resolvido que a página já tinha (chave antiga «exemplos»)
                x['titulo'], x['html'] = d['exemplos'][x['n']]['titulo'], d['exemplos'][x['n']]['html'].replace('<p>', '<p class="tf-p">')
        perguntas += (f'<section class="task-section tf-pergunta" id="{ident}" data-task-card="Pergunta {k}" aria-labelledby="pergunta-{k}-titulo">'
                      f'<h2 id="pergunta-{k}-titulo"><span class="tf-n">Pergunta\xa0{k}</span> {p["titulo"]}</h2>\n'
                      f'<p class="tf-meta">{p["meta"]}</p>\n'
                      + f'<div class="tf-pedido"><h3>{p["pedido_titulo"]}</h3>'
                      + (f'<p class="tf-p">{p["antes"]}</p>' + lista(p['escolhas'], 'ul') if p.get('escolhas') else '')
                      + (f'<p class="tf-p">{p["para_cada"]}</p>' if p.get('para_cada') else '')
                      + lista(p['alineas'], 'ol', 'tf-alineas')
                      + ''.join(f'<p class="tf-ajuda">{x}</p>' for x in p.get('ajudas', []))
                      + f'<p class="tf-citar"><b>Como citar.</b> {p["citar"]}</p></div>\n{relogio}'
                      + f'<p class="tf-p tf-ler">{p["ler"]}</p>\n'
                      + ''.join(bloco_texto(textos[i]) for i in p['textos'])
                      + (onde_esta(p['onde_esta']) if p.get('onde_esta') else '')
                      + exemplos(exs) + '</section>\n')

    # Cartão «Tema A ou B»: os passos à vista; o que é só de um tema fica num desdobrável (fechado no ecrã, aberto em papel).
    temas = ''
    for t in f['temas']:
        m = t['material']
        dentro = ((figura(m['figura'], raiz) if m.get('figura') else '')
                  + (dossie(d['dossie_titulo'], d['dossie']) if m.get('dossie') else '')
                  + ''.join(bloco_texto(textos[i]) for i in m.get('textos', []))
                  + ''.join(f'<p class="tf-p">{x}</p>' for x in m.get('notas', []))
                  + exemplos(m.get('exemplos', [])))
        temas += (f'<article class="task-theme" data-task-theme="{t["letra"]}" aria-labelledby="tema-{t["letra"]}">'
                  f'<h3 id="tema-{t["letra"]}"><span><span class="sr-only">Tema </span>{t["letra"]}</span> {t["nome"]}</h3>'
                  f'<p class="tf-resumo">{t["resumo"]}</p><p class="tf-p">{t["intro"]}</p>{lista(t["passos"], "ol", "tf-passos")}'
                  f'<details class="tf-so-tema"><summary>{m["titulo"]}</summary><div>{dentro}</div></details></article>')
    tema = (f'<section class="task-section tf-tema" id="tema" data-task-card="Tema A ou B" aria-labelledby="tema-titulo">'
            f'<h2 id="tema-titulo">{f["temas_titulo"]}</h2><p class="tf-meta">{f["temas_nota"]}</p>\n'
            f'<div class="task-themes">{temas}</div></section>\n')

    # Cartão «Fechar e entregar»: duas linhas finais, verificação em perguntas de sim ou não, entrega em passos.
    fi, grupos = f['finais'], ''
    for g in f['verificar']:
        itens = ''.join(f'<label><input type="checkbox"> <span>{x}</span></label>' for x in g['itens'])
        bloco = f'<fieldset class="task-checklist"><legend>{g["titulo"]}</legend>{itens}</fieldset>'
        grupos += f'<details class="tf-so-tema"><summary>{g["so"]}</summary><div>{bloco}</div></details>' if g.get('so') else bloco
    fechar = (f'<section class="task-section" id="entregar" data-task-card="Fechar e entregar" aria-labelledby="entregar-title">'
              f'<h2 id="finais-titulo">{fi["titulo"]}</h2><p class="tf-p">{fi["texto"]}</p>{lista(fi["passos"], "ol", "tf-passos")}\n'
              f'<h2 id="entregar-title">{f["verificar_titulo"]}</h2><p class="tf-p" id="criterios">{f["verificar_texto"]}</p>\n{grupos}\n'
              f'<h2>{f["entrega_titulo"]}</h2>{lista(f["entrega"], "ol", "tf-passos")}</section>\n')

    # Cartão «Rever a matéria» (não sai em papel): uma linha por pergunta ou tema e a pergunta opcional de sempre.
    op = d['opcional']
    rever = (f'<section class="task-section tf-rever" id="apoios" data-task-card="Rever a matéria" aria-labelledby="preparacao">'
             f'<h2 id="preparacao">{f["rever_titulo"]}</h2><p class="tf-p">{f["rever_texto"]}</p>'
             + lista([f'<b>{x["para"]}.</b> {x["texto"]}' for x in f['rever']], 'ul', 'tf-rever-lista') + '\n'
             f'<details data-task-optional-preparation><summary>{f["opcional_titulo"]}</summary><div class="task-quiz" aria-label="Uma pergunta opcional">\n'
             f'<article class="task-question" data-task-question="1" aria-labelledby="q1"><h3 id="q1">{op["pergunta"]}</h3>{opcoes(op["opcoes"])}</article>\n'
             f'<p data-task-status role="status">Respostas exploradas: 0 de 1. Podes rever qualquer escolha.</p></div></details>\n'
             f'</section>\n')
    assert foot.count('</main>\n') == 1, slug
    return head + comecar + perguntas + tema + fechar + rever + foot.replace('</main>\n', '</main>\n' + IMPRIMIR)
