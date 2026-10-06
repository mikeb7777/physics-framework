# -*- coding: utf-8 -*-
"""Version 6D release on download.html (6 Oct 2026; Michael: "Yes, change everything to 6D"). Copies the 6D files
from Book-Drafts, points both download buttons to 6D, adds a Version 6D entry with its change list above 6C,
and moves the "Latest" badge. 6C stays listed and downloadable as an archived version. Run once."""
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(os.path.dirname(ROOT), "Book-Drafts")
for ext in ("docx", "pdf"):
    shutil.copy2(os.path.join(BOOK, f"A Quest for The Big TOE Version 6D.{ext}"), os.path.join(ROOT, f"A Quest for The Big TOE Version 6D.{ext}"))

P = os.path.join(ROOT, "download.html")
s = open(P, encoding="utf-8").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('<a href="A%20Quest%20for%20The%20Big%20TOE%20Version%206C.pdf" class="btn-pill" style="font-size: 1.2rem; padding: 1rem 3rem;" download>Download Now: Version 6C</a>',
    '<a href="A%20Quest%20for%20The%20Big%20TOE%20Version%206D.pdf" class="btn-pill" style="font-size: 1.2rem; padding: 1rem 3rem;" download>Download Now: Version 6D</a>')

# the old Latest badge on 6C becomes a published date
m = re.search(r'<h3>Version 6C <span style="display:inline-block;background:#f1e303;[^"]*" class="blink">[^<]*</span>', s)
assert m
badge = s[m.start() + len("<h3>Version 6C "):m.end()]
s = s[:m.start()] + '<h3>Version 6C <span style="font-weight:400;font-size:0.82rem;opacity:0.7;margin-left:0.5rem;">Published: 30 September 2026</span>' + s[m.end():]

ENTRY = '''<div class="foundation-accordion" style="--acc-color:#1a5c2a; --acc-stroke:#b01558; border-left:4px solid #b01558;">
          <div class="foundation-header" onclick="this.parentElement.classList.toggle('active')">
            <h3>Version 6D ''' + badge + '''</h3>
            <span class="toggle-indicator">&#9660;</span>
          </div>
          <div class="fa-content">
            <div class="fa-inner">
              <p style="color:#2c3e50;line-height:1.8;margin-bottom:1rem;">Correction edition, 6 October 2026. Every claim about the brain and the cosmic web checked against the published paper, one figure redrawn, and the remaining parked corrections applied. This is the current text; the print edition is formatted from it.</p>
              <div class="changelog">
                <h4>Changes in Version 6D</h4>
                <ul>
                    <li>Element 7: the brain and cosmic web comparison now describes what Vazza and Feletti (2020) actually measured, the power spectrum and network statistics of both networks. The earlier account of machine-learning classifiers performing at 50% chance, and a &ldquo;spectral dimension&rdquo; figure, are removed; neither is in the paper. The tissue is identified correctly as human, under light microscopy, and the paper&rsquo;s own limit is stated: connections were defined by proximity, not synapses</li>
                    <li>Element 7: Figure 7-2 redrawn. Dark matter is about 85% of all matter; glial cells and neurons are about equal in number. The earlier figure showed 85/15 for both</li>
                    <li>Element 5: the matter excess is attributed to CP violation, not parity violation alone, with the measured amount noted as too small; the link to the first-instant asymmetry is posed as a question</li>
                    <li>Element 12: the anthropic principle, the multiverse and the Past Hypothesis are named and answered before the framework&rsquo;s account of the low-entropy start</li>
                    <li>Element 17: the last legacy &ldquo;25-million-to-one&rdquo; ratio corrected to 100 million to one; the duplicate pinwheel figure removed in favor of Figure 3-3</li>
                    <li>Element 19: Hawking radiation described consistently with the Page curve: each particle looks thermal, while the information returns in correlations across the radiation</li>
                    <li>Figure 16-1: caption corrected; the molecules come from structural data, and the artist arranged the scene</li>
                </ul>
              </div>
              <div class="btn-container" style="margin-top:1.25rem;">
                <a href="A%20Quest%20for%20The%20Big%20TOE%20Version%206D.pdf" class="btn-pill" download>Download PDF</a>
              </div>
            </div>
          </div>
        </div>

        '''
anchor = '<div class="foundation-accordion" style="--acc-color:#8B0000; --acc-stroke:#00838f; border-left:4px solid #00838f;">\n          <div class="foundation-header" onclick="this.parentElement.classList.toggle(\'active\')">\n            <h3>Version 6C'
rep(anchor, ENTRY + anchor)
open(P, "w", encoding="utf-8").write(s)
print("ok")
