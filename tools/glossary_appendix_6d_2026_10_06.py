# -*- coding: utf-8 -*-
"""Glossary, appendix and references, matched to Book Version 6D (6 Oct 2026; Michael: "check to see if an
update is needed for the references, appendix, and glossary").
- Glossary: new terms CP Violation and Parity Violation (6D's Element 5 now distinguishes them).
- Appendix: the information paradox paragraph says the radiation appeared thermal in Hawking's original
  calculation, and points to the Page curve result, matching Element 19 in 6D.
- References: Muir & Bhatt (2025), "Universal pinwheel density ... meta-analysis", Nature Neuroscience 28,
  412-421, removed. No such paper exists in Crossref or the journal (checked 6 Oct 2026), and the book does
  not cite it. Kaschube et al. (2010) remains the source for pinwheel density.
Run once."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def edit(name, pairs):
    p = os.path.join(ROOT, name); s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:60], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)


CP = '''    <div class="term-entry">
    <div class="term-name">CP Violation</div>
    <div class="term-definition">A difference in how the weak force treats matter and antimatter: a process and its mirror image with every particle swapped for its antiparticle do not behave identically. CP violation is one of the three conditions (Sakharov, 1967) the universe needs to end up with more matter than antimatter. It has been measured in kaons and B mesons, but the amount is far too small to explain the matter we see, so the origin of the excess is still open. See also: Parity Violation, Weak Force.</div>
    </div>
    <div class="term-entry">
    <div class="term-name">Cross-Frequency Validation</div>'''
PARITY = '''    <div class="term-entry">
    <div class="term-name">Parity Violation</div>
    <div class="term-definition">The weak force's distinction between left and right: a weak interaction viewed in a mirror does not behave like the original. Discovered in 1956 and 1957 (Lee, Yang and Wu). Parity violation alone does not separate matter from antimatter; that takes CP violation. See also: CP Violation, Weak Force.</div>
    </div>
    <div class="term-entry">
    <div class="term-name">Past Hypothesis</div>'''
edit("glossary.html", [
    ('    <div class="term-entry">\n    <div class="term-name">Cross-Frequency Validation</div>', CP),
    ('    <div class="term-entry">\n    <div class="term-name">Past Hypothesis</div>', PARITY),
])

edit("appendix.html", [
    ("Hawking radiation appears thermal, carrying no information about the black hole's contents.",
     "In Hawking's original calculation the radiation appears thermal, carrying no information about the black hole's contents. Since 2019 the Page curve calculations (Penington; Almheiri et al.) indicate that the information does return, carried in correlations across the radiation as a whole (Element 19)."),
])

p = os.path.join(ROOT, "references.html"); s = open(p, encoding="utf-8").read()
m = re.search(r'\s*<div class="reference-item">(?:\s*<!--[^>]*-->)?\s*<p><strong>\[38\]</strong> Muir, D\. R\., &amp; Bhatt, D\. L\. \(2025\).*?</div>', s, re.S)
assert m, "Muir entry not found"
s = s[:m.start()] + s[m.end():]
open(p, "w", encoding="utf-8").write(s)
print("ok")
