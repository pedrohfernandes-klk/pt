(function () {
  'use strict';
  var DB_NAME = 'pt-exame-dossie-v1', STORE = 'entries', FORMAT = 'pt-exame-dossier', VERSION = 1;
  var MiB = 1024 * 1024, PHOTO_LIMIT = 8 * MiB, TOTAL_LIMIT = 64 * MiB;
  var FILE_LIMIT = Math.ceil(TOTAL_LIMIT * 4 / 3) + 4 * MiB;
  var ENTRY_KEYS = ['sessionId', 'title', 'session', 'notes', 'revisedText', 'answers', 'checklist', 'updatedAt', 'photos'];
  var PHOTO_KEYS = ['id', 'name', 'type', 'size', 'blob'];
  var PORTABLE_PHOTO_KEYS = ['id', 'name', 'type', 'size', 'dataURL'];
  var TYPES = ['image/jpeg', 'image/png', 'image/webp'];
  var opening = null;
  function fail(message) { throw new Error(message); }
  function own(o, k) { return Object.prototype.hasOwnProperty.call(o, k); }
  function plain(o) { return o !== null && typeof o === 'object' && (Object.getPrototypeOf(o) === Object.prototype || Object.getPrototypeOf(o) === null); }
  function allow(o, keys, label) {
    if (!plain(o)) fail(label + ': objeto inválido.');
    Object.keys(o).forEach(function (k) { if (keys.indexOf(k) < 0) fail(label + ': campo não permitido (' + k + ').'); });
  }
  function safeJSON(value, depth) {
    depth = depth || 0;
    if (depth > 24) fail('Os dados têm demasiados níveis.');
    if (value === null || typeof value === 'boolean') return value;
    if (typeof value === 'number') { if (!Number.isFinite(value)) fail('Número inválido.'); return value; }
    if (typeof value === 'string') { if (value.length > Math.ceil(PHOTO_LIMIT * 4 / 3) + 64) fail('Um campo de dados é demasiado grande.'); return value; }
    if (Array.isArray(value)) { if (value.length > 10000) fail('Lista demasiado longa.'); return value.map(function (x) { return safeJSON(x, depth + 1); }); }
    if (!plain(value) || Object.keys(value).length > 10000) fail('Dados JSON inválidos.');
    var copy = {};
    Object.keys(value).forEach(function (k) {
      if (k === '__proto__' || k === 'constructor' || k === 'prototype') fail('Campo inseguro nos dados.');
      copy[k] = safeJSON(value[k], depth + 1);
    });
    return copy;
  }
  function text(v, max, label, fallback) {
    if (v === undefined && fallback !== undefined) return fallback;
    if (typeof v !== 'string' || v.length > max || /\u0000/.test(v)) fail(label + ': texto inválido.');
    return v;
  }
  function id(v, label) {
    if (typeof v !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._:-]{0,119}$/.test(v)) fail(label + ': identificador inválido.');
    return v;
  }
  function stamp(v) {
    if (v === undefined) return new Date().toISOString();
    if (typeof v !== 'string' || !/^\d{4}-\d\d-\d\dT/.test(v) || !Number.isFinite(Date.parse(v))) fail('Data de atualização inválida.');
    return new Date(v).toISOString();
  }
  function metadata(e) {
    allow(e, ENTRY_KEYS, 'Registo');
    var answers = e.answers === undefined ? {} : e.answers, checklist = e.checklist === undefined ? {} : e.checklist;
    if (!plain(answers) || !plain(checklist) || !plain(e.session)) fail('A sessão, as respostas e a lista de verificação devem ser objetos.');
    return { sessionId: id(e.sessionId, 'Sessão'), title: text(e.title, 300, 'Título', ''), session: safeJSON(e.session),
      notes: text(e.notes, MiB, 'Notas', ''), revisedText: text(e.revisedText, MiB, 'Texto revisto', ''),
      answers: safeJSON(answers), checklist: safeJSON(checklist), updatedAt: stamp(e.updatedAt) };
  }
  function photoName(v) {
    v = text(v, 255, 'Nome da fotografia');
    if (!v.trim() || /[\x00-\x1f\x7f/\\]/.test(v)) fail('Nome da fotografia inválido.');
    return v;
  }
  async function validatePhoto(p) {
    allow(p, PHOTO_KEYS, 'Fotografia');
    id(p.id, 'Fotografia'); photoName(p.name);
    if (TYPES.indexOf(p.type) < 0 || !(p.blob instanceof Blob) || p.blob.type !== p.type || !Number.isSafeInteger(p.size) || p.size !== p.blob.size || p.size < 12 || p.size > PHOTO_LIMIT) fail('Fotografia inválida: usa JPEG, PNG ou WebP, até 8 MiB.');
    var h = new Uint8Array(await p.blob.slice(0, 16).arrayBuffer()), real = '';
    if (h[0] === 255 && h[1] === 216 && h[2] === 255) real = 'image/jpeg';
    if (h[0] === 137 && h[1] === 80 && h[2] === 78 && h[3] === 71 && h[4] === 13 && h[5] === 10 && h[6] === 26 && h[7] === 10) real = 'image/png';
    if (String.fromCharCode.apply(null, h.slice(0, 4)) === 'RIFF' && String.fromCharCode.apply(null, h.slice(8, 12)) === 'WEBP') real = 'image/webp';
    if (real !== p.type) fail('O conteúdo da fotografia não corresponde ao formato indicado.');
    return { id: p.id, name: p.name, type: p.type, size: p.size, blob: p.blob };
  }
  async function validatePhotos(photos) {
    if (!Array.isArray(photos) || photos.length > 4) fail('Cada registo pode ter até quatro fotografias.');
    var seen = {}, out = [];
    for (var p of photos) { var q = await validatePhoto(p); if (seen[q.id]) fail('Identificador de fotografia repetido.'); seen[q.id] = true; out.push(q); }
    return out;
  }
  function bytes(entries) {
    var count = 0;
    entries.forEach(function (e) {
      var m = {}; ENTRY_KEYS.forEach(function (k) { if (k !== 'photos') m[k] = e[k]; });
      m.photos = (e.photos || []).map(function (p) { return { id: p.id, name: p.name, type: p.type, size: p.size }; });
      count += new Blob([JSON.stringify(m)]).size;
      (e.photos || []).forEach(function (p) { count += p.size; });
    });
    if (count > TOTAL_LIMIT) fail('O dossiê ultrapassa 64 MiB. Remove fotografias antes de guardar.');
    return count;
  }
  function db() {
    if (opening) return opening;
    opening = new Promise(function (resolve, reject) {
      var req;
      try { if (!window.indexedDB) fail('Este navegador não permite guardar o dossiê local.'); req = indexedDB.open(DB_NAME, 1); }
      catch (e) { reject(e); return; }
      req.onupgradeneeded = function () { if (!req.result.objectStoreNames.contains(STORE)) req.result.createObjectStore(STORE, { keyPath: 'sessionId' }); };
      req.onerror = function () { reject(new Error('Não foi possível abrir o dossiê local: ' + (req.error && req.error.name || 'armazenamento indisponível') + '.')); };
      req.onblocked = function () { reject(new Error('O dossiê está bloqueado noutra aba. Fecha-a e tenta novamente.')); };
      req.onsuccess = function () { var d = req.result; d.onversionchange = function () { d.close(); opening = null; }; resolve(d); };
    }).catch(function (e) { opening = null; throw e; });
    return opening;
  }
  async function listEntries() {
    var d = await db();
    return new Promise(function (resolve, reject) {
      var tx = d.transaction(STORE, 'readonly'), request = tx.objectStore(STORE).getAll(), rows;
      request.onsuccess = function () { rows = request.result; };
      tx.oncomplete = function () { resolve(rows.sort(function (a, b) { return Date.parse(b.updatedAt) - Date.parse(a.updatedAt); })); };
      tx.onerror = tx.onabort = function () { reject(new Error('Não foi possível ler o dossiê local.')); };
    });
  }
  async function getEntry(sessionId) { id(sessionId, 'Sessão'); return (await listEntries()).find(function (e) { return e.sessionId === sessionId; }) || null; }
  async function mutate(fn) {
    var d = await db();
    return new Promise(function (resolve, reject) {
      var tx = d.transaction(STORE, 'readwrite'), store = tx.objectStore(STORE), request = store.getAll(), result, problem;
      request.onsuccess = function () { try { result = fn(request.result, store); } catch (e) { problem = e; tx.abort(); } };
      tx.oncomplete = function () { resolve(result); };
      tx.onerror = tx.onabort = function () { reject(problem || new Error('Não foi possível guardar o dossiê. O armazenamento pode estar cheio ou indisponível.')); };
    });
  }
  async function saveEntry(entry) {
    var e = metadata(entry), explicit = own(entry, 'photos');
    if (explicit) e.photos = await validatePhotos(entry.photos);
    return mutate(function (rows, store) {
      var current = rows.find(function (x) { return x.sessionId === e.sessionId; });
      if (!explicit) e.photos = current ? current.photos : [];
      bytes(rows.filter(function (x) { return x.sessionId !== e.sessionId; }).concat([e])); store.put(e); return e;
    });
  }
  function randomId() { return window.crypto && crypto.randomUUID ? crypto.randomUUID() : 'photo-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2); }
  async function addPhotos(sessionId, files, sessionSnapshot) {
    id(sessionId, 'Sessão'); var input = Array.from(files || []);
    if (!input.length || input.length > 4) fail('Escolhe entre uma e quatro fotografias.');
    var photos = await validatePhotos(input.map(function (f) { return { id: randomId(), name: f.name, type: f.type, size: f.size, blob: f }; }));
    var snap = sessionSnapshot === undefined ? null : safeJSON(sessionSnapshot);
    if (snap !== null && !plain(snap)) fail('A sessão deve ser um objeto.');
    return mutate(function (rows, store) {
      var e = rows.find(function (x) { return x.sessionId === sessionId; });
      if (!e) { if (!snap) fail('Guarda a sessão antes de juntar fotografias.'); e = metadata({ sessionId: sessionId, title: typeof snap.title === 'string' ? snap.title : '', session: snap }); e.photos = []; }
      if (e.photos.length + photos.length > 4) fail('Cada registo pode ter até quatro fotografias.');
      e.photos = e.photos.concat(photos); e.updatedAt = new Date().toISOString();
      bytes(rows.filter(function (x) { return x.sessionId !== sessionId; }).concat([e])); store.put(e); return e;
    });
  }
  async function removePhoto(sessionId, photoId) {
    id(sessionId, 'Sessão'); id(photoId, 'Fotografia');
    return mutate(function (rows, store) { var e = rows.find(function (x) { return x.sessionId === sessionId; }); if (!e) fail('A sessão não existe neste dossiê.'); e.photos = e.photos.filter(function (p) { return p.id !== photoId; }); e.updatedAt = new Date().toISOString(); store.put(e); return e; });
  }
  async function deleteEntry(sessionId) { id(sessionId, 'Sessão'); return mutate(function (rows, store) { store.delete(sessionId); return rows.some(function (e) { return e.sessionId === sessionId; }); }); }
  function escapeHTML(v) { return String(v).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function render(v) {
    if (v === undefined || v === null) return '<p>—</p>';
    if (Array.isArray(v)) return '<ol>' + v.map(function (x) { return '<li>' + render(x) + '</li>'; }).join('') + '</ol>';
    if (plain(v)) return '<dl>' + Object.keys(v).map(function (k) { return '<dt>' + escapeHTML(k) + '</dt><dd>' + render(v[k]) + '</dd>'; }).join('') + '</dl>';
    return '<p class="text">' + escapeHTML(v) + '</p>';
  }
  // Textos compostos (27/10/2026): versos e parágrafos em texto simples, notas e crédito no fim.
  function readingText(source) {
    if (!Array.isArray(source.passages)) return source.excerpt;
    return source.passages.map(function (p) {
      var notes = [];
      function plainText(t) { return String(t || '').replace(/\{([^|{}]+)\|([^{}]+)\}/g, function (m, a, b) { notes.push(a + ': ' + b); return a; }).replace(/_([^_]+)_/g, '$1'); }
      var body = p.form === 'verso' ? (p.stanzas || []).map(function (st) { return st.map(plainText).join('\n'); }).join('\n\n')
        : (p.paragraphs || []).map(function (q) { return (q.n ? '[' + q.n + '] ' : '') + plainText(q.text); }).join('\n\n');
      return [(p.label ? 'Texto ' + p.label + '. ' : '') + plainText(p.head), body, notes.length ? 'Vocabulário: ' + notes.join('; ') + '.' : '', plainText(p.credit), p.note || ''].filter(Boolean).join('\n\n');
    }).join('\n\n');
  }
  function studyParts(p) {
    var s=p.session, w=s.writing||{}, c=s.correction||{}, source=s.source||{};
    var reading={'Título':source.title,'Autor ou origem':source.author,'Contexto':source.context,'Leitura':readingText(source),'Referência':source.url,'Nota':source.note};
    var writing={'Tarefa':w.prompt,'Tempo de escrita (minutos)':w.minutes,'Extensão':w.target,'Passos':w.instructions,'Critérios':w.criteria};
    var correction={'Tipo de apoio':c.kind,'Proposta':c.model,'Passos de revisão':Array.isArray(c.steps)?c.steps.map(function(x){return x.label+': '+x.detail;}):[],'O que evitar':c.pitfalls};
    var questions=(Array.isArray(s.warmup)?s.warmup:[]).concat(c.check?[c.check]:[]);
    var answers=questions.filter(function(q){return own(p.answers,q.id);}).map(function(q){var a=p.answers[q.id],choice=a&&Number.isInteger(a.choice)&&Array.isArray(q.options)?q.options[a.choice]:undefined;return {'Pergunta':q.q,'A minha escolha':choice,'Resposta esperada':Array.isArray(q.options)?q.options[q.answer]:undefined,'Explicação':q.feedback};});
    var checks=Array.isArray(w.criteria)?w.criteria.map(function(text,i){return (p.checklist['c'+i]?'Revisto: ':'Por rever: ')+text;}):[];
    return {reading:reading,writing:writing,correction:correction,answers:answers,checks:checks};
  }
  function dataURL(blob) { return new Promise(function (resolve, reject) { var reader = new FileReader(); reader.onload = function () { resolve(String(reader.result)); }; reader.onerror = function () { reject(new Error('Não foi possível ler uma fotografia para a cópia.')); }; reader.readAsDataURL(blob); }); }
  async function exportHTML() {
    var entries = await listEntries(); bytes(entries); var portable = [], sections = [];
    for (var e of entries) {
      var p = metadata(e); p.photos = [];
      for (var photo of await validatePhotos(e.photos)) p.photos.push({ id: photo.id, name: photo.name, type: photo.type, size: photo.size, dataURL: await dataURL(photo.blob) });
      portable.push(p); var study=studyParts(p);
      sections.push('<article><h2>' + escapeHTML(p.title || p.sessionId) + '</h2><p>Atualizado: ' + escapeHTML(p.updatedAt) + '</p><h3>Enunciado e fontes</h3>' + render(study.reading) + '<h3>Proposta de escrita</h3>' + render(study.writing) + '<h3>Correção e critérios</h3>' + render(study.correction) + '<h3>Respostas</h3>' + render(study.answers) + '<h3>Notas</h3>' + render(p.notes) + '<h3>Texto revisto</h3>' + render(p.revisedText) + '<h3>Lista de verificação</h3>' + render(study.checks) + p.photos.map(function (x) { return '<figure><img data-session="' + escapeHTML(p.sessionId) + '" data-photo="' + escapeHTML(x.id) + '" alt="' + escapeHTML(x.name) + '"><figcaption>' + escapeHTML(x.name) + '</figcaption></figure>'; }).join('') + '</article>');
    }
    var json = JSON.stringify({ format: FORMAT, version: VERSION, exportedAt: new Date().toISOString(), entries: portable }).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
    var html = '<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>O meu dossiê de Português</title><style>body{max-width:900px;margin:auto;padding:24px;font:17px/1.55 Georgia,serif;color:#171715;background:#fff}article{border-top:2px solid;padding-top:16px;margin-top:30px}h1,h2,h3,summary{font-family:Arial,sans-serif}img{max-width:100%;height:auto}figure{margin:20px 0}.text{white-space:pre-wrap;overflow-wrap:anywhere}dt{font-weight:bold}dd{margin-left:20px}details{margin:20px 0}@media print{body{padding:0;font-size:11pt}article{break-before:page}img{max-height:240mm;object-fit:contain}details{display:block}details>*{display:block!important}}</style></head><body><h1>O meu dossiê de Português</h1><p>Cópia autónoma para ler, imprimir e repor na aplicação. Inclui os originais das fotografias e os dados de estudo.</p>' + sections.join('') + '<script id="pt-exame-dossier-data" type="application/json">' + json + '</script><script>(function(){var d=JSON.parse(document.getElementById("pt-exame-dossier-data").textContent);document.querySelectorAll("img[data-photo]").forEach(function(im){var e=d.entries.find(function(x){return x.sessionId===im.dataset.session});var p=e&&e.photos.find(function(x){return x.id===im.dataset.photo});if(p)im.src=p.dataURL})}());</script></body></html>';
    var result = new Blob([html], { type: 'text/html;charset=utf-8' });
    if (result.size > FILE_LIMIT) fail('A cópia HTML é demasiado grande para voltar a importar. Reduz fotografias ou texto antes de exportar.');
    return result;
  }
  function decodePhoto(p) {
    allow(p, PORTABLE_PHOTO_KEYS, 'Fotografia importada'); id(p.id, 'Fotografia'); photoName(p.name);
    if (TYPES.indexOf(p.type) < 0 || !Number.isSafeInteger(p.size) || p.size < 12 || p.size > PHOTO_LIMIT || typeof p.dataURL !== 'string') fail('Fotografia importada inválida.');
    var prefix = 'data:' + p.type + ';base64,', encoded = p.dataURL.slice(prefix.length);
    if (!p.dataURL.startsWith(prefix) || encoded.length > Math.ceil(PHOTO_LIMIT / 3) * 4 || (encoded.length % 4 !== 0 || !/^[A-Za-z0-9+/]*={0,2}$/.test(encoded))) fail('Codificação da fotografia inválida.');
    var raw; try { raw = atob(encoded); } catch (e) { fail('Fotografia incompleta.'); }
    if (raw.length !== p.size || btoa(raw) !== encoded) fail('O tamanho da fotografia não corresponde ao declarado.');
    var bytes = new Uint8Array(raw.length); for (var i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
    return { id: p.id, name: p.name, type: p.type, size: p.size, blob: new Blob([bytes], { type: p.type }) };
  }
  async function importHTML(file) {
    if (!(file instanceof Blob) || !file.size || file.size > FILE_LIMIT) fail('Ficheiro de dossiê vazio ou demasiado grande.');
    var html = await file.text(), matches = html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi), payload = null;
    // Parse only inert script candidates, never the untrusted document or its images.
    for (var m of matches) {
      var doc = new DOMParser().parseFromString('<!doctype html><html><body><script' + m[1] + '></script></body></html>', 'text/html');
      var tag = doc.querySelector('script');
      if (tag && tag.id === 'pt-exame-dossier-data' && tag.type === 'application/json' && !tag.hasAttribute('src')) {
        if (payload !== null) fail('O ficheiro contém mais de um dossiê.'); payload = m[2];
      }
    }
    if (payload === null) fail('Este HTML não contém um dossiê de Português.');
    var data; try { data = safeJSON(JSON.parse(payload)); } catch (e) { fail('Os dados do dossiê são inválidos: ' + e.message); }
    allow(data, ['format', 'version', 'exportedAt', 'entries'], 'Dossiê');
    if (data.format !== FORMAT || data.version !== VERSION || !Array.isArray(data.entries) || data.entries.length > 1000) fail('Formato ou versão de dossiê não suportado.');
    if (!own(data, 'exportedAt')) fail('Falta a data de exportação.'); stamp(data.exportedAt); var entries = [], seen = {}, total = 0;
    for (var raw of data.entries) {
      allow(raw, ENTRY_KEYS, 'Registo importado');
      if (!own(raw, 'photos') || !Array.isArray(raw.photos) || raw.photos.length > 4 || !own(raw, 'updatedAt')) fail('Registo importado incompleto.');
      var e = metadata(raw); if (seen[e.sessionId]) fail('Sessão repetida no ficheiro.'); seen[e.sessionId] = true;
      // Bound the decoded data before retaining all image Blobs.
      raw.photos.forEach(function (p) { if (!Number.isSafeInteger(p.size) || p.size < 0) fail('Tamanho de fotografia inválido.'); total += p.size; });
      total += new Blob([JSON.stringify(e)]).size; if (total > TOTAL_LIMIT) fail('O ficheiro ultrapassa 64 MiB de dados.');
      e.photos = await validatePhotos(raw.photos.map(decodePhoto)); entries.push(e);
    }
    bytes(entries);
    // No write transaction is opened until every imported entry and photo is valid.
    return mutate(function (rows, store) {
      var merged = new Map(rows.map(function (e) { return [e.sessionId, e]; })), accepted = [];
      entries.forEach(function (e) { var old = merged.get(e.sessionId); if (!old || Date.parse(e.updatedAt) > Date.parse(old.updatedAt)) { merged.set(e.sessionId, e); accepted.push(e); } });
      bytes(Array.from(merged.values())); accepted.forEach(function (e) { store.put(e); }); return accepted.length;
    });
  }
  function photoURL(photo) { if (!photo || !(photo.blob instanceof Blob)) fail('Fotografia indisponível.'); return URL.createObjectURL(photo.blob); }
  window.PTExameDossier = Object.freeze({ getEntry: getEntry, listEntries: listEntries, saveEntry: saveEntry, addPhotos: addPhotos, removePhoto: removePhoto, deleteEntry: deleteEntry, exportHTML: exportHTML, importHTML: importHTML, photoURL: photoURL });
}());
