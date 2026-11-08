// Render the Sunday poster: node shoot.js → ../sunday-paperwork-feed.png
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'poster.html'));
  await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(500);
  await p.locator('#p').screenshot({ path: path.join(__dirname, '..', 'sunday-paperwork-feed.png') });
  await b.close();
})();
