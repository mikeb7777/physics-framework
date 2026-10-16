# -*- coding: utf-8 -*-
"""Site changes for the consolidated Version 6D (Michael, 16 Oct 2026). See
tools/book_6d_consolidated_2026_10_16.py for the book itself.

  download.html    the four interim cards (6G, 6F, 6E, 6D) become one Version 6D card whose changelog
                   holds every change made after 6C, in book order; the CTA points to 6D
  references.html  "Matched to Version 6D"; Introduction [61] to [64] added
  appendix.html    "Version 6F" -> "Version 6D" (two notes)
  blog.html        "Five changes are in Version 6F" -> "Version 6D"
  glossary.html    Critical Point, Ising Model, Conformal Transformation, Renormalization Group added;
                   Phase Transition no longer says every transition is abrupt

Run once:  python3 tools/site_6d_consolidated_2026_10_16.py   then rebuild search-index.json.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def edit(name, fn):
    path = os.path.join(ROOT, name)
    s = open(path, encoding="utf-8").read()
    t = fn(s)
    assert t != s, name
    open(path, "w", encoding="utf-8").write(t)
    print("edited", name)


def once(s, old, new):
    assert s.count(old) == 1, (old[:70], s.count(old))
    return s.replace(old, new)


# ---------------------------------------------------------------- download.html
Y = "color:#f1e303;font-weight:600;"
CHANGES = [
    # Introduction
    "Introduction, new section: &ldquo;When the Boundary Costs Nothing&rdquo;. What happens to the point, circle and sphere at a "
    "phase transition: when a boundary costs nothing, domains become fractal, the circle survives as the symmetry of the critical "
    "state, and the sphere and the fractal appear as two fixed points of one substrate. Four new references and four new glossary terms",
    "Introduction: the Fibonacci sequence credited to the Indian scholars of poetic meter who described it centuries before Leonardo of Pisa",
    "Introduction: Egyptian multiplication by doubling, the oldest written binary arithmetic, still taught in a halving-and-doubling "
    "form in Ethiopia and Eritrea",
    # Elements 1 to 3
    "Element 1: the history of &pi; reached independently in Egypt, Greece, China, India and Persia (Archimedes, Liu Hui, Zu Chongzhi, "
    "Madhava, al-Kashi)",
    "Element 2: the word &ldquo;algorithm&rdquo; credited to al-Khwarizmi",
    "Element 2: the mental-practice result corrected to about 22 percent (Yue and Cole, 1992); Lloyd&rsquo;s analysis in Nature named as "
    "the synthesis of the physical limits of computation; processors described as still far above the Landauer limit",
    "Element 3: the single-bit Landauer test credited to Berkeley (nanomagnetic bits); the Bennu samples&rsquo; 14 of 20 protein amino "
    "acids stated correctly; the 2025 adversarial test of IIT and Global Workspace Theory described as challenging both",
    # Element 5
    "Element 5: beta decay stated correctly (a down quark becomes an up quark); the W and Z bosons are about 86 to 97 times the "
    "proton&rsquo;s mass",
    "Element 5: the matter excess is attributed to CP violation, not parity violation alone, with the measured amount noted as too small; "
    "the link to the first-instant asymmetry is posed as a question",
    # Element 7
    "Element 7: the brain and cosmic web comparison now describes what Vazza and Feletti (2020) actually measured, the power spectrum and "
    "network statistics of both networks. The earlier account of machine-learning classifiers performing at 50% chance, and a "
    "&ldquo;spectral dimension&rdquo; figure, are removed; neither is in the paper. The tissue is identified correctly as human, under "
    "light microscopy, and the paper&rsquo;s own limit is stated: connections were defined by proximity, not synapses",
    "Element 7: Figure 7-2 redrawn. Dark matter is about 85% of all matter; glial cells and neurons are about equal in number. The "
    "earlier figure showed 85/15 for both",
    "Element 7: the information content of matter stated as the Bekenstein bound, a maximum",
    # Elements 10 to 14
    "Elements 10 and 11: what the Zenodo records contain stated accurately (the five-band paper; code for a related analysis)",
    "Element 12: the anthropic principle, the multiverse and the Past Hypothesis are named and answered before the framework&rsquo;s "
    "account of the low-entropy start",
    "Element 14: the fractal-dimension passage on the CMB corrected. Caruso and Oguri&rsquo;s result is an upper limit, not evidence that "
    "space differs from three dimensions, and the fractal temperature contours on CMB maps describe the pattern on the sky, not the "
    "dimension of space",
    # Elements 15 to 18
    "Elements 15, 18 and 19: the 2025 Annals of Physics work (Neukart) described as a proposal",
    "Element 16: water&rsquo;s proton tunneling and the disputed room-temperature coherence claim stated accurately; Figure 16-1 caption "
    "corrected (the molecules come from structural data, and the artist arranged the scene)",
    "Element 17: the last legacy &ldquo;25-million-to-one&rdquo; ratio corrected to 100 million to one, and the share of visual "
    "information discarded corrected to match; the duplicate pinwheel figure removed in favor of Figure 3-3",
    # Element 19
    "Element 19: Hawking radiation described consistently with the Page curve: each particle looks thermal, while the information "
    "returns in correlations across the radiation",
    "Element 19: the Penrose-Hawking theorems described as proving that the paths of particles and light end, not that density becomes "
    "infinite",
    "Element 19: the singularity inside a black hole is a moment only without rotation; in a rotating black hole it is a ring that some "
    "paths can in principle avoid",
    "Element 19: the infalling observer notices nothing at the horizon; closer in, tidal forces grow without limit",
    "Element 19: &ldquo;the universe as evidence&rdquo; replaced by the test that can decide it, gravitational-wave echoes after black "
    "hole mergers; the uncertainty-principle argument marked as heuristic",
    "Element 19, added: two meanings of one word, the mathematical and the physical singularity; and everything physics says about a "
    "black hole it says through relationships, with what the absence of singularities would and would not show",
    # Elements 20 and 21
    "Element 20: the 2019 verified-scrambling experiment correctly described (trapped ions, University of Maryland); Sekino and "
    "Susskind dated 2008",
    "Element 21: USTC&rsquo;s Zuchongzhi 3.2 result (<em>Physical Review Letters</em>, December 2025), the second, independent "
    "demonstration of error correction below threshold",
    # Citations
    "Citations: every citation checked against the sentence that cites it and against the publisher&rsquo;s record; in Elements 2, 6, "
    "8, 13, 15 and 19 the numbers renumbered so each marks one source",
    f"Twelve new references: eight from the source audit and four in the Introduction ([61] to [64]), all on the "
    f"<a href=\"references.html\" style=\"{Y}\">references page</a>, which now matches the book in full",
]
for c in CHANGES:
    assert "—" not in c and "&mdash;" not in c

CARD = f"""        <div class="foundation-accordion" style="--acc-color:#8e0c45; --acc-stroke:#1a7a36; border-left:4px solid #1a7a36;">
          <div class="foundation-header" onclick="this.parentElement.classList.toggle('active')">
            <h3>Version 6D <span style="display:inline-block;background:#f1e303;color:#8B0000;font-size:0.68rem;font-weight:800;padding:0.18rem 0.6rem;border-radius:20px;margin-left:0.5rem;text-transform:uppercase;letter-spacing:0.06em;" class="blink">Latest Version</span></h3>
            <span class="toggle-indicator">&#9660;</span>
          </div>
          <div class="fa-content">
            <div class="fa-inner">
              <p style="color:#2c3e50;line-height:1.8;margin-bottom:1rem;">16 October 2026. Every change made since 6C, in one edition. Each claim about the brain and the cosmic web, and every citation in the book, was checked against its source. An audit of where the sources come from led the book to credit mathematics it had told only half the story of; what the audit found is in <a href="blog.html#reading-the-whole-map" style="{Y}">Reading the Whole Map</a>. Element 19 now uses the word singularity the way physics does. One new section, in the Introduction, follows the sphere to a phase transition and finds the fractal. The framework&rsquo;s argument is otherwise unchanged. The next revision will be Version 7.</p>
              <div class="changelog">
                <h4>Changes in Version 6D</h4>
                <ul>
""" + "".join(f"                    <li>{c}</li>\n" for c in CHANGES) + """                </ul>
              </div>
              <div class="btn-container" style="margin-top:1.25rem;">
                <a href="A%20Quest%20for%20The%20Big%20TOE%20Version%206D.pdf" class="btn-pill" download>Download PDF</a>
              </div>
            </div>
          </div>
        </div>

"""


def download(s):
    start = s.index('        <div class="foundation-accordion" style="--acc-color:#8B0000; --acc-stroke:#00838f; border-left:4px solid #00838f;">\n'
                    '          <div class="foundation-header" onclick="this.parentElement.classList.toggle(\'active\')">\n'
                    '            <h3>Version 6G')
    end = s.index('        <div class="foundation-accordion"', s.index("<h3>Version 6D ") + 10)   # the 6C card
    assert "<h3>Version 6C " in s[end:end + 400]
    s = s[:start] + CARD + s[end:]
    s = once(s, 'href="A%20Quest%20for%20The%20Big%20TOE%20Version%206G.pdf" class="btn-pill" style="font-size: 1.2rem; padding: 1rem 3rem;" download>Download Now: Version 6G</a>',
                'href="A%20Quest%20for%20The%20Big%20TOE%20Version%206D.pdf" class="btn-pill" style="font-size: 1.2rem; padding: 1rem 3rem;" download>Download Now: Version 6D</a>')
    for v in "EFG":
        assert f"Version%206{v}" not in s and f"Version 6{v}" not in s, v
    return s


edit("download.html", download)

# ---------------------------------------------------------------- references.html
NEW_REFS = [
    ("61", "Stanley, H. E. (1971). Introduction to Phase Transitions and Critical Phenomena. Oxford University Press. "
           "[Critical points, the vanishing of surface tension between coexisting phases, and scale-free fluctuations.]", None),
    ("62", "Duplantier, B., &amp; Saleur, H. (1989). &quot;Exact fractal dimension of 2D Ising clusters.&quot; Physical Review "
           "Letters, 63(22), 2536&ndash;2537. doi:10.1103/PhysRevLett.63.2536 [The boundaries of critical Ising clusters have fractal "
           "dimension 11/8.]", "10.1103/PhysRevLett.63.2536"),
    ("63", "Belavin, A. A., Polyakov, A. M., &amp; Zamolodchikov, A. B. (1984). &quot;Infinite conformal symmetry in two-dimensional "
           "quantum field theory.&quot; Nuclear Physics B, 241(2), 333&ndash;380. doi:10.1016/0550-3213(84)90052-X [Conformal invariance "
           "of two-dimensional critical systems.]", "10.1016/0550-3213(84)90052-X"),
    ("64", "Wilson, K. G. (1971). &quot;Renormalization group and critical phenomena. I. Renormalization group and the Kadanoff "
           "scaling picture.&quot; Physical Review B, 4(9), 3174&ndash;3183. doi:10.1103/PhysRevB.4.3174 [A critical point as a fixed "
           "point of the renormalization group.]", "10.1103/PhysRevB.4.3174"),
]


def references(s):
    s = once(s, "<strong>Matched to Version 6G (October 2026).</strong>", "<strong>Matched to Version 6D (October 2026).</strong>")
    anchor = "Imhausen, A. (2016). Mathematics in Ancient Egypt: A Contextual History. Princeton University Press. [Multiplication by doubling in the Rhind papyrus.]</p>\n                </div>\n"
    add = ""
    for n, text, doi in NEW_REFS:
        link = (f' <a href="https://doi.org/{doi}" target="_blank" rel="noopener" class="ref-src">View Source</a>' if doi else "")
        add += (f"                <div class=\"reference-item\">\n"
                f"                    <p><strong>[{n}]</strong> {text}{link}</p>\n"
                f"                </div>\n")
    return once(s, anchor, anchor + add)


edit("references.html", references)

# ---------------------------------------------------------------- appendix.html, blog.html
edit("appendix.html", lambda s: once(once(s, "Version 6F summarizes Section A", "Version 6D summarizes Section A"),
                                     "<strong>In the book from Version 6F</strong>", "<strong>In the book from Version 6D</strong>"))
edit("blog.html", lambda s: once(s, "Five changes are in Version 6F of", "Five changes are in Version 6D of"))

# ---------------------------------------------------------------- glossary.html
def entry(name, text):
    return (f'    <div class="term-entry">\n    <div class="term-name">{name}</div>\n'
            f'    <div class="term-definition">{text}</div>\n    </div>\n')


GLOSS = {
    "Phase Transition": None,  # rewritten below
    "Critical Point": "The point at which a continuous phase transition happens, such as water at 374 &deg;C and 218 atmospheres, where "
        "liquid and vapor stop being different, or a magnet at the temperature where its magnetization disappears. At a critical point "
        "the surface tension between the two phases falls to zero, fluctuations occur at every scale at once, and the system looks the "
        "same at every magnification. See also: Phase Transition, Renormalization Group.",
    "Ising Model": "The simplest model of a magnet: a grid of sites, each pointing up or down, with neighbors preferring to agree. In two "
        "dimensions it was solved exactly by Lars Onsager in 1944, which made it the standard testing ground for phase transitions. At "
        "its critical point the clusters of aligned sites are fractal, and their boundaries have a fractal dimension of exactly 11/8.",
    "Conformal Transformation": "A change of coordinates that preserves angles at every point, though it may stretch distances by "
        "different amounts in different places. In their global form, conformal transformations carry circles into circles. Systems "
        "at a critical point in two dimensions are unchanged by them, a symmetry strong enough to fix many of their properties exactly.",
    "Renormalization Group": "A method, developed by Kenneth Wilson in the early 1970s, for asking how a physical system looks when it "
        "is viewed at coarser and coarser scales. Repeating the step moves the description toward a fixed point. A critical point is "
        "such a fixed point: a state that looks identical at every magnification. Wilson received the 1982 Nobel Prize in Physics for "
        "this work.",
}
PHASE_OLD = ("An abrupt change in a system's properties when conditions cross a critical threshold. Examples include water freezing "
             "into ice or a superconductor becoming resistanceless.")
PHASE_NEW = ("A change in a system's state when conditions cross a threshold. In a first-order transition, such as water freezing, "
             "the change is abrupt and the new phase forms as droplets or crystals. In a continuous transition, such as a magnet "
             "losing its magnetization at its critical point, the change is gradual and fluctuations appear at every scale.")


def glossary(s):
    s = once(s, PHASE_OLD, PHASE_NEW)
    for name in ("Critical Point", "Ising Model", "Conformal Transformation", "Renormalization Group"):
        assert f'term-name">{name}<' not in s, name
    # each new entry goes before the first existing entry that sorts after it, among entries with the same first letter
    names = re.findall(r'<div class="term-entry">\n    <div class="term-name">([^<]+)</div>', s)
    for name in ("Conformal Transformation", "Critical Point", "Ising Model", "Renormalization Group"):
        same = [n for n in names if n[0] == name[0]]
        after = next((n for n in same if n.lower() > name.lower()), None)
        if after is None:
            after = next(n for n in names if n[0] > name[0])
        marker = f'    <div class="term-entry">\n    <div class="term-name">{after}</div>'
        s = once(s, marker, entry(name, GLOSS[name]) + marker)
        names = re.findall(r'<div class="term-entry">\n    <div class="term-name">([^<]+)</div>', s)
    return s


edit("glossary.html", glossary)
