# -*- coding: utf-8 -*-
"""Recolor the four consciousness program pages to the site palette (Michael, 4 Oct 2026: "let's use our
navy, gray, red, QCD colors"). Navy #1a1d33 for heroes and dark bands, flat grays #4a5868/#5a6878, brand
red #8B0000 (hover #6b0000), and one QCD pair per program as its accent:
  NBI                    B+Yw  #005ba5 / #f1e303
  Consciousness Tuning   Mg+G  #8e0c45 / #1a7a36
  Cognitive Extension    Cy+R  #005f6e / #c62828  (overview and pilot)
Invented gradients become flat fills. The cork pin board (browns) is a deliberate motif and stays.
Run once."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCENT = {
    "program-nbi.html": ("#005ba5", "0,91,165"),
    "program-consciousness-tuning.html": ("#8e0c45", "142,12,69"),
    "program-cognitive-extension-overview.html": ("#005f6e", "0,95,110"),
    "program-cognitive-extension-pilot.html": ("#005f6e", "0,95,110"),
}
GRADIENTS = [
    ("linear-gradient(135deg, #0a2a4e 0%, #0e5fa8 60%, #1a7ad4 100%)", "#1a1d33"),
    ("linear-gradient(135deg, #1a1d33 0%, #8e0c45 60%, #8e0c45 100%)", "#1a1d33"),
    ("linear-gradient(135deg, #0a1a2e 0%, #1a3a5c 60%, #1a3a5c 100%)", "#1a1d33"),
    ("linear-gradient(135deg, #0a2a4e 0%, #0e5fa8 100%)", "#1a1d33"),
    ("linear-gradient(135deg, #0a1a2e 0%, #1a3a5c 100%)", "#1a1d33"),
    ("linear-gradient(135deg, #1a1d33 0%, #8e0c45 100%)", "#1a1d33"),
    ("linear-gradient(135deg, #0e5fa8 0%, #003d73 100%)", "#005ba5"),
    ("linear-gradient(135deg, #1a5c2a 0%, #0d3317 100%)", "#1a5c2a"),
    ("linear-gradient(135deg, #8B0000 0%, #5a0000 100%)", "#8B0000"),
    ("linear-gradient(135deg, #8e0c45 0%, #1a1d33 100%)", "#8e0c45"),
]
HEX = [  # off-palette -> palette
    ("#0e5fa8", "#005ba5"), ("#0a4580", "#1a1d33"), ("#1a7ad4", "#1565c0"), ("#004080", "#1a1d33"),
    ("#0a2a4e", "#1a1d33"), ("#0a1a2e", "#1a1d33"), ("#0d1b2e", "#1a1d33"), ("#102035", "#1a1d33"),
    ("#1a1a2e", "#1a1d33"), ("#2c3e50", "#1a1d33"), ("#2d3f52", "#4a5868"),
    ("#cc2200", "#c62828"), ("#a00000", "#6b0000"), ("#7a4f00", "#7a5000"),
    ("#f9a825", "#f1e303"), ("#e65100", "#7a5000"), ("#1a4a2e", "#1a5c2a"), ("#4fc3f7", "#00bcd4"),
    ("#444", "#4a5868"), ("#555", "#4a5868"), ("#666", "#5a6878"),
    ("#e33d2f", "#c62828"), ("#a1cd5f", "#2e7d32"), ("#f58b2b", "#7a5000"),
]

for name, (acc, rgb) in ACCENT.items():
    path = os.path.join(ROOT, name)
    s = open(path, encoding="utf-8").read()
    # the hero: navy with the program's accent as a rule and a soft glow
    m = re.search(r"(\.page-header \{\s*background: )([^;]+);", s)
    assert m, name
    s = s[:m.start(2)] + f"#1a1d33;\n    border-bottom: 6px solid {acc}" + s[m.end(2):]
    s = s.replace("rgba(26,122,212,0.3)", f"rgba({rgb},0.45)")
    s = s.replace("rgba(14,95,168,", f"rgba({rgb},").replace("rgba(0,91,165,", f"rgba({rgb},")
    if name == "program-cognitive-extension-overview.html":
        s = s.replace("--accent-blue", "--accent-program")
        s = s.replace("--accent-program: #005ba5;", f"--accent-program: {acc};")
        s = s.replace("linear-gradient(135deg, var(--accent-program) 0%, #004080 100%)", "var(--accent-program)")
    if name == "program-cognitive-extension-pilot.html":
        s = s.replace("#1a3a5c", acc)
    else:
        s = s.replace("border: 2px solid #1a3a5c;", f"border: 2px solid {acc};")
    for a, b in GRADIENTS:
        s = s.replace(a, b)
    for a, b in HEX:
        s = re.sub(re.escape(a) + r"(?![0-9a-fA-F])", b, s, flags=re.I)
    left = sorted(set(re.findall(r"linear-gradient\(135deg[^;\"]*", s)))
    print(name, "remaining 135deg gradients:", left)
    open(path, "w", encoding="utf-8").write(s)
print("done")
