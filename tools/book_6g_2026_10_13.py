# -*- coding: utf-8 -*-
"""Version 6G of A Quest for The Big TOE, from Version 6F (Michael, 13 Oct 2026: "let's do 6G now").

Applies 6G-PROPOSED-CHANGES.md, which came out of a review of how Element 19 describes
singularities (mathematics and physics use the word differently; the singularity theorems prove
geodesic incompleteness, not infinite density; a rotating black hole's singularity is a ring):

  A1  "The Singularity That Isn't": what the singularity theorems actually prove
  A2  "Open Questions": not every black hole singularity is a temporal boundary
  A3  "Open Questions": the infalling observer notices nothing at the horizon, not near the centre
  A4  "Chaos as Information Processing": the universe continuing is not evidence; the echo test is
  A5  "Chaos as Information Processing": the uncertainty argument is heuristic
  B1  "The Singularity That Isn't": two meanings of one word
  B2  "How Not to Have a Universe": properties come from relationships
  A6  Element 14, "Fractal dimensions in the CMB": what Caruso and Oguri found (an upper limit), and
      what the fractal CMB isotherms are (a pattern on the sky, not the dimension of space). Added
      14 Oct 2026 on Michael's question about fractal dimension; 6G was rebuilt with it, still 6G.
  --  Edition line: "Version 6F" -> "Version 6G"

No new references in Element 19. Element 14 [12] to [15] are restored on the references page. New paragraphs are copies of the paragraph they follow, with the text replaced,
so they keep the book's body style. Run once:  python3 tools/book_6g_2026_10_13.py
"""
import copy, os
import docx

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "A Quest for The Big TOE Version 6F.docx")
DST = os.path.join(ROOT, "A Quest for The Big TOE Version 6G.docx")

d = docx.Document(SRC)
P = d.paragraphs


def para(start):
    """The one paragraph whose text starts with `start`."""
    hits = [p for p in P if p.text.startswith(start)]
    assert len(hits) == 1, (start, len(hits))
    return hits[0]


def set_run(p, k, old, new):
    """Replace `old` with `new` inside run k of paragraph p, checking it is there exactly once."""
    r = p.runs[k]
    assert r.text.count(old) == 1, (old, r.text[:80])
    r.text = r.text.replace(old, new)


def add_paragraph_after(p, text):
    """A copy of paragraph `p` (style and first-run formatting) holding `text`, placed after it."""
    new = copy.deepcopy(p._p)
    p._p.addnext(new)
    q = docx.text.paragraph.Paragraph(new, p._parent)
    for r in q.runs[1:]:
        r._r.getparent().remove(r._r)
    q.runs[0].text = text
    return q


# Edition line
ed = [p for p in P if p.text.strip() == "Version 6F"]
assert len(ed) == 1
ed[0].runs[0].text = "Version 6G"

# A1  what the theorems prove (runs: text, [20], text, "However,", text)
p = para("General relativity predicts that gravitational collapse produces a singularity: a point of infinite density")
set_run(p, 0, "produces a singularity: a point of infinite density where the equations break down entirely. "
              "This prediction emerges from the Penrose-Hawking singularity theorems ",
              "produces a singularity. In the classical solutions, density and curvature grow without limit as "
              "the centre is approached and the equations break down. The Penrose-Hawking singularity theorems ")
set_run(p, 2, ", which prove that under certain reasonable conditions, singularities are mathematically unavoidable. ",
              " prove that under certain reasonable conditions this cannot be avoided, in a precise sense: the paths "
              "of falling particles and of light end after a finite time and cannot be continued. The theorems do "
              "not themselves prove that anything becomes infinite. ")
a1 = p

# B1  two meanings of one word, straight after A1
add_paragraph_after(a1,
    "Two meanings of one word. In mathematics, a singularity is a point where a function is undefined or stops "
    "behaving smoothly, such as 1/x at x = 0. The point is still part of the number line, and everything about it "
    "is learned from limits: how the function behaves as the point is approached. In general relativity, a "
    "singularity is not a point in spacetime at all. It is where spacetime stops: where the paths of particles and "
    "light end and cannot be continued. Physicists also separate coordinate singularities, which disappear in "
    "better coordinates (the event horizon is one), from curvature singularities, which do not. When this book "
    "says the singularity is a mathematical fixed point rather than a physical state, it means the first sense is "
    "being mistaken for the second.")

# B2  the relational point, after "Neither can be a starting point for anything, because neither exists."
p = para("The fixed-point parallel makes this precise")
assert p.text.rstrip().endswith("Neither can be a starting point for anything, because neither exists."), p.text[-80:]
add_paragraph_after(p,
    "There is a further point. Everything general relativity can say about a black hole, it says from outside, "
    "through relationships: its mass by how things orbit it, its spin by how it drags spacetime around it, its "
    "charge by its field. At a singularity there is nothing left to relate to, and nothing is defined. The absence "
    "of true singularities would be consistent with relationship being more fundamental than the things related. "
    "It would not prove it: other approaches to quantum gravity also remove singularities, and none has yet been "
    "observed or ruled out.")

# A5  heuristic (runs: "The uncertainty principle makes this ", "definitive", " ", "[21]", text)
p = para("The uncertainty principle makes this definitive")
set_run(p, 0, "makes this ", "points the same way")
set_run(p, 1, "definitive", "")
set_run(p, 4, "The uncertainty principle does not merely make singularities hard to achieve. "
              "It generates the precise resistance that prevents them.",
              "On the framework’s reading, the uncertainty principle does not merely make singularities hard "
              "to achieve; it generates the resistance that prevents them. This is a heuristic argument, not a "
              "calculation. A full answer needs a quantum theory of gravity.")

# A4  the universe as evidence (runs: text, [11], text)
p = para("The universe as evidence:")
set_run(p, 2, ". If true singularities formed inside them, singularities that represent literal endpoints of "
              "spacetime where causality breaks down, that breakdown would propagate. The universe continues. "
              "Structure persists. We are here to discuss black holes. This is not an anthropic tautology. It is a "
              "data point. The universe has been stress-tested by its most extreme objects and passed.",
              ". If true singularities formed inside them, they would be literal endpoints of spacetime. In classical "
              "general relativity, though, each one would sit behind its event horizon and could affect nothing "
              "outside. So the universe continuing is not, by itself, evidence against singularities. The evidence "
              "has to come from the black holes themselves. If the interior is a quantum structure rather than a "
              "singularity, faint gravitational-wave echoes should follow the main signal when black holes merge "
              "(see Appendix Element 19, Section F). That is the test the framework commits to.")

# A2  temporal boundary (one run)
p = para("The Penrose-Hawking singularity theorems establish that the singularity at the origin of the universe")
assert len(p.runs) == 1
p.runs[0].text = (
    "In the standard cosmological solutions, the singularity at the origin of the universe is a temporal boundary: "
    "not a location in space but the boundary of time itself. Inside a non-rotating black hole, the singularity is "
    "a temporal boundary in the same sense. The singularity theorems put both in the same class, because in both "
    "the paths of particles and light come to an end; they do not decide whether that end is a moment or a place. "
    "Real black holes rotate, and in the rotating solution the classical singularity is a ring that some paths can "
    "in principle avoid.")

# A3  the infalling observer (one run)
p = para("Inside the event horizon, the direction toward the singularity becomes timelike.")
assert len(p.runs) == 1
p.runs[0].text = (
    "Inside the event horizon of a non-rotating black hole, the direction toward the singularity becomes timelike. "
    "It is not a place you reach. It is a moment you cannot avoid. At the horizon itself, the infalling observer "
    "experiences no breakdown, no discontinuity, no local signal that anything unusual is happening. Closer in, "
    "tidal forces grow without limit, and that is where the classical description ends. What the framework "
    "questions is whether the physics ends with it.")

# A6  Element 14, fractal dimensions in the CMB (runs: lead-in, text, [12, 13], text, [14, 15], ".")
p = para("Fractal dimensions in the CMB.")
assert [r.text for r in p.runs][2] == "[12, 13]" and [r.text for r in p.runs][4] == "[14, 15]", [r.text for r in p.runs]
p.runs[1].text = (" Caruso and Oguri fitted the CMB spectrum with a Planck law generalized to a non-integer number of "
                  "spatial dimensions, 3 + \u03b5. They found \u03b5 of about 10\u207b\u2075 and read it as an upper limit on "
                  "how far space could differ from three dimensions, not as evidence that it does; a later analysis of "
                  "the same data bounds the deviation without settling its sign ")
p.runs[3].text = (". A different kind of fractal appears on the sky itself. Lines of equal temperature on CMB maps are "
                  "fractal curves, with a dimension between one and two, and the real maps match simulations of the "
                  "standard cosmological model. Fractal dimension here measures how crinkled a curve is, as for "
                  "Mandelbrot\u2019s coastline of Britain, not how many directions space has ")

d.core_properties.revision = (d.core_properties.revision or 0) + 1
d.save(DST)
print("wrote", os.path.basename(DST))
