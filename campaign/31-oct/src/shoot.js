// Render the 31 Oct slides to 1080×1350 PNGs: node shoot.js [ids…] [--out dir]
const { chromium } = require('playwright');
const path = require('path');

const all = { cover: '00_cover', s1: '01_receptionist', s2: '02_tiers', s3: '03_calendar', cta: '04_cta' };
const args = process.argv.slice(2);
const oi = args.indexOf('--out');
const out = oi > -1 ? args.splice(oi, 2)[1] : path.join(__dirname, '..');
const ids = args.length ? args : Object.keys(all);

(async () => {
  const browser = await chromium.launch({ args: ['--enable-gpu-rasterization', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const id of ids) {
    await page.goto('file://' + path.join(__dirname, 'slides.html') + '?s=' + id);
    await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 60000 });
    await page.waitForTimeout(400);
    const glass = await page.evaluate(() => document.body.dataset.glass);
    await page.locator('#' + id).screenshot({ path: path.join(out, all[id] + '.png') });
    console.log(id, '→', all[id] + '.png', 'glass:', glass);
  }
  await browser.close();
})();
