#!/usr/bin/env python3
"""Mede o comprimento das opções de todas as escolhas múltiplas do sítio (30/10/2026).

Pedido do docente (29/10/2026): «Ainda há demasiadas escolhas múltiplas em que a resposta certa é claramente a de maior
dimensão. Não pode ser.» A certa não pode ser «quase de certeza» a mais comprida; o ideal é as opções serem o mais
semelhantes possível em dimensão.

Caracteres visíveis: sem etiquetas HTML, sem _ nem * (marcas de itálico e negrito), espaços normalizados.
* denunciadora: a certa (a mais longa das certas) tem pelo menos 1,25 × a maior errada E pelo menos 5 caracteres a mais
  (entre palavras soltas, 2 ou 3 letras a mais não denunciam a resposta: «ortónimo / heterónimo / fingidor»);
* amplitude: mais longa / mais curta; «fora dos 20 %» quando passa de 1,20 com pelo menos 8 caracteres de diferença;
* certa_mais_longa: a certa é estritamente a mais longa.
Ficam de fora as opções oficiais das provas do IAVE (cartões de tipo «item» nas provas em cartões).

Este script procura as perguntas em toda a árvore publicada (lições, painéis, arquivos dos índices, recursos, guiões),
qualquer que seja o formato dos dados ({"o": [...], "c": n}, "opcoes" em pares ou em objetos). Os limiares 1,25 e 1,20 são
os de scripts/opcoes_equilibradas.py, a medição única das páginas feitas já com a regra inteira (provas em cartões e
aquecimentos), que é mais estrita (sem pisos de caracteres e com limite por baralho). Essas páginas têm os seus testes
(tests/test_provas_cartoes.py, com a catraca de prova.json, e tests/test_aquecimentos_m*_opcoes.py) e ficam fora da regra
deste (na_regra()). tests/test_opcoes_equilibradas.py usa este script: zero denunciadoras e uma catraca por pasta.

Uso:
  python3 scripts/medir_opcoes.py [RAIZ]                    resumo por pasta (RAIZ: por omissão, a raiz do repositório)
  python3 scripts/medir_opcoes.py --regra                   só o que a regra de tests/test_opcoes_equilibradas.py mede
  python3 scripts/medir_opcoes.py --catraca                 os números da catraca, para colar no teste quando descerem
  python3 scripts/medir_opcoes.py --json SAIDA.json         todas as perguntas medidas
  python3 scripts/medir_opcoes.py --listas PASTA            uma lista de denunciadoras por grupo (m1 … m9, outros)
  python3 scripts/medir_opcoes.py --fora tarefas/m1-u1/     deixa caminhos de fora (pode repetir-se)
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from opcoes_equilibradas import MAX_AMPLITUDE, MAX_VANTAGEM  # noqa: E402

RAZAO, PISO = MAX_VANTAGEM, 5             # denunciadora: 1,25 × a maior errada e 5 caracteres a mais
AMPL, PISO_AMPL = 1 + MAX_AMPLITUDE, 8    # amplitude: 1,20, com 8 caracteres de diferença

# Fora da regra de tests/test_opcoes_equilibradas.py, porque têm testes de opções próprios: as provas em cartões
# (geradas por scripts/provas/gerar.py; catraca em prova.json) e os aquecimentos em cartões (scripts/aquecimentos.py).
FORA_DA_REGRA = re.compile(r'^(exame/provas/|tarefas/[^/]+/aquecimento/)')


def na_regra(rel):
    return not FORA_DA_REGRA.match(rel)


def limpa(s):
    s = re.sub(r'<[^>]+>', '', str(s))
    s = re.sub(r'[_*]', '', s)
    s = s.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return re.sub(r'\s+', ' ', s).strip()


def objetos(texto):
    """Literais JSON/JS que começam por { ou [ depois de '=', ':' ou '(' (emparelhamento de chavetas, aspas duplas)."""
    for m in re.finditer(r'(?:=|:|\()\s*([\[{])', texto):
        i = m.start(1)
        prof = 0
        dentro = False
        esc = False
        for j in range(i, min(len(texto), i + 3_000_000)):
            ch = texto[j]
            if dentro:
                if esc:
                    esc = False
                elif ch == '\\':
                    esc = True
                elif ch == '"':
                    dentro = False
                continue
            if ch == '"':
                dentro = True
            elif ch in '[{':
                prof += 1
            elif ch in ']}':
                prof -= 1
                if prof == 0:
                    bloco = texto[i:j + 1]
                    if len(bloco) > 60:
                        try:
                            yield json.loads(bloco)
                        except Exception:
                            pass
                    break


def itens(no):
    """As escolhas múltiplas de um literal: (formato, pergunta, opções limpas, índices das certas)."""
    if isinstance(no, dict):
        oficial = no.get('t') == 'item'
        o = no.get('o')
        c = no.get('c')
        if isinstance(c, str) and c.isdigit():
            c = int(c)
        if (not oficial and isinstance(o, list) and len(o) >= 2 and all(isinstance(x, str) for x in o)
                and isinstance(c, int) and 0 <= c < len(o)):
            yield ('o/c', no.get('p') or no.get('pergunta') or no.get('titulo') or '', [limpa(x) for x in o], [c])
        op = no.get('opcoes')
        if not oficial and isinstance(op, list) and len(op) >= 2 and all(isinstance(x, list) and len(x) >= 2 for x in op):
            certos = [k for k, x in enumerate(op) if str(x[1]).lower() in ('certo', 'certa', 'correto', 'ok', 'true')]
            if certos and len(certos) < len(op):
                yield ('opcoes', no.get('pergunta') or no.get('p') or '', [limpa(x[0]) for x in op], certos)
        for chave in ('opcoes', 'options', 'alternativas'):
            op = no.get(chave)
            if not oficial and isinstance(op, list) and len(op) >= 2 and all(isinstance(x, dict) for x in op):
                certos = [k for k, x in enumerate(op)
                          if x.get('certa') or x.get('correta') or x.get('correct') or x.get('certo')]
                txt = [limpa(x.get('texto') or x.get('t') or x.get('text') or '') for x in op]
                if certos and len(certos) < len(op) and all(txt):
                    yield (chave, no.get('pergunta') or no.get('p') or '', txt, certos)
        for v in no.values():
            yield from itens(v)
    elif isinstance(no, list):
        for v in no:
            yield from itens(v)


def avalia(opts, certos):
    ls = [len(x) for x in opts]
    lc = max(ls[c] for c in certos)
    outros = [n for k, n in enumerate(ls) if k not in certos]
    if not outros or min(ls) == 0:
        return None
    me = max(outros)
    return {'certa': lc, 'maior_errada': me, 'razao': round(lc / me, 2) if me else 9.99,
            'denunciadora': lc >= RAZAO * me and lc - me >= PISO,
            'amplitude': round(max(ls) / min(ls), 2),
            'fora20': max(ls) / min(ls) > AMPL and max(ls) - min(ls) >= PISO_AMPL,
            'certa_mais_longa': lc > me}


def medir(raiz=ROOT, fora=()):
    """Todas as perguntas medidas da árvore (uma vez por ficheiro, pergunta e opções)."""
    raiz = Path(raiz)
    res = []
    vistos = set()
    for f in sorted(raiz.rglob('*')):
        rel = f.relative_to(raiz).as_posix()
        if f.suffix not in ('.html', '.js', '.json') or not f.is_file():
            continue
        if rel.split('/')[0] in ('.git', 'tests', 'scripts', 'docs', 'node_modules') or 'imprimir' in rel:
            continue
        if any(rel.startswith(x) for x in fora):
            continue
        try:
            t = f.read_text('utf-8')
        except Exception:
            continue
        if '"o":' not in t and '"opcoes"' not in t and '"options"' not in t:
            continue
        for obj in objetos(t):
            for tipo, perg, opts, certos in itens(obj):
                chave = (rel, limpa(perg)[:80], tuple(opts))
                if chave in vistos:
                    continue
                vistos.add(chave)
                a = avalia(opts, certos)
                if a:
                    res.append({'ficheiro': rel, 'tipo': tipo, 'pergunta': limpa(perg)[:200], 'opcoes': opts,
                                'certas': certos, **a})
    return res


def pasta(rel):
    return rel.split('/')[0]


def grupo(rel):
    top = pasta(rel)
    return top if re.fullmatch(r'm[1-9]', top) else 'outros'


def por_pasta(res):
    por = collections.defaultdict(collections.Counter)
    for r in res:
        c = por[pasta(r['ficheiro'])]
        c['n'] += 1
        c['den'] += r['denunciadora']
        c['f20'] += r['fora20']
        c['ml'] += r['certa_mais_longa']
    return por


def catraca(res):
    """Os números da catraca de tests/test_opcoes_equilibradas.py, por pasta, só com o que a regra mede."""
    por = por_pasta([r for r in res if na_regra(r['ficheiro'])])
    return {g: {'fora20': c['f20'], 'certa_mais_longa': c['ml']} for g, c in sorted(por.items())}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('raiz', nargs='?', default=str(ROOT))
    ap.add_argument('--json')
    ap.add_argument('--listas')
    ap.add_argument('--fora', action='append', default=[])
    ap.add_argument('--regra', action='store_true', help='só o que a regra do teste mede (sem provas nem aquecimentos)')
    ap.add_argument('--catraca', action='store_true', help='os números da catraca do teste, por pasta')
    a = ap.parse_args()
    res = medir(a.raiz, a.fora)
    if a.regra or a.catraca:
        res = [r for r in res if na_regra(r['ficheiro'])]
    if a.catraca:
        for g, c in catraca(res).items():
            print(f"    {g!r}: {{'fora20': {c['fora20']}, 'certa_mais_longa': {c['certa_mais_longa']}}},")
        return
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), 'utf-8')
    tot = collections.Counter()
    print(f"{'pasta':10s} {'perguntas':>9s} {'denunc.':>8s} {'fora20':>7s} {'certa+longa':>12s}")
    for g, c in sorted(por_pasta(res).items(), key=lambda x: (-x[1]['den'], x[0])):
        print(f"{g:10s} {c['n']:9d} {c['den']:8d} {c['f20']:7d} {c['ml']:12d}")
        tot.update(c)
    print(f"{'TOTAL':10s} {tot['n']:9d} {tot['den']:8d} {tot['f20']:7d} {tot['ml']:12d}")
    if a.listas:
        d = Path(a.listas)
        d.mkdir(parents=True, exist_ok=True)
        gl = collections.defaultdict(list)
        for r in res:
            if r['denunciadora']:
                gl[grupo(r['ficheiro'])].append(r)
        for g in ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'outros']:
            (d / f'lista-{g}.json').write_text(json.dumps(gl.get(g, []), ensure_ascii=False, indent=1), 'utf-8')
            print(f'lista-{g}.json: {len(gl.get(g, []))} denunciadoras')


if __name__ == '__main__':
    main()
