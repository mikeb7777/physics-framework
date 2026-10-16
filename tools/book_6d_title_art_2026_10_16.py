# -*- coding: utf-8 -*-
"""Version 6D, title page art (Michael, 16 Oct 2026: "replace with B's art").

The footprint picture behind the title on page 2 is replaced with cover direction B's footprint
(point, circle, disc, shaded disc, sphere for the toes; a field of stars for the sole), redrawn in dark
ink for the white page: cover/title-footprint.png, transparent, 5.55 x 5.39 in at 300 DPI, the same
size and place as the old picture so nothing on the page moves.
Run once:  python3 tools/book_6d_title_art_2026_10_16.py
"""
import os
import docx
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "A Quest for The Big TOE Version 6D.docx")
ART = os.path.join(ROOT, "cover", "title-footprint.png")

d = docx.Document(DOC)
hits = []
for a in d.element.body.iter(qn("wp:anchor")):
    blip = a.find(".//" + qn("a:blip"))
    if blip is None:
        continue
    part = d.part.related_parts[blip.get(qn("r:embed"))]
    if str(part.partname).endswith("/image2.png"):
        hits.append(part)
assert len(hits) == 1, len(hits)
hits[0]._blob = open(ART, "rb").read()
d.save(DOC)
print("title art replaced")
