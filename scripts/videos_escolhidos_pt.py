"""Vídeos escolhidos (28/10/2026) nas lições do Português.

Lê docs/pedagogia/videos-escolhidos-pt-20261028.json e acrescenta cada vídeo no fim de um cartão de
leitura que já existe (componente .yt de assets/pt-lessons/video-youtube.js). Os índices dos cartões não
mudam: painéis, relâmpagos e progresso ficam iguais. Só o cartão alterado é reescrito, com a mesma
serialização compacta. Idempotente: o bloco com o mesmo data-pv sai antes de voltar a entrar.

Uso: python3 scripts/videos_escolhidos_pt.py [--verificar]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs' / 'pedagogia' / 'videos-escolhidos-pt-20261028.json'
SCRIPT = '<script defer src="../../assets/pt-lessons/video-youtube.js"></script>'
ANCORA_SCRIPT = '@media print{.amp-ov{display:none}}</style>'
ID = re.compile(r'^[A-Za-z0-9_-]{11}$')


def cartoes(s):
    m = re.search(r'CARTOES\s*=\s*\[', s)
    if not m:
        raise ValueError('sem CARTOES')
    dec, p, out = json.JSONDecoder(), m.end(), []
    while True:
        while s[p] in ' ,\n\r\t':
            p += 1
        if s[p] == ']':
            return out
        obj, fim = dec.raw_decode(s, p)
        out.append((obj, p, fim))
        p = fim


def bloco(v):
    e = lambda t: html.escape(t, quote=True)
    url = 'https://www.youtube.com/watch?v=' + v['yt']
    return ('<div class="yt" data-pv="%s" data-yt="%s" data-titulo="%s"><button type="button" class="yt-abrir" data-yt-abrir>%s</button>'
            '<p class="yt-cred"><b>Antes de ver:</b> %s</p><p class="yt-cred"><b>No caderno:</b> %s</p>'
            '<p class="yt-cred">%s <a href="%s" target="_blank" rel="noopener">Ver no YouTube</a>.</p></div>') % (
        e(v['id']), v['yt'], e(v['titulo']), e(v['botao']), e(v['antes']), e(v['caderno']), e(v['credito']), url)


def aplicar(s, vs):
    for v in vs:
        itens = cartoes(s)
        (campo, valor), = v['cartao'].items()
        alvo = [(o, i, f) for o, i, f in itens if o.get('t') == 'ler' and (o.get(campo) or '').strip() == valor]
        if len(alvo) != 1:
            raise ValueError('%s: cartão %s=%r encontrado %d vezes' % (v['id'], campo, valor, len(alvo)))
        o, i, f = alvo[0]
        h = re.sub(r'<div class="yt" data-pv="%s".*?</div>' % re.escape(v['id']), '', o['html'], flags=re.S)
        o = dict(o, html=h + bloco(v))
        s = s[:i] + json.dumps(o, ensure_ascii=False, separators=(',', ':')) + s[f:]
    if 'video-youtube.js' not in s:
        if ANCORA_SCRIPT not in s:
            raise ValueError('sem lugar para o script do vídeo')
        s = s.replace(ANCORA_SCRIPT, ANCORA_SCRIPT + SCRIPT, 1)
    return s


def verificar(dados):
    erros = []
    por_pagina = {}
    for v in dados['videos']:
        por_pagina.setdefault(v['pagina'], []).append(v)
        if not ID.match(v['yt']):
            erros.append(v['id'] + ': id inválido')
        texto = ' '.join(v[k] for k in ('botao', 'antes', 'caderno', 'credito')).lower()
        for w in ('professor', 'jogar', 'ficha', 'folha'):
            if re.search(r'\b' + w, texto):
                erros.append('%s: «%s»' % (v['id'], w))
        if '—' in texto or '·' in texto:
            erros.append(v['id'] + ': travessão ou ponto médio')
    return erros, por_pagina


def main():
    dados = json.loads(DADOS.read_text('utf-8'))
    erros, por_pagina = verificar(dados)
    if erros:
        print('\n'.join(erros))
        sys.exit(1)
    mudou = []
    for pagina, vs in por_pagina.items():
        p = ROOT / pagina
        s = p.read_text('utf-8')
        novo = aplicar(s, vs)
        if novo != s:
            mudou.append(pagina)
            if '--verificar' not in sys.argv:
                p.write_text(novo, 'utf-8')
    if '--verificar' in sys.argv and mudou:
        print('Por aplicar: ' + ', '.join(mudou))
        sys.exit(1)
    print('%d vídeos em %d lições%s' % (len(dados['videos']), len(por_pagina), (': ' + ', '.join(mudou)) if mudou else ' (sem mudanças)'))


if __name__ == '__main__':
    main()
