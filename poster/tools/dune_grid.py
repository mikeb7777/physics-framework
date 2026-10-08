"""Builds the measurement grid that lies over the dunes in poster v5.

Finds the skyline (where the sand meets the sky) in each column of the
photograph, then draws a perspective grid on the sand: lines of equal depth
follow the skyline and flatten towards the foreground, with a small lift from
the sand's shading so the grid reads as draped over the surface. Writes an SVG
in poster coordinates (the photo sits at left -336 px, top 0, 3000 px wide).

    python3 -I poster/tools/dune_grid.py poster/bg-desert-night.jpg poster/dune-grid.svg
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
W0, H0 = im.size
SC = 3000 / W0                      # photo px -> poster px
OX, OY = -336, 0
POSTER_W = 2328

small = im.resize((W0 // 4, H0 // 4))
a = np.asarray(small).astype(float)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
notsky = B <= R - 6                 # sky is blue; sand, lit or in shadow, is not
h, w = notsky.shape
sky = np.zeros(w)
for x in range(w):
    col = notsky[:, x]
    ys = np.where(col[h // 3:])[0] + h // 3
    y0 = h - 1
    for y in ys:                    # first run of not-sky at least 8 px deep
        if col[y:y + 8].all():
            y0 = y; break
    sky[x] = y0
m = 15                              # median filter: removes spikes from grass and shadow
pad = np.pad(sky, m, mode='edge')
sky = np.array([np.median(pad[i:i + 2 * m + 1]) for i in range(w)])
k = 12
sky = np.convolve(np.pad(sky, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), mode='valid')

lum = np.asarray(small.convert('L').filter(ImageFilter.GaussianBlur(16))).astype(float) / 255

def skyline(px):                     # photo px -> skyline y in photo px
    i = min(w - 1, max(0, int(px / 4)))
    return sky[i] * 4

def shade(px, py):
    i, j = min(w - 1, max(0, int(px / 4))), min(h - 1, max(0, int(py / 4)))
    return lum[j, i]

def to_poster(px, py):
    return OX + px * SC, OY + py * SC

bottom = H0 * 1.0
vpx = W0 * 0.56                      # vanishing point on the horizon
depths = [((i + 1) / 26) ** 1.9 for i in range(26)]   # dense near the horizon
paths = []
# lines of equal depth: follow the skyline, lifted a little by the shading
for d in depths:
    pts = []
    for px in np.linspace(0, W0, 260):
        s = skyline(px)
        py = s + (bottom - s) * d
        py -= (shade(px, py) - .35) * 34 * d          # ridges lift, hollows dip
        py = max(py, s + 2)                           # never above the skyline
        pts.append(to_poster(px, py))
    paths.append(('h', d, pts))
# lines that run away from the viewer, converging on the vanishing point
for t in np.linspace(-1.6, 2.6, 46):
    pts = []
    for d in np.linspace(0.0, 1.0, 80):
        dd = d ** 1.9
        px = vpx + (t * W0 * .5) * (0.04 + dd)
        if px < -50 or px > W0 + 50: continue
        s = skyline(px)
        py = s + (bottom - s) * dd
        py -= (shade(px, py) - .35) * 34 * dd
        py = max(py, s + 2)
        pts.append(to_poster(px, py))
    if len(pts) > 2: paths.append(('v', t, pts))

def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)

# depth-cued opacity: faint near the horizon, stronger close up
lines = []
for kind, v, pts in paths:
    op = .16 + .30 * (v if kind == 'h' else .6)
    lines.append(f'<path d="{poly(pts)}" stroke-opacity="{op:.2f}"/>')
# a measured baseline: a dimension line with ticks across the foreground
by = to_poster(0, skyline(W0 * .3) + (bottom - skyline(W0 * .3)) * .42)[1]
ticks = ''.join(f'<line x1="{x}" y1="{by - 10:.0f}" x2="{x}" y2="{by + 10:.0f}"/>' for x in range(260, 2120, 186))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{POSTER_W}" height="2002" viewBox="0 0 {POSTER_W} 2002">
<defs><filter id="glow" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g fill="none" stroke="#9ff3ff" stroke-width="2.1" filter="url(#glow)">
{chr(10).join(lines)}
</g>
</svg>'''
open(out, 'w').write(svg)
print('skyline (poster y) min/max:', round(OY + sky.min() * 4 * SC), round(OY + sky.max() * 4 * SC), 'paths:', len(paths))
