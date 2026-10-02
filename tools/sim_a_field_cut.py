# -*- coding: utf-8 -*-
"""Sim A becomes the 3D field with a movable section cut (2 Oct 2026). Michael: the mesh
looked like a sheet; show the field in 3D with a slider to take a section cut along any
line, since what we were looking at is one cut. field-cut.js draws it. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "simulations.html")
s = open(P, encoding="utf-8").read()
assert "c-field" not in s

OLD_HEAD = '<div class="figure-title">Sim A: Spacetime Mesh Deforming Around Information Density Wells</div>'
NEW_HEAD = '<div class="figure-title">Sim A: The Information-Density Field in 3D, Cut Any Way You Like</div>'
a = s.index('<div class="sim-wrap" id="w-peg">')
b = s.index('</div>', s.index('<span class="sim-pill">Landauer → curvature</span>')) + len('</div>')
b = s.index('</div>', b) + len('</div>')          # close .sim-wrap
NEW_BODY = '''<div class="fc-grid">
          <div class="sim-wrap fc-3d" id="w-field">
            <canvas id="c-field" aria-label="Three-dimensional view of the information-density field and the cut plane. Drag to turn it."></canvas>
            <div class="sim-tl"><div class="sim-live"><div class="sim-dot"></div>Live · drag to turn</div></div>
            <div class="sim-tr"><span class="sim-pill">The field in 3D</span></div>
          </div>
          <div class="fc-cut">
            <canvas id="c-cut" width="480" height="480" aria-label="Heatmap of the field on the cut plane, changing over time."></canvas>
            <div class="sim-tl"><span class="sim-pill" style="background:rgba(241,227,3,.9);color:#1a1a2e;">The cut</span></div>
          </div>
        </div>
        <div class="fc-controls">
          <label>Direction <input type="range" id="cut-angle" min="0" max="180" value="0"></label>
          <label>Tilt <input type="range" id="cut-tilt" min="-90" max="90" value="90"></label>
          <label>Position <input type="range" id="cut-offset" min="-90" max="90" value="0"></label>
          <button type="button" id="cut-play" class="fc-play" aria-pressed="false">Pause</button>
          <p id="cut-readout" class="fc-readout"></p>
        </div>'''
s = s[:a] + NEW_BODY + s[b:]
assert s.count(OLD_HEAD) == 1
s = s.replace(OLD_HEAD, NEW_HEAD)

OLD_CAP = s[s.index('<div class="figure-caption">Three information-density wells warp the spacetime mesh in real time.'):]
OLD_CAP = OLD_CAP[:OLD_CAP.index('</div>') + len('</div>')]
NEW_CAP = ('<div class="figure-caption">Three information-density wells drift on slow orbits inside a volume of space. '
           'The density is highest at each well and falls off with distance, the pull inward that the framework identifies with gravity, '
           'while ripples move outward through time. On the left, the field as a glowing cloud: drag to turn it. On the right, '
           'the yellow plane’s cut through it, in viridis, where brightness tracks density. Move the sliders to cut along any direction. '
           'A flat, stretched sheet is the usual picture of curved space, but it is only one cut through something that fills every direction. '
           'An illustration of the framework’s equations, not measured data.</div>')
s = s.replace(OLD_CAP, NEW_CAP)

OLD_P = ("The simulation above renders this equation directly. Each of the three wells you see is a region of elevated P(x,t). "
         "The mesh deforms in proportion to ∇<sub>μ</sub>∇<sub>ν</sub>P, the gradient of that information field, just as mass deforms spacetime in standard GR. "
         "The gold coloring marks regions where the correction term is largest.")
NEW_P = ("The simulation above illustrates this equation. Each gold well is a region of elevated P(x,t); the correction term grows with how sharply "
         "P changes across space, ∇<sub>μ</sub>∇<sub>ν</sub>P, so the brightest bands in the cut are where it is largest. "
         "In standard general relativity, mass and energy play the role that information density plays here.")
assert s.count(OLD_P) == 1, s.count(OLD_P)
s = s.replace(OLD_P, NEW_P)

CSS = """
    /* Sim A: the field in 3D and its cut (field-cut.js) */
    .fc-grid { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr); gap: .75rem; background: #020408; padding: .75rem; border-radius: 8px; }
    .fc-3d { position: relative; height: 420px; }
    .fc-3d canvas { width: 100%; height: 100%; display: block; cursor: grab; }
    .fc-cut { position: relative; aspect-ratio: 1 / 1; align-self: center; }
    .fc-cut canvas { width: 100%; height: 100%; display: block; border-radius: 6px; border: 2px solid #f1e303; }
    .fc-controls { display: flex; flex-wrap: wrap; align-items: center; gap: .75rem 1.5rem; padding: .9rem .25rem .25rem; }
    .fc-controls label { display: flex; align-items: center; gap: .6rem; font: 600 .9rem 'IBM Plex Sans', sans-serif; color: #1a1a2e; }
    .fc-controls input[type=range] { width: 160px; accent-color: #005ba5; }
    .fc-play { font: 700 .85rem 'IBM Plex Sans', sans-serif; padding: .45rem 1rem; min-height: 40px; border-radius: 6px; border: 2px solid #005ba5; background: #fff; color: #005ba5; cursor: pointer; }
    .fc-readout { flex-basis: 100%; margin: 0; font: 500 .85rem 'IBM Plex Mono', monospace; color: #4a5868; }
    @media (max-width: 760px) { .fc-grid { grid-template-columns: minmax(0, 1fr); } .fc-3d { height: 320px; } .fc-cut { max-width: 340px; width: 100%; justify-self: center; } .fc-controls input[type=range] { width: 100%; } .fc-controls label { flex: 1 1 100%; } }
"""
i = s.index("</style>")
s = s[:i] + CSS + s[i:]
assert s.count("</body>") == 1
s = s.replace("</body>", '<script src="field-cut.js"></script>\n</body>')
open(P, "w", encoding="utf-8").write(s)
print("Sim A replaced")
