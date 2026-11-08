// Render the transparent overlay PNGs: node shoot.js → ov/<id>.png
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const ids = ['head1', 'cap_wait', 'wait', 'head2', 'cap_quote', 'chip_draft', 'chip_sent', 'end'];
(async () => {
  fs.mkdirSync(path.join(__dirname, 'ov'), { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const id of ids) {
    await p.goto('file://' + path.join(__dirname, 'overlays.html') + '?o=' + id);
    await p.waitForFunction(() => document.body.dataset.ready === '1'); await p.waitForTimeout(200);
    await p.locator('#' + id).screenshot({ path: path.join(__dirname, 'ov', id + '.png'), omitBackground: true });
  }
  await b.close();
})();
