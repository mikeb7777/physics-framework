# -*- coding: utf-8 -*-
"""Michael, 29 Sep 2026 ("Those are valid changes"):
1. Footer: "independent platform" becomes "independent research institute".
2. Research Opportunities: the "limited budget and manpower" line is restated
   the way an institute in its founding years describes itself.
3. Instruments: the "not an argument against science" thesis line gives way to
   the Quest page header used on the Map and Follow pages."""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quest_header import head_section, CSS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 0
for p in glob.glob(os.path.join(ROOT, "*.html")):
    t = open(p, encoding="utf-8").read()
    u = t.replace("is an independent platform advancing theoretical physics", "is an independent research institute advancing theoretical physics")
    if u != t:
        open(p, "w", encoding="utf-8", newline="").write(u); n += 1
print("footer wording:", n, "pages")

p = os.path.join(ROOT, "research-opportunities.html")
t = open(p, encoding="utf-8").read()
for old, new in (
    ("<h2>Early stage. Real ceiling. Consequential direction.</h2>", "<h2>Founding years. A consequential direction.</h2>"),
    ("""                    The Ic² Research Institute is an independent research program with limited budget and manpower.
                    That is stated plainly because obscuring it would undermine everything else.""",
     """                    The Ic² Research Institute is an independent research institute in its founding years.
                    Its pace is set by people and time, which is where support at this stage makes the most difference."""),
):
    assert t.count(old) == 1, old[:50]
    t = t.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok research-opportunities.html")

p = os.path.join(ROOT, "instruments.html")
t = open(p, encoding="utf-8").read()
m = re.search(r'<section class="q-hero">.*?</section>', t, re.S)
assert m, "instruments q-hero"
print("instruments hero was:", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0)))[:400])
