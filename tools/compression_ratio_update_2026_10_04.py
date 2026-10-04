# -*- coding: utf-8 -*-
"""Update the conscious-bandwidth figures sitewide (4 Oct 2026, Michael: "The compression ratio there is
still the old numbers"). Zheng & Meister, Neuron (2024): about 10 bits/s of conscious throughput against
about 10^9 bits/s of sensory input, about 100 million to one. Supersedes the 40 bits/s (Norretranders) and
"25 million to one" / "10 to 40 bits" figures. references.html already cites Zheng & Meister. Run once."""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = [
    (r"somewhere about", "about"),
    (r"between 10 and 40 bits per second", "about 10 bits per second"),
    (r"somewhere between ten and forty", "about ten"),
    (r"(?:about )?10 to 40 bits per second", "about 10 bits per second"),
    (r"25-million-to-one", "100-million-to-one"),
    (r"tens-of-millions-to-one", "hundred-million-to-one"),
    (r"tens of millions to one", "about a hundred million to one"),
    (r'(<span class="stat-value">)25–100M:1(</span>)', r"\g<1>100M:1\g<2>"),
    (r'(<span class="stat-value">)10–40(</span>\s*<span class="stat-label">Bits per second)', r"\g<1>~10\g<2>"),
]
total = 0
for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    if os.path.basename(path) in ("references.html", "knowledge-tree.html"):
        continue
    s = open(path, encoding="utf-8").read(); n0 = 0
    for pat, rep in RULES:
        s, n = re.subn(pat, rep, s); n0 += n
    s = s.replace("about about", "about")
    if n0:
        open(path, "w", encoding="utf-8").write(s); total += n0
        print(f"{os.path.basename(path)}: {n0}")
print("total replacements:", total)
