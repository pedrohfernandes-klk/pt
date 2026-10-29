#!/usr/bin/env python3
"""Aplica trocas literais de texto, de forma idempotente, e gera o manifesto reversível.

28/10/2026: auditoria do M7 (todos os achados confirmados), resto do M4 e resto do M1, depois do PR #128.

Cada troca é {ficheiro, local, antigo, novo, ocorrencias, achado}. O script:

* aplica as trocas pela ordem do JSON, ficheiro a ficheiro;
* falha se o texto antigo não aparecer exatamente «ocorrencias» vezes (nada se troca em silêncio); a falha é por
  ficheiro (29/10/2026): esse ficheiro fica como estava, sai do manifesto e é listado no fim, e os outros aplicam-se;
* reconhece uma troca já aplicada (o novo está lá «ocorrencias» vezes e o antigo já não), e por isso pode
  voltar a correr sobre a mesma árvore, ou sobre uma base onde outro PR mexeu noutras partes destes ficheiros;
* confere que, no fim, cada «novo» aparece exatamente «ocorrencias» vezes e que desfazer as trocas (da última
  para a primeira) devolve a base, letra a letra;
* escreve o manifesto no formato do #128 (base_commit, _nota, files com base_sha256_lf, after_sha256_lf e
  edits [location, old, new, occurrences]), que tests/auditoria_20261028.py usa para desfazer as trocas
  antes das comparações com estados congelados.

Ordem com o PR que tira a Sala (29/10/2026): este lote funde-se primeiro; o corte da Sala (scripts/desligar_sala.py)
corre-se depois, sobre as lições já corrigidas, e refaz o relâmpago e o material dos painéis a partir delas. Sobre uma
árvore onde a Sala já foi cortada, os painéis do M7 cujo relâmpago este lote corrige não conferem e ficam por resolver
(ver docs/pedagogia/auditoria-m4-m7-20261028.md).

Uso:
  python3 scripts/aplicar_trocas.py               aplica o que faltar e regenera o manifesto
  python3 scripts/aplicar_trocas.py --verificar   só confere; sai com 1 se faltar aplicar ou o manifesto
                                                  não corresponder às páginas
  python3 scripts/aplicar_trocas.py OUTRO.json --manifesto tests/fixtures/OUTRO.json --nota "…"
                                                  outro lote, com a sua nota (29/10/2026: sem --nota, o manifesto
                                                  levava a nota fixa do lote de 28/10)
  python3 scripts/aplicar_trocas.py --verificar --desfazer-antes tests/fixtures/aquecimentos-m7-edits-20261029.json \
      --fora tarefas/m7-u3/index.html
                                                  29/10/2026 (revisão técnica): confere um lote que já tem outra camada
                                                  por cima. Cada --desfazer-antes (pode repetir-se, da camada mais recente
                                                  para a mais antiga) desfaz no texto lido as trocas desse manifesto antes
                                                  de conferir; nada se escreve. --fora deixa de fora um ficheiro gerado de
                                                  novo por cima do lote (como a tarefa da M7-U3).
Sai com 2 se algum ficheiro não conferir (nos dois modos).
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TROCAS = ROOT / 'scripts/auditoria_m4_m7_20261028.json'
MANIFESTO = ROOT / 'tests/fixtures/auditoria-m4-m7-edits-20261028.json'
NOTA = (
    '28/10/2026: correções confirmadas pela auditoria do M7 (todos os achados), do resto do M4 (tarefa da '
    'unidade 1 individual e em papel, numeração atual das tarefas, «As tarefas do Teams» do mapa, guião da '
    'aula 9 reescrito a partir da lição M4-F28 e do painel) e do resto do M1 (itálicos nos guiões, «·» nos '
    'cartões de tarefa). Gerado por scripts/aplicar_trocas.py a partir de scripts/auditoria_m4_m7_20261028.json: '
    'não se edita à mão. Só texto. Ordem, tipos, chaves e respostas certas dos cartões ficam iguais, salvo onde o '
    'achado o pede expressamente: M7-F07 CARTOES[9].certas (e a cópia no arquivo do índice), CARTOES[3].pares[1]; '
    'M7-F04 CARTOES[17].pares[2]; M7-F10 CARTOES[6].passos (e a cópia no arquivo do índice) e CARTOES[17].pares; '
    'tipo do relâmpago k19 do painel-m7-f02 (o cartão 19 da lição já é «escolha»). Desfaz-se antes do manifesto do #128 '
    '(auditoria-m1-m4-edits-20261028.json): o mais recente primeiro. O corte da Sala (scripts/desligar_sala.py) '
    'entra depois deste lote, por isso o seu manifesto desfaz-se antes deste.'
)


class TrocaFalhou(Exception):
    pass


def sha_lf(text):
    return hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def carregar(caminho):
    trocas = json.loads(Path(caminho).read_text('utf-8'))
    por_ficheiro = {}
    for numero, troca in enumerate(trocas, 1):
        for chave in ('ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'):
            if chave not in troca:
                raise TrocaFalhou(f'troca {numero}: falta «{chave}»')
        if not troca['novo']:
            raise TrocaFalhou(f'troca {numero} ({troca["ficheiro"]}): «novo» vazio; para apagar, ancora num pedaço vizinho')
        if troca['antigo'] == troca['novo']:
            raise TrocaFalhou(f'troca {numero} ({troca["ficheiro"]}): «antigo» e «novo» iguais')
        if not isinstance(troca['ocorrencias'], int) or troca['ocorrencias'] < 1:
            raise TrocaFalhou(f'troca {numero} ({troca["ficheiro"]}): «ocorrencias» tem de ser um inteiro positivo')
        por_ficheiro.setdefault(troca['ficheiro'], []).append((numero, troca))
    return trocas, por_ficheiro


def _fora_do_novo(text, antigo, novo):
    """Conta o antigo sem contar o que estiver dentro de uma ocorrência do novo."""
    return text.replace(novo, '\0').count(antigo)


def estado(text, troca):
    antigo, novo, n = troca['antigo'], troca['novo'], troca['ocorrencias']
    novo_na_base = n * antigo.count(novo)
    if _fora_do_novo(text, antigo, novo) == 0 and text.count(novo) == n:
        return 'aplicada'
    if text.count(antigo) == n and text.count(novo) == novo_na_base:
        return 'por aplicar'
    return None


def processar(ficheiro, trocas, text):
    """Devolve (base, depois, estados) para o texto atual de um ficheiro, ou levanta TrocaFalhou."""
    estados = []
    for numero, troca in trocas:
        situacao = estado(text, troca)
        if situacao is None:
            raise TrocaFalhou(
                f'{ficheiro}: troca {numero} ({troca["local"]}): o antigo aparece {text.count(troca["antigo"])} '
                f'vez(es) e o novo {text.count(troca["novo"])}, mas a troca pede {troca["ocorrencias"]}')
        estados.append(situacao)
    # A base desfaz só as trocas que já estão aplicadas, da última para a primeira.
    base = text
    for (numero, troca), situacao in reversed(list(zip(trocas, estados))):
        if situacao == 'aplicada':
            base = base.replace(troca['novo'], troca['antigo'])
    depois = base
    for numero, troca in trocas:
        if depois.count(troca['antigo']) != troca['ocorrencias']:
            raise TrocaFalhou(
                f'{ficheiro}: troca {numero} ({troca["local"]}): o antigo aparece {depois.count(troca["antigo"])} '
                f'vez(es) na base, e a troca pede {troca["ocorrencias"]}')
        depois = depois.replace(troca['antigo'], troca['novo'])
    for numero, troca in trocas:
        if depois.count(troca['novo']) != troca['ocorrencias']:
            raise TrocaFalhou(
                f'{ficheiro}: troca {numero} ({troca["local"]}): depois de todas as trocas, o novo aparece '
                f'{depois.count(troca["novo"])} vez(es), não {troca["ocorrencias"]}: o manifesto não seria reversível')
    desfeito = depois
    for numero, troca in reversed(trocas):
        if desfeito.count(troca['novo']) != troca['ocorrencias']:
            raise TrocaFalhou(f'{ficheiro}: troca {numero} ({troca["local"]}): não se desfaz com segurança')
        desfeito = desfeito.replace(troca['novo'], troca['antigo'])
    if desfeito != base:
        raise TrocaFalhou(f'{ficheiro}: desfazer as trocas não devolve a base')
    return base, depois, estados


def desfazer_camadas(ficheiro, text, camadas):
    """29/10/2026: desfaz no texto as trocas das camadas mais recentes (da última troca para a primeira, camada a camada)."""
    for caminho, files in camadas:
        for edit in reversed(files.get(ficheiro, {}).get('edits', [])):
            if text.count(edit['new']) != edit['occurrences']:
                raise TrocaFalhou(f'{ficheiro}: a camada {caminho} já não confere ({edit["location"]})')
            text = text.replace(edit['new'], edit['old'])
    return text


def commit_base(manual):
    if manual:
        return manual
    for comando in (['git', 'merge-base', 'HEAD', 'origin/main'], ['git', 'rev-parse', 'HEAD']):
        try:
            return subprocess.run(comando, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            continue
    return 'desconhecido'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('trocas', nargs='?', default=str(TROCAS), help='JSON com as trocas')
    parser.add_argument('--manifesto', default=str(MANIFESTO), help='manifesto a gerar')
    parser.add_argument('--base-commit', help='commit da base (por omissão, git merge-base HEAD origin/main)')
    parser.add_argument('--verificar', action='store_true', help='não escreve nada; sai com 1 se faltar algo')
    parser.add_argument('--nota', default=None,
                        help='29/10/2026: a nota do manifesto (por omissão, a do manifesto que já existe, ou a do lote de 28/10)')
    parser.add_argument('--desfazer-antes', action='append', default=[], metavar='MANIFESTO',
                        help='29/10/2026: com --verificar, desfaz antes as trocas deste manifesto (camada mais recente primeiro)')
    parser.add_argument('--fora', action='append', default=[], metavar='FICHEIRO',
                        help='29/10/2026: com --verificar, não confere este ficheiro (gerado de novo por cima do lote)')
    args = parser.parse_args(argv)
    if (args.desfazer_antes or args.fora) and not args.verificar:
        print('ERRO: --desfazer-antes e --fora só servem com --verificar (o texto desfeito nunca se escreve)', file=sys.stderr)
        return 2
    camadas = []
    for caminho in args.desfazer_antes:
        camadas.append((caminho, json.loads(Path(caminho).read_text('utf-8'))['files']))

    try:
        lista, por_ficheiro = carregar(args.trocas)
    except TrocaFalhou as erro:
        print('ERRO:', erro, file=sys.stderr)
        return 2
    # 29/10/2026 (revisão): cada ficheiro é independente. Um ficheiro em que alguma troca não confere fica como
    # estava (nenhuma das suas trocas se aplica) e é listado no fim; os outros aplicam-se na mesma.
    resultados, falhas = {}, {}
    for ficheiro, trocas in por_ficheiro.items():
        if ficheiro in args.fora:
            continue
        caminho = ROOT / ficheiro
        try:
            if not caminho.is_file():
                raise TrocaFalhou(f'{ficheiro}: o ficheiro não existe')
            text = caminho.read_bytes().decode('utf-8')
            text = desfazer_camadas(ficheiro, text, camadas)
            resultados[ficheiro] = (text,) + processar(ficheiro, trocas, text)
        except TrocaFalhou as erro:
            falhas[ficheiro] = str(erro)

    manifesto_path = Path(args.manifesto)
    anterior = json.loads(manifesto_path.read_text('utf-8')) if manifesto_path.is_file() else {}
    files = {}
    for ficheiro, (atual, base, depois, estados) in resultados.items():
        files[ficheiro] = {
            'base_sha256_lf': sha_lf(base),
            'after_sha256_lf': sha_lf(depois),
            'edits': [
                {'location': troca['local'], 'old': troca['antigo'], 'new': troca['novo'],
                 'occurrences': troca['ocorrencias']}
                for _, troca in por_ficheiro[ficheiro]
            ],
        }
    # O commit da base só muda quando muda alguma base (assim, voltar a correr não mexe no manifesto).
    mesmas_bases = anterior.get('files') and all(
        anterior['files'].get(f, {}).get('base_sha256_lf') == r['base_sha256_lf'] for f, r in files.items())
    base_commit = args.base_commit or (anterior.get('base_commit') if mesmas_bases else None) or commit_base(None)
    # 29/10/2026 (revisão técnica): sem --nota, fica a nota do manifesto que já existe (voltar a correr ou conferir outro
    # lote não troca a nota pela do lote de 28/10).
    nota = args.nota if args.nota is not None else (anterior.get('_nota') or NOTA)
    manifesto = {'base_commit': base_commit, '_nota': nota, 'files': files}
    novo_manifesto = json.dumps(manifesto, ensure_ascii=False, indent=1) + '\n'

    por_aplicar = sum(e.count('por aplicar') for (_, _, _, e) in resultados.values())
    ja = sum(e.count('aplicada') for (_, _, _, e) in resultados.values())
    mudam = [f for f, (atual, _, depois, _) in resultados.items() if atual != depois]
    manifesto_muda = not manifesto_path.is_file() or manifesto_path.read_text('utf-8') != novo_manifesto

    if args.verificar:
        if camadas or args.fora:
            fora = sum(len(por_ficheiro[f]) for f in args.fora if f in por_ficheiro)
            print(f'(29/10/2026) conferido com {len(camadas)} camada(s) desfeita(s) antes; {len(args.fora)} ficheiro(s) '
                  f'de fora ({fora} trocas); o manifesto compara-se só com os ficheiros conferidos.')
        print(f'{len(lista)} trocas em {len(resultados)} ficheiros: {ja} aplicadas, {por_aplicar} por aplicar; '
              f'manifesto {"desatualizado" if manifesto_muda else "em dia"}.')
        avisar_falhas(falhas, por_ficheiro, escrito=False)
        return 2 if falhas else 1 if por_aplicar or manifesto_muda else 0

    for ficheiro in mudam:
        (ROOT / ficheiro).write_bytes(resultados[ficheiro][2].encode('utf-8'))
    if manifesto_muda:
        manifesto_path.parent.mkdir(parents=True, exist_ok=True)
        manifesto_path.write_text(novo_manifesto, 'utf-8')
    print(f'{len(lista)} trocas em {len(resultados)} ficheiros: {por_aplicar} aplicadas agora, {ja} já estavam; '
          f'{len(mudam)} ficheiros mudados; manifesto {"escrito" if manifesto_muda else "sem mudanças"} '
          f'({manifesto_path.relative_to(ROOT) if manifesto_path.is_relative_to(ROOT) else manifesto_path}).')
    avisar_falhas(falhas, por_ficheiro, escrito=True)
    return 2 if falhas else 0


def avisar_falhas(falhas, por_ficheiro, escrito):
    """Lista os ficheiros que ficaram como estavam, com a primeira troca que não confere em cada um."""
    if not falhas:
        return
    trocas = sum(len(por_ficheiro[f]) for f in falhas)
    print(f'ERRO: {len(falhas)} ficheiro(s) por resolver ({trocas} trocas), que ficaram como estavam'
          f'{"; o manifesto não os inclui" if escrito else ""}:', file=sys.stderr)
    for ficheiro, erro in falhas.items():
        print('  ' + erro, file=sys.stderr)
    if any('/painel-' in f for f in falhas):
        print('  Nos painéis, a causa mais provável é a Sala já desligada (scripts/desligar_sala.py refaz o relâmpago '
              'a partir das lições). A ordem certa está em docs/pedagogia/auditoria-m4-m7-20261028.md: este lote '
              'funde-se primeiro e o corte da Sala corre-se depois, sobre as lições já corrigidas.', file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())
