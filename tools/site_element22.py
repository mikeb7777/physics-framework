# -*- coding: utf-8 -*-
"""Site updates for the 30 September 2026 6C (Element 22 and the corrections):
contents list, element counts, and the 6C changelog on the download page."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITS = {
    "book.html": [
        ('<li><span class="num">21</span>Quantum Error Correction: Information Preservation in Practice</li>',
         '<li><span class="num">21</span>Quantum Error Correction: Information Preservation in Practice</li>\n'
         '            <li><span class="num">22</span>The Chromatic Ledger: Energy in Color</li>'),
        ('<h2 class="section-title" data-aos="fade-up" data-aos-delay="100">Twenty-One Elements</h2>',
         '<h2 class="section-title" data-aos="fade-up" data-aos-delay="100">Twenty-Two Elements</h2>'),
        ("An introduction, twenty-one elements that each follow one idea", "An introduction, twenty-two elements that each follow one idea"),
    ],
    "framework.html": [("The 21 elements below set out the argument in full.", "The 22 elements below set out the argument in full.")],
    "media.html": [("21 elements covering information, gravity, consciousness, and spacetime.", "22 elements covering information, gravity, consciousness, and spacetime.")],
    "download.html": [
        ("It presents the COSMIC Framework in full: 21 Elements covering", "It presents the COSMIC Framework in full: 22 Elements covering"),
        ("""                    <li>Added for print: a note that the printed text is a snapshot""",
         """                    <li>New: Element 22, The Chromatic Ledger, Energy in Color, placed after Element 21 so that no Element is renumbered. It shows how an additive, conserved quantity such as energy can be read as color, where the method stops working, and why information itself cannot be one of its channels</li>
                    <li>Conservation of information stated precisely: closed quantum systems conserve it; whether the universe as a whole does is an open question; the black hole information paradox is described as unresolved, with preservation the leading theoretical view and no experiment yet</li>
                    <li>The Willow result is no longer described as appearing &ldquo;four months after the prediction was documented&rdquo;; it is consistent with the framework, and standard quantum error correction theory predicts it too</li>
                    <li>Conclusion: ALMA&rsquo;s hot intracluster gas in SPT2349-56 (Nature, January 2026) added as the fourth published result consistent with the framework; &ldquo;one corroborating observation in progress&rdquo; removed</li>
                    <li>Added for print: a note that the printed text is a snapshot"""),
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
