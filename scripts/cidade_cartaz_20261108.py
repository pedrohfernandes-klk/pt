#!/usr/bin/env python3
"""08/11/2026: cartaz «Ler a cidade» na entrada do Português e nome novo da secção nas páginas publicadas.

O utilizador: «quero que [Ler a cidade] tenha um banner em português». A secção «Ler a cidade» vive no Lente
(https://pedrohfernandes-klk.github.io/lente/cidade/); na entrada do Português só havia uma linha pequena de texto a apontar
para ela, por baixo do portal do Lente.

Constrói scripts/cidade_cartaz_20261108.json, a camada literal deste pedido, que se aplica com scripts/aplicar_trocas.py; o
manifesto fica em tests/fixtures/cidade-cartaz-edits-20261108.json:

  python3 scripts/cidade_cartaz_20261108.py
  python3 scripts/aplicar_trocas.py scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --nota "…"

Cada família é uma função que devolve trocas {ficheiro, local, antigo, novo, ocorrencias, achado}, calculadas sobre a base (o
texto de cada página com esta camada desfeita, pelo manifesto, quando ele já existe): o script pode voltar a correr depois de a
camada estar aplicada e dá o mesmo JSON. As contagens conferem-se aqui e outra vez no fim.

Famílias desta camada:
- C1, entrada (index.html): um cartaz novo, «Ler a cidade», logo a seguir ao cartaz do Atlas, com as classes do cartaz do Atlas
  (assets/retro-portals.css), para ficar igual no modo claro, no escuro, na projeção (assets/cartaz-cabecalho.css) e em cores
  forçadas; só a grelha dos números (14 quadrados, em vez de 8) tem regras próprias, num <style> curto à frente do cartaz. O texto
  sai da página do Lente (cidade/index.html): a frase de abertura e as «14 missões, no bairro ou a partir das fotografias» saem do
  parágrafo de abertura; os 14 números são os das missões dessa página (m01 a m06, m08, m10 a m12, m15 a m18), e #m01 é a âncora
  da primeira missão. A linha pequena (p.sp-credit «Português × Cidadania · Ler a cidade: …») sai, porque passa a repetir o
  cartaz. O aplicar_trocas.py não aceita um «novo» vazio: a troca que a retira ancora-se no fim do «i» da fotografia de Muybridge
  e no fim do portal (</details> … </nav>), que ficam iguais.
- C2, frase da sugestão «continua» (o banco de frases de cada página, 238 páginas): «A cidade antes da aula: {nmissoes} missões
  feitas, relê o teu caderno» passa a «Ler a cidade: {nmissoes} missões feitas, relê o teu caderno».
- C3, as outras formas do nome antigo, visíveis ou lidas em voz alta: o título do cartão de sugestão e o rótulo «Sugestão: …» do
  cartão (a versão antiga do cartão, que só sobrevive em m2/gram-subordinadas/index.html), a marca do mesmo cartão («A EPI · a
  cidade antes da aula», em minúsculas) e a ligação da lista «todos» de cada ano (1/, 2/ e 3/todos/index.html).

Não mexe em bairro/index.html, a página do endereço antigo, que redireciona para o Lente e explica a mudança de nome. Também não
mexe nos JSON das camadas antigas (scripts/licoes_m16_20261101.json, scripts/licoes_m89_20261101.json,
scripts/tarefas_m356_20261031.json, scripts/tarefas_m89_20261101.json) nem nos seus manifestos, que trazem a frase antiga no texto
de contexto das suas trocas: são o registo das camadas de baixo, e esta camada é que muda o resultado por cima delas. Nenhum
gerador em scripts/ ou em docs/ escreve hoje a frase ou o nome antigo numa página final fora do sistema de camadas.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/cidade_cartaz_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cidade-cartaz-edits-20261108.json'
ACHADO = ('08/11/2026: pedido do utilizador, «quero que [Ler a cidade] tenha um banner em português»: cartaz «Ler a cidade» na '
          'entrada do Português e nome novo da secção nas páginas publicadas. {f}')
# A página do endereço antigo fica como está: redireciona para o Lente e explica a mudança de nome.
FORA = {'bairro/index.html'}
LENTE_CIDADE = 'https://pedrohfernandes-klk.github.io/lente/cidade/'


_MANIFESTO = json.loads(MANIFESTO.read_text('utf-8'))['files'] if MANIFESTO.is_file() else {}
_BASES = {}


def base(rel):
    """O texto da página sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    if rel not in _BASES:
        texto = (ROOT / rel).read_bytes().decode('utf-8')
        for edit in reversed(_MANIFESTO.get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
        _BASES[rel] = texto
    return _BASES[rel]


def troca(rel, texto, local, antigo, novo, familia, contagem=1):
    """Uma troca literal sobre a base, com a contagem exata conferida já aqui."""
    assert rel not in FORA, rel
    assert texto.count(antigo) == contagem, (rel, local, texto.count(antigo))
    return {'ficheiro': rel, 'local': local, 'antigo': antigo, 'novo': novo, 'ocorrencias': contagem,
            'achado': ACHADO.format(f=familia)}


def publicadas():
    """As páginas publicadas (HTML e JS servidos, segundo o git), sem a página do endereço antigo."""
    saida = subprocess.run(['git', 'ls-files', '-z', '--', '*.html', '*.js'], cwd=ROOT, capture_output=True, check=True)
    return sorted(f for f in saida.stdout.decode('utf-8').split('\0')
                  if f and f not in FORA and not f.startswith(('scripts/', 'tests/', 'docs/')))


def paginas_com(texto):
    """As páginas publicadas cuja base (sem esta camada) traz o texto: a lista é a mesma antes e depois de a camada se aplicar."""
    return [rel for rel in publicadas() if texto in base(rel)]


# ---------------------------------------------------------------------------------------------------------------------
# C1: o cartaz «Ler a cidade» na entrada, logo a seguir ao cartaz do Atlas, e a linha pequena que sai.
C1_FAMILIA = ('Família C1 (entrada): o cartaz «Ler a cidade», com as classes do cartaz do Atlas, logo a seguir a ele; a linha '
              'pequena por baixo do portal do Lente sai, porque passa a repetir o cartaz.')
# Os números das 14 missões da página do Lente, pela ordem dela.
MISSOES = ('01', '02', '03', '04', '05', '06', '08', '10', '11', '12', '15', '16', '17', '18')
C1_ESTILO = ('<style>.atlas-poster-art.cidade-poster-art{grid-template-columns:repeat(4,minmax(0,1fr));font-size:1.15rem}'
             '@media(max-width:760px){.atlas-poster-art.cidade-poster-art{grid-template-columns:repeat(3,minmax(0,1fr));'
             'font-size:.9rem}.cidade-poster-art span{min-height:36px;padding:4px}}@media(max-width:520px){'
             '.atlas-poster-art.cidade-poster-art{grid-template-columns:repeat(7,minmax(0,1fr));font-size:.85rem}}</style>')
C1_CARTAZ = (
    C1_ESTILO
    + '<section class="atlas-poster cidade-poster" aria-labelledby="cidade-poster-title"><div class="atlas-poster-copy">'
    '<p class="portal-kicker">Português × Cidadania</p><h2 id="cidade-poster-title">Ler a<br>cidade<span aria-hidden="true">↗'
    '</span></h2><p>Uma rua pode ser lida como um texto e discutida como um espaço de todos. São 14 missões, no bairro ou a partir '
    'das fotografias.</p><nav aria-label="Entradas de Ler a cidade">'
    f'<a href="{LENTE_CIDADE}">Entrar na cidade <span aria-hidden="true">→</span></a>'
    f'<a href="{LENTE_CIDADE}#m01">Ver as missões <span aria-hidden="true">→</span></a></nav></div>'
    '<div class="atlas-poster-art cidade-poster-art" aria-hidden="true">'
    + ''.join(f'<span>{n}</span>' for n in MISSOES) + '</div></section>')
C1_ANTIGO = '</div></section><nav class="site-portal-wrap" aria-label="Explorar o Lente">'
C1_NOVO = '</div></section>' + C1_CARTAZ + '<nav class="site-portal-wrap" aria-label="Explorar o Lente">'
C1_LINHA = (f'<p class="sp-credit"><strong>Português × Cidadania</strong> · <a href="{LENTE_CIDADE}">Ler a cidade: observar, '
            'criar e discutir o espaço comum →</a></p>')
# A âncora: o fim do «i» da fotografia de Muybridge, antes da linha, e o fim do portal do Lente, depois dela.
C1_LINHA_ANTIGO = '</details>' + C1_LINHA + '</nav>'
C1_LINHA_NOVO = '</details></nav>'


def entrada():
    rel = 'index.html'
    texto = base(rel)
    # O cartaz do Atlas acaba uma só vez assim, logo antes do portal do Lente; a âncora da linha também é única.
    assert texto.count(C1_ANTIGO) == 1 and texto.count(C1_LINHA) == 1 and texto.count(C1_LINHA_NOVO) == 0, rel
    return [
        troca(rel, texto, 'C1, entrada: o cartaz «Ler a cidade», logo a seguir ao cartaz do Atlas', C1_ANTIGO, C1_NOVO,
              C1_FAMILIA),
        troca(rel, texto, 'C1, entrada: sai a linha pequena «Português × Cidadania · Ler a cidade: …», que o cartaz repete',
              C1_LINHA_ANTIGO, C1_LINHA_NOVO, C1_FAMILIA),
    ]


# ---------------------------------------------------------------------------------------------------------------------
# C2: a frase da sugestão «continua», no banco de frases de cada página (cidade, «completo»).
C2_FAMILIA = ('Família C2 (frase da sugestão «continua»): com as missões todas feitas, a frase diz o nome novo da secção, «Ler a '
              'cidade».')
C2_ANTIGO = 'A cidade antes da aula: {nmissoes} missões feitas, relê o teu caderno'
C2_NOVO = 'Ler a cidade: {nmissoes} missões feitas, relê o teu caderno'


def frase():
    trocas = []
    for rel in paginas_com(C2_ANTIGO):
        texto = base(rel)
        assert texto.count(C2_NOVO) == 0, rel
        trocas.append(troca(rel, texto, 'C2, frase da sugestão «continua» (cidade, missões todas feitas): o nome novo', C2_ANTIGO,
                            C2_NOVO, C2_FAMILIA, texto.count(C2_ANTIGO)))
    return trocas


# ---------------------------------------------------------------------------------------------------------------------
# C3: as outras formas do nome antigo, visíveis ou lidas em voz alta.
C3_FAMILIA = ('Família C3 (outras formas do nome antigo, visíveis ou lidas em voz alta): o título, a marca e o rótulo do cartão de '
              'sugestão e a ligação da lista «todos» passam a «Ler a cidade».')
C3_TROCAS = [
    # (ficheiros, local, antigo, novo)
    (('m2/gram-subordinadas/index.html',), 'C3, cartão de sugestão (versão antiga): o título',
     '{"titulo":"A cidade antes da aula","texto":"Um mapa do bairro', '{"titulo":"Ler a cidade","texto":"Um mapa do bairro'),
    (('m2/gram-subordinadas/index.html',), 'C3, cartão de sugestão (versão antiga): a marca',
     '"A EPI · a cidade antes da aula"', '"A EPI · Ler a cidade"'),
    (('m2/gram-subordinadas/index.html',), 'C3, cartão de sugestão (versão antiga): o rótulo «Sugestão: …» lido em voz alta',
     '"Atlas Lusófono":"A cidade antes da aula")', '"Atlas Lusófono":"Ler a cidade")'),
    (('1/todos/index.html', '2/todos/index.html', '3/todos/index.html'), 'C3, lista «todos» do ano: a ligação para a secção',
     f'<a href="{LENTE_CIDADE}">A cidade antes da aula<small>percurso extra',
     f'<a href="{LENTE_CIDADE}">Ler a cidade<small>percurso extra'),
]


def outras_formas():
    trocas = []
    for ficheiros, local, antigo, novo in C3_TROCAS:
        for rel in ficheiros:
            texto = base(rel)
            assert texto.count(novo) == 0, (rel, local)
            trocas.append(troca(rel, texto, local, antigo, novo, C3_FAMILIA))
    return trocas


FAMILIAS = [entrada, frase, outras_formas]


def construir():
    """As trocas da camada, ficheiro a ficheiro (pela ordem das famílias dentro de cada ficheiro)."""
    trocas = []
    for familia in FAMILIAS:
        trocas += familia()
    for t in trocas:
        assert base(t['ficheiro']).count(t['antigo']) == t['ocorrencias'], t['local']
    ordem = {id(t): i for i, t in enumerate(trocas)}
    trocas.sort(key=lambda t: (t['ficheiro'], ordem[id(t)]))
    # No fim, nenhuma página publicada (HTML e JS servidos), fora da do endereço antigo, fica com o nome antigo.
    restos = {}
    for t in trocas:
        restos.setdefault(t['ficheiro'], base(t['ficheiro']))
    for rel in list(restos):
        for t in trocas:
            if t['ficheiro'] == rel:
                restos[rel] = restos[rel].replace(t['antigo'], t['novo'])
    for rel in publicadas():
        texto = restos.get(rel, base(rel))
        assert 'cidade antes da aula' not in texto.lower(), rel
    return trocas


def main():
    trocas = construir()
    CAMADA.write_text(json.dumps(trocas, ensure_ascii=False, indent=1) + '\n', 'utf-8', newline='\n')
    print(f'{len(trocas)} trocas em {len({t["ficheiro"] for t in trocas})} ficheiros')


if __name__ == '__main__':
    main()
