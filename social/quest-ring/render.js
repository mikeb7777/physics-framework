// Renders ring.html to quest-ring.jpg and quest-ring.webp (760 x 980) in the repo root.
// From the repo root, with a local server on port 8765:
//   python3 -m http.server 8765 &
//   node social/quest-ring/render.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 760, height: 980 } });
  await p.goto('http://localhost:8765/social/quest-ring/ring.html');
  await p.waitForFunction(() => document.body.dataset.ready);
  await (await p.$('canvas')).screenshot({ path: 'quest-ring.png' });
  await b.close();
  execFileSync('python3', ['-c', "from PIL import Image; im=Image.open('quest-ring.png').convert('RGB'); im.save('quest-ring.jpg', quality=88, optimize=True, progressive=True); im.save('quest-ring.webp', quality=86, method=6); import os; os.remove('quest-ring.png')"]);
  console.log('wrote quest-ring.jpg and quest-ring.webp');
})();
