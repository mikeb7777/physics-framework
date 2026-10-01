// Renders a reel page to an Instagram reel: 1080 x 1920, 30 fps, H.264 MP4.
// A reel page draws every frame with REEL.render(t) and lists REEL.duration
// (seconds) and REEL.stills (times for layout checks).
//
// Usage, from the repo root with a local server on port 8765:
//   python3 -m http.server 8765 &
//   node social/render-reel.js social/rubin-reel/reel.html rubin-reel.mp4
//   node social/render-reel.js social/rubin-reel/reel.html rubin-reel.mp4 --stills
// --stills writes one PNG per entry in REEL.stills instead of the video.
const { chromium } = require('playwright');
const { spawn } = require('child_process');

(async () => {
  const [pagePath, out = 'reel.mp4'] = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const stills = process.argv.includes('--stills');
  const FPS = 30;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('http://localhost:8765/' + pagePath);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const { duration, times } = await page.evaluate(() => ({ duration: REEL.duration, times: REEL.stills || [] }));

  if (stills) {
    for (const [i, t] of times.entries()) {
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
