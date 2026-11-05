<!doctype html>
<html lang="pt-PT" data-appearance-site="pt" data-appearance-family="cards">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>@@TITLE@@ | Português</title>
<link rel="stylesheet" href="../../assets/pt-lessons/lesson.css">
<script defer src="../../assets/pt-lessons/casca.js"></script>
<script defer src="../../assets/pt-lessons/jogo.js?v=20261021-ux06"></script>
<link rel="stylesheet" href="../../assets/appearance.css?v=20261025-universal-1">
<script src="../../assets/appearance.js?v=20261025-universal-1"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;display=swap">
<!-- 05/11/2026: decisão 153, a peça comum dos créditos atrás de um «i» (igual no Português e no Lente). -->
<link rel="stylesheet" href="../../assets/info-i.css?v=20261105">
<script defer src="../../assets/info-i.js?v=20261105"></script>
<style>
.jogo .tit,.jogo .q{text-wrap:balance}
.jogo .pares{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
/* 02/11/2026: as palavras dos pares ficam inteiras (sem hifenização automática); só uma palavra maior do que a coluna parte. */
.jogo .pares .op,.jogo .pares .op .tx{min-width:0;-webkit-hyphens:manual;hyphens:manual;overflow-wrap:break-word}
.casca-topo .c-marca{min-width:44px;justify-content:center}
.casca-folha .c-veredito .c-pts{color:var(--suave)}
.jogo .acoes-fim a,.jogo .depois a{display:inline-flex;align-items:center;min-height:44px}
.jogo .xp{color:var(--suave)}
@media(max-width:360px){.jogo .pares{column-gap:12px}.jogo .pares .op{padding-left:8px;padding-right:8px;gap:6px;font-size:.875rem}.jogo .pares .op.ligado{padding-left:7px;padding-right:7px}}
@media(max-width:480px){.jogo .pares .op .marca-par{position:absolute;top:-9px;background:var(--papel)}.jogo .pares .esq .marca-par{right:-9px}.jogo .pares .dir .marca-par{left:-9px}.jogo .pares .op .marca-par:empty{display:none}}
.jogo .ler blockquote{margin:1.25rem 0;padding:0 0 0 1rem;border-left:2px solid currentColor;line-height:1.65}
.jogo .ler h3{font-size:1.3em;line-height:1.3}
.jogo .ler table{width:100%;border-collapse:collapse;font-size:.9em}
.jogo .ler th,.jogo .ler td{text-align:left;vertical-align:top;padding:.35em;border-bottom:1px solid currentColor}
.jogo .ler .fig{margin:1.25rem 0}.jogo .ler .fig img{display:block;margin:auto;max-width:100%;max-height:38vh;width:auto;height:auto;object-fit:contain}.jogo .ler .fig figcaption{font-size:.85em;line-height:1.5}.jogo .ler .fig td{overflow-wrap:anywhere}
/* 05/11/2026: decisão 153. No documento visual, o «i» fica logo por baixo do canto direito da imagem (a imagem continua centrada e a ligação «Abrir a imagem inteira» continua filha da figura); a tabela de identificação abre por baixo, centrada, com a largura da coluna (até 34rem), e não alarga nem desloca a imagem. */
.jogo .ler .documento{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);container-type:inline-size}.jogo .ler .documento>a{grid-column:2;min-width:0}.jogo .ler .documento>details.info-i{grid-column:2;justify-self:end}.jogo .ler .documento>details.info-i[open]{justify-self:stretch;contain:inline-size}.jogo .ler .documento>details.info-i[open]>.info-i-texto{inline-size:min(100cqi,34rem);margin-inline-start:calc((100% - min(100cqi,34rem))/2)}.jogo .ler .documento>figcaption{grid-column:1/-1}
@media(min-width:1024px){:root{--col:min(850px,100%)}.casca .jogo .ler{font-size:1.24rem;line-height:1.62}.casca .jogo .q{font-size:1.6rem}.casca .jogo .tit{font-size:1.6rem}.casca .jogo .tit.cartaz{font-size:clamp(2.4rem,3.2vw,3rem)}}
</style>
</head>
<body data-unit-return="../#unidade-pedagogica-@@UNIT@@" data-unit-number="@@UNIT@@">
<div class="casca" data-casca>
<header class="casca-topo"><a class="c-marca" href="../#unidade-pedagogica-@@UNIT@@" aria-label="Voltar à unidade @@UNIT@@ do módulo @@NUMBER@@">@@MODULE@@</a><span class="c-num" data-c-num></span><button type="button" class="c-barra" data-c-barra aria-label="Ver os cartões já feitos" disabled><svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg></button><span class="c-modo" data-c-modo hidden></span><button type="button" class="c-ic" data-c-som aria-pressed="false" aria-label="Som"><span class="c-roda">♪</span></button><button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false"><span class="c-tres"></span></button></header>
<h1 class="c-sr">@@TITLE@@</h1>
<main class="casca-corpo" tabindex="-1"><div id="baralho" class="jogo-alvo"></div></main>
<footer class="casca-acoes" data-c-acoes></footer>
<section class="casca-folha" data-c-folha role="status" aria-live="polite" hidden></section>
<div class="casca-menu" data-c-painel hidden><div class="c-menu-in" role="dialog" aria-label="Menu"><div class="c-menu-cab"><p>Módulo @@NUMBER@@<br>Unidade @@UNIT@@</p><button type="button" class="c-ic" data-c-fecha-menu aria-label="Fechar o menu">✕</button></div><nav aria-label="Navegação da lição"><a href="../#@@ID@@">Esta lição no percurso</a><a href="@@PREVIOUS@@">Lição anterior</a><a href="@@NEXT@@">Lição seguinte</a></nav><p class="c-menu-extra">As citações têm crédito junto ao texto. Os exemplos criados estão identificados. O progresso fica neste aparelho.</p></div></div>
</div>
<noscript>Esta lição precisa de JavaScript. <a href="../">Voltar ao módulo</a>.</noscript>
<script>
window.addEventListener('DOMContentLoaded',function(){"use strict";
var K="licao-@@ID@@",CARTOES=@@CARDS@@;
function save(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
var C=EPICasca.pagina();
EPIJogo.montar({casca:C,el:document.getElementById("baralho"),marca:"@@MODULE@@",itens:CARTOES,chave:K,titulo:@@JSON_TITLE@@,variar:false,gestalt:true,percurso:"../#@@ID@@",seguinte:"@@NEXT@@",depois:'<p><a href="../#@@ID@@">Voltar ao percurso</a></p>',fim:function(){save(K+"-a1",{lida:true,t:Date.now()})}});
if(!/[?&]projetar=1(&|$)/.test(location.search))save("epi-ultima",{id:"@@ID@@",m:"@@MODULE@@",t:Date.now()});
});
</script>
<script defer src="../../assets/projection-launcher.js?v=20261019.4" data-site="pt"></script>
</body></html>
