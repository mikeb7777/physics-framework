# -*- coding: utf-8 -*-
"""Program pages, one color system (Michael, 7 Oct 2026: the cymatics page "deviates from our color layout ...
low-contrast, same colors on background and foreground ... update all of these pages so we don't add more
color patterns").

1. Each program keeps the QCD pair the Programs gateway and the Testing Schedule already give it. The
   5 Oct recolor (program_pages_palette_2026_10_05.py) used a different mapping for three pages; this
   corrects them:
     Cognitive Extension (overview, pilot)  #005ba5 / #f1e303   (was #005f6e)
     Consciousness Tuning                   #1a5c2a / #b01558   (was #8e0c45)
     NBI                                    #8e0c45 / #1a7a36   (was #005ba5)
     3D Cymatics                            #005f6e / #c62828
     Elite Performance                      #8B0000 / #00838f
2. Cymatics and Elite Performance get the same treatment as the others: navy #1a1d33 hero with a 6px rule in
   the program color, navy dark bands, flat fills instead of gradients, palette text colors, and yellow
   #f1e303 headings on navy instead of cyan on teal.
3. Cymatics text updates: gas and schlieren checks in Phase 1, literature-check status, and "can begin now"
   in place of "begins immediately" (nothing has started).
Run once."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def edit(name, pairs, regex=()):
    p = os.path.join(ROOT, name)
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        n = s.count(a)
        assert n >= 1, (name, a[:70])
        s = s.replace(a, b)
    for pat, rep, cnt in regex:
        s, k = re.subn(pat, rep, s)
        assert k == cnt, (name, pat, k)
    open(p, "w", encoding="utf-8").write(s)
    print("ok", name)


def swap_accent(name, old_hex, old_rgb, new_hex, new_rgb, keep=()):
    """Replace one program accent everywhere except protected lines (semantic status colors)."""
    p = os.path.join(ROOT, name)
    lines = open(p, encoding="utf-8").read().split("\n")
    n = 0
    for i, l in enumerate(lines):
        if any(k in l for k in keep):
            continue
        m = l.replace(old_hex, new_hex).replace(f"rgba({old_rgb},", f"rgba({new_rgb},")
        if m != l:
            n += 1
            lines[i] = m
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("accent", name, n, "lines")


# 1. correct the three pages recolored on 5 Oct
swap_accent("program-nbi.html", "#005ba5", "0,91,165", "#8e0c45", "142,12,69")
swap_accent("program-consciousness-tuning.html", "#8e0c45", "142,12,69", "#1a5c2a", "26,92,42",
            keep=(".status-unknown",))
for f in ("program-cognitive-extension-overview.html", "program-cognitive-extension-pilot.html"):
    swap_accent(f, "#005f6e", "0,95,110", "#005ba5", "0,91,165")

# 2a. Elite Performance
edit("program-elite-performance-overview.html", [
    ("--secondary-color: #2d3f52;", "--secondary-color: #4a5868;"),
    ("--accent-program-dark: #5a0000;", "--accent-program-dark: #1a1d33;"),
    ("--accent-nbi-light: #1a7ad4;", "--accent-nbi-light: #00838f;"),
    ("--text-dark: #2c3e50;", "--text-dark: #1a1d33;"),
    ("--text-light: #666;", "--text-light: #5a6878;"),
    ("background: linear-gradient(135deg, #5a0000 0%, #8B0000 60%, #8B0000 100%);",
     "background: #1a1d33;\n    border-bottom: 6px solid #8B0000;"),
    ("rgba(26,122,212,0.3)", "rgba(139,0,0,0.45)"),
    ("background: linear-gradient(135deg, #5a0000 0%, #8B0000 100%);", "background: #1a1d33;"),
    ("background: #a00000;", "background: #6b0000;"),
    ("rgba(14,95,168,0.3)", "rgba(139,0,0,0.3)"),
    ("background: #1a1a2e;", "background: #1a1d33;"),
])

# 2b + 3. Cymatics
edit("program-cymatics.html", [
    ("--secondary-color: #2d3f52;", "--secondary-color: #4a5868;"),
    ("--accent: #006064;", "--accent: #005f6e;"),
    ("--accent-mid: #00838f;", "--accent-mid: #1a1d33;"),
    ("--accent-light: #00bcd4;", "--accent-light: #f1e303;"),
    ("--text-dark: #2c3e50;", "--text-dark: #1a1d33;"),
    ("--text-light: #666;", "--text-light: #5a6878;"),
    ("background: linear-gradient(135deg, #003740 0%, #006064 100%);\n        color: white;\n        padding: 3.5rem 2rem 3rem;",
     "background: #1a1d33;\n        border-bottom: 6px solid #005f6e;\n        color: white;\n        padding: 3.5rem 2rem 3rem;"),
    ("border: 1px solid rgba(0,188,212,0.1);", "border: 1px solid rgba(255,255,255,0.08);"),
    ("border: 1px solid rgba(0,188,212,0.07);", "border: 1px solid rgba(255,255,255,0.06);"),
    ("color: #80deea; }", "color: #ffffff; }"),
    (".content-section.dark-section { background: linear-gradient(135deg, #003740 0%, #005060 100%); color: white; }",
     ".content-section.dark-section { background: #1a1d33; border-top: 6px solid #005f6e; color: white; }"),
    (".predictions-box { background: rgba(0,188,212,0.06); border: 1px solid rgba(0,188,212,0.2);",
     ".predictions-box { background: rgba(0,95,110,0.06); border: 1px solid rgba(0,95,110,0.25);"),
    ("border-bottom: 1px solid rgba(0,188,212,0.1); color: var(--text-light);", "border-bottom: 1px solid rgba(0,95,110,0.12); color: var(--text-dark);"),
    ('.predictions-box ul li::before { content: "—"; position: absolute; left: 0; color: var(--accent-light); }',
     '.predictions-box ul li::before { content: "—"; position: absolute; left: 0; color: var(--accent); }'),
    (".phase-cost { display: inline-block; background: #e0f7f4; color: #00695c;", ".phase-cost { display: inline-block; background: #e8edf2; color: #005f6e;"),
    (".info-box { background: #1a1a2e;", ".info-box { background: #1a1d33;"),
    ("border: 1px solid #f9a825; border-left: 4px solid #f9a825;", "border: 1px solid #f1e303; border-left: 4px solid #7a5000;"),
    (".cta-section { background: linear-gradient(135deg, #003740 0%, #006064 100%);", ".cta-section { background: #1a1d33;"),
    (".btn-white:hover { background: #e0f7f4;", ".btn-white:hover { background: #e8edf2;"),
    ("footer { background: #2c3e50;", "footer { background: #1a1d33;"),
    ('<div style="background: linear-gradient(135deg, #003740 0%, #006064 100%); color: white; padding: 3rem; border-radius: 12px; text-align: center;" data-aos="fade-up">',
     '<div style="background: #1a1d33; border-bottom: 6px solid #005f6e; color: white; padding: 3rem; border-radius: 12px; text-align: center;" data-aos="fade-up">'),
    ("background: white; color: #006064;", "background: white; color: #005f6e;"),
    ('<a href="testing-schedule.html#cymatics-prediction" style="color: var(--accent); font-weight: 600; font-size: 0.9rem;">',
     '<a href="testing-schedule.html#cymatics-prediction" style="color: #ffffff; font-weight: 600; font-size: 0.9rem;">'),
    ('<a href="visualizations.html#chamber-model" style="color: var(--accent); font-weight: 600; font-size: 0.9rem;">',
     '<a href="visualizations.html#chamber-model" style="color: #ffffff; font-weight: 600; font-size: 0.9rem;">'),
    # text
    ('<span class="phase-cost">Under $1,000: begins immediately</span>', '<span class="phase-cost">Under $1,000: can begin now</span>'),
    ("which gather where the beads do not. The chamber model predicts how each medium shifts the pattern, so the comparison tests the model, and separates what belongs to the chamber's geometry from what belongs to the medium, before any flight.</p>",
     "which gather where the beads do not. The chamber model predicts how each medium shifts the pattern, so the comparison tests the model, and separates what belongs to the chamber's geometry from what belongs to the medium, before any flight.</p>\n"
     "                <p>Two more checks of the model need no flight. Filling the air chamber with helium, carbon dioxide or sulfur hexafluoride changes the speed of sound, so every resonance should shift by a predictable factor while the node geometry stays the same. And because the sound field itself does not depend on gravity, schlieren imaging, which photographs the small density changes sound makes in a gas, can map the field on the ground for comparison with the model.</p>"),
    ("All experimental predictions for Phases 2 and 3 will be pre-registered on Zenodo and the Open Science Framework before any microgravity data collection begins. This is a firm commitment.</p>",
     "All experimental predictions for Phases 2 and 3 will be pre-registered on Zenodo and the Open Science Framework before any microgravity data collection begins. This is a firm commitment.</p>\n"
     "                <p>October 2026: a check of related published work (drops and other fluids driven by sound, other gases, and imaging of sound fields) is under way. Ideas that hold up will be added to Phase 1 before its predictions are registered. Nothing will be described as new until that check is complete.</p>"),
])
