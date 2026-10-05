# -*- coding: utf-8 -*-
"""Consciousness Tuning page: factual corrections and a recent-research note (5 Oct 2026). Heading matches
the ~10 bits/s figure; the golden-ratio idea is attributed and posed as the question it is; the geometric
form constants are explained by visual-cortex dynamics (Kluver; Ermentrout & Cowan 1979; Bressloff et al.
2001) rather than claimed as perception of hidden signal; studies from 2023-2025 added. Run once."""
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "program-consciousness-tuning.html")
s = open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)


rep("<h2>The Forty Bits Problem</h2>", "<h2>The Ten Bits Problem</h2>")

rep("""<p>The brain's neural oscillations have been proposed to follow the golden ratio: the centers of neighboring EEG frequency bands sit roughly a factor of phi apart, an arrangement that keeps adjacent rhythms from locking into synchrony. This is the same constant that appears in sunflower seed packing. The brain may be organizing its frequency structure around the same mathematical attractor that appears wherever systems optimize constrained relationships. If so, consciousness tuning is not metaphor. It is literally tuning the oscillator to the attractor.</p>""",
    """<p>Pletzer, Kerschbaum and Klimesch (2010) proposed that the brain's rhythms follow the golden ratio: the centers of neighboring EEG frequency bands sit roughly a factor of phi apart, the most irrational ratio there is, which keeps adjacent rhythms from locking into synchrony. It is the same constant that appears in sunflower seed packing, wherever a system has to keep neighbors from interfering. So the question is a sharp one: is consciousness tuning literally tuning the oscillator toward that ratio? EEG can answer it.</p>""")

rep("""<span class="stat-label">Golden ratio organizing neural oscillation frequency relationships</span>""",
    """<span class="stat-label">Golden ratio proposed between neighboring EEG band centers (Pletzer et al. 2010)</span>""")

rep("""The phi-based frequency ratios in neural oscillations suggest the brain optimizes its frequency organization around a mathematical attractor.""",
    """If the proposed phi ratios between neural oscillation bands hold, the brain organizes its frequencies around a mathematical attractor.""")

rep("<h3>The Phenomenology Is Not Hallucination</h3>", "<h3>The Phenomenology Is Not Random</h3>")

rep("""What deep meditators and people in flow states report is strikingly consistent across individuals, cultures, and decades of research: geometric patterns, boundary dissolution,""",
    """What people report from deep meditation, flow and psychedelic states shares recurring features across individuals, cultures, and decades of research: boundary dissolution, geometric patterns (most often in psychedelic and flicker states),""")

rep("""<p>The framework's reading is that what people report seeing is not invented. Colors are more saturated, not fabricated. Movement is perceived in things that move microscopically but below normal detection threshold. The geometric patterns that consistently appear are the same patterns Turing derived from reaction-diffusion equations, the same patterns in Islamic geometric art, Celtic knotwork, and the phosphene patterns produced by pressure on closed eyes. These are the structural attractors of the visual processing system when certain filtering is removed. On this reading, they are always there, and normal perception edits them out.</p>""",
    """<p>Why do the same geometric shapes keep appearing? Heinrich Kl&uuml;ver catalogued them in the 1920s as "form constants": lattices, tunnels, spirals, cobwebs. In 1979 Ermentrout and Cowan showed that they follow from the wiring of the visual cortex itself. When its input-driven activity loosens, the cortex settles into Turing-type patterns, and the map from eye to cortex turns those stripes into the tunnels and spirals people describe (extended by Bressloff and colleagues in 2001). That is why the same shapes turn up in pressure phosphenes, migraine auras, flicker and psychedelics, and echo through geometric art traditions. They are real structure: the structure of the perceiving system. Which raises the question this program asks. When the filter loosens, how much of what comes through is signal from outside, and how much is the shape of the instrument? Vividness alone cannot tell them apart. Measurement can.</p>""")

rep("""<p>Advanced meditators report the same phenomenology. Long-term flow practitioners report the same phenomenology.""",
    """<p>Advanced meditators report much of the same phenomenology. So do long-term flow practitioners.""")

rep("""The therapeutic effects, the documented success in treating depression,""",
    """The therapeutic effects, the results in clinical trials for depression,""")

RECENT = """
        <div style="margin-top: 1.25rem; padding: 1.5rem 1.75rem; background: white; border-radius: 8px; border-left: 4px solid #8e0c45;" data-aos="fade-up">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #8e0c45; font-weight: 700; margin-bottom: 0.75rem;">New in the research, 2023 to 2025</p>
            <ul style="font-size: 0.9rem; color: var(--text-dark); line-height: 1.75; margin: 0; padding-left: 1.2rem;">
                <li><strong>The ten bits.</strong> Zheng and Meister (<em>Neuron</em>, 2024) put conscious throughput at about 10 bits per second against roughly a billion bits per second of sensory input, a ratio of about a hundred million to one.</li>
                <li><strong>Psilocybin and the self-model network.</strong> Siegel and colleagues (<em>Nature</em>, 2024) scanned people repeatedly before, during and after psilocybin. Brain networks desynchronized, most of all the default mode network, and a link between the hippocampus and that network stayed weaker for weeks.</li>
                <li><strong>Training versus medication.</strong> In a randomized trial of 276 adults with anxiety disorders, eight weeks of mindfulness-based stress reduction did as well as the drug escitalopram (Hoge et al., <em>JAMA Psychiatry</em>, 2023).</li>
                <li><strong>Breathwork.</strong> A meta-analysis of randomized trials found breathwork lowered self-reported stress, with small to moderate effects (Fincham et al., <em>Scientific Reports</em>, 2023).</li>
                <li><strong>The theories themselves.</strong> A large adversarial test of the two leading theories of consciousness, designed with both camps, found that neither theory's predictions held up cleanly (Cogitate Consortium, <em>Nature</em>, 2025). The field's central question is still open. See the <a href="program-nbi.html#information-and-consciousness" style="color: #8e0c45; font-weight: 600;">NBI program</a> for how information measures track conscious level.</li>
            </ul>
        </div>"""

rep("""Josipovic, Z. (2014), neural correlates of nondual awareness, Annals of the New York Academy of Sciences.</p>
        </div>""",
    """Josipovic, Z. (2014), neural correlates of nondual awareness, Annals of the New York Academy of Sciences. Pletzer, B., Kerschbaum, H. &amp; Klimesch, W. (2010), golden ratio in brain oscillations, Brain Research. Ermentrout, G. B. &amp; Cowan, J. D. (1979), Biological Cybernetics. Bressloff, P. C. et al. (2001), Philosophical Transactions of the Royal Society B.</p>
        </div>""" + RECENT)

open(P, "w", encoding="utf-8").write(s)
print("ok")
