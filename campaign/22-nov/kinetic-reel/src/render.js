// V=1|2 node render.js [outDir] [t,t,t | t0] [t1] [workers] → JPEG frames of reel.html?v=V at 30 fps
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const [out = 'tmp/out', t0 = '0', t1 = '', workers = '3'] = process.argv.slice(2); const FPS = 30;
fs.mkdirSync(out, { recursive: true });
(async () => {
  const b0 = await chromium.launch(); const pg = await b0.newPage(); await pg.goto('file://' + path.join(__dirname, 'reel.html') + '?v=' + (process.env.V || 1));
  await pg.waitForFunction(() => document.body.dataset.ready === '1'); const END = await pg.evaluate(() => window.END); await b0.close();
  let frames = String(t0).includes(',') ? String(t0).split(',').map(s => Math.round(+s * FPS)) : [];
  if (!frames.length) { const a = Math.round(+t0 * FPS), z = Math.round((t1 !== '' ? +t1 : END) * FPS); for (let i = a; i < z; i++) frames.push(i); }
  const nw = Math.min(+workers, frames.length), per = Math.ceil(frames.length / nw);
  await Promise.all([...Array(nw)].map(async (_, w) => {
    const mine = frames.slice(w * per, (w + 1) * per); if (!mine.length) return;
    const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
    p.on('pageerror', e => console.error('pageerror', e.message));
    await p.goto('file://' + path.join(__dirname, 'reel.html') + '?v=' + (process.env.V || 1)); await p.waitForFunction(() => document.body.dataset.ready === '1');
    for (const f of mine) { await p.evaluate(tt => window.renderAt(tt), f / FPS); await p.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 94 }); }
    await b.close();
  }));
  console.log('done', frames.length, 'frames, END', END);
})();
