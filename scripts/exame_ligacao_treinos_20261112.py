#!/usr/bin/env python3
"""12/11/2026: a ligação «Treinos» na navegação da página principal do Exame (exame/index.html).

Constrói scripts/exame_ligacao_treinos_20261112.json, a camada literal exame_ligacao_treinos_20261112, com uma só troca: a
navegação do cabeçalho de exame/index.html ganha a ligação «Treinos» (para exame/treinos/), logo a seguir a «Provas em cartões»,
com o mesmo rótulo e na mesma ordem dos cabeçalhos de exame/provas/index.html e de exame/laboratorio/index.html, onde a ligação já
estava (os treinos são de 11/11/2026, scripts/exame_treinos.py). A página principal do Exame é uma página congelada, registada em
camadas literais (exame_licao_20261105 e exame_contexto_20261105): só muda por camada. A camada aplica-se com
scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/exame-ligacao-treinos-edits-20261112.json:

  python3 scripts/exame_ligacao_treinos_20261112.py
  python3 scripts/aplicar_trocas.py scripts/exame_ligacao_treinos_20261112.json \\
      --manifesto tests/fixtures/exame-ligacao-treinos-edits-20261112.json \\
      --base-commit 927bab632a0aefb1d3cb090d655a0f4356e3f9f8 --nota "…"

Fica por cima da decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112, no main 927bab63, #198), com a qual não
partilha nenhum ficheiro.

- Só a ligação: a navegação está escrita em exame/index.html (assets/exame/app.js monta as vistas dentro de <main id="app"> e
  não toca no cabeçalho), por isso app.js não muda, nem a sua versão de cache (que tests/test_exame_licao.py fixa), nem nenhum
  outro texto. A ligação nova não leva classe nem atributos: fica com o aspeto das outras ligações da mesma navegação.
- A troca ancora-se no fim de «Provas em cartões» e no início de «Programa e fontes», para o texto antigo não caber dentro do
  novo (scripts/aplicar_trocas.py reconhece assim a troca já aplicada) e para o novo se desfazer letra a letra.
- As páginas exame/treinos/ e os geradores (scripts/exame_treinos.py, scripts/provas/gerar.py, scripts/exame_aquecimentos.py) não
  mudam.

O script calcula a troca sobre a base (o ficheiro com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar a
correr depois de a camada estar aplicada e dá o mesmo JSON.

As camadas de baixo desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]), tests/auditoria_20261028.py e
scripts/desligar_sala.py. As duas camadas de baixo que mexem em exame/index.html (exame_licao_20261105 e exame_contexto_20261105)
não têm gerador (só o JSON), e os geradores que desfazem a decisão 152 no Exame (o desenho comum dos índices, os acertos dos
índices e os créditos atrás de um «i») não leem exame/index.html: não há gerador a mudar.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/exame_ligacao_treinos_20261112.json'
MANIFESTO = ROOT / 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
PAGINA = 'exame/index.html'
# As páginas que já tinham a ligação no cabeçalho, de onde vêm o rótulo e a ordem (a seguir a «Provas em cartões»).
MODELOS = ('exame/provas/index.html', 'exame/laboratorio/index.html')
ROTULO = 'Treinos'
LIGACAO = f'<a href="treinos/">{ROTULO}</a>'
ANTES, DEPOIS = 'Provas em cartões</a>', '<a href="#cobertura">'
ANTIGO = ANTES + DEPOIS
NOVO = ANTES + LIGACAO + DEPOIS
LOCAL = ('Página principal do Exame (exame/index.html), navegação do cabeçalho («Navegação da preparação»): a ligação «Treinos», '
         'entre «Provas em cartões» e «Programa e fontes»')
ACHADO = ('12/11/2026: os treinos do Exame (exame/treinos/, de 11/11/2026) já estavam ligados nos cabeçalhos das provas em cartões e '
          'do laboratório; faltava a ligação na página principal do Exame, que é uma página congelada e só muda por camada literal. '
          'Entra a ligação «Treinos», com o mesmo rótulo e na mesma ordem (a seguir a «Provas em cartões»); nenhum outro texto muda.')


def base(rel):
    """O texto do ficheiro sem esta camada (desfeita pelo manifesto, da última troca para a primeira, com contagem estrita). Se a
    camada estiver por aplicar (o novo não está lá e o antigo está, as vezes que o manifesto diz), o ficheiro já é a base."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if MANIFESTO.is_file():
        for e in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) == 0 and texto.count(e['old']) == e['occurrences']:
                continue
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: o manifesto desta camada já não confere ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
    return texto


def construir():
    """Devolve (trocas, base, depois). Confere o rótulo e a ordem com os cabeçalhos que já têm a ligação, e a troca como o
    aplicar_trocas.py a vai conferir: a partir da base, e com tudo já aplicado."""
    for rel in MODELOS:
        modelo = (ROOT / rel).read_bytes().decode('utf-8')
        if modelo.count(f'Provas em cartões</a><a href="../treinos/">{ROTULO}</a>') != 1:
            raise SystemExit(f'{rel}: o cabeçalho já não tem a ligação «{ROTULO}» a seguir a «Provas em cartões»')
    if not (ROOT / 'exame/treinos/index.html').is_file():
        raise SystemExit('exame/treinos/index.html não existe')
    base_txt = base(PAGINA)
    if base_txt.count(ANTIGO) != 1 or 'treinos' in base_txt:
        raise SystemExit(f'{PAGINA}: a base não é a esperada')
    final = base_txt.replace(ANTIGO, NOVO)
    trocas = [{'ficheiro': PAGINA, 'local': LOCAL, 'antigo': ANTIGO, 'novo': NOVO, 'ocorrencias': 1, 'achado': ACHADO}]
    lista = list(enumerate(trocas, 1))
    try:
        for texto in (base_txt, final):
            b, depois, _ = processar(PAGINA, lista, texto)
            assert b == base_txt and depois == final
    except (TrocaFalhou, AssertionError) as erro:
        raise SystemExit(f'{PAGINA}: a troca não confere: {erro}')
    return trocas, base_txt, final


def main():
    trocas, _, _ = construir()
    CAMADA.write_text(json.dumps(trocas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(trocas)} troca em 1 ficheiro: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
