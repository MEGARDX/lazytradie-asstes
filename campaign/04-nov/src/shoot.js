// Render the A$1.61 carousel: node shoot.js → ../01..04.png + overview.png
const { chromium } = require('playwright'); const path = require('path');
const names = ['01_hook', '02_maths', '03_what', '04_close'];
(async () => {
  const b = await chromium.launch();
  for (let i = 1; i <= 4; i++) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
    await p.goto('file://' + path.join(__dirname, 'slides.html') + '?s=' + i);
    await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(500);
    await p.locator('#s' + i).screenshot({ path: path.join(__dirname, '..', names[i - 1] + '.png') }); await p.close();
  }
  await b.close();
})();
