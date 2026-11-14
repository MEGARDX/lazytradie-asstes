// Render the cricket scoreboard post: node shoot.js → ../cricket-feed.png (1080×1350) + ../cricket-story.png (1080×1920)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [f, h] of [['feed', 1350], ['story', 1920]]) {
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + path.join(__dirname, 'poster.html') + '?f=' + f);
    await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(400);
    await p.locator('#p').screenshot({ path: path.join(__dirname, '..', 'cricket-' + f + '.png') }); await p.close();
  }
  await b.close();
})();
