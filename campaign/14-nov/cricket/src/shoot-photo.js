// Render the photo version of the cricket post: node shoot-photo.js → ../cricket-photo-feed.png
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'photo.html'));
  await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(300);
  await p.locator('#p').screenshot({ path: path.join(__dirname, '..', 'cricket-photo-feed.png') });
  await b.close();
})();
