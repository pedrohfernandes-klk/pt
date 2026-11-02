#!/usr/bin/env python3
"""02/11/2026: desenho da calçada «mar largo» (Rossio, Lisboa) para a entrada do Português.

Gera assets/calcada-mar.svg: um ladrilho que se repete na horizontal sem costura. As ondas são faixas largas, alternadamente de
basalto (pedra escura) e de calcário (pedra clara), entre curvas paralelas. Cada faixa é assente em fiadas que seguem a onda;
cada pedra é um quadrilátero irregular, com as arestas gastas e a junta de argamassa à vista. Tudo é determinístico (semente
fixa), para que o ficheiro se possa regenerar e conferir: python3 scripts/gerar_calcada_mar.py --verificar.
"""
import argparse
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / 'assets/calcada-mar.svg'

LARGURA = 960          # um ladrilho: dois comprimentos de onda
ALTURA = 440
PERIODO = 480
AMPLITUDE = 44
FAIXA = 72             # espessura (na vertical) de cada faixa, escura ou clara
FIADA = 12             # altura de uma fiada de pedras
PEDRA = 15             # comprimento médio de uma pedra
JUNTA = 0.9            # meia junta: o quadrilátero encolhe para o centro
TREMOR = 1.15          # irregularidade dos cantos
ARGAMASSA = '#9c958a'
ESCURAS = ['#1f1e1c', '#262523', '#2c2a27', '#33312d', '#3b3934', '#2a2926']
CLARAS = ['#f3f0e9', '#ece8df', '#e6e1d6', '#f7f5f0', '#e1dccf', '#efebe3']


def onda(x, base):
    return base + AMPLITUDE * math.sin(2 * math.pi * x / PERIODO)


def pedras():
    rnd = random.Random(1923)
    por_fiada = round(LARGURA / PEDRA)          # o mesmo número em todas as fiadas: o ladrilho fecha sem costura
    passo = LARGURA / por_fiada
    # as curvas começam acima do ladrilho e acabam abaixo, para a faixa cobrir toda a altura com a amplitude da onda
    topo = -AMPLITUDE - FAIXA
    fiadas = []
    y = topo
    while y < ALTURA + AMPLITUDE + FIADA:
        fiadas.append(y)
        y += FIADA
    # cada canto (fiada, posição) tem um deslocamento próprio, igual de um lado e do outro do ladrilho
    desloc = {}
    for j in range(len(fiadas)):
        for i in range(por_fiada):
            desloc[j, i] = (rnd.uniform(-0.28, 0.28) * passo, rnd.uniform(-TREMOR, TREMOR))
    saida = {'e': {}, 'c': {}}
    for j in range(len(fiadas) - 1):
        faixa = math.floor((fiadas[j] - topo) / FAIXA)
        tipo = 'e' if faixa % 2 == 0 else 'c'
        meio = 0.5 * passo if j % 2 else 0.0      # aparelho desencontrado, como na calçada
        for i in range(por_fiada):
            def canto(jj, ii):
                dx, dy = desloc[jj, ii % por_fiada]
                x = meio + ii * passo + dx
                return x, onda(x, fiadas[jj]) + dy
            a = canto(j, i)
            b = canto(j, i + 1)
            c = canto(j + 1, i + 1)
            d = canto(j + 1, i)
            # encolher para o centro: a junta de argamassa
            cx = (a[0] + b[0] + c[0] + d[0]) / 4
            cy = (a[1] + b[1] + c[1] + d[1]) / 4
            pts = []
            for px, py in (a, b, c, d):
                vx, vy = px - cx, py - cy
                n = math.hypot(vx, vy) or 1
                k = max(0.0, 1 - (JUNTA * 2.1) / n)
                pts.append((cx + vx * k, cy + vy * k))
            if max(p[1] for p in pts) < -2 or min(p[1] for p in pts) > ALTURA + 2:
                continue
            tom = rnd.randrange(len(ESCURAS if tipo == 'e' else CLARAS))
            saida[tipo].setdefault(tom, []).append(pts)
            # a pedra que sai pela direita entra pela esquerda (e vice-versa): o ladrilho repete-se sem costura
            if max(p[0] for p in pts) > LARGURA:
                saida[tipo][tom].append([(px - LARGURA, py) for px, py in pts])
            if min(p[0] for p in pts) < 0:
                saida[tipo][tom].append([(px + LARGURA, py) for px, py in pts])
    return saida


def caminho(lista):
    partes = []
    for pts in lista:
        (x0, y0), *resto = [(round(x, 1), round(y, 1)) for x, y in pts]
        seg = f'M{x0:g} {y0:g}'
        px, py = x0, y0
        for x, y in resto:
            seg += f'l{round(x - px, 1):g} {round(y - py, 1):g}'
            px, py = x, y
        partes.append(seg + 'z')
    return ''.join(partes)


def svg():
    dados = pedras()
    linhas = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}" width="{LARGURA}" height="{ALTURA}" '
              f'preserveAspectRatio="none">',
              '<!-- Desenho nosso, EPI, 2026: calçada portuguesa, padrão de ondas «mar largo» (Rossio, Lisboa). '
              'Gerado por scripts/gerar_calcada_mar.py. -->',
              f'<rect width="{LARGURA}" height="{ALTURA}" fill="{ARGAMASSA}"/>',
              '<g stroke-linejoin="round" stroke-width="1.5">']
    for tipo, cores in (('c', CLARAS), ('e', ESCURAS)):
        for tom, lista in sorted(dados[tipo].items()):
            cor = cores[tom]
            linhas.append(f'<path fill="{cor}" stroke="{cor}" d="{caminho(lista)}"/>')
    linhas.append('</g></svg>')
    return '\n'.join(linhas) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verificar', action='store_true')
    args = parser.parse_args()
    texto = svg()
    if args.verificar:
        assert DESTINO.read_text('utf-8') == texto, 'assets/calcada-mar.svg não corresponde ao gerador'
        print('Conferido:', DESTINO.relative_to(ROOT))
    else:
        DESTINO.write_text(texto, 'utf-8', newline='\n')
        print('Gerado:', DESTINO.relative_to(ROOT), len(texto.encode()), 'bytes')


if __name__ == '__main__':
    main()
