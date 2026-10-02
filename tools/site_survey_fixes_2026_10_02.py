# -*- coding: utf-8 -*-
"""Site survey fixes (2 Oct 2026). Michael: survey the site for outliers in text, font,
color and format, and make sure every link works. Run once.

Links: one dead internal link; six DOIs that are not registered (doi.org returns 404) and
three moved pages, each replaced with a checked target; a dead placeholder-image service.
Text: an out-of-date sentence (the NSF 15% cap was vacated in June 2025), a British
spelling, two em dashes, one 'failure' in our own copy.
Fonts: one post loaded DM Sans / DM Mono / Crimson Pro; one led with Segoe UI.
Colors: template defaults (Bootstrap / Flat UI purples, greens, reds) mapped to the palette;
one off-registry QCD pair corrected.
Format: three titles that broke the 'Page | Ic² Research Institute' pattern; two missing
meta descriptions."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def edit(f, pairs, count_ok=lambda n: n >= 1):
    s = open(f, encoding="utf-8").read()
    for a, b in pairs:
        n = s.count(a)
        if n == 0 and b in s:      # already applied on an earlier run
            continue
        assert count_ok(n), (f, n, a[:70])
        s = s.replace(a, b)
    open(f, "w", encoding="utf-8").write(s)


# ---- links
edit("media.html", [('<a href="contact.html" class="news-card-link">', '<a href="about-page.html#contact" class="news-card-link">')])
edit("tools/media_field_watch.py", [('<a href="contact.html" class="news-card-link">', '<a href="about-page.html#contact" class="news-card-link">')])
edit("references.html", [
    ("https://doi.org/10.1007/s11229-006-9100-9", "https://doi.org/10.1007/s10701-007-9186-9"),          # Tegmark 2008, Found. Phys.
    ("https://doi.org/10.1147/rd.171.0525", "https://doi.org/10.1147/rd.176.0525"),                      # Bennett 1973, IBM J. Res. Dev. 17(6)
    ("https://doi.org/10.1016/S0896-6273(03)00824-4", "https://doi.org/10.1016/S0010-0277(00)00123-2"),  # Dehaene & Naccache 2001, Cognition
    ("https://doi.org/10.1093/jcs/2.3.200", "https://consc.net/papers/facing.html"),                     # Chalmers 1995: JCS has no DOI
    ("https://press.princeton.edu/books/paperback/9780691130262/galactic-dynamics", "https://press.princeton.edu/books/paperback/9780691130279/galactic-dynamics"),
])
# Wheeler 1989 (proceedings, no DOI): keep the citation, drop the link to an unregistered DOI
s = open("references.html", encoding="utf-8").read()
s, n = re.subn(r'\s*<a href="https://doi\.org/10\.1007/978-94-011-3530-2_3"[^>]*>.*?</a>', "", s, flags=re.S)
assert n <= 1, n
open("references.html", "w", encoding="utf-8").write(s)
edit("appendix.html", [
    ("https://doi.org/10.1007/s11229-006-9100-9", "https://doi.org/10.1007/BF02084158"),   # entropy and computation: Bennett 1982
    ("https://doi.org/10.1007/978-3-030-11927-3", "https://doi.org/10.1007/978-3-030-11298-1"),  # Li & Vitanyi, Kolmogorov complexity, 4th ed.
])
edit("glossary.html", [("https://plato.stanford.edu/entries/spacetime-beingbecoming/", "https://plato.stanford.edu/entries/spacetime-bebecome/")])
# members: the placeholder image service is gone; use the institute's own mark
s = open("members.html", encoding="utf-8").read()
s, n = re.subn(r'src="https://via\.placeholder\.com/[^"]*"', 'src="spinner-centered.png"', s)
open("members.html", "w", encoding="utf-8").write(s)

# ---- text
edit("quest-map.html", [
    ("In May 2025 the NSF capped its rate at 15 percent for universities, which tells you how much was riding on that number.",
     "In May 2025 the NSF capped its rate at 15 percent for universities; a federal court struck the cap down that June. The attempt shows how much was riding on that number."),
    ("https://www.nsf.gov/policies/document/indirect-cost-rate", "https://www.forbes.com/sites/michaeltnietzel/2025/06/22/judge-sides-with-universities-blocks-nsfs-15--indirect-cost-cap/"),
    ("NSF 15% indirect cost policy", "NSF 15% cap, vacated June 2025"),
    ("database licence", "database license"),
])
edit("quest-guide.html", [("Revise and resubmit is the normal path, not a failure of it.", "Revise and resubmit is the normal path, not a detour from it.")])
s = open("blog.html", encoding="utf-8").read()
vis_dash = re.findall(r"[^<>\n]{0,40} — [^<>\n]{0,40}", s)
s = s.replace(" &mdash; which is why", ", which is why").replace(" — which is why", ", which is why")
s = re.sub(r"(?<=[a-z]) — (?=[a-z])", ", ", s)
open("blog.html", "w", encoding="utf-8").write(s)

# ---- fonts
s = open("blog-post-institution-and-the-idea.html", encoding="utf-8").read()
s = re.sub(r"family=Crimson\+Pro[^&\"']*", "family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700", s)
s = re.sub(r"family=DM\+Sans[^&\"']*", "family=IBM+Plex+Sans:wght@400;500;600;700", s)
s = re.sub(r"family=DM\+Mono[^&\"']*", "family=IBM+Plex+Mono:wght@400;500", s)
s = s.replace("'Crimson Pro'", "'Source Serif 4'").replace("\"Crimson Pro\"", "'Source Serif 4'")
s = s.replace("'DM Sans'", "'IBM Plex Sans'").replace("\"DM Sans\"", "'IBM Plex Sans'")
s = s.replace("'DM Mono'", "'IBM Plex Mono'").replace("\"DM Mono\"", "'IBM Plex Mono'")
assert "DM Sans" not in s and "Crimson Pro" not in s and "DM Mono" not in s
open("blog-post-institution-and-the-idea.html", "w", encoding="utf-8").write(s)
s = open("blog-post-isolation-may-be-required.html", encoding="utf-8").read()
s = re.sub(r"font-family:\s*'Segoe UI'", "font-family: 'IBM Plex Sans', 'Segoe UI'", s)
open("blog-post-isolation-may-be-required.html", "w", encoding="utf-8").write(s)

# ---- colors: template defaults to the palette
CMAP = {"#667eea": "#005ba5", "#764ba2": "#1a1d33", "#3498db": "#005ba5", "#2ecc71": "#2e7d32", "#27ae60": "#2e7d32",
        "#1e8449": "#1a5c2a", "#95a5a6": "#8fa0b0", "#7f8c8d": "#5a6878", "#e74c3c": "#c62828", "#c0392b": "#8B0000",
        "#f39c12": "#7a5000", "#28a745": "#2e7d32", "#ff4444": "#e53935", "#ff6b6b": "#e53935", "#a9dfbf": "#8fa0b0",
        "#f0f9f4": "#f8f9fa", "#ff8c00": "#7a5000"}
changed = {}
for f in ("blog.html", "blog-prime-numbers.html", "unsubscribe.html", "simulations.html", "members.html", "research-publications.html"):
    s = open(f, encoding="utf-8").read(); t = s
    for a, b in CMAP.items():
        t = re.sub(re.escape(a) + r"\b", b, t, flags=re.I)
    if t != s:
        changed[f] = sum(len(re.findall(re.escape(a) + r"\b", s, re.I)) for a in CMAP); open(f, "w", encoding="utf-8").write(t)
edit("framework.html", [('style="background: #ad1457; border-left: 4px solid #2e7d32;', 'style="background: #8e0c45; border-left: 4px solid #1a7a36;')])

# ---- format
edit("blog-prime-numbers.html", [("| Ic² Research</title>", "| Ic² Research Institute</title>")])
edit("instruments.html", [("<title>The Instruments | The Quest</title>", "<title>The Instruments | The Quest | Ic² Research Institute</title>")])
edit("testing-schedule.html", [("<title>Testing Schedule - COSMIC Framework Predictions</title>", "<title>Testing Schedule | Ic² Research Institute</title>")])
for f, d in (("search.html", "Search every page of the Ic² Research Institute site: the COSMIC Framework, its tests, results, the book and the blog."),
             ("unsubscribe.html", "Unsubscribe from The Quest, the Ic² Research Institute newsletter.")):
    s = open(f, encoding="utf-8").read()
    if 'name="description"' not in s:
        s = s.replace("</title>", f'</title>\n    <meta name="description" content="{d}">', 1); open(f, "w", encoding="utf-8").write(s)
print("colors changed:", changed)
print("em dashes found in blog:", len(vis_dash))
