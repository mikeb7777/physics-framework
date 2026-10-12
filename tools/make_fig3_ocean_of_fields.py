#!/usr/bin/env python3
"""Redraw fig3-ocean-of-fields.png on a white background with corrected labels.

Schematic only: the rings are illustrative, not computed field solutions.
Run from the repository root:  python3 tools/make_fig3_ocean_of_fields.py
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

W, H = 2501, 1415
fig = plt.figure(figsize=(W / 200, H / 200), dpi=200, facecolor='white')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-0.7075, 0.7075)
ax.set_aspect('equal')
ax.axis('off')

rng = np.random.default_rng(7)
th = np.linspace(0, 2 * np.pi, 1600)

BLUE, RED, PINK, GOLD, TEAL, GREY = '#2b6cb0', '#b91c1c', '#c0397b', '#b7791f', '#2c7a7b', '#9aa3ad'
INK, MUTED = '#1f2933', '#52606d'


def ring(r, ax_ratio=0.62, wob=(), phase=0.0):
    rr = r * np.ones_like(th)
    for k, a, p in wob:
        rr = rr * (1 + a * np.cos(k * th + phase))
    return rr * np.cos(th), rr * ax_ratio * np.sin(th)


# faint thermal rings and speckle
for r in (0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2):
    x, y = ring(r, 0.62)
    ax.plot(x, y, color=GREY, lw=0.6, alpha=0.35)
ax.scatter(rng.uniform(-1.2, 1.2, 160), rng.uniform(-0.68, 0.68, 160), s=2, color=TEAL, alpha=0.35, lw=0)

# Schumann EM (blue), slow wobble
for r, a in ((0.5, 0.04), (0.72, 0.05), (0.92, 0.06)):
    x, y = ring(r, 0.64, [(2, a, 0), (4, a * 0.6, 0), (6, a * 0.3, 0)])
    ax.plot(x, y, color=BLUE, lw=2.2 if r < 0.9 else 1.4, alpha=0.9 if r < 0.9 else 0.55)

# higher Schumann modes (gold dotted)
for r in (0.43, 0.63):
    x, y = ring(r, 0.66, [(4, 0.04, 0), (2, 0.02, 0)])
    ax.plot(x, y, color=GOLD, lw=1.6, ls=(0, (1, 2.2)), alpha=0.9)

# 60 Hz grid field (red zigzag)
for r in (0.36, 0.55):
    n = 90 if r < 0.4 else 80
    t = np.linspace(0, 2 * np.pi, 4000)
    rr = r * (1 + 0.05 * np.cos(2 * t)) + 0.02 * np.sin(n * t)
    ax.plot(rr * np.cos(t), rr * 0.64 * np.sin(t), color=RED, lw=1.3, alpha=0.75)

# acoustic field (pink)
for r, a in ((0.2, 0.18), (0.45, 0.1)):
    x, y = ring(r, 0.85 if r < 0.3 else 0.7, [(4, a, 0), (2, a * 0.4, 0)])
    ax.plot(x, y, color=PINK, lw=1.6, alpha=0.85)

# nodal-surface intersections
stars = [(-0.30, 0.0), (0.30, 0.0), (0.55, 0.24), (-0.55, 0.24), (0.66, 0.0), (-0.66, 0.0),
         (0.45, -0.3), (-0.45, -0.3)]
ax.scatter([s[0] for s in stars], [s[1] for s in stars], marker='*', s=210, color='#d69e2e',
           edgecolor='#975a16', lw=0.6, zorder=5)

ax.scatter([0], [0], s=110, color='#f6ad55', edgecolor=INK, lw=1.2, zorder=6)
ax.text(0.07, 0.07, 'YOU', fontsize=13, fontweight='bold', color=INK, zorder=6)

# labels
ax.text(0.85, 0.5, 'Thermal EM\n(broadband)', color=TEAL, fontsize=10, va='top')
ax.text(-1.2, 0.2, 'Acoustic field\n(heartbeat, 1.2 Hz)', color=PINK, fontsize=10, va='bottom')
ax.text(1.0, 0.03, 'Schumann EM\n(7.83 Hz)', color=BLUE, fontsize=10)
ax.text(0.9, -0.24, '60 Hz power\ngrid field', color=RED, fontsize=10)
ax.text(-1.2, -0.2, 'Higher Schumann modes\n(~6.5 Hz spacing;\none near 60 Hz)', color=GOLD, fontsize=10)

ax.text(0, 0.675, 'Figure 3: The Ocean of Fields We Inhabit, Simultaneously, Always\n'
        'Every physics diagram shows one field, in isolation, in two dimensions.',
        ha='center', va='top', fontsize=13, fontweight='bold', color=INK)
ax.text(-1.2, -0.585, '★ = Point where multiple field nodal surfaces intersect simultaneously',
        color=GOLD, fontsize=10, style='italic', va='center')
ax.text(0, -0.655, 'A schematic of the field structure of the space you occupy right now.\n'
        'None of these fields exist in isolation. Their coupled 3D nodal topology has never been mapped.',
        ha='center', va='center', fontsize=10, style='italic', color=MUTED)

fig.savefig('fig3-ocean-of-fields.png', dpi=200, facecolor='white')
print('saved fig3-ocean-of-fields.png', W, H)
