# Cache-bust apple-touch-icon.png after the recolor (it had the old yellow Spinner).
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 0
for p in glob.glob(os.path.join(ROOT, "*.html")):
    t = open(p, encoding="utf-8").read()
    u = t.replace('apple-touch-icon.png"', 'apple-touch-icon.png?v=rgb"')
    if u != t:
        open(p, "w", encoding="utf-8", newline="").write(u); n += 1
print(n, "pages")
