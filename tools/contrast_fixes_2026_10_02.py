# -*- coding: utf-8 -*-
"""Contrast fixes (2 Oct 2026). Michael: look for faint text (light blue on white was hard
to read). A rendered audit of every page (WCAG AA: 4.5:1, 3:1 for large text) found the
failing text; this writes one scoped <style id="contrast-fixes"> block per page.

Rule for the replacement color, by the background the text actually sits on:
  light background: grays -> #5a6878, yellow -> #7a5000 (its registry partner), else #1a1d33
  dark or colored background: #ffffff
Decorative accordion icons (antiquark on quark, by design) are left alone.
Input: the audit's JSON (path given on the command line)."""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
audit = json.load(open(sys.argv[1], encoding="utf-8"))


def rgb(s):
    v = [float(x) for x in re.findall(r"[\d.]+", s)]
    return v[:3], (v[3] if len(v) > 3 else 1)


def lum(c):
    f = lambda x: x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4
    r, g, b = (x / 255 for x in c)
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def seg(s):
    """'div#copyright.legal-section.aos-init' -> 'div#copyright.legal-section' (drop animation classes)."""
    parts = re.split(r"(?=[.#])", s)
    keep = [p for p in parts if p not in (".aos-init", ".aos-animate")]
    return "".join(keep)


def selector(path):
    segs = [seg(x.strip()) for x in path.split(">")]
    # use the last segment plus the nearest ancestor that has a class or id, for precision
    last = segs[-1]
    anc = next((s for s in reversed(segs[:-1]) if ("." in s or "#" in s)), None)
    if not ("." in last or "#" in last) and not anc:
        return None
    return (anc + " " if anc else "") + last


rules = collections.defaultdict(dict)
skipped = []
for page, rows in audit.items():
    for r in rows:
        if "material-symbols" in r["path"]:
            continue
        fg, fa = rgb(r["fg"]); bg, _ = rgb(r["bg"])
        if fg[0] > 250 and fg[1] > 250 and fg[2] > 250 and sum(bg) > 740:
            continue                                  # white over a photo: the audit cannot see the image
        if "youtube" in r["path"] or "instagram" in r["path"]:
            continue
        sel = selector(r["path"])
        if not sel:
            skipped.append((page, r["path"], r["txt"][:30])); continue
        light = lum(bg) > 0.4
        if light:
            grayish = max(fg) - min(fg) < 40
            yellow = fg[0] > 200 and fg[1] > 180 and fg[2] < 80
            new = "#7a5000" if yellow else "#5a6878" if grayish and fa == 1 else "#1a1d33"
        else:
            new = "#ffffff"
        rules[page].setdefault(sel, set()).add(new)

conflicts = []
for page in list(rules):
    for sel, cs in list(rules[page].items()):
        if len(cs) > 1:                               # same selector on light and dark backgrounds: fix by context instead
            conflicts.append((page, sel, sorted(cs))); del rules[page][sel]
        else:
            rules[page][sel] = cs.pop()
# Context rules where one selector covers panels of different colors (checked by a second audit run).
OVERRIDES = {
    "download.html": {"drop": ["div.changelog h4", "div.fa-inner p", "div.fa-inner strong", "div.changelog li"], "add": [
        '.fa-inner .changelog h4, .fa-inner .changelog li { color: #ffffff !important; }',
        '.foundation-accordion[style*="--acc-stroke:#f1e303"] .fa-inner .changelog h4, .foundation-accordion[style*="--acc-stroke:#f1e303"] .fa-inner .changelog li { color: #1a1d33 !important; }',
        '.fa-inner p[style*="#f4f6f8"], .fa-inner p[style*="#f4f6f8"] strong { color: #1a1d33 !important; }']},
    "member-bio-template.html": {"drop": ["div.project-card span.project-role"], "add": ['.project-card .project-role { color: #ffffff !important; }']},
    "programs-gateway.html": {"drop": ["div.pc-head span.pc-phase"], "add": []},
    "simulations.html": {"drop": [".equation", "div.foundation-inner div.equation"], "add": [
        '.foundation-inner .equation { color: #f1e303 !important; background: #1a1d33 !important; }',
        '.highlight .viz-btn-outline { color: #005ba5 !important; border-color: #005ba5 !important; }']},
    "results-substrate-dynamics.html": {"drop": [], "add": ['.results-table thead tr th { color: #ffffff !important; }']},
    "testing-schedule.html": {"drop": [], "add": ['.warning-box strong, .detail-box[style*="#1a1a2e"] li strong { color: #f1e303 !important; }']},
}
for page, o in OVERRIDES.items():
    rs = rules.setdefault(page, {})
    for sel in o["drop"]:
        rs.pop(sel, None)
    for i, line in enumerate(o["add"]):
        sel, css = line.split("{", 1)
        rs[sel.strip()] = "RAW:" + css.strip().rstrip("}").strip()
for page, rs in rules.items():
    s = open(page, encoding="utf-8").read()
    s = re.sub(r'\n?<style id="contrast-fixes">.*?</style>', "", s, flags=re.S)
    css = "\n".join(f"  {sel} {{ {c[4:]} }}" if c.startswith("RAW:") else f"  {sel} {{ color: {c} !important; }}"
                    for sel, c in sorted(rs.items()))
    block = f'\n<style id="contrast-fixes">\n  /* readable text (WCAG AA), from the 2 Oct 2026 contrast audit: tools/contrast_fixes_2026_10_02.py */\n{css}\n</style>'
    m = re.search(r"</head>|<body\b", s)       # validation.html has no </head>: then go before <body>
    s = s[:m.start()] + block + "\n" + s[m.start():]
    open(page, "w", encoding="utf-8").write(s)
print(len(rules), "pages,", sum(len(v) for v in rules.values()), "rules")
print("conflicts (same selector, light and dark grounds):", conflicts)
print("skipped (no precise selector):", len(skipped))
for x in skipped[:40]: print("  ", x)
