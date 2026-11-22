// Cover: the "money in the bin" beat, reframed so it also survives Instagram's 4:5 grid crop. node cover.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const browser = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--use-gl=angle', '--use-angle=swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'reel.html'));
  await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 180000 });
  await page.evaluate(async () => {
    await window.renderAt(27.88);
    CAP[10].el.style.top = '360px';
    document.querySelector('#s10 > .lbl').style.top = '660px';
    document.querySelector('#s10 > .abs').style.top = '700px';
    document.getElementById('cnt').textContent = '$9,300';
    document.getElementById('cnt').style.transform = 'none';
  });
  await page.screenshot({ path: path.join(__dirname, '..', 'cover-9x16.png') });
  await browser.close();
})();
