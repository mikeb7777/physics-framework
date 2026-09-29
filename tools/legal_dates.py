# Date stamps for the 29 Sep 2026 wording change (tools/institute_wording.py).
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for name, old, new in (
    ("legal.html", '<h2>Community Forum &amp; Collaboration</h2><span class="last-updated">Last Updated: March 2026</span>',
     '<h2>Community Forum &amp; Collaboration</h2><span class="last-updated">Last Updated: September 2026</span>'),
    ("privacy-policy.html", "<strong>Last Updated:</strong> March 1, 2026", "<strong>Last Updated:</strong> September 29, 2026"),
):
    p = os.path.join(ROOT, name)
    t = open(p, encoding="utf-8").read()
    assert t.count(old) == 1, name
    open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new))
    print("ok", name)
