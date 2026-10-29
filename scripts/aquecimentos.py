#!/usr/bin/env python3
"""Aquecimentos em cartões antes das aulas de tarefa (29/10/2026, decisão do docente; piloto no M7).

Lê docs/pedagogia/aquecimentos/<slug>.json e escreve tarefas/<slug>/aquecimento/index.html no molde de uma lição
sem a Sala, com o motor e a casca atuais:

* o CSS de computador da casca (<style id="casca-pc">) copia-se, em tempo de geração, da lição-molde
  m4/licao-m4-f28/index.html, para não se copiar uma lição à mão (falha se o bloco não aparecer uma vez);
* motor partilhado (assets/pt-lessons/casca.js e jogo.js, em defer), banco CARTOES embutido num script que espera
  pelo DOMContentLoaded, como em m2/licao-m2-f12 (assim scripts/audit_cards.lesson_cards lê-o sem configuração);
* chave de progresso própria, «aquecimento-<slug>»: não começa por licao-, percurso-, desafio- nem epi-pt-, por isso
  não conta como lição no percurso, não mexe no «Continuar» e não entra no learning_storage dos testes de browser das
  tarefas; não escreve «epi-ultima». Com ?projetar=1 o motor não grava nada (modo de aula).

Antes de escrever, valida o baralho e recusa-o com a lista dos erros:
* scripts/audit_cards.validate_cards, o validador do sítio;
* cada opção errada de uma «escolha» ou de um «rever» com explicação («fe» por opção, null na certa) e «fe» nos outros
  tipos de fazer;
* nenhuma palavra ou sinal proibido no texto do aluno («jog», «ficha», «folha», «professor», «—», «·» dentro de uma
  frase), também em «trecho», «apoio» e «cita»;
* cada citação entre «» com 12 ou mais carateres (versos separados por « / ») está letra a letra nas páginas de
  «licoes_das_citacoes» (as marcas ** de negrito não contam); as frases inventadas escrevem-se sem «»;
* nenhum cartão de fazer usa as passagens «reservadas» à tarefa (o aquecimento não faz a tarefa por ti); a comparação
  não distingue maiúsculas (revisão técnica de 29/10/2026);
* o título, a descrição e o menu (texto visível no <h1>, no <title>, na meta descrição e no menu) também passam pelas
  palavras e sinais proibidos (revisão técnica de 29/10/2026).
«momento» (opcional) diz no menu quando se faz o aquecimento: «Antes de começar» na U1, «No início da aula de tarefa» na
U2 e na U3 (revisão pedagógica de 29/10/2026, para a página dizer o mesmo que a tarefa e a linha A do percurso).
Carrega rever-frase.js sempre que o baralho tem um cartão «rever» (o tipo não vive em jogo.js).

Uso: python3 scripts/aquecimentos.py [--saida PASTA] [--dados PASTA] [slug ...]
Idempotente: só reescreve um ficheiro quando o conteúdo muda. --saida escreve noutra raiz, para os testes compararem
sem mexer na árvore.
"""
from html import escape
from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs' / 'pedagogia' / 'aquecimentos'
MOLDE = 'm4/licao-m4-f28/index.html'
V_JOGO = '20261021-ux06'
PROIBIDAS = (r'\bjog', r'\bficha', r'\bfolha', r'\bprofessor', '—')
# Tipos que não vivem em jogo.js: o gerador carrega o script respetivo logo depois do motor.
EXTERNOS = {'rever': 'rever-frase.js?v=20261021'}
COM_FE_POR_OPCAO = ('escolha', 'rever')
FAZER_COM_FE = ('vf', 'completar', 'emparelhar', 'ordenar', 'frase', 'sublinhar')
BOTAO_PROJETAR = 'Projetar para a turma'
MOMENTO = 'Antes da aula de tarefa'  # por omissão, quando o baralho não diz «momento»
CAMPOS = ('slug', 'modulo', 'unidade', 'versao', 'titulo', 'descricao', 'licoes_das_citacoes', 'cartoes')


def molde(raiz):
    s = (raiz / MOLDE).read_text('utf-8')
    estilo = re.findall(r'<style id="casca-pc">.*?</style>', s, re.S)
    if len(estilo) != 1:
        raise SystemExit('O molde mudou: <style id="casca-pc"> não aparece uma vez em ' + MOLDE)
    return estilo[0]


def sem_marcas(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def texto_visivel(c):
    """Tudo o que o aluno lê num cartão (sem marcas HTML)."""
    partes = []
    for k in ('p', 'p2', 'frase', 'f', 'titulo', 'html', 'rot', 'trecho', 'apoio', 'cita'):
        if isinstance(c.get(k), str):
            partes.append(c[k])
    for k in ('o', 'passos', 'palavras', 'linhas'):
        partes += [x for x in c.get(k, []) if isinstance(x, str)]
    for par in c.get('pares', []):
        partes += par
    for lacuna in c.get('lacunas', []):
        partes += lacuna.get('o', [])
    fe = c.get('fe')
    partes += [x for x in (fe if isinstance(fe, list) else [fe]) if isinstance(x, str)]
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', ' '.join(partes)))


def plano(raiz, pagina):
    s = (raiz / pagina / 'index.html').read_text('utf-8')
    s = s.replace('\\"', '"').replace('\\n', ' ').replace('**', '')
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))


def validar(raiz, d):
    sys.path.insert(0, str(raiz / 'scripts'))
    from audit_cards import validate_cards  # noqa: E402  (o validador do sítio, sem cópia)
    erros = [f'falta o campo «{k}»' for k in CAMPOS if k not in d]
    if erros:
        return erros
    if not d['slug'].startswith(d['modulo'] + '-u'):
        erros.append('o slug não é da forma <módulo>-u<n>')
    cartoes = d['cartoes']
    erros += list(validate_cards(cartoes))
    for pagina in d['licoes_das_citacoes']:
        if not (raiz / pagina / 'index.html').is_file():
            erros.append(f'«licoes_das_citacoes»: não existe {pagina}/index.html')
    fontes = ' '.join(plano(raiz, p) for p in d['licoes_das_citacoes'] if (raiz / p / 'index.html').is_file())
    reservadas = d.get('reservadas', [])
    for n, c in enumerate(cartoes, 1):
        t = c.get('t')
        if t in COM_FE_POR_OPCAO:
            fe = c.get('fe')
            if not isinstance(fe, list) or len(fe) != len(c.get('o', [])):
                erros.append(f'cartão {n}: «fe» tem de explicar cada opção (lista do tamanho de «o»)')
            else:
                for j, x in enumerate(fe):
                    if j == c.get('c') and x is not None:
                        erros.append(f'cartão {n}: a opção certa leva null em «fe»')
                    if j != c.get('c') and not (isinstance(x, str) and x.strip()):
                        erros.append(f'cartão {n}: a opção errada {j} não diz porquê')
        elif t in FAZER_COM_FE:
            if not (isinstance(c.get('fe'), str) and c['fe'].strip()):
                erros.append(f'cartão {n}: falta «fe» (o que se diz a quem erra)')
        visivel = texto_visivel(c).replace('**', '')
        for padrao in PROIBIDAS:
            if re.search(padrao, visivel, re.I):
                erros.append(f'cartão {n}: texto proibido {padrao!r}')
        if re.search(r'\w ·|· \w', visivel):
            erros.append(f'cartão {n}: «·» dentro de uma frase')
        for citacao in re.findall(r'«([^»]{12,})»', visivel):
            for verso in [v.strip() for v in citacao.split(' / ')]:
                if verso not in fontes:
                    erros.append(f'cartão {n}: citação que não está letra a letra nas lições indicadas: «{verso}»')
        if t != 'ler':
            for r in reservadas:
                # 29/10/2026 (revisão técnica): sem distinguir maiúsculas («Dá força a um país?» também é a pergunta do tema).
                if r.casefold() in visivel.casefold():
                    erros.append(f'cartão {n}: usa uma passagem reservada à tarefa: «{r}»')
    # 29/10/2026 (revisão técnica): o título, a descrição, o momento e o menu também são texto visível.
    cabeca = sem_marcas(' '.join([d['titulo'], d['descricao'], d.get('momento', '')] + [t for _, t in d.get('menu', [])]))
    for padrao in PROIBIDAS:
        if re.search(padrao, cabeca, re.I):
            erros.append(f'título, descrição ou menu: texto proibido {padrao!r}')
    if re.search(r'\w ·|· \w', cabeca):
        erros.append('título, descrição ou menu: «·» dentro de uma frase')
    if not any(c.get('t') != 'ler' for c in cartoes):
        erros.append('o baralho não tem cartões de fazer')
    return erros


def scripts_externos(d):
    tipos = {c.get('t') for c in d['cartoes']}
    return ''.join(f'<script defer src="../../../assets/pt-lessons/{EXTERNOS[t]}"></script>'
                   for t in sorted(tipos) if t in EXTERNOS)


def pagina(raiz, d):
    slug, m, u = d['slug'], d['modulo'], d['unidade']
    M = m.upper()
    unidade = f'../../../{m}/#unidade-pedagogica-{u}'
    chave = 'aquecimento-' + slug
    titulo = d['titulo']
    simples = sem_marcas(titulo)
    menu = ''.join(f'<a href="{escape(h)}">{escape(t, quote=False)}</a>' for h, t in d.get('menu', []))
    cfg = {
        'marca': M, 'titulo': 'Aquecer: ' + simples, 'variar': False, 'gestalt': True,
        'percurso': unidade, 'seguinte': '../', 'seguinteRotulo': 'Abrir a aula de tarefa',
    }
    if d.get('versao'):
        cfg['versao'] = d['versao']
    cfg_js = json.dumps(cfg, ensure_ascii=False)[1:-1]
    banco = json.dumps(d['cartoes'], ensure_ascii=False).replace('</', '<\\/')
    depois = (f'<p><a href="../">Abrir a aula de tarefa</a> · <a href="{unidade}">Voltar à unidade {u}</a></p>')
    return (
        '<!doctype html><html lang="pt-PT" data-appearance-site="pt" data-appearance-family="cards"><head>'
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<title>Aquecer · {escape(simples, quote=False)} · {M}</title>'
        f'<meta name="description" content="{escape(d["descricao"])}">'
        '<link rel="stylesheet" href="../../../assets/pt-lessons/lesson.css">'
        '<script defer src="../../../assets/pt-lessons/casca.js"></script>'
        f'<script defer src="../../../assets/pt-lessons/jogo.js?v={V_JOGO}"></script>'
        + scripts_externos(d) + molde(raiz) +
        '<link rel="stylesheet" href="../../../assets/appearance.css?v=20261025-universal-1">'
        '<script src="../../../assets/appearance.js?v=20261025-universal-1"></script></head>'
        f'<body data-unit-return="{unidade}" data-unit-number="{u}">'
        '<div class="casca" data-casca><header class="casca-topo">'
        f'<a class="c-marca" href="../" aria-label="Voltar à aula de tarefa da unidade {u} do módulo {m[1:]}">{M}</a>'
        '<span class="c-num" data-c-num></span><button type="button" class="c-barra" data-c-barra aria-label="Ver os cartões já feitos" disabled>'
        '<svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg></button>'
        '<span class="c-modo" data-c-modo hidden></span>'
        '<button type="button" class="c-ic" data-c-som aria-pressed="false" aria-label="Som"><span class="c-roda">♪</span></button>'
        '<button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false"><span class="c-tres"></span></button></header>'
        f'<h1 class="c-sr">Aquecer: {titulo}</h1>'
        '<main class="casca-corpo" tabindex="-1"><div id="baralho" class="jogo-alvo"></div></main>'
        '<footer class="casca-acoes" data-c-acoes></footer>'
        '<section class="casca-folha" data-c-folha role="status" aria-live="polite" hidden></section>'
        '<div class="casca-menu" data-c-painel hidden><div class="c-menu-in" role="dialog" aria-label="Menu"><div class="c-menu-cab">'
        f'<p>Módulo {m[1:]} · {escape(d.get("momento", MOMENTO), quote=False)}<br>Unidade {u}</p>'
        '<button type="button" class="c-ic" data-c-fecha-menu aria-label="Fechar o menu">✕</button></div>'
        f'<nav aria-label="Navegação do aquecimento"><a href="../">Aula de tarefa</a><a href="{unidade}">Unidade {u} no percurso</a>'
        f'{menu}<a href="?projetar=1">{BOTAO_PROJETAR}</a></nav>'
        '<p class="c-menu-extra">Aquecimento com consulta livre; não conta para a nota. O progresso fica neste aparelho.</p></div></div></div>'
        f'<noscript>Este aquecimento precisa de JavaScript. <a href="../">Abrir a aula de tarefa</a>.</noscript>'
        '<script>document.addEventListener("DOMContentLoaded",function(){"use strict";'
        f'var K="{chave}",CARTOES={banco};'
        'var C=EPICasca.pagina();EPIJogo.montar({casca:C,el:document.getElementById("baralho"),itens:CARTOES,'
        f'chave:K,{cfg_js},depois:{json.dumps(depois, ensure_ascii=False)}}});}});</script>'
        '<script defer src="../../../assets/projection-launcher.js?v=20261019.4" data-site="pt"></script></body></html>\n'
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--raiz', default=str(ROOT), help='raiz do sítio pt (só leitura, salvo sem --saida)')
    ap.add_argument('--dados', help='pasta dos JSON (por omissão, <raiz>/docs/pedagogia/aquecimentos)')
    ap.add_argument('--saida', help='raiz onde escrever (por omissão, a própria raiz)')
    ap.add_argument('slugs', nargs='*')
    a = ap.parse_args(argv)
    raiz = Path(a.raiz).resolve()
    dados = Path(a.dados).resolve() if a.dados else raiz / 'docs/pedagogia/aquecimentos'
    saida = Path(a.saida).resolve() if a.saida else raiz
    feitos, falhas = [], {}
    for p in sorted(dados.glob('*.json')):
        d = json.loads(p.read_text('utf-8'))
        if p.stem != d.get('slug'):
            falhas[p.stem] = ['o nome do ficheiro não é o slug']
            continue
        if a.slugs and d['slug'] not in a.slugs:
            continue
        erros = validar(raiz, d)
        if erros:
            falhas[d['slug']] = erros
            continue
        alvo = saida / 'tarefas' / d['slug'] / 'aquecimento' / 'index.html'
        html = pagina(raiz, d)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        if not alvo.exists() or alvo.read_text('utf-8') != html:
            alvo.write_text(html, 'utf-8')
        feitos.append(d['slug'])
    for slug, erros in falhas.items():
        print(f'NÃO GERADO {slug}:', *erros, sep='\n  ', file=sys.stderr)
    print('Aquecimentos gerados: ' + (', '.join(feitos) or 'nenhum'))
    return 1 if falhas else 0


if __name__ == '__main__':
    sys.exit(main())
