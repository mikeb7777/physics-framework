# -*- coding: utf-8 -*-
"""Mission names and symbols follow the medal series (Ic2-Mission-Medal/build_medal_series.py,
29 Sep 2026). Copies the rebuilt marks and logos from prereg/missions (missions.json is the
source), removes the old-named files, renames every mention (Title Case, UPPER CASE, slugs)
and recolors the mission-log dots to each mission's new color. Run once."""
import glob, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), "instagram-panels-handoff", "instagram-panels", "prereg", "missions")
os.chdir(ROOT)
MAP = [  # old, new, new color (QCD registry quark shade)
    ("Midnight Phoenix", "Cerulean Phoenix", "#005ba5"),
    ("Blue Crater", "Citrine Monoceros", "#7a5000"),
    ("Amber Ara", "Citrine Telescopium", "#7a5000"),
    ("Cyan Libra", "Crimson Centaurus", "#8B0000"),
    ("Cyan Triangulum", "Crimson Draco", "#8B0000"),
    ("Cyan Corona Borealis", "Magenta Aquila", "#8e0c45"),
    ("Cyan Draco", "Magenta Sextans", "#8e0c45"),
    ("Teal Lyra", "Emerald Lupus", "#1a5c2a"),
    ("Magenta Gemini", "Aqua Delphinus", "#00838f"),
]
slug = lambda n: n.lower().replace(" ", "-")

# 1. artwork
for folder, src in (("mission-marks", "marks"), ("mission-logos", "logos")):
    for old, new, _ in MAP:
        shutil.copy2(os.path.join(SRC, src, slug(new) + ".svg"), os.path.join(folder, slug(new) + ".svg"))
        if os.path.exists(os.path.join(folder, slug(old) + ".svg")):
            subprocess.run(["git", "rm", "-q", os.path.join(folder, slug(old) + ".svg")], check=True)
    for keep in ("midnight-eridanus", "midnight-orion"):   # unchanged names, rebuilt from the same source
        shutil.copy2(os.path.join(SRC, src, keep + ".svg"), os.path.join(folder, keep + ".svg"))

# 2. every mention
files = glob.glob("*.html") + ["search-index.json", "test-loggers.js"]
total = 0
for f in files:
    s = open(f, encoding="utf-8").read(); t = s
    for old, new, _ in MAP:
        t = t.replace(old, new).replace(old.upper(), new.upper()).replace(slug(old), slug(new))
    if t != s:
        total += sum(s.count(o) + s.count(o.upper()) + s.count(slug(o)) for o, _, _ in MAP)
        open(f, "w", encoding="utf-8").write(t)
print("mentions renamed:", total)

# 3. mission-log dots take each mission's new color
f = "mission-log.html"; s = open(f, encoding="utf-8").read()
for _, new, hx in MAP:
    s = re.sub(r'(data-mission="' + re.escape(new) + r'"[^>]*>(?:(?!</article>).)*?class="ml-dot" style="background:)#[0-9a-fA-F]{6}', r'\g<1>' + hx, s, flags=re.S)
open(f, "w", encoding="utf-8").write(s)
left = [o for o, _, _ in MAP if any(o in open(x, encoding="utf-8").read() for x in files)]
assert not left, left
print("done")
