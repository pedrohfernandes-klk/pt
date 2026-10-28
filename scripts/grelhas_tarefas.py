"""Grelhas /20 das tarefas de unidade (27/10/2026): página do aluno, versão de correção e ligação na tarefa.

Dados em docs/pedagogia/grelhas-tarefas-20261027.json. Para cada tarefa escreve:
- tarefas/<slug>/grelha/: os critérios com os níveis 0, parcial e máximo, um exemplo por nível, o que custa
  pontos e a autoavaliação em papel antes de entregar;
- tarefas/<slug>/correcao/: a grelha de correção do docente, com a nota do aluno ao lado e o feedback em três
  partes (o que funciona, o que custa pontos, o próximo passo);
- na tarefa, uma linha em «Verificar e entregar» com a ligação à grelha (marca autorizada nos testes).
Idempotente. Uso: python3 scripts/grelhas_tarefas.py
"""
from html import escape as e
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs/pedagogia/grelhas-tarefas-20261027.json'
LIGACAO = '<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>\n'
ANCORA = '<p>Fecha com duas linhas'
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
.lead{font-size:1.15rem;margin:0 0 8px}p{margin:0 0 12px}
table{width:100%;border-collapse:collapse;background:var(--g-papel);margin:16px 0 8px}
.g-tab{overflow-x:auto;margin:16px 0 8px}.g-tab>table{margin:0}
caption{text-align:left;font:700 .75rem Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:0 0 8px}
th,td{border:1px solid var(--g-linha);padding:8px 10px;text-align:left;vertical-align:top}
thead th{font:700 .8rem Arial,Helvetica,sans-serif;border-bottom:2px solid var(--g-tinta)}
td.n,th.n{text-align:center;width:4.5em;font:700 1rem Arial,Helvetica,sans-serif}
tr.total th,tr.total td{border-top:2px solid var(--g-tinta);font-weight:700}
.g-crit{margin:28px 0 0;padding:20px 0 0;border-top:2px solid var(--g-tinta)}
.g-crit h2{display:flex;gap:12px;align-items:baseline}.g-crit h2 .num{font-size:1.6rem}.g-crit h2 .max{margin-left:auto;font-size:.85rem;white-space:nowrap;border:2px solid var(--g-tinta);padding:2px 8px}
.g-niveis{margin:0;display:grid;gap:10px}
.g-niveis>div{display:grid;grid-template-columns:5.5em minmax(0,1fr);gap:4px 14px;background:var(--g-papel);border:1px solid var(--g-linha);padding:12px 14px}
.g-niveis dt{font:700 1rem Arial,Helvetica,sans-serif}.g-niveis dt small{display:block;font-weight:400;font-size:.75rem;color:var(--g-suave)}
.g-niveis dd{margin:0}.g-niveis .ex{margin:6px 0 0;padding-left:12px;border-left:4px solid var(--g-linha);font-style:italic}
.g-niveis .ex b{font:700 .7rem Arial,Helvetica,sans-serif;font-style:normal;letter-spacing:.1em;text-transform:uppercase;margin-right:6px}
.custa{margin:14px 0 0}.custa b{font:700 .75rem Arial,Helvetica,sans-serif;letter-spacing:.1em;text-transform:uppercase}
ul{margin:6px 0 0;padding-left:22px}
.g-auto{margin:36px 0 0;padding:20px;background:var(--g-papel);border:3px solid var(--g-tinta)}
.g-auto td{height:2.6em}
.g-fb{display:grid;gap:12px;margin:16px 0 0}.g-fb>div{border:2px solid var(--g-tinta);background:var(--g-papel);padding:10px 14px;min-height:7em}
.g-fb h3{font:700 .8rem Arial,Helvetica,sans-serif;letter-spacing:.1em;text-transform:uppercase;margin:0 0 4px}
.g-fb p{font-size:.9rem;color:var(--g-suave);margin:0}
.nome{display:flex;flex-wrap:wrap;gap:8px 32px;font:700 .9rem Arial,Helvetica,sans-serif;margin:12px 0}
.nome span{min-width:12em;border-bottom:1px solid var(--g-tinta);display:inline-block}
footer{margin-top:36px;padding-top:12px;border-top:2px solid var(--g-tinta);font:700 .85rem Arial,Helvetica,sans-serif;display:flex;flex-wrap:wrap;gap:4px 24px}
footer a{color:inherit;min-height:44px;display:inline-flex;align-items:center}
a:focus-visible,button:focus-visible,.g-tab:focus-visible{outline:3px solid currentColor;outline-offset:3px}
@media(max-width:560px){.g-niveis>div{grid-template-columns:1fr}.g-crit h2{flex-wrap:wrap}.g-crit h2 .max{margin-left:0}th,td{padding:6px}td.n,th.n{width:3em;padding:6px 4px}thead th.n{font-size:.8rem}.g-auto{padding:16px 10px}}
@media(min-width:760px){.g-fb{grid-template-columns:repeat(3,minmax(0,1fr))}}
@page{size:A4;margin:12mm}
@media print{body{background:#fff;color:#000;font-size:10.5pt}.g-tab{overflow:visible}.g-nav,footer,button{display:none!important}.g-crit,.g-auto{break-inside:avoid}.grelha{padding:0;max-width:none}.g-niveis>div{grid-template-columns:5em minmax(0,1fr)}}
"""


def casca(titulo, corpo):
    return ('<!doctype html><html lang="pt-PT" data-appearance-site="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(titulo)} · Português</title><link rel="stylesheet" href="../../../assets/appearance.css?v=20261025-universal-1">'
            '<script src="../../../assets/appearance.js?v=20261025-universal-1"></script>'
            f'<style>{CSS}</style></head><body><main class="grelha">{corpo}</main>'
            '<script>document.querySelectorAll("[data-print]").forEach(function(b){b.hidden=false;b.onclick=function(){window.print()}})</script>'
            '<script defer src="../../../assets/projection-launcher.js?v=20261019.4" data-site="pt"></script></body></html>\n')


def intervalo(c):
    return '1' if c['max'] == 2 else f"1 a {c['max'] - 1}"


def pagina_aluno(slug, t):
    m = t['modulo'].lower()
    corpo = (f'<nav class="g-nav" aria-label="Navegação"><a href="../">← Voltar à tarefa</a><a href="../../../{m}/">Módulo {t["modulo"][1:]}</a>'
             '<button type="button" data-print hidden>Imprimir</button></nav>'
             f'<header><p class="rot">{e(t["modulo"])} · Unidade {t["unidade"]} · Como é avaliado</p><h1>{e(t["titulo"])}</h1>'
             '<p class="lead">20 valores em cinco critérios. Lê antes de começar e volta aqui antes de entregar.</p>'
             f'<p>{e(t["produto"])}</p></header>'
             f'<div class="g-tab" {REGIAO.format("Os cinco critérios")}><table class="g-resumo"><caption>Os cinco critérios</caption><thead><tr><th>Critério</th><th class="n">Máximo</th></tr></thead><tbody>')
    for i, c in enumerate(t['criterios'], 1):
        corpo += f'<tr><td><a href="#criterio-{i}">{e(c["nome"])}</a></td><td class="n">{c["max"]}</td></tr>'
    corpo += '<tr class="total"><th>Total</th><td class="n">20</td></tr></tbody></table></div>'
    for i, c in enumerate(t['criterios'], 1):
        n = c['niveis']
        corpo += (f'<section class="g-crit" id="criterio-{i}"><h2><span class="num">{i}</span><span>{e(c["nome"])}</span><span class="max">máx. {c["max"]}</span></h2><dl class="g-niveis">')
        for chave, rotulo, sub in (('0', '0', 'sem evidência'), ('parcial', intervalo(c), 'evidência incompleta'), ('max', str(c['max']), 'cumprimento consistente')):
            desc, ex = n[chave]
            corpo += f'<div><dt>{rotulo}<small>{sub}</small></dt><dd><p>{e(desc)}</p><p class="ex"><b>Exemplo</b>{e(ex)}</p></dd></div>'
        corpo += '</dl><p class="custa"><b>Custa pontos</b></p><ul>' + ''.join(f'<li>{e(x)}</li>' for x in c['custa']) + '</ul></section>'
    corpo += ('<section class="g-auto" id="autoavaliacao"><h2>Antes de entregar: dá-te pontos</h2>'
              '<p>Em papel, critério a critério: escreve o número e a passagem do teu texto que o prova. Entrega esta autoavaliação com as fotografias. '
              'O docente põe a nota dele ao lado da tua e comenta a diferença.</p>'
              f'<div class="g-tab" {REGIAO.format("Autoavaliação")}><table><thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Eu</th><th>A passagem que o prova</th></tr></thead><tbody>')
    for c in t['criterios']:
        corpo += f'<tr><td>{e(c["nome"])}</td><td class="n">{c["max"]}</td><td></td><td></td></tr>'
    corpo += ('<tr class="total"><th>Total</th><td class="n">20</td><td></td><td></td></tr></tbody></table></div></section>'
              f'<footer><a href="../">Voltar à tarefa</a><a href="../correcao/">Para o docente: versão de correção</a></footer>')
    return casca(f'Grelha /20: {t["titulo"]}', corpo)


def pagina_correcao(slug, t):
    corpo = ('<nav class="g-nav" aria-label="Navegação"><a href="../grelha/">← Grelha do aluno</a><a href="../">Tarefa</a>'
             '<button type="button" data-print hidden>Imprimir</button></nav>'
             f'<header><p class="rot">{e(t["modulo"])} · Unidade {t["unidade"]} · Correção</p><h1>{e(t["titulo"])}</h1>'
             '<p class="lead">Franqueza com cuidado: fala do texto, nunca da pessoa; aponta a passagem; diz o que fazer a seguir.</p>'
             '<p class="nome">Aluno <span></span> Turma <span></span> Data <span></span></p></header>'
             f'<div class="g-tab" {REGIAO.format("Notas por critério")}><table><thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Aluno</th><th class="n">Docente</th><th>Observações</th></tr></thead><tbody>')
    for c in t['criterios']:
        corpo += f'<tr><td>{e(c["nome"])}<br><small>{e(c["niveis"]["max"][0])}</small></td><td class="n">{c["max"]}</td><td></td><td></td><td></td></tr>'
    corpo += ('<tr class="total"><th>Total</th><td class="n">20</td><td></td><td></td><td></td></tr></tbody></table></div>'
              '<div class="g-fb">'
              '<div><h3>O que funciona</h3><p>Uma coisa concreta, com a passagem.</p></div>'
              '<div><h3>O que te custa pontos</h3><p>O critério e a passagem, sem rodeios.</p></div>'
              '<div><h3>Próximo passo</h3><p>Uma ação que podes fazer já.</p></div>'
              '</div><p class="custa"><b>Diferença entre a tua nota e a minha</b></p><p>Onde nos afastámos mais de um ponto, a razão está nas observações.</p>'
              '<footer><a href="../grelha/">Grelha do aluno</a><a href="../">Tarefa</a></footer>')
    return casca(f'Correção: {t["titulo"]}', corpo)


def main():
    dados = json.loads(DADOS.read_text('utf-8'))
    for slug, t in dados['tarefas'].items():
        assert sum(c['max'] for c in t['criterios']) == 20, slug
        base = ROOT / 'tarefas' / slug
        for pasta, html in (('grelha', pagina_aluno(slug, t)), ('correcao', pagina_correcao(slug, t))):
            p = base / pasta / 'index.html'
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists() or p.read_text('utf-8') != html:
                p.write_text(html, 'utf-8')
        tarefa = base / 'index.html'
        s = tarefa.read_text('utf-8')
        if LIGACAO not in s:
            assert s.count(ANCORA) == 1, slug
            s = s.replace(ANCORA, LIGACAO + ANCORA)
            tarefa.write_text(s, 'utf-8')
        print('grelha:', slug)


if __name__ == '__main__':
    main()
