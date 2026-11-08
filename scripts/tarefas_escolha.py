"""Tarefas de unidade no formato «aquecimento + núcleo comum + tema à escolha» (28/10/2026; piloto no M2, depois o M1).

Dados em docs/pedagogia/tarefas-escolha/<slug>.json, um ficheiro por tarefa, só com o que a página publica
(sem a grelha nem a chave da correção, que ficam fora do repositório). Escreve tarefas/<slug>/index.html com a
mesma estrutura, classes, relógio e versões ?v= das tarefas do piloto (tarefas/m2-u1/).
Se a tarefa tiver grelha /20 em docs/pedagogia/grelhas-tarefas-20261027.json, a ligação à grelha entra antes do
fecho («Fecha com duas linhas»), igual à que scripts/grelhas_tarefas.py escreve: os dois geradores ficam
idempotentes e podem correr por qualquer ordem.
28/10/2026 (revisão do PR #122): as letras das opções e dos temas ficam no nome acessível (deixam de estar
escondidas aos leitores de ecrã, porque as instruções mandam escrevê-las); o fecho diz o que é a síntese; e
--saida PASTA escreve as páginas noutra raiz, para os testes compararem sem mexer na árvore.
29/10/2026 (decisão do docente, M7-U3): uma tarefa pode trocar as duas máquinas em papel pelo aquecimento em cartões
(«aquecer»: {"cartoes": ...}, página de scripts/aquecimentos.py). O cartão «Aquecer» fica primeiro, com o relógio do
aquecimento e a ligação em destaque; não há pergunta «aquecer», só a opcional; o enunciado ganha a mesma ligação. Os
exemplos resolvidos («exemplos») entram em «Relembrar», depois da lista. O <title> leva o título sem marcas (<i>). As
páginas sem estas chaves saem iguais, byte a byte.
06/11/2026: decisão 152 (cuidado em todas as lições), M1: o aquecimento em cartões pode trazer «tabela» ({"colunas": […],
"linhas": [[…], …]}) e «depois»: o texto, a tabela de apoio (class apoio-tabela, como na M7-F10, com th scope, td data-label
e os role) e o parágrafo seguinte; a página carrega então assets/pt-lessons/apoios-tabelas.css antes da camada de aparência.
Com «nao_partir», os números do molde («90 minutos» na descrição, «10 min» do aquecimento e «90 min» do enunciado) levam
espaço que não quebra (U+00A0). As páginas sem estas chaves saem iguais, byte a byte.
08/11/2026: decisão 152, M5: o texto de um tema pode acabar numa lista (fecha o parágrafo, abre a lista e termina em «<p>»); o
parágrafo vazio que sobra no fim («<p></p>») sai. As páginas sem listas no fim de um tema saem iguais, byte a byte.
Uso: python3 scripts/tarefas_escolha.py [--saida PASTA] [slug ...]
"""
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs' / 'pedagogia' / 'tarefas-escolha'
GRELHAS = ROOT / 'docs' / 'pedagogia' / 'grelhas-tarefas-20261027.json'
LIGACAO = '<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>\n'
# 06/11/2026: decisão 152. A folha das tabelas de apoio entra antes da camada de aparência, só nas tarefas com «tabela».
APARENCIA = '<link rel="stylesheet" href="../../assets/appearance.css?v=20261025-universal-1">'
FOLHA_TABELAS = '<link rel="stylesheet" href="../../assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
V = '20261028-escolha-2'
HEAD = '''<!doctype html>
<html lang="pt-PT" data-appearance-site="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aula de tarefa · {title} · {MOD}</title>
<meta name="description" content="Aula de tarefa com consulta: aquecimento, núcleo comum e um tema à escolha, em papel, durante 90{sep}minutos, com entrega no Teams.">
<link rel="stylesheet" href="../../assets/pt-lessons/lesson.css?v=20261027-task-reader-1"><link rel="stylesheet" href="../../assets/task-90.css?v=20261027-tarefas-1"><link rel="stylesheet" href="../../assets/docente-access.css?v=20261026.1">
<script defer src="../../assets/task-90.js?v=20261027-compact-1"></script>
<link rel="stylesheet" href="../../assets/task-reader.css?v=20261027-task-reader-1"><link rel="stylesheet" href="../../assets/relogio.css?v=20261027-relogio-1"><link rel="stylesheet" href="../../assets/task-choice.css?v={V}"><script defer src="../../assets/relogio.js?v=20261027-relogio-1"></script><script defer src="../../assets/pt-lessons/casca.js?v=20261027-task-reader-1"></script><script defer src="../../assets/task-reader.js?v={V}"></script><link rel="stylesheet" href="../../assets/appearance.css?v=20261025-universal-1"><script src="../../assets/appearance.js?v=20261025-universal-1"></script></head>
<body data-site="pt" class="task-lesson"><main class="task-page task-choice-page" data-task-compact data-task-choice>
<nav class="task-nav" aria-label="Onde estás"><a href="../../">Português</a><a href="../../{mod}/#unidade-pedagogica-{unit}">{MOD} · Unidade {unit}</a></nav>
'''
FOOT = '''</main>
<a class="teacher-access" href="https://pedrohfernandes-klk.github.io/lente/docente/#portugues" aria-label="Guiões e materiais do docente" title="Para o docente"><svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><circle cx="20" cy="20" r="15" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="20" cy="20" r="8" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="m9.5 9.5 5 5m11 11 5 5m-21 0 5-5m11-11 5-5" fill="none" stroke="currentColor" stroke-width="5"/></svg></a>
<script defer src="../../assets/projection-launcher.js?v=20261019.4" data-site="pt"></script></body></html>
'''


def opts(items):
    out = []
    for correct, label, text, response in items:
        # As explicações vão num atributo e saem como texto (task-90.js usa textContent): sem aspas nem marcas.
        assert '"' not in response and '<' not in response, response
        # 28/10/2026: a letra fica no nome acessível («A: …»); a máquina 02 manda escrevê-la no papel.
        out.append(f'<button type="button" aria-pressed="false" data-correct="{"true" if correct else "false"}" data-response="{response}"><span class="task-letter">{label}<span class="sr-only">:</span></span> {text}</button>')
    return '<div class="task-options">' + ''.join(out) + '</div><p class="task-feedback" data-task-feedback role="status" aria-live="polite" hidden></p>'


def warmup(slug, instruction, anatomy, claim, qtitle, options):
    dl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in anatomy)
    return f'''<section class="task-section task-warmup" id="aquecer" aria-labelledby="aquecer-title">
<p class="task-warmup-kicker">Antes de escrever · 15 min · em papel, sem consultar</p>
<h2 id="aquecer-title">Aquecer com duas máquinas do exame</h2>
<p>Faz cada máquina no papel. Só depois confirmas.</p>
<div class="task-relogio" data-relogio data-max="15" data-passo="1" data-rotulo="Aquecimento" data-chave="pt-relogio:tarefas/{slug}:aquecimento"></div>
<article class="task-machine" data-task-machine="1" aria-labelledby="maquina-1"><p class="task-machine-tag"><span>01</span> Pensa.</p><h3 id="maquina-1">Descobre o que te pedem</h3>
<blockquote class="task-instruction">{instruction}</blockquote>
<p>Copia a instrução. Sublinha os verbos que mandam fazer, rodeia o objeto e põe a condição entre parênteses.</p>
<details class="task-confirm"><summary>Confirmar depois de marcares</summary><dl class="task-anatomy">{dl}</dl></details></article>
<article class="task-machine" data-task-machine="2" aria-labelledby="maquina-2"><p class="task-machine-tag"><span>02</span> Prova.</p><h3 id="maquina-2">Prova ou distração?</h3>
<p class="task-claim">{claim}</p>
<div class="task-question" data-task-question="aquecer" aria-labelledby="q-aquecer"><p class="task-question-title" id="q-aquecer">{qtitle}</p>{opts(options)}</div></article>
</section>
'''


def tabela_apoio(t):
    """06/11/2026: decisão 152. A tabela de apoio, igual às das lições (M7-F10, M7-F15): cabeçalho com th scope=col, primeira
    coluna com th scope=row, td data-label com o nome da coluna, e os role, porque no telemóvel a tabela passa a display:block."""
    cab = ''.join(f'<th scope="col" role="columnheader">{c}</th>' for c in t['colunas'])
    linhas = ''.join('<tr role="row"><th scope="row" role="rowheader">' + linha[0] + '</th>'
                     + ''.join(f'<td role="cell" data-label="{t["colunas"][k]}">{v}</td>' for k, v in enumerate(linha[1:], 1))
                     + '</tr>' for linha in t['linhas'])
    return (f'<table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row">{cab}</tr></thead>'
            f'<tbody role="rowgroup">{linhas}</tbody></table>')


def warmup_cards(slug, a, sep=' '):
    """29/10/2026: o aquecimento faz-se em cartões (página própria); não há máquinas nem pergunta «aquecer».
    06/11/2026: decisão 152. Com «tabela», o texto, a tabela dos tempos e «depois»; sep é o espaço do molde (U+00A0 com «nao_partir»)."""
    texto = f"<p>{a['texto']}</p>" + (tabela_apoio(a['tabela']) + f"<p>{a['depois']}</p>" if 'tabela' in a else '')
    return f'''<section class="task-section task-warmup" id="aquecer" aria-labelledby="aquecer-title" data-task-warm="cartoes">
<p class="task-warmup-kicker">Antes de escrever · {a['minutos']}{sep}min · em cartões, com consulta</p>
<h2 id="aquecer-title">Aquecer em cartões</h2>
{texto}
<p class="task-aquecer"><a href="{a['cartoes']}">{a['ligacao']}</a></p>
<div class="task-relogio" data-relogio data-max="{a['minutos']}" data-passo="1" data-rotulo="Aquecimento" data-chave="pt-relogio:tarefas/{slug}:aquecimento"></div>
</section>
'''


def header(slug, unit, title, lead, core, themes, aquecer=None, sep=' '):
    li = ''.join(f'<li>{x}</li>' for x in core)
    # 29/10/2026: com o aquecimento em cartões, o enunciado leva também a ligação em destaque, logo a seguir ao lead.
    link = f'<p class="task-aquecer"><a href="{aquecer["cartoes"]}">{aquecer["ligacao_enunciado"]}</a></p>\n' if aquecer else ''
    # 28/10/2026: «Tema A» / «Tema B» no nome acessível; o fecho manda escrever no topo o tema escolhido.
    # 08/11/2026: decisão 152, M5. Um tema cujo texto acaba numa lista não deixa um parágrafo vazio no fim.
    corpo = lambda text: re.sub(r'<p></p>$', '', f'<p>{text}</p>')
    th = ''.join(f'<article class="task-theme" data-task-theme="{k}" aria-labelledby="tema-{k}"><h3 id="tema-{k}"><span><span class="sr-only">Tema </span>{k}</span> {name}</h3>{corpo(text)}</article>' for k, name, text in themes)
    return f'''<header><p class="task-kicker">Tarefa individual · Unidade {unit} · 90{sep}min</p><h1>{title}</h1>
<p>{lead}</p>
{link}<section id="produzir" aria-label="Enunciado">
<h2 class="task-part">Núcleo comum <small>para todos</small></h2><ol>{li}</ol>
<h2 class="task-part">Escolhe um tema <small>só um</small></h2><div class="task-themes">{th}</div>
</section><div class="task-relogio" data-relogio data-max="60" data-passo="5" data-rotulo="Produção em papel" data-chave="pt-relogio:tarefas/{slug}:producao"></div></header>
'''


def apoios(links, dossier_title, facts, qtitle, options, examples=(), questions=2):
    li = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    fa = ''.join(f'<li>{f} <a class="task-fonte" href="{h}">{s}</a></li>' for f, h, s in facts)
    # 29/10/2026: exemplos resolvidos («Ver como se faz»), quando a tarefa os tem; ficam fora do enunciado.
    ex = ('<section class="task-examples" aria-labelledby="exemplos"><h3 id="exemplos">Ver como se faz</h3>'
          + ''.join(f'<article class="task-example"><h4>{t}</h4>{h}</article>' for t, h in examples) + '</section>\n') if examples else ''
    return f'''<section class="task-section" id="apoios" aria-labelledby="preparacao"><h2 id="preparacao">Relembrar</h2><ul>{li}</ul>
{ex}<section class="task-dossier" aria-labelledby="dossie"><h3 id="dossie">{dossier_title}</h3><ul>{fa}</ul></section>
<details data-task-optional-preparation><summary>Experimentar uma pergunta</summary><div class="task-quiz" aria-label="Uma pergunta opcional">
<article class="task-question" data-task-question="1" aria-labelledby="q1"><h3 id="q1">{qtitle}</h3>{opts(options)}</article>
<p data-task-status role="status">Respostas exploradas: 0 de {questions}. Podes rever qualquer escolha.</p></div></details>
</section>
'''


def entregar(criteria, close, grelha):
    cr = ''.join(f'<li>{c}</li>' for c in criteria)
    return f'''<section class="task-section" id="entregar" aria-labelledby="entregar-title"><h2 id="entregar-title">Verificar e entregar</h2>
<h3 id="criterios">O que conta</h3><ul class="task-criteria">{cr}</ul>
{LIGACAO if grelha else ''}<p>{close}</p>
<p>Escreve no topo da tua resposta o tema que escolheste (A ou B). Fotografa o teu trabalho em papel, incluindo a síntese (as duas linhas finais), e entrega as fotografias legíveis no Teams.</p></section>
'''


def tarefa(d, com_grelha, raiz=ROOT):
    slug, unit = d['slug'], d['unidade']
    assert d['fecho'].startswith('Fecha com duas linhas'), slug
    mod = slug.split('-')[0]
    a = d['aquecer']
    cartoes = 'cartoes' in a
    op = lambda xs: [(x['certa'], x['letra'], x['texto'], x['resposta']) for x in xs]
    titulo = escape(re.sub(r'<[^>]+>', '', d['titulo']), quote=False)
    # 06/11/2026: decisão 152. «nao_partir»: os números do molde com espaço que não quebra (só nas tarefas que o pedem).
    sep = '\xa0' if d.get('nao_partir') else ' '
    html = (HEAD.format(title=titulo, unit=unit, V=V, mod=mod, MOD=mod.upper(), sep=sep)
            + (warmup_cards(slug, a, sep) if cartoes else
               warmup(slug, a['instrucao'], [tuple(x) for x in a['anatomia']], a['afirmacao'], a['pergunta'], op(a['opcoes'])))
            + header(slug, unit, d['titulo'], d['lead'], d['nucleo'], [(t['letra'], t['nome'], t['texto']) for t in d['temas']],
                     a if cartoes else None, sep)
            + apoios([(x['href'], x['texto']) for x in d['apoios']], d['dossie_titulo'], [(x['facto'], x['href'], x['fonte']) for x in d['dossie']],
                     d['opcional']['pergunta'], op(d['opcional']['opcoes']),
                     [(x['titulo'], x['html']) for x in d.get('exemplos', [])], 1 if cartoes else 2)
            + entregar(d['criterios'], d['fecho'], com_grelha)
            + FOOT)
    if 'tabela' in a:
        # 06/11/2026: decisão 152. A folha das tabelas de apoio, antes da camada de aparência.
        assert html.count(APARENCIA) == 1, slug
        html = html.replace(APARENCIA, FOLHA_TABELAS + APARENCIA)
    p = raiz / 'tarefas' / slug / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_bytes() != html.encode('utf-8'):
        p.write_text(html, 'utf-8', newline='\n')


def main():
    args, raiz = sys.argv[1:], ROOT
    if '--saida' in args:
        i = args.index('--saida')
        raiz = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    pedidos = set(args)
    grelhas = json.loads(GRELHAS.read_text('utf-8'))['tarefas']
    feitos = []
    for p in sorted(DADOS.glob('*.json')):
        d = json.loads(p.read_text('utf-8'))
        assert p.stem == d['slug'], p
        # Só o que é público: a grelha e a chave da correção não vivem nestes dados.
        assert not {'grelha', 'provas', 'notas_docente', 'chave'} & set(d), p
        if pedidos and d['slug'] not in pedidos:
            continue
        tarefa(d, d['slug'] in grelhas, raiz)
        feitos.append(d['slug'])
    print('Tarefas com escolha: ' + ', '.join(feitos))


if __name__ == '__main__':
    main()
