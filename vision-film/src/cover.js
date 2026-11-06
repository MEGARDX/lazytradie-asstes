// Vision film cover (Reels / Facebook / LinkedIn): the answered, glowing map from the film + title + wordmark.
// node cover.js <outDir>  → cover-9x16.png (1080×1920) and cover-4x5.png (1080×1350, centre crop for the grid/feed)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const out = process.argv[2] || '.'; fs.mkdirSync(out, { recursive: true });
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json')));
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('pageerror', e.message));
  await page.addInitScript(tl => { window.TL = tl; }, TL);
  await page.goto('file://' + path.join(__dirname, 'vision.html'));
  await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 180000 });
  await page.evaluate(t => {
    window.renderAt(t);                                    // map fully answered + warm aura, just before the flag
    document.querySelectorAll('.c').forEach(el => { el.style.visibility = 'hidden'; });
    const w = document.getElementById('world'); w.style.opacity = 1; w.style.transform = 'translateY(262px) scale(.94)';
    const css = document.createElement('style'); css.textContent = `
      .cv{position:absolute;left:0;right:0;display:flex;justify-content:center}
      .kick{height:66px;padding:0 30px;border-radius:33px;display:flex;align-items:center;gap:14px;font-size:21px;font-weight:700;letter-spacing:.22em;color:var(--gold)}
      .kick i{font-size:22px;color:var(--am)}
      .ttl{text-align:center;letter-spacing:-.05em;line-height:.98;font-size:112px}
      .ttl .a{display:block;font-weight:300;color:#F6F0E6}.ttl .b{display:block;font-weight:700;color:#F6F0E6}
      .aura{position:absolute;left:50%;top:640px;width:900px;height:420px;transform:translate(-50%,-50%);border-radius:50%;
        background:radial-gradient(closest-side,rgba(245,166,35,.16),rgba(245,166,35,0));filter:blur(10px)}`;
    document.head.appendChild(css);
    const st = document.getElementById('stage'), before = document.getElementById('flash');
    const add = html => { const d = document.createElement('div'); d.innerHTML = html.trim(); const el = d.firstChild; st.insertBefore(el, before); return el; };
    add('<div class="aura"></div>');
    const k = add('<div class="cv" style="top:338px"><div class="g kick mono"><i class="ph-fill ph-play"></i>A LAZYTRADIE FILM</div></div>');
    add('<div class="cv" style="top:440px"><div class="ttl"><span class="a">Built for the people</span><span class="b">who build <span class="am">Australia.</span></span></div></div>');
    add('<div class="cv" style="top:1478px"><img src="wm_white.png" style="width:430px"></div>');
    add('<div class="cv" style="top:1580px"><div class="mono" style="font-size:25px;font-weight:700;letter-spacing:.06em;color:#CDBFA8">lazytradie.com.au</div></div>');
    liquidGlass(k.firstChild, { scale: -90, chroma: 6, blur: 3 });
  }, 77.9);
  await page.waitForTimeout(400);
  const full = path.join(out, 'cover-9x16.png');
  await page.screenshot({ path: full, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  await page.screenshot({ path: path.join(out, 'cover-4x5.png'), clip: { x: 0, y: 285, width: 1080, height: 1350 } });
  await browser.close(); console.log('ok');
})();
