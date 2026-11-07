"""Gera os aquecimentos do exame, com a casca e o motor das lições.

Os bancos são editoriais: cada cartão conserva a lição e o cartão de origem.
O gerador não escolhe perguntas nem altera os dados das lições.
"""
import argparse
from collections import Counter
from html import escape
import json
from pathlib import Path
import re
import sys

from aquecimentos import molde, V_JOGO, BOTAO_PROJETAR
from audit_cards import validate_cards
from medir_opcoes import limpa

ROOT = Path(__file__).resolve().parents[1]
TIPOS = {'escolha', 'vf', 'emparelhar', 'ordenar', 'sublinhar', 'completar', 'versos'}


# 07/11/2026: os ficheiros de main que este pedido muda (duração de 50 minutos, aquecimento de 10 minutos e a
# ligação para os cartões); as camadas literais que os registam têm de ver os resumos refeitos sobre a árvore atual.
FICHEIROS_DO_PEDIDO = ('assets/exame/sessoes.json', 'assets/exame/app.js', 'exame/index.html')
NOTA_50 = (' 01/11/2026: duração das sessões de exame atualizada para 50 minutos (decisão 106); trocas, ocorrências e '
           'restantes ficheiros preservados; só os resumos dos ficheiros do exame que o pedido pt #155 muda foram '
           'refeitos (07/11/2026: sobre a fusão com o main), sem mudar o base_commit do manifesto, que continua a ser '
           'o das bases dos outros ficheiros.')


def atualizar_contratos():
    """01/11/2026: regista os 50 minutos sem mudar as trocas antigas de texto.

    07/11/2026 (pt #155, achados 9, 43, 60, 61 e 73): a cadeia de camadas é a de scripts/verificar_camadas.py, a mesma
    do CI (cada camada confere-se com as mais recentes desfeitas antes); só mudam os dois resumos das entradas dos
    ficheiros do exame que este pedido muda, e só se as trocas da camada estiverem todas aplicadas. O base_commit fica
    e a nota junta-se uma vez só.
    """
    from aplicar_trocas import carregar, processar, desfazer_camadas, sha_lf
    from verificar_camadas import LAYERS
    for i, (layer, manifest_name) in enumerate(LAYERS):
        target = ROOT / 'tests/fixtures' / (manifest_name + '.json')
        manifest = json.loads(target.read_text('utf-8'))
        relevantes = [f for f in FICHEIROS_DO_PEDIDO if f in manifest['files']]
        if not relevantes:
            continue
        _, changes = carregar(str(ROOT / 'scripts' / (layer + '.json')))
        newer = [ROOT / 'tests/fixtures' / (m + '.json') for _, m in LAYERS[:i]]
        camadas = [(str(p), json.loads(p.read_text('utf-8'))['files']) for p in newer]
        mudou = False
        for relative in relevantes:
            text = (ROOT / relative).read_bytes().decode('utf-8')
            text = desfazer_camadas(relative, text, camadas)
            before, after, states = processar(relative, changes[relative], text)
            if after != text or any(state != 'aplicada' for state in states):
                raise ValueError(f'{layer}: {relative}: as trocas têm de estar todas aplicadas; não se altera o seu conteúdo.')
            entry = manifest['files'][relative]
            hashes = {'base_sha256_lf': sha_lf(before), 'after_sha256_lf': sha_lf(after)}
            if any(entry[k] != value for k, value in hashes.items()):
                entry.update(hashes)
                mudou = True
        if mudou:
            if '(decisão 106)' not in manifest['_nota']:
                manifest['_nota'] += NOTA_50
            target.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n', 'utf-8')
            print('contrato refeito:', target.relative_to(ROOT))


def validar(d):
    cards = d['cartoes']
    erros = validate_cards(cards)
    fazer = [c for c in cards if c['t'] != 'ler']
    if len(fazer) < 12:
        erros.append('São necessários pelo menos 12 cartões de fazer.')
    if len({c['t'] for c in fazer}) < 5:
        erros.append('São necessários pelo menos cinco tipos.')
    if any(c['t'] not in TIPOS for c in fazer):
        erros.append('Tipo não autorizado neste aquecimento.')
    if not any(c['t'] == 'completar' and len(c['lacunas']) >= 2 for c in fazer):
        erros.append('Falta completar com várias lacunas.')
    for i, c in enumerate(fazer, 1):
        if not c.get('recycledFrom'):
            erros.append(f'{i}: falta a lição de origem.')
        if not c.get('fe'):
            erros.append(f'{i}: falta o retorno de erro.')
        if c['t'] == 'escolha':
            if not isinstance(c['fe'], list) or len(c['fe']) != len(c['o']):
                erros.append(f'{i}: falta o retorno por opção.')
        ops = [c] if c['t'] == 'escolha' else c.get('lacunas', [])
        for op in ops:
            if not isinstance(op.get('fe'), list) or len(op['fe']) != len(op['o']):
                erros.append(f'{i}: falta retorno por alternativa.')
            elif any(not text for j, text in enumerate(op['fe']) if j != op['c']):
                erros.append(f'{i}: alternativa errada sem explicação.')
            ns = [len(limpa(s)) for s in op['o']]
            if max(ns) > min(ns) * 1.2:
                erros.append(f'{i}: opções fora dos 20 %: {ns}.')
            if ns[op['c']] > max(n for j, n in enumerate(ns) if j != op['c']):
                erros.append(f'{i}: a certa é a única mais longa: {ns}.')
    antigos = {c.get('legacyId') for c in fazer}
    for n in range(1, 4):
        if f'{d["sessao"]}-q{n}' not in antigos:
            erros.append(f'Falta a pergunta antiga {n}.')
    return erros


def pagina(d, raiz=ROOT):
    sid = d['sessao']
    titulo = escape(d['titulo'])
    dados = json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
    return f'''<!doctype html>
<html lang="pt-PT" data-appearance-site="pt" data-appearance-family="cards">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Aquecer: {titulo} | Português</title>
<meta name="description" content="Doze cartões para preparar a leitura e a escrita da sessão de exame.">
<link rel="stylesheet" href="../../../assets/pt-lessons/lesson.css">
<script defer src="../../../assets/pt-lessons/casca.js"></script>
<script defer src="../../../assets/pt-lessons/jogo.js?v={V_JOGO}"></script>
<link rel="stylesheet" href="../../../assets/relogio.css">
<script defer src="../../../assets/relogio.js"></script>
{molde(raiz)}
<link rel="stylesheet" href="../../../assets/exame/aquecimento.css?v=20261101">
<link rel="stylesheet" href="../../../assets/appearance.css?v=20261025-universal-1">
<script src="../../../assets/appearance.js?v=20261025-universal-1"></script>
</head><body><div class="casca" data-casca>
<header class="casca-topo"><a class="c-marca" data-exame-voltar href="../../#{sid}/aquecer" aria-label="Voltar à sessão">Exame</a>
<span class="c-num" data-c-num></span><button type="button" class="c-barra" data-c-barra aria-label="Ver os cartões já feitos" disabled><svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg></button>
<span class="c-modo" data-c-modo hidden></span>
<button type="button" class="c-ic" data-c-como hidden aria-label="Como se faz este cartão?">?</button>
<button type="button" class="c-ic" data-c-som aria-pressed="false" aria-label="Som"><span class="c-roda">♪</span></button>
<button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false"><span class="c-tres"></span></button></header>
<h1 class="c-sr">Aquecer: {titulo}</h1>
<main class="casca-corpo" tabindex="-1"><div id="baralho" class="jogo-alvo"></div></main>
<footer class="casca-acoes" data-c-acoes></footer>
<section class="casca-folha" data-c-folha role="status" aria-live="polite" hidden></section>
<div class="casca-menu" data-c-painel hidden><div class="c-menu-in" role="dialog" aria-label="Menu"><div class="c-menu-cab"><p>Aquecer: sessão {sid[1:]}<br>10 minutos</p><button type="button" class="c-ic" data-c-fecha-menu aria-label="Fechar o menu">✕</button></div>
<nav aria-label="Navegação do aquecimento"><a data-exame-voltar href="../../#{sid}/aquecer">Voltar à sessão</a><a href="?projetar=1">{BOTAO_PROJETAR}</a></nav>
<div id="relogio-aquecer"></div>
<p class="c-menu-extra">Podes consultar os textos. O progresso fica neste aparelho; a projeção não o guarda.</p></div></div></div>
<noscript>Ativa JavaScript para abrir os cartões. <a href="../../#{sid}/aquecer">Voltar à sessão</a>.</noscript>
<script id="exame-aquecimento-dados" type="application/json">{dados}</script>
<script defer src="../../../assets/exame/aquecimento.js?v=20261101"></script>
<script defer src="../../../assets/projection-launcher.js?v=20261019.4" data-site="pt"></script>
</body></html>
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='confere também se as páginas estão atualizadas')
    ap.add_argument('--atualizar-contratos', action='store_true', help='regenera os resumos de verificação de sessoes.json, preservando as trocas anteriores')
    a = ap.parse_args()
    if a.atualizar_contratos:
        if a.check:
            ap.error('--check não escreve contratos')
        atualizar_contratos()
    falhas = []
    for p in sorted((ROOT / 'docs/pedagogia/exame-aquecimentos').glob('s*.json')):
        d = json.loads(p.read_text('utf-8'))
        erros = validar(d)
        if erros:
            falhas.extend(f'{p.stem}: {e}' for e in erros)
            continue
        alvo = ROOT / 'exame/aquecimentos' / d['sessao'] / 'index.html'
        html = pagina(d)
        if a.check:
            if not alvo.exists() or alvo.read_text('utf-8') != html:
                falhas.append(f'{p.stem}: página por regenerar')
        else:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(html, 'utf-8')
        print(d['sessao'], dict(Counter(c['t'] for c in d['cartoes'])))
    if falhas:
        print('\n'.join(falhas), file=sys.stderr)
    return bool(falhas)


if __name__ == '__main__':
    sys.exit(main())
