// Renders the poster to a print PDF (24.25 x 36.25 in, with 0.125 in bleed) and a preview PNG.
// From the repo root, with a local server on port 8765:
//   python3 -m http.server 8765 &
//   node poster/render.js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2328, height: 3480 } });
  await page.goto('http://localhost:8765/poster/cosmic-poster-v2.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.pdf({ path: 'poster/cosmic-poster-v2.pdf', width: '24.25in', height: '36.25in', printBackground: true });
  await page.screenshot({ path: 'poster/cosmic-poster-v2-preview.png', type: 'png' });
  await browser.close();
  console.log('wrote poster/cosmic-poster-v2.pdf and poster/cosmic-poster-v2-preview.png');
})();
