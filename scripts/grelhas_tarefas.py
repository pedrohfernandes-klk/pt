"""Grelhas /20 das tarefas de unidade (27/10/2026): página do aluno, versão de correção e ligação na tarefa.

Dados em docs/pedagogia/grelhas-tarefas-20261027.json. Para cada tarefa escreve:
- tarefas/<slug>/grelha/: os critérios com os níveis 0, parcial e máximo, um exemplo por nível, o que custa
  pontos e a autoavaliação em papel antes de entregar;
- tarefas/<slug>/correcao/: a grelha de correção do docente, com a nota do aluno ao lado e o feedback em três
  partes (o que funciona, o que custa pontos, o próximo passo);
- na tarefa, uma linha em «Verificar e entregar» com a ligação à grelha (marca autorizada nos testes).
Regra das soluções (28/10/2026): as duas páginas são públicas. Nenhum descritor nem exemplo responde à tarefa:
os descritores dizem o que se avalia em termos gerais e os exemplos usam outro caso do mesmo tipo. A chave da
correção não vive nestes dados. A «nota» opcional de cada grelha diz ao aluno de onde vêm os exemplos.
28/10/2026 (revisão do PR #122): as ligações de volta à tarefa abrem o cartão «Verificar» (../#entregar), de onde
se chega à grelha; na correção, os três blocos do comentário ficam sob um título h2; e --saida PASTA escreve as
páginas noutra raiz (a tarefa lê-se dessa raiz ou, se lá não estiver, da árvore), para os testes compararem
sem mexer na árvore.
29/10/2026 (M7-U3): os títulos de obras escrevem-se nos dados entre _…_ e saem em itálico (<i>); no <title>, sem marcas.
As grelhas sem _…_ saem iguais, byte a byte.
06/11/2026: decisão 152 (cuidado em todas as lições), M1: com «max_em_listas» num critério, o descritor do nível máximo da
página do aluno abre os elementos de cada tema em lista («Tema A: x; y; z. Explicação: … Tema B: …»); a versão de correção
fica com o texto corrido (está num <small> dentro de uma célula). As grelhas sem a chave saem iguais, byte a byte.
08/11/2026: decisão 152, M3: com «nao_partir» numa grelha, o intervalo do nível parcial («1 a 3») leva espaços que não quebram
(U+00A0), para não se partir entre linhas. As grelhas sem a chave saem iguais, byte a byte.
08/11/2026: decisão 152, M5: com «max_em_listas», o fecho de cada tema pode ser «Explicação: …» ou «Conclusão: …» (o tema B da
M5-U2 fecha com a conclusão do parágrafo de opinião). As grelhas que já tinham a chave saem iguais, byte a byte.
08/11/2026: decisão 152, M6: com «nao_partir_valores» numa grelha, «20 valores em cinco critérios» leva espaço que não quebra
(U+00A0) entre o número e «valores»; e a ligação à grelha pode estar já com «Grelha /20» preso (U+00A0, a tarefa com
«nao_partir_grelha», scripts/tarefas_escolha.py), e então não se repete. As grelhas e as tarefas sem as chaves saem iguais, byte a byte.
12/11/2026: tarefas «mais fáceis de fazer» (piloto na m3-u1, aprovado pelo docente; a seguir, o M3 inteiro). Duas chaves opcionais:
«autoavaliacao_so_tua» (decisão do docente: a autoavaliação é só para o aluno e não se entrega; o texto da caixa muda) e
«trocas_aluno», pares [antes, depois] com as palavras que o enunciado novo trocou por outras mais simples (na página do aluno,
cada par tem de ocorrer). «Tudo junto» (decisão do docente): a versão de correção usa as mesmas palavras (as mesmas trocas, nos
textos que mostra) e, com «autoavaliacao_so_tua», deixa de supor que a autoavaliação é entregue: sai a coluna «Aluno» da tabela
de notas e sai a nota «Diferença entre a tua nota e a minha»; ficam a nota e o comentário do docente. As grelhas sem as chaves
saem iguais, byte a byte.
Idempotente. Uso: python3 scripts/grelhas_tarefas.py [--saida PASTA]
"""
from html import escape as e
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs/pedagogia/grelhas-tarefas-20261027.json'
LIGACAO = '<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>\n'
# 08/11/2026: decisão 152, M6. A mesma ligação, com «Grelha /20» preso (U+00A0), como a escreve scripts/tarefas_escolha.py.
LIGACAO_NAO_PARTE = LIGACAO.replace('Grelha /20', 'Grelha\xa0/20')
ANCORA = '<p>Fecha com duas linhas'
# 28/10/2026: voltar à tarefa leva ao cartão «Verificar e entregar», onde está a ligação à grelha.
VOLTAR = '../#entregar'
# 28/10/2026: cada tabela fica num contentor que desliza sozinho; a página nunca desliza na horizontal (320 a 1440 px).
REGIAO = 'role="region" aria-label="{}" tabindex="0"'

CSS = """:root{--g-tinta:var(--tinta,#161616);--g-papel:var(--papel,#fff);--g-fundo:var(--fundo,#f4f3ee);--g-suave:var(--suave,#5c5a55);--g-linha:var(--linha,#dcd9d0)}
*{box-sizing:border-box}body{margin:0;background:var(--g-fundo);color:var(--g-tinta);font:17px/1.55 Georgia,'Times New Roman',serif}
.grelha{max-width:880px;margin:0 auto;padding:16px clamp(16px,4vw,32px) 56px}
.g-nav{display:flex;flex-wrap:wrap;gap:4px 20px;align-items:center;padding:8px 0 12px;border-bottom:2px solid var(--g-tinta);font:700 .85rem Arial,Helvetica,sans-serif}
.g-nav a{color:inherit;min-height:44px;display:inline-flex;align-items:center}.g-nav button{margin-left:auto}
button{font:700 .85rem Arial,Helvetica,sans-serif;min-height:44px;padding:8px 14px;background:var(--g-papel);color:var(--g-tinta);border:2px solid var(--g-tinta);border-radius:0;cursor:pointer}
.rot{font:700 .75rem/1.3 Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase;margin:24px 0 8px}
h1{font:700 clamp(1.8rem,5vw,2.6rem)/1.1 Arial,Helvetica,sans-serif;margin:0 0 12px;letter-spacing:-.02em}
h2{font:700 1.2rem/1.3 Arial,Helvetica,sans-serif;margin:0 0 12px}
.lead{font-size:1.15rem;margin:0 0 8px}p{margin:0 0 12px}.g-nota{font-size:.9rem;color:var(--g-suave);border-left:4px solid var(--g-linha);padding-left:12px}
table{width:100%;border-collapse:collapse;background:var(--g-papel);margin:16px 0 8px}
.g-tab td a{color:inherit;text-decoration:none;display:block;min-height:44px;padding:12px 0}
.g-tab{overflow-x:auto;margin:16px 0 8px}.g-tab>table{margin:0}
caption{text-align:left;font:700 .75rem Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:0 0 8px}
th,td{border:1px solid var(--g-linha);padding:8px 10px;text-align:left;vertical-align:top}
.g-resumo td{vertical-align:baseline}
thead th{font:700 .8rem Arial,Helvetica,sans-serif;border-bottom:2px solid var(--g-tinta)}
td.n,th.n{text-align:center;width:4.5em;font:700 1rem Arial,Helvetica,sans-serif}
tr.total th,tr.total td{border-top:2px solid var(--g-tinta);font-weight:700}
.g-crit{margin:28px 0 0;padding:20px 0 0;border-top:2px solid var(--g-tinta)}
.g-crit h2{display:flex;gap:12px;align-items:baseline}.g-crit h2 .num{font-size:1.6rem}.g-crit h2 .max{margin-left:auto;font-size:.85rem;white-space:nowrap;border:2px solid var(--g-tinta);padding:2px 8px}
.g-niveis{margin:0;display:grid;gap:10px}
.g-niveis>div{display:grid;grid-template-columns:5.5em minmax(0,1fr);gap:4px 14px;background:var(--g-papel);border:1px solid var(--g-linha);padding:12px 14px}
.g-niveis dt{font:700 1rem Arial,Helvetica,sans-serif}.g-niveis dt small{display:block;font-weight:400;font-size:.75rem;color:var(--g-suave)}
.g-niveis dd{margin:0}.g-niveis .ex{margin:6px 0 0;padding-left:12px;border-left:4px solid var(--g-linha);font-style:italic}
.g-niveis .ex b{font:700 .8125rem Arial,Helvetica,sans-serif;font-style:normal;letter-spacing:.1em;text-transform:uppercase;margin-right:6px}
.custa{margin:14px 0 0}.custa b{font:700 .75rem Arial,Helvetica,sans-serif;letter-spacing:.1em;text-transform:uppercase}
ul{margin:6px 0 0;padding-left:22px}
.g-auto{margin:36px 0 0;padding:20px;background:var(--g-papel);border:3px solid var(--g-tinta)}
.g-auto td{height:2.6em}
.g-fb-t{margin:28px 0 0}.g-fb{display:grid;gap:12px;margin:12px 0 0}.g-fb>div{border:2px solid var(--g-tinta);background:var(--g-papel);padding:10px 14px;min-height:7em}
.g-fb h3{font:700 .8rem Arial,Helvetica,sans-serif;letter-spacing:.1em;text-transform:uppercase;margin:0 0 4px}
.g-fb p{font-size:.9rem;color:var(--g-suave);margin:0}
.nome{display:flex;flex-wrap:wrap;gap:8px 32px;font:700 .9rem Arial,Helvetica,sans-serif;margin:12px 0}
.nome span{min-width:12em;border-bottom:1px solid var(--g-tinta);display:inline-block}
footer{margin-top:36px;padding-top:12px;border-top:2px solid var(--g-tinta);font:700 .85rem Arial,Helvetica,sans-serif;display:flex;flex-wrap:wrap;gap:4px 24px}
footer a{color:inherit;min-height:44px;display:inline-flex;align-items:center}
a:focus-visible,button:focus-visible,.g-tab:focus-visible{outline:3px solid currentColor;outline-offset:3px}
@media(max-width:560px){.g-niveis>div{grid-template-columns:1fr}.g-crit h2{flex-wrap:wrap}.g-crit h2 .max{margin-left:0}th,td{padding:6px}td.n,th.n{width:3em;padding:6px 4px}thead th.n{font-size:.8rem}.g-auto{padding:16px 10px}}
@media(min-width:760px){.g-fb{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media screen and (max-width:480px){.g-tab th:nth-child(5),.g-tab td:nth-child(5){display:none}}
@page{size:A4;margin:12mm}
@media print{.g-tab table{table-layout:fixed;width:100%}.g-tab th:first-child{width:55%}.g-tab th.n{width:9%}.g-tab thead th.n{font-size:.8rem}.g-tab td{line-height:1.25}h1{font-size:20pt;margin-bottom:6px}.lead{font-size:11pt}.g-fb-t{margin-top:14px;break-after:avoid-page}.g-fb>div{min-height:7em}.g-fb{gap:8px}.g-fb h3{font-size:9pt}th,td{padding:5px 7px}.g-fb-t{break-after:avoid-page}.g-fb{break-inside:avoid}.custa{break-after:avoid-page}.g-tab small{font-size:8.5pt;line-height:1.3}}
@media print{body{background:#fff;color:#000;font-size:10.5pt}.g-tab{overflow:visible}.g-nav,footer,button{display:none!important}.g-crit,.g-auto{break-inside:avoid}.grelha{padding:0;max-width:none}.g-niveis>div{grid-template-columns:5em minmax(0,1fr)}}
"""


def ital(s):
    """29/10/2026: escapa e põe em itálico os títulos de obras escritos entre _…_ (regra editorial dos itálicos)."""
    return re.sub(r'(?<![\w/])_([^_<>]{1,100}?)_(?!\w)', r'<i>\1</i>', e(s))


def simples(s):
    return re.sub(r'(?<![\w/])_([^_<>]{1,100}?)_(?!\w)', r'\1', s)


def casca(titulo, corpo):
    return ('<!doctype html><html lang="pt-PT" data-appearance-site="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(simples(titulo))} · Português</title><link rel="stylesheet" href="../../../assets/appearance.css?v=20261025-universal-1">'
            '<script src="../../../assets/appearance.js?v=20261025-universal-1"></script>'
            f'<style>{CSS}</style></head><body><main class="grelha">{corpo}</main>'
            '<script>document.querySelectorAll("[data-print]").forEach(function(b){b.hidden=false;b.onclick=function(){window.print()}})</script>'
            '<script defer src="../../../assets/projection-launcher.js?v=20261019.4" data-site="pt"></script></body></html>\n')


def em_listas(desc):
    """06/11/2026: decisão 152. «Antes. Tema A: x; y; z. Explicação: …. Tema B: u; v. Explicação: ….» passa a um parágrafo, e,
    por tema, o título, a lista dos elementos (cada um com o «;» ou o «.» que tinha) e a explicação. Só o texto que lá está."""
    # 08/11/2026: decisão 152, M5. O fecho de cada tema pode ser a explicação ou a conclusão (o tema B da M5-U2).
    m = re.fullmatch(r'(.*? )(Tema A): (.+?)\. ((?:Explicação|Conclusão): .+?\.) (Tema B): (.+?)\. ((?:Explicação|Conclusão): .+?\.)', desc)
    assert m, desc
    html = f'<p>{ital(m[1])}</p>'
    for titulo, itens, explicacao in ((m[2], m[3], m[4]), (m[5], m[6], m[7])):
        partes = itens.split('; ')
        lis = ''.join(f'<li>{ital(p)}{";" if k < len(partes) - 1 else "."}</li>' for k, p in enumerate(partes))
        html += f'<p><b>{ital(titulo)}</b>:</p><ul>{lis}</ul><p>{ital(explicacao)}</p>'
    return html


def intervalo(c, sep=' '):
    # 08/11/2026: decisão 152, M3. sep é o espaço do intervalo (U+00A0 com «nao_partir» na grelha).
    return '1' if c['max'] == 2 else f"1{sep}a{sep}{c['max'] - 1}"


def trocado(x, pares, vistos):
    """12/11/2026: aplica as trocas de vocabulário a todos os textos de uma grelha (só para a página do aluno)."""
    if isinstance(x, str):
        for a, b in pares:
            if a in x:
                vistos.add(a)
                x = x.replace(a, b)
        return x
    if isinstance(x, list):
        return [trocado(i, pares, vistos) for i in x]
    if isinstance(x, dict):
        return {k: (v if k in ('trocas_aluno', 'titulo') else trocado(v, pares, vistos)) for k, v in x.items()}
    return x


def pagina_aluno(slug, t):
    if t.get('trocas_aluno'):
        vistos = set()
        t = trocado(t, t['trocas_aluno'], vistos)
        assert vistos == {a for a, _ in t['trocas_aluno']}, (slug, vistos)
    m = t['modulo'].lower()
    # 08/11/2026: decisão 152, M6. «nao_partir_valores»: «20 valores» com espaço que não quebra.
    valores = '\xa0' if t.get('nao_partir_valores') else ' '
    corpo = (f'<nav class="g-nav" aria-label="Navegação"><a href="{VOLTAR}">← Voltar à tarefa</a><a href="../../../{m}/">Módulo {t["modulo"][1:]}</a>'
             '<button type="button" data-print hidden>Imprimir</button></nav>'
             f'<header><p class="rot">{e(t["modulo"])} · Unidade {t["unidade"]} · Como é avaliado</p><h1>{ital(t["titulo"])}</h1>'
             f'<p class="lead">20{valores}valores em cinco critérios. Lê antes de começar e volta aqui antes de entregar.</p>'
             f'<p>{ital(t["produto"])}</p>'
             + (f'<p class="g-nota">{ital(t["nota"])}</p>' if t.get('nota') else '') + '</header>'
             f'<div class="g-tab" {REGIAO.format("Os cinco critérios")}><table class="g-resumo"><caption>Os cinco critérios</caption><thead><tr><th>Critério</th><th class="n">Máximo</th></tr></thead><tbody>')
    for i, c in enumerate(t['criterios'], 1):
        corpo += f'<tr><td><a href="#criterio-{i}">{ital(c["nome"])}</a></td><td class="n">{c["max"]}</td></tr>'
    corpo += '<tr class="total"><th>Total</th><td class="n">20</td></tr></tbody></table></div>'
    # 08/11/2026: decisão 152, M3. «nao_partir»: o intervalo do nível parcial com espaços que não quebram.
    sep = '\xa0' if t.get('nao_partir') else ' '
    for i, c in enumerate(t['criterios'], 1):
        n = c['niveis']
        corpo += (f'<section class="g-crit" id="criterio-{i}"><h2><span class="num">{i}</span><span>{ital(c["nome"])}</span><span class="max">máx. {c["max"]}</span></h2><dl class="g-niveis">')
        for chave, rotulo, sub in (('0', '0', 'sem evidência'), ('parcial', intervalo(c, sep), 'evidência incompleta'), ('max', str(c['max']), 'cumprimento consistente')):
            desc, ex = n[chave]
            # 06/11/2026: decisão 152. Com «max_em_listas», o nível máximo abre os elementos de cada tema em lista.
            texto = em_listas(desc) if chave == 'max' and c.get('max_em_listas') else f'<p>{ital(desc)}</p>'
            corpo += f'<div><dt>{rotulo}<small>{sub}</small></dt><dd>{texto}<p class="ex"><b>Exemplo</b>{ital(ex)}</p></dd></div>'
        corpo += '</dl><p class="custa"><b>Custa pontos</b></p><ul>' + ''.join(f'<li>{ital(x)}</li>' for x in c['custa']) + '</ul></section>'
    corpo += ('<section class="g-auto" id="autoavaliacao"><h2>Antes de entregar: dá-te pontos</h2>'
              '<p>Em papel, critério a critério: escreve o número e a passagem do teu texto que o prova. '
              + ('Esta autoavaliação é só para ti: não se entrega.</p>' if t.get('autoavaliacao_so_tua') else
                 'Entrega esta autoavaliação com as fotografias. O docente põe a nota dele ao lado da tua e comenta a diferença.</p>') +
              f'<div class="g-tab" {REGIAO.format("Autoavaliação")}><table><thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Eu</th><th>A passagem que o prova</th></tr></thead><tbody>')
    for c in t['criterios']:
        corpo += f'<tr><td>{ital(c["nome"])}</td><td class="n">{c["max"]}</td><td></td><td></td></tr>'
    corpo += ('<tr class="total"><th>Total</th><td class="n">20</td><td></td><td></td></tr></tbody></table></div></section>'
              f'<footer><a href="{VOLTAR}">Voltar à tarefa</a><a href="../correcao/">Para o docente: versão de correção</a></footer>')
    return casca(f'Grelha /20: {t["titulo"]}', corpo)


def pagina_correcao(slug, t):
    # 12/11/2026: «tudo junto». As mesmas palavras do enunciado e da grelha do aluno; sem a nota do aluno, que não se entrega.
    so_tua = bool(t.get('autoavaliacao_so_tua'))
    if t.get('trocas_aluno'):
        vistos = set()
        t = trocado(t, t['trocas_aluno'], vistos)
        assert vistos, slug
    aluno_th, aluno_td = ('', '') if so_tua else ('<th class="n">Aluno</th>', '<td></td>')
    corpo = (f'<nav class="g-nav" aria-label="Navegação"><a href="../grelha/">← Grelha do aluno</a><a href="{VOLTAR}">Tarefa</a>'
             '<button type="button" data-print hidden>Imprimir</button></nav>'
             f'<header><p class="rot">{e(t["modulo"])} · Unidade {t["unidade"]} · Correção</p><h1>{ital(t["titulo"])}</h1>'
             '<p class="lead">Franqueza com cuidado: fala do texto, nunca da pessoa; aponta a passagem; diz o que fazer a seguir.</p>'
             '<p class="nome">Aluno <span></span> Turma <span></span> Data <span></span></p></header>'
             f'<div class="g-tab" {REGIAO.format("Notas por critério")}><table><thead><tr><th>Critério</th><th class="n">Máx.</th>{aluno_th}<th class="n">Docente</th><th>Observações</th></tr></thead><tbody>')
    for c in t['criterios']:
        corpo += f'<tr><td>{ital(c["nome"])}<br><small>{ital(c["niveis"]["max"][0])}</small></td><td class="n">{c["max"]}</td>{aluno_td}<td></td><td></td></tr>'
    corpo += (f'<tr class="total"><th>Total</th><td class="n">20</td>{aluno_td}<td></td><td></td></tr></tbody></table></div>'
              '<h2 class="g-fb-t">Comentário ao aluno</h2><div class="g-fb">'
              '<div><h3>O que funciona</h3><p>Uma coisa concreta, com a passagem.</p></div>'
              '<div><h3>O que te custa pontos</h3><p>O critério e a passagem, sem rodeios.</p></div>'
              '<div><h3>Próximo passo</h3><p>Uma ação que podes fazer já.</p></div>'
              '</div>' + ('' if so_tua else '<p class="custa"><b>Diferença entre a tua nota e a minha</b></p><p>Onde nos afastámos mais de um ponto, a razão está nas observações.</p>') +
              f'<footer><a href="../grelha/">Grelha do aluno</a><a href="{VOLTAR}">Tarefa</a></footer>')
    return casca(f'Correção: {t["titulo"]}', corpo)


def main():
    args, raiz = sys.argv[1:], ROOT
    if '--saida' in args:
        raiz = Path(args[args.index('--saida') + 1]).resolve()
    dados = json.loads(DADOS.read_text('utf-8'))
    for slug, t in dados['tarefas'].items():
        assert sum(c['max'] for c in t['criterios']) == 20, slug
        base = raiz / 'tarefas' / slug
        for pasta, html in (('grelha', pagina_aluno(slug, t)), ('correcao', pagina_correcao(slug, t))):
            p = base / pasta / 'index.html'
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists() or p.read_bytes() != html.encode('utf-8'):
                p.write_text(html, 'utf-8', newline='\n')
        tarefa = base / 'index.html'
        s = (tarefa if tarefa.exists() else ROOT / 'tarefas' / slug / 'index.html').read_text('utf-8')
        # 08/11/2026: decisão 152, M6. A ligação com «Grelha /20» preso também conta (não se acrescenta outra).
        if LIGACAO not in s and LIGACAO_NAO_PARTE not in s:
            assert s.count(ANCORA) == 1, slug
            s = s.replace(ANCORA, LIGACAO + ANCORA)
            tarefa.write_text(s, 'utf-8', newline='\n')
        print('grelha:', slug)


if __name__ == '__main__':
    main()
