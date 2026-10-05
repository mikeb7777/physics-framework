# -*- coding: utf-8 -*-
"""AI-Mediated Cognitive Extension, overview and pilot: factual corrections and recent research (5 Oct 2026).
- Working memory is about four chunks (Cowan 2001) and does vary with fluid intelligence; the ~7 stat goes.
- "Validation" becomes "test" in program language (claims standard IC2-COM-001). Nav links stay.
- The Landauer test as written (heat from erasure read by cerebral thermometry) is not measurable: kT ln 2 is
  about 3e-21 J per bit at body temperature against a 20 W brain. Restated as energy per bit, measured
  metabolically, against Landauer's floor.
- Named "prospective" universities and meditation centers removed (no false affiliations).
- Pilot contrast bugs fixed: white text and a yellow link on a white column.
Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def patch(name, pairs):
    p = os.path.join(ROOT, name)
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)
    print(name, len(pairs))


RECENT_OVERVIEW = """
        <div class="info-box" data-aos="fade-up" style="border-left-color: #1a1d33; background: white;">
            <h3>New in the Research, 2023 to 2025</h3>
            <p style="color: var(--text-dark);">The first large studies of everyday AI use have arrived since this program was written. They bear directly on its predictions.</p>
            <ul>
                <li><strong>Who gains most.</strong> In a field study of 5,179 customer-support agents, an AI assistant raised productivity about 15% on average, and most for the least experienced; the most skilled gained little (Brynjolfsson, Li and Raymond, <em>Quarterly Journal of Economics</em>, 2025). That supports the novice side of the predicted U-shaped curve. The veteran side is still untested.</li>
                <li><strong>The jagged frontier.</strong> Consultants using GPT-4 did better and faster on tasks inside the model's competence, and worse on a task just outside it (Dell'Acqua et al., Harvard Business School working paper, 2023). Extension works where the tool is strong and misleads where it is not.</li>
                <li><strong>Offloading has a cost.</strong> A survey of 319 knowledge workers found that the more people trusted the AI, the less critical thinking they reported doing (Lee et al., CHI 2025). In a small MIT study of essay writing, people who used ChatGPT showed the weakest brain connectivity of three groups and recalled less of their own essays (Kosmyna et al., 2025, preprint, 54 participants).</li>
            </ul>
            <p style="color: var(--text-dark); margin-bottom: 0;">Together these sharpen the program's central distinction: extension that frees working memory for adaptive reasoning, versus substitution that lets the reasoning lapse. The protocols measure both.</p>
        </div>"""

patch("program-cognitive-extension-overview.html", [
    ("constrained by working memory limitations: approximately 4 to 7 items regardless of intelligence or expertise.",
     "constrained by working memory: about four chunks of information at a time."),
    ("""<span class="stat-value">~7</span>""", """<span class="stat-value">~4</span>"""),
    ("""<span class="stat-label">Working Memory Items</span>""", """<span class="stat-label">Working Memory Chunks</span>"""),
    ("Human working memory holds roughly four chunks (older estimates said seven, plus or minus two) regardless of intelligence, education, or expertise. This constraint persists across all cognitive activities and represents a fundamental architectural limitation of biological neural substrates.",
     "Human working memory holds roughly four chunks (Cowan, 2001; the older estimate was seven, plus or minus two). Capacity varies a little between people and tracks fluid intelligence, but no one holds forty. Expertise does not add slots; it packs more into each chunk. The limit holds across cognitive activities and is an architectural feature of biological neural substrates."),
    ("<p>From the COSMIC Framework's information-theoretic perspective, consciousness represents information processing through a biological neural substrate with severe bandwidth limitations.",
     "<p>The program's working proposal is that consciousness is information processing through a biological neural substrate with severe bandwidth limits."),
    ("<p>Reducing risk through incremental validation before major hardware investment</p>",
     "<p>Reducing risk by testing each step before major hardware investment</p>"),
    ("<p><strong>Objective:</strong> Validate framework principles using existing display technology</p>",
     "<p><strong>Objective:</strong> Test the program's principles using existing display technology</p>"),
    ("<li>Validated neuroplastic adaptation timeline</li>", "<li>Neuroplastic adaptation timeline measured against prediction</li>"),
    ("after Phase 1 validation</p>", "if Phase 1 meets its criteria</p>"),
    ("<!-- Validation Pathways -->", "<!-- Lines of test -->"),
    ("<h2>Multiple Independent Validation Pathways</h2>", "<h2>Four Independent Lines of Test</h2>"),
    ("<p>Convergent evidence from diverse methodologies strengthens framework confidence</p>",
     "<p>Each can come out for or against the proposal on its own</p>"),
    ("<h3>2. Autonomic Control Validation</h3>", "<h3>2. Autonomic Control Tests</h3>"),
    ("<li><strong>Consciousness Transitions:</strong> Sleep, meditation produce measurable heat from information erasure</li>",
     "<li><strong>Energy per Bit:</strong> Landauer's principle sets a floor of about 3 &times; 10<sup>&minus;21</sup> joules per erased bit at body temperature, far too small to read directly in a 20-watt brain. The test is how far above that floor the brain runs, from metabolic cost against information processed</li>"),
    ("<li><strong>Landauer Principle:</strong> Heat dissipation correlates with information reorganization amount</li>",
     "<li><strong>Consciousness Transitions:</strong> Prediction: energy per bit changes measurably between waking, sleep and meditation</li>"),
    ("<li><strong>Technology:</strong> Cerebral thermometry, fNIRS, EEG complexity measures</li>",
     "<li><strong>Technology:</strong> PET and calibrated fMRI for metabolic rate, fNIRS, EEG complexity measures</li>"),
    ("<h3>4. Psychedelic Research Validation</h3>", "<h3>4. Psychedelic Research Tests</h3>"),
    ("<li><strong>Geometric Patterns:</strong> Mathematical structures match information-optimized predictions</li>",
     "<li><strong>Geometric Patterns:</strong> Prediction: reported structures match information-optimized forms, beyond the form constants already explained by visual-cortex dynamics</li>"),
    ("<li><strong>DMN Suppression:</strong> Depth correlates with geometric complexity",
     "<li><strong>DMN Suppression:</strong> Prediction: depth correlates with geometric complexity"),
    ("<li>Autonomic control validation studies</li>", "<li>Autonomic control studies</li>"),
    ("<li>Landauer principle testing</li>", "<li>Energy-per-bit (Landauer floor) studies</li>"),
    ("<li>Cross-domain validation expansion</li>", "<li>Cross-domain testing</li>"),
    ("<li>Neuroscience Lead (Validation Studies)</li>", "<li>Neuroscience Lead (Test Studies)</li>"),
    ("detailed experimental protocols, validation methodologies,", "detailed experimental protocols, test methods,"),
    ("<li>Complete experimental protocols for 5 validation pathways</li>", "<li>Complete experimental protocols for 5 lines of test</li>"),
    ("""                <li><strong>Technology:</strong> fMRI during controlled sessions, pattern documentation</li>
            </ul>
        </div>""",
     """                <li><strong>Technology:</strong> fMRI during controlled sessions, pattern documentation</li>
            </ul>
        </div>""" + RECENT_OVERVIEW),
])

patch("program-cognitive-extension-pilot.html", [
    ("Autonomic control validation tests whether neurofeedback accelerates the predicted adaptation curve.",
     "The autonomic control test asks whether neurofeedback accelerates the predicted adaptation curve."),
    ("<p>The Landauer principle prediction is the most directly framework-connected: information erasure during cognitive processing should produce measurable heat signatures consistent with the theoretical minimum. This connects the cognitive extension research directly to the framework's claim that information processing is physical.</p>",
     "<p>The Landauer prediction is the most directly framework-connected. Landauer's principle sets the minimum energy to erase one bit: about 3 &times; 10<sup>&minus;21</sup> joules at body temperature. That is far too small to read as heat in a brain running on about 20 watts, so the test is energy per bit: how far above Landauer's floor the brain operates, measured from metabolic cost against information processed, and whether that changes with tool use, sleep and meditation. It connects the cognitive extension research directly to the principle that information is physical.</p>"),
    ("Participants across all three validation protocols", "Participants across all three test protocols"),
    ("IRB submissions for all validation protocols.", "IRB submissions for all test protocols."),
    ("Beta Testing &amp; Validation</h4>", "Beta Testing &amp; Trials</h4>"),
    (">Validation study design and analysis.", ">Test study design and analysis."),
    ("limited validation scope.", "limited test scope."),
    ("""<p style="margin-top: 0.75rem; color: rgba(255,255,255,0.9);">The three validation protocols also recruit from specific populations:</p>""",
     """<p style="margin-top: 0.75rem; color: var(--text-dark);">The three test protocols also recruit from specific populations:</p>"""),
    ("""<a href="mailto:ic2.info@proton.me" style="color: #f1e303; font-weight: 600;">""",
     """<a href="mailto:ic2.info@proton.me" style="color: #005f6e; font-weight: 600;">"""),
    (""">Prospective University Partners</p>""", """>Partners We Are Seeking</p>"""),
    ("UC Berkeley, Stanford, UCSF, MIT for fMRI access, sleep research collaboration, statistical support, and IRB oversight. Spirit Rock and Insight Meditation Society for experienced meditator recruitment and DMN modulation expertise.",
     "University neuroscience and sleep laboratories for fMRI access, sleep research, statistical support, and IRB oversight. Meditation centers for experienced-meditator recruitment and default-mode-network expertise."),
])
