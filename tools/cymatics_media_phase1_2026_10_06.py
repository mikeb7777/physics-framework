# -*- coding: utf-8 -*-
"""Cymatics program page: Phase 1 also compares media (Michael, 6 Oct 2026: not new enough for its own
experiment, so it joins CYM-002 Phase 1). Same chamber in brine, water-glycerol and with gas bubbles, as a
ground test of the chamber model before any flight. Run once."""
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "program-cymatics.html")
s = open(P, encoding="utf-8").read()
a = "so they follow the acoustic force on the ground and let Phase 1 test the shell predictions before any flight.</p>"
assert s.count(a) == 1
s = s.replace(a, a + """
                <p>Phase 1 also runs the same chamber in more than one medium: brine, water and glycerol mixtures, and water with small gas bubbles, which gather where the beads do not. The chamber model predicts how each medium shifts the pattern, so the comparison tests the model, and separates what belongs to the chamber's geometry from what belongs to the medium, before any flight.</p>""")
open(P, "w", encoding="utf-8").write(s)
print("ok")
