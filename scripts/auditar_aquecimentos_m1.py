#!/usr/bin/env python3
"""Mede as opções novas do M1, incluindo lacunas, sem alterar os dados.

Amplitude conservadora: (maior - menor) / menor. Empates contam como
«certa mais longa». V/F usa os rótulos fixos do motor, não opções redigidas.
30/10/2026: a medição passou para scripts/opcoes_equilibradas.py, a medição única do sítio (também usada pelas
Provas em cartões, scripts/provas/opcoes.py); este script escolhe as perguntas e devolve o mesmo que antes.
Uso: python scripts/auditar_aquecimentos_m1.py
"""
from pathlib import Path
import json

from opcoes_equilibradas import avaliar

ROOT = Path(__file__).resolve().parents[1]


def auditar(d):
    perguntas = []
    for numero, cartao in enumerate(d['cartoes'], 1):
        for q in ([cartao] if cartao.get('t') in ('escolha', 'rever') else cartao.get('lacunas', [])):
            perguntas.append(dict(opcoes=q['o'], certa=q['c'], cartao=numero, onde=f'cartão {numero}'))
    r = avaliar(perguntas)
    grupos = [dict(cartao=g['cartao'], k=g['k'], caracteres=g['caracteres'], amplitude=g['amplitude'],
                   certa_mais_longa=g['certa_mais_longa'], certa_25_porcento=g['certa_25_porcento']) for g in r['grupos']]
    return dict(slug=d['slug'], grupos=grupos, maior_amplitude=r['maior_amplitude'],
                certas_mais_longas=r['certas_mais_longas'], grupos_de_opcoes=r['grupos_de_opcoes'], erros=r['erros'])


def main():
    resultados=[auditar(json.loads((ROOT / 'docs/pedagogia/aquecimentos' / f'm1-u{n}.json').read_text('utf-8'))) for n in (1,2)]
    print(json.dumps(resultados,ensure_ascii=False,indent=2))
    raise SystemExit(1 if any(r['erros'] for r in resultados) else 0)


if __name__ == '__main__':
    main()
