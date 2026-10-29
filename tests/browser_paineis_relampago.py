"""Painéis corrigidos (27/10/2026): cada pergunta-relâmpago abre, na lição, o exercício que o painel anuncia.

O aluno entra numa sala local (modo `?local`, canal BroadcastChannel, como na aula sem rede); outra página
envia pelo mesmo canal a mensagem do painel ({t:"relampago",k}). Confere-se que a lição abre a sobreposição
«Relâmpago» com o enunciado do painel, no telemóvel, sem erros.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json,re,threading,time
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler
from test_paineis_cartoes import CORRIGIDOS,banco

def limpo(t):return re.sub(r'\s+',' ',re.sub(r'[«»…]',' ',t)).strip().lower()

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True)
            for pasta in CORRIGIDOS:
                P=banco((ROOT/pasta/'index.html').read_text('utf-8'));licao=pasta.replace('painel-','licao-')
                ctx=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
                ctx.add_init_script('localStorage.setItem("epi-sala",JSON.stringify({cod:"QATST",alc:"Ana",t:Date.now()}))')
                ctx.route('**/fonts.g*/**',lambda r:r.abort())
                aluno=ctx.new_page();erros=[];aluno.on('pageerror',lambda e:erros.append(str(e)))
                aluno.goto(host+'/'+licao+'/?local',wait_until='networkidle')
                painel=ctx.new_page();painel.goto(host+'/'+pasta+'/?local',wait_until='networkidle')
                for c in P:
                    painel.evaluate('m=>new BroadcastChannel("epi-pt-QATST").postMessage(JSON.stringify(m))',{'t':'relampago','k':c['k'],'s':60,'id':'qa'+str(c['k']),'ts':int(time.time()*1000)})
                    aluno.wait_for_function('()=>window.REL&&[...document.querySelectorAll(".casca")].some(e=>/rel[aâ]mpago/i.test(e.innerText))')
                    texto=aluno.evaluate('()=>{const l=[...document.querySelectorAll(".casca")].filter(e=>/rel[aâ]mpago/i.test(e.innerText));return l[l.length-1].innerText}')
                    alvo=limpo(c['p'].split('…')[0])[:28]  # nos cartões de completar, as lacunas intercalam as opções
                    assert alvo in limpo(texto),(pasta,c['k'],alvo,texto[:300])
                    aluno.evaluate('()=>{try{REL.fechar()}catch(e){};window.REL=null}')
                assert not erros,(pasta,erros)
                print('PASS',pasta,len(P),'perguntas abrem na lição',flush=True);ctx.close()
            b.close()
    finally:server.shutdown()
if __name__=='__main__':main()
