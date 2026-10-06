# -*- coding: utf-8 -*-
"""Version 6E release on download.html (6 Oct 2026; Michael: "6E is fine; rewrite using new sources. You can renumber
now"). Copies the 6E files from Book-Drafts, points both download buttons to 6E, adds a Version 6E entry above 6D,
and moves the "Latest" badge. 6D stays listed. Run once."""
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(os.path.dirname(ROOT), "Book-Drafts")
for ext in ("docx", "pdf"):
    shutil.copy2(os.path.join(BOOK, f"A Quest for The Big TOE Version 6E.{ext}"), os.path.join(ROOT, f"A Quest for The Big TOE Version 6E.{ext}"))

P = os.path.join(ROOT, "download.html")
s = open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('href="A%20Quest%20for%20The%20Big%20TOE%20Version%206D.pdf" class="btn-pill" style="font-size: 1.2rem; padding: 1rem 3rem;" download>Download Now: Version 6D</a>',
    'href="A%20Quest%20for%20The%20Big%20TOE%20Version%206E.pdf" class="btn-pill" style="font-size: 1.2rem; padding: 1rem 3rem;" download>Download Now: Version 6E</a>')
m = re.search(r'<h3>Version 6D <span style="display:inline-block;background:#f1e303;[^"]*" class="blink">[^<]*</span>', s)
assert m
badge = s[m.start() + len("<h3>Version 6D "):m.end()]
s = s[:m.start()] + '<h3>Version 6D <span style="font-weight:400;font-size:0.82rem;opacity:0.7;margin-left:0.5rem;">Published: 6 October 2026</span>' + s[m.end():]

ENTRY = '''<div class="foundation-accordion" style="--acc-color:#005ba5; --acc-stroke:#f1e303; border-left:4px solid #f1e303;">
          <div class="foundation-header" onclick="this.parentElement.classList.toggle('active')">
            <h3>Version 6E ''' + badge + '''</h3>
            <span class="toggle-indicator">&#9660;</span>
          </div>
          <div class="fa-content">
            <div class="fa-inner">
              <p style="color:#2c3e50;line-height:1.8;margin-bottom:1rem;">Source edition, 6 October 2026. Every citation in the book was checked against the sentence that cites it and against the publisher&rsquo;s record while the reference list was rebuilt. This edition corrects what that check found, and each citation number now marks one claim. This is the current text; the print edition is formatted from it.</p>
              <div class="changelog">
                <h4>Changes in Version 6E</h4>
                <ul>
                    <li>Element 5: beta decay stated correctly (a down quark becomes an up quark); the W and Z bosons are about 86 to 97 times the proton&rsquo;s mass</li>
                    <li>Element 2: the mental-practice result corrected to about 22 percent (Yue and Cole, 1992); Lloyd&rsquo;s analysis in Nature named as the synthesis of the physical limits of computation; processors described as still far above the Landauer limit</li>
                    <li>Element 3: the single-bit Landauer test credited to Berkeley (nanomagnetic bits); the Bennu samples&rsquo; 14 of 20 protein amino acids stated correctly; the 2025 adversarial test of IIT and Global Workspace Theory described as challenging both</li>
                    <li>Element 7: the information content of matter stated as the Bekenstein bound, a maximum</li>
                    <li>Elements 10 and 11: what the Zenodo records contain stated accurately (the five-band paper; code for a related analysis)</li>
                    <li>Elements 15, 18 and 19: the 2025 Annals of Physics work (Neukart) described as a proposal</li>
                    <li>Element 16: water&rsquo;s proton tunneling and the disputed room-temperature coherence claim stated accurately</li>
                    <li>Element 17: the share of visual information discarded corrected to match the hundred-million-to-one ratio</li>
                    <li>Element 20: the 2019 verified-scrambling experiment correctly described (trapped ions, University of Maryland); Sekino and Susskind dated 2008</li>
                    <li>Elements 2, 6, 8, 13, 15 and 19: citation numbers renumbered so each marks one source; the references page matches</li>
                </ul>
              </div>
              <div class="btn-container" style="margin-top:1.25rem;">
                <a href="A%20Quest%20for%20The%20Big%20TOE%20Version%206E.pdf" class="btn-pill" download>Download PDF</a>
              </div>
            </div>
          </div>
        </div>

        '''
anchor = '<div class="foundation-accordion" style="--acc-color:#1a5c2a; --acc-stroke:#b01558; border-left:4px solid #b01558;">\n          <div class="foundation-header" onclick="this.parentElement.classList.toggle(\'active\')">\n            <h3>Version 6D'
rep(anchor, ENTRY + anchor)
open(P, "w", encoding="utf-8").write(s)
print("ok")
