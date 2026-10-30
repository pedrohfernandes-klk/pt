#!/usr/bin/env python3
"""Mede as opções novas do M1, incluindo lacunas, sem alterar os dados.

Amplitude conservadora: (maior - menor) / menor. Empates contam como
«certa mais longa». V/F usa os rótulos fixos do motor, não opções redigidas.
Uso: python scripts/auditar_aquecimentos_m1.py
"""
from collections import Counter
from html import unescape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def visivel(texto):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', '', texto)).replace('**', '')).strip()


def auditar(d):
    grupos = []
    for numero, cartao in enumerate(d['cartoes'], 1):
        for q in ([cartao] if cartao.get('t') in ('escolha', 'rever') else cartao.get('lacunas', [])):
            textos = [visivel(x) for x in q['o']]
            medidas = [len(x) for x in textos]
            correta = medidas[q['c']]
            errada = max(x for i, x in enumerate(medidas) if i != q['c'])
            grupos.append(dict(cartao=numero, k=len(medidas), caracteres=medidas,
                               amplitude=(max(medidas)-min(medidas))/min(medidas),
                               certa_mais_longa=correta == max(medidas),
                               certa_25_porcento=correta >= errada * 1.25))
    totais = Counter(g['k'] for g in grupos)
    longas = Counter(g['k'] for g in grupos if g['certa_mais_longa'])
    erros = [f"cartão {g['cartao']}: amplitude ou vantagem acima do limite"
             for g in grupos if g['amplitude'] > .20 or g['certa_25_porcento']]
    for k, n in totais.items():
        if longas[k] > n / k:
            erros.append(f'{longas[k]}/{n} certas mais longas nas perguntas com {k} opções')
    return dict(slug=d['slug'],grupos=grupos,maior_amplitude=max(g['amplitude'] for g in grupos),
                certas_mais_longas=sum(longas.values()),grupos_de_opcoes=len(grupos),erros=erros)


def main():
    resultados=[auditar(json.loads((ROOT / 'docs/pedagogia/aquecimentos' / f'm1-u{n}.json').read_text('utf-8'))) for n in (1,2)]
    print(json.dumps(resultados,ensure_ascii=False,indent=2))
    raise SystemExit(1 if any(r['erros'] for r in resultados) else 0)


if __name__ == '__main__':
    main()
