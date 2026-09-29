"""Natural glow for the index hero, drawn behind the Spinner (not part of it).

Writes hero-glow.png (transparent) for .hero-glow. Everything is irregular on
purpose, because an even glow reads as artificial:
  - a nebula made of several octaves of smooth noise, stretched along a tilted
    axis so it is not a perfect circle, with warm and cool lobes;
  - starburst rays at random angles, lengths, widths and brightness, a few long
    ones and many short ones, each tapering and slightly soft;
  - a white core that stays bright under the Spinner's arms so all three
    colors read (they fail 3:1 on the navy hero directly);
  - a sprinkling of faint stars in the outer haze.
Deterministic: the same seed always gives the same image.
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageFilter

N = 1100                  # output size, px (displayed at about 2.3x the Spinner's width)
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 11
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hero-glow.png")
SPIN_R = 0.217            # Spinner half-width as a fraction of the glow width (213 / 2.3 / 213 / 2)

rng = np.random.default_rng(SEED)
yy, xx = np.mgrid[0:N, 0:N].astype(float)
cx = cy = (N - 1) / 2
dx, dy = (xx - cx) / N, (yy - cy) / N           # -0.5 .. 0.5
r = np.hypot(dx, dy)                            # 0 at centre, 0.5 at the edge midpoints
theta = np.arctan2(dy, dx)


def smooth_noise(cells, blur):
    small = rng.random((cells, cells))
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
    return np.array(im.filter(ImageFilter.GaussianBlur(blur))).astype(float) / 255


def fbm():
    total, amp, norm = 0, 1.0, 0
    for cells, blur in ((5, 40), (11, 18), (23, 8), (47, 3)):
        total = total + amp * smooth_noise(cells, blur)
        norm += amp
        amp *= 0.55
    return total / norm


# 1 nebula: tilted, stretched falloff whose edge is broken up by noise
tilt = math.radians(rng.uniform(-35, 35))
u = dx * math.cos(tilt) + dy * math.sin(tilt)
v = -dx * math.sin(tilt) + dy * math.cos(tilt)
stretched = np.hypot(u / 1.18, v / 0.86)
warp = fbm()
neb = np.exp(-((stretched * (0.72 + 0.6 * warp)) / 0.27) ** 2)
wisps = np.clip((fbm() - 0.40) * 2.6, 0, 1) * np.exp(-(r / 0.36) ** 2)
filaments = np.clip((fbm() - 0.52) * 4.0, 0, 1) * np.exp(-(r / 0.42) ** 2)
nebula = np.clip(0.62 * neb + 0.42 * wisps + 0.32 * filaments, 0, 1)

# 2 core: a soft glow (no hard disc edge) that is still near-white where the
# arms sit, so all three Spinner colors read
core = np.clip(1.25 * np.exp(-(r / (SPIN_R * 1.05)) ** 2.4), 0, 1)

# 3 rays: irregular angles, lengths (a few long, many short), widths, strengths
rays = np.zeros((N, N))
count = 40
angles = np.sort(rng.uniform(0, 2 * math.pi, count))
for ang in angles:
    long_one = rng.random() < 0.3
    length = rng.uniform(0.38, 0.49) if long_one else rng.uniform(0.24, 0.37)
    width = rng.uniform(0.0035, 0.0065) if long_one else rng.uniform(0.005, 0.012)   # half-width at the core, fraction of N
    strength = rng.uniform(0.75, 1.0) if long_one else rng.uniform(0.3, 0.7)
    d = np.angle(np.exp(1j * (theta - ang)))
    across = np.abs(np.sin(d)) * r * (np.cos(d) > 0)  # distance from the ray's line, outward half only
    across = np.where(np.cos(d) > 0, across, 1.0)
    taper = width * (1.0 - 0.6 * np.clip(r / length, 0, 1))  # narrows toward the tip
    along = np.clip(1 - r / length, 0, 1) ** rng.uniform(0.9, 1.6)
    rays += strength * np.exp(-(across / taper) ** 2) * along
rays = np.clip(rays, 0, 1)
rays = np.array(Image.fromarray((rays * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))).astype(float) / 255
ray_glow = np.array(Image.fromarray((rays * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))).astype(float) / 255
rays = np.clip(1.35 * rays + 0.7 * ray_glow, 0, 1) * (0.65 + 0.45 * warp)   # rays flicker along their length

# 4 faint stars in the outer haze
stars = np.zeros((N, N))
for _ in range(38):
    rr_ = rng.uniform(0.2, 0.47); a = rng.uniform(0, 2 * math.pi)
    sx, sy = int(cx + rr_ * N * math.cos(a)), int(cy + rr_ * N * math.sin(a))
    if 2 <= sx < N - 2 and 2 <= sy < N - 2:
        stars[sy, sx] = rng.uniform(0.35, 1.0)
stars = np.array(Image.fromarray((stars * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.3))).astype(float) / 255 * 6
stars = np.clip(stars, 0, 1) * np.clip(1 - r / 0.5, 0, 1)

# alpha: everything fades to nothing before the square's edge
edge = np.clip(1 - (r / 0.49) ** 4, 0, 1)
alpha = np.clip(np.maximum.reduce([core, nebula, rays, stars]) + 0.25 * nebula * rays, 0, 1) * edge

# colour: white core, then pale blue, with violet, cyan and a faint rose in lobes
lobe_a, lobe_b = fbm(), fbm()
t = np.clip((r - SPIN_R * 0.9) / 0.28, 0, 1)[..., None]
white = np.array([255, 255, 255.0])
pale = np.array([214, 232, 255.0])
violet = np.array([176, 150, 255.0])
cyan = np.array([150, 222, 255.0])
rose = np.array([255, 186, 226.0])
tint = (pale
        + (violet - pale) * np.clip((lobe_a - 0.40) * 3.0, 0, 1)[..., None]
        + (cyan - pale) * np.clip((lobe_b - 0.45) * 2.8, 0, 1)[..., None] * 0.9
        + (rose - pale) * np.clip((lobe_a - 0.58) * 3.2, 0, 1)[..., None] * 0.6)
rgb = white * (1 - t) + tint * t
rgb = np.where((rays > 0.35)[..., None], rgb * 0.6 + white * 0.4, rgb)   # rays stay near white

img = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
Image.fromarray(img, "RGBA").save(OUT, optimize=True)
print(f"wrote {OUT} ({N}x{N}, seed {SEED}, {os.path.getsize(OUT) // 1024} KB)")
