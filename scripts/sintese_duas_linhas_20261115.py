#!/usr/bin/env python3
"""15/11/2026: «duas linhas finais» em vez de «síntese integrada» nos índices, nos portefólios, nos mapas e nos guias da tarefa do
M1, do M3, do M5, do M6, do M7 e do M8.

DECISÃO DO DOCENTE (15/11/2026): nos índices e nos portefólios dos módulos M1, M3, M5, M6, M7 e M8, «síntese integrada» e «síntese
simples integrada» passam a «duas linhas finais». O vocabulário muda junto nos mapas do módulo e no guia da tarefa que dizia o mesmo
(só o do M1). O M4 já o fez na camada anterior (tarefa_m4u2_tema_b_20261115: «escreves duas linhas finais» no guia da tarefa e «duas
linhas finais» no índice, no mapa e no portefólio); as frases novas seguem as do M4. O M2 e o M9 não entram na decisão.

O que muda é só a peça da aula de tarefa (as duas linhas escritas no papel do trabalho, no fim da aula). Ficam como estão os outros
usos de «síntese»: as perguntas de escolha das lições (no JSON embutido nos índices), «a síntese oral ou no caderno» do desafio (nos
mapas e nas linhas «pergunta» dos portefólios do M3, do M5 e do M6), as lições, os painéis e as aulas. Também fica a chave interna
«synthesis»: «integrated» do JSON das unidades nos índices, que não é texto que se leia e que tests/test_unit_synthesis.py confere.

Ficheiros (18):
- os índices: m1, m3, m5, m6, m7 e m8 (index.html);
- os portefólios: m1, m3, m5, m6, m7 e m8 (portefolio-do-modulo-mN/);
- os mapas: m1, m3, m5, m6 e m7 (mapa-do-modulo-mN/; o do M8 não fala da síntese);
- o guia da tarefa do M1 (guia-da-tarefa-m1/; os guias do M3, do M5, do M6, do M7 e do M8 não falam da síntese).

Nenhuma destas páginas sai de um gerador nem de dados: são páginas escritas, que só mudam por esta camada literal.

Constrói scripts/sintese_duas_linhas_20261115.json, a camada literal, que se aplica com scripts/aplicar_trocas.py; o manifesto fica em
tests/fixtures/sintese-duas-linhas-edits-20261115.json:

  python3 scripts/sintese_duas_linhas_20261115.py
  python3 scripts/aplicar_trocas.py scripts/sintese_duas_linhas_20261115.json \\
      --manifesto tests/fixtures/sintese-duas-linhas-edits-20261115.json \\
      --base-commit 4f4135bf679176c6c8e4abda543837632aad7325 --nota "…"

Fica na segunda posição da pilha (scripts/verificar_camadas.py), por baixo da fila final (fila_final_20261115, que partilha com ela o portefólio do M8 e a desfaz primeiro), por cima da tarefa m4-u2 com «Tema A ou B»
(tarefa_m4u2_tema_b_20261115), com a qual não partilha ficheiros. Partilha ficheiros com camadas mais antigas (as tarefas mais fáceis
de fazer do M1, do M3, do M5, do M6, do M7 e do M8, a decisão 152, a autonomia 154, o índice da decisão 148, as camadas do cuidado e
as do índice, do mapa, do guia e do portefólio): todas a desfazem primeiro.

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver manifesto,
ou com --base-do-commit, o ficheiro no commit de base, lido com git) e a árvore, com as mesmas funções da camada anterior: pode voltar
a correr depois de a camada estar aplicada e dá o mesmo JSON. Confere cada ficheiro como scripts/aplicar_trocas.py o vai conferir (da
base para o resultado e de volta, letra a letra).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402
from tarefa_m4u2_tema_b_20261115 import trocas_do_texto, _visivel  # noqa: E402

CAMADA = ROOT / 'scripts/sintese_duas_linhas_20261115.json'
MANIFESTO = ROOT / 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'
BASE_COMMIT = '4f4135bf679176c6c8e4abda543837632aad7325'

INDICES = [f'm{m}/index.html' for m in (1, 3, 5, 6, 7, 8)]
PORTEFOLIOS = [f'm{m}/portefolio-do-modulo-m{m}/index.html' for m in (1, 3, 5, 6, 7, 8)]
MAPAS = [f'm{m}/mapa-do-modulo-m{m}/index.html' for m in (1, 3, 5, 6, 7)]
GUIAS = ['m1/guia-da-tarefa-m1/index.html']
FICHEIROS = INDICES + PORTEFOLIOS + MAPAS + GUIAS

ACHADO = ('15/11/2026: Decisão do docente: nos índices e nos portefólios do M1, do M3, do M5, do M6, do M7 e do M8, «síntese '
          'integrada» e «síntese simples integrada» passam a «duas linhas finais», como no M4; o vocabulário muda junto nos mapas e no '
          'guia da tarefa. Só a peça da aula de tarefa: os outros usos de «síntese» ficam.')


def ler(rel):
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 15/11/2026: por cima desta camada fica a fila final (fila_final_20261115), que muda o portefólio do M8 (partilha-o com esta camada):
    # desfaz-se primeiro, com contagem estrita, quando o ficheiro a traz.
    fila_final = ROOT / 'tests/fixtures/fila-final-edits-20261115.json'
    if fila_final.is_file():
        for e in reversed(json.loads(fila_final.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: a fila final já não confere ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
    return texto


DO_COMMIT = False  # com --base-do-commit: a base lê-se do commit de base


def base(rel):
    """O texto do ficheiro sem esta camada: desfeita pelo manifesto (da última troca para a primeira, com contagem estrita); se a
    camada estiver por aplicar nesse ficheiro, o ficheiro já é a base. Antes de haver manifesto (ou com --base-do-commit), o
    ficheiro no commit de base."""
    texto = ler(rel)
    if MANIFESTO.is_file() and not DO_COMMIT:
        edits = json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])
        if edits and all(texto.count(e['new']) == 0 and texto.count(e['old']) == e['occurrences'] for e in edits):
            return texto
        for e in reversed(edits):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: o manifesto desta camada já não confere ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
        return texto
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    if r.returncode:
        raise SystemExit(f'{rel}: sem manifesto e sem o commit de base {BASE_COMMIT[:8]}')
    return r.stdout.decode('utf-8')


def nome(rel):
    m = rel[1]
    if rel.endswith('/index.html') and rel.count('/') == 1:
        return f'Índice do M{m}'
    if 'portefolio' in rel:
        return f'Portefólio do módulo M{m}'
    if 'mapa' in rel:
        return f'Mapa do módulo M{m}'
    return f'Guia da tarefa do M{m}'


def trocas_do_ficheiro(rel, a, b):
    trocas = []
    for antigo, novo in trocas_do_texto(a, b):
        trecho = _visivel(novo)
        trecho = trecho if len(trecho) <= 90 else trecho[:88].rstrip() + '…'
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}: «{trecho}»', 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
                       'achado': ACHADO})
    return trocas


def construir():
    """Devolve (trocas, {ficheiro: (base, final)})."""
    finais = {rel: (base(rel), ler(rel)) for rel in FICHEIROS}
    if all(a == b for a, b in finais.values()):
        raise SystemExit('a camada não está aplicada nesta árvore: aplica-a com scripts/aplicar_trocas.py e o JSON que já existe')
    todas = []
    for rel in FICHEIROS:
        a, b = finais[rel]
        if a == b:
            raise SystemExit(f'{rel}: nada muda')
        for velho in ('síntese integrada', 'síntese simples integrada', 'integra a síntese', 'síntese integra'):
            if velho in b:
                raise SystemExit(f'{rel}: ainda diz «{velho}»')
        trocas = trocas_do_ficheiro(rel, a, b)
        lista = list(enumerate(trocas, 1))
        try:
            for texto in (a, b):
                x, y, _ = processar(rel, lista, texto)
                assert x == a and y == b
        except (TrocaFalhou, AssertionError) as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
        todas += trocas
    return todas, finais


def main():
    global DO_COMMIT
    DO_COMMIT = '--base-do-commit' in sys.argv[1:]
    todas, finais = construir()
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {len(finais)} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
