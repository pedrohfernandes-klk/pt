"""01/11/2026: todos os cartões, ajuda, progresso, projeção e larguras de ecrã."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import os
import tempfile
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_provas_cartoes import Quiet, nova, responder, sem_desvio, dentro_do_cartao

ROOT = Path(__file__).resolve().parents[1]
BANKS = [json.loads(p.read_text('utf-8')) for p in sorted((ROOT / 'docs/pedagogia/exame-aquecimentos').glob('s*.json'))]
HELP = {'escolha':'escolher', 'vf':'verdadeiro-falso', 'emparelhar':'ligar-pares', 'ordenar':'ordenar', 'versos':'ordenar', 'completar':'completar', 'sublinhar':'tocar-palavras'}


def main():
    # 07/11/2026 (achados 1 e 50): o sítio é servido em /pt/, como no GitHub Pages; em «/», assets/projection-launcher.js
    # não atuava e o teste não via a troca das ligações de regresso por «Projetar esta página».
    raiz = tempfile.mkdtemp(prefix='exame-aquecimentos-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
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
                        # 07/11/2026 (achados 14, 37 e 70): os cartões de leitura têm rótulo próprio, nunca «Faz».
                        if c['t'] == 'ler':
                            assert page.locator('#baralho .cartao .rot').first.text_content().strip().lower() != 'faz', where
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
                    # 01/11/2026: aguardar o desenho do motor antes de verificar o estado guardado.
                    page.locator('#baralho .cartao').wait_for()
                    # 07/11/2026: o rótulo do fim concorda com «aquecimento» (revisão de 7/11, ponto 15): «Já feito», e nunca «Já feita».
                    feito = page.locator('#baralho').text_content()
                    assert 'Já feito' in feito and 'Já feita' not in feito, (sid, feito[:250], page.evaluate('(k)=>localStorage.getItem(k)', 'aquecimento-exame-'+sid))
                    page.goto(target+'?recomecar=1', wait_until='networkidle')
                    page.locator('#baralho .cartao').wait_for()
                    # 07/11/2026: «Já feito» (antes «Já feita»), nem uma forma nem a outra depois de recomeçar.
                    assert all(t not in page.locator('#baralho').text_content() for t in ('Já feito', 'Já feita'))
                    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).melhor', 'aquecimento-exame-'+sid) == 12
                    print('PASS', sid, width, '12 cartões, ajuda e progresso', flush=True)
                assert not errors, errors
                ctx.close()
            # Retorno da alternativa escolhida, incluindo uma só lacuna errada.
            ctx, page, errors = nova(browser, 390)
            d = BANKS[19]
            page.goto(host+'/exame/aquecimentos/s20/', wait_until='networkidle')
            # 07/11/2026: os bancos abrem com «Abre» e, onde há texto, «Texto de apoio»; passam-se todos os cartões de
            # leitura antes do primeiro de fazer (antes havia um só). As asserções do retorno ficam iguais.
            leitura = [c for c in d['cartoes'] if c['t'] == 'ler']
            assert leitura and d['cartoes'][:len(leitura)] == leitura
            for k, c in enumerate(leitura):
                responder(page, k, c, 'apoio s20')
            fazer = [c for c in d['cartoes'] if c['t'] != 'ler']
            page.locator('#baralho .op[data-j="1"]').click()
            assert fazer[0]['fe'][1] in page.locator('[data-c-folha]').text_content()
            page.locator('[data-c-folha] [data-seguinte]').click()
            # 07/11/2026: com os bancos reordenados (nunca três seguidos do mesmo tipo), o primeiro completar com duas
            # lacunas de s20 deixou de ser o sexto cartão; procura-se pela posição, com as mesmas asserções.
            assert fazer[0]['t'] == 'escolha'
            j = next(i for i, x in enumerate(fazer) if x['t'] == 'completar' and len(x['lacunas']) >= 2)
            for k, c in enumerate(fazer[1:j], 1):
                responder(page, len(leitura) + k, c, 'retorno s20')
            c = fazer[j]
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
            # 07/11/2026 (achados 1, 13, 50 e 70): depois de o lançador da projeção correr, o regresso e a continuação
            # continuam a ser «Voltar à sessão» e «Continuar a sessão», para a sessão projetada, sem «·» nem «Projetar»;
            # o fim diz que acabou o aquecimento. O clique em «Continuar a sessão» abre a fase Ler projetada.
            page.wait_for_timeout(500)
            ligacoes = [('.casca-topo .c-marca', 'Exame', '?projetar=1#s12/aquecer'),
                        ('[data-c-painel] [data-exame-voltar]', 'Voltar à sessão', '?projetar=1#s12/aquecer'),
                        ('[data-ao-percurso]', 'Voltar à sessão', '?projetar=1#s12/aquecer'),
                        ('[data-licao-seguinte]', 'Continuar a sessão', '?projetar=1#s12/ler')]
            for sel, texto, destino in ligacoes:
                a = page.locator(sel)
                assert a.count() == 1, sel
                assert a.text_content().strip() == texto, (sel, a.text_content())
                assert a.get_attribute('href').endswith(destino) and '/projetar/' not in a.get_attribute('href'), (sel, a.get_attribute('href'))
            assert page.locator('a', has_text='Projetar esta página').count() == 1  # só a do menu
            fim = page.locator('#baralho .cartao.fim').text_content()
            assert 'Aquecimento feito' in fim and 'Fim do aquecimento.' in fim, fim
            assert 'A aula acaba aqui' not in fim and 'Fim da lição' not in fim, fim
            page.locator('[data-licao-seguinte]').click()
            page.wait_for_url('**/pt/exame/?projetar=1#s12/ler')
            assert page.locator('h1').first.is_visible()
            assert not errors, errors
            ctx.close(); browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
