// Render the reel to JPEG frames: node render.js <1x1|9x16> <outDir> [fps] [t0] [t1] [workers]
// node render.js 1x1 out 30 12.5 12.5 → a single still at t = 12.5 s (for checking).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const [fmt = '1x1', out = 'frames', fps = 30, t0 = 0, t1, workers = 3] = process.argv.slice(2);
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json')));
const W = 1080, H = fmt === '9x16' ? 1920 : 1080;
const end = t1 != null && t1 !== "" ? +t1 : TL.dur, n0 = Math.round((parseFloat(t0) || 0) * fps), n1 = Math.round(end * fps);
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-gpu-rasterization'] });
  // t0 may be a comma list of seconds (check stills); otherwise render frames [t0, t1)
  const frames = String(t0).includes(',') ? String(t0).split(',').map(s => Math.round(+s * fps)) : [];
  if (!frames.length) for (let i = n0; i < Math.max(n1, n0 + 1); i++) frames.push(i);
  const nw = Math.min(+workers, frames.length);
  await Promise.all([...Array(nw)].map(async (_, w) => {
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    await page.addInitScript(tl => { window.TL = tl; }, TL);
    await page.goto('file://' + path.join(__dirname, 'reel.html') + '?f=' + fmt);
    await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 120000 });
    for (let j = w; j < frames.length; j += nw) {
      const f = frames[j];
      await page.evaluate(t => window.renderAt(t), f / fps);
      await page.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 94, clip: { x: 0, y: 0, width: W, height: H } });
      if (w === 0 && j % 150 === 0) console.log(fmt, 'frame', f, '/', n1);
    }
    await page.close();
  }));
  await browser.close();
})();
