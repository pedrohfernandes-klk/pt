#!/usr/bin/env python3
"""28/10/2026: desliga a «Sala de aula em tempo real» nas páginas publicadas do pt.

Decisão do docente de 17/10/2026 (ponto 22 de DECISOES; história e código antigo em
_interno/arquivo/sala-desligada-2026-10-17.md, nas fontes): a Sala enviava a alcunha, a lição e os pontos
de cada aluno para tópicos públicos do ntfy.sh, que qualquer pessoa com o código podia ler e escrever.
Nas fontes a mudança fez-se nesse dia; aqui, no sítio publicado, faz-se agora, página a página.

O que o script faz, sempre com trocas literais (nunca reescreve uma página à mão):
- lições (m*/licao-*): saem o botão «Sala» do menu, o formulário (código e alcunha), a faixa da pausa,
  o cartão que interrompe, o envio do estado (evento do baralho) e o código que recebia pausa, relâmpago,
  votação e fecho; esc() fica, porque o «Cartão extra» a usa;
- painéis do docente (m*/painel-*): ficam o pedido em letra de cartaz, o cronómetro, o QR, a pausa, o
  relâmpago e o «Quem sou eu?» do Atlas no projetor; saem o código da sala, o placar com alcunhas, o
  sorteio, a votação, o código do aluno e todos os envios para os telemóveis. Como já não há telemóveis do
  outro lado (revisão de 28/10/2026), o projetor passa a bastar: o relâmpago mostra o material do cartão k da
  lição (opções, pares, versos, palavras, frase com lacunas), baralhado e sem a solução, e, quando o tempo acaba,
  a correção do próprio cartão (o texto f que a lição mostrava depois de responder); os enunciados que tinham
  ficado para trás passam aos da lição; o «Quem sou eu?» mostra uma pista por cada terço do tempo e
  a resposta no fim; «Voltar ao início» (I) repõe o ecrã de abertura, onde o QR cresce; a tecla A funciona;
- índices dos módulos (m1/ a m9/): sai o envio do resultado do Desafio da unidade;
- Atlas (atlas/): saem o botão «Sala de aula», o formulário e o envio para o «mapa da turma»;
- mapa da turma (atlas/sala/): passa a página curta que leva ao Atlas, como nas fontes;
- em todas estas páginas, o canal window.EPISala dá lugar à limpeza única do que a Sala deixou no
  aparelho (SALA_LIMPAR_JS de sala.mjs); a página inicial (index.html) também a corre antes de exportar
  ou repor o progresso.

Regras:
- cada bloco tem de aparecer exatamente como se conhece (uma vez); se não aparecer, ou se depois das trocas
  ainda houver marcas da Sala, o script avisa, não escreve nada e sai com erro;
- corre outra vez sem mudar nada: as páginas já desligadas reconhecem-se pela limpeza e, nas congeladas,
  o manifesto desfaz-se, refaz-se e tem de dar a página atual (o resto da página pode ter mudado depois, por
  outras trocas; se o manifesto já não se desfaz, o aviso diz isso, e não que a forma da Sala é desconhecida);
- nas páginas congeladas pelos testes (hash ou digest em tests/fixtures), as trocas ficam em
  tests/fixtures/sala-desligada-edits-20261028.json (location, old, new, occurrences), com texto novo
  nunca vazio, para os testes as desfazerem antes de comparar.

Uso:
  python3 scripts/desligar_sala.py              aplica (ou confirma que já está aplicado)
  python3 scripts/desligar_sala.py --verificar  não escreve; sai com 1 se houver alguma coisa por fazer
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFESTO = ROOT / 'tests/fixtures/sala-desligada-edits-20261028.json'
SITIO = 'https://pedrohfernandes-klk.github.io/pt'
FORA = {'.git', '.github', 'tests', 'scripts', 'docs', 'tools', 'node_modules'}

NOTA = ('28/10/2026: a Sala de aula em tempo real sai das páginas publicadas (decisão do docente de 17/10/2026; '
        'scripts/desligar_sala.py). Trocas literais pela ordem em que se aplicam; desfazem-se da última para a '
        'primeira, antes de todos os outros manifestos. Só entram aqui as páginas cujo conteúdo os testes congelam '
        '(task-route-lesson-content-before.json, module-layout-before.json, m1-grammar-pilot e apoios-tabelas); '
        '«paginas» lista todas as páginas onde a Sala existia e onde agora corre a limpeza. base_sha256_lf e '
        'after_sha256_lf registam o dia do corte e não se voltam a verificar: o script, corrido outra vez, só confirma '
        'que estas trocas se desfazem e refazem na página atual.')


class FormaDesconhecida(Exception):
    """Uma forma da Sala que o script não reconhece: avisa e não escreve nada."""


class ManifestoDesatualizado(Exception):
    """Uma página congelada já desligada onde o manifesto da Sala deixou de se desfazer e refazer."""


# ── a limpeza (cópia literal de SALA_LIMPAR_JS, _interno/modelo/sala.mjs, 17/10/2026)
SALA_LIMPAR_JS = '''(function(){try{["epi-sala","epi-sala-atlas"].forEach(function(k){if(localStorage.getItem(k)!==null)localStorage.removeItem(k)});
for(var i=localStorage.length-1;i>=0;i--){var k=localStorage.key(i);if(k&&k.indexOf("painel-sala-")===0)localStorage.removeItem(k)}}catch(x){}
try{sessionStorage.removeItem("epi-atlas-sala")}catch(x){}})();'''
LIMPEZA_COMENTARIO = ('// 28/10/2026: a Sala de aula está desligada desde 17/10/2026 (decisão do docente); '
                      'só se apaga o que ela deixou neste aparelho\n')
LIMPEZA_SCRIPT = '<script>\n' + LIMPEZA_COMENTARIO + SALA_LIMPAR_JS + '\n</script>'

# ── textos novos (pt-PT, AO90; «docente»; sem «—» nem «·» em frases)
LICAO_FIM_JS = ('// 28/10/2026: a Sala de aula saiu (decisão do docente de 17/10/2026); '
                'esc() fica, porque abrirExtra() a usa\n')
PAINEL_PEDIDO_ANTIGO = 'Abre a lição no telemóvel e entra na sala'
PAINEL_PEDIDO_NOVO = 'Abre a lição no telemóvel pelo QR'


def painel_como(atlas):
    """As instruções do ecrã de abertura; com o grupo Atlas, também a tecla A (o botão já a anunciava)."""
    return ('<p class="como"><b>1</b> Projeta esta página (<kbd>F</kbd>). <b>2</b> Os alunos abrem a lição pelo QR; '
            'o que fazem fica só no telemóvel de cada um. <b>3</b> Durante a aula: <kbd>P</kbd> pausa cronometrada, '
            '<kbd>R</kbd> relâmpago no ecrã, ' + ('<kbd>A</kbd> «Quem sou eu?», ' if atlas else '')
            + '<kbd>Esc</kbd> esconde o cronómetro, <kbd>I</kbd> volta ao início.</p>')


PAINEL_COMO_NOVO = painel_como(False)
PAINEL_COMO_NOVO_ATLAS = painel_como(True)
PAINEL_INICIO_NOVO = ('<div class="grupo"><button type="button" class="sec" data-projetar title="F">Projetar</button>'
                      '<button type="button" class="sec" data-inicio title="I">Voltar ao início</button></div>')
PAINEL_ESC_NOVO = '<div class="grupo"><button type="button" class="sec" data-fecha title="Esc">Parar o cronómetro</button></div>'
PAINEL_TEMPO_NOVO = 'Pousa o telemóvel e olha para o projetor'
PAINEL_RELAMPAGO_NOVO = 'Responde no caderno; depois, em voz alta'
# o que se pede no caderno, por tipo de cartão (o relâmpago passa a mostrar no projetor o material do cartão da lição)
PAINEL_DICAS = {
    'escolha': 'No caderno, escreve a letra',
    'rever': 'No caderno, escreve a letra da melhor revisão',
    'vf': 'No caderno, escreve V (verdadeiro) ou F (falso)',
    'completar': 'No caderno, escreve o que vai em cada espaço',
    'sublinhar': 'No caderno, escreve a palavra ou as palavras',
    'ordenar': 'No caderno, escreve as letras pela ordem certa',
    'versos': 'No caderno, escreve as letras pela ordem certa',
    'frase': 'No caderno, escreve a frase pela ordem certa',
    'emparelhar': 'No caderno, escreve os pares: 1 A, 2 B…',
    'classes': 'No caderno, escreve a letra de cada um: 1 A, 2 B…',
}
PAINEL_ATLAS_ROT = 'Três pistas, uma de cada vez; no caderno, escreve a letra'

# ── marcas da Sala: se alguma ficar depois das trocas, a forma não é conhecida
MARCAS = ('ntfy', 'EventSource', 'BroadcastChannel', 'EPISala', 'epi-sala', 'epi-atlas-sala', 'painel-sala-',
          'aoEvento', 'ligaSala', 'enviarSala', 'abrirSala', 'aoReceber', 'liga-sala', 'data-sala', 'id="sala"',
          'faixa-pausa', 'id="sobre"', 'data-fechar-sala', 'sala-cod', 'data-placar', 'data-nova', 'Nova sala',
          '>Sala de aula<', 'Código da sala', 'alcunha', 'placar', 'data-sorteio', 'data-votacao', 'data-codigo',
          'data-limpar', 'enviar({t:')


def sem_limpeza(texto):
    return texto.replace(LIMPEZA_SCRIPT, '').replace(SALA_LIMPAR_JS, '')


def marcas(texto):
    t = sem_limpeza(texto)
    return [m for m in MARCAS if m in t]


def tem_sala(texto):
    t = sem_limpeza(texto)
    return any(m in t for m in ('ntfy', 'EPISala', 'EventSource', 'BroadcastChannel', 'liga-sala', 'data-sala',
                                'aoEvento', 'enviarSala', 'painel-sala-', 'epi-sala', 'data-placar', 'sala-cod'))


# ── blocos conhecidos (cópias literais do que as páginas publicadas tinham a 28/10/2026; coincidem com o código
# arquivado a 17/10 em sala-desligada-2026-10-17.md: sala.mjs, licao.mjs, painel.mjs, percurso.mjs e atlas.mjs)
CASCA_MENU_SALA = '.casca-menu .sala{margin:0;padding:10px 0 0;background:none}\n'
MENU_COMO = '<a href="https://pedrohfernandes-klk.github.io/pt/como/">Como se faz (vídeos)</a></nav>'
INDICE_DESAFIO_ENVIO = ('if(festa)surpresa(u);if(window.EPISala){var S=EPISala.sala();if(S&&S.cod)EPISala.enviar(S.cod,'
                        '{t:"desafio",a:S.alc,u:u.n,c:s.certas,n:8,ganho:!!ch.ganho})}')
PROGRESSO_INICIO = '<script>(function(){var S=document.getElementById("progresso");'

EPISALA_SCRIPT = r'''<script>
window.EPISala=(function(){"use strict";
var BASE="https://ntfy.sh",PREF="epi-pt-",LOCAL=location.protocol==="file:"||/[?&]local\b/.test(location.search),bc={};
function topico(cod){return PREF+String(cod||"").toUpperCase()}
function enviar(cod,msg){msg.ts=Date.now();var s=JSON.stringify(msg);
 if(LOCAL){try{(bc[cod]=bc[cod]||new BroadcastChannel(topico(cod))).postMessage(s)}catch(x){}return Promise.resolve(true)}
 return fetch(BASE+"/"+topico(cod),{method:"POST",body:s,headers:{"Content-Type":"text/plain"}}).then(function(r){return r.ok}).catch(function(){return false})}
function ligar(cod,onMsg,desde){
 if(LOCAL){var c=new BroadcastChannel(topico(cod));c.onmessage=function(ev){try{onMsg(JSON.parse(ev.data),Date.now()/1000)}catch(x){}};return {fechar:function(){c.close()},local:true}}
 var es=new EventSource(BASE+"/"+topico(cod)+"/sse"+(desde?"?since="+encodeURIComponent(desde):""));
 var h=function(ev){try{var d=JSON.parse(ev.data);if(d.event&&d.event!=="message")return;var m=JSON.parse(d.message);onMsg(m,d.time)}catch(x){}};
 es.onmessage=h;es.addEventListener("message",h);return {fechar:function(){es.close()},es:es}}
function codigo(){var A="ABCDEFGHJKMNPQRSTUVWXYZ23456789",s="";for(var i=0;i<5;i++)s+=A[Math.floor(Math.random()*A.length)];return s}
function sala(k){try{return JSON.parse(localStorage.getItem(k||"epi-sala")||"null")}catch(x){return null}}
function entrar(cod,alc,k){try{localStorage.setItem(k||"epi-sala",JSON.stringify({cod:String(cod).toUpperCase().replace(/[^A-Z0-9]/g,"").slice(0,5),alc:String(alc).trim().slice(0,16),t:Date.now()}))}catch(x){}return sala(k)}
function sair(k){try{localStorage.removeItem(k||"epi-sala")}catch(x){}}
// modo código (sem canal): o telemóvel mostra um código com a alcunha e os pontos; o painel descodifica-o
function codificar(m){try{return btoa(unescape(encodeURIComponent(JSON.stringify(m)))).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"")}catch(x){return ""}}
function descodificar(s){try{s=String(s||"").trim().replace(/-/g,"+").replace(/_/g,"/");while(s.length%4)s+="=";return JSON.parse(decodeURIComponent(escape(atob(s))))}catch(x){return null}}
return {enviar:enviar,ligar:ligar,codigo:codigo,sala:sala,entrar:entrar,sair:sair,topico:topico,codificar:codificar,descodificar:descodificar,LOCAL:LOCAL,BASE:BASE}})();
</script>'''

LICAO_SALA_CSS = r'''.sala{background:var(--papel);padding:14px 16px;margin:10px 0 0}.sala .sala-tit{font:400 1.5rem/1 var(--cartaz,"Arial Black",Arial);margin:0 0 8px}
.sala label{display:block;font:700 .72rem Arial;letter-spacing:.1em;text-transform:uppercase;color:var(--suave);margin:8px 0 2px}
.sala input.maq{display:block;width:100%;max-width:18rem;font:1.15rem/1.5 "Special Elite","Courier New",monospace;padding:6px 8px;border:0;border-bottom:2px solid var(--tinta);background:transparent;color:var(--tinta);letter-spacing:.08em}
.sala input[data-cod]{text-transform:uppercase;letter-spacing:.3em;max-width:9rem}
.sala .sala-nota{font-size:.82rem;color:var(--suave);margin:8px 0 0}.sala .acoes{display:flex;gap:16px;margin:8px 0 0}
.sala .sala-estado{font:1rem "Special Elite","Courier New",monospace;margin:4px 0 0}
.faixa-pausa{position:sticky;top:0;z-index:7;background:var(--tinta);color:var(--papel);padding:8px 14px;display:flex;align-items:center;gap:12px;font:700 .85rem Arial;letter-spacing:.04em}.faixa-pausa b{font:400 1.6rem/1 var(--cartaz,"Arial Black",Arial);color:var(--mostarda,#d9a520)}
.sobre{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:90;display:flex;align-items:flex-end;justify-content:center;padding:12px;animation:surge .25s ease-out}.sobre .sobre-c{background:var(--fundo,#f3f2ee);color:var(--tinta);width:100%;max-width:46rem;max-height:92vh;overflow:auto;padding:12px 14px 10px;animation:sobe .35s cubic-bezier(.2,.7,.2,1)}
.sobre .sobre-t{display:flex;justify-content:space-between;align-items:baseline;font:400 1.4rem/1 var(--cartaz,"Arial Black",Arial);margin:0 0 8px}.sobre .sobre-t b{color:var(--vermelho,#c8232c);font-weight:400}
.sobre .ops{display:flex;flex-direction:column;gap:8px}.sobre .ops button{font:600 1rem/1.3 Arial;text-align:left;min-height:48px;padding:10px 12px;border:0;background:var(--papel);color:var(--tinta);cursor:pointer}.sobre .ops button[aria-pressed="true"]{background:var(--tinta);color:var(--papel)}
.sobre .enviado{font:700 .9rem Arial;color:var(--mostarda,#d9a520);margin:8px 0 0}
@keyframes surge{from{opacity:0}to{opacity:1}}@keyframes sobe{from{transform:translateY(40px);opacity:.3}to{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.sobre,.sobre .sobre-c{animation:none}}
'''

LICAO_SALA_FORM = r'''<div class="sala" id="sala" hidden><p class="sala-tit">Sala de aula</p><label>Código da sala<input class="maq" data-cod maxlength="5" autocapitalize="characters" autocomplete="off" spellcheck="false"></label><label>A tua alcunha<input class="maq" data-alc maxlength="16" autocomplete="off" spellcheck="false"></label><p class="sala-nota">O código está no projetor. A alcunha fica guardada neste aparelho; para o placar vão só a alcunha e os pontos.</p><p class="sala-estado"></p><div class="acoes"><button type="button" data-entrar>Entrar</button><button type="button" class="sec" data-sair>Sair da sala</button><button type="button" class="sec" data-fechar-sala>Fechar</button></div></div>'''

LICAO_SALA_JS = r'''// sala de aula (11/10/2026): código e alcunha à máquina; os pontos vão para o painel do docente; relâmpago, votação e pausa chegam daqui
var SALA=window.EPISala?EPISala.sala():null,canal=null,ultEnvio=0,pend=null;
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function ligaSala(){var a=$("#liga-sala");if(a)a.textContent=SALA&&SALA.cod?"Sala "+SALA.cod+" · "+SALA.alc:"Sala";if(canal){canal.fechar();canal=null}if(!SALA||!SALA.cod||!window.EPISala)return;canal=EPISala.ligar(SALA.cod,aoReceber);EPISala.enviar(SALA.cod,{t:"ola",a:SALA.alc,l:ID})}
function estadoDe(ev){return {t:ev.t==="fim"?"fim":"estado",a:SALA.alc,l:ID,xp:ev.xp||0,c:ev.certas||0,n:ev.n||0,i:(ev.i||0)+1}}
function mostrarCodigo(ev){var cod=EPISala.codificar({a:SALA.alc,l:ID,xp:ev.xp||0,c:ev.certas||0,n:ev.n||0});sobre('<p class="sobre-t">Sem ligação à sala</p><p>Mostra este código ao docente, ou dita-o:</p><p class="sala-estado" style="font-size:1.3rem;word-break:break-all">'+esc(cod)+'</p><div class="acoes"><button type="button" data-fecha>Fechar</button></div>');$("[data-fecha]").onclick=fechaSobre}
function aoEvento(ev){if(!SALA||!SALA.cod||!window.EPISala)return;var agora=Date.now();var manda=function(){ultEnvio=Date.now();EPISala.enviar(SALA.cod,estadoDe(ev)).then(function(ok){if(!ok&&ev.t==="fim")mostrarCodigo(ev)})};clearTimeout(pend);if(ev.t==="fim"||agora-ultEnvio>15000)manda();else pend=setTimeout(manda,15000-(agora-ultEnvio))}
function sobre(h){var s=$("#sobre");s.innerHTML='<div class="sobre-c">'+h+'</div>';s.hidden=false;return s}
function fechaSobre(){var s=$("#sobre");s.hidden=true;s.innerHTML=""}
function aoReceber(m){if(!m||!m.t)return;
 if(m.t==="pausa"){var f=$("#faixa-pausa");f.hidden=false;var fim=m.fim||(Date.now()+(m.min||3)*60000);var tick=function(){var sg=Math.max(0,Math.round((fim-Date.now())/1000));f.innerHTML='<span>Pausa: cartões '+esc(m.de||"")+(m.ate?" a "+esc(m.ate):"")+'</span><b>'+Math.floor(sg/60)+":"+String(sg%60).padStart(2,"0")+'</b>';if(sg<=0){clearInterval(f._t);setTimeout(function(){f.hidden=true},4000)}};clearInterval(f._t);tick();f._t=setInterval(tick,1000)}
 if(m.t==="relampago"){var x=m.x||CARTOES[m.k];if(!x||x.t==="ler")return;if(window.REL)try{REL.fechar()}catch(z){}var R=EPICasca.abrir({marca:"Relâmpago",semVoltar:true});window.REL=R;var t0=Date.now(),seg=m.s||60;var tick=function(){var r=Math.max(0,seg-Math.round((Date.now()-t0)/1000));R.modo(r+" s");if(r<=0){clearInterval(tm);R.fechar()}},tm=setInterval(tick,500);
  EPIJogo.montar({casca:R,itens:[x],chave:"rel-"+(m.id||m.k),mostrarAnterior:false,variar:false,fim:function(st){clearInterval(tm);EPISala.enviar(SALA.cod,{t:"rel",id:m.id||m.k,a:SALA.alc,ok:st.certas===1,ms:Date.now()-t0});setTimeout(function(){R.fechar()},2500)}});tick()}
 if(m.t==="votacao"){var v=sobre('<p class="sobre-t">Votação</p><p class="q">'+esc(m.p||"")+'</p><div class="ops">'+(m.o||[]).map(function(o,j){return '<button type="button" data-j="'+j+'">'+esc(o)+'</button>'}).join("")+'</div><p class="enviado" hidden>Voto enviado</p>');
  $$("[data-j]",v).forEach(function(b){b.onclick=function(){$$("[data-j]",v).forEach(function(o){o.setAttribute("aria-pressed",String(o===b))});EPISala.enviar(SALA.cod,{t:"voto",id:m.id,a:SALA.alc,j:+b.dataset.j});$(".enviado",v).hidden=false;setTimeout(fechaSobre,1500)}})}
 if(m.t==="fecha"){fechaSobre();if(window.REL)try{REL.fechar()}catch(z){}}}
(function(){var a=$("#liga-sala"),d=$("#sala");if(!a||!d||!window.EPISala)return;a.onclick=function(ev){ev.preventDefault();d.hidden=!d.hidden;if(!d.hidden){var c=$("[data-cod]",d),n=$("[data-alc]",d);if(SALA){c.value=SALA.cod||"";n.value=SALA.alc||""}$(".sala-estado",d).textContent=SALA&&SALA.cod?"Estás na sala "+SALA.cod+" como "+SALA.alc+".":"";(SALA&&SALA.cod?n:c).focus()}};
 $$("input.maq",d).forEach(function(i){i.addEventListener("keydown",function(ev){if(window.EPIJogo&&(ev.key.length===1||ev.key==="Backspace"))EPIJogo.tocar("tecla")})});
 $("[data-entrar]",d).onclick=function(){var c=$("[data-cod]",d).value.trim(),n=$("[data-alc]",d).value.trim();if(c.replace(/[^A-Za-z0-9]/g,"").length!==5||n.length<2){$(".sala-estado",d).textContent="Preciso do código de cinco letras e de uma alcunha.";return}SALA=EPISala.entrar(c,n);ligaSala();d.hidden=true;avisar("Estás na sala "+SALA.cod+" como "+SALA.alc)};
 $("[data-sair]",d).onclick=function(){EPISala.sair();SALA=null;ligaSala();d.hidden=true;avisar("Saíste da sala")};
 $("[data-fechar-sala]",d).onclick=function(){d.hidden=true}})();
ligaSala()})();'''

LICAO_ESC = r'''function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
'''

PAINEL_CSS_SALACOD = r'''.sala-cod{font:400 2.2rem/1 var(--cartaz);letter-spacing:.08em}.sala-cod b{font-weight:400;letter-spacing:.3em;background:var(--tinta);color:var(--papel);padding:4px 14px;margin-left:8px}
'''

PAINEL_CSS_PLACAR = r'''.placar{background:var(--papel);padding:18px 20px;display:flex;flex-direction:column}
.placar h2{font:400 1.8rem/1 var(--cartaz);margin:0 0 10px;letter-spacing:.04em;display:flex;justify-content:space-between;align-items:baseline}.placar h2 small{font:700 .7rem Arial;letter-spacing:.1em;color:var(--suave)}
ol.lista{list-style:none;margin:0;padding:0;flex:1;overflow:auto}
ol.lista li{display:grid;grid-template-columns:2rem 1fr auto;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--fundo);transition:transform .6s cubic-bezier(.2,.7,.2,1)}
ol.lista .pos{font:400 1.6rem/1 var(--cartaz);color:var(--suave)}ol.lista li:first-child .pos{color:var(--mostarda)}
ol.lista .alc{font:1.15rem var(--maq);letter-spacing:.03em}ol.lista .alc small{display:block;font:700 .62rem Arial;letter-spacing:.1em;text-transform:uppercase;color:var(--suave)}
ol.lista .fio{display:flex;gap:2px;margin-top:4px}ol.lista .fio i{width:6px;height:6px;border-radius:50%;background:var(--fundo)}ol.lista .fio i.ok{background:var(--mostarda)}
ol.lista .pts{font:400 2rem/1 var(--cartaz)}ol.lista li.selo .pts::after{content:" ✓";color:var(--mostarda);font-size:.6em}
ol.lista li.novo{animation:entra .5s ease-out}@keyframes entra{from{background:var(--mostarda)}to{background:transparent}}
.estado-canal{font:700 .7rem Arial;letter-spacing:.08em;text-transform:uppercase;color:var(--suave);margin:8px 0 0}.estado-canal.mau{color:var(--vermelho)}
'''

PAINEL_CSS_SORTEIO = r'''.sorteio{font:400 clamp(3rem,10vw,7rem)/1 var(--maq);margin:10px 0}.sorteio.roda{animation:treme .12s linear infinite}@keyframes treme{50%{opacity:.5}}
.barras{display:grid;gap:10px;margin-top:10px}.barras div{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center}.barras span{font:400 1.4rem/1.1 Arial}.barras b{font:400 2rem/1 var(--cartaz);min-width:2.5rem;text-align:right}.barras i{grid-column:1/3;display:block;height:14px;background:var(--fundo);position:relative}.barras i::after{content:"";position:absolute;left:0;top:0;bottom:0;width:var(--w,0%);background:var(--tinta);transition:width .6s ease}
.rel{list-style:none;margin:10px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:6px 14px}.rel li{display:flex;justify-content:space-between;gap:8px;font:1.05rem var(--maq);border-bottom:1px solid var(--fundo)}.rel li.ok{color:var(--tinta)}.rel li.mau{color:var(--suave);text-decoration:line-through}.rel li small{font:700 .7rem Arial;color:var(--suave)}
'''

PAINEL_COMO = r'''<p class="como"><b>1</b> Toca em «Nova sala» e projeta (<kbd>F</kbd>). <b>2</b> Os alunos abrem a lição pelo QR, tocam em «Sala» e escrevem o código e uma alcunha. <b>3</b> Durante a aula: <kbd>P</kbd> pausa cronometrada, <kbd>R</kbd> relâmpago, <kbd>S</kbd> sorteio, <kbd>V</kbd> votação, <kbd>Esc</kbd> fecha o cartão nos telemóveis. Só a alcunha e os pontos circulam.</p>'''

PAINEL_PLACAR = r'''<aside class="placar"><h2>Placar <small data-n>0 na sala</small></h2><ol class="lista" data-placar></ol><p class="estado-canal" data-canal>sem sala</p></aside>
'''

PAINEL_RODAPE_SALA = r'''<div class="grupo"><b>Sorteio</b><button type="button" data-sorteio title="S">Tirar um nome</button></div>
<div class="grupo"><b>Votação</b><input type="text" data-v-p placeholder="pergunta"><input type="text" data-v-1 placeholder="A"><input type="text" data-v-2 placeholder="B"><input type="text" data-v-3 placeholder="C"><button type="button" data-votacao title="V">Lançar</button></div>
<div class="grupo"><b>Código do aluno</b><input type="text" data-codigo placeholder="cola o código"><button type="button" class="sec" data-add>Acrescentar</button></div>
<div class="grupo"><button type="button" class="sec" data-fecha title="Esc">Fechar o cartão nos telemóveis</button></div>'''

PAINEL_JS_ESTADO = r''',cod=null,canal=null,placar={},rel={},votos={},crono=null,pedidoBase="Abre a lição no telemóvel e entra na sala";
function ls(k){try{return JSON.parse(localStorage.getItem(k)||"null")}catch(x){return null}}
function gravar(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(x){}}
'''

PAINEL_JS_CANAL = r'''function canalEstado(t,mau){var c=$("[data-canal]");c.textContent=t;c.className="estado-canal"+(mau?" mau":"")}
function abrirSala(novo){if(novo||!cod){cod=EPISala.codigo();placar={};rel={};votos={};gravar(K,{cod:cod,t:Date.now()})}$("[data-cod]").textContent=cod;if(canal)canal.fechar();
 canal=EPISala.ligar(cod,aoReceber,novo?null:"12h");canalEstado(EPISala.LOCAL?"sala local, neste navegador":"sala aberta em "+EPISala.BASE.replace(/^https?:\/\//,""));
 if(canal.es){canal.es.onerror=function(){canalEstado("sem ligação ao canal: usa o código do aluno",true)};canal.es.onopen=function(){canalEstado("sala aberta em "+EPISala.BASE.replace(/^https?:\/\//,""))}}
 pedido("Sala "+cod,pedidoBase);pintar()}
function aoReceber(m){if(!m||!m.t)return;
 if(m.t==="ola"||m.t==="estado"||m.t==="fim"){var p=placar[m.a]||{xp:0,c:0,n:0,i:0,t:0,selos:0};p.novo=!placar[m.a];if(m.t!=="ola"){p.xp=Math.max(p.xp,m.xp||0);p.c=m.c||p.c;p.n=m.n||p.n;p.i=Math.max(p.i,m.i||0);if(m.t==="fim")p.fim=true}p.t=Date.now();placar[m.a]=p;pintar()}
 if(m.t==="desafio"){var q=placar[m.a]||{xp:0,c:0,n:0,i:0,t:0,selos:0};q.selos=(q.selos||0)+(m.ganho?1:0);q.xp+=(m.c||0)*10+(m.ganho?50:0);q.t=Date.now();placar[m.a]=q;pintar()}
 if(m.t==="rel"){(rel[m.id]=rel[m.id]||[]).push(m);pintarRel(m.id)}
 if(m.t==="voto"){var v=votos[m.id]=votos[m.id]||{};v[m.a]=m.j;pintarVotos(m.id)}}
var posAntes={};
function pintar(){var ol=$("[data-placar]"),nomes=Object.keys(placar).sort(function(a,b){return (placar[b].xp-placar[a].xp)||(placar[b].i-placar[a].i)||a.localeCompare(b)});
 $("[data-n]").textContent=nomes.length+(nomes.length===1?" na sala":" na sala");
 ol.innerHTML=nomes.map(function(a,k){var p=placar[a];var fio="";for(var j=0;j<Math.min(p.n||0,20);j++)fio+='<i class="'+(j<p.i?"ok":"")+'"></i>';return '<li data-a="'+esc(a)+'" class="'+(p.novo?"novo":"")+(p.selos?" selo":"")+'"><span class="pos">'+(k+1)+'</span><span class="alc">'+esc(a)+(p.n?'<small>'+p.i+' de '+p.n+' cartões'+(p.fim?' · feita':'')+'</small><span class="fio">'+fio+'</span>':'<small>na sala</small>')+'</span><span class="pts">'+p.xp+'</span></li>'}).join("");
 $$("li",ol).forEach(function(li){var a=li.dataset.a,y=li.getBoundingClientRect().top,antes=posAntes[a];if(antes!=null&&antes!==y){li.style.transition="none";li.style.transform="translateY("+(antes-y)+"px)";requestAnimationFrame(function(){li.style.transition="";li.style.transform=""})}posAntes[a]=y;placar[a].novo=false})}
function pintarRel(id){var lista=(rel[id]||[]).slice().sort(function(a,b){return (b.ok-a.ok)||(a.ms-b.ms)});$("[data-extra]").innerHTML='<p class="rot">Relâmpago: quem respondeu</p><ol class="rel">'+lista.map(function(r,k){return '<li class="'+(r.ok?"ok":"mau")+'"><span>'+(k+1)+'. '+esc(r.a)+'</span><small>'+(r.ms/1000).toFixed(1)+' s</small></li>'}).join("")+'</ol>'}
function pintarVotos(id){var v=votos[id]||{},o=votos[id+"-o"]||[],n={};Object.keys(v).forEach(function(a){n[v[a]]=(n[v[a]]||0)+1});var tot=Object.keys(v).length||1;$("[data-extra]").innerHTML='<p class="rot">Votação: '+tot+(tot===1?" voto":" votos")+'</p><div class="barras">'+o.map(function(t,j){return '<div><span>'+esc(t)+'</span><b>'+(n[j]||0)+'</b><i style="--w:'+Math.round((n[j]||0)/tot*100)+'%"></i></div>'}).join("")+'</div>'}
'''

PAINEL_JS_ENVIAR = r'''function enviar(m){if(!cod){abrirSala(true)}return EPISala.enviar(cod,m)}
$("[data-nova]").onclick=function(){abrirSala(true)};
$("[data-limpar]").onclick=function(){placar={};rel={};votos={};pintar();$("[data-extra]").innerHTML=""};
'''

PAINEL_JS_PAUSA = r'''var fim=contar(min*60,function(){pedido("Tempo","Olha para o placar")});pedido("Pausa de "+min+(min===1?" minuto":" minutos"),"Cartões "+de+" a "+ate+", no telemóvel");$("[data-extra]").innerHTML="";enviar({t:"pausa",de:de,ate:ate,min:min,fim:fim})};'''

PAINEL_JS_RELAMPAGO = r'''if(!x)return;var id="r"+Date.now();rel[id]=[];contar(s,function(){enviar({t:"fecha"})});pedido("Relâmpago, "+s+" segundos",x.p);$("[data-extra]").innerHTML='<p class="rot">À espera das respostas</p>';enviar({t:"relampago",k:k,s:s,id:id})};'''

PAINEL_JS_SORTEIO_ATE_ADD = r'''$("[data-sorteio]").onclick=function(){var nomes=Object.keys(placar);if(!nomes.length){pedido("Sorteio","Ainda ninguém na sala");return}pedido("Sorteio","Quem lê em voz alta?");var el=document.createElement("p");el.className="sorteio roda";$("[data-extra]").innerHTML="";$("[data-extra]").appendChild(el);var n=0,t=setInterval(function(){el.textContent=nomes[Math.floor(Math.random()*nomes.length)];if(++n>14){clearInterval(t);el.className="sorteio"}},110)};
$("[data-votacao]").onclick=function(){var p=$("[data-v-p]").value.trim(),o=[$("[data-v-1]").value.trim(),$("[data-v-2]").value.trim(),$("[data-v-3]").value.trim()].filter(Boolean);if(!p||o.length<2){pedido("Votação","Escreve a pergunta e pelo menos duas opções");return}var id="v"+Date.now();votos[id]={};votos[id+"-o"]=o;pedido("Votação",p);pintarVotos(id);enviar({t:"votacao",id:id,p:p,o:o})};
$("[data-fecha]").onclick=function(){enviar({t:"fecha"});clearInterval(crono);$("[data-crono]").hidden=true};
$("[data-add]").onclick=function(){var m=EPISala.descodificar($("[data-codigo]").value);if(!m||!m.a){canalEstado("código inválido",true);return}aoReceber({t:"fim",a:m.a,xp:m.xp,c:m.c,n:m.n,i:m.n});$("[data-codigo]").value=""};
'''

PAINEL_JS_RETOMA = r'''
var g=ls(K);if(g&&g.cod&&Date.now()-g.t<6*3600000){cod=g.cod;abrirSala(false)}else pintar();
'''

PAINEL_ATLAS_ANTIGO = ('if(!x)return;var id="r"+Date.now();rel[id]=[];contar(s,function(){enviar({t:"fecha"})});'
                       'pedido("Quem sou eu? "+s+" segundos",x.pistas[0]);$("[data-extra]").innerHTML=\'<p class="rot">'
                       'Atlas Lusófono · três pistas</p><ol>\'+x.pistas.map(function(p){return "<li>"+%s+"</li>"})'
                       '.join("")+\'</ol>\';enviar({t:"relampago",k:-1,x:x,s:s,id:id})};')
PAINEL_ATLAS_VARIANTES = ('esc(p).replace(/_([^_]+)_/g,"<i>$1</i>")', 'esc(p)')

# ── o que entra nos painéis (28/10/2026, depois da revisão): sem telemóveis do outro lado, o projetor tem de bastar
# - CSS do material do relâmpago e do «Quem sou eu?»; o QR cresce no ecrã de abertura (onde estava o placar) e sai,
#   com o símbolo da unidade, enquanto há material à vista
PAINEL_CSS_NOVO = r'''.material{font:1.3rem/1.35 Arial,Helvetica,sans-serif;color:var(--tinta);margin:0 0 8px}.material .rot{margin:0 0 12px}
.material .mat-cita{font:italic 1.35rem/1.4 Georgia,"Times New Roman",serif;margin:0 0 14px;padding-left:14px;border-left:4px solid var(--tinta)}
.material .mat-ver{margin:0 0 14px}.material .mat-ver img{display:block;max-width:100%;max-height:30vh;width:auto;height:auto;border:1px solid var(--tinta)}
.material .mat-apoio{margin:0 0 10px;color:var(--suave)}.material .mat-frase{font:1.45rem/1.6 Georgia,"Times New Roman",serif;margin:0 0 14px}.material .mat-frase u{text-decoration-thickness:3px;text-underline-offset:5px}
.material .lac{display:inline-block;min-width:4.5em;border-bottom:3px solid var(--tinta);text-align:center;font:400 1.2rem/1 var(--cartaz);color:var(--suave)}
.material .mat-lac{margin:0 0 8px}.material .mat-lac b,.material ol li>b{font:400 1.7rem/1 var(--cartaz);min-width:1.6rem;margin-right:10px}
.material ol{list-style:none;margin:0 0 12px;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(22rem,100%),1fr));align-content:start;gap:10px 32px}.material ol li{display:flex;align-items:baseline}
.material .mat-pares{display:grid;grid-template-columns:1fr 1fr;gap:0 48px}.material .mat-pares ol,.material .mat-pistas{grid-template-columns:1fr}
.material .mat-pal{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 14px}.material .mat-pal span{font:1.4rem "Special Elite","Courier New",monospace;border:2px solid var(--tinta);padding:4px 10px}
.material .mat-remate{font:1.15rem/1.45 Arial,Helvetica,sans-serif;color:var(--suave);margin:12px 0 0;max-width:60rem}
.material .mat-correcao{font:1.3rem/1.45 Arial,Helvetica,sans-serif;color:var(--tinta);margin:14px 0 0;padding-top:10px;border-top:3px solid var(--tinta);max-width:60rem}.material .mat-correcao>b:first-child{font:400 1.6rem/1 var(--cartaz);letter-spacing:.04em;margin-right:10px}
.pedido:has(.material) h1{font-size:clamp(2rem,4.2vw,3.8rem);padding-right:0}.pedido:has(.material) .extra{margin-top:0}
.pedido:has(.material) .crono{order:1;margin:auto 0 0;font-size:clamp(3.4rem,8vw,6.5rem)}.pedido:has(.material) .qr,.pedido:has(.material) .simb{display:none}
.pedido:has(.como) .qr{width:min(36vh,340px)}.pedido:has(.como) .qr img{width:100%;height:auto}.pedido:has(.como) h1{padding-right:calc(min(36vh,340px) + 30px)}.pedido:has(.como) .como{max-width:min(40rem,calc(100% - min(36vh,340px) - 30px))}
@media (max-width:900px){.material .mat-pares{grid-template-columns:1fr}.pedido:has(.como) .qr{width:min(60vw,260px)}.pedido:has(.como) h1{padding-right:0}.pedido:has(.como) .como{max-width:none}}
'''

# - o relâmpago mostra o material do cartão da lição (opções, pares, versos, frase…), baralhado e sem a solução;
#   «Voltar ao início» (I) repõe o ecrã de abertura; o «Quem sou eu?» mostra uma pista por cada terço do tempo
PAINEL_MATERIAL_JS = r'''var LETRAS="ABCDEFGHIJKLMNOPQRSTUVWXYZ",DICA=%(dicas)s,ROT_ATLAS=%(rot_atlas)s,INICIO={rot:$("[data-rot]").textContent,p:$("[data-pedido]").innerHTML,x:$("[data-extra]").innerHTML};
function md(s){return esc(s).replace(/[*]{2}([^*]{1,80})[*]{2}/g,"<b>$1</b>").replace(/(^|[^0-9A-Za-zÀ-ÖØ-öø-ÿ_\/])_([^_\n<>]{1,100}?)_(?![0-9A-Za-zÀ-ÖØ-öø-ÿ_])/g,"$1<i>$2</i>")}
function citar(c){c=String(c).trim();return /^«[\s\S]*»[.!?…]?$/.test(c)&&c.indexOf("«",1)<0?md(c):"«"+md(c)+"»"}
function baralhar(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
function lista(a,num,cl){return '<ol'+(cl?' class="'+cl+'"':'')+'>'+a.map(function(t,j){return '<li><b>'+(num?j+1:LETRAS[j])+'</b><span>'+md(t)+'</span></li>'}).join("")+'</ol>'}
function material(x){var m=MATERIAL[x.k]||{},t=x.t==="emparelhar"&&m.esq&&m.dir&&m.dir.length<m.esq.length?"classes":x.t,h='<div class="material"><p class="rot">'+(DICA[t]||%(dica_geral)s)+%(dica_fim)s+'</p>';
 if(m.cita)h+='<p class="mat-cita">'+citar(m.cita)+'</p>';
 if(m.ver)h+='<figure class="mat-ver">'+m.ver+'</figure>';
 if(m.apoio)h+='<p class="mat-apoio">'+md(m.apoio)+'</p>';
 if(m.frase){var f=md(m.frase);if(m.trecho)f=f.replace(md(m.trecho),function(a){return "<u>"+a+"</u>"});h+='<p class="mat-frase">'+f.replace(/\[(\d)\]/g,'<span class="lac">$1</span>')+'</p>'}
 if(m.lac)h+=m.lac.map(function(o,j){return '<p class="mat-lac"><b>'+(j+1)+'</b>'+o.map(function(s){return md(s)}).join(" / ")+'</p>'}).join("");
 if(m.o)h+=lista(m.o);
 if(m.itens)h+=lista(m.itens);
 if(m.palavras)h+='<p class="mat-pal">'+m.palavras.map(function(w){return '<span>'+md(w)+'</span>'}).join("")+'</p>';
 if(m.esq)h+='<div class="mat-pares">'+lista(m.esq,true)+lista(m.dir)+'</div>';
 return h+'</div>'}
''' % {
    'dicas': json.dumps(PAINEL_DICAS, ensure_ascii=False, separators=(',', ':')),
    'rot_atlas': json.dumps(PAINEL_ATLAS_ROT, ensure_ascii=False),
    'dica_geral': json.dumps(PAINEL_RELAMPAGO_NOVO.split('; ')[0], ensure_ascii=False),
    'dica_fim': json.dumps('; ' + PAINEL_RELAMPAGO_NOVO.split('; ')[1], ensure_ascii=False),
}

# 28/10/2026 (revisão): quando o tempo acaba, aparece por baixo do material a correção do cartão (f, da lição)
PAINEL_RELAMPAGO_JS = ('if(!x)return;contar(s,function(){var d=$("[data-extra] .material"),m=MATERIAL[x.k];'
                       'if(d&&m&&m.f)d.insertAdjacentHTML("beforeend",\'<p class="mat-correcao"><b>Correção</b>\'+md(m.f)+\'</p>\')});'
                       'pedido("Relâmpago, "+s+" segundos",x.p);$("[data-extra]").innerHTML=material(x)};')

PAINEL_ATLAS_JS = (
    'if(!x)return;var P=x.pistas||[],O=x.o||[],ord=baralhar(O.map(function(_,j){return j})),t0=Date.now(),vistas=0,ol;'
    'pedido("Quem sou eu? "+s+" segundos","Quem sou eu?");'
    '$("[data-extra]").innerHTML=\'<div class="material"><p class="rot">\'+ROT_ATLAS+\'</p><ol class="mat-pistas"></ol>\''
    '+lista(ord.map(function(j){return O[j]}))+\'</div>\';ol=$("[data-extra] .mat-pistas");\n'
    'var mostra=function(n){while(vistas<Math.min(n,P.length)){var li=document.createElement("li");'
    'li.innerHTML="<b>"+(vistas+1)+"</b><span>"+md(P[vistas])+"</span>";ol.appendChild(li);vistas++}};mostra(1);\n'
    'clearInterval(tPistas);tPistas=setInterval(function(){if(!ol.isConnected){clearInterval(tPistas);return}'
    'mostra(1+Math.floor((Date.now()-t0)*3/(s*1000)))},250);\n'
    'contar(s,function(){clearInterval(tPistas);if(!ol.isConnected)return;mostra(P.length);pedido("Quem sou eu?",O[x.c]);'
    'if(x.f)ol.parentNode.insertAdjacentHTML("beforeend",\'<p class="mat-remate">\'+md(x.f)+\'</p>\')})};')

PAINEL_FECHA_INICIO_JS = (
    '$("[data-fecha]").onclick=function(){clearInterval(crono);clearInterval(tPistas);$("[data-crono]").hidden=true};\n'
    '$("[data-inicio]").onclick=function(){clearInterval(crono);clearInterval(tPistas);$("[data-crono]").hidden=true;'
    '$("[data-rot]").textContent=INICIO.rot;$("[data-pedido]").innerHTML=INICIO.p;$("[data-extra]").innerHTML=INICIO.x};\n')

PAINEL_TECLAS_JS = ('else if(k==="a"&&$("[data-atlas]"))$("[data-atlas]").click();'
                    'else if(k==="i")$("[data-inicio]").click();else if(k==="f")')

PEDIDO_ITALICO = 'function pedido(rot,t){$("[data-rot]").textContent=rot;$("[data-pedido]").innerHTML=esc(t).replace(/_([^_]+)_/g,"<i>$1</i>")}'
PEDIDO_SIMPLES = 'function pedido(rot,t){$("[data-rot]").textContent=rot;$("[data-pedido]").textContent=t}'

ATLAS_CSS_SALA = r'''.sala-f label{display:block;font:700 .85rem var(--sans);margin:10px 0 4px}.sala-f input{font:1.2rem var(--sans);width:100%;min-height:48px;padding:0 10px;border:0;border-bottom:2px solid var(--tinta);background:var(--fundo);color:var(--tinta);text-transform:none}
.sala-f .sala-estado{min-height:1.4em;font:.9rem var(--sans);color:var(--suave)}
'''

ATLAS_JS_SALA = r'''// ── sala (mapa da turma): a fração de cada país (f, de 0 a 100) e ainda c (6 = conquistado; senão 0 a 5) para páginas antigas
function enviarSala(){if(!window.EPISala)return;var s=EPISala.sala("epi-sala-atlas");if(!s||!s.cod)return;var c={},f={};ORDEM.forEach(function(p){c[p]=dominado(p)?6:Math.round(fracao(p)*5);f[p]=pct(p)});EPISala.enviar(s.cod,{t:"atlas",alc:s.alc,c:c,f:f})}
function sala(){var s=window.EPISala?EPISala.sala("epi-sala-atlas"):null,f=folha('<p class="meta">Atlas Lusófono</p><h3>Sala de aula</h3><p>Se o docente projetar o mapa da turma, escreve o código do ecrã e uma alcunha. Só a alcunha e a parte acesa de cada país vão para o ecrã.</p><div class="sala-f"><label>Código da sala<input data-cod maxlength="5" autocapitalize="characters" autocomplete="off" value="'+esc(s&&s.cod||"")+'"></label><label>Alcunha<input data-alc maxlength="16" autocomplete="off" value="'+esc(s&&s.alc||"")+'"></label><p class="sala-estado">'+(s&&s.cod?"Estás na sala "+esc(s.cod)+".":"")+'</p><button type="button" class="c-prim" data-entrar>Entrar</button> '+(s&&s.cod?'<button type="button" class="c-sec" data-sair>Sair da sala</button>':'')+'</div>');
 $("[data-entrar]",f).onclick=function(){var c=$("[data-cod]",f).value.trim(),n=$("[data-alc]",f).value.trim();if(c.replace(/[^A-Za-z0-9]/g,"").length!==5||n.length<2){$(".sala-estado",f).textContent="O código tem 5 caracteres; a alcunha, pelo menos 2.";return}EPISala.entrar(c,n,"epi-sala-atlas");enviarSala();$(".sala-estado",f).textContent="Estás na sala. O ecrã acende os teus países."};
 var bs=$("[data-sair]",f);if(bs)bs.onclick=function(){EPISala.sair("epi-sala-atlas");$(".sala-estado",f).textContent="Saíste da sala."}}
$("[data-passaporte]").onclick=passaporte;$("[data-sala]").onclick=sala;
'''


# ── motor das trocas: cada troca é literal, o texto antigo aparece uma vez e o novo também (por isso desfaz-se)
def aplicar(rel, texto, trocas):
    edits = []
    for local, antigo, novo in trocas:
        if not novo:
            raise ValueError(f'{rel}: {local}: troca sem texto novo (ancora-a num pedaço vizinho que fica)')
        n = texto.count(antigo)
        if n != 1:
            raise FormaDesconhecida(f'{rel}: {local}: esperava o bloco conhecido uma vez e encontrei-o {n} vez(es)')
        depois = texto.replace(antigo, novo)
        if depois.count(novo) != 1:
            raise FormaDesconhecida(f'{rel}: {local}: o texto novo aparece {depois.count(novo)} vezes; a troca não se desfaria')
        edits.append({'location': local, 'old': antigo, 'new': novo, 'occurrences': 1})
        texto = depois
    resto = marcas(texto)
    if resto:
        raise FormaDesconhecida(f'{rel}: depois das trocas ainda há marcas da Sala: {", ".join(resto)}')
    return texto, edits


def desfazer(rel, texto, edits):
    for e in reversed(edits):
        if texto.count(e['new']) != e['occurrences']:
            raise FormaDesconhecida(f'{rel}: a troca «{e["location"]}» do manifesto já não confere')
        texto = texto.replace(e['new'], e['old'])
    return texto


def confirmar_congelada(rel, tipo, texto, reg):
    """28/10/2026 (revisão): numa página congelada que já está desligada, só se confirma que o manifesto da Sala se
    desfaz e se refaz na página atual. O resto da página pode ter mudado depois (outras trocas literais, outros
    manifestos); base_sha256_lf e after_sha256_lf ficam como registo do dia do corte e não se voltam a verificar."""
    try:
        original = desfazer(rel, texto, reg['edits'])
    except FormaDesconhecida as e:
        raise ManifestoDesatualizado(str(e)) from None
    if EPISALA_SCRIPT not in original:
        raise ManifestoDesatualizado(f'{rel}: desfeito o manifesto, o canal antigo não volta ao sítio')
    try:
        novo, edits = aplicar(rel, original, TIPOS[tipo](rel, original))
    except FormaDesconhecida as e:
        raise ManifestoDesatualizado(f'{rel}: desfeito o manifesto, as trocas do script já não se aplicam ({e})') from None
    if novo != texto or edits != reg['edits']:
        raise ManifestoDesatualizado(f'{rel}: as trocas do script já não são as do manifesto')


def trocas_licao(rel, texto):
    return [
        ('CSS: comentário «Sala e fontes» e .sala input.maq',
         '/* o menu ☰: Sala e fontes */\n.sala input.maq{max-width:100%}\n.extra-sobre{', '.extra-sobre{'),
        ('CSS: .casca-menu .sala', CASCA_MENU_SALA + '.c-grelha{', '.c-grelha{'),
        ('CSS: formulário, faixa da pausa e cartão que interrompe (SALA_CSS)',
         '@media (prefers-color-scheme:dark){:root{--papel2:#1a1a17}}\n\n' + LICAO_SALA_CSS,
         '@media (prefers-color-scheme:dark){:root{--papel2:#1a1a17}}\n'),
        ('HTML: faixa da pausa', '<div class="casca" data-casca><div class="faixa-pausa casca-faixa" id="faixa-pausa" hidden></div>',
         '<div class="casca" data-casca>'),
        ('menu: botão «Sala»', '<button type="button" data-sala id="liga-sala">Sala</button>' + MENU_COMO, MENU_COMO),
        ('menu: formulário da sala (código e alcunha)', LICAO_SALA_FORM + '<p class="c-menu-extra">', '<p class="c-menu-extra">'),
        ('HTML: cartão que interrompe (#sobre)', '<div class="sobre" id="sobre" hidden></div><div id="aviso" role="status"></div>',
         '<div id="aviso" role="status"></div>'),
        ('canal window.EPISala (ntfy.sh) passa à limpeza', EPISALA_SCRIPT, LIMPEZA_SCRIPT),
        ('baralho: sem evento para a sala', '</svg>",evento:function(ev){aoEvento(ev)},pistas:[', '</svg>",pistas:['),
        ('script: envio do estado, pausa, relâmpago, votação e formulário da sala', LICAO_SALA_JS,
         LICAO_FIM_JS + LICAO_ESC + '})();'),
    ]


def html_esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def sem_italico(s):
    return re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', s)


def enunciado(c, italico=False):
    """O enunciado do cartão da lição como o painel o guarda (tests/test_paineis_cartoes.py; com itálico no M1 e no M4)."""
    p = c.get('p') or c.get('frase') or ''
    p = re.sub(r'\*\*(.+?)\*\*', r'\1', p if italico else sem_italico(p))
    return re.sub(r'\[\d\]', '…', p)


def normal(s):
    """Para comparar enunciados: sem itálico nem negrito, e a lacuna [1] vale o mesmo que «…» (o M8-F10 e o M2-F06
    guardam no painel a frase com [1] e [2], e tests/test_m8_comparacao_prova.py conta com isso)."""
    return re.sub(r'\s+', ' ', re.sub(r'\[\d\]', '…', re.sub(r'\*\*(.+?)\*\*', r'\1', sem_italico(s)))).strip()


def baralhado(itens, semente):
    """Ordem fixa e reprodutível (o script corre outra vez e dá o mesmo), nunca a da lição, que nas ordenações é a solução."""
    ordem = sorted(range(len(itens)), key=lambda j: hashlib.sha256(f'{semente}|{j}'.encode('utf-8')).hexdigest())
    if len(itens) > 1 and ordem == list(range(len(itens))):
        ordem = ordem[1:] + ordem[:1]
    return [itens[j] for j in ordem]


def material_de(rel, k, x, semente):
    """O que o telemóvel mostrava no relâmpago (o cartão k da lição), sem a solução: sem c, v, certas nem a ordem certa.
    A correção (f) vai à parte e só aparece quando o tempo acaba."""
    t, m = x['t'], {}
    if not x.get('f'):
        raise FormaDesconhecida(f'{rel}: cartão {k}: sem a correção (f) que o projetor mostra no fim do tempo')
    m['f'] = x['f']
    if x.get('cita'):
        m['cita'] = x['cita']
    if x.get('ver'):
        m['ver'] = x['ver']
    if t == 'escolha':
        m['o'] = baralhado(x['o'], semente)
    elif t == 'vf':
        pass
    elif t == 'completar':
        m['frase'] = x['frase']
        m['lac'] = [baralhado(lac['o'], f'{semente}-{j}') for j, lac in enumerate(x['lacunas'])]
        if len(re.findall(r'\[\d\]', x['frase'])) != len(x['lacunas']):
            raise FormaDesconhecida(f'{rel}: cartão {k} (completar): as lacunas da frase não batem com as opções')
    elif t == 'sublinhar':
        m['frase'] = x['frase']
    elif t == 'ordenar':
        m['itens'] = baralhado(x['passos'], semente)
    elif t == 'versos':
        m['itens'] = baralhado(x['linhas'], semente)
    elif t == 'frase':
        m['palavras'] = baralhado(x['palavras'], semente)
    elif t == 'emparelhar':
        valores = []
        for _, b in x['pares']:
            if b not in valores:
                valores.append(b)
        m['esq'] = baralhado([a for a, _ in x['pares']], semente + '-e')
        m['dir'] = baralhado(valores, semente + '-d')
    elif t == 'rever':
        if x['trecho'] not in x['frase']:
            raise FormaDesconhecida(f'{rel}: cartão {k} (rever): o trecho não está na frase')
        m.update(apoio=x['apoio'], frase=x['frase'], trecho=x['trecho'], o=baralhado(x['o'], semente))
    else:
        raise FormaDesconhecida(f'{rel}: cartão {k}: tipo «{t}» sem material conhecido para o projetor')
    # 28/10/2026 (revisão): quando a citação é a própria frase do exercício (43 cartões), o projetor mostra-a uma vez
    if 'cita' in m and 'frase' in m and so_letras(m['cita']) == so_letras(m['frase']):
        del m['cita']
    return m


def so_letras(s):
    return re.sub(r'[«»\s.,;:!?…]+', ' ', re.sub(r'[*_]', '', s)).strip().lower()


def json_js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def relampago_do_painel(rel, texto, ident):
    """Os cartões do relâmpago a partir da lição: o material de cada um e, onde o enunciado do painel ficou para trás
    (a lição mudou o cartão k e o painel não), o tipo e o enunciado atuais. Antes, o telemóvel abria o cartão k da lição;
    agora o projetor mostra esse mesmo cartão."""
    licao = ROOT / rel.split('/')[0] / f'licao-{ident}' / 'index.html'
    if not licao.exists():
        raise FormaDesconhecida(f'{rel}: não encontrei a lição {licao.relative_to(ROOT).as_posix()}')
    tl = ler(licao)
    i = tl.find('CARTOES=')
    if i < 0:
        raise FormaDesconhecida(f'{rel}: a lição não tem CARTOES')
    L = json.JSONDecoder().raw_decode(tl, i + len('CARTOES='))[0]
    if PEDIDO_ITALICO in texto:
        italico = True
    elif PEDIDO_SIMPLES in texto:
        italico = False
    else:
        raise FormaDesconhecida(f'{rel}: função pedido() desconhecida')
    j = texto.index('CARTOES=') + len('CARTOES=')
    P, fim = json.JSONDecoder().raw_decode(texto, j)
    antigo = texto[j:fim]
    if json_js(P) != antigo:
        raise FormaDesconhecida(f'{rel}: CARTOES do painel não está no formato conhecido')
    sel = re.search(r'<select data-r-k>(.*?)</select>', texto, re.S)
    opcoes = re.findall(r'<option value="(\d+)">(.*?)</option>', sel.group(1)) if sel else []
    if [int(v) for v, _ in opcoes] != [c['k'] for c in P] or ''.join(f'<option value="{v}">{o}</option>' for v, o in opcoes) != sel.group(1):
        raise FormaDesconhecida(f'{rel}: o seletor do relâmpago não corresponde a CARTOES')
    novos, material, novas_opcoes, refeitos = [], {}, [], 0
    for c, (v, o) in zip(P, opcoes):
        k = c['k']
        if not (0 <= k < len(L)) or L[k]['t'] == 'ler':
            raise FormaDesconhecida(f'{rel}: o cartão {k} não é um exercício da lição')
        x = L[k]
        if x['t'] == c['t'] and normal(enunciado(x)) == normal(c['p']):
            novos.append(c)
            novas_opcoes.append(o)
        else:
            p = enunciado(x, italico)
            novos.append({'k': k, 't': x['t'], 'p': p})
            novas_opcoes.append(html_esc(sem_italico(p) if italico else p))
            refeitos += 1
        material[str(k)] = material_de(rel, k, x, f'{ident}-{k}')
    novo = json_js(novos)
    sel_antigo = '<select data-r-k>' + sel.group(1) + '</select>'
    sel_novo = '<select data-r-k>' + ''.join(f'<option value="{c["k"]}">{o}</option>' for c, o in zip(novos, novas_opcoes)) + '</select>'
    return antigo, novo, json_js(material), sel_antigo, sel_novo, refeitos


def trocas_painel(rel, texto):
    pasta = rel.split('/')[1]
    ident = pasta[len('painel-'):]
    m = re.search(r'var K="painel-sala-([a-z0-9-]+)",ID="([a-z0-9-]+)",CARTOES=', texto)
    if not m or m.group(1) != ident or m.group(2) != ident:
        raise FormaDesconhecida(f'{rel}: script do painel: não encontrei var K="painel-sala-{ident}",ID="{ident}",CARTOES=')
    cartoes_antigo, cartoes_novo, material, sel_antigo, sel_novo, refeitos = relampago_do_painel(rel, texto, ident)
    atlas = '<button type="button" data-atlas title="A">Quem sou eu?</button>' in texto
    variantes = [PAINEL_ATLAS_ANTIGO % v for v in PAINEL_ATLAS_VARIANTES if PAINEL_ATLAS_ANTIGO % v in texto]
    if len(variantes) != 1:
        raise FormaDesconhecida(f'{rel}: script do «Quem sou eu?» desconhecido')
    seletor = ([('seletor do relâmpago: os enunciados que ficaram para trás passam aos cartões atuais da lição '
                 f'({refeitos})', sel_antigo, sel_novo)] if refeitos else [])
    return seletor + [
        ('CSS: código da sala no cabeçalho; a grelha passa a uma coluna (sem placar)',
         PAINEL_CSS_SALACOD + 'main.grelha{flex:1;display:grid;grid-template-columns:1fr minmax(300px,34%);gap:20px;padding:0 24px 16px}',
         'main.grelha{flex:1;display:grid;grid-template-columns:1fr;gap:20px;padding:0 24px 16px}'),
        ('CSS: placar e estado do canal', PAINEL_CSS_PLACAR + 'footer.comandos{', 'footer.comandos{'),
        ('CSS: sorteio, barras da votação e respostas ao relâmpago saem; entram o material do relâmpago e o QR grande',
         PAINEL_CSS_SORTEIO + '@keyframes pulsa{', PAINEL_CSS_NOVO + '@keyframes pulsa{'),
        ('CSS: ecrã estreito (a grelha já tem uma coluna)', '@media (max-width:900px){main.grelha{grid-template-columns:1fr}.qr{',
         '@media (max-width:900px){.qr{'),
        ('cabeçalho: código da sala', '<div class="sala-cod">Sala <b data-cod>—</b></div></header>', '</header>'),
        ('pedido inicial', f'<h1 data-pedido>{PAINEL_PEDIDO_ANTIGO}</h1>', f'<h1 data-pedido>{PAINEL_PEDIDO_NOVO}</h1>'),
        ('instruções do painel', PAINEL_COMO, PAINEL_COMO_NOVO_ATLAS if atlas else PAINEL_COMO_NOVO),
        ('placar', PAINEL_PLACAR + '</main>', '</main>'),
        ('rodapé: Nova sala e Limpar o placar saem; entra «Voltar ao início»',
         '<div class="grupo"><button type="button" data-nova>Nova sala</button><button type="button" class="sec" data-projetar title="F">Projetar</button><button type="button" class="sec" data-limpar title="Limpar o placar">Limpar</button></div>',
         PAINEL_INICIO_NOVO),
        ('rodapé: sorteio, votação e código do aluno; Esc só para o cronómetro', PAINEL_RODAPE_SALA, PAINEL_ESC_NOVO),
        ('canal window.EPISala (ntfy.sh) passa à limpeza', EPISALA_SCRIPT, LIMPEZA_SCRIPT),
        ('script: chave da sala guardada', m.group(0), f'var ID="{ident}",CARTOES='),
        ('script: estado da sala, ls() e gravar() saem; os cartões do relâmpago ganham o material da lição',
         cartoes_antigo + PAINEL_JS_ESTADO, cartoes_novo + ',MATERIAL=' + material + ',crono=null,tPistas=null;\n' + PAINEL_MATERIAL_JS),
        ('script: canal, placar ao vivo, respostas e votos', PAINEL_JS_CANAL + 'function contar(seg,aoFim){',
         'function contar(seg,aoFim){'),
        ('script: enviar(), Nova sala e Limpar', PAINEL_JS_ENVIAR + '$("[data-projetar]").onclick=', '$("[data-projetar]").onclick='),
        ('script: pausa só no projetor', PAINEL_JS_PAUSA,
         'contar(min*60,function(){pedido("Tempo","' + PAINEL_TEMPO_NOVO + '")});pedido("Pausa de "+min+(min===1?" minuto":" minutos"),"Cartões "+de+" a "+ate+", no telemóvel");$("[data-extra]").innerHTML=""};'),
        ('script: relâmpago só no projetor, com o material do cartão', PAINEL_JS_RELAMPAGO, PAINEL_RELAMPAGO_JS),
        ('script: Atlas «Quem sou eu?» sem envio, uma pista por cada terço do tempo e a resposta no fim',
         variantes[0], PAINEL_ATLAS_JS),
        ('script: sorteio, votação, fecho nos telemóveis e código do aluno saem; Esc para o cronómetro, I volta ao início',
         PAINEL_JS_SORTEIO_ATE_ADD, PAINEL_FECHA_INICIO_JS),
        ('teclas S (sorteio) e V (votação) saem; entram A (o botão já a anunciava) e I',
         'else if(k==="s")$("[data-sorteio]").click();else if(k==="v")$("[data-v-p]").focus();else if(k==="f")',
         PAINEL_TECLAS_JS),
        ('retoma da sala guardada (6 h)', '$("[data-fecha]").click()});' + PAINEL_JS_RETOMA, '$("[data-fecha]").click()});\n'),
    ]


def trocas_indice(rel, texto):
    t = [('CSS: .casca-menu .sala', CASCA_MENU_SALA + '.c-grelha{', '.c-grelha{'),
         ('canal window.EPISala (ntfy.sh) passa à limpeza', EPISALA_SCRIPT, LIMPEZA_SCRIPT)]
    if 'if(window.EPISala){var S=EPISala.sala();' in texto:
        t.append(('Desafio da unidade: sem envio do resultado para a sala', INDICE_DESAFIO_ENVIO, 'if(festa)surpresa(u);'))
    return t


def trocas_atlas(rel, texto):
    return [
        ('CSS: formulário da sala', ATLAS_CSS_SALA + '.final{text-align:center}', '.final{text-align:center}'),
        ('CSS: .casca-menu .sala', CASCA_MENU_SALA + '.c-grelha{', '.c-grelha{'),
        ('botão «Sala de aula»', '<p class="a-acoes"><button type="button" class="c-sec" data-sala>Sala de aula</button></p>\n<details class="metodo-l">',
         '\n<details class="metodo-l">'),
        ('canal window.EPISala (ntfy.sh) passa à limpeza', EPISALA_SCRIPT, LIMPEZA_SCRIPT),
        ('fim de cada ronda: sem envio para o mapa da turma',
         'PEND={p:p,k:k,ok:ok,quase:!ok&&st.certas===precisa-1}}enviarSala()},', 'PEND={p:p,k:k,ok:ok,quase:!ok&&st.certas===precisa-1}}},'),
        ('comentário das folhas', '// ── folhas: pessoa, todas as pessoas, passaporte, sala, final',
         '// ── folhas: pessoa, todas as pessoas, passaporte, final'),
        ('enviarSala(), sala() e o botão', ATLAS_JS_SALA, '$("[data-passaporte]").onclick=passaporte;\n'),
    ]


def pagina_mapa():
    """A página curta que leva ao Atlas: o molde das outras páginas que mudaram de sítio (web.mjs, redireciona)."""
    molde = (ROOT / 'm1/percurso-do-modulo-m1/index.html').read_bytes().decode('utf-8')
    antigo_url, antigo_tit = f'{SITIO}/m1/', 'Percurso do módulo 1'
    if (molde.count(antigo_url) != 3 or molde.count(antigo_tit) != 2
            or 'Esta página mudou de sítio: <a href=' not in molde or '<script>' in molde.split('</style>', 1)[0]):
        raise FormaDesconhecida('m1/percurso-do-modulo-m1/index.html: o molde da página que mudou de sítio não é o conhecido')
    pagina = molde.replace(antigo_url, f'{SITIO}/atlas/').replace(antigo_tit, 'Atlas Lusófono')
    return pagina.replace('</main></body>', '</main>' + LIMPEZA_SCRIPT + '</body>')


def trocas_mapa(rel, texto):
    for marca in ('<title>Atlas Lusófono · mapa da turma</title>', EPISALA_SCRIPT,
                  'cod=sessionStorage.getItem("epi-atlas-sala")||EPISala.codigo()', 'EPISala.ligar(cod,function(m){'):
        if texto.count(marca) != 1:
            raise FormaDesconhecida(f'{rel}: o mapa da turma não é o conhecido (falta {marca[:60]!r})')
    return [('a página inteira passa à página curta que leva ao Atlas (com a limpeza)', texto, pagina_mapa())]


def trocas_raiz(rel, texto):
    return [('limpeza da Sala antes de exportar ou repor o progresso', PROGRESSO_INICIO, LIMPEZA_SCRIPT + PROGRESSO_INICIO)]


TIPOS = {'licao': trocas_licao, 'painel': trocas_painel, 'indice': trocas_indice, 'atlas': trocas_atlas, 'mapa': trocas_mapa}


def tipo_de(rel):
    if re.fullmatch(r'm[1-9]/licao-m[1-9]-f\d+/index\.html', rel):
        return 'licao'
    if re.fullmatch(r'm[1-9]/painel-m[1-9]-f\d+/index\.html', rel):
        return 'painel'
    if re.fullmatch(r'm[1-9]/index\.html', rel):
        return 'indice'
    return {'atlas/index.html': 'atlas', 'atlas/sala/index.html': 'mapa'}.get(rel)


def publicados():
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if p.is_file() and p.suffix in ('.html', '.js') and rel.parts[0] not in FORA:
            yield rel.as_posix(), p


def congelados():
    """As páginas cujo conteúdo os testes congelam por hash ou digest."""
    fx = ROOT / 'tests/fixtures'
    ler_json = lambda nome: json.loads((fx / nome).read_text('utf-8'))
    paginas = set()
    for modulo in ler_json('task-route-lesson-content-before.json').values():
        paginas.update(modulo['files'])
    paginas.update(f'm{m}/index.html' for m in ler_json('module-layout-before.json')['modules'])
    for nome in ('m1-grammar-pilot-edits-20261027.json', 'apoios-tabelas-edits-20261027.json'):
        paginas.update(ler_json(nome)['files'])
    return paginas


def sha(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


def ler(p):
    return p.read_bytes().decode('utf-8')


def commit_atual():
    try:
        return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    ap = argparse.ArgumentParser(description='Desliga a Sala de aula nas páginas publicadas (28/10/2026).')
    ap.add_argument('--verificar', action='store_true', help='não escreve; sai com 1 se houver alguma coisa por fazer')
    args = ap.parse_args()
    antigo = json.loads(MANIFESTO.read_text('utf-8')) if MANIFESTO.exists() else {}
    registos_antigos = antigo.get('files', {})
    congel = congelados()
    escrever, registos = {}, {}
    erros = {'forma': [], 'manifesto': []}
    paginas = {t: [] for t in ('licao', 'painel', 'indice', 'atlas', 'mapa', 'raiz')}
    contagem = Counter()
    for rel, p in publicados():
        texto = ler(p)
        tipo = tipo_de(rel)
        if rel == 'index.html':
            continue
        if tem_sala(texto):
            if tipo is None:
                erros['forma'].append(f'{rel}: tem marcas da Sala ({", ".join(marcas(texto))}) numa página que o script não conhece')
                continue
            try:
                novo, edits = aplicar(rel, texto, TIPOS[tipo](rel, texto))
            except FormaDesconhecida as e:
                erros['forma'].append(str(e))
                continue
            escrever[rel] = novo
            contagem[tipo + ' desligada agora'] += 1
            paginas[tipo].append(rel)
            if rel in congel:
                registos[rel] = {'base_sha256_lf': sha(texto), 'after_sha256_lf': sha(novo), 'edits': edits}
        elif LIMPEZA_SCRIPT in texto:
            if tipo is None:
                erros['forma'].append(f'{rel}: tem a limpeza da Sala numa página que o script não conhece')
                continue
            paginas[tipo].append(rel)
            contagem[tipo + ' já desligada'] += 1
            reg = registos_antigos.get(rel)
            if not reg:
                # 28/10/2026 (revisão): uma página congelada depois do corte já foi congelada sem a Sala; não há nada
                # a desfazer por este manifesto
                if rel in congel:
                    contagem['congelada depois do corte (fora do manifesto)'] += 1
                continue
            try:
                confirmar_congelada(rel, tipo, texto, reg)
            except ManifestoDesatualizado as e:
                erros['manifesto'].append(str(e))
                continue
            registos[rel] = reg
    raiz = ler(ROOT / 'index.html')
    if LIMPEZA_SCRIPT not in raiz:
        try:
            escrever['index.html'], _ = aplicar('index.html', raiz, trocas_raiz('index.html', raiz))
            contagem['raiz desligada agora'] += 1
        except FormaDesconhecida as e:
            erros['forma'].append(str(e))
    else:
        contagem['raiz já desligada'] += 1
    paginas['raiz'].append('index.html')
    avisos = {'forma': 'AVISO: há formas da Sala que o script não reconhece; não escrevi nada.',
              'manifesto': ('AVISO: o manifesto da Sala já não se desfaz e refaz nestas páginas congeladas (mudaram num '
                            'bloco que as trocas tocam, ou as trocas do script mudaram); não escrevi nada.')}
    if any(erros.values()):
        for chave, lista in erros.items():
            if not lista:
                continue
            print(avisos[chave], file=sys.stderr)
            grupos = {}
            for e in lista:
                rel, _, motivo = e.partition(': ')
                grupos.setdefault(motivo, []).append(rel)
            for motivo, rels in grupos.items():
                print(f'  {motivo}: {len(rels)} página(s): ' + ', '.join(rels[:6]) + (' …' if len(rels) > 6 else ''), file=sys.stderr)
        return 2
    manifesto = {'base_commit': antigo.get('base_commit') or commit_atual(), '_nota': NOTA,
                 'paginas': {t: sorted(v) for t, v in paginas.items()},
                 'files': {rel: registos[rel] for rel in sorted(registos)}}
    texto_manifesto = json.dumps(manifesto, ensure_ascii=False, indent=1) + '\n'
    muda_manifesto = not MANIFESTO.exists() or MANIFESTO.read_text('utf-8') != texto_manifesto
    for chave in sorted(contagem):
        print(f'{chave}: {contagem[chave]}')
    print('páginas com a limpeza: ' + ', '.join(f'{t} {len(v)}' for t, v in paginas.items()))
    print(f'no manifesto (congeladas): {len(registos)}')
    if args.verificar:
        if escrever or muda_manifesto:
            print(f'POR FAZER: {len(escrever)} página(s)' + (' e o manifesto' if muda_manifesto else ''))
            return 1
        print('Nada a mudar: a Sala já está desligada.')
        return 0
    if not escrever and not muda_manifesto:
        print('Nada a mudar: a Sala já está desligada.')
        return 0
    for rel, novo in sorted(escrever.items()):
        (ROOT / rel).write_bytes(novo.encode('utf-8'))
    if muda_manifesto:
        MANIFESTO.write_text(texto_manifesto, 'utf-8')
    print(f'Escritas: {len(escrever)} página(s)' + (' e o manifesto' if muda_manifesto else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
