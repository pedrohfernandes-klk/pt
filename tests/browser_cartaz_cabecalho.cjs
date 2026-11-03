// 03/11/2026: abertura normal e projeção real, pausa, teclado, zoom e regressão visual.
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), http = require('node:http'), os = require('node:os');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '..'), out = process.env.CABECALHO_OUTPUT;
// Usa sem alterações a função de medição fornecida pelo docente.
const measurement = fs.readFileSync(path.join(root, 'tools/medir-hierarquia.js'), 'utf8').split('const MEASURE=')[1].split('srv.listen')[0].trim().replace(/;$/, '');
const MEASURE = require('node:vm').runInNewContext('(' + measurement + ')');
const options = { headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) };
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'tests/fixtures/cartaz-cabecalho-edits-20261103.json'), 'utf8'));
let before = fs.readFileSync(path.join(root, 'index.html'), 'utf8').replace(/\r\n/g, '\n');
for (const edit of [...manifest.files['index.html'].edits].reverse()) {
  assert.equal(before.split(edit.new).length - 1, edit.occurrences);
  before = before.split(edit.new).join(edit.old);
}
const server = http.createServer((req, res) => {
  const u = new URL(req.url, 'http://local'), old = u.pathname.startsWith('/before/');
  let rel = decodeURIComponent(u.pathname.replace(/^\/(?:before\/)?pt\//, ''));
  if (!rel || rel.endsWith('/')) rel += 'index.html';
  const file = path.resolve(root, rel);
  if (!file.startsWith(root + path.sep)) { res.writeHead(403); return res.end(); }
  try {
    res.setHeader('content-type', ({ '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml' })[path.extname(file)] || 'application/octet-stream');
    res.end(old && rel === 'index.html' ? before : fs.readFileSync(file));
  } catch { res.writeHead(404); res.end(); }
});
function luminance(rgb) { return rgb.map(v => v / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4).reduce((n, v, i) => n + v * [.2126, .7152, .0722][i], 0); }
(async () => {
  if (out) fs.mkdirSync(out, { recursive: true });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port, browser = await chromium.launch(options), rows = [];
  async function local(context) { await context.route('**/*', r => new URL(r.request().url()).origin === base ? r.continue() : r.abort()); }
  try {
    for (const width of [320, 390, 1366]) for (const theme of ['light', 'dark']) for (const projection of [false, true]) {
      const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme: theme });
      await local(context);
      const page = await context.newPage(), errors = [], row = { width, theme, projection };
      page.on('pageerror', e => errors.push(String(e)));
      for (const version of ['before', 'after']) {
        const prefix = version === 'before' ? '/before/pt/' : '/pt/';
        await page.goto(base + prefix + (projection ? 'projetar/?pagina=/pt/' : ''));
        let frame = page;
        if (projection) {
          await page.frameLocator('#lesson-frame').locator('html.epi-projection').waitFor();
          if (await page.locator('#qr-toggle').getAttribute('aria-expanded') === 'true') await page.locator('#qr-toggle').click();
          frame = await (await page.locator('#lesson-frame').elementHandle()).contentFrame();
          await frame.waitForFunction(() => [...document.styleSheets].some(s => s.href && s.href.includes('projection-frame.css')));
        }
        await frame.evaluate(() => document.fonts.ready);
        row[version] = await frame.evaluate(() => {
          const title = document.querySelector('.p-cab h1'), lead = document.querySelector('.pt-entry-lead'), stones = document.querySelector('.cf-pedras');
          return { overflow: document.documentElement.scrollWidth - innerWidth, titleHeight: title.offsetHeight, titleLine: parseFloat(getComputedStyle(title).lineHeight), gap: lead.getBoundingClientRect().top - title.getBoundingClientRect().bottom, animations: stones.getAnimations().length, opacity: +getComputedStyle(stones).opacity, ink: getComputedStyle(lead).color, paper: getComputedStyle(document.body).backgroundColor, credit: document.querySelector('.cf-credito').textContent, storage: JSON.stringify(Object.entries(localStorage)) };
        });
        if (out) await (projection ? page.locator('#lesson-frame') : page).screenshot({ fullPage: !projection, path: path.join(out, `${width}-${theme}-${projection ? 'projection' : 'normal'}-${version}.png`) });
        if (version === 'after') {
          // 03/11/2026: nenhum destaque ou reabertura; os destinos continuam em Mais.
          assert.equal(await frame.locator('aside.ed-sugestao, [data-reabrir]').count(), 0);
          assert.equal(await frame.locator('.mais-l a[href$="/narrativas/variantes/#escrita"]').count(), 1);
          assert.equal(await frame.locator('.mais-l a[href$="/ver-para-fazer/"]').count(), 1);
          const result = row.after;
          result.hierarchy = await frame.evaluate(MEASURE);
          for (const rule of ['r1', 'r2', 'r3', 'r5']) assert.deepEqual(result.hierarchy[rule], [], JSON.stringify({ width, theme, projection, rule, cases: result.hierarchy[rule] }));
          assert.equal(result.overflow, 0); assert(result.titleHeight <= result.titleLine + 1); assert(result.gap >= 24);
          assert(result.credit.includes('Grafismo gerado com recurso a IA')); assert(result.credit.includes('Rossio'));
          const ink = result.ink.match(/\d+/g).map(Number), paper = result.paper.match(/\d+/g).map(Number);
          result.contrast = Math.min(...[0, 255].map(extreme => { const pair = [luminance(ink), luminance(paper.map(v => v * (1 - result.opacity) + extreme * result.opacity))].sort((a, b) => a - b); return (pair[1] + .05) / (pair[0] + .05); }));
          assert(result.contrast >= 4.5);
          if (projection) { assert.equal(result.animations, 0); assert(await frame.locator('[data-fundo-botao=cf]').isHidden()); }
          else {
            assert.equal(result.animations, 1);
            const button = frame.locator('[data-fundo-botao=cf]'); await button.focus(); await page.keyboard.press('Enter');
            assert.equal(await frame.locator('.cf-pedras').evaluate(e => e.getAnimations().length), 0); assert(await button.evaluate(e => document.activeElement === e));
            await page.keyboard.press('Enter'); assert.equal(await frame.locator('.cf-pedras').evaluate(e => e.getAnimations().length), 1);
          }
        }
      }
      assert.deepEqual(errors, []); assert.equal(row.after.storage, row.before.storage); rows.push(row); await context.close(); console.log('PASS cabeçalho', width, theme, projection);
    }
    for (const javaScriptEnabled of [true, false]) {
      const context = await browser.newContext({ javaScriptEnabled, reducedMotion: 'reduce', viewport: { width: 320, height: 900 } }); await local(context);
      const page = await context.newPage(); await page.goto(base + '/pt/'); assert(await page.locator('.pt-entry-lead').isVisible());
      assert.equal(await page.locator('aside.ed-sugestao, [data-reabrir]').count(), 0);
      assert.equal(await page.locator('.cf-pedras').evaluate(e => e.getAnimations().length), 0);
      await page.emulateMedia({ media: 'print' }); assert(await page.locator('.cf-mar').isHidden()); await context.close();
    }
    // Zoom nativo, com Chromium completo: o shell sem interface ignora Preferences.
    const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'cartaz-cabecalho-zoom-'));
    fs.mkdirSync(path.join(profile, 'Default'));
    fs.writeFileSync(path.join(profile, 'Default', 'Preferences'), JSON.stringify({ partition: { default_zoom_level: { x: Math.log(2) / Math.log(1.2) } } }));
    const zoomContext = await chromium.launchPersistentContext(profile, { ...options, ...(!process.env.CHROME_PATH ? { channel: 'chromium' } : {}), viewport: null, args: ['--window-size=1366,1000'] });
    let zoom;
    try {
      await local(zoomContext); const page = await zoomContext.newPage(); await page.goto(base + '/pt/');
      zoom = await page.evaluate(() => ({ outerWidth, innerWidth, dpr: devicePixelRatio, overflow: document.documentElement.scrollWidth - innerWidth, cssZoom: getComputedStyle(document.documentElement).zoom }));
      assert.equal(zoom.dpr, 2); assert(Math.abs(zoom.innerWidth - zoom.outerWidth / 2) <= 10); assert.equal(zoom.cssZoom, '1'); assert.equal(zoom.overflow, 0);
      // 03/11/2026: captura a superfície completa com zoom nativo, sem recorte a metade.
      if (out) {
        const cdp = await zoomContext.newCDPSession(page);
        const shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false, fromSurface: true });
        const png = Buffer.from(shot.data, 'base64');
        const view = await page.evaluate(() => ({ width: visualViewport.width * devicePixelRatio, height: visualViewport.height * devicePixelRatio }));
        assert(Math.abs(png.readUInt32BE(16) - view.width) <= 1);
        assert(Math.abs(png.readUInt32BE(20) - view.height) <= 1);
        fs.writeFileSync(path.join(out, 'zoom-nativo-200.png'), png);
        await cdp.detach();
      }
    } finally {
      await zoomContext.close();
      assert(path.resolve(profile).startsWith(path.resolve(os.tmpdir()) + path.sep) && path.basename(profile).startsWith('cartaz-cabecalho-zoom-'));
      fs.rmSync(profile, { recursive: true, force: true });
    }
    if (out) fs.writeFileSync(path.join(out, 'medidas.json'), JSON.stringify({ rows, zoom }, null, 2));
    console.log('PASS 24 páginas: normal e visor real, ambos os temas; teclado, contraste, movimento reduzido, sem JS e impressão.');
  } finally { await browser.close(); server.closeAllConnections(); server.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
