# -*- coding: utf-8 -*-
"""Undo the Element 22 site changes (tools/site_element22.py) after Michael
folded the material into Element 5 (30 Sep 2026). The book stays at 21
Elements; the 6C changelog records the Element 5 passage instead."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITS = {
    "book.html": [
        ('\n            <li><span class="num">22</span>The Chromatic Ledger: Energy in Color</li>', ""),
        ('data-aos-delay="100">Twenty-Two Elements</h2>', 'data-aos-delay="100">Twenty-One Elements</h2>'),
        ("An introduction, twenty-two elements that each follow one idea", "An introduction, twenty-one elements that each follow one idea"),
    ],
    "framework.html": [("The 22 elements below set out the argument in full.", "The 21 elements below set out the argument in full.")],
    "media.html": [("22 elements covering information, gravity, consciousness, and spacetime.", "21 elements covering information, gravity, consciousness, and spacetime.")],
    "download.html": [
        ("It presents the COSMIC Framework in full: 22 Elements covering", "It presents the COSMIC Framework in full: 21 Elements covering"),
        ("<li>New: Element 22, The Chromatic Ledger, Energy in Color, placed after Element 21 so that no Element is renumbered. It shows how an additive, conserved quantity such as energy can be read as color, where the method stops working, and why information itself cannot be one of its channels</li>",
         "<li>Element 5: a new passage, &ldquo;Why It Is Called Color&rdquo;, on why quark charge is named color, how color works as a ledger for conserved quantities, and why information, which is conserved but not additive, cannot be one of its columns</li>"),
    ],
}
for name, pairs in EDITS.items():
    p = os.path.join(ROOT, name)
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:60], t.count(old))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", name)
