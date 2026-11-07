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
import unicodedata

from aquecimentos import molde, V_JOGO, BOTAO_PROJETAR
from audit_cards import validate_cards
from medir_opcoes import limpa
from opcoes_equilibradas import avaliar

ROOT = Path(__file__).resolve().parents[1]
TIPOS = {'escolha', 'vf', 'emparelhar', 'ordenar', 'sublinhar', 'completar', 'versos'}
EXTENSO = {10: 'Dez', 11: 'Onze', 12: 'Doze', 13: 'Treze', 14: 'Catorze'}


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


# 02/11/2026 (pt #155): retornos genéricos, remissões para peças da lição que não existem na página, títulos de
# poemas em itálico dentro de aspas.
RETORNO_GENERICO = re.compile(r'voltares a responder|Confere o indício|^Nesta lacuna,.*não corresponde')
PECAS_AUSENTES = re.compile(r'«O essencial»|«Abre»|«Em paralelo»|linha de vida|«Recorda»|árvore da frase|parágrafo modelo|'
                            r'tese (?:do )?modelo|resumo-modelo|\(aula \d|lição F\d|coluna «|guião de visionamento|glossário')
ITALICO_EM_ASPAS = re.compile(r'«_|«<i>')
# 07/11/2026: explicações antigas que test_exame_alignment obriga a serem iguais às da lição de origem (página
# congelada); só mudam com uma camada sobre a lição, num pedido próprio. Fica a lista fechada, e nada mais escapa.
LEGADO_DA_LICAO = {'s11-q2': "O «épico d'outr'ora» é a estátua de Camões, «Bronzeo, monumental», segundo o glossário."}
ROTULOS_LER = {'Abre', 'Texto de apoio'}


def _sem_acentos(s):
    s = unicodedata.normalize('NFD', limpa(s).lower())
    return ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')


def _contem(texto, trecho):
    t, x = _sem_acentos(texto), _sem_acentos(trecho)
    return bool(x) and re.search(r'(?<!\w)' + re.escape(x) + r'(?!\w)', t) is not None


def _textos(c):
    """Os textos visíveis de um cartão, para as regras de redação."""
    out = [c.get(k) for k in ('p', 'f', 'frase', 'cita', 'titulo')]
    out += c.get('o', []) + c.get('passos', []) + c.get('linhas', [])
    out += [x for par in c.get('pares', []) for x in par]
    fe = c.get('fe')
    out += fe if isinstance(fe, list) else [fe]
    for gap in c.get('lacunas', []):
        out += gap['o'] + [x for x in gap.get('fe', []) if x]
    return [x for x in out if isinstance(x, str)]


def saltos_de_estrofe(html):
    """Blocos de versos (p.v) com dois versos seguidos de numeração não contígua: estrofes coladas."""
    erros = []
    for bloco in re.findall(r'<p class="v">(.*?)</p>', html, re.S):
        nums = [(int(a), int(b)) for a, b in re.findall(r'data-l="(\d+)-(\d+)"', bloco)]
        for (a0, b0), (a1, b1) in zip(nums, nums[1:]):
            if a1 != a0 or b1 != b0 + 1:
                erros.append(f'{a0}-{b0} seguido de {a1}-{b1}')
    return erros


def grupos_de_opcoes(d):
    """As perguntas de escolha e as lacunas do banco, como a medição única da casa as conta."""
    out = []
    for i, c in enumerate(d['cartoes']):
        if c['t'] == 'escolha':
            out.append({'opcoes': c['o'], 'certa': c['c'], 'k': min(3, len(c['o'])), 'onde': f'{d["sessao"]} cartão {i}'})
        for k, gap in enumerate(c.get('lacunas', [])):
            out.append({'opcoes': gap['o'], 'certa': gap['c'], 'k': len(gap['o']), 'onde': f'{d["sessao"]} cartão {i}, lacuna {k + 1}'})
    return out


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
    # 02/11/2026: abertura com título e tempo; o texto de apoio tem rótulo próprio (o motor escrevia «Faz»).
    if not cards or cards[0]['t'] != 'ler' or cards[0].get('rot') != 'Abre':
        erros.append('O primeiro cartão é a abertura (ler, com "rot": "Abre").')
    for i, c in enumerate(cards):
        if c['t'] == 'ler':
            if c.get('rot') not in ROTULOS_LER:
                erros.append(f'{i}: cartão de leitura sem rótulo próprio.')
            for e in saltos_de_estrofe(c.get('html', '')):
                erros.append(f'{i}: estrofes coladas num só bloco de versos ({e}).')
        for texto in _textos(c):
            if c.get('legacyId') in LEGADO_DA_LICAO and texto == c.get('f') == LEGADO_DA_LICAO[c['legacyId']]:
                continue
            if PECAS_AUSENTES.search(texto):
                erros.append(f'{i}: remete para uma peça que não está na página: {PECAS_AUSENTES.search(texto).group(0)}')
            if ITALICO_EM_ASPAS.search(texto):
                erros.append(f'{i}: título em itálico dentro de aspas.')
    # 02/11/2026: nunca mais de dois cartões de fazer seguidos do mesmo tipo.
    for i in range(2, len(fazer)):
        if fazer[i]['t'] == fazer[i - 1]['t'] == fazer[i - 2]['t']:
            erros.append(f'{i + 1}: três cartões seguidos do tipo {fazer[i]["t"]}.')
    for i, c in enumerate(fazer, 1):
        if not c.get('recycledFrom'):
            erros.append(f'{i}: falta a lição de origem.')
        if not c.get('fe'):
            erros.append(f'{i}: falta o retorno de erro.')
        if isinstance(c.get('fe'), str) and RETORNO_GENERICO.search(c['fe']):
            erros.append(f'{i}: retorno de erro genérico: nomeia a confusão e manda reler uma pista.')
        if c['t'] == 'escolha':
            if not isinstance(c['fe'], list) or len(c['fe']) != len(c['o']):
                erros.append(f'{i}: falta o retorno por opção.')
        if c['t'] in ('versos', 'ordenar') and c.get('cita') in (c.get('linhas') or c.get('passos') or []):
            erros.append(f'{i}: a citação é uma das linhas a ordenar.')
        ops = [c] if c['t'] == 'escolha' else c.get('lacunas', [])
        for op in ops:
            if not isinstance(op.get('fe'), list) or len(op['fe']) != len(op['o']):
                erros.append(f'{i}: falta retorno por alternativa.')
            elif any(not text for j, text in enumerate(op['fe']) if j != op['c']):
                erros.append(f'{i}: alternativa errada sem explicação.')
            elif any(RETORNO_GENERICO.search(text) for j, text in enumerate(op['fe']) if j != op['c']):
                erros.append(f'{i}: retorno de alternativa no molde genérico.')
            ns = [len(limpa(s)) for s in op['o']]
            if max(ns) > min(ns) * 1.2:
                erros.append(f'{i}: opções fora dos 20 %: {ns}.')
            if ns[op['c']] > max(n for j, n in enumerate(ns) if j != op['c']):
                erros.append(f'{i}: a certa é a única mais longa: {ns}.')
        if c['t'] == 'completar':
            for k, gap in enumerate(c['lacunas'], 1):
                if len(gap['o']) < 3:
                    erros.append(f'{i}: a lacuna {k} tem menos de três opções.')
                certa = gap['o'][gap['c']]
                for campo in ('cita', 'p'):
                    if c.get(campo) and _contem(c[campo], certa):
                        erros.append(f'{i}: a resposta da lacuna {k} («{certa}») está escrita em {campo}.')
    # 02/11/2026: a medição única das opções equilibradas (scripts/opcoes_equilibradas.py), empates contam.
    erros += [f'opções: {e}' for e in avaliar(grupos_de_opcoes(d))['erros']]
    antigos = {c.get('legacyId') for c in fazer}
    for n in range(1, 4):
        if f'{d["sessao"]}-q{n}' not in antigos:
            erros.append(f'Falta a pergunta antiga {n}.')
    return erros


def validar_conjunto(bancos):
    """02/11/2026 (pt #155): regras entre bancos: nenhum retorno de erro, enunciado, frase ou par repetido em dois
    cartões, e verdadeiros entre 40 % e 60 % dos cartões de verdadeiro ou falso."""
    erros, vistos = [], {}
    def ver(chave, onde):
        if chave in vistos:
            erros.append(f'{onde}: repete {vistos[chave]} ({chave[0]}).')
        else:
            vistos[chave] = onde
    vf = []
    for d in bancos:
        for i, c in enumerate(d['cartoes']):
            if c['t'] == 'ler':
                continue
            onde = f'{d["sessao"]} cartão {i}'
            if isinstance(c.get('fe'), str):
                ver(('retorno', limpa(c['fe'])), onde)
            ver(('enunciado', limpa(c.get('p', '')) + '|' + limpa(c.get('frase', ''))), onde)
            for par in c.get('pares', []):
                ver(('par', limpa(par[0]) + '|' + limpa(par[1])), onde)
            if c['t'] == 'vf':
                vf.append(c['v'])
    if vf and not 0.4 <= sum(vf) / len(vf) <= 0.6:
        erros.append(f'verdadeiro ou falso desequilibrado: {sum(vf)} verdadeiros em {len(vf)}.')
    return erros


def preparar(d):
    """02/11/2026 (pt #155): o conteúdo dos desdobráveis de leitura vai dentro de um <div>, que lesson.css almofada."""
    d = json.loads(json.dumps(d))
    for c in d['cartoes']:
        if c['t'] == 'ler' and '<details>' in c.get('html', ''):
            c['html'] = re.sub(r'(<details><summary>.*?</summary>)(?!<div>)(.*?)(</details>)', r'\1<div>\2</div>\3', c['html'], flags=re.S)
    return d


def pagina(d, raiz=ROOT):
    sid = d['sessao']
    titulo = escape(d['titulo'])
    n = sum(1 for c in d['cartoes'] if c['t'] != 'ler')
    texto = any(c.get('rot') == 'Texto de apoio' for c in d['cartoes'])
    # 02/11/2026 (pt #155): o menu só promete textos quando há texto de apoio; «dispositivo», como no resto do exame.
    extra = ('Podes consultar os textos. ' if texto else '') + 'O progresso fica neste dispositivo; a projeção não o guarda.'
    dados = json.dumps(preparar(d), ensure_ascii=False).replace('</', '<\\/')
    return f'''<!doctype html>
<html lang="pt-PT" data-appearance-site="pt" data-appearance-family="cards">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Aquecer: {titulo} | Português</title>
<meta name="description" content="{EXTENSO[n]} cartões para preparar a leitura e a escrita da sessão de exame.">
<link rel="stylesheet" href="../../../assets/pt-lessons/lesson.css">
<script defer src="../../../assets/pt-lessons/casca.js"></script>
<script defer src="../../../assets/pt-lessons/jogo.js?v={V_JOGO}"></script>
<link rel="stylesheet" href="../../../assets/relogio.css">
<script defer src="../../../assets/relogio.js"></script>
{molde(raiz)}
<link rel="stylesheet" href="../../../assets/exame/aquecimento.css?v=20261102">
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
<p class="c-menu-extra">{extra}</p></div></div></div>
<noscript>Ativa o JavaScript para abrir os cartões. <a href="../../#{sid}/aquecer">Voltar à sessão</a>.</noscript>
<script id="exame-aquecimento-dados" type="application/json">{dados}</script>
<script defer src="../../../assets/exame/aquecimento.js?v=20261102"></script>
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
    caminhos = sorted((ROOT / 'docs/pedagogia/exame-aquecimentos').glob('s*.json'))
    bancos = [json.loads(p.read_text('utf-8')) for p in caminhos]
    falhas.extend(f'conjunto: {e}' for e in validar_conjunto(bancos))
    for p, d in zip(caminhos, bancos):
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
