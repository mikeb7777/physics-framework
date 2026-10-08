# -*- coding: utf-8 -*-
"""Moving thumbnails for visualizations.html (2 Oct 2026). Michael: the simulations page looks
static, needs thumbnails, and should show motion through time. Opens each simulation's
panel in a real browser, records a short loop of the running canvas, and encodes it as a
small silent looping MP4 (sim-thumbs/<canvas id>.mp4) plus a poster JPEG (the brightest
frame, so a sim that starts dark still shows something). Canvases much wider or taller
than 16:9 are letterboxed rather than cropped. Static charts (NBI, CMB) are left out.
Rerun after changing a simulation: python tools/record_sim_thumbs.py [canvas ids...]"""
import os, subprocess, sys, time, shutil, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sim-thumbs"); os.makedirs(OUT, exist_ok=True)
IDS = ["c-field", "c-ent", "c-rot", "c-four", "c-scram", "c-bang", "c-bamboo", "c-bell", "c-subplanck", "c-chamber", "c-nowwin", "c-phi"]
SECONDS = {"c-bang": 6, "c-bamboo": 6, "c-subplanck": 6}      # one full cycle of the slower sims
FPS, TW, TH, BG = 15, 480, 270, (2, 4, 8)
FF = shutil.which("ffmpeg")
only = sys.argv[1:] or IDS


def fit(im):
    """16:9 thumbnail: crop when the aspect is close, letterbox when it is not."""
    ar, tar = im.width / im.height, TW / TH
    if 0.8 < ar / tar < 1.25:
        r = max(TW / im.width, TH / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        l, t = (im.width - TW) // 2, (im.height - TH) // 2
        return im.crop((l, t, l + TW, t + TH))
    r = min(TW / im.width, TH / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    bg = Image.new("RGB", (TW, TH), im.getpixel((2, 2)) if im.width > 4 else BG)
    bg.paste(im, ((TW - im.width) // 2, (TH - im.height) // 2))
    return bg


srv = subprocess.Popen([sys.executable, "-m", "http.server", "8797"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto("http://localhost:8797/visualizations.html", wait_until="load"); pg.wait_for_timeout(1500)
        pg.add_style_tag(content="[data-aos]{transform:none!important;opacity:1!important}")
        for cid in only:
            opened = pg.evaluate("""(id)=>{const c=document.getElementById(id); if(!c) return false;
                const a=c.closest('.foundation-accordion'); if(a && !a.classList.contains('active')) a.querySelector('.foundation-header').click();
                return true;}""", cid)
            if not opened:
                print("missing", cid); continue
            pg.wait_for_timeout(1800)
            pg.evaluate("(id)=>document.getElementById(id).scrollIntoView({block:'center'})", cid); pg.wait_for_timeout(600)
            el = pg.locator("#" + cid)
            frames, n = [], FPS * SECONDS.get(cid, 4)
            t0 = time.time()
            for i in range(n):
                frames.append(fit(Image.open(io.BytesIO(el.screenshot(type="jpeg", quality=90))).convert("RGB")))
                time.sleep(max(0, t0 + (i + 1) / FPS - time.time()))
            mp4 = os.path.join(OUT, cid + ".mp4")
            proc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-vcodec", "mjpeg", "-i", "-",
                                     "-vf", "scale=in_range=pc:out_range=tv,format=yuv420p",
                                     "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-an", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
            for fr in frames:
                buf = io.BytesIO(); fr.save(buf, "JPEG", quality=92); proc.stdin.write(buf.getvalue())
            proc.stdin.close(); proc.wait()
            poster = max(frames, key=lambda f: ImageStat.Stat(f.convert("L")).mean[0])
            poster.save(os.path.join(OUT, cid + ".jpg"), quality=82)
            print(cid, os.path.getsize(mp4) // 1024, "KB", flush=True)
            pg.evaluate("""(id)=>{const a=document.getElementById(id).closest('.foundation-accordion'); if(a && a.classList.contains('active')) a.querySelector('.foundation-header').click();}""", cid)
            pg.wait_for_timeout(400)
        b.close()
finally:
    srv.terminate()
