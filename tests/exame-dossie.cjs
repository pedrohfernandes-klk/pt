const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync(require('path').join(__dirname,'../assets/exame/dossier.js'),'utf8');
class Reader{readAsDataURL(b){b.arrayBuffer().then(x=>{this.result='data:'+b.type+';base64,'+Buffer.from(x).toString('base64');this.onload()}).catch(()=>this.onerror())}}
// Minimal parser double: tests import control flow only, not browser DOMParser conformance.
class Parser{parseFromString(s){return{querySelector(){const attrs=s.match(/<script([^>]*)>/i)[1];const get=k=>{const m=attrs.match(new RegExp('\\b'+k+'=["\x27]([^"\x27]*)["\x27]','i'));return m?m[1]:''};return{id:get('id'),type:get('type'),hasAttribute:k=>new RegExp('\\b'+k+'\\s*=','i').test(attrs)}}}}}
const ctx=vm.createContext({Blob,Uint8Array,TextEncoder,console,URL,atob,btoa,FileReader:Reader,DOMParser:Parser,window:{},setTimeout,clearTimeout});
vm.runInContext(source.replace('window.PTExameDossier =','window.__test={safeJSON:safeJSON,metadata:metadata,validatePhoto:validatePhoto,decodePhoto:decodePhoto,bytes:bytes,setRows:function(v){var rows=v;listEntries=async function(){return rows};mutate=async function(fn){var next=rows.slice(),puts=[];var result=fn(rows,{put:function(e){puts.push(e)},delete:function(id){next=next.filter(function(e){return e.sessionId!==id})}});puts.forEach(function(e){next=next.filter(function(x){return x.sessionId!==e.sessionId}).concat([e])});rows=next;return result};return function(){return rows}}};window.PTExameDossier ='),ctx);
const tests=`(async function(){
var A=window.PTExameDossier,T=window.__test,passes=[];
function ok(name,fn){fn();passes.push(name)}
async function rejects(name,fn){var failed=false;try{await fn()}catch(e){failed=true}if(!failed)throw Error('Expected rejection: '+name);passes.push(name)}
ok('recursive prototype keys rejected',function(){for(var key of ['__proto__','constructor','prototype']){var bad=JSON.parse('{"x":{"'+key+'":1}}');var threw=false;try{T.safeJSON(bad)}catch(e){threw=true}if(!threw)throw Error(key)}});
var jpg=new Blob([new Uint8Array([255,216,255,224,0,0,0,0,0,0,0,0,0,0,0,0])],{type:'image/jpeg'});
var photo={id:'p1',name:'folha.jpg',type:'image/jpeg',size:jpg.size,blob:jpg};
await T.validatePhoto(photo);passes.push('JPEG magic validated');
await rejects('spoofed PNG MIME rejected',function(){return T.validatePhoto({id:'p2',name:'bad.png',type:'image/png',size:jpg.size,blob:new Blob([jpg],{type:'image/png'})})});
await rejects('unknown entry fields rejected',function(){return A.saveEntry({sessionId:'s1',session:{},title:'t',evil:true})});
var get=T.setRows([]);
await A.saveEntry({sessionId:'s1',title:'<img src=x onerror=alert(1)>',session:{source:'</script><script>alert(1)</script>',writing:'Escreve',correction:{criteria:'Lê'}},notes:'<b>notas</b>',answers:{one:'resposta'},checklist:{done:true},photos:[photo],updatedAt:'2026-10-19T10:00:00Z'});
await A.saveEntry({sessionId:'s1',title:'t',session:{source:'</script><script>alert(1)</script>',writing:'Escreve',correction:'Critério'},notes:'nova nota',updatedAt:'2026-10-19T11:00:00Z'});
ok('save without photos preserves originals',function(){if(get()[0].photos.length!==1)throw Error('lost photos')});
var backup=await A.exportHTML(),html=await backup.text();
ok('standalone export contains one dataURL copy',function(){if((html.match(/data:image\\/jpeg;base64,/g)||[]).length!==1)throw Error('duplicated or missing original')});
ok('export scripts JSON-escaped and text escaped',function(){if(html.includes('</script><script>alert(1)'))throw Error('script breakout');if(!html.includes('\\\\u003c/script'))throw Error('JSON escaping');if(!html.includes('Enunciado e fontes')||!html.includes('Correção e critérios')||!html.includes('data-photo="p1"'))throw Error('missing view')});
get=T.setRows([]);var imported=await A.importHTML(backup);
ok('HTML round trip metadata and photo bytes',function(){if(imported!==1||get()[0].notes!=='nova nota'||get()[0].photos[0].size!==16)throw Error('round trip')});
var original=Buffer; // host Buffer is intentionally unavailable; byte comparison uses Uint8Array below.
})()`;
// No Buffer exposure in the application context; replace the final placeholder with further portable checks.
const finalTests=tests.replace('var original=Buffer; // host Buffer is intentionally unavailable; byte comparison uses Uint8Array below.',`
var arr=new Uint8Array(await get()[0].photos[0].blob.arrayBuffer());if(arr[0]!==255||arr[1]!==216||arr.length!==16)throw Error('changed binary');passes.push('original binary restored');
var count=await A.importHTML(backup);if(count!==0)throw Error('equal timestamp overwritten');passes.push('equal timestamp not overwritten');
get()[0].updatedAt='2026-10-19T12:00:00.000Z';count=await A.importHTML(backup);if(count!==0)throw Error('older overwrite');passes.push('older import not overwritten');
function packageHTML(entries){return new Blob(['<script id="pt-exame-dossier-data" type="application/json">'+JSON.stringify({format:'pt-exame-dossier',version:1,exportedAt:'2026-10-19T10:00:00Z',entries:entries})+'</script>'],{type:'text/html'})}
var clean={sessionId:'s2',title:'two',session:{},notes:'',revisedText:'',answers:{},checklist:{},updatedAt:'2026-10-19T13:00:00Z',photos:[]};
var invalid=JSON.parse(JSON.stringify(clean));invalid.sessionId='s3';invalid.photos=[{id:'p3',name:'bad.png',type:'image/png',size:16,dataURL:'data:image/png;base64,/9j/4AAAAAAAAAAAAAAAAA=='}];
await rejects('invalid late entry leaves all previous entries unchanged',function(){return A.importHTML(packageHTML([clean,invalid]))});if(get().length!==1||get()[0].sessionId!=='s1')throw Error('partial import');
await rejects('duplicate session ids rejected',function(){return A.importHTML(packageHTML([clean,clean]))});
await rejects('unknown photo metadata rejected',function(){var bad=JSON.parse(JSON.stringify(clean));bad.photos=[{id:'p1',name:'x',type:'image/jpeg',size:16,dataURL:'x',extra:1}];return A.importHTML(packageHTML([bad]))});
await rejects('wrong data URL and size rejected',function(){return T.decodePhoto({id:'p1',name:'x.jpg',type:'image/jpeg',size:16,dataURL:'data:text/html;base64,AAAA'})});
await rejects('fifth photo rejected',function(){return A.saveEntry({sessionId:'s4',session:{},photos:[photo,photo,photo,photo,photo]})});
await rejects('64MiB decoded aggregate enforced',function(){T.bytes([{photos:[{id:'x',name:'x',type:'image/jpeg',size:64*1024*1024}],session:{}}])});
if(await A.importHTML(packageHTML([clean]))!==1||get().length!==2)throw Error('new merge');passes.push('new entry merged without deleting old entry');
if(!html.includes("default-src 'none'")||!html.includes('img-src data:'))throw Error('CSP');passes.push('export network disabled by CSP');
return {passed:passes.length,tests:passes,limits:['IndexedDB transaction and quota require real browser tests.','DOMParser is a minimal double; inert parsing and zero network need browser verification.','Image magic tests do not certify complete image decoding.']};
`);
vm.runInContext(finalTests,ctx).then(result=>{console.log(JSON.stringify(result,null,2))}).catch(e=>{console.error(e);process.exitCode=1});
