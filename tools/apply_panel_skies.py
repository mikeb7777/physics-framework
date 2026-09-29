# -*- coding: utf-8 -*-
"""Title-panel Spinner on the testing schedule and the results registry:
a real sky behind it (each page its own), the centred Spinner over it."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    "testing-schedule.html": ("sky-testing.png", "Behind the Spinner: Terzan 5. NASA, ESA, CSA, STScI, G.&nbsp;Zullo"),
    "results.html": ("sky-results.png", "Behind the Spinner: the Milky Way over Rubin. RubinObs/NOIRLab/SLAC/NSF/DOE/AURA/H.&nbsp;Stockebrand (CC BY 4.0)"),
}
OLD_CSS = """      .panel-spinner {
        position: absolute; top: 50%; right: clamp(1rem, 5vw, 6rem);
        width: clamp(150px, 16vw, 200px); height: auto;
        opacity: .85; pointer-events: none;"""
NEW_CSS = """      /* A real sky behind the Spinner (tools/make_spinner_skies.py), still
         while the Spinner turns over it, lit where the arms sit so all three
         colors read on the navy panel. Centred on the Spinner by construction. */
      .panel-sky {
        --spin-w: clamp(150px, 16vw, 200px);
        position: absolute; top: 50%;
        right: calc(clamp(1rem, 5vw, 6rem) + var(--spin-w) / 2);
        width: calc(var(--spin-w) * 2.1); height: auto;
        transform: translate(50%, -50%); pointer-events: none; z-index: 0;
      }
      .panel-sky-credit {
        position: absolute; right: clamp(1rem, 5vw, 6rem); bottom: .55rem; margin: 0; z-index: 1;
        font-size: .68rem; color: rgba(255, 255, 255, .55); max-width: 320px; text-align: right;
      }
      @media (max-width: 1100px) { .panel-sky, .panel-sky-credit { display: none; } }
      .panel-spinner {
        position: absolute; top: 50%; right: clamp(1rem, 5vw, 6rem);
        width: clamp(150px, 16vw, 200px); height: auto; z-index: 1;
        padding: clamp(18px, 2vw, 26px); box-sizing: border-box;
        pointer-events: none;"""
OLD_IMG = '<img src="our logo.png?v=rgb" class="panel-spinner" alt="" aria-hidden="true">'

for page, (sky, credit) in PAGES.items():
    p = os.path.join(ROOT, page)
    t = open(p, encoding="utf-8").read()
    assert t.count(OLD_CSS) == 1 and t.count(OLD_IMG) == 1, page
    t = t.replace(OLD_CSS, NEW_CSS)
    t = t.replace(OLD_IMG, f'<img src="{sky}?v=1" class="panel-sky" alt="" aria-hidden="true">\n    '
                           f'<img src="spinner-centered.png?v=1" class="panel-spinner" alt="" aria-hidden="true">\n    '
                           f'<p class="panel-sky-credit">{credit}</p>')
    if "--write" in sys.argv:
        open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", page)
