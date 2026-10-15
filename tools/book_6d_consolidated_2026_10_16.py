# -*- coding: utf-8 -*-
"""Version 6D of A Quest for The Big TOE, consolidated (Michael, 16 Oct 2026: "rename this as 6D and
compile all changes after 6C into its description. No one has downloaded the other revisions. The
next revision will be 7 to prevent confusion.").

The interim files 6D, 6E, 6F and 6G are folded into one Version 6D. This script builds it from the
6G text and adds one new section:

  Introduction, after "Why the Sphere Carries Incompleteness": "When the Boundary Costs Nothing".
  What happens to the sphere at a continuous phase transition: surface tension vanishes, domains
  become fractal, the order parameter fluctuates over the whole sphere, conformal (circle-preserving)
  symmetry appears, and the critical point is a renormalization-group fixed point. Fractals may be as
  fundamental as the sphere. Came out of Michael's question (16 Oct 2026) about fractals near phase
  transitions in his point, circle, sphere example.

  New references, Introduction [61] to [64] (the Introduction already ran to [60]).
  New glossary markers [g]: critical point, Ising model, conformal transformations, renormalization group.
  Edition line: "Version 6G" -> "Version 6D".

The 2D Ising value is the hull (cluster boundary) dimension 11/8 from Duplantier and Saleur (1989),
not 7/4, which is the percolation hull. Run once:  python3 tools/book_6d_consolidated_2026_10_16.py
"""
import copy, os, re
import docx

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "A Quest for The Big TOE Version 6G.docx")
DST = os.path.join(ROOT, "A Quest for The Big TOE Version 6D.docx")

d = docx.Document(SRC)
P = d.paragraphs
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def only(pred, what):
    hits = [p for p in P if pred(p)]
    assert len(hits) == 1, (what, len(hits))
    return hits[0]


def copy_after(anchor_p, template_p, text):
    """A copy of `template_p` (paragraph style, first-run formatting) placed after `anchor_p`.
    Citation numbers [n] and glossary markers [g] are set as superscript runs, as in the book."""
    new = copy.deepcopy(template_p._p)
    for c in list(new):
        if c.tag in (W + "hyperlink", W + "bookmarkStart", W + "bookmarkEnd", W + "proofErr"):
            new.remove(c)
    anchor_p._p.addnext(new)
    q = docx.text.paragraph.Paragraph(new, template_p._parent)
    for r in q.runs[1:]:
        r._r.getparent().remove(r._r)
    base = q.runs[0]
    parts = [s for s in re.split(r"(\[(?:\d+|g)\])", text) if s]
    base.text = parts[0]
    base.font.superscript = None
    prev = base._r
    for s in parts[1:]:
        r = copy.deepcopy(base._r)
        prev.addnext(r)
        prev = r
        run = docx.text.run.Run(r, q)
        run.text = s
        run.font.superscript = True if re.fullmatch(r"\[(?:\d+|g)\]", s) else None
    return q


# Edition line
ed = only(lambda p: p.text.strip() == "Version 6G", "edition line")
ed.runs[0].text = "Version 6D"

# Introduction: new section after "Why the Sphere Carries Incompleteness"
head = only(lambda p: p.text.strip() == "WHY THE SPHERE CARRIES INCOMPLETENESS" and p.style.name == "subchapter",
            "incompleteness heading")
last = only(lambda p: p.text.startswith("This mirrors Zeno") and p.style.name == "main body", "Zeno paragraph")
nxt = only(lambda p: p.text.strip() == "WHY CONCEPTS HAVE ENERGY WITHOUT BEING COMPUTED", "next heading")
assert last._p.getnext() is nxt._p, "the Zeno paragraph must end the incompleteness section"

HEADING = "WHEN THE BOUNDARY COSTS NOTHING"
BODY = [
    "The sphere wins its contest for a specific reason: every boundary carries a cost. In physical systems, that "
    "cost is surface tension, and the sphere minimizes it. Remove the cost, and the sphere loses its privilege.",

    "Nature performs this experiment at every continuous phase transition. As a magnet or a fluid approaches its "
    "critical point[g], the surface tension between its two phases falls to zero [61]. Domains of the new phase stop "
    "forming as rounded droplets. They become fractal: clusters nested within clusters at every scale, with no "
    "typical size. In the two-dimensional Ising model[g] of a magnet, the boundaries of these clusters have a fractal "
    "dimension of exactly 11/8, more than a line and less than a plane [62]. At the critical point of water, density "
    "fluctuations of every size scatter light, and the clear fluid turns milky.",

    "The first distinction appears here as well. In a magnet whose atoms favor no direction in space, the possible "
    "orientations form a sphere. Above the critical temperature, the average orientation sits at the center: a "
    "point, with no direction at all. Below it, the system selects a single point on the sphere, and the symmetry "
    "breaks. At the transition itself, the system cannot settle, and it fluctuates across the entire sphere at every "
    "scale at once.",

    "The circle does not vanish. In two dimensions, critical systems become invariant under conformal "
    "transformations[g], which preserve angles at every point and, in their global form, carry circles into circles "
    "[63]. The round shapes disappear from the physical domains, yet circle-preserving geometry becomes the symmetry "
    "of the whole critical state.",

    "Physics therefore offers two geometric limits, not one. A critical point is a fixed point of the "
    "renormalization group[g]: a configuration that looks identical at every magnification [64]. The sphere is the "
    "fixed point that appears when boundaries are costly. The fractal is the fixed point that appears when they are "
    "free. Neither is a state that physical reality occupies, and each marks a direction in which it is drawn. This "
    "suggests that fractals may be as fundamental as the sphere: the signature of the same substrate when "
    "fluctuation, rather than order, dominates.",
]
for t in [HEADING] + BODY:
    assert "—" not in t and "–" not in t, "no dashes in published text"
    assert not re.search(r"n't\b|'(re|ll|ve)\b", t.replace("’", "'")), "no contractions in published text"

anchor = copy_after(last, head, HEADING)
for t in BODY:
    anchor = copy_after(anchor, last, t)

d.core_properties.revision = (d.core_properties.revision or 0) + 1
d.save(DST)
print("wrote", os.path.basename(DST))
