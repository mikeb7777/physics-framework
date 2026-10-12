#!/usr/bin/env python3
"""Factual corrections to the blog posts, 12 October 2026.

Every replacement must match exactly once, so a re-run after the edits are in
place stops with an error instead of applying twice.
Run from the repository root:  python3 tools/blog_corrections_2026_10_12.py
"""
import sys

NOTE_STYLE = ('background:#eef2f6; border-left:4px solid #5a6878; padding:0.9rem 1.1rem; '
              'border-radius:4px; font-size:0.95rem;')


def note(text):
    return ('<p style="%s"><strong>Correction, October 2026:</strong> %s</p>' % (NOTE_STYLE, text))


class Page:
    def __init__(self, path):
        self.path = path
        self.text = open(path, encoding='utf-8').read()

    def rep(self, old, new, count=1):
        n = self.text.count(old)
        if n != count:
            sys.exit('%s: expected %d match(es), found %d for: %r' % (self.path, count, n, old[:90]))
        self.text = self.text.replace(old, new)

    def add_note(self, content_id, text):
        tag = '<div class="post-content collapsed" id="%s-content">' % content_id
        self.rep(tag, tag + '\n\n        ' + note(text) + '\n')

    def save(self):
        open(self.path, 'w', encoding='utf-8').write(self.text)


blog = Page('blog.html')
R = blog.rep

# ---------------------------------------------------------------- Cosmic Conversation (Aug 2025)
blog.add_note('cosmic-conversation',
    'Several statements in this post have been corrected. Van Helmont died in 1644 and his account of the willow '
    'was published in 1648, so the experiment cannot be dated to the 1640s; he was also half right about water, which '
    'supplies much of a plant&rsquo;s hydrogen and oxygen, and missed the carbon from the air. The claim that a tree '
    'takes 95% of its substance from CO&#8322; was replaced with the dry-weight breakdown. Hydrogen was made in the '
    'Big Bang, not in stars. &ldquo;Ashes to ashes&rdquo; comes from the Book of Common Prayer, not the Bible. '
    'The Betelgeuse distance is now given as a range, measurement is no longer described as a conscious '
    '&ldquo;collapse&rdquo;, and the universe&rsquo;s entropy history is stated correctly.')
R("Sometime in the 1640s, Jan Baptist van Helmont weighed out 200 pounds",
  "In the early seventeenth century, the Flemish physician Jan Baptist van Helmont (whose account was published "
  "after his death, in 1648) weighed out 200 pounds")
R("He drew the wrong conclusion, deciding the extra 164 pounds had arrived out of water alone, and he did not "
  "trouble to weigh the leaves that fell each autumn. But he had put a balance where an opinion used to be, and "
  "that's why we still know his name. The answer he could not see was in the air above the pot.",
  "He concluded that the extra 164 pounds had come from the water alone, and he did not trouble to weigh the "
  "leaves that fell each autumn. He was half right: water really does supply much of a plant's hydrogen and "
  "oxygen. But he had put a balance where an opinion used to be, and that's why we still know his name. What he "
  "could not see was that the carbon, about half the dry weight of the tree, came from the air above the pot.")
R("A tree gets roughly 95% of its physical substance from carbon dioxide in the air, from the sky, not the ground. "
  "Through photosynthesis it pulls CO₂ out of the atmosphere and reassembles those carbon atoms into wood, leaves, "
  "bark, and roots. The soil provides minerals, but the mass is literally air made solid.",
  "Roughly half of a tree's dry weight is carbon, and nearly all of that carbon came from carbon dioxide in the "
  "air, from the sky, not the ground. Through photosynthesis the tree pulls CO₂ out of the atmosphere and "
  "reassembles those carbon atoms into wood, leaves, bark, and roots. Most of the rest is hydrogen and oxygen from "
  "water and CO₂, and the soil's minerals add only a few percent. The carbon is literally air made solid.")
R("Your physical mass is, in a very direct and measurable sense, atmospheric carbon reorganized by biological "
  "information processing. You are concentrated air, shaped by life.",
  "The carbon in your body, about a fifth of your weight and the backbone of every organic molecule in you, is in "
  "a very direct and measurable sense atmospheric carbon reorganized by biological information processing. You "
  "are, in large part, air and water shaped by life.")
R("Those oxygen molecules (O₂) you just inhaled are precisely the same oxygen molecules that exist throughout the "
  "universe. The nitrogen (N₂) making up 78% of the air you breathe is identical to nitrogen in distant nebulae. "
  "These aren't copies. They're not \"Earth versions\" of cosmic molecules. They're the <em>exact same stuff</em>.",
  "The oxygen atoms in the O₂ you just inhaled are identical to oxygen atoms anywhere in the universe. The "
  "nitrogen (N₂) making up 78% of the air you breathe is made of the same nitrogen atoms found in distant "
  "nebulae. These aren't copies. They're not \"Earth versions\" of cosmic atoms. They're the <em>exact same "
  "stuff</em>.")
R("When a star explodes in a supernova, it creates oxygen and nitrogen through nuclear fusion. Those atoms drift",
  "Massive stars forge oxygen by nuclear fusion and scatter it into space when they explode as supernovae; "
  "nitrogen is made mostly by fusion in stars of various sizes and shed into space too. Those atoms drift")
R("The oxygen you breathe right now might have been forged in a stellar explosion before Earth even existed.",
  "The oxygen atoms you breathe right now were forged inside stars, many of them scattered by stellar "
  "explosions, before Earth even existed.")
R("The Standard Model of Physics completely accounts for every component of biological systems.",
  "Everything in a living body is made of the particles and forces that physics describes.")
R("The light from Betelgeuse left that star 642 years ago. When you see it, you're directly receiving information "
  "transmitted across 642 light-years of space through the cosmic electromagnetic field.",
  "The light from Betelgeuse left that star roughly 550 to 700 years ago (estimates of its distance vary). When "
  "you see it, you're directly receiving information transmitted across more than five hundred light-years of "
  "space through the cosmic electromagnetic field.")
R("The Bible says \"ashes to ashes, dust to dust.\" As we've seen,",
  "The burial service of the Book of Common Prayer says \"earth to earth, ashes to ashes, dust to dust,\" "
  "echoing Genesis 3:19. As we've seen,")
R("Your carbon mass came from atmospheric CO₂ captured by plants.",
  "The carbon in your body came from atmospheric CO₂ captured by plants.")
R("The atoms in your body were forged in stars. The fields permeating",
  "Nearly all the atoms in your body heavier than hydrogen were forged in stars. The fields permeating")
R("When you measure or observe anything, you're collapsing wave functions, extracting information from quantum "
  "superposition states, affecting the very reality you observe.",
  "Any measurement is a physical interaction: it extracts information from the system and, at the quantum scale, "
  "disturbs the very state it records. It takes a detector or some other physical interaction, not a conscious "
  "mind.")
R("The universe spent 13.8 billion years organizing itself from high-entropy uniformity to low-entropy complexity "
  "specifically to create conditions where conscious information processing like yours could exist.",
  "Over 13.8 billion years the universe went from a smooth, nearly uniform hot state to stars, planets and minds, "
  "building local complexity while total entropy kept rising, and that history produced the conditions where "
  "conscious information processing like yours could exist.")

# ---------------------------------------------------------------- Raise Your Vibration (Aug 2026)
R("Richard Feynman put it most simply: \"Nature does not know what you're looking at.\"",
  "Richard Feynman is widely quoted making the same point most simply: \"Nature does not know what you're "
  "looking at.\"")

# ---------------------------------------------------------------- Never the Present (Sep 2026)
R("which is the correction mentioned earlier in this article.", "which is the correction discussed later in this article.")
R("precisely what that's and is not.", "precisely what that is and is not.")

# ---------------------------------------------------------------- What Most People Think Science Is (Jul 2026)
blog.add_note('science-institution',
    'Einstein&rsquo;s first dissertation was withdrawn, not rejected. The Peters and Ceci result is restated '
    '(three of the twelve papers were recognised as resubmissions, and eight of the other nine were rejected). The '
    '&ldquo;28 percent&rdquo; figure for reviewer bias was replaced by the odds ratios the 2017 PNAS study reports. '
    'The peer-review awareness figure was removed because the cited survey questioned researchers, not the public. '
    'Slipher&rsquo;s 1912 measurement showed Andromeda approaching, not receding. Hoyle&rsquo;s &ldquo;Big Bang&rdquo; '
    'is no longer described as mockery. The Scopus percentages could not be confirmed and were replaced. The 10 percent '
    'authorship figure is now attributed to its actual source and time frame.')
R("His earlier doctoral thesis had been rejected.",
  "His first doctoral dissertation, submitted in 1901, had been withdrawn; the one that earned his doctorate was "
  "accepted in 1905.")
R("Researchers who study peer review estimate that only 30 percent of the public understands what the term "
  "actually means.<sup><a href=\"#sci-ref-5\">[5]</a></sup>",
  "Researchers themselves doubt how much the label guarantees: in a 2009 Sense About Science survey of more than "
  "4,000 researchers, only about a third thought peer review capable of detecting both plagiarism and "
  "fraud.<sup><a href=\"#sci-ref-5\">[5]</a></sup>")
R("Nine of the 12 were rejected. Reviewers cited serious methodological flaws",
  "Only three of the 12 were recognized as resubmissions, and eight of the other nine were rejected. Reviewers "
  "cited serious methodological flaws")
R("More recent research found that papers from prestigious institutions received 28 percent higher acceptance "
  "rates and better reviewer scores when institutional affiliations were visible rather than blinded.",
  "More recent research found that reviewers who could see author names and affiliations were roughly 1.6 times "
  "as likely, in odds, to recommend acceptance of papers from famous authors and from top universities as "
  "reviewers who could not (about 2.1 times for papers from top companies).")
R("Vesto Slipher measured the recession velocity of the Andromeda nebula in 1912 and 1913. By 1917 he had "
  "measured recession velocities for 25 spiral nebulae and presented systematic evidence of a general expansion.",
  "Vesto Slipher measured the radial velocity of the Andromeda nebula in 1912 and 1913, finding it approaching "
  "us. By 1917 he had measured velocities for 25 spiral nebulae, most of them receding, a pattern that later "
  "proved to be evidence of a general expansion.")
R("In a 2005 study, 10 percent of researchers surveyed admitted to assigning authorship inadequately at least "
  "once in their career.<sup><a href=\"#sci-ref-113\">[113]</a></sup>",
  "In a 2005 survey of U.S. scientists, 10 percent admitted to inappropriately assigning authorship credit in the "
  "previous three years.<sup><a href=\"#sci-ref-119\">[119]</a></sup>")
R("<span id=\"sci-ref-118\">",
  "<span id=\"sci-ref-119\">[119] Martinson, B. C., Anderson, M. S., and de Vries, R. (2005). Scientists behaving "
  "badly. <em>Nature</em> 435, 737&ndash;738.</span><br>\n          <span id=\"sci-ref-118\">")
R("Fred Hoyle coined &#8220;Big Bang&#8221; in 1949 as mockery; the cosmic microwave background confirmed "
  "expansion in 1965.",
  "Fred Hoyle, an opponent of the theory, coined &#8220;Big Bang&#8221; on BBC radio in 1949 (he later said the "
  "name was not meant as an insult); the cosmic microwave background, discovered in 1965, supported the Big Bang "
  "picture.")
R("A 2024 study found that Scopus, one of the major scholarly databases, incorrectly categorizes 99 percent of "
  "retracted papers.<sup><a href=\"#sci-ref-68\">[68]</a></sup> A separate analysis found that 31.7 percent of "
  "retracted papers in the literature are not marked as retracted in Scopus at all.<sup><a "
  "href=\"#sci-ref-68\">[68]</a></sup>",
  "A 2024 comparison of seven scholarly databases found that retracted papers are indexed and labelled "
  "inconsistently: a paper marked as retracted in one database is often not marked in another, so checking a "
  "single source is not enough.<sup><a href=\"#sci-ref-68\">[68]</a></sup>")

# ---------------------------------------------------------------- Below the Threshold (Jun 2026)
blog.add_note('below-threshold',
    'The Cambrian dates and wording were tightened (about 540 million years ago; most, not every, major animal body '
    'plan), and the quantum-biology paragraph no longer says that long-lived coherence in photosynthesis is '
    '&ldquo;established&rdquo;: it is reported, and its functional role is still debated.')
R("550 million years ago, after roughly three billion years of single-celled life, every major animal body plan "
  "that exists today appeared in the fossil record within a geologically instantaneous 20-million-year window.",
  "About 540 million years ago, after roughly three billion years of single-celled life, most major animal body "
  "plans that exist today appeared in the fossil record within a geologically brief window of roughly "
  "20 million years.")
R("Quantum biology has established that coherence effects in living systems persist far longer than thermal noise "
  "should allow. Photosynthesis achieves near-perfect energy transfer efficiency through quantum superposition "
  "across multiple pathways simultaneously.",
  "Quantum biology has reported coherence effects in living systems that persist longer than simple "
  "thermal-noise estimates would predict, though how much they matter functionally is still debated. Energy "
  "transfer in photosynthetic complexes is remarkably efficient, and quantum coherence across multiple pathways "
  "has been proposed as part of the reason.")

# ---------------------------------------------------------------- Non-Biological Intelligence (Apr 2026)
blog.add_note('non-biological-intelligence',
    'The passage on sexual reproduction no longer says there was &ldquo;no viable intermediate state&rdquo;: '
    'evolution reached it through intermediate stages. The objection to Integrated Information Theory is now '
    'stated as the one actually made in the literature.')
R("all functioning together from the first instance. There is no viable intermediate state. A reward architecture "
  "for sexual reproduction provides no fitness benefit until the other side has the complementary architecture. "
  "Selection cannot drive toward a payoff that only exists when both partners have what neither has yet. The "
  "reward system therefore had to be present as a structural feature before selection had anything to work with.",
  "working together. Evolution built this gradually, through intermediate stages such as external fertilization "
  "and coevolving signals and preferences, so the claim is not that it appeared all at once. The point is "
  "narrower: the finished system is a coupled pair, and a reward architecture on one side pays off only when the "
  "other side has a matching one. Selection can assemble such pairs step by step, but the result is a mechanism "
  "in which valuation states do real coordinating work.")
R("runs into the power grid problem: by that measure, the electrical grid would be conscious at a very high level.",
  "draws the objection, pressed by Scott Aaronson among others, that the theory's own measure rates some simple, "
  "inert systems, such as a suitably connected grid of logic gates, as highly conscious.")

# ---------------------------------------------------------------- Thinking About Thinking (Mar 2026)
blog.add_note('thinking-about-thinking',
    'Two quotations were removed or replaced because neither can be traced to its supposed author: &ldquo;Logic will '
    'get you from A to B&hellip;&rdquo; (Einstein) and &ldquo;You have power over your mind&hellip;&rdquo; (Marcus '
    'Aurelius, replaced with Meditations 8.47). The Egyptian and Hermetic sources are described more precisely, and '
    'the claim about time perception in flow is now stated as a hypothesis.')
R(" Here he was even more direct: \"Logic will get you from A to B. Imagination will take you everywhere.\"", "")
R("<em>\"You have power over your mind, not outside events. Realize this, and you will find strength.\"</em> This "
  "is not a statement about attitude.",
  "<em>\"If you are pained by any external thing, it is not this thing that disturbs you, but your own judgment "
  "about it. And it is in your power to wipe out this judgment now.\"</em> (Meditations 8.47, in a modernized "
  "version of George Long's translation.) This is not a statement about attitude.")
R("The Hermetic tradition that grew from this same Egyptian soil gave us the phrase <em>as above, so below</em>,",
  "The Hermetic tradition, which grew from Greco-Egyptian soil, is the source of the phrase <em>as above, so "
  "below</em> (it comes from the Emerald Tablet, first known in medieval Arabic),")
R("as documented in the Pyramid Texts and Hermetic literature.", "as documented in the Pyramid Texts.")
R("When that suspension occurs, time dilation follows naturally, because normal time perception is partly a "
  "construction of the DMN's predictive narrative. Without it, duration becomes more direct, closer to what's "
  "actually there. Time dilation in flow is not a side effect or an illusion. It's what unfiltered present-moment "
  "experience actually feels like from the inside.",
  "One hypothesis is that when that suspension occurs, the sense of time changes, because normal time perception "
  "is partly a construction of the DMN's predictive narrative. Without it, duration may feel more direct. On "
  "this reading, the stretched sense of time in flow is not a side effect or an illusion but what less filtered "
  "present-moment experience feels like from the inside. That is a hypothesis, not an established finding.")

# ---------------------------------------------------------------- Fuzzy Logic / ocean of fields (Feb 2026)
R("What the diagram does not show, and what's almost never mentioned, is that the sand pattern is a cross-section "
  "of a three-dimensional acoustic field at the surface of the plate. The field continues above the plate in a "
  "complete geometry. Vertical planes, nested cylindrical shells, compound ribbons. The sand cannot reveal any of "
  "this structure, and it has never been directly visualized.",
  "What the diagram does not show, and what's almost never mentioned, is the air above the plate. The moving plate "
  "drives a three-dimensional sound field there, predicted to have nodal structure in the form of vertical "
  "planes, nested cylindrical shells and compound ribbons. The sand cannot reveal any of it, and it is almost "
  "never drawn.")
R("The 2D sand pattern on the left has been presented as the phenomenon since 1787. The teal structure on the "
  "right is the predicted 3D nodal surface rising above the plate. The pattern is a cross-section of the "
  "structure, not the structure itself.",
  "The 2D sand pattern on the left has been presented as the phenomenon since 1787. The teal structure on the "
  "right is the predicted 3D nodal surface in the air above the plate. The sand pattern maps the plate itself; it "
  "is related to that structure but is not a slice through it.")
R("The two-dimensional pattern is not the phenomenon. It's where the phenomenon intersects the plate surface. The "
  "rest of the field extends right above it, following the same wave equation that produces the pattern below. "
  "Apply the Helmholtz equation with the boundary conditions the sand pattern provides and the full "
  "three-dimensional structure falls out of the mathematics immediately. It has always been mathematically "
  "accessible. Nobody asked for it because the cross-section was satisfying enough that the question stopped "
  "there.",
  "The sand pattern is a map of the plate, not of the whole phenomenon. The plate's motion drives a sound field in "
  "the air above it, and that field obeys the Helmholtz equation with the plate's vibration as its boundary "
  "condition. In principle the three-dimensional structure can be calculated from the plate's motion; the sand "
  "pattern gives only the nodal lines, so the full calculation also needs the plate's mode shape. The mathematics "
  "has long been available. Few people asked for the picture because the pattern on the plate was satisfying "
  "enough that the question stopped there.")
R("The aurora bands visible at the Earth's edge are the 3D nodal structure of magnetohydrodynamic waves made "
  "visible by ionospheric plasma.",
  "The aurora bands visible at the Earth's edge trace the field-aligned structure of the magnetosphere, made "
  "visible where charged particles strike the upper atmosphere.")
R("So has anyone ever seen a real field in full? Once, and most of us have filed it under weather. The aurora "
  "borealis is the full coupled field geometry made visible by its interaction with ionospheric plasma. The "
  "bright curtains are antinodal regions of a magnetohydrodynamic wave structure. The dark spaces between them "
  "trace the nodal surfaces where the parallel field component reaches zero. Nature has been displaying this every "
  "night in high latitudes.",
  "So has anyone ever seen a real field in full? Not quite, but the aurora comes closest, and most of us have "
  "filed it under weather. Charged particles guided along the magnetic field lines strike the upper atmosphere and "
  "make it glow, so the curtains trace the field-aligned structure of the coupled magnetosphere and ionosphere. "
  "The bright curtains and dark gaps are not a simple picture of nodes and antinodes, but they are a direct view "
  "of structure that no toroid diagram shows. Nature has been displaying this every night in high latitudes.")
R("the 62.64 Hz 8th Schumann harmonic,",
  "the higher Schumann modes (spaced roughly 6.5 Hz apart, so one falls within a few hertz of 60 Hz),")
R("The 8th harmonic of the Schumann resonance sits at 62.64 Hz, within 2.64 Hz of the grid frequency, overlapping "
  "spatially with it across an entire continent, continuously.",
  "The Schumann resonances are not exact multiples of the 7.83 Hz fundamental: the observed modes step upward by "
  "roughly 6.5 Hz (7.83, 14.3, 20.8, 27.3, 33.8 Hz and so on), so extrapolating puts a higher mode within a few "
  "hertz of the grid frequency, though modes that high are weak and hard to observe. The grid field overlaps "
  "spatially with them across an entire continent, continuously.")
blog.rep("<strong>Correction, September 2026:</strong>", "<strong>Correction, September 2026:</strong>")  # anchor check
R("kept drawing the toroid.</p>\n\n        <h3>Fields Are Not Empty Space With Lines Drawn Through It</h3>",
  "kept drawing the toroid.</p>\n\n        " + note(
      'The aurora description above replaces an earlier claim that auroral curtains are the nodes and antinodes of '
      'magnetohydrodynamic waves. The Schumann-mode figures were also corrected, but the label on the field-structure '
      'figure still shows the old 62.64 Hz value and will be redrawn.') +
  "\n\n        <h3>Fields Are Not Empty Space With Lines Drawn Through It</h3>")

# ---------------------------------------------------------------- The Veteran's Edge: no factual changes needed

# ---------------------------------------------------------------- What Is an Interstellar Object (Dec 2025)
blog.add_note('interstellar-objects',
    'The history of quasars was corrected: the extragalactic interpretation was settled in 1963, not rejected. The '
    'Roman Space Telescope launched on August 30, 2026, so &ldquo;launching in 2027&rdquo; was updated. The '
    'cosmic-ray-processing analysis of 3I/ATLAS is now identified as a single preprint that other measurements '
    'dispute.')
R("When spectra revealed emission lines that matched no known element, the extragalactic explanation was rejected "
  "because it implied luminosities that seemed impossibly high.",
  "When spectra revealed emission lines that matched no known element, the puzzle lasted until 1963, when Maarten "
  "Schmidt recognized the lines of 3C 273 as ordinary hydrogen shifted far to the red. That put the object "
  "billions of light-years away and implied luminosities that many astronomers found hard to accept.")
R("They were supermassive black holes at the centers of distant galaxies,",
  "They were powered by supermassive black holes at the centers of distant galaxies,")
R("The Roman Space Telescope, launching in 2027, should dramatically increase our detection rate.",
  "The Roman Space Telescope, which launched on August 30, 2026, should dramatically increase our detection rate.")
R("Recent analysis of 3I/ATLAS suggests that its anomalous",
  "One recent analysis of 3I/ATLAS (a preprint, and disputed by other measurements) suggests that its anomalous")

# ---------------------------------------------------------------- The Speed of Novelty (Nov 2025)
blog.add_note('information-velocity',
    'The JWST item listed among the framework&rsquo;s &ldquo;predictions&rdquo; was written after the observations it '
    'cites, so it is now labelled as consistent with them, not as a confirmed prediction. The Einstein remark was '
    'reworded, the &ldquo;transient hypofrontality&rdquo; description was hedged, hydrogen was excluded from '
    '&ldquo;atoms forged in stars&rdquo;, and &ldquo;ashes to ashes&rdquo; was attributed to the Book of Common Prayer.')
R("Einstein famously said that a physicist was \"effectively dead\" by the age of 30. In his era, he was right.",
  "Einstein is often quoted as saying that a person who has not made a great contribution to science by the age of "
  "thirty never will. In his era, that was close to the truth.")
R("temporarily deactivates. This is referred to as \"transient hypofrontality.\"",
  "becomes less active, according to one hypothesis known as \"transient hypofrontality.\" The evidence is still "
  "limited.")
R("<h4>COSMIC Framework Predictions</h4>", "<h4>What the COSMIC Framework Would Expect</h4>")
R("This has testable predictions:</p>",
  "This leads to testable expectations. The first was written after the JWST observations, so it counts as "
  "consistent with them, not as a prediction:</p>")
R("should be 4-5× standard predictions ✓ (JWST confirms)",
  "should be 4-5× standard predictions (consistent with JWST observations, which came first)")
R("Every atom in your body was forged in stellar explosions. The carbon in your DNA,",
  "Nearly every atom in your body heavier than hydrogen was forged in stars, many of them scattered by stellar "
  "explosions. The carbon in your DNA,")
R("The Bible says \"ashes to ashes, dust to dust.\" You ARE the earth,",
  "The burial service of the Book of Common Prayer says \"earth to earth, ashes to ashes, dust to dust,\" "
  "echoing Genesis. You ARE the earth,")

# ---------------------------------------------------------------- Prime numbers (Oct 2025)
blog.add_note('prime-numbers',
    'The claim that no other number system has unique factorization was wrong (some do and some do not), '
    'factoring is believed hard but has not been proven hard, and Shor&rsquo;s algorithm factors large integers, '
    'not primes.')
R("No other number system has this property.",
  "Not every number system has this property, which is part of what makes the integers special.")
R("Prime multiplication is easy; prime factorization is exponentially hard.",
  "Prime multiplication is easy; prime factorization is believed to be hard, since no efficient classical "
  "algorithm is known (its hardness has not been proven).")
R("Shor's algorithm shows quantum computers can factor primes efficiently,",
  "Shor's algorithm shows that a sufficiently large quantum computer could factor large integers into primes "
  "efficiently,")

# ---------------------------------------------------------------- Isolation May Be Required (Dec 2025)
blog.add_note('isolation',
    'This post had arithmetic and physics errors that are now fixed. The chance a 1,000-year civilization is active '
    'now is 1 in 10 million, not 1 in 10,000 or 100,000; the 73 km/s recession applies to galaxies 3.26 million '
    'light-years away, not to stars in our own galaxy, which is not expanding; the Hubble radius is not the event '
    'horizon; the energy example, laser, plasma and galaxy-fraction figures were recalculated; and the claims that '
    'interstellar absorption, cosmic rays and quantum noise make radio contact impossible were removed, because '
    'radio waves cross the galaxy with little absorption and ordinary telescopes detect far weaker signals. The '
    '10,000-light-year figure is a practical horizon for particular transmitters and receivers, not a law of '
    'physics, and the rate and power tables are order-of-magnitude illustrations, not derived results.')
R("= 0.0001 = 0.01%</p>", "= 0.0000001 = 0.00001%</p>")
R("<p>That's a one in 100,000 chance that any given civilization is alive right now.</p>",
  "<p>That's a one in 10 million chance that any given civilization is alive right now.</p>")
R("<p>Expected number of contactable civilizations within our reach right now: less than 0.01</p>",
  "<p>Expected number of contactable civilizations within our reach right now: about 0.000007 (70 planets × 1 in "
  "10 million)</p>")
R("We'd have to wait about 3 million years between opportunities for contact, on average.",
  "We'd have to wait about 140 million years between opportunities for contact, on average (a 1,000-year window "
  "divided by 0.000007).")
R("Do the math: At about 4,200 megaparsecs (13.7 billion light-years), recession velocity equals the speed of light. "
  "Beyond that distance, galaxies recede faster than light can travel through the expanding space between us.",
  "Do the math: At about 4,100 megaparsecs (roughly 13.4 billion light-years), recession velocity equals the speed "
  "of light. This distance is called the Hubble radius, and galaxies beyond it are receding faster than light "
  "right now.")
R("This distance is called the cosmic event horizon. Any civilization beyond it's permanently unreachable: no "
  "matter how long we wait, no signal they send will ever reach us. The expanding space between us grows faster "
  "than light can traverse it.",
  "The Hubble radius is not the same thing as the cosmic event horizon. Light from galaxies receding faster than "
  "light can still reach us, because the Hubble radius itself grows as the universe expands. The true limit is "
  "the cosmic event horizon, at roughly 16 billion light-years in today's measure of distance: a signal sent from "
  "beyond it today will never reach us, however long we wait.")
R("So immediately, the entire universe beyond 13.7 billion light-years is not just difficult to contact; it's "
  "physically impossible to contact.",
  "So the universe beyond roughly 16 billion light-years is not just difficult to contact; for anything sent "
  "today, it's physically impossible to contact.")
R("They're receding from us at about 73 km/s due to cosmic expansion (about 0.024% the speed of light, negligible "
  "relativistic effects, but the distance matters enormously).",
  "Stars in our galaxy move relative to one another at tens of kilometers per second, in random directions, so "
  "this civilization might be moving away from us at, say, 30 km/s (about 0.01% the speed of light, negligible "
  "relativistic effects, but the distance matters enormously). Cosmic expansion does not act inside a "
  "gravitationally bound galaxy.")
R("Greetings from the Kepler-442 civilization.", "Greetings from a civilization 1,000 light-years away.")
R("Our message reaches Kepler-442... but here's the problem.", "Our message reaches them... but here's the problem.")
R("Let's say their civilization lasts 2,000 years total (optimistic). When they sent the signal, they were perhaps "
  "500 years into their technological phase. By the time our response arrives, they're 1,500 years into it.",
  "Let's say their civilization lasts 3,000 years total (very optimistic). When they sent the signal, they were "
  "perhaps 500 years into their technological phase. By the time our response arrives, they're 2,500 years into "
  "it.")
R("But that civilization is now 2,000 years older than when they first contacted us. If their civilization lasted "
  "only 2,000 years total, they went extinct right as their response arrived at Earth.",
  "But that civilization is now 3,000 years older than when they first contacted us. If their civilization "
  "lasted 3,000 years total, it ended about 500 years before their response arrived at Earth.")
R("They've been extinct for 1,000 years.</p>", "They've been extinct for 1,500 years.</p>")
R("Forty human generations, entire civilizations rising and falling, for a single back-and-forth exchange.",
  "Eighty human generations, entire civilizations rising and falling, for a single back-and-forth exchange: forty "
  "for each leg.")
R("even that becomes: Two generations per exchange if we're optimistic about human lifespan and civilization "
  "continuity. Fifty generations to have the conversation your distant ancestors started.",
  "even that becomes: Four generations per exchange (a 100-year round trip) if we're optimistic about human "
  "lifespan and civilization continuity, so a conversation your great-grandparents started would be finished by "
  "your great-grandchildren.")
R("Remember that civilization receding at 73 km/s? That recession velocity causes a Doppler shift,",
  "Remember that civilization moving relative to us at tens of kilometers per second? Relative motion causes a "
  "Doppler shift,")
R("For electromagnetic signals (radio waves, light), recession causes redshift. The frequency decreases. A radio "
  "signal broadcast at 1,420 MHz (the famous hydrogen line frequency, a common choice for interstellar "
  "communication) arrives shifted to a lower frequency.",
  "For electromagnetic signals (radio waves, light), recession causes redshift (the frequency decreases) and "
  "approach causes blueshift. A radio signal broadcast at 1,420 MHz (the famous hydrogen line frequency, a common "
  "choice for interstellar communication) arrives shifted to a slightly lower or higher frequency.")
R("At 73 km/s recession velocity: - Frequency shift: Δf/f ≈ v/c = 73/300,000 = 0.024% - Signal transmitted at "
  "1,420 MHz arrives at 1,419.65 MHz",
  "At 30 km/s recession velocity: - Frequency shift: Δf/f ≈ v/c = 30/300,000 = 0.01% - Signal transmitted at "
  "1,420 MHz arrives at about 1,419.86 MHz")
R("It's arriving at a different frequency.</p>",
  "It's arriving at a different frequency. Real searches correct for known motion and scan for drift, so this is "
  "a complication rather than a barrier.</p>")
R("And for civilizations at greater distances with higher recession velocities, the shift becomes dramatic: - At "
  "10% light speed: signal shifts by 10% - At 50% light speed: signal shifts by 50% - A radio signal becomes an "
  "infrared signal becomes a microwave signal",
  "And for galaxies at cosmological distances, which really do recede with the expansion of space, the shift "
  "becomes dramatic: - At 10% light speed: signal shifts by about 10% - At 50% light speed: signal shifts by "
  "about 42% (relativistic Doppler) - A radio signal arrives at a much lower radio frequency")
R("The message arrives in a completely different part of the electromagnetic spectrum than it was sent.",
  "The message arrives at a very different frequency than it was sent.")
R("arrives as a drawn-out \"whoooosh\" spread across seconds or even minutes.",
  "arrives as a drawn-out \"whoooosh\" spread across tens of milliseconds to seconds, depending on the frequency "
  "band and the distance.")
R("A 1-millisecond pulse spreads to several seconds", "A broadband 1-millisecond pulse at 1.4 GHz spreads to tens of "
  "milliseconds")
R("You'd need sophisticated de-dispersion algorithms, but you can't design those unless you know the exact "
  "properties of the interstellar medium the signal traveled through, which varies along every line of sight.",
  "Undoing the smear (de-dispersion) is routine in pulsar astronomy: the delay follows a known law and its "
  "strength can be fitted from the data itself, so it costs computing effort rather than new physics.")
R("A powerful signal that starts at 100% strength: - Loses 10-30% to absorption in the first 100 light-years - "
  "Loses another 20-40% in the next 100 light-years - By 1,000 light-years, perhaps 20-30% of the original signal "
  "survives",
  "At the radio frequencies SETI uses (roughly 1-10 GHz), the interstellar medium is almost transparent over "
  "1,000 light-years, so absorption is a minor loss there. It matters far more for infrared, optical, ultraviolet "
  "and X-ray signals, and for very low radio frequencies.")
R("Molecular clouds block certain frequencies entirely", "Dense molecular clouds absorb some wavelengths")
R("Combined with inverse square law, your signal is now 50,000 times weaker than it started, shifted in "
  "frequency, and smeared in time.",
  "Combined with the inverse square law, your signal is about a million times weaker than it was at one "
  "light-year, shifted in frequency, and smeared in time.")
R("At 10% light speed, time dilation factor ≈ 1.005. Their clocks run 0.5% slower from our perspective.",
  "At 10% light speed, time dilation alone is a factor of about 1.005 (their clocks run 0.5% slower from our "
  "perspective). For a receding source the growing distance stretches arrival times further, for a total stretch "
  "(the relativistic Doppler factor) of about 1.1.")
R("A 1-second pulse they transmit arrives as a 1.005-second pulse", "A 1-second pulse they transmit arrives as a "
  "1.1-second pulse")
R("- 50% light speed: time dilation factor ≈ 1.15 (15% slower) - 90% light speed: time dilation factor ≈ 2.3 "
  "(messages take 2.3× longer than intended)",
  "- 50% light speed: total stretch factor ≈ 1.7 - 90% light speed: total stretch factor ≈ 4.4 (messages take "
  "4.4× longer than intended)")
R("- Frequency-shifted to 1,419.65 MHz (you're not listening there) - Signal strength reduced by 50,000× (inverse "
  "square + absorption) - 1-millisecond pulses dispersed into 3-second smears (unreadable) - Buried in cosmic "
  "microwave background noise - Time-dilated by 0.024% (minimal at this velocity, but adds to timing errors)",
  "- Frequency-shifted by roughly 0.01% (you have to search for it) - Signal strength reduced about a "
  "millionfold relative to one light-year (inverse square) - 1-millisecond pulses dispersed into smears tens of "
  "milliseconds long (correctable, but only if you know to try) - Competing with cosmic microwave background and "
  "galactic noise")
R("Even with perfect error-correction coding, there's a hard physical limit. Beyond a certain distance, no amount "
  "of clever engineering can recover the message because the physics of spacetime itself has destroyed the "
  "information.",
  "Even with perfect error-correction coding, there's a limit set by transmitter power, receiver size and noise. "
  "Beyond a certain distance the message falls below the noise floor. Larger transmitters, bigger receivers and "
  "longer integration times push that distance outward, but at rising cost.")
R("Con: Artificially generating detectable gravitational waves is IMPOSSIBLE - Limit: Cannot generate artificial "
  "signals at all",
  "Con: Artificially generating detectable gravitational waves is far beyond any known or foreseeable technology - "
  "Limit: no practical way to generate an artificial signal")
R("Diffraction spreads beam to 31 AU diameter at 1,000 light-years (wider than Neptune's orbit) - Con: Pointing "
  "accuracy needed: 10⁻¹⁵ radians (quantum uncertainty makes this impossible) - Con: Still absorbed 60-85% by "
  "interstellar dust",
  "Diffraction spreads beam to about 31 AU diameter at 1,000 light-years (roughly the radius of Neptune's orbit) - "
  "Con: Pointing accuracy needed: about 10⁻⁸ radians to hit a star's habitable zone, which is extremely demanding "
  "but not forbidden by physics - Con: Optical and infrared light is partly absorbed and scattered by interstellar "
  "dust")
R("Cosmic Rays (high-energy particles): - 10²¹ cosmic rays per cm² over 1,000 light-year path - Each creates "
  "particle shower, triggers false detections - Ionizes interstellar medium, creating scattering - Effect: 1-10% "
  "random bit corruption over 1,000 light-years",
  "Cosmic Rays (high-energy particles): - They do not alter a radio signal in flight - They can trigger false "
  "detections in sensitive detectors - Effect: a source of noise at the receiver, not corruption of the message in "
  "transit")
R("Molecular Clouds (opaque gas/dust): - 10-100 light-years across, completely opaque to most radiation - Effect: "
  "10-20% chance of cloud blocking signal over 1,000 light-years - When it happens: total signal loss for "
  "months/years",
  "Molecular Clouds (dense gas/dust): - 10-100 light-years across, opaque to visible light but largely "
  "transparent to radio waves - Effect: block optical and infrared signals along many lines of sight")
R("- Over 1,000 light-years: 3×10¹⁹ - 3×10²⁰ electrons per cm² - Effect: Dispersion spreads 1ms pulses to seconds, "
  "limiting information rate to <1 kbps",
  "- Over 1,000 light-years: roughly 10¹⁹ - 10²⁰ electrons per cm² - Effect: Dispersion spreads 1ms broadband "
  "pulses to tens of milliseconds at radio frequencies, which can be corrected")
R("Heisenberg Uncertainty: - Cannot measure both frequency AND timing with arbitrary precision - Effect: "
  "Fundamental limit on timing precision: ~10⁻¹⁵ seconds",
  "Time-Frequency Uncertainty: - A pulse cannot be arbitrarily short and arbitrarily narrow-band at once - "
  "Effect: sets the trade-off between pulse length and bandwidth, not a barrier at the timescales discussed here")
R("Photon Shot Noise: - Light is discrete photons, not continuous waves - For weak signals, counting statistics "
  "create noise - Effect: Signal must be >>10¹⁸ photons/second/cm² to distinguish from noise",
  "Photon Shot Noise: - Light is discrete photons, not continuous waves - For weak signals, counting statistics "
  "create noise - Effect: longer integration times and bigger collecting areas average it down")
R("Vacuum Fluctuations: - \"Empty\" space has quantum foam - Virtual particles pop in/out of existence - Energy "
  "density: ~10⁻⁹ J/m³ - Effect: Signals weaker than ~10⁻²⁴ W/m² indistinguishable from quantum noise at 1,000 "
  "light-years",
  "Vacuum Fluctuations: - Quantum vacuum noise sets a floor for any detector - Effect: that floor is far below the "
  "signal levels discussed here; radio telescopes routinely detect sources much weaker than 10⁻²⁴ W/m²")
R("Total energy: ~3×10²⁶ joules (0.001% of Sun's lifetime output)",
  "Total energy: ~3×10²⁰ joules (about a millionth of a second of the Sun's output)")
R("10,000 light-years: - Information rate: <100 bps theoretical - Energy cost: ~100 GW continuous (entire modern "
  "civilization's power output) - Methods: All severely degraded - Interference: Guaranteed multiple transits, "
  "thick plasma screens - Channel capacity approaching zero - PHYSICALLY IMPRACTICAL",
  "10,000 light-years: - Information rate: <100 bps theoretical - Energy cost: ~100 GW continuous (entire modern "
  "civilization's power output) - Methods: All severely degraded - Interference: Multiple transits of dense "
  "gas and plasma - Channel capacity approaching zero for a transmitter and receiver of this size - IMPRACTICAL "
  "WITH ANY PLAUSIBLE TECHNOLOGY")
R("Beyond 10,000 light-years: - Inverse square law: signal weakened by 10⁸ - Interstellar absorption: 99.9%+ "
  "absorbed - Dispersion: microsecond pulses spread to hours - Cosmic interference: continuous corruption - "
  "Quantum noise floor: signal indistinguishable from vacuum fluctuations - Shannon limit: channel capacity ≈ 0 - "
  "PHYSICALLY IMPOSSIBLE",
  "Beyond 10,000 light-years: - Inverse square law: signal weakened by 10⁸ relative to one light-year - "
  "Absorption and scattering: significant at many wavelengths, though radio stays comparatively clear - "
  "Dispersion: larger, but correctable - Shannon limit: channel capacity falls toward zero for a given "
  "transmitter and receiver - EXTREMELY DEMANDING, AND BEYOND ANY PLAUSIBLE TRANSMITTER")
R("That means 99% of our galaxy's volume is beyond the coherence horizon for information transmission.",
  "That means about 96% of our galaxy's volume is beyond that horizon for information transmission.")
R("You could develop perfect technology, unlimited energy, and it wouldn't matter. The laws of physics, quantum "
  "mechanics, thermodynamics, information theory, impose this limit.",
  "With plausible transmitters and receivers, the cost of communicating rises steeply with distance. Better "
  "technology moves the horizon outward, but each step costs far more.")
R("- Cosmic rays: clean data → random corruption (entropy increases)",
  "- Cosmic rays: false triggers at the detector (noise increases)")
R("Beyond ~10,000 light-years, the entropy cost exceeds any civilization's energy budget.</p>",
  "Beyond ~10,000 light-years, the energy cost likely exceeds what any civilization would spend.</p>")
R("The hard limit isn't technological. It's thermodynamic.", "The limit is practical rather than absolute, and "
  "it comes from energy and entropy costs.")
R("Some scientists have proposed the \"Dark Forest\" hypothesis,",
  "Some writers have proposed the \"Dark Forest\" hypothesis, a name taken from Liu Cixin's 2008 novel,")
R("In fact, we observe exactly this pattern: We've never found planets in globular clusters despite searching. "
  "Nearly all the exoplanets we've discovered orbit stars in low-density regions like ours. The data confirms it: "
  "habitable places are isolated.",
  "In fact, we see hints of this pattern: only a handful of planets have been found in globular clusters despite "
  "searching (the best known, PSR B1620-26 b in M4, orbits a pulsar and a white dwarf), while nearly all the "
  "exoplanets we've discovered orbit stars in low-density regions like ours. That is partly an observational "
  "bias, since dense regions are hard to survey, so it supports the idea without confirming it.")
R("(0.000001% of the galaxy's diameter)", "(0.05% of the galaxy's diameter)")
R("Probability two civilizations exist simultaneously = 0.01% (one in 10,000 chance).",
  "Probability two civilizations exist simultaneously = 0.00001% (about one in 10 million, for a 1,000-year "
  "window).")
R("Cosmic event horizons make ~90% of the observable universe permanently unreachable",
  "The cosmic event horizon makes about 95% of the observable universe unreachable for anything sent today")
R("Inverse square law weakens signals by factors of 50,000× or more", "Inverse square law weakens signals a "
  "million-fold at 1,000 light-years")
R("Interstellar absorption removes 70-80% of signal strength", "Interstellar absorption removes much of the "
  "signal at infrared, optical and X-ray wavelengths")
R("Shannon limit: channel capacity approaches zero beyond ~1,000 light-years",
  "Shannon limit: for a given transmitter and receiver, channel capacity falls toward zero with distance")
R("Quantum limits (Heisenberg uncertainty, photon shot noise, vacuum fluctuations)",
  "Quantum noise (photon shot noise and vacuum fluctuations set a detector floor, not a barrier at these "
  "distances)")
R("Hard boundary: ~10,000 light-years maximum (1% of galaxy) for ANY method - Even unlimited technology and energy "
  "cannot overcome these limits",
  "Practical horizon: roughly 10,000 light-years (about 4% of the galaxy's area) under the assumptions used here - "
  "Larger transmitters and receivers push the horizon outward, at rising cost")
R("Within our 50-light-year bubble, we've already discovered extraordinary things. We know about planets where it "
  "rains molten glass (HD 189733b, 63 light-years away). Planets with iron rain (WASP-76b).",
  "Within a few hundred light-years, we've already discovered extraordinary things. We know about planets where "
  "it rains molten glass (HD 189733b, about 64 light-years away). Planets with iron rain (WASP-76b, about 640 "
  "light-years away).")
R("an asteroid that's essentially a giant ball of metal and possibly the exposed iron-nickel core",
  "a metal-rich asteroid and possibly the exposed iron-nickel core")

blog.save()

# ---------------------------------------------------------------- The Institution and the Idea (standalone page)
page = Page('blog-post-institution-and-the-idea.html')
page.rep('    <!-- SECTION 1: OPENING -->',
         '    <section class="prose-section"><div class="prose-inner">' +
         note('Chandrasekhar&rsquo;s 1930s work was on the maximum mass of a white dwarf, not black holes directly. '
              'Einstein&rsquo;s first lecture course was given in Bern in 1908, before the Zurich post. The 11 percent '
              'cancer-biology figure comes from Amgen (Begley and Ellis, 2012), not the Reproducibility Project, and the '
              'economics figure is the 61 percent reported by Camerer and colleagues in 2016. The arXiv endorsement '
              'description was updated to the current rules.') +
         '</div></section>\n\n    <!-- SECTION 1: OPENING -->')
page.rep('Presented calculations on stellar collapse and black hole formation.',
         'Calculated the maximum mass of a white dwarf, implying that heavier stars must collapse further.')
page.rep('he received his first academic position, an associate professorship at the University of Zurich. His first '
         'lecture was attended by three students, two of whom were personal friends.',
         'he received his first paid academic position, an associate professorship at the University of Zurich. His '
         'first lecture course, given in Bern in 1908 as an unpaid lecturer, drew three listeners, among them two '
         'friends from the patent office.')
page.rep('Landmark cancer biology studies that replicated fully (Reproducibility Project)',
         'Landmark cancer biology studies that replicated (Begley and Ellis, Amgen, 2012)')
page.rep('<span class="stat-number">~50%</span>', '<span class="stat-number">61%</span>')
page.rep('Estimated replication rate in neuroscience and economics',
         'Experimental economics studies that replicated (Camerer et al., 2016)')
page.rep('requires endorsement from someone already inside the system who has published within the last two years. '
         'A closed referral network.',
         'requires a new author to have either an institutional email plus a previously accepted paper, or a '
         'personal endorsement from an established arXiv author in the same area (since January 2026 an institutional '
         'email alone is no longer enough). A closed referral network for anyone outside an institution.')
page.save()
print('corrections applied')
