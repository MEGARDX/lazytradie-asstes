// Render text overlays (ov/*.png) and the Copilot card animation (ui/frame_0000.png …), 1080×1920, transparent.
// node shoot.js [uiDurationSeconds=6.69]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const DUR = parseFloat(process.argv[2] || '6.69'), FPS = 30;
(async () => {
  for (const d of ['ov', 'ui']) fs.mkdirSync(path.join(__dirname, d), { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const id of ['title', 'quote', 'sub1', 'sub2', 'end']) {
    await p.goto('file://' + path.join(__dirname, 'text.html') + '?o=' + id);
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.screenshot({ path: path.join(__dirname, 'ov', id + '.png'), omitBackground: true });
  }
  const n = Math.round(DUR * FPS);
  for (let i = 0; i < n; i++) {
    await p.goto('file://' + path.join(__dirname, 'ui.html') + '?t=' + (i / FPS).toFixed(4));
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.screenshot({ path: path.join(__dirname, 'ui', `frame_${String(i).padStart(4, '0')}.png`), omitBackground: true });
  }
  await b.close(); console.log('ui frames', n);
})();
