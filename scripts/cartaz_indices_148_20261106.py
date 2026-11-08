#!/usr/bin/env python3
"""06/11/2026: decisão 148. O desenho do índice do M4 (#166) passa aos nove índices do Português.

Constrói scripts/cartaz_indices_148_20261106.json, a camada literal que dá aos nove índices (m1/ a m9/index.html) o
desenho do piloto M4, com as três mudanças da decisão 148: a palavra do módulo à vista (só CSS), a imagem documental mais
pequena a seguir às unidades e os botões flutuantes de sempre (modo noturno e acesso do docente) fora de «Recursos do
módulo». A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/cartaz-indices-148-edits-20261106.json:

  python3 scripts/cartaz_indices_148_20261106.py
  python3 scripts/aplicar_trocas.py scripts/cartaz_indices_148_20261106.json --manifesto tests/fixtures/cartaz-indices-148-edits-20261106.json --nota "…"

As trocas calculam-se sobre a base (o texto de cada página com esta camada desfeita, pelo manifesto, quando ele já existe):
o script pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON. Só muda a camada de desenho: ligações,
âncoras, ids, chaves de progresso, dados do motor e textos ficam todos, pela mesma ordem; a imagem documental muda de sítio
sem mudar uma letra; o título de cada unidade passa do cabeçalho do grupo para a banda da unidade (o mesmo <h2> com o mesmo
id, como no M4); a prova esperada passa para junto da pergunta da unidade.

Nos oito índices que ainda tinham o desenho de 1/11 (cartaz-indices.css):
- os estilos passam a assets/cartaz-indice-comum.css e o script dos recursos (assets/cartaz-indice-comum.js) entra antes de
  </body>; o <main> ganha data-cz-indice="20261106";
- a imagem sai da abertura e o bloco «Mapa do módulo» e «Como se cumpre uma unidade» passa para <details
  class="cz-recursos"> («Recursos do módulo»), logo a seguir ao cabeçalho, como no M4;
- em cada unidade, o <span class="cz-fold-t"> da banda passa ao <h2 class="cz-fold-t" id="unidade-pedagogica-N"> (o
  <h2> do cabeçalho do grupo sai, com o mesmo texto), o cabeçalho do grupo e o percurso ficam dentro de <div
  class="cz-unit-body">, e a prova esperada sobe para o fim do cabeçalho do grupo;
- a imagem documental fica logo a seguir à última unidade.

No M4 (que já tinha o piloto):
- os estilos e o script do piloto passam aos comuns e data-m4-piloto="20261102" passa a data-cz-indice="20261106";
- <details class="m4-recursos"> passa a <details class="cz-recursos">, <nav class="m4-resource-links"> volta a <nav
  class="ligas"> e as três <div class="m4-unit-body"> passam a <div class="cz-unit-body">;
- dentro dos recursos ficam só o mapa e a regra: a imagem passa para depois das unidades, o acesso do docente volta a
  flutuar no sítio de onde o piloto o tirou (igual ao dos outros oito) e o lugar do modo noturno («Neste aparelho») sai,
  para o botão voltar a flutuar.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/cartaz_indices_148_20261106.json'
MANIFESTO = ROOT / 'tests/fixtures/cartaz-indices-148-edits-20261106.json'
# 07/11/2026: a camada que fica por cima desta (os acertos da decisão 173); base() desfá-la primeiro.
ACERTOS = ROOT / 'tests/fixtures/indices-acertos-edits-20261107.json'
# 07/11/2026 (fusão do main 29441e6b no pedido #182): por cima dos acertos fica a decisão 152 no M1.
CUIDADO = ROOT / 'tests/fixtures/cuidado-m1-edits-20261106.json'
# 07/11/2026: por cima da decisão 152 no M1 ficam os créditos atrás de um «i» do pedido pt-1 (a imagem documental dos índices).
CREDITOS_PT1 = ROOT / 'tests/fixtures/creditos-i-pt1-edits-20261107.json'
# 08/11/2026: por cima dos créditos do pedido pt-1 fica o cartaz «Ler a cidade» e o nome novo da secção (a frase da sugestão dos índices).
CIDADE_CARTAZ = ROOT / 'tests/fixtures/cidade-cartaz-edits-20261108.json'
# 08/11/2026: por cima do cartaz «Ler a cidade» fica a decisão 152 no M2 (os espaços que não quebram no índice do M2).
CUIDADO_M2 = ROOT / 'tests/fixtures/cuidado-m2-edits-20261108.json'
# 08/11/2026: por cima da decisão 152 no M2 fica a decisão 152 no M3 (a tabela dos pesos e os espaços que não quebram no índice do M3).
CUIDADO_M3 = ROOT / 'tests/fixtures/cuidado-m3-edits-20261108.json'
VERSAO = '20261106'
ACHADO = ('06/11/2026: decisão 148 (o desenho do índice do M4 passa aos nove, com a palavra do módulo, a imagem documental '
          'mais pequena a seguir às unidades e os botões flutuantes de sempre). {o}')
OITO = (1, 2, 3, 5, 6, 7, 8, 9)
ESTILOS_ANTIGOS = '<link rel="stylesheet" href="../assets/cartaz-indices.css?v=20261101">'
ESTILOS_COMUNS = f'<link rel="stylesheet" href="../assets/cartaz-indice-comum.css?v={VERSAO}">'
SCRIPT_NOVO = f'<script src="../assets/cartaz-indice-comum.js?v={VERSAO}"></script>'
# O bloco flutuante dos materiais do docente que o piloto M4 tirou (é o «antigo» da segunda troca do piloto).
PILOTO = json.loads((ROOT / 'scripts/cartaz_m4_piloto_20261102.json').read_text('utf-8'))
DOCENTE_FLUTUANTE_M4 = next(t['antigo'] for t in PILOTO if t['local'] == 'M4 retirar a cópia flutuante dos materiais')
COMENTARIO_PILOTO = next(t['novo'] for t in PILOTO if t['local'] == 'M4 retirar a cópia flutuante dos materiais')


def base(rel):
    """O texto da página sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 08/11/2026: antes de tudo, a decisão 152 no M3 (camada cuidado_m3_20261108), a mais recente, com contagem estrita.
    for edit in reversed(json.loads(CUIDADO_M3.read_text('utf-8'))['files'].get(rel, {}).get('edits', []) if CUIDADO_M3.is_file() else []):
        if texto.count(edit['new']) != edit['occurrences']:
            raise SystemExit(f'{rel}: a decisão 152 no M3 já não confere ({edit["location"]})')
        texto = texto.replace(edit['new'], edit['old'])
    # 08/11/2026: antes de tudo, a decisão 152 no M2 (camada cuidado_m2_20261108), a mais recente, com contagem estrita.
    for edit in reversed(json.loads(CUIDADO_M2.read_text('utf-8'))['files'].get(rel, {}).get('edits', []) if CUIDADO_M2.is_file() else []):
        if texto.count(edit['new']) != edit['occurrences']:
            raise SystemExit(f'{rel}: a decisão 152 no M2 já não confere ({edit["location"]})')
        texto = texto.replace(edit['new'], edit['old'])
    # 08/11/2026: antes de tudo, o cartaz «Ler a cidade» e o nome novo da secção (camada cidade_cartaz_20261108), a mais recente, com contagem estrita.
    for edit in reversed(json.loads(CIDADE_CARTAZ.read_text('utf-8'))['files'].get(rel, {}).get('edits', []) if CIDADE_CARTAZ.is_file() else []):
        if texto.count(edit['new']) != edit['occurrences']:
            raise SystemExit(f'{rel}: o cartaz «Ler a cidade» e o nome novo da secção já não conferem ({edit["location"]})')
        texto = texto.replace(edit['new'], edit['old'])
    # 07/11/2026: antes de tudo, os créditos atrás de um «i» do pedido pt-1 (camada creditos_i_pt1_20261107), a mais recente, com contagem estrita.
    for edit in reversed(json.loads(CREDITOS_PT1.read_text('utf-8'))['files'].get(rel, {}).get('edits', []) if CREDITOS_PT1.is_file() else []):
        if texto.count(edit['new']) != edit['occurrences']:
            raise SystemExit(f'{rel}: os créditos atrás de um «i» do pedido pt-1 já não conferem ({edit["location"]})')
        texto = texto.replace(edit['new'], edit['old'])
    # 07/11/2026 (fusão do main 29441e6b no pedido #182): antes de tudo, a decisão 152 no M1 (camada cuidado_m1_20261106), a mais recente, com contagem estrita.
    for edit in reversed(json.loads(CUIDADO.read_text('utf-8'))['files'].get(rel, {}).get('edits', []) if CUIDADO.is_file() else []):
        if texto.count(edit['new']) != edit['occurrences']:
            raise SystemExit(f'{rel}: a decisão 152 no M1 já não confere ({edit["location"]})')
        texto = texto.replace(edit['new'], edit['old'])
    # 07/11/2026: antes, os acertos da decisão 173 (camada indices_acertos_20261107), que estão por cima desta, com contagem estrita.
    for edit in reversed(json.loads(ACERTOS.read_text('utf-8'))['files'].get(rel, {}).get('edits', []) if ACERTOS.is_file() else []):
        if texto.count(edit['new']) != edit['occurrences']:
            raise SystemExit(f'{rel}: os acertos da decisão 173 já não conferem ({edit["location"]})')
        texto = texto.replace(edit['new'], edit['old'])
    if MANIFESTO.is_file():
        for edit in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    return texto


def um(texto, padrao, rel, o_que):
    achados = re.findall(padrao, texto, re.S)
    if len(achados) != 1:
        raise SystemExit(f'{rel}: {o_que} aparece {len(achados)} vezes')
    return achados[0]


def troca(rel, local, antigo, novo, texto):
    if texto.count(antigo) != 1:
        raise SystemExit(f'{rel}: «{local}» aparece {texto.count(antigo)} vezes')
    return {'ficheiro': rel, 'local': local, 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
            'achado': ACHADO.format(o=local + '.')}


def unidades(rel, texto):
    """Cada unidade: (n, secção inteira). A secção vai de <section ... class="unidade-pedagogica"> a </details></section>."""
    secoes = re.findall(r'<section\b[^>]*\bclass="unidade-pedagogica"[^>]*>.*?</details></section>', texto, re.S)
    if not secoes:
        raise SystemExit(f'{rel}: sem unidades')
    return [(int(um(s, r'data-unidade="(\d+)"', rel, 'data-unidade')), s) for s in secoes]


def trocas_unidades(rel, texto, figura):
    """Banda com o <h2>, corpo da unidade e prova junto da pergunta; a imagem a seguir à última unidade."""
    lista = unidades(rel, texto)
    saida = []
    for i, (n, secao) in enumerate(lista):
        titulo = um(secao, r'<span class="cz-fold-t">(.*?)</span>', rel, f'título da banda da unidade {n}')
        saida.append(troca(rel, f'M{rel[1]} unidade {n}: o título passa para a banda',
                           f'<span class="cz-fold-t">{titulo}</span>',
                           f'<h2 class="cz-fold-t" id="unidade-pedagogica-{n}">{titulo}</h2>', texto))
        topo = um(secao, r'<header class="grupo-topo">.*?</header>', rel, f'cabeçalho do grupo da unidade {n}')
        etq, h2, pergunta = re.fullmatch(
            r'<header class="grupo-topo">(<p class="grupo-etq">.*?</p>)<h2 id="unidade-pedagogica-%d">(.*?)</h2>'
            r'(<p class="grupo-pergunta">.*?</p>)</header>' % n, topo, re.S).groups()
        if h2 != titulo:
            raise SystemExit(f'{rel}: unidade {n}: o título do grupo ({h2}) não é o da banda ({titulo})')
        prova = um(secao, r'<p class="prova-esperada">.*?</p>', rel, f'prova da unidade {n}')
        saida.append(troca(rel, f'M{rel[1]} unidade {n}: pergunta e prova junto do percurso',
                           topo, f'<div class="cz-unit-body"><header class="grupo-topo">{etq}{pergunta}{prova}</header>',
                           texto))
        fim = prova + '</section></details></section>'
        if not secao.endswith(fim):
            raise SystemExit(f'{rel}: unidade {n}: a prova não fecha a unidade')
        if i + 1 < len(lista):
            # O «novo» tem de ser único: leva a abertura da unidade seguinte, que não muda.
            seguinte = re.match(r'<section\b[^>]*>', lista[i + 1][1]).group(0)
            antigo = fim + texto[texto.index(fim) + len(fim):texto.index(seguinte, texto.index(fim))] + seguinte
            novo = '</section></div></details></section>' + antigo[len(fim):]
            saida.append(troca(rel, f'M{rel[1]} unidade {n}: fecho do corpo da unidade', antigo, novo, texto))
        else:
            saida.append(troca(rel, f'M{rel[1]} unidade {n}: fecho do corpo e imagem documental a seguir às unidades',
                               fim, '</section></div></details></section>' + figura, texto))
    return saida


def oito(n):
    rel = f'm{n}/index.html'
    texto = base(rel)
    t = []
    t.append(troca(rel, f'M{n} estilos comuns dos nove índices', ESTILOS_ANTIGOS, ESTILOS_COMUNS, texto))
    t.append(troca(rel, f'M{n} adesão ao desenho comum', '<main data-cartaz="2" class="cz-index">',
                   f'<main data-cartaz="2" class="cz-index" data-cz-indice="{VERSAO}">', texto))
    abertura = um(texto, r'<div class="module-opening">.*?</header>', rel, 'abertura')
    # No M3, no M5 e no M6 a abertura vinha antes da pergunta e do âmbito (o meio); como no M4, o botão passa para depois
    # deles (sem ligações nem ids pelo meio, a ordem das ligações e dos ids não muda).
    entrada, figura, meio, modsec, comentario = re.fullmatch(
        r'<div class="module-opening">(<div class="module-entry">.*?</div>)(<figure class="doc">.*?</figure>)</div>'
        r'((?:(?!<div class="mod-sec">).)*)(<div class="mod-sec">.*?</details></div>)(<!--.*?-->)</header>', abertura,
        re.S).groups()
    t.append(troca(rel, f'M{n} abertura: recursos no fluxo e imagem fora da abertura', abertura,
                   f'{meio}<div class="module-opening">{entrada}</div>{comentario}</header>'
                   f'<details class="cz-recursos"><summary>Recursos do módulo</summary>{modsec}</details>', texto))
    t += trocas_unidades(rel, texto, figura)
    t.append(troca(rel, f'M{n} teclado dos recursos', '</body>', SCRIPT_NOVO + '</body>', texto))
    return t


def m4():
    rel = 'm4/index.html'
    texto = base(rel)
    t = []
    t.append(troca(rel, 'M4 estilos comuns dos nove índices', '<link rel="stylesheet" href="../assets/cartaz-m4-piloto.css?v=20261102">',
                   ESTILOS_COMUNS, texto))
    t.append(troca(rel, 'M4 adesão ao desenho comum', '<main data-cartaz="2" class="cz-index" data-m4-piloto="20261102">',
                   f'<main data-cartaz="2" class="cz-index" data-cz-indice="{VERSAO}">', texto))
    recursos = um(texto, r'<details class="m4-recursos">.*?<div class="m4-device">.*?</div></details>', rel, 'recursos do piloto')
    modsec, figura, docente, aparelho = re.fullmatch(
        r'<details class="m4-recursos"><summary>Recursos do módulo</summary>(<div class="mod-sec">.*?</details></div>)'
        r'(<figure class="doc">.*?</figure>)(<details class="route-teacher-tools">.*?</details>)'
        r'(<div class="m4-device">.*?</div>)</details>', recursos, re.S).groups()
    modsec_novo = modsec.replace('<nav class="m4-resource-links">', '<nav class="ligas">', 1)
    if modsec_novo == modsec:
        raise SystemExit('m4: sem a navegação dos recursos')
    t.append(troca(rel, 'M4 recursos só com o mapa e a regra; imagem, docente e modo noturno saem', recursos,
                   f'<details class="cz-recursos"><summary>Recursos do módulo</summary>{modsec_novo}</details>', texto))
    t.append(troca(rel, 'M4 o acesso do docente volta a flutuar', COMENTARIO_PILOTO, DOCENTE_FLUTUANTE_M4, texto))
    for n, secao in unidades(rel, texto):
        if secao.count('<div class="m4-unit-body">') != 1:
            raise SystemExit(f'm4: unidade {n} sem o corpo do piloto')
        cabeca = um(secao, r'<div class="m4-unit-body"><header class="grupo-topo"><p class="grupo-etq">.*?</p>', rel,
                    f'corpo da unidade {n}')
        t.append(troca(rel, f'M4 unidade {n}: corpo comum', cabeca, cabeca.replace('m4-unit-body', 'cz-unit-body', 1), texto))
    ultima = unidades(rel, texto)[-1][1]
    # A última linha do percurso (a aula de tarefa da última unidade) é única e ancora a imagem.
    fim_ultima = ultima[ultima.rindex('<li'):]
    t.append(troca(rel, 'M4 imagem documental a seguir às unidades', fim_ultima, fim_ultima + figura, texto))
    t.append(troca(rel, 'M4 teclado dos recursos', '<script src="../assets/cartaz-m4-piloto.js?v=20261102"></script></body>',
                   SCRIPT_NOVO + '</body>', texto))
    # Nada do piloto fica por mudar além do acento do título, que é só do M4.
    return t


def construir():
    """As trocas dos nove índices, pela ordem m1 a m9 (sem escrever nada)."""
    trocas = []
    for n in range(1, 10):
        trocas += m4() if n == 4 else oito(n)
    return trocas


def main():
    trocas = construir()
    CAMADA.write_text(json.dumps(trocas, ensure_ascii=False, indent=1) + '\n', 'utf-8', newline='\n')
    por = {}
    for x in trocas:
        por[x['ficheiro']] = por.get(x['ficheiro'], 0) + 1
    print(f'{len(trocas)} trocas em {len(por)} ficheiros: ' + ', '.join(f'{k} {v}' for k, v in por.items()))


if __name__ == '__main__':
    main()
