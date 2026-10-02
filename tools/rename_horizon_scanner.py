# -*- coding: utf-8 -*-
"""Rename the Media page to Horizon Scanner (2 Oct 2026). Michael: "Change Media to
Horizon Scanner." The page now leads with the living review of new research and the
field trends; press stays below. File name media.html is kept so links keep working.
Section names follow the standard terms: horizon scanning (the page), living review
(new research on our tests), trends (scientometrics). Run once."""
import glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

n = 0
for p in glob.glob("*.html"):
    s = open(p, encoding="utf-8").read()
    t = s.replace('<a href="media.html">Media</a>', '<a href="media.html">Horizon Scanner</a>')
    t = t.replace('see the <a href="media.html" style="color:#f1e303;">media page</a>', 'see the <a href="media.html" style="color:#f1e303;">Horizon Scanner</a>')
    if t != s:
        n += t.count("Horizon Scanner</a>"); open(p, "w", encoding="utf-8").write(t)
print("links renamed:", n)

P = "media.html"
s = open(P, encoding="utf-8").read()
R = [
    ("<title>Media &amp; Press | Ic² Research Institute</title>", "<title>Horizon Scanner | Ic² Research Institute</title>"),
    ('<meta property="og:title" content="Media &amp; Press | Ic² Research Institute">', '<meta property="og:title" content="Horizon Scanner | Ic² Research Institute">'),
    ('content="Media resources, press coverage, conference appearances, and visual assets for the Ic² Research Institute and The Big TOE framework."',
     'content="The Ic² Research Institute\'s horizon scanner: a living review of new research on every test we run, trends in interest and funding across the field, and our news and press record."'),
    ('<p class="eyebrow page-label">Press</p>\n      <h1>The story so far, for the record</h1>',
     '<p class="eyebrow page-label">Horizon Scanner</p>\n      <h1>Watching the field our tests belong to</h1>'),
    ("<p>What the field is finding that bears on our tests, updated every week, alongside news coverage, conference appearances and press resources.</p>",
     "<p>A living review of new research on every question we test, how interest and funding are moving across the field, and the institute&rsquo;s own news and press record. Updated every week.</p>"),
    ('<p class="section-label eyebrow">Field Watch</p>', '<p class="section-label eyebrow">Living Review</p>'),
    ("Every week an automated search reads new papers on arXiv and in journals for work that bears on our registered tests.",
     "Our predictions are kept under living review. Every week an automated search reads new papers on arXiv and in journals for work that bears on our registered tests."),
    ('<p class="section-label eyebrow">Field Trends</p>', '<p class="section-label eyebrow">Trends</p>'),
    ('<p class="section-label eyebrow">Featured</p>\n        <h2 class="section-title">In the News</h2>',
     '<p class="section-label eyebrow">Press</p>\n        <h2 class="section-title">In the News</h2>'),
]
for a, b in R:
    assert s.count(a) == 1 or (a.startswith('content=') and s.count(a) >= 1), a[:60]
    s = s.replace(a, b)
open(P, "w", encoding="utf-8").write(s)

idx = json.load(open("search-index.json", encoding="utf-8"))
for e in idx:
    if e["u"] == "media.html":
        e["t"] = "Horizon Scanner"
        e["d"] = "A living review of new research on every test, trends in interest and funding, and the institute's news and press record."
        e["h"] = "Watching the field our tests belong to | Living Review | What the Field Is Finding | Trends | How the Field Is Moving | Press | " + e.get("h", "")
for e in idx:                                       # menu text inside every page's indexed body
    e["x"] = e.get("x", "").replace(" Media Gallery ", " Horizon Scanner Gallery ")
json.dump(idx, open("search-index.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("media.html and search index updated")
