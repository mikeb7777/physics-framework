# -*- coding: utf-8 -*-
"""Michael's decisions on the program pages (6 Oct 2026):
1. "85% of Shannon's maximum" stat: no source, removed (Consciousness Tuning and Elite Performance).
2. NBI "3 physical conditions" and "30+ NBI-candidate structures" stats: nothing published, removed.
3. NBI "Processes That Invite Explanation": updated. The question stays (where does the specification come
   from, and is selection the whole answer?); the claims that intermediates are not viable go, since
   precursors are documented (statocysts; rotary ATPase ancestry, Mulkidjanian et al. 2007).
4. Cognitive Extension phase dates: counted from funding instead of fixed calendar years.
Run once."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def patch(name, pairs):
    p = os.path.join(ROOT, name)
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        n = len(re.findall(a, s, flags=re.S)) if a.startswith("RE:") is False and False else s.count(a)
        assert n == 1, (name, a[:70], n)
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)
    print(name, len(pairs))


def drop_stat(value):
    return (re.compile(r'\s*<div class="stat-card">\s*<span class="stat-value">' + re.escape(value) + r'</span>\s*<span class="stat-label">[^<]*</span>\s*</div>'))


for name, values in [("program-consciousness-tuning.html", ["85%"]), ("program-elite-performance-overview.html", ["85%"]),
                     ("program-nbi.html", ["3", "30+"])]:
    p = os.path.join(ROOT, name)
    s = open(p, encoding="utf-8").read()
    for v in values:
        s, n = drop_stat(v).subn("", s)
        assert n == 1, (name, v, n)
    open(p, "w", encoding="utf-8").write(s)
    print(name, "stats removed:", values)

patch("program-nbi.html", [
    ("These processes are not selected for their mystery. They are selected because they are well-studied, uncontroversial in their description, and resistant to explanation by undirected trial and error without significant additional assumptions. The question is not whether they evolved. The question is whether the word \"evolved\" is doing the explanatory work it is being asked to do.",
     "These processes are not selected for their mystery. They are selected because they are well studied and uncontroversial in their description. Evolutionary biology has working accounts for each of them: simpler precursors, parts borrowed from other jobs, gradual refinement. The question is not whether they evolved. They did. The question is whether those accounts are complete: where the information that specifies each structure comes from, and whether selection on random variation is the whole of the answer or one part of it."),
    ("It achieves near-perfect thermodynamic efficiency: approximately 100% of the available free energy is captured in ATP bonds. No human-engineered motor approaches this.",
     "Single-molecule experiments put the efficiency of its rotary step close to 100% (Kinosita and colleagues). No human-engineered motor approaches this."),
    ("A rotary motor operating at near-100% thermodynamic efficiency with integrated quality control and self-repair. The intermediate states between no motor and a functional motor are not viable energy-producing states. What process produces a specification for a machine that does not yet exist?",
     "A rotary motor operating near 100% efficiency, with integrated quality control and self-repair. Its parts have relatives that do other jobs: the rotary ATPases appear to descend from a membrane protein-transport machine and an RNA-unwinding enzyme (Mulkidjanian et al., 2007). How did parts built for other work come to specify a machine that did not yet exist?"),
    ("These are four processes among thousands that share the same property: they require their complete functional form from the first moment they operate, the intermediate states are not viable, and the final form encodes a specification that precedes the structure it produces. The word \"evolved\" is not wrong. It is incomplete. It describes the timescale and the mechanism of selection. It does not describe where the specification comes from before the structure exists to be selected.",
     "These are four processes among thousands that share the same property: each encodes a specification that precedes the structure it produces, and each works with a precision we would call brilliant engineering if a person had done it. Biology has partial histories for all four: precursors, borrowed parts, simpler versions still alive today. The word \"evolved\" is not wrong. The question is whether it is complete. It describes the timescale and the mechanism of selection. Does it describe where the specification comes from before the structure exists to be selected?"),
])

patch("program-cognitive-extension-overview.html", [
    ("2026-2027 | $2-5M</p>", "Years 1 to 2 from funding | $2-5M</p>"),
    ("2027-2029 | $15-25M</p>", "Years 3 to 4, if Phase 1 meets its criteria | $15-25M</p>"),
    ("<p><strong>Phase 1 (2026-2027):</strong> $2-5M</p>", "<p><strong>Phase 1 (years 1 to 2 from funding):</strong> $2-5M</p>"),
    ("<p><strong>Phase 2 (2027-2029):</strong> $15-25M</p>", "<p><strong>Phase 2 (years 3 to 4):</strong> $15-25M</p>"),
    ("<p><strong>Ongoing (2029+):</strong> $15-30M annually</p>", "<p><strong>Ongoing (year 5 on):</strong> $15-30M annually</p>"),
])
