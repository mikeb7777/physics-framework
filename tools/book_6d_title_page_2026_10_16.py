# -*- coding: utf-8 -*-
"""Version 6D, title page (Michael, 16 Oct 2026: "the second page of the .docx file is a foot image.
Let's improve that page and use your other foot").

Page 2 is redesigned to match the new cover: the title, subtitle, author and institute mark set in the
cover's type, with cover direction C's footprint (circles at every scale, the big toe a gold sphere).
It is one picture, cover/title-page.png (6 x 7.55 in at 300 DPI, white), pinned to the top of the page
behind the text, where the old footprint picture was. The old title, subtitle, author and logo paragraphs are removed;
the copyright line stays as text, moved down to sit under the picture.
Run once:  python3 tools/book_6d_title_page_2026_10_16.py
"""
import os
import docx
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.enum.text import WD_LINE_SPACING

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "A Quest for The Big TOE Version 6D.docx")
ART = os.path.join(ROOT, "cover", "title-page.png")
EMU_IN = 914400
ART_H = 7.55

d = docx.Document(DOC)
P = d.paragraphs
p0 = P[0]
assert p0.text.strip() == "A QUEST FOR", p0.text
copyright_p = next(p for p in P[:20] if p.text.startswith("Copyright"))

# the picture: swap the image, pin it to the top-left of the page, full width, behind the text
anchor = p0._p.find(".//" + qn("wp:anchor"))
blip = anchor.find(".//" + qn("a:blip"))
part = d.part.related_parts[blip.get(qn("r:embed"))]
assert str(part.partname).endswith("/image2.png"), part.partname
part._blob = open(ART, "rb").read()
for tag in ("wp:positionH", "wp:positionV"):
    pos = anchor.find(qn(tag)); pos.set("relativeFrom", "page"); pos.find(qn("wp:posOffset")).text = "0"
cx, cy = str(6 * EMU_IN), str(int(ART_H * EMU_IN))
anchor.find(qn("wp:extent")).set("cx", cx); anchor.find(qn("wp:extent")).set("cy", cy)
anchor.find(".//" + qn("a:ext")).set("cx", cx); anchor.find(".//" + qn("a:ext")).set("cy", cy)
anchor.set("behindDoc", "1")
doc_pr = anchor.find(qn("wp:docPr"))
doc_pr.set("name", "Title page")
doc_pr.set("descr", "A Quest for The Big TOE: The COSMIC Framework's Theory of Everything. Michael K. Baines. "
                    "A footprint made of circles of every size, its big toe a gold sphere.")

# paragraph 0 keeps only the picture, at minimal height
for r in list(p0.runs):
    if not r._r.findall(".//" + qn("w:drawing")):
        r._r.getparent().remove(r._r)
pf = p0.paragraph_format
pf.space_before = Pt(0); pf.space_after = Pt(0)
pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY; pf.line_spacing = Pt(1)

# the old title, subtitle, author and logo paragraphs go
nxt = p0._p.getnext()
while nxt is not copyright_p._p:
    after = nxt.getnext()
    nxt.getparent().remove(nxt)
    nxt = after

# the copyright line sits under the author line, in the picture's blank lower band (page text area ends at 8.45 in)
copyright_p.paragraph_format.space_before = Inches(7.0 - 0.65)

d.save(DOC)
print("title page rebuilt")
