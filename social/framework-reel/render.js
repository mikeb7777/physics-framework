// Renders reel.html to an Instagram reel: 1080 x 1920, 30 fps, H.264 MP4.
// Usage (from the repo root, with a local server on port 8765):
//   python3 -m http.server 8765 &
//   node social/framework-reel/render.js [out.mp4] [--stills]
// --stills writes one PNG per scene instead, for checking the layout.
const { chromium } = require('playwright');
const { spawn } = require('child_process');

(async () => {
  const out = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'framework-reel.mp4';
  const stills = process.argv.includes('--stills');
  const FPS = 30;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('http://localhost:8765/social/framework-reel/reel.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const duration = await page.evaluate(() => REEL.duration);

  if (stills) {
    for (const [i, t] of [3.6, 7.8, 12.6, 16.8, 21.6, 25.2].entries()) {
      await page.evaluate(t => REEL.render(t), t);
      await page.screenshot({ path: out.replace(/\.mp4$/, '') + `-scene${i + 1}.png` });
    }
    await browser.close();
    return;
  }

  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'slow', '-crf', '18', '-movflags', '+faststart',
    '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const frames = Math.round(duration * FPS);
  for (let f = 0; f < frames; f++) {
    await page.evaluate(t => REEL.render(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('wrote', out, frames, 'frames');
})();
