#!/usr/bin/env python3
"""07/11/2026: três acertos dos índices do Português que a decisão 173 deixou para um pedido próprio (decisão 48).

Constrói scripts/indices_acertos_20261107.json, a camada literal que muda os nove índices (m1/ a m9/index.html) por cima do
desenho comum (camada cartaz_indices_148_20261106). Aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/indices-acertos-edits-20261107.json:

  python3 scripts/indices_acertos_20261107.py
  python3 scripts/aplicar_trocas.py scripts/indices_acertos_20261107.json --manifesto tests/fixtures/indices-acertos-edits-20261107.json --base-commit 93907af1fb2481cb537df27ad6a777d0a87c3f8a --nota "…"

As trocas calculam-se sobre a base (o texto de cada página com esta camada desfeita, pelo manifesto, quando ele já existe):
o script pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON. Desfeita, a camada devolve os nove índices
do main 93907af1 letra a letra.

1. Acesso do docente repetido (M3, M5 e M6): sai a ligação a.teacher-access («Guiões e materiais do docente»), que ficava por
   baixo do botão dos materiais e recebia o foco sem se ver. O destino (lente/docente/#portugues) continua no menu dos
   materiais do docente da mesma página, em «Guiões do docente» (o script confere que lá está antes de tirar a ligação).
2. «·» nas contagens de «Neste módulo» (M8 e M9): « · » passa a «, » nas quatro legendas <small>, como nos outros sete índices
   (regra da casa: nunca «·» dentro de frases).
3. Menu dos materiais do docente sem JavaScript, abaixo de 640 px: o lugar flutuante (position:fixed;left:12px;bottom:64px)
   sai do style do HTML e passa para assets/cartaz-indice-comum.css, que o mantém igual com JavaScript e a partir de 640 px e,
   sem JavaScript abaixo de 640 px, abre o menu no fluxo, por baixo do botão. Nenhuma regra de CSS ganha a um
   style escrito no HTML sem !important (que o teste da camada proíbe), por isso a mudança é aqui. A versão do CSS comum
   passa a 20261107 nos nove, para a página nova não se juntar ao CSS antigo guardado no navegador.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/indices_acertos_20261107.json'
MANIFESTO = ROOT / 'tests/fixtures/indices-acertos-edits-20261107.json'
# 12/11/2026: por cima fica a decisão 152 no M8 (os espaços que não quebram no índice do M8), que se desfaz antes.
CUIDADO_M8 = ROOT / 'tests/fixtures/cuidado-m8-edits-20261112.json'
# 12/11/2026: por cima fica também a decisão 152 no M9 (os espaços que não quebram no índice do M9), que se desfaz antes.
CUIDADO_M9 = ROOT / 'tests/fixtures/cuidado-m9-edits-20261112.json'
# 12/11/2026: por cima fica a decisão 152 no Exame e nas páginas transversais (os espaços que não quebram na entrada do Português e
# nas páginas dos anos), que se desfaz antes de todas.
CUIDADO_EXAME = ROOT / 'tests/fixtures/cuidado-exame-edits-20261112.json'
ACHADO = ('07/11/2026: três acertos dos índices deixados pela decisão 173 (acesso do docente repetido no M3, no M5 e no M6, '
          '«·» nas contagens do M8 e do M9, menu dos materiais sem JavaScript no telemóvel). {o}')
GUIOES = 'https://pedrohfernandes-klk.github.io/lente/docente/#portugues'
ESTILOS_148 = '<link rel="stylesheet" href="../assets/cartaz-indice-comum.css?v=20261106">'
ESTILOS_NOVOS = '<link rel="stylesheet" href="../assets/cartaz-indice-comum.css?v=20261107">'
MENU_FLUTUANTE = '<nav aria-label="Materiais do docente" style="position:fixed;left:12px;bottom:64px;z-index:1001;'
MENU_SEM_LUGAR = '<nav aria-label="Materiais do docente" style="z-index:1001;'
REPETIDO = (3, 5, 6)
PONTO_MEDIO = (8, 9)


def base(rel):
    """O texto da página sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 12/11/2026: antes de tudo, a decisão 152 no Exame e nas páginas transversais (camada cuidado_exame_20261112), a mais recente,
    # com contagem estrita.
    if CUIDADO_EXAME.is_file():
        for edit in reversed(json.loads(CUIDADO_EXAME.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a decisão 152 no Exame e nas páginas transversais já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    # 12/11/2026: antes de tudo, a decisão 152 no M9 (camada cuidado_m9_20261112), a mais recente, com contagem estrita: prende
    # «90 min» nas contagens do índice do M9, dentro do texto que este acerto mudou («, » em vez de « · »).
    if CUIDADO_M9.is_file():
        for edit in reversed(json.loads(CUIDADO_M9.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a decisão 152 no M9 já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    # 12/11/2026: a seguir, a decisão 152 no M8 (camada cuidado_m8_20261112), com contagem estrita: prende
    # «90 min» nas contagens do índice do M8, dentro do texto que este acerto mudou («, » em vez de « · »).
    if CUIDADO_M8.is_file():
        for edit in reversed(json.loads(CUIDADO_M8.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a decisão 152 no M8 já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    if MANIFESTO.is_file():
        for edit in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    return texto


def troca(rel, local, antigo, novo, texto):
    if texto.count(antigo) != 1:
        raise SystemExit(f'{rel}: «{local}» aparece {texto.count(antigo)} vezes')
    if novo in antigo or texto.count(novo):
        # O «novo» não pode estar já na página nem dentro do «antigo»: aplicar_trocas.py tomá-lo-ia por troca já aplicada.
        raise SystemExit(f'{rel}: «{local}»: o novo já está na página ou dentro do antigo')
    return {'ficheiro': rel, 'local': local, 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
            'achado': ACHADO.format(o=local + '.')}


def indice(n):
    rel = f'm{n}/index.html'
    texto = base(rel)
    t = [troca(rel, f'M{n} CSS comum na versão dos acertos', ESTILOS_148, ESTILOS_NOVOS, texto)]
    if n in PONTO_MEDIO:
        lista = re.search(r'<nav aria-label="Unidades do módulo" class="unit-index">.*?</nav>', texto, re.S).group(0)
        legendas = re.findall(r'<small>[^<]*</small>', lista)
        com_ponto = [x for x in legendas if '·' in x]
        if len(legendas) != 2 or com_ponto != legendas:
            raise SystemExit(f'{rel}: esperava duas legendas com «·» em «Neste módulo»: {legendas}')
        for k, legenda in enumerate(legendas, 1):
            if legenda.count(' · ') != 1:
                raise SystemExit(f'{rel}: a legenda {k} não tem um só « · »: {legenda}')
            t.append(troca(rel, f'M{n} «Neste módulo», unidade {k}: «, » em vez de « · »', legenda,
                           legenda.replace(' · ', ', '), texto))
    if n in REPETIDO:
        ligacao = re.findall(r'</script>(<a class="teacher-access" href="[^"]*" aria-label="Guiões e materiais do docente" '
                             r'title="Para o docente"><svg [^>]*>.*?</svg></a>)<details class="route-teacher-tools">', texto, re.S)
        if len(ligacao) != 1 or f'href="{GUIOES}"' not in ligacao[0]:
            raise SystemExit(f'{rel}: esperava uma ligação repetida aos guiões antes do menu dos materiais')
        menu = re.findall(r'<details class="route-teacher-tools">.*?<nav aria-label="Materiais do docente"[^>]*>(.*?)</nav>',
                          texto, re.S)
        if len(menu) != 1 or f'<a href="{GUIOES}">Guiões do docente</a>' not in menu[0]:
            raise SystemExit(f'{rel}: o menu dos materiais não tem os guiões; a ligação não pode sair')
        # O «novo» leva o fim do script anterior e o início do menu, que não mudam (para apagar, ancora-se nos vizinhos).
        t.append(troca(rel, f'M{n} sai a ligação repetida aos guiões (o destino fica no menu dos materiais)',
                       '</script>' + ligacao[0] + '<details class="route-teacher-tools">',
                       '</script><details class="route-teacher-tools">', texto))
    t.append(troca(rel, f'M{n} menu dos materiais sem o lugar flutuante no HTML (passa para o CSS comum)',
                   MENU_FLUTUANTE, MENU_SEM_LUGAR, texto))
    return t


def construir():
    """As trocas dos nove índices, pela ordem m1 a m9 (sem escrever nada)."""
    trocas = []
    for n in range(1, 10):
        trocas += indice(n)
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
