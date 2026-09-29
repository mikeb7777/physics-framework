# Adds "Support" beside "Contribute" in the footer link lists only (the header
# nav is full; see the header-fits-the-container note), plus the sitemap entry.
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = '<li><a href="contribute.html">Contribute</a></li>'
NEW = OLD + '<li><a href="support.html">Support</a></li>'
n = 0
for p in glob.glob(os.path.join(ROOT, "*.html")):
    t = open(p, encoding="utf-8").read()
    m = re.search(r"<footer\b.*?</footer>", t, re.S)
    if not m or 'href="support.html">Support<' in m.group(0) or OLD not in m.group(0):
        continue
    f = m.group(0).replace(OLD, NEW, 1)
    open(p, "w", encoding="utf-8", newline="").write(t[:m.start()] + f + t[m.end():])
    n += 1
print("footers updated:", n)
sm = os.path.join(ROOT, "sitemap.xml")
t = open(sm, encoding="utf-8").read()
if "support.html" not in t:
    block = re.search(r"\s*<url>\s*<loc>https://eequalsicsquared.com/contribute.html</loc>.*?</url>", t, re.S)
    assert block, "contribute entry not found"
    t = t[:block.end()] + block.group(0).replace("contribute.html", "support.html") + t[block.end():]
    open(sm, "w", encoding="utf-8", newline="").write(t)
    print("sitemap: support.html added")
