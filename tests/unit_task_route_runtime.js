const fs=require("fs"),vm=require("vm"),assert=require("assert");
const code=fs.readFileSync("assets/unit-task-route.js","utf8");
for(const unavailable of [false,true]){
 const stored={"licao-m1-f01":JSON.stringify({lida:true}),"epi-pt-longos":JSON.stringify({feitas:{"m1-voz":true}})};
 const writes=[];const progress={},taskChip={textContent:"90 min"},entry={setAttribute(k,v){this[k]=v}},label={};
 const items={"m1-f01":{querySelector(s){if(s==="[data-chip]")return {};if(s==="[data-k]")return {};return null;}},
 "m1-f02":{querySelector(s){if(s==="[data-chip]")return {};if(s==="a")return {getAttribute(){return "./licao-m1-f02/"},querySelector(){return {textContent:"Segunda lição"}}};return null;}}};
 const section={querySelector(s){if(s==="[data-prog]")return progress;if(s==="[data-barra]")return {style:{}};if(s==="[data-ok]")return {};const match=s.match(/data-passo="([^"]+)"/);return match?items[match[1]]:null;}};
 const document={hidden:false,querySelector(s){if(s.startsWith(".unidade"))return section;if(s==="[data-module-next]")return entry;if(s==="[data-module-next-label]")return label;return null;},
 querySelectorAll(){return []},getElementById(){return null},addEventListener(){}};
 const window={addEventListener(){}};
 const localStorage={getItem(k){if(unavailable)throw Error("blocked");return stored[k]||null},setItem(){writes.push("write")},removeItem(){writes.push("delete")}};
 const context={window,document,localStorage,location:{search:""},URLSearchParams};
 vm.runInNewContext(code,context);
 window.EPIUnitTaskRoute.mount({module:"M1",units:[{n:1,passos:[{id:"m1-f01",licao:"m1-f01"},{id:"m1-f02",licao:"m1-f02"}]}]});
 assert(progress.textContent.includes((unavailable?"0":"1")+" de 2 lições"));
 assert(progress.textContent.includes("tarefa individual com consulta"));
 assert.strictEqual(taskChip.textContent,"90 min");assert.deepStrictEqual(writes,[]);
 assert(window.EPIUnitTaskRoute.historicalKeys("M7",5).includes("percurso-sintese-M7-u5"));
 if(!unavailable)assert(window.EPIUnitTaskRoute.lessonDone({exs:["m1-voz"]}));
 // 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 usa o mesmo percurso, também sem escrever no aparelho.
 progress.textContent="";
 window.EPIUnitTaskRoute.mount({module:"M2",units:[{n:1,passos:[{id:"m1-f01",licao:"m1-f01"},{id:"m1-f02",licao:"m1-f02"}]}]});
 assert(progress.textContent.includes("de 2 lições"));assert.deepStrictEqual(writes,[]);
 progress.textContent="";window.EPIUnitTaskRoute.mount({module:"M3",units:[{n:1,passos:[]}]});assert.strictEqual(progress.textContent,"");
}
console.log("Route runtime OK: storage available/unavailable; no card nodes; no completion writes.");
