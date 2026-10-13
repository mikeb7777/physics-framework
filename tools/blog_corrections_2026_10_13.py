#!/usr/bin/env python3
"""Follow-up corrections, 13 October 2026.

Brings the wisdom-tradition passages in line with the research notes (traditions
differ, antiquity is provenance not evidence, 'Native American' covers hundreds of
nations) and fixes how Landauer's principle is described in the Isolation post.
Each replacement must match exactly once.
Run from the repository root:  python3 tools/blog_corrections_2026_10_13.py
"""
import sys

path = 'blog.html'
text = open(path, encoding='utf-8').read()


def rep(old, new):
    global text
    n = text.count(old)
    if n != 1:
        sys.exit('expected 1 match, found %d for: %r' % (n, old[:90]))
    text = text.replace(old, new)


# ---------------------------------------------------------------- Cosmic Conversation
rep("<h3>Ancient Wisdom, Modern Physics</h3>", "<h3>Old Ideas, Examined With Modern Tools</h3>")
rep("This understanding isn't new. It's ancient wisdom that modern physics is starting to echo.",
    "Versions of this idea are old. Several traditions reached something like it, each in its own terms. They differ, "
    "and none is proved by physics, but they are worth setting beside it as ancient hypotheses examined with modern "
    "tools.")
rep("This isn't mysticism. It's recognition that individual consciousness is universal information processing "
    "localized in biological systems.",
    "The framework reads this as the claim that individual consciousness is universal information processing "
    "localized in biological systems; that reading is ours, not the tradition's.")
rep("This isn't religion. It's physics. There's no boundary where \"you\" end and \"universe\" begins.",
    "The physics above is compatible with that: there's no boundary where \"you\" end and \"universe\" begins.")
rep("Native American traditions speak of humans as part of nature, not separate from it. This isn't primitive "
    "animism. It's accurate observation that biological processes use the same constituents and follow the same laws "
    "as all natural processes.",
    "Many Indigenous traditions, which differ widely across hundreds of nations, treat people as part of a web of "
    "relations that includes animals, rivers and mountains, and some treat those as persons or ancestors. \"Primitive "
    "animism\" is a label applied from outside. The physics here is compatible with the relational part; it says "
    "nothing about the rest.")
rep("This isn't mystical nonsense. It's recognition that human consciousness follows universal principles, "
    "processes universal information, and participates in cosmic self-organization.",
    "The framework reads this as consistent with human consciousness following universal principles and processing "
    "universal information; again, that reading is ours.")
rep("Every wisdom tradition already knew this truth: we are not separate from the universe. Modern physics is "
    "finally catching up, providing the mathematical and experimental framework to understand what ancient teachers "
    "intuited.",
    "These ideas differ, and the likeness is partial: Brahman, the Tao, mana and kinship are not the same thing. What "
    "they share is a refusal to treat the self as separate from the world. Modern physics is compatible with that "
    "refusal; it does not prove any of them, and an idea's age is where it comes from, not evidence for it.")
rep("and the universe&rsquo;s entropy history is stated correctly.</p>",
    "and the universe&rsquo;s entropy history is stated correctly. The closing section on wisdom traditions was also "
    "reworded: the traditions differ, &ldquo;Native American&rdquo; covers hundreds of nations, and an idea&rsquo;s "
    "age is not evidence for it.</p>")

# ---------------------------------------------------------------- The Speed of Novelty
rep("<h4>The Ancient Wisdom Was Right</h4>", "<h4>Old Ideas, Same Direction</h4>")
rep("This understanding isn't new; it's ancient wisdom that modern physics is starting to echo:",
    "Versions of this idea are old. The traditions differ, and none is proved by physics, but several point the same "
    "way:")
rep("Individual consciousness IS universal information processing localized in biological systems. Buddhist",
    "The framework reads that as individual consciousness being universal information processing localized in "
    "biological systems. Buddhist")
rep("Native American traditions speak of humans as part of nature, not separate from it. Biological processes use "
    "the same constituents following the same laws.",
    "Many Indigenous traditions, which differ widely across hundreds of nations, treat people as part of a web of "
    "relations with other living things.")
rep("Every wisdom tradition already knew: we are not separate from the universe. Modern physics just provides the "
    "mathematical framework to understand it.",
    "What they share is a refusal to treat the self as separate from the world. Modern physics is compatible with "
    "that refusal; it does not prove any of them.")
rep("&ldquo;ashes to ashes&rdquo; was attributed to the Book of Common Prayer.</p>",
    "&ldquo;ashes to ashes&rdquo; was attributed to the Book of Common Prayer. The wisdom-tradition passage was "
    "reworded because the traditions differ and an idea&rsquo;s age is not evidence for it.</p>")

# ---------------------------------------------------------------- Thinking About Thinking
rep("The Egyptian priests understood it. The Stoics understood it.",
    "Egyptian thought distinguished perceiving from expressing. The Stoics trained attention.")
rep("Exactly what Einstein demonstrated, though separated by four thousand years",
    "A similar order to the one Einstein described, though separated by four thousand years")
rep("the claim about time perception in flow is now stated as a hypothesis.</p>",
    "the claim about time perception in flow is now stated as a hypothesis, and the claim that Egyptian priests "
    "&ldquo;understood&rdquo; the idea was softened.</p>")

# ---------------------------------------------------------------- Isolation May Be Required
rep("Landauer's Principle (from COSMIC Framework Element 2): - Erasing 1 bit costs minimum energy: E = kT ln(2) ≈ "
    "3×10⁻²¹ joules - Transmitting 1 bit",
    "Landauer's Principle (from COSMIC Framework Element 2): - Erasing 1 bit costs minimum energy: E = kT ln(2) ≈ "
    "3×10⁻²¹ joules; the cost applies to erasure, and reversible computing can in principle avoid it - Communicating "
    "1 bit reliably costs at least about kT ln(2) at the receiver's noise temperature, a Shannon-limit result "
    "separate from Landauer's - Transmitting 1 bit")
rep("Thermodynamic constraints (Landauer's principle: fighting entropy requires energy)",
    "Thermodynamic constraints (Landauer's principle for erasure; a minimum energy per bit for communication)")
rep("the rate and power tables are order-of-magnitude illustrations, not derived results.</p>",
    "the rate and power tables are order-of-magnitude illustrations, not derived results. Landauer&rsquo;s principle "
    "is now described as applying to erasure, not to transmission.</p>")

open(path, 'w', encoding='utf-8').write(text)
print('follow-up corrections applied')
