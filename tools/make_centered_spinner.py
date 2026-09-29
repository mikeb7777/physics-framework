"""spinner-centered.png: the Spinner on a square canvas with its centre of
symmetry exactly in the middle, so it turns in place.

"our logo.png" is 254 x 266 and the arms balance 26 px off its centre, so a
CSS rotation swung the tips out past any disc drawn round it. The three arms
are congruent, so their centre of mass is the centre of symmetry: that point
goes in the middle, with an even margin to the farthest tip. Drawn from the
vector mark (Ic2-Mission-Medal/spinner-mark.svg) for a sharp edge at any size.
"""
import os
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(os.path.dirname(HERE), "Ic2-Mission-Medal", "spinner-mark.svg")
OUT = os.path.join(HERE, "spinner-centered.png")
BIG, SIZE, MARGIN = 1600, 640, 0.02

svg = open(SVG, encoding="utf-8").read()
svg = svg[svg.index("<svg"):].replace('width="100" height="100"', f'width="{BIG}" height="{BIG}"')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": BIG, "height": BIG})
    pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
    raw = pg.screenshot(omit_background=True, clip={"x": 0, "y": 0, "width": BIG, "height": BIG})
    b.close()
import io
im = Image.open(io.BytesIO(raw)).convert("RGBA")
a = np.asarray(im).astype(float)
w = a[:, :, 3] / 255
yy, xx = np.mgrid[0:BIG, 0:BIG]
cx, cy = (xx * w).sum() / w.sum(), (yy * w).sum() / w.sum()
R = np.hypot(xx[w > 0.5] - cx, yy[w > 0.5] - cy).max() * (1 + MARGIN)
box = (int(round(cx - R)), int(round(cy - R)), int(round(cx + R)), int(round(cy + R)))
canvas = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 0))
canvas.alpha_composite(im, (-box[0], -box[1]))
canvas.resize((SIZE, SIZE), Image.LANCZOS).save(OUT, optimize=True)
print(f"wrote {OUT}: {SIZE}x{SIZE}, centre of symmetry in the middle, tips reach {1 / (1 + MARGIN):.1%} of the half-width")
