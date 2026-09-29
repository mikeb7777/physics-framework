# Adds "Guide" after "Map" in the Quest menu on the Quest pages, and a pointer
# from the Quest Map's lede to the Quest Guide. Safe to rerun.
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for name in ("quest-map.html", "quest-follow.html", "instruments.html"):
    p = os.path.join(ROOT, name)
    t = open(p, encoding="utf-8").read()
    if 'href="quest-guide.html">Guide<' not in t:
        t, n = re.subn(r'(<li><a href="quest-map.html"( aria-current="page")?>Map</a></li>)',
                       r'\1\n            <li><a href="quest-guide.html">Guide</a></li>', t, count=1)
        assert n == 1, name
    if name == "quest-map.html" and "quest-guide.html\">Quest Guide" not in t:
        t, n = re.subn(r"(and links to the sources\.)", r'\1 For every gate in detail, with the way through and where to go, see the <a href="quest-guide.html">Quest Guide</a>.', t, count=1)
        assert n == 1
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", name)
