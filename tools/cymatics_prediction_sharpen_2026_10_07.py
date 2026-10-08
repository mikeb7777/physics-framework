# -*- coding: utf-8 -*-
"""Sharpen the COSMIC Framework prediction on program-cymatics.html (Michael, 7 Oct 2026: "Sharpen it to what
we know now but we can change it during preliminary testing"). The February 2026 wording ("will match
theoretical predictions for electromagnetic field node geometry ... High confidence") named no geometry and
no measure. Sound in a rigid sphere and electromagnetic waves in a conducting sphere obey the same wave
equation (Helmholtz), so they share angular structure (spherical harmonics) but differ in boundary conditions.
The sharpened version states what is measured, the tolerances, and what a match would and would not show,
under the evidence standard. Run once."""
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "program-cymatics.html")
s = open(P, encoding="utf-8").read()

OLD_LI = """            <ul>
                <li>The three-dimensional node structures will match theoretical predictions for electromagnetic field node geometry in three-dimensional space, providing physical demonstration that complex geometric patterns arise naturally from field dynamics without external design</li>
            </ul>"""
NEW_LI = """            <p style="color: var(--text-dark); margin-bottom: 0.5rem; font-size: 0.9rem;"><strong>Sharpened 7 October 2026.</strong> The February wording said the patterns would match &ldquo;electromagnetic field node geometry&rdquo; without saying which geometry or how a match would be measured. Sound in a rigid sphere and electromagnetic waves in a conducting sphere obey the same wave equation, so the claim can be stated exactly:</p>
            <ul>
                <li><strong>Shared angular pattern.</strong> At each resonance the chamber model identifies, the angular positions of the particle clusters follow the same spherical harmonic pattern (the same l and m, combined as the model gives for the tetrahedral drive) that labels the electromagnetic cavity mode with those numbers. Tolerance: 10 degrees for each cluster, within the camera system&rsquo;s tracking accuracy.</li>
                <li><strong>Different boundary, different spacing.</strong> Shell radii and the ratios between resonant frequencies follow the acoustic condition for a rigid wall, not the electromagnetic conditions for a conducting wall. Example: the first three radially symmetric modes stand in the ratio 1 : 1.719 : 2.427. Tolerance: frequency ratios within 2 percent, shell radii within 5 percent of the chamber radius.</li>
                <li><strong>What a match would show, and what it would not.</strong> Both statements also follow from standard wave physics. A match would show directly that one wave equation sets the geometry in both kinds of field. It would not, by itself, count as evidence for the COSMIC Framework. That needs a prediction standard physics does not make, and none is registered for this experiment yet.</li>
            </ul>
            <p style="margin-top: 0.5rem; font-size: 0.85rem; color: #5a6878;">Status: preliminary. The tolerances may be revised during Phase 1 ground testing, once the tracking accuracy is measured, and will be fixed before the predictions are registered.</p>"""
assert s.count(OLD_LI) == 1
s = s.replace(OLD_LI, NEW_LI)

OLD_CONF = 'Prediction confidence: High &nbsp;|&nbsp; Physical basis: Acoustic field theory, nodal surface geometry &nbsp;|&nbsp;'
NEW_CONF = 'Confidence that it holds: high (standard wave physics) &nbsp;|&nbsp; Weight as evidence for the framework: none on its own &nbsp;|&nbsp; Physical basis: the Helmholtz wave equation in a sphere &nbsp;|&nbsp;'
assert s.count(OLD_CONF) == 1
s = s.replace(OLD_CONF, NEW_CONF)

OLD_INTRO = "It represents the COSMIC Framework&rsquo;s interpretation of what the physics results would mean for the NBI hypothesis if confirmed."
NEW_INTRO = "It records how the COSMIC Framework reads the physics results."
assert s.count(OLD_INTRO) == 1
s = s.replace(OLD_INTRO, NEW_INTRO)

open(P, "w", encoding="utf-8").write(s)
print("ok")
