# -*- coding: utf-8 -*-
"""references.html (6 Oct 2026): parked book change 2 and a citation fix.
- Zheng & Meister: the journal record is Neuron 113(2), 192-204, 22 January 2025 (online December 2024),
  checked at the DOI. The page said "124(8)". Year kept as the online date the book uses, with the issue added.
- Element 17 (Vision as Reality Construction), reference [2] now cites Zheng & Meister as the source of the
  10 bits per second figure, with Norretranders kept as background (BigTOE_Parked_Changes, change 2).
Run once."""
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references.html")
s = open(P, encoding="utf-8").read()
old = "<em>Neuron</em>, 124(8)."
assert s.count(old) == 3, s.count(old)
s = s.replace(old, "<em>Neuron</em>, 113(2), 192&ndash;204 (issue of 22 January 2025; published online December 2024).")
a = ('<p><strong>[2]</strong> N&oslash;rretranders, T. (1998). <em>The User Illusion: Cutting Consciousness Down to Size</em>. Viking Press. '
     '[Broader context for sensory compression argument. The 40 bits/second figure has been updated to 10 bits/second by Zheng &amp; Meister (2024).]')
assert s.count(a) == 1
s = s.replace(a, '<p><strong>[2]</strong> Zheng, J., &amp; Meister, M. (2024). &quot;The unbearable slowness of being: Why do we live at 10 bits/s?&quot; '
                 '<em>Neuron</em>, 113(2), 192&ndash;204. <a href="https://doi.org/10.1016/j.neuron.2024.11.008" target="_blank" rel="noopener">doi.org/10.1016/j.neuron.2024.11.008</a> '
                 '[Source of the 10 bits per second figure. Background: N&oslash;rretranders, T. (1998), <em>The User Illusion</em>, Viking Press, which gave the older 40 bits per second estimate.]')
open(P, "w", encoding="utf-8").write(s)
print("ok")
