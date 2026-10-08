"""Builds the neon scan grid that lies over the dunes in poster v5.

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

def surface(px, d):                  # a point on the draped surface, at depth d (0 = horizon)
    s = skyline(px)
    py = s + (bottom - s) * d
    py -= (shade(px, py) - .35) * 34 * d
    return to_poster(px, max(py, s + 2))

# The scan: one sweep line part-way down the sand; the mesh is brightest around it,
# as if a beam from above is passing over it now.
DS = .30
def lit(d):
    return float(np.exp(-((d - DS) / .10) ** 2))

wide, crisp = [], []
for kind, v, pts in paths:
    if kind == 'h':
        op = .30 + .55 * lit(v)
    else:
        op = .34
    wide.append(f'<path d="{poly(pts)}" stroke-opacity="{op * .55:.2f}"/>')
    crisp.append(f'<path d="{poly(pts)}" stroke-opacity="{op:.2f}"/>')

# scanned points where the lines cross, brightest near the sweep
dots = []
for d in depths:
    for t in np.linspace(-1.6, 2.6, 46):
        px = vpx + (t * W0 * .5) * (0.04 + d)
        if px < 0 or px > W0: continue
        x, y = surface(px, d)
        r = 2.4 + 4 * d
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill-opacity="{.55 + .45 * lit(d):.2f}"/>')

# the sweep itself, and a curtain of light rising from it
scan = [surface(px, DS) for px in np.linspace(0, W0, 260)]
curtain = scan + [(x, y - 150) for x, y in reversed(scan)]

# beams from a scanner high above, fanning down onto the sweep line
SRC = (1900, 260)
beams = []
for i, (x, y) in enumerate(scan[::6]):
    if x < 1050: continue           # keep the beams in the open sky, clear of the subheading
    beams.append(f'<line x1="{SRC[0]}" y1="{SRC[1]}" x2="{x:.1f}" y2="{y:.1f}"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{POSTER_W}" height="2002" viewBox="0 0 {POSTER_W} 2002">
<defs>
  <linearGradient id="neon" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{POSTER_W}" y2="0">
    <stop offset="0" stop-color="#3fd8ff"/><stop offset=".45" stop-color="#8a6bff"/><stop offset="1" stop-color="#ff4fd8"/>
  </linearGradient>
  <linearGradient id="curtain" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#b98cff" stop-opacity=".45"/><stop offset="1" stop-color="#b98cff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="beam" gradientUnits="userSpaceOnUse" x1="0" y1="{SRC[1]}" x2="0" y2="1400">
    <stop offset="0" stop-color="#ff7be6" stop-opacity="0"/><stop offset=".55" stop-color="#b98cff" stop-opacity=".10"/><stop offset="1" stop-color="#7fe3ff" stop-opacity=".32"/>
  </linearGradient>
  <filter id="blur8" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="blur3" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="2.5"/></filter>
</defs>
<g stroke="url(#beam)" stroke-width="2">
{chr(10).join(beams)}
</g>
<path d="{poly(curtain)} Z" fill="url(#curtain)"/>
<g fill="none" stroke="url(#neon)" stroke-width="7" filter="url(#blur8)">
{chr(10).join(wide)}
</g>
<g fill="none" stroke="url(#neon)" stroke-width="2.2">
{chr(10).join(crisp)}
</g>
<g fill="#ffe6fb" filter="url(#blur3)">
{chr(10).join(dots)}
</g>
<path d="{poly(scan)}" fill="none" stroke="#ffd6f6" stroke-width="12" stroke-opacity=".55" filter="url(#blur8)"/>
<path d="{poly(scan)}" fill="none" stroke="#fff2fc" stroke-width="3"/>
</svg>'''
open(out, 'w').write(svg)
print('skyline (poster y) min/max:', round(OY + sky.min() * 4 * SC), round(OY + sky.max() * 4 * SC), 'paths:', len(paths), 'dots:', len(dots))
