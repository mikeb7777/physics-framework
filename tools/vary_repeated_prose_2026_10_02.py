# -*- coding: utf-8 -*-
"""Vary overused prose (2 Oct 2026). Michael: find phrases used more than twice and
restate them or replace them with something new. Found with a phrase count over the
visible text of every page (8+ word runs used 3+ times). Left as they are on purpose:
prediction and result statements (the record must read the same everywhere), legal
language, citations and titles. Run once."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def ed(f, pairs):
    s = open(f, encoding="utf-8").read()
    for a, b in pairs:
        if a not in s and b in s:
            continue
        assert s.count(a) == 1, (f, s.count(a), a[:60])
        s = s.replace(a, b)
    open(f, "w", encoding="utf-8").write(s)


# 1. Blog: each post's closing line, in its own words (was the same sentence 14 times)
LEAD = {
    "never-the-present": "The next post, and each test result as it comes in, can come to you by email.",
    "raise-your-vibration": "Want the next post, and the results of the tests behind ideas like this one?",
    "science-institution": "See how this idea fares in the institutions, one result at a time.",
    "below-threshold": "Results like this one are where the framework gets checked. Get each one by email.",
    "first-contact": "New posts and test results, every couple of months.",
    "non-biological-intelligence": "The NBI program reports its results here as they come in.",
    "thinking-about-thinking": "More on how minds handle information, and every test result, by email.",
    "seeing-clearly": "One theory, followed the whole way, every couple of months.",
    "veterans-edge": "Results from the Elite Performance program will be reported as they arrive.",
    "interstellar-objects": "If another visitor from outside the solar system turns up, there will be a post about it.",
    "information-velocity": "The next post, and the data that tests these ideas.",
    "prime-numbers": "Speculation like this, and the tests that keep it honest, by email.",
    "isolation": "The Fermi question is slow to answer. New posts arrive every couple of months.",
    "cosmic-conversation": "The conversation continues in the next post.",
}
OLD = "Get the next post, and each test result, by email. "
s = open("blog.html", encoding="utf-8").read()
out, pos, n = [], 0, 0
for m in re.finditer(re.escape(OLD), s):
    art = re.findall(r'<article id="([^"]+)"', s[:m.start()])[-1]
    out.append(s[pos:m.start()] + LEAD[art] + " "); pos = m.end(); n += 1
s = "".join(out) + s[pos:]
open("blog.html", "w", encoding="utf-8").write(s)
print("blog closing lines:", n)

# 2. Appendix placeholders (the same three sentences 9 times)
s = open("appendix.html", encoding="utf-8").read()
s, k = re.subn(r'This appendix entry is under development\. The mathematical framework for Element (\d+) will be added as the COSMIC Framework documentation expands\. Check back for updates or <a href="contribute\.html">contribute to the project</a>\.',
               lambda m: f"Element {m.group(1)}'s mathematics is in preparation.", s)
open("appendix.html", "w", encoding="utf-8").write(s)
print("appendix placeholders:", k)

# 3. The honor system: the full wording stays where the book is offered (Book, Download, FAQ, Shop)
ed("index.html", [("The book is sold on an honor system: pay what you are willing and able to pay.", "Readers set their own price for the book."),
                  ("It is sold on an honor system: pay what you are willing and able to pay.", "What you pay for it is up to you.")])
ed("media.html", [("on an honor system: pay what you are willing and able to pay.", "and readers decide what to pay for it.")])
ed("research-opportunities.html", [("The book is distributed on an honor system: pay what you are willing and able to pay. The science is not behind a paywall.", "The science is not behind a paywall: readers decide what, if anything, to pay for the book.")])
ed("contribute.html", [("No sign-up required; pay what you are willing and able to pay.", "No sign-up, and the price is yours to set.")])

# 4. Validation cards: one wording per card, and a different one in each card's expanded view
s = open("validation.html", encoding="utf-8").read()
s = s.replace("Standard error-correction theory predicts the same, and the earliest record of the framework's version dates from October 2025.",
              "Standard error-correction theory predicts the same; the framework's version was first written down in October 2025.", 1)
s = s.replace("The earliest record of the framework's version dates from October 2025, after the first JWST results.",
              "The framework's version was first written down in October 2025, after the first JWST results.", 1)
s = s.replace("The earliest record of the framework's version dates from October 2025, after the first JWST results.",
              "Our written version came in October 2025, after those first results.", 1)
s = s.replace("The earliest record of the framework's version dates from May 2026, after the result.",
              "The framework's version was first recorded in May 2026, after the result.", 1)
s = s.replace("The earliest record of the framework's version dates from May 2026, after the result.",
              "The framework put this in writing in May 2026, once the result was known.", 1)
s = s.replace("None counts as a test, because the earliest surviving record of each prediction dates from after the result.",
              "None counts as a test, because the framework's written version of each came after the result.", 1)
open("validation.html", "w", encoding="utf-8").write(s)
ed("index.html", [("The earliest surviving record of each prediction dates from after its result, so we count these as consistent, not as advance predictions.",
                   "Each was written into the framework after the result appeared, so we count them as consistent, not as advance predictions.")])

# 5. Smaller repeats
ed("contribute.html", [("Four published results are consistent with the framework, 51 predictions are open,", "Four outside results line up with the framework so far, 51 predictions are open,")])
ed("research-opportunities.html", [("Four published results are consistent with the framework, though none was predicted on the record in advance.",
                                    "Four results from other teams agree with it, though none was on the record beforehand.")])
ed("index.html", [("together with the result that would prove it wrong. The first to report", "along with the outcome that would count against it. The first to report")])
ed("book.html", [("It is told as a video series, with a written companion for every episode: the submissions, the people, the waiting and the data.",
                  "Each episode is a video with a written account beside it: the submissions, the people, the waiting and the data.")])
ed("index.html", [("Some biological systems appear to sustain quantum effects in warm, noisy conditions that would destroy them in a laboratory.",
                   "Living cells seem to keep fragile quantum states alive in warm, noisy conditions that would destroy them in a laboratory.")])
print("done")
# 6. Blog author notes, applied by hand afterward: four posts now carry their own line
#    (career in aircraft systems; develops the framework; author and founder; writes about
#    information, physics and the mind). The prime-numbers note was already distinct.
