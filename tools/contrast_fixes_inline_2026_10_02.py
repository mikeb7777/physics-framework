# -*- coding: utf-8 -*-
"""Second pass of the contrast fixes: failing text whose element has no class to target,
usually because its color is set inline. Finds the text in the source, then changes the
color in the style attribute of the element that holds it (or its parent). Same color
rule as contrast_fixes_2026_10_02.py. Prints anything it cannot place."""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def rgb(s):
    v = [float(x) for x in re.findall(r"[\d.]+", s)]
    return v[:3], (v[3] if len(v) > 3 else 1)


def lum(c):
    f = lambda x: x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4
    r, g, b = (x / 255 for x in c)
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def selector(path):
    """Same test as the first pass: True when that pass could target the element by class or id."""
    segs = [x.strip().replace(".aos-init", "").replace(".aos-animate", "") for x in path.split(">")]
    return ("." in segs[-1] or "#" in segs[-1]) or any(("." in x or "#" in x) for x in segs[:-1])

audit = json.load(open(sys.argv[1], encoding="utf-8"))
left = []
for page, rows in audit.items():
    s = open(page, encoding="utf-8").read(); orig = s
    for r in rows:
        if "material-symbols" in r["path"] or "youtube" in r["path"] or "instagram" in r["path"] or selector(r["path"]):
            continue
        fg, fa = rgb(r["fg"]); bg, _ = rgb(r["bg"])
        if min(fg) > 250 and sum(bg) > 740:
            continue
        light = lum(bg) > 0.4
        yellow = fg[0] > 200 and fg[1] > 180 and fg[2] < 80
        new = ("#7a5000" if yellow else "#5a6878" if max(fg) - min(fg) < 40 and fa == 1 else "#1a1d33") if light else "#ffffff"
        txt = r["txt"].strip()[:24]
        i = s.find(html.escape(txt, quote=False)) if html.escape(txt, quote=False) in s else s.find(txt)
        if i < 0:
            left.append((page, r["path"], txt)); continue
        placed = False
        for depth in range(2):                       # the element holding the text, then its parent
            o = s.rfind("<", 0, i)
            while o >= 0 and s[o + 1] == "/":         # skip closing tags back to an opening tag
                o = s.rfind("<", 0, o)
            if depth:
                o = s.rfind("<", 0, o)
                while o >= 0 and s[o + 1] == "/":
                    o = s.rfind("<", 0, o)
            tag_end = s.find(">", o)
            tag = s[o:tag_end + 1]
            m = re.search(r'style="([^"]*)"', tag)
            if m and re.search(r"(^|;)\s*color\s*:", m.group(1)):
                st = re.sub(r"((?:^|;)\s*color\s*:\s*)[^;]+", lambda k: k.group(1) + new, m.group(1), count=1)
                s = s[:o] + tag.replace(m.group(0), f'style="{st}"') + s[tag_end + 1:]
                placed = True; break
        if not placed:
            left.append((page, r["path"], txt))
    if s != orig:
        open(page, "w", encoding="utf-8").write(s)
print("unplaced:", len(left))
for x in left: print("  ", x)
