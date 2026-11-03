"""03/11/2026: documento do aluno, gerado sem respostas nem estado do motor.

Uso: python scripts/cartoes_papel.py dados.json --saida atividade.html
Aceita uma lista de cartões ou um objeto com titulo e cartoes. Os tipos
suportados são os registados em tipos_regras, incluindo extensões integradas.
Não publica páginas nem altera os dados recebidos.
"""
import argparse
from html import escape
import json
from pathlib import Path
import re
import tipos_regras as regras


def texto(s):
    """As únicas marcas aceites são as de ênfase do motor, após escapar HTML."""
    s = escape(s)
    s = re.sub(r'\*\*([^*\n]{1,80})\*\*', r'<b>\1</b>', s)
    return re.sub(r'(^|[^\w/])_([^_\n<>]{1,100})_(?!\w)', r'\1<i>\2</i>', s)


CSS = '''
:root{color-scheme:light;color:#20201d;background:#f6f3e9;font:18px/1.5 Arial,Helvetica,sans-serif}
*{box-sizing:border-box}body{margin:0}main{max-width:780px;margin:auto;padding:24px}
h1{font-size:1.8rem;line-height:1.15;margin:0 0 16px}h2{font-size:1.12rem;line-height:1.4;margin:0 0 12px}
.cartao-papel{border-top:2px solid;padding:20px 0;break-inside:avoid-page;overflow-wrap:anywhere}
.numero{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 8px}
.dica{font-size:.9rem;margin:12px 0;color:#494941}.material p{margin:10px 0}
.material ol{padding-left:1.8em}.material li{padding:3px 0;break-inside:avoid}
.material img{display:block;max-width:100%;max-height:190px;object-fit:contain}
.material figure{margin:0}.material figcaption{font:13px/1.4 Arial,sans-serif;margin:6px 0 12px}
.mat-versos>p{margin:0;padding-left:1.4em;text-indent:-1.4em}
.mat-marcas,.mat-sinais{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0!important}
.mat-marcas li,.mat-sinais li{border:1px solid;padding:4px 8px}
@page{size:A4;margin:17mm}
@media(max-width:400px){main{padding:16px}h1{font-size:1.5rem}}
@media print{:root,body{background:white;color:black;font-size:11pt}main{max-width:none;padding:0}h1{font-size:19pt}.dica{color:black}a{color:inherit;text-decoration:none}}
'''


def pagina(cartoes, titulo='Português: observar e responder', base_url=None):
    """Página final para imprimir; só enunciado, dica e material público.

    A validação ocorre antes da renderização e a entrada não é serializada
    para HTML/JS. O documento não contém chaves de correção escondidas.
    """
    if not isinstance(cartoes, list) or not cartoes:
        raise ValueError('É necessária uma lista de cartões.')
    ids = set()
    blocos = []
    for n, c in enumerate(cartoes, 1):
        if not isinstance(c, dict) or c.get('t') not in regras.ENTROU:
            raise ValueError(f'Cartão {n}: tipo não registado para papel.')
        erros = regras.validar(c, 'licao')
        if erros:
            raise ValueError(f'Cartão {n}: ' + '; '.join(erros))
        if c['id'] in ids:
            raise ValueError('ID repetido: ' + c['id'])
        ids.add(c['id'])
        blocos.append('<section class="cartao-papel" data-cartao="'+escape(c['id'],quote=True)+'">'
                      '<p class="numero">Atividade '+str(n)+'</p><h2 class="pedido">'+texto(c['p'])+'</h2>'
                      '<p class="dica">'+texto(regras.DICAS_PAPEL[c['t']])+'</p>'
                      '<div class="material">'+regras.material_html(c,c['id'])+'</div></section>')
    base = '<base href="'+escape(base_url,quote=True)+'">' if base_url else ''
    return '<!doctype html><html lang="pt-PT"><head><meta charset="utf-8">'+base+\
           '<meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(titulo)+\
           '</title><style>'+CSS+'</style></head><body><main><h1>'+texto(titulo)+'</h1>'+\
           ''.join(blocos)+'</main></body></html>\n'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('dados',type=Path)
    ap.add_argument('--saida',required=True,type=Path)
    ap.add_argument('--base-url',help='Raiz pública para resolver imagens, quando existam.')
    args=ap.parse_args()
    dados=json.loads(args.dados.read_text(encoding='utf-8'))
    cards=dados if isinstance(dados,list) else dados['cartoes']
    titulo='Português: observar e responder' if isinstance(dados,list) else dados.get('titulo','Português: observar e responder')
    html=pagina(cards,titulo,args.base_url)
    args.saida.parent.mkdir(parents=True,exist_ok=True)
    args.saida.write_text(html,encoding='utf-8',newline='\n')


if __name__=='__main__':main()
