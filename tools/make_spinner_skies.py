# -*- coding: utf-8 -*-
"""Backdrops for the Spinner, made from real images (Michael, 29 Sep 2026:
"clouds or something behind them... made from actual images... each different").

Each is a crop of a real astronomical image, softened slightly so it sits
behind the Spinner, brightened at the centre where the arms are (all three
Spinner colors fall below 3:1 on a dark sky), and faded out through an
irregular edge so it reads as sky, not as a disc. Transparent PNG.

  sky-about.png    Red Spider Nebula, NGC 6537  ESA/Webb, NASA & CSA, J. H. Kast (CC BY 4.0)
  sky-testing.png  Terzan 5                     NASA, ESA, CSA, STScI, G. Zullo
  sky-results.png  Milky Way core over Rubin    RubinObs/NOIRLab/SLAC/NSF/DOE/AURA/H. Stockebrand (CC BY 4.0)
"""
import math, os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.dirname(ROOT)
N = 900
SKIES = {
    # name: (source, crop box as fractions (x0, y0, x1, y1), rotate deg, seed, centre brightening)
    "sky-about.png": (os.path.join(ROOT, "color-red-spider.jpg"), (0.2, 0.2, 0.8, 0.8), -18, 3, 0.78),
    "sky-testing.png": (os.path.join(ROOT, "color-terzan5.jpg"), (0.2, 0.12, 0.88, 0.8), 0, 7, 0.50),
    "sky-results.png": (os.path.join(DL, r"rubin-carousel\src\photos\iotw2616a.jpg"), (0.25, 0.02, 0.62, 0.57), 12, 11, 0.42),
}
WANDER = {"sky-results.png": 0.22}               # a less regular edge where the image is smooth


def noise(rng, cells, blur):
    im = Image.fromarray((rng.random((cells, cells)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(blur))).astype(float) / 255


for name, (src, box, rot, seed, lift) in SKIES.items():
    im = Image.open(src).convert("RGB")
    W, H = im.size
    x0, y0, x1, y1 = box
    side = min((x1 - x0) * W, (y1 - y0) * H)
    cx, cy = (x0 + x1) / 2 * W, (y0 + y1) / 2 * H
    crop = im.crop((int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2)))
    crop = crop.rotate(rot, resample=Image.BICUBIC, expand=False).resize((N, N), Image.LANCZOS)
    crop = crop.filter(ImageFilter.GaussianBlur(1.6))                 # it sits behind the mark
    crop = ImageEnhance.Color(crop).enhance(1.15)
    a = np.asarray(crop).astype(float) / 255
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:N, 0:N]
    r = np.hypot(xx - N / 2, yy - N / 2) / (N / 2)
    # brighten where the arms sit: a soft screen toward white, like a lit core
    glow = lift * np.exp(-(r / 0.46) ** 2)[..., None]
    a = 1 - (1 - a) * (1 - glow)
    # irregular edge: the fade radius wanders, so the sky has no outline
    theta = np.arctan2(yy - N / 2, xx - N / 2)
    wander = WANDER.get(name, 0.12) * (noise(rng, 7, 40) - 0.5) + 0.05 * np.sin(3 * theta + seed)
    edge = np.clip((0.97 + wander - r) / 0.42, 0, 1) ** 1.6
    alpha = edge * (0.75 + 0.25 * noise(rng, 13, 18))
    out = np.dstack([np.clip(a, 0, 1) * 255, alpha * 255]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(os.path.join(ROOT, name), optimize=True)
    print("wrote", name, f"{os.path.getsize(os.path.join(ROOT, name)) // 1024} KB")
