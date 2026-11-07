// Render the Saturday carousel: node shoot.js → ../00..03.png, overview.png, LinkedIn PDF
const { chromium } = require('playwright'); const path = require('path');
const names = ['00_cover', '01_calls', '02_texts', '03_big_jobs', '04_monday'];
(async () => {
  const b = await chromium.launch();
  for (let i = 0; i < 5; i++) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
    await p.goto('file://' + path.join(__dirname, 'slides.html') + '?s=' + i);
    await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(400);
    await p.locator('#s' + i).screenshot({ path: path.join(__dirname, '..', names[i] + '.png') }); await p.close();
  }
  await b.close();
})();
