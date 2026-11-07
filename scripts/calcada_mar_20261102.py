#!/usr/bin/env python3
"""02/11/2026: decisão 139 (docente: «maiores e mais bem feitos; a calçada tem de parecer realmente calçada»).

Constrói scripts/calcada_mar_20261102.json, a camada literal da entrada do Português: sai o desenho a traço (pedras soltas em
SVG dentro do cabeçalho e a folha da entrada) e entra, por baixo do nome, a faixa da calçada «mar largo» (assets/calcada-mar.svg,
gerada por scripts/gerar_calcada_mar.py), com o mesmo motor comum (data-fundo="cf") e o mesmo botão «Parar o desenho».
A camada aplica-se com scripts/aplicar_trocas.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACHADO = 'Pedido do docente de 02/11/2026: o desenho da entrada maior e mais bem feito; a calçada tem de parecer calçada.'


def main():
    texto = (ROOT / 'index.html').read_text('utf-8')
    inicio = '<header class="p-cab" data-fundo="cf" data-fundo-ciclo="16"><div class="cf-fundo" aria-hidden="true">'
    fim = '<div class="cf-papel" aria-hidden="true"></div>'
    i = texto.index(inicio)
    j = texto.index(fim, i) + len(fim)
    trocas = [
        (texto[i:j], '<header class="p-cab" data-fundo="cf" data-fundo-ciclo="40">'),
        ('<p class="pt-entry-lead">Ler com atenção. Relacionar ideias. Experimentar outras vozes.</p></header>',
         '<p class="pt-entry-lead">Ler com atenção. Relacionar ideias. Experimentar outras vozes.</p><div class="cf-mar" aria-hidden="true">'
         '<div class="cf-pedras"></div></div></header>'),
        ('<p class="cf-credito">Desenho nosso, a traço, EPI, 2026, a partir do padrão de ondas da calçada portuguesa',
         '<p class="cf-credito">Desenho nosso, pedra a pedra, EPI, 2026, a partir do padrão de ondas da calçada portuguesa'),
        ('assets/fundo-calcada.css?v=20261102-2"', 'assets/fundo-calcada.css?v=20261102-3"'),
    ]
    saida = []
    for n, (antigo, novo) in enumerate(trocas, 1):
        k = texto.count(antigo)
        assert k == 1, (n, k)
        texto = texto.replace(antigo, novo)
        assert texto.count(novo) == 1, n
        saida.append({'ficheiro': 'index.html', 'local': f'Calçada «mar largo», troca {n}', 'antigo': antigo, 'novo': novo,
                      'ocorrencias': 1, 'achado': ACHADO})
    destino = ROOT / 'scripts/calcada_mar_20261102.json'
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + '\n', 'utf-8', newline='\n')
    print(len(saida), 'trocas')


if __name__ == '__main__':
    main()
