// Renders the poster to a print PDF (24.25 x 36.25 in, with 0.125 in bleed) and a preview PNG.
// From the repo root, with a local server on port 8765:
//   python3 -m http.server 8765 &
//   node poster/render.js [cosmic-poster-v3]
const { chromium } = require('playwright');

(async () => {
  const name = process.argv[2] || 'cosmic-poster-v2';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2328, height: 3480 } });
  await page.goto(`http://localhost:8765/poster/${name}.html`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.pdf({ path: `poster/${name}.pdf`, width: '24.25in', height: '36.25in', printBackground: true });
  await page.screenshot({ path: `poster/${name}-preview.png`, type: 'png' });
  await browser.close();
  console.log('wrote', `poster/${name}.pdf`);
})();
