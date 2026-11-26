// node shoot.js → renders black-friday and partners posters (1080×1350)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [dir, out] of [['black-friday', 'black-friday-poster.png'], ['partners', 'partners-poster.png']]) {
    await p.goto('file://' + path.join(__dirname, dir, 'src', 'poster.html'));
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.screenshot({ path: path.join(__dirname, dir, out) });
  }
  await b.close();
})();
