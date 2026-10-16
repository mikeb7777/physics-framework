# -*- coding: utf-8 -*-
"""Version 6D: cover credit and file size (Michael, 16 Oct 2026: "Remove German creative ... nothing
remains of what she did. The file size is large and loads slow.").

  1. The front-matter line "Cover design by: GermanCreative" is removed. Nothing of that design remains:
     the front, back and title page are new.
  2. The PDF Word exports was about 8 MB, and 3.9 MB of it was one font: Segoe UI Emoji, a colour-emoji
     font, embedded for the single link icon (U+1F517) before "COSMIC CONNECTIONS" at the head of each of
     the 23 chapters. The icon is removed and the label kept, so the font is no longer embedded.
     The other symbols (arrows, check marks) are set in Segoe UI Symbol, which is small, and stay.
Run once:  python3 tools/book_6d_credit_and_size_2026_10_16.py
"""
import os
import docx
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "A Quest for The Big TOE Version 6D.docx")
LINK = "\U0001F517"

d = docx.Document(DOC)

credit = [p for p in d.paragraphs[:120] if p.text.strip() == "Cover design by: GermanCreative"]
assert len(credit) == 1, len(credit)
credit[0]._p.getparent().remove(credit[0]._p)

removed = 0
for p in list(d.element.body.iter(qn("w:p"))):
    runs = list(p.iter(qn("w:r")))
    for i, r in enumerate(runs):
        texts = list(r.iter(qn("w:t")))
        if "".join(t.text or "" for t in texts) == LINK:
            r.getparent().remove(r)
            removed += 1
            nxt = runs[i + 1] if i + 1 < len(runs) else None          # " COSMIC CONNECTIONS:" loses its leading space
            if nxt is not None:
                t = nxt.find(qn("w:t"))
                if t is not None and t.text and t.text.startswith(" "):
                    t.text = t.text[1:]
assert removed == 23, removed
assert LINK not in d.element.xml

# leftover references to the emoji font on empty runs and paragraph marks would still make Word embed it
cleared = 0
for rf in list(d.element.body.iter(qn("w:rFonts"))):
    if "Segoe UI Emoji" in rf.attrib.values():
        r = rf.getparent().getparent()
        assert not "".join(t.text or "" for t in r.iter(qn("w:t"))), "emoji font on a run with text"
        rf.getparent().remove(rf)
        cleared += 1
d.save(DOC)
print("emoji-font references cleared:", cleared)
print("credit removed; link icons removed:", removed)
