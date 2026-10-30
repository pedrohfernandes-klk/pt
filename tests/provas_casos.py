"""Provas em cartões: um caso por transcrição conferida (30/10/2026).

Cada tests/fixtures/prova-639-AAAA-Nf-vN.json é uma prova publicada: as lições estão em exame/provas/AAAA-Nf/grupo-*/, as
chaves do progresso são prova-AAAA-Nf-gN e os parâmetros (versão da lição, imagem com direitos, ligações) estão em
scripts/provas/dados/AAAA-Nf/prova.json. tests/test_provas_cartoes.py e tests/browser_provas_cartoes.py correm um caso
por fixture com estas peças; para juntar uma prova, basta a fixture, os dados e as páginas geradas.

A numeração das linhas nas lições (data-l de cada span.ln): o número da linha na prosa e «v» mais o número do verso nas
estrofes. Se um grupo tiver dois textos numerados de forma independente (por exemplo, dois poemas, cada um a partir do
verso 1), prova.json diz o prefixo de cada um em «prefixos_data_l» ({id do texto: prefixo}); o teste falha se dois
textos derem o mesmo data-l.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards  # noqa: E402

FIXTURES = ROOT / 'tests/fixtures'
DADOS = ROOT / 'scripts/provas/dados'
SECCAO = ROOT / 'exame/provas/index.html'
RE_FIXTURE = re.compile(r'^prova-(\d{3})-(\d{4})-(\d)f-v(\d)\.json$')
ROMANOS = ['I', 'II', 'III', 'IV', 'V']


def plano(s):
    """Texto simples: sem etiquetas, sem a marcação dos dados (_itálico_, **negrito**, [^n]), espaços normalizados."""
    s = re.sub(r'<sup>\d+</sup>', '', s)
    s = re.sub(r'</?(?:i|b|em|strong|span|a|sub|small|cite)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\[\^\d+\]', '', s).replace('**', '')
    s = re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def textos(x):
    """As cadeias de um objeto da transcrição, sem as chaves «_…» nem os campos nossos («…nossa…»)."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from textos(y)
    elif isinstance(x, dict):
        for k, y in x.items():
            if not k.startswith('_') and 'nossa' not in k:
                yield from textos(y)


def textos_do_grupo(gfx):
    return list(gfx.get('textos', [])) + [t for p in gfx.get('partes', []) for t in p.get('textos', [])]


def itens_do_grupo(gfx):
    """(item, textos ao alcance do item: os da parte, ou os do grupo quando não há partes)."""
    if gfx.get('partes'):
        return [(i, p.get('textos', [])) for p in gfx['partes'] for i in p.get('itens', [])]
    return [(i, gfx.get('textos', [])) for i in gfx.get('itens', [])]


def imagem_do_grupo(gfx):
    for it, _ in itens_do_grupo(gfx):
        if it.get('imagem'):
            return it['imagem']
    return gfx.get('imagem')


class Prova:
    def __init__(self, caminho):
        m = RE_FIXTURE.match(caminho.name)
        assert m, caminho.name
        self.fixture = caminho
        self.codigo, ano, fase, versao = m.groups()
        self.ano, self.fase, self.versao = int(ano), int(fase), int(versao)
        self.pasta = f'{self.ano}-{self.fase}f'
        self.id = f'{self.pasta}-v{self.versao}'
        self.fx = json.loads(caminho.read_text('utf-8'))
        cfg = DADOS / self.pasta / 'prova.json'
        self.cfg = json.loads(cfg.read_text('utf-8')) if cfg.is_file() else None
        self.nome = f'Prova {self.codigo}, {self.fase}.ª fase, {self.ano}'
        self.grupos = {g: 'grupo-' + ROMANOS[g - 1].lower() for g in range(1, len(self.fx['grupos']) + 1)}
        self.paginas = {g: ROOT / 'exame/provas' / self.pasta / slug / 'index.html' for g, slug in self.grupos.items()}
        fontes = self.fx['prova']['fontes']
        self.url_enunciado, self.url_criterios = fontes['enunciado_url'], fontes['criterios_url']
        self.corpus = ' \n '.join(plano(t) for t in textos({k: v for k, v in self.fx.items() if k != '_sobre'}))
        self.fontes_textos = [t['fonte'] for gfx in self.fx['grupos'] for t in textos_do_grupo(gfx)]
        self._cartoes = {}

    def __repr__(self):
        return f'Prova({self.id})'

    def chave(self, g):
        return f'prova-{self.pasta}-g{g}'

    def versao_licao(self, g):
        return self.cfg['grupos'][g - 1].get('versao_licao', self.cfg['versao_licao'])

    def cartoes(self, g):
        if g not in self._cartoes:
            self._cartoes[g] = lesson_cards(self.paginas[g])
        return self._cartoes[g]

    def imagem(self):
        """Os parâmetros da imagem com direitos (grupo, página do PDF, se se reproduz), ou None."""
        return (self.cfg or {}).get('imagem')

    def autor_nao_iave(self):
        """A instituição que a transcrição dá como autora, quando não é o IAVE (2026: a EduQA), ou None."""
        a = self.fx['prova'].get('autor_instituicao') or ''
        return None if not a or 'IAVE' in a else a

    # ---------- o que é oficial e o que é nosso ----------
    def oficial(self, trecho):
        t = plano(trecho)
        return bool(t) and t in self.corpus

    def nosso(self, texto):
        """O texto que escrevemos: sem as referências dos textos, como a prova as dá, nem as citações «…» que são da
        prova ou dos critérios (uma citação com «[…]» conta se cada pedaço for da prova)."""
        t = plano(texto)
        for f in self.fontes_textos:
            t = t.replace(plano(f).rstrip('.'), ' ')
        return re.sub(r'«([^«»]*)»', lambda m: ' ' if all(self.oficial(x) or not x.strip() for x in m.group(1).split('[…]')) else m.group(0), t)

    # ---------- a numeração da prova ----------
    def linhas_da_prova(self):
        """{grupo: {data-l: texto da linha na transcrição}}, para os grupos com textos."""
        prefixos = (self.cfg or {}).get('prefixos_data_l', {})
        out = {}
        for g, gfx in enumerate(self.fx['grupos'], 1):
            ts = textos_do_grupo(gfx)
            if not ts:
                continue
            out[g] = {}
            for t in ts:
                for linha in t.get('linhas', []):
                    k = prefixos.get(t.get('id'), '') + str(linha['n'])
                    assert k not in out[g], f'{self.id}, grupo {g}: data-l «{k}» repetido; diz o prefixo em prefixos_data_l'
                    out[g][k] = linha['t']
                for estrofe in t.get('estrofes', []):
                    for v in estrofe:
                        k = prefixos.get(t.get('id'), 'v') + str(v['v'])
                        assert k not in out[g], f'{self.id}, grupo {g}: data-l «{k}» repetido; diz o prefixo em prefixos_data_l'
                        out[g][k] = v['t']
        return out


def provas():
    """Um caso por fixture, da prova mais recente para a mais antiga (a ordem da secção)."""
    ps = [Prova(p) for p in FIXTURES.glob('prova-*-*-*f-v*.json')]
    return sorted(ps, key=lambda P: (P.ano, P.fase), reverse=True)


PROVAS = provas()
