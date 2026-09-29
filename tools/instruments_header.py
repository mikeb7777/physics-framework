# -*- coding: utf-8 -*-
# Instruments page: the Quest header (tools/quest_header.py) replaces the old
# centered hero and its "not an argument against science" thesis line.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quest_header import head_section, CSS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "instruments.html")
t = open(p, encoding="utf-8").read()
new = head_section(
    "<strong>The Instruments</strong> that will decide every prediction the Institute has registered: machines designed, funded and built by others, whose data is released to anyone who asks.",
    "These are those machines, what each one measures, and which of the Institute&rsquo;s tests it will settle.")
t, k = re.subn(r'<section class="q-hero">.*?</section>', new, t, count=1, flags=re.S)
assert k == 1
if 'id="q-head"' not in t:
    t = t.replace("</head>", CSS + "</head>", 1)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok instruments.html")
