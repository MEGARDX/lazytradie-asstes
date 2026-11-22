// node shoot.js → ../ai-poster-1x1.png (1080×1080, like the reference) and ../ai-poster-4x5.png (1080×1350)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [h, name] of [[1080, 'ai-poster-1x1.png'], [1350, 'ai-poster-4x5.png']]) {
    const p = await b.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.join(__dirname, 'poster.html') + '?h=' + h);
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.screenshot({ path: path.join(__dirname, '..', name), clip: { x: 0, y: 0, width: 1080, height: h } });
    await p.close();
  }
  await b.close();
})();
