// node shoot.js → ../black-friday-greeting.png (1620×1080, 3:2 landscape)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1620, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'poster.html')); await p.waitForFunction(() => document.body.dataset.ready === '1');
  await p.screenshot({ path: path.join(__dirname, '..', 'black-friday-greeting.png') }); await b.close();
})();
