# -*- coding: utf-8 -*-
"""Simulations page -> Visualizations page, sitewide links (6 Oct 2026). Every link to simulations.html
points to visualizations.html, and its text "Simulations" becomes "Visualizations" (the page is the same;
simulation is one kind of visual on it). simulations.html stays as a redirect that keeps the #anchor.
Also the sitemap, the search index, and the rerunnable footer and thumbnail tools. Run once."""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
total = 0
for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))) + [os.path.join(ROOT, "tools", n) for n in ("unify_footer.py", "record_sim_thumbs.py")]:
    if os.path.basename(path) == "simulations.html":
        continue
    s = open(path, encoding="utf-8").read(); s0 = s
    s = re.sub(r'(href="[^"]*?)simulations\.html', r"\1visualizations.html", s)
    s = re.sub(r'(<a [^>]*href="[^"]*visualizations\.html[^"]*"[^>]*>)Simulations(</a>)', r"\1Visualizations\2", s)
    s = s.replace("Explore the chamber model on the Simulations page", "Explore the chamber model on the Visualizations page")
    s = s.replace("simulations.html", "visualizations.html") if path.endswith(".py") else s
    if s != s0:
        open(path, "w", encoding="utf-8").write(s); total += 1
print("files changed:", total)

p = os.path.join(ROOT, "sitemap.xml")
s = open(p, encoding="utf-8").read()
assert s.count("https://eequalsicsquared.com/simulations.html</loc><lastmod>2026-09-13</lastmod>") == 1
s = s.replace("https://eequalsicsquared.com/simulations.html</loc><lastmod>2026-09-13</lastmod>",
              "https://eequalsicsquared.com/visualizations.html</loc><lastmod>2026-10-06</lastmod>")
open(p, "w", encoding="utf-8").write(s)

p = os.path.join(ROOT, "search-index.json")
idx = json.load(open(p, encoding="utf-8"))
n = 0
for e in idx:
    if e.get("u", "").startswith("simulations.html"):
        e["u"] = e["u"].replace("simulations.html", "visualizations.html"); n += 1
        if e.get("t") == "Simulations":
            e["t"] = "Visualizations"
        e["d"] = "Maps, simulations, models, concepts and renderings of the COSMIC Framework and the physics behind it, each labeled by what kind of picture it is."
json.dump(idx, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("search entries:", n)
