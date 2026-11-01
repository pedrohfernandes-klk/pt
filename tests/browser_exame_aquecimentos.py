"""01/11/2026: todos os cartões, ajuda, progresso, projeção e larguras de ecrã."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_provas_cartoes import Quiet, nova, responder, sem_desvio, dentro_do_cartao

ROOT = Path(__file__).resolve().parents[1]
BANKS = [json.loads(p.read_text('utf-8')) for p in sorted((ROOT / 'docs/pedagogia/exame-aquecimentos').glob('s*.json'))]
HELP = {'escolha':'escolher', 'vf':'verdadeiro-falso', 'emparelhar':'ligar-pares', 'ordenar':'ordenar', 'versos':'ordenar', 'completar':'completar', 'sublinhar':'tocar-palavras'}


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for width in (320, 390, 1366):
                ctx, page, errors = nova(browser, width)
                page.route('https://pedrohfernandes-klk.github.io/pt/como/**', lambda r: r.abort())
                seen_help = set()
                for d in BANKS:
                    sid = d['sessao']; target = host + '/exame/aquecimentos/' + sid + '/'
                    page.goto(target, wait_until='networkidle')
                    page.locator('#baralho .cartao').wait_for()
                    for k, c in enumerate(d['cartoes']):
                        where = f'{sid}, cartão {k + 1}, {width}px'
                        sem_desvio(page, where); dentro_do_cartao(page, where)
                        if c['t'] != 'ler':
                            help_name = HELP[c['t']]
                            if c['t'] == 'emparelhar' and len({p[1] for p in c['pares']}) < len(c['pares']):
                                help_name = 'ligar-lados'
                            if help_name not in seen_help:
                                page.locator('[data-c-como]').click()
                                assert page.locator('.casca-video source').first.get_attribute('src').endswith('/'+help_name+'.mp4'), where
                                page.locator('[data-fechar-como]').first.click()
                                seen_help.add(help_name)
                        responder(page, k, c, where)
                    state = page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))', 'aquecimento-exame-'+sid)
                    assert state['lida'] and state['total'] == 12 and state['certas'] == 12, (sid, state)
                    assert page.locator('[data-licao-seguinte]').get_attribute('href').endswith('#'+sid+'/ler')
                    page.reload(wait_until='networkidle')
                    assert 'Já feita' in page.locator('#baralho').text_content(), (sid, page.locator('#baralho').text_content()[:250], page.evaluate('(k)=>localStorage.getItem(k)', 'aquecimento-exame-'+sid))
                    page.goto(target+'?recomecar=1', wait_until='networkidle')
                    assert 'Já feita' not in page.locator('#baralho').text_content()
                    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).melhor', 'aquecimento-exame-'+sid) == 12
                    print('PASS', sid, width, '12 cartões, ajuda e progresso', flush=True)
                assert not errors, errors
                ctx.close()
            # Retorno da alternativa escolhida, incluindo uma só lacuna errada.
            ctx, page, errors = nova(browser, 390)
            d = BANKS[19]
            page.goto(host+'/exame/aquecimentos/s20/', wait_until='networkidle')
            page.locator('#baralho .op[data-j="1"]').click()
            assert d['cartoes'][0]['fe'][1] in page.locator('[data-c-folha]').text_content()
            page.locator('[data-c-folha] [data-seguinte]').click()
            for k, c in enumerate(d['cartoes'][1:5], 1):
                responder(page, k, c, 'retorno s20')
            c = d['cartoes'][5]
            assert c['t'] == 'completar'
            page.locator('select[data-k="0"]').select_option('1')
            page.locator('select[data-k="1"]').select_option('0')
            feedback = page.locator('[data-c-folha]').text_content()
            assert c['lacunas'][0]['fe'][1] in feedback
            assert c['lacunas'][1]['fe'][1] not in feedback
            assert not errors, errors
            ctx.close()
            # Projeção: dados privados sem alteração e resposta pública do motor.
            ctx, page, errors = nova(browser, 390)
            page.add_init_script("localStorage.setItem('licao-m7-f02','privado');localStorage.setItem('aquecimento-exame-s12',JSON.stringify({lida:true,melhor:999,tentativas:4}));window.__writes=[];const put=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){window.__writes.push(k);return put.call(this,k,v)}")
            page.goto(host+'/exame/aquecimentos/s12/?projetar=1', wait_until='networkidle')
            assert '999' not in page.locator('#baralho').text_content()
            for c in BANKS[11]['cartoes']:
                if c['t']=='ler': page.locator('[data-c-acoes] [data-seguinte]').click()
                else:
                    page.get_by_role('button', name='Mostrar resposta', exact=True).click()
                    page.locator('[data-c-folha] [data-seguinte]').click()
            assert page.evaluate('window.__writes') == []
            assert '?projetar=1#s12/ler' in page.locator('[data-licao-seguinte]').get_attribute('href')
            assert not errors, errors
            ctx.close(); browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
