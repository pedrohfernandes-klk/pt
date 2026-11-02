"""02/11/2026: ensaio gerado do contrato F2/F3 contra o motor real, sem página publicada."""
from pathlib import Path
from urllib.parse import urlsplit
import mimetypes
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = '''<!doctype html><html lang="pt-PT"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="/assets/pt-lessons/lesson.css">
<link rel="stylesheet" href="/assets/pt-lessons/tipos-mais.css">
<script src="/assets/pt-lessons/casca.js"></script>
<script src="/assets/pt-lessons/jogo.js"></script>
<script src="/assets/pt-lessons/tipos-mais.js"></script>
</head><body><script>
window.CARTOES=[1,2].map(n=>({t:'ensaio_f3',id:'ensaio-'+n,p:'Que indício distingue as duas leituras?',f:'O indício tem de distinguir as leituras, não apenas repetir o tema.',fe:'original',texto:'Duas leituras possíveis.'}));
window.antes=JSON.stringify(CARTOES);
window.contextos=[];
EPITiposMais.registar('ensaio_f3',{rot:'Ensaio do contrato',como:'marcar-texto',criar(x,api,ctx){
 let escolhido=null;
 contextos.push({id:x.id,repeticao:ctx.repeticao,falhas:ctx.falhas,projecao:ctx.projecao});
 function marcar(n){escolhido=n;api.el.querySelectorAll('[data-ensaio]').forEach(b=>{const s=Number(b.dataset.ensaio)===n;b.classList.toggle('sel',s);b.setAttribute('aria-pressed',String(s))});ctx.atualizar(true,'Uma opção escolhida.')}
 function resultado(n){marcar(n);const b=api.el.querySelector('[data-ensaio="'+n+'"]');b.classList.add(n===0?'bom':'mau');api.el.querySelector('[data-ensaio-check]').checked=true;return {ok:n===0,certas:n===0?1:0,total:1,erros:n===0?[]:['Confundes o tema com o indício. Relê a palavra que distingue as leituras.'],falhas:n===0?[]:[1]}}
 return {html(){return '<p class="q">'+api.it(x.p)+'</p><p class="dica">Escolhe uma leitura e confirma.</p><p data-variante>'+ (ctx.repeticao?'Revê só o indício falhado.':'Compara os dois indícios.') +'</p><button class="tm-r uma" type="button" data-ensaio="0" aria-pressed="false">Indício que distingue</button><button class="tm-r uma" type="button" data-ensaio="1" aria-pressed="false">Tema que se repete</button><input type="checkbox" data-ensaio-check aria-label="Estado de ensaio" tabindex="-1" hidden><p class="tm-conta"></p><p class="tm-viva c-sr" aria-live="polite"></p>'},
 ligar(){api.el.querySelectorAll('[data-ensaio]').forEach(b=>b.onclick=()=>marcar(Number(b.dataset.ensaio)));ctx.atualizar(false,'Falta escolher uma opção.')},
 confirmar(){return resultado(escolhido)},revelar(){return resultado(0)}};
}});
window.C=EPICasca.abrir({marca:'Ensaio',semVoltar:true});
EPIJogo.montar({casca:C,itens:CARTOES,chave:'ensaio-contrato',variar:false,pistas:['Procura o indício que distingue.','Conta as sílabas do verso.']});
</script></body></html>'''


def route_local(route):
    path = urlsplit(route.request.url).path
    if path == '/ensaio/':
        route.fulfill(body=HTML, content_type='text/html; charset=utf-8')
        return
    f = (ROOT/path.lstrip('/')).resolve()
    if f.is_relative_to(ROOT) and f.is_file():
        route.fulfill(path=str(f), content_type=mimetypes.guess_type(f)[0] or 'application/octet-stream')
    else:
        route.fulfill(status=404, body='Not found')


def main():
    n = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width, scheme in [(320,'light'),(390,'dark'),(1024,'light'),(1366,'dark')]:
            for projection in (False, True):
                context = browser.new_context(viewport={'width':width,'height':768},color_scheme=scheme,reduced_motion='no-preference')
                page = context.new_page()
                page.route('**/*',route_local)
                errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto('https://tipos.test/ensaio/'+('?projetar=1' if projection else ''))
                page.locator('[data-confirmar]').wait_for()
                assert page.locator('[data-confirmar]').is_disabled()
                labels=page.locator('[data-c-acoes] button').all_text_contents()
                assert labels==(['Pista','Mostrar resposta','Confirmar'] if projection else ['Pista','Confirmar']),labels
                page.locator('[data-pista-ess]').click()
                assert page.locator('.pista').inner_text()=='Pista: Procura o indício que distingue.'
                assert page.locator('[data-pista-ess]').is_disabled()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                assert page.locator('[data-tipo-ext]').evaluate('(e)=>e.getAnimations({subtree:true}).length')==0
                for b in page.locator('[data-ensaio]').all():
                    assert b.bounding_box()['height']>=48
                if projection:
                    before=page.evaluate('JSON.stringify(localStorage)')
                    page.keyboard.press('r')
                    assert page.locator('[data-c-folha] .c-veredito').inner_text()=='✓\nResposta'
                    assert page.locator('[data-c-folha] .c-pts').count()==0
                    assert page.locator('.cartao .f-rev b').inner_text()=='Resposta:'
                else:
                    page.locator('[data-ensaio="0"]').focus()
                    page.keyboard.press('Enter')
                    assert page.locator('.tm-conta').inner_text()=='Uma opção escolhida.'
                    page.locator('[data-confirmar]').focus()
                    page.keyboard.press('Enter')
                    assert 'Acertaste 1 de 1.' in page.locator('[data-c-folha]').inner_text()
                assert page.evaluate('JSON.stringify(CARTOES)===antes')
                page.locator('[data-c-folha] [data-seguinte]').click()
                page.locator('[data-volta]').click()
                assert page.locator('[data-ensaio-check]').get_attribute('checked') is not None
                assert page.locator('[data-ensaio="0"]').get_attribute('aria-pressed')=='true'
                assert page.locator('[data-ensaio]:enabled').count()==0
                if projection:
                    assert page.locator('.cartao .f-rev b').inner_text()=='Resposta:'
                page.locator('[data-rv="sai"]').click()
                if projection:
                    page.locator('[data-mostrar]').click()
                    page.locator('[data-c-folha] [data-seguinte]').click()
                    assert page.evaluate('JSON.stringify(localStorage)')==before
                    assert page.locator('.cartao.fim .grande').inner_text()=='Fim da lição.'
                else:
                    page.locator('[data-ensaio="1"]').click()
                    page.locator('[data-confirmar]').click()
                    assert 'Confundes o tema com o indício.' in page.locator('[data-c-folha]').inner_text()
                    assert page.evaluate('JSON.stringify(CARTOES)===antes')
                    page.locator('[data-c-folha] [data-seguinte]').click()
                    page.locator('[data-errados]').click()
                    assert page.locator('[data-variante]').inner_text()=='Revê só o indício falhado.'
                    assert page.evaluate('contextos[contextos.length-1].falhas')==[1]
                    assert page.evaluate('contextos[contextos.length-1].repeticao') is True
                assert errors==[],errors
                n+=1
                context.close()
        browser.close()
    print(f'PASS {n} cenários do adaptador: barra, pista, teclado, DOM de revisão, variante, banco intacto e projeção sem gravação')


if __name__=='__main__':
    main()
