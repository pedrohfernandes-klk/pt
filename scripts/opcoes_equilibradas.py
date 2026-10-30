#!/usr/bin/env python3
"""Opções equilibradas: a medição única do sítio (regra do docente de 29 e 30/10/2026).

Regra: em todas as escolhas múltiplas que escrevemos, as opções têm comprimento o mais semelhante possível.
* Por pergunta: entre a opção mais curta e a mais longa, no máximo 20 % de diferença em carateres visíveis, contada
  sobre a mais curta (amplitude = (maior - menor) / menor); a certa nunca 25 % ou mais acima da maior errada.
* Por conjunto (uma lição, um baralho): a certa não é a mais longa em mais de 1 de cada k perguntas, para cada número
  de opções k (as perguntas com k opções: no máximo n/k com a certa a mais longa).
Empates contam: uma certa empatada com a mais longa conta como «certa mais longa», também quando as opções têm todas o
mesmo tamanho (decisão de #134, conferida em tests/test_aquecimentos_m1_opcoes.py). Sem tolerância para as opções
curtas: a regra diz 20 %, sem exceções.

Antes de 30/10/2026 havia duas medições da mesma regra: a de scripts/auditar_aquecimentos_m1.py (#134 e #135) e a de
scripts/provas/opcoes.py (Provas em cartões), que deixava passar diferenças de 2 carateres, não contava os empates e
dava um limite por lição mais largo. A revisão técnica da 2026-2f pediu uma só; ficou esta, a mais estrita, que é a que
já estava em main. Os dois scripts escolhem as perguntas (o que é nosso) e medem-nas aqui.
"""
from collections import Counter
from html import unescape
import re

MAX_AMPLITUDE = 0.20
MAX_VANTAGEM = 1.25  # a certa < 1,25 × a maior errada
EPS = 1e-9


def visivel(texto):
    """Os carateres que o aluno vê: sem etiquetas HTML nem as marcas dos dados (**negrito**, _itálico_, [^n]), com os
    espaços seguidos contados como um. O motor das lições (jogo.js, it()) mostra **x** e _x_ sem as marcas."""
    s = unescape(re.sub(r'<[^>]*>', '', str(texto)))
    s = re.sub(r'\[\^\d+\]', '', s).replace('**', '')
    s = re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def medir(opcoes, certa, k=None):
    """Os números de uma pergunta: comprimentos, amplitude, vantagem da certa e se é a mais longa (com empates)."""
    medidas = [len(visivel(o)) for o in opcoes]
    correta = medidas[certa]
    erradas = [x for i, x in enumerate(medidas) if i != certa]
    errada = max(erradas)
    menor = min(medidas)
    amplitude = (max(medidas) - menor) / menor if menor else float('inf')
    return dict(k=k or len(medidas), caracteres=medidas, amplitude=amplitude,
                vantagem=correta / errada if errada else float('inf'),
                certa_mais_longa=correta == max(medidas), certa_sozinha=correta > errada,
                todas_iguais=len(set(medidas)) == 1, certa_25_porcento=correta >= errada * MAX_VANTAGEM - EPS,
                amplitude_acima=amplitude > MAX_AMPLITUDE + EPS)


def avaliar(perguntas):
    """perguntas: dicionários com «opcoes», «certa» e, opcionalmente, «k» (opções que o aluno vê) e «onde» (para as
    mensagens). Devolve as medidas de cada pergunta, a contagem por k e os erros da regra."""
    grupos = []
    for p in perguntas:
        m = medir(p['opcoes'], p['certa'], p.get('k'))
        m.update({x: y for x, y in p.items() if x not in ('opcoes', 'certa', 'k')})
        grupos.append(m)
    totais = Counter(g['k'] for g in grupos)
    longas = Counter(g['k'] for g in grupos if g['certa_mais_longa'])
    erros = [f"{g.get('onde', 'pergunta')}: amplitude ou vantagem acima do limite"
             for g in grupos if g['amplitude_acima'] or g['certa_25_porcento']]
    por_k = {}
    for k, n in sorted(totais.items()):
        por_k[k] = dict(perguntas=n, certa_mais_longa=longas[k], limite=n / k)
        if longas[k] > n / k + EPS:
            erros.append(f'{longas[k]}/{n} certas mais longas nas perguntas com {k} opções')
    return dict(grupos=grupos, por_k=por_k, erros=erros,
                maior_amplitude=max((g['amplitude'] for g in grupos), default=0.0),
                certas_mais_longas=sum(longas.values()), grupos_de_opcoes=len(grupos))
