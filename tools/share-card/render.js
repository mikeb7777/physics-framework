// Renders tools/share-card/card.html to share-card.jpg (1200 x 630) in the repo root.
//   python3 -m http.server 8765 &   then   node tools/share-card/render.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('http://localhost:8765/tools/share-card/card.html');
  await p.evaluate(() => Promise.all(['700 76px Inter', '600 28px Inter', 'italic 500 34px "Source Serif 4"'].map(f => document.fonts.load(f))));
  await p.waitForTimeout(300);
  await (await p.$('.card')).screenshot({ path: 'share-card.png' });
  await b.close();
  execFileSync('python3', ['-c', "from PIL import Image; import os; Image.open('share-card.png').convert('RGB').save('share-card.jpg', quality=88, optimize=True, progressive=True); os.remove('share-card.png')"]);
  console.log('wrote share-card.jpg');
})();
