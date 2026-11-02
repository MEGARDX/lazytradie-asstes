// Render the AI Admin Tool poster: node shoot.js → ../ai-admin-tool-free.png
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'poster.html'));
  await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(400);
  await p.locator('#p').screenshot({ path: path.join(__dirname, '..', 'ai-admin-tool-free.png') }); await b.close();
})();
