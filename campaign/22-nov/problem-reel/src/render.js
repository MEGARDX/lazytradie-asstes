// Render reel.html to JPEG frames: node render.js <outDir> [t0|"t,t,t"] [t1] [workers]
// Each worker renders one contiguous chunk so the real orb (simulated forward) stays deterministic.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'timeline.js'), 'utf8');
const TL = JSON.parse(src.slice(src.indexOf('{'), src.lastIndexOf('}') + 1));
const FPS = TL.fps;
const [out = 'tmp/out', t0 = '0', t1 = '', workers = '4'] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
let frames = String(t0).includes(',') ? String(t0).split(',').map(s => Math.round(+s * FPS)) : [];
if (!frames.length) { const a = Math.round(+t0 * FPS), b = Math.round((t1 !== '' ? +t1 : TL.total) * FPS); for (let i = a; i < Math.max(b, a + 1); i++) frames.push(i); }
const nw = Math.min(+workers, frames.length), per = Math.ceil(frames.length / nw);

(async () => {
  const t = Date.now();
  await Promise.all([...Array(nw)].map(async (_, w) => {
    const mine = frames.slice(w * per, (w + 1) * per); if (!mine.length) return;
    // one browser per worker: pages in one browser share a single (software) GPU process, which serialises them
    const browser = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-gpu-rasterization', '--use-gl=angle', '--use-angle=swiftshader', '--allow-file-access-from-files'] });
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => console.error('pageerror', e.message));
    page.on('console', m => { if (m.type() === 'error') console.error('console', m.text()); });
    await page.goto('file://' + path.join(__dirname, 'reel.html'));
    await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 180000 });
    if (w === 0) console.log('glass', await page.evaluate(() => document.body.dataset.glass.split(',').filter(x => x === 'true').length), 'elements');
    for (let j = 0; j < mine.length; j++) {
      const f = mine[j];
      await page.evaluate(tt => window.renderAt(tt), f / FPS);
      await page.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 93 });
      if (w === 0 && j % 60 === 0) console.log('frame', f, `${j}/${mine.length}`, ((Date.now() - t) / 1000).toFixed(0) + 's');
    }
    await browser.close();
  }));
  console.log('done', frames.length, 'frames in', ((Date.now() - t) / 1000).toFixed(0), 's');
})();
