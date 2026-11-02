// Render the 3 Nov poster: node shoot.js → ../copilot-free-story.png, ../copilot-free-feed.png
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [f, h] of [['story', 1920], ['feed', 1350]]) {
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + path.join(__dirname, 'poster.html') + '?f=' + f);
    await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(500);
    await p.locator('#p').screenshot({ path: path.join(__dirname, '..', 'copilot-free-' + f + '.png') }); await p.close();
  }
  await b.close();
})();
