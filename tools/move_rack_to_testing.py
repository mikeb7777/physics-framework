# -*- coding: utf-8 -*-
"""Move the test rack from validation.html to the top of testing-schedule.html as test
loggers (2 Oct 2026). Michael: make them look like a bench data logger (Graphtec GL260),
one per test, and move them from the bottom of the Validation page to the top of the
Testing page. The cards' own markup moves unchanged (prediction and outcome text is the
record's); test-loggers.js turns each into a logger. Run once."""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V, TS = os.path.join(ROOT, "validation.html"), os.path.join(ROOT, "testing-schedule.html")
v, t = open(V, encoding="utf-8").read(), open(TS, encoding="utf-8").read()
assert 'id="lg-grid"' not in t

# ---- the cards, exactly as they are
g0 = v.index('<div class="rcard-grid">') + len('<div class="rcard-grid">')
g1 = v.index('</div><!-- /rcard-grid -->')
cards = v[g0:g1].replace(' data-bench="desi"', '')

# ---- validation.html: pointer in place of the rack
p0 = v.index('<p style="color:rgba(255,255,255,.92); font-size:.78rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:.9rem;">Next tests:')
p1 = v.index('</div><!-- /rack-housing -->') + len('</div><!-- /rack-housing -->')
pointer = '''<div style="display:flex; flex-wrap:wrap; align-items:center; gap:1rem 1.5rem; background:#1d2027; border-left:4px solid #f1e303; border-radius:8px; padding:1.1rem 1.4rem;" data-aos="fade-up">
      <p style="margin:0; flex:1 1 320px; color:rgba(255,255,255,.92); font-size:.95rem; line-height:1.6;"><strong style="color:#fff;">The next tests now have their own instruments.</strong> Each one runs on a test logger at the top of the Testing page: what it measures, how it will be decided, its countdown, the new papers bearing on it, and all three outcomes.</p>
      <a href="testing-schedule.html#loggers" style="flex:0 0 auto; color:#1a1d33; background:#f1e303; font-weight:700; font-size:.9rem; text-decoration:none; border-radius:6px; padding:.55rem 1rem;">Open the test loggers &rarr;</a>
    </div>'''
v = v[:p0] + pointer + v[p1:]
assert v.count('<script src="rack-bench.js" defer></script>\n') == 1
v = v.replace('<script src="rack-bench.js" defer></script>\n', '')

# ---- testing-schedule.html: the loggers right under the page header
SECTION = '''

    <!-- Test loggers: one bench data logger per test (test-loggers.js, test-loggers.css) -->
    <section class="lg-section" id="loggers" aria-labelledby="lg-title">
      <div class="lg-inner">
        <p class="eyebrow">Test loggers</p>
        <h2 id="lg-title" style="color:var(--text-dark); margin:0;">Every test on its own instrument</h2>
        <p class="lg-intro">Each test has a logger. Its screen shows what the test measures and how it will be decided, the lights show its stage, the readout counts down to the data and counts the new papers bearing on it, and <strong>ENTER</strong> opens the prediction with all three outcomes. A green, yellow or red lamp lights only when the data arrives.</p>
        <div class="lg-grid" id="lg-grid"></div>
        <div id="lg-src" class="lg-src" hidden>''' + cards + '''</div>
      </div>
    </section>'''
h0 = t.index('<section id="main-content" tabindex="-1" class="page-header tp-left">')
h1 = t.index('</section>', h0) + len('</section>')
t = t[:h1] + SECTION + t[h1:]
assert t.count('</head>') == 1 and t.count('</body>') == 1
t = t.replace('</head>', '  <link rel="stylesheet" href="test-loggers.css">\n</head>')
t = t.replace('</body>', '<script src="test-loggers.js" defer></script>\n</body>')

open(V, "w", encoding="utf-8").write(v)
open(TS, "w", encoding="utf-8").write(t)
subprocess.run(["git", "rm", "-q", "rack-bench.js"], cwd=ROOT, check=True)   # superseded by test-loggers.js
print("moved", cards.count('class="rcard"'), "cards; validation pointer added")
