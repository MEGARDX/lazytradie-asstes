// Render the vision film to JPEG frames: node render.js <outDir> [fps] [t0|"t,t,t"] [t1] [workers]
// Each worker renders one CONTIGUOUS chunk, so the real orb (which simulates forward) stays deterministic.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const [out = 'frames', fps = 30, t0 = 0, t1 = '', workers = 4] = process.argv.slice(2);
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json')));
fs.mkdirSync(out, { recursive: true });
let frames = String(t0).includes(',') ? String(t0).split(',').map(s => Math.round(+s * fps)) : [];
if (!frames.length) { const a = Math.round((parseFloat(t0) || 0) * fps), b = Math.round((t1 !== '' ? +t1 : TL.dur) * fps); for (let i = a; i < Math.max(b, a + 1); i++) frames.push(i); }
const nw = Math.min(+workers, frames.length), per = Math.ceil(frames.length / nw);

(async () => {
  const browser = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-gpu-rasterization', '--use-gl=angle', '--use-angle=swiftshader'] });
  await Promise.all([...Array(nw)].map(async (_, w) => {
    const mine = frames.slice(w * per, (w + 1) * per); if (!mine.length) return;
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => console.error('pageerror', e.message));
    await page.addInitScript(tl => { window.TL = tl; }, TL);
    await page.goto('file://' + path.join(__dirname, 'vision.html'));
    await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 180000 });
    for (let j = 0; j < mine.length; j++) {
      const f = mine[j];
      await page.evaluate(t => window.renderAt(t), f / fps);
      await page.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 94, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
      if (w === 0 && j % 100 === 0) console.log('frame', f, `(${j}/${mine.length})`);
    }
    await page.close();
  }));
  await browser.close();
})();
