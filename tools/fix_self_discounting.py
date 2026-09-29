# -*- coding: utf-8 -*-
"""Michael, 29 Sep 2026: we are building an institute the way existing ones were
built, so the site should not describe the Institute as lacking an institution."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITS = {
    "about-page.html": [(
        "An independent, community-driven research entity with no institutional affiliation and no gatekeeping. Traditional hierarchies are deliberately avoided.",
        "An independent research institute, built and run by its community. Membership is open, and the work itself is the only standard.")],
    "research-opportunities.html": [(
        "<strong>Independent:</strong> No institutional affiliation means no agenda to protect and no constraints on where the evidence leads.",
        "<strong>Independent:</strong> The Institute answers to no parent organization or funder, so no outside agenda shapes where the evidence leads.")],
}
for name, pairs in EDITS.items():
    p = os.path.join(ROOT, name)
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:40])
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", name)
