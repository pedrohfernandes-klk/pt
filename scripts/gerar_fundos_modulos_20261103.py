"""03/11/2026: desenhos próprios a traço e camada literal dos pilotos M4/M6.

Grafismos construídos em SVG com recurso a IA, sem reproduzir imagens documentais.
Este gerador prepara as trocas; aplicar_trocas.py aplica-as e gera o manifesto.
"""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

def svg(body):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 640" fill="none" stroke="#716b5d" stroke-width="1.5">' + body + '</svg>\n'

fish = '<defs><g id="peixe"><path d="M0 0C30-26 70-26 104 0C70 26 30 26 0 0L-24-18V18Z"/><path d="M62-17Q48 0 62 17M28-17L42-30L60-21M30 18L42 28L56 21"/><circle cx="82" cy="-3" r="2"/><path d="M18-4Q36-10 48-5M18 4Q36 10 48 5"/></g></defs>'
for x,y,s in [(650,75,.9),(810,150,1.1),(565,224,.75),(735,298,1.3),(905,390,.9),(560,440,1.05),(760,535,.8),(930,600,1.1)]:
    fish += f'<use href="#peixe" transform="translate({x} {y}) scale({s})"/>'
for y in (110,260,420,570):
    fish += f'<path opacity=".35" d="M390 {y}Q550 {y-36} 700 {y}T1010 {y}"/>'
(ASSETS/'fundo-m4-cardume.svg').write_text(svg(fish),encoding='utf-8',newline='\n')

street = '<path d="M450 608H960M510 630L790 390L960 470M450 580L760 365"/>'
for x,y,w,h in [(450,90,125,450),(585,160,110,360),(705,55,145,445),(860,130,110,420)]:
    street += f'<path d="M{x} {y+h}V{y}H{x+w}V{y+h}M{x-8} {y}H{x+w+8}M{x} {y+12}H{x+w}"/>'
    for row in range(4):
        for col in range(2):
            xx=x+18+col*(w-36)/2; yy=y+40+row*79
            street += f'<path d="M{xx} {yy+48}V{yy}H{xx+25}V{yy+48}ZM{xx+12} {yy}V{yy+48}M{xx} {yy+24}H{xx+25}"/>'
    street += f'<path d="M{x+w/2-16} {y+h}V{y+h-58}Q{x+w/2} {y+h-75} {x+w/2+16} {y+h-58}V{y+h}"/>'
(ASSETS/'fundo-m6-cidade.svg').write_text(svg(street),encoding='utf-8',newline='\n')

layer=[]
for m,motif,label in [(4,'cardume','Peixes e escuta, a partir do sermão de Vieira'),(6,'cidade','Rua e luz, a partir da poesia de Cesário Verde')]:
    rel=f'm{m}/index.html'
    changes=[('</head>','<link rel="stylesheet" href="../assets/fundos-modulos.css?v=20261103"><script defer src="../assets/fundos.js?v=20261102"></script></head>'),
      ('<header class="topo">',f'<header class="topo" data-fundo="fm{m}" data-fundo-ciclo="32"><div class="fm-desenho fm-{motif}" aria-hidden="true"><span class="fm-traco"></span><span class="fm-luz"></span></div>'),
      ('class="cz-motion-title"','class="fm-titulo"'),
      ('class="cz-motion-part"','class="fm-titulo-parte"'),
      ('<!-- id="podcast":',f'<div class="fm-legenda"><small>{label}. Grafismo gerado com recurso a IA.</small><button type="button" data-fundo-botao="fm{m}" hidden>Parar o desenho</button></div><!-- id="podcast":')]
    for old,new in changes:
        layer.append(dict(ficheiro=rel,local=f'M{m}: fundo {motif}',antigo=old,novo=new,ocorrencias=1,achado='03/11/2026: piloto isolado, título e ação imóveis; motor comum e crédito explícito.'))
(ROOT/'scripts/fundos_modulos_20261103.json').write_text(json.dumps(layer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
