# -*- coding: utf-8 -*-
"""Moving thumbnail gallery at the top of simulations.html (2 Oct 2026). Michael: the page
looks static; he expected to see the simulations move. Each tile is a short silent loop
recorded by tools/record_sim_thumbs.py; clicking one opens that simulation's panel.
Videos load and play only while on screen; with reduced motion they show the poster. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "simulations.html")
s = open(P, encoding="utf-8").read()
assert "sim-gallery" not in s

TILES = [  # canvas id, lazy key, label
    ("c-field", "peg3d", "A · The field in 3D, cut any way"),
    ("c-ent", "ent3d", "B · Space from entanglement"),
    ("c-rot", "rot3d", "C · Spin across scales"),
    ("c-four", "four3d", "D · Four forces"),
    ("c-scram", "scram3d", "E · Information scrambling"),
    ("c-bang", "bang3d", "F · Spacetime crystallizes"),
    ("c-bamboo", "bamboo", "G · The Bamboo Principle"),
    ("c-bell", "bell", "H · Bell correlation"),
    ("c-subplanck", "subplanck", "I · Sub-Planck substrate"),
    ("c-chamber", "chamber", "Model · Acoustic chamber"),
    ("c-nowwin", "nowwin", "Where your “now” is"),
    ("c-phi", "phimotion", "The journey never shown"),
]
tiles = "\n".join(
    f'''        <button type="button" class="sg-tile" data-open="{k}">
          <video muted loop playsinline preload="none" poster="sim-thumbs/{c}.jpg" data-src="sim-thumbs/{c}.mp4" aria-hidden="true"></video>
          <span class="sg-label">{lab}</span>
        </button>''' for c, k, lab in TILES)
HTML = f'''
    <div class="sim-gallery" aria-label="Simulations at a glance">
      <p class="eyebrow">Watch them move</p>
      <h2 style="margin:.25rem 0 .5rem;">Every simulation, running</h2>
      <p class="sg-intro">Each tile is a few seconds of the live simulation. Click one to open it below, where you can turn it, change its settings and read what it shows.</p>
      <div class="sg-grid">
{tiles}
      </div>
    </div>
    <hr class="section-rule">
'''
ANCHOR = '<div class="color-key"'
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, HTML + "    " + ANCHOR)

CSS = """
    /* Moving thumbnail gallery (sim-thumbs/, tools/sim_gallery.py) */
    .sim-gallery { max-width: 1200px; margin: 0 auto 2rem; }
    .foundation-accordion { scroll-margin-top: 90px; }
    .sg-intro { color: #4a5868; margin: 0 0 1rem; }
    .sg-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(250px, 100%), 1fr)); gap: 1rem; }
    .sg-tile { position: relative; display: block; padding: 0; border: 1px solid #1f2a3a; border-radius: 8px; overflow: hidden; background: #020408; cursor: pointer; aspect-ratio: 16 / 9; transition: transform .2s ease, box-shadow .2s ease; }
    .sg-tile:hover, .sg-tile:focus-visible { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,.25); }
    .sg-tile:focus-visible { outline: 3px solid #f1e303; outline-offset: 2px; }
    .sg-tile video { width: 100%; height: 100%; object-fit: cover; display: block; }
    .sg-label { position: absolute; left: 0; right: 0; bottom: 0; padding: 1.4rem .75rem .55rem; text-align: left; font: 600 .9rem 'IBM Plex Sans', sans-serif; color: #fff; background: linear-gradient(transparent, rgba(2,4,8,.92)); }
    @media (max-width: 560px) { .sg-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .6rem; } .sg-label { font-size: .75rem; padding: 1rem .5rem .4rem; } }
"""
i = s.index("</style>")
s = s[:i] + CSS + s[i:]

JS = """<script>
/* Simulation gallery: play tiles only while visible; click opens the matching panel. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.sg-tile').forEach(function (tile) {
    var v = tile.querySelector('video');
    tile.addEventListener('click', function () {
      var acc = document.querySelector('.foundation-accordion[data-lazy-sim="' + tile.getAttribute('data-open') + '"]');
      if (!acc) return;
      if (!acc.classList.contains('active')) acc.querySelector('.foundation-header').click();
      setTimeout(function () { acc.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }, 360);
    });
    if (reduce || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { if (!v.src) v.src = v.getAttribute('data-src'); var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }, { rootMargin: '100px' }).observe(tile);
  });
})();
</script>
"""
assert s.count("</body>") == 1
s = s.replace("</body>", JS + "</body>")
open(P, "w", encoding="utf-8").write(s)
print("gallery added")
