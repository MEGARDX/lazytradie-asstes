// node shoot.js → ../partners-poster.png (1080×1350)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'poster.html')); await p.waitForFunction(() => document.body.dataset.ready === '1');
  await p.screenshot({ path: path.join(__dirname, '..', 'partners-poster.png') }); await b.close();
})();
