# -*- coding: utf-8 -*-
"""Visualizations: the black hole anatomy, computed rather than painted (6 Oct 2026). The handoff planned an AI
background image (Illustration); Michael had none, so viz/black-hole.html ray-traces a non-spinning black hole
from general relativity in the browser, which makes it a Simulation, with the guided label tour from the
handoff (Play, Step, Explore). Adds the card to the Simulations section and updates the Renderings note.
Run once."""
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "visualizations.html")
s = open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


CARD = """<article class="viz-card" data-prov="simulated" id="black-hole">
        <div class="viz-embed"><iframe src="viz/black-hole.html" title="Black hole anatomy: computed from general relativity, with a guided tour" loading="lazy" style="height:620px"></iframe></div>
        <div class="viz-body">
          <div class="viz-tags"><span class="tag tag-simulated">Simulated</span></div>
          <h3>Black hole anatomy, computed in your browser</h3>
          <p>This black hole is not a painting. Every pixel follows a ray of light backward through the curved spacetime of a non-spinning black hole, as general relativity describes it, until the light falls in, strikes the disk, or escapes to the stars. That is why the far side of the disk appears arched over the top, and why one side of the disk is brighter than the other.</p>
          <p>Press Play tour for a guided walk from the singularity outward, step through the parts with Back and Next, or explore by tapping. Change the view angle to see the lensing shift. The last stop, the information paradox, is marked as the framework's proposal; everything else is established physics.</p>
          <dl class="viz-meta">
            <div><dt>Method: </dt><dd>Light paths in the Schwarzschild geometry; thin disk with gravitational redshift and Doppler beaming. No spin, so no ergosphere or jets. Colors scaled to visible light.</dd></div>
            <div><dt>Source: </dt><dd>Ic&sup2; Research Institute. Label wording from the Big TOE visualization brief.</dd></div>
            <div><dt>In the book: </dt><dd>Element 19, Black Hole Information</dd></div>
            <div><a class="viz-link" href="viz/black-hole.html" target="_blank" rel="noopener">Open full screen</a></div>
          </dl>
        </div>
      </article>
      """

anchor = '<div class="foundation-accordion" data-prov="simulated" id="chamber-model"'
i = s.index(anchor)
s = s[:i] + CARD + s[i:]

rep("The first rendering, an annotated anatomy of a spinning black hole, is in preparation. The artwork will be labeled as illustration; its labels will follow general relativity.",
    "No renderings yet. The black hole anatomy was planned as an AI rendering, but it is now computed from general relativity instead, so it sits under Simulations. Renderings will appear here when an image is made for explanation rather than computed.")

rep("    /* Watermark: names the Institute", """    .viz-embed { background:#05070d; }
    .viz-embed iframe { display:block; width:100%; border:0; }
    .viz-link { font-weight:600; color:#005ba5; }
    /* Watermark: names the Institute""")

rep("  window.addEventListener('hashchange', applyHash);", """  window.addEventListener('message', function (e) {
    if (!e.data || !e.data.bhHeight) return;
    document.querySelectorAll('.viz-embed iframe').forEach(function (f) { if (f.contentWindow === e.source) f.style.height = e.data.bhHeight + 'px'; });
  });
  window.addEventListener('hashchange', applyHash);""")
open(P, "w", encoding="utf-8").write(s)
print("ok")
