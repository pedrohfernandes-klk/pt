#!/usr/bin/env python3
"""Opções equilibradas nas escolhas múltiplas nossas das «Provas em cartões» (regra do docente de 29 e 30/10/2026).

Conta só as escolhas que escrevemos: os cartões «escolha» que não são um item da prova (o rótulo «Item n da prova» sem
«adaptado»), os «rever» e cada lacuna dos «completar». As opções oficiais da prova (o tipo «item» e as escolhas com o
rótulo da prova) ficam como estão e não entram. Lê os cartões das páginas geradas
(exame/provas/AAAA-Nf/grupo-x/index.html), como o aluno os recebe.

A medição é a única do sítio, scripts/opcoes_equilibradas.py (30/10/2026; antes, este script tinha uma tolerância de
2 carateres, não contava os empates e dava um limite mais largo): por pergunta, no máximo 20 % entre a opção mais
curta e a mais longa e a certa nunca 25 % ou mais acima da maior errada; por lição (um grupo), a certa a mais longa,
empates incluídos, em não mais de 1 de cada k perguntas (k = opções que o aluno vê; o tipo «escolha» do motor mostra no
máximo três).

As provas feitas antes da regra (prova.json com «opcoes_equilibradas»: false) têm uma catraca: «opcoes_catraca» guarda,
por grupo, as perguntas com falhas e as vezes em que a certa é a mais longa, e nenhum dos dois números pode subir.

Uso: python3 scripts/provas/opcoes.py [-v] [--json] [--exigir] [AAAA-Nf ...]
  -v lista também as perguntas que cumprem;
  --exigir sai com 1 se alguma prova não cumprir: as provas com «opcoes_equilibradas»: true têm de cumprir a regra, as
  outras não podem passar a catraca (sem pastas, todas as provas com dados; com pastas, só essas);
  --catraca escreve os números atuais de cada grupo, no formato de «opcoes_catraca».
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards  # noqa: E402
from opcoes_equilibradas import avaliar, visivel  # noqa: E402,F401  (visivel: para quem importa este módulo)

OFICIAL = re.compile(r'\bItem \d+ da prova\b(?! \(adaptado)')
MOSTRA_ESCOLHA = 3  # jogo.js: o tipo «escolha» mostra a certa e duas erradas
DADOS = Path(__file__).resolve().parent / 'dados'


def perguntas(cartoes):
    """Cada escolha múltipla nossa: número do cartão, g, tipo, opções, índice da certa e k (opções que o aluno vê)."""
    out = []
    for k, c in enumerate(cartoes, 1):
        t = c.get('t')
        if t == 'escolha' and not OFICIAL.search(c.get('rot', '')):
            out.append(dict(cartao=k, g=c.get('g'), tipo=t, opcoes=c['o'], certa=int(c['c']), k=min(len(c['o']), MOSTRA_ESCOLHA)))
        elif t == 'rever':
            out.append(dict(cartao=k, g=c.get('g'), tipo=t, opcoes=c['o'], certa=int(c['c']), k=len(c['o'])))
        elif t == 'completar':
            for j, lac in enumerate(c.get('lacunas', []), 1):
                out.append(dict(cartao=k, g=f'{c.get("g")}[{j}]', tipo='lacuna', opcoes=lac['o'], certa=int(lac['c']), k=len(lac['o'])))
    for p in out:
        p['onde'] = f'cartão {p["cartao"]} ({p["g"]})'
    return out


def medir(cartoes):
    r = avaliar(perguntas(cartoes))
    linhas, falhas = [], []
    for x in r['grupos']:
        motivos = []
        if x['amplitude_acima']:
            motivos.append(f'dispersão {x["amplitude"]:.0%}')
        if x['certa_25_porcento']:
            motivos.append(f'certa {x["vantagem"] - 1:+.0%} sobre a maior errada')
        linha = {'cartao': x['cartao'], 'g': x['g'], 'tipo': x['tipo'], 'k': x['k'], 'comprimentos': x['caracteres'],
                 'dispersao': round(x['amplitude'], 3), 'certa_sobre_maior_errada': round(x['vantagem'], 3),
                 'certa_mais_longa': x['certa_mais_longa'], 'empatada': x['certa_mais_longa'] and not x['certa_sozinha'],
                 'todas_iguais': x['todas_iguais'], 'falhas': motivos}
        linhas.append(linha)
        if motivos:
            falhas.append(linha)
    acima = {k: v for k, v in r['por_k'].items() if v['certa_mais_longa'] > v['limite'] + 1e-9}
    return {'perguntas': len(linhas), 'dispersao_acima': sum(1 for x in linhas if any(f.startswith('dispersão') for f in x['falhas'])),
            'certa_destacada': sum(1 for x in linhas if any(f.startswith('certa') for f in x['falhas'])),
            'certa_mais_longa': r['certas_mais_longas'], 'por_k': r['por_k'], 'mais_longa_acima_do_limite': bool(acima),
            'maior_dispersao': round(r['maior_amplitude'], 3), 'linhas': linhas, 'falhas': falhas}


def cumpre(m):
    return not m['falhas'] and not m['mais_longa_acima_do_limite']


def catraca_de(m):
    """Os números que a catraca guarda para um grupo."""
    return {'falhas': len(m['falhas']), 'certa_mais_longa': m['certa_mais_longa']}


def dentro_da_catraca(m, guardado):
    """[] se nenhum número passou do guardado; senão, o que passou."""
    agora = catraca_de(m)
    return [f'{x}: {agora[x]} (catraca {guardado[x]})' for x in ('falhas', 'certa_mais_longa') if agora[x] > guardado[x]]


def parametros(pasta):
    p = DADOS / pasta / 'prova.json'
    return json.loads(p.read_text('utf-8')) if p.is_file() else {}


def paginas(pastas=None):
    for p in sorted((ROOT / 'exame/provas').glob('*/grupo-*/index.html')):
        if not pastas or p.parent.parent.name in pastas:
            yield p.parent.parent.name, p.parent.name, p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('-v', action='store_true', help='lista todas as perguntas')
    ap.add_argument('--exigir', action='store_true', help='sai com 1 se alguma prova falhar a regra ou passar a catraca')
    ap.add_argument('--json', action='store_true', help='escreve os números em JSON')
    ap.add_argument('--catraca', action='store_true', help='escreve os números atuais no formato de «opcoes_catraca»')
    ap.add_argument('pastas', nargs='*')
    a = ap.parse_args(argv)
    todas, catracas, ok = {}, {}, True
    for pasta, slug, p in paginas(a.pastas):
        cfg = parametros(pasta)
        m = medir(lesson_cards(p))
        todas[f'{pasta}/{slug}'] = {k: v for k, v in m.items() if k != 'linhas'}
        catracas.setdefault(pasta, {})[slug] = catraca_de(m)
        if cfg.get('opcoes_equilibradas', True) is False:
            guardado = cfg.get('opcoes_catraca', {}).get(slug)
            passou = dentro_da_catraca(m, guardado) if guardado else ['sem catraca em prova.json']
            estado = 'feita antes da regra; catraca ' + ('cumprida' if not passou else 'passada: ' + '; '.join(passou))
            ok &= not passou
        else:
            estado = 'cumpre' if cumpre(m) else 'não cumpre'
            ok &= cumpre(m)
        if a.json or a.catraca:
            continue
        por_k = '; '.join(f'{v["certa_mais_longa"]} de {v["perguntas"]} com {k} opções (limite {v["limite"]:.2f})' for k, v in m['por_k'].items())
        print(f'{pasta} {slug}: {m["perguntas"]} escolhas nossas; dispersão acima de 20 %: {m["dispersao_acima"]}; '
              f'certa 25 % ou mais acima da maior errada: {m["certa_destacada"]}; certa a mais longa, empates incluídos: '
              f'{por_k or "nenhuma pergunta"}; maior dispersão {m["maior_dispersao"]:.0%}  [{estado}]')
        for x in (m['linhas'] if a.v else m['falhas']):
            marca = '  (a mais longa)' if x['certa_mais_longa'] and not x['empatada'] else (
                '  (todas iguais)' if x['todas_iguais'] else ('  (empatada na mais longa)' if x['empatada'] else ''))
            print(f'   cartão {x["cartao"]:>3} {x["g"]:<8} {x["tipo"]:<8} {x["comprimentos"]} '
                  + (f'  {"; ".join(x["falhas"])}' if x['falhas'] else '') + marca)
    if a.json:
        print(json.dumps(todas, ensure_ascii=False, indent=1))
    if a.catraca:
        print(json.dumps(catracas, ensure_ascii=False, indent=1))
    return 1 if a.exigir and not ok else 0


if __name__ == '__main__':
    sys.exit(main())
