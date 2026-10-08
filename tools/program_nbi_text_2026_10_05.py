# -*- coding: utf-8 -*-
"""NBI page (5 Oct 2026): factual corrections and the new section "From Information to Consciousness",
from drafts/nbi-information-and-consciousness-DRAFT.md (Michael's pasted text, corrected and sourced).
- Observer card: decoherence gives the working answer (any recording interaction), consistent with the
  vibration blog post; what stays open is why one outcome occurs.
- Human otoconia are calcite (aragonite is fish otoliths); simpler gravity sensors (statocysts) exist.
- The ribosome is about two-thirds RNA and its catalytic core is RNA; the genetic code has variants.
The "invite explanation" framing itself is left for Michael's decision. Run once."""
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "program-nbi.html")
s = open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


rep("<p>Quantum mechanics requires an observer to collapse the wavefunction but does not define what counts as an observer. A photon detector? A human? A rock? The theory is silent.</p>",
    "<p>Quantum mechanics speaks of observation but never defines an observer. A photon detector? A human? A rock? Decoherence gives the working answer: any physical interaction that records the information counts, a rock included. What it does not explain is why one outcome is the one that happens.</p>")

rep("Your inner ear contains otoliths: calcium carbonate crystals of a specific mineral form (aragonite rather than the more thermodynamically stable calcite) sitting on a bed of mechanosensitive hair cells.",
    "Your inner ear contains otoconia: tiny calcium carbonate crystals (calcite in humans; the otoliths of fish are aragonite) sitting on a bed of mechanosensitive hair cells.")
rep("The cells that deposit these crystals actively control which polymorph forms, producing aragonite to specification rather than the form that uncontrolled calcium carbonate chemistry would default to. The otolin protein matrix templates the crystal geometry at the molecular level before the crystal forms.",
    "The cells that deposit these crystals control which mineral form grows, its size and its shape. In fish, switching off a single matrix protein, starmaker, turns aragonite into calcite (Söllner et al., 2003). The otolin and otoconin proteins template the crystal at the molecular level before the crystal forms.")
rep("Balance is required from the first moment of movement. There is no viable intermediate state between a functional vestibular system and the absence of one in a mobile organism.",
    "Balance is required from the first moment of movement. Simpler gravity sensors do exist: jellyfish and many invertebrates balance with statocysts, a chamber holding a single mineral grain over sensory hairs.")
rep("The cells manufacture a specific crystal polymorph to a specification encoded in protein scaffolding that precedes the crystal. This is directed mineral deposition producing a precision instrument. How does an undirected process arrive at a specification before the structure it produces?",
    "The cells manufacture a specific crystal to a specification encoded in protein scaffolding that precedes the crystal. This is directed mineral deposition producing a precision instrument. Where does the specification come from, and what carries it from the simplest statocyst to the human inner ear?")

rep("with an error rate of roughly one mistake per 10,000 amino acids incorporated.",
    "with an error rate of roughly one mistake per 1,000 to 10,000 amino acids incorporated.")
rep("The ribosome itself is made of proteins. Those proteins were made by ribosomes. The code it reads is arbitrary",
    "The ribosome itself is about two-thirds RNA, and its catalytic heart, the site that joins amino acids, is RNA rather than protein (the 2009 Nobel Prize in Chemistry). Its proteins were made by ribosomes. The code it reads is largely arbitrary")
rep("A language requires that all parties use the same mapping. A mapping adopted by only some components produces nothing functional. The code had to be universal from the first instance in which it operated.",
    "A language requires that all parties use the same mapping. Yet the code is not frozen: mitochondria and some single-celled organisms reassign codons and still function. How a shared code arises, and how it can change while it is in use, is one of the open questions of the origin of life.")
rep("An arbitrary mapping that must be universal to function at all, implemented by a machine that is itself a product of the mapping. A partial version of the genetic code is not a simpler version of the genetic code. It is not a code. What process produces a convention before there are parties to the convention?",
    "A largely arbitrary mapping shared across life, implemented by a machine that is itself partly a product of the mapping. What process produces a convention before there are parties to the convention?")

CARD = """            <div style="background: #f0f2f5; border-radius: 8px; padding: 1.5rem; border-top: 4px solid {c};">
                <h4 style="color: var(--text-dark); margin-bottom: 0.6rem; font-size: 1rem;">{h}</h4>
                <p style="color: var(--text-dark); font-size: 0.9rem; line-height: 1.75; margin: 0;">{p}</p>
            </div>
"""
CARDS = [
    ("#005ba5", "Information became measurable",
     "In 1948 Claude Shannon published &ldquo;A Mathematical Theory of Communication&rdquo; and made information something that could be counted. Entropy, channel capacity, the bit: ideas built for telephone lines turned out to apply wherever a system reduces uncertainty, and that includes brains."),
    ("#8e0c45", "Consciousness as integrated information",
     "In 2004 Giulio Tononi proposed Integrated Information Theory (IIT): consciousness is the degree to which a system&rsquo;s information is both differentiated and unified, measured by a quantity he called &Phi;. It is one of the most influential theories in the field and one of the most disputed. In 2023 more than a hundred researchers signed an open letter calling it untestable in its current form, and in 2025 a large adversarial study in <em>Nature</em>, designed with both IIT&rsquo;s proponents and its main rival&rsquo;s, found that neither theory&rsquo;s predictions held up cleanly."),
    ("#1a5c2a", "Complexity tracks conscious level",
     "Researchers at the University of Sussex measured how varied and unpredictable brain signals are, using a compression-based measure. Signals became markedly less complex under general anesthesia, and more complex than ordinary waking under psychedelics. An information measure follows the level of consciousness in both directions, one of the clearest bridges yet between information theory and experience."),
    ("#7a5000", "A brain built for efficient flow",
     "Maps of the brain&rsquo;s wiring, including the Human Connectome Project, show networks that balance two costs: the expense of long connections and the need to move information quickly between distant regions. The result is a &ldquo;small world&rdquo; architecture that information theory would recognize as efficient. Whether that efficiency relates to consciousness, or only to good computation, is not yet known."),
    ("#005f6e", "Can a group know more than its members?",
     "Rock ants (<em>Temnothorax</em>) choosing a new nest avoid errors that individual ants make, and colonies outperform individuals when the choice is hard. Networked groups of people, connected in real time, have outperformed individual experts on some forecasting and diagnostic tasks. That is collective intelligence, well documented. Whether any collective is conscious is a separate question, and no study yet answers it."),
    ("#8B0000", "And machines?",
     "In 2022 a Google engineer said the company&rsquo;s LaMDA chatbot had become sentient. Most researchers saw fluent language rather than experience. A 2023 report by nineteen researchers (Butlin, Long and colleagues) turned the leading theories into a checklist of indicator properties and concluded that no current AI system is a strong candidate, while finding no obvious technical barrier to building one that would satisfy more of them. Fluency, it turns out, is not a measurement."),
]
SECTION = """<!-- From information to consciousness -->
<section class="content-section" id="information-and-consciousness" style="background: white;">
    <div class="section-inner">
        <div class="section-header" data-aos="fade-up">
            <h2>From Information to Consciousness</h2>
            <p>How the question took shape, and where it stands now</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 1.5rem;" data-aos="fade-up">
""" + "".join(CARD.format(c=c, h=h, p=p) for c, h, p in CARDS) + """        </div>

        <div style="margin-top: 1.5rem; background: #fff8e1; border-left: 4px solid #f1e303; border-radius: 0 8px 8px 0; padding: 1.25rem 1.75rem;" data-aos="fade-up">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #7a5000; font-weight: 700; margin-bottom: 0.4rem;">A claim that did not hold up</p>
            <p style="color: var(--text-dark); font-size: 0.92rem; line-height: 1.75; margin: 0;">Since 1998 the Global Consciousness Project, begun by Roger Nelson with support from the Institute of Noetic Sciences, has looked for links between world events and the output of random number generators around the world. Independent analyses have attributed its reported effects to how the events and time windows were chosen. It is here for a reason: an idea about consciousness has to survive exactly this kind of scrutiny, and this program&rsquo;s predictions are written to face it.</p>
        </div>

        <div style="margin-top: 1.5rem; padding: 1.75rem 2rem; background: #1a1d33; border-radius: 8px; color: white;" data-aos="fade-up">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #f1e303; margin-bottom: 0.5rem;">Where this leaves us</p>
            <p style="color: rgba(255,255,255,0.88); line-height: 1.9; font-size: 0.95rem; margin: 0;">Information can be measured. Consciousness, so far, cannot be measured directly. Every approach above is an attempt to close that gap. Our question is whether the information measures that already track consciousness in brains can be applied, by the same rules, to systems that are not brains. That is what the predictions on this page are designed to test.</p>
        </div>

        <p style="margin-top: 1.25rem; font-size: 0.8rem; color: var(--text-light); line-height: 1.7;"><strong>Sources:</strong> Shannon (1948), <em>Bell System Technical Journal</em>. Tononi (2004), <em>BMC Neuroscience</em>. Fleming et al. (2023), open letter, PsyArXiv. Cogitate Consortium (2025), <em>Nature</em>. Schartner et al. (2015), <em>PLOS ONE</em>; Schartner et al. (2017), <em>Scientific Reports</em>. Bullmore &amp; Sporns (2012), <em>Nature Reviews Neuroscience</em>. Van Essen et al. (2013), <em>NeuroImage</em>. Sasaki &amp; Pratt (2012), <em>Behavioral Ecology</em>; Sasaki et al. (2013), <em>PNAS</em>. Rosenberg et al. (2018), IEEE IEMCON. Butlin, Long et al. (2023), &ldquo;Consciousness in Artificial Intelligence,&rdquo; arXiv. Nelson et al. (2002), <em>Foundations of Physics Letters</em>; May &amp; Spottiswoode (2011), <em>Journal of Scientific Exploration</em>.</p>
    </div>
</section>

<!-- Current Status -->"""
rep("<!-- Current Status -->", SECTION)

open(P, "w", encoding="utf-8").write(s)
print("ok")
