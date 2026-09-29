# -*- coding: utf-8 -*-
"""Page headlines (Michael approved 29 Sep 2026): a plain label that matches
the menu word, then a headline with character. Each entry: page, the exact
old <h1> (or header) markup, the new markup. Every entry must match once."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lab(label):
    return f'<p class="eyebrow page-label">{label}</p>\n      '


E = [
 ("events.html", "<h1>Events</h1>", lab("Events") + "<h1>Bring your hardest question</h1>"),
 ("blog.html", "<h1>Research Blog</h1>", lab("Blog") + "<h1>Notes from the middle of the work</h1>"),
 ("faq-page.html", '<h1 class="page-title">Frequently Asked Questions</h1>', lab("Questions") + '<h1 class="page-title">The questions people actually ask</h1>'),
 ("contribute.html", '<h1 data-aos="fade-down" data-aos-duration="800">Support Open Research</h1>', lab("Support") + '<h1 data-aos="fade-down" data-aos-duration="800">Open research runs on people</h1>'),
 ("join.html", "<h1>Join</h1>", lab("Join") + "<h1>Work on it with us</h1>"),
 ("subscribe.html", "<h1>Subscribe</h1>", lab("Subscribe") + "<h1>Hear it when a prediction reports</h1>"),
 ("members.html", "<h1>Our Members</h1>", lab("Members") + "<h1>The people doing the work</h1>"),
 ("media.html", "<h1>Media and Press</h1>", lab("Press") + "<h1>The story so far, for the record</h1>"),
 ("gallery.html", "<h1>Gallery</h1>", lab("Gallery") + "<h1>The work, in pictures</h1>"),
 ("glossary.html", '<div class="page-title">Glossary</div>\n    <div class="page-subtitle">Comprehensive definitions of key terms, concepts, and principles used throughout The Big TOE.</div>',
  lab("Glossary") + '<h1 class="page-title">Every term, defined once</h1>\n    <div class="page-subtitle">The words the book and this site rely on, each explained in plain language.</div>'),
 # the hidden old header also has an h1 and the same subtitle: demote it first
 ("references.html", '<div class="page-header-old" style="display:none;">\n            <h1>References</h1>\n            <p>Comprehensive Bibliography & Citations</p>',
  '<div class="page-header-old" style="display:none;">\n            <p>References</p>\n            <p>Bibliography</p>'),
 ("references.html", "<h1>References</h1>\n", lab("References") + "<h1>Everything we stand on</h1>\n"),
 ("results.html", "<h1>Results Registry</h1>", lab("Results") + "<h1>Every prediction, and what it showed</h1>"),
 ("testing-schedule.html", "<h1>Prediction Forecast and Testing Schedule</h1>", lab("Testing Schedule") + "<h1>What gets tested next, and when</h1>"),
 ("validation.html", "<h1>Iterative Refinement<br>Validation System</h1>", lab("Validation") + "<h1>How a result changes the framework</h1>"),
 ("programs-gateway.html", '<h1 data-aos="fade-up">Research Programs</h1>', lab("Programs") + '<h1 data-aos="fade-up">Seven programs, each with a test and a price</h1>'),
 ("simulations.html", "<h1>Simulations</h1>", lab("Simulations") + "<h1>Turn the ideas in your hands</h1>"),
 ("download.html", "<h1>Download A Quest for The Big TOE</h1>", lab("The Book") + "<h1>The whole framework, free to read</h1>"),
 ("zenodo-papers.html", "<h1>Zenodo Research Archive</h1>", lab("Archive") + "<h1>Dated before the data</h1>"),
 ("research-publications.html", "<h1>Research Publications</h1>", lab("Publications") + "<h1>Open to read, open to check</h1>"),
 ("legal.html", "<h1>Legal &amp; Policies</h1>", lab("Legal") + "<h1>The rules we hold ourselves to</h1>"),
 ("privacy-policy.html", "<h1>Privacy Policy</h1>", lab("Privacy") + "<h1>We collect as little as we can</h1>"),
 ("unsubscribe.html", '<h1 data-aos="fade-up">Manage Your Subscriptions</h1>', lab("Subscriptions") + '<h1 data-aos="fade-up">One click, no questions</h1>'),
 # generic opening lines, rewritten with the headlines
 ("faq-page.html", "Everything you need to know about The Big TOE and our research", "Straight answers about the framework, the book, and how we test ideas in public."),
 ("discussions-page.html", "Connect, collaborate, and explore ideas with fellow researchers", "Ask a question, argue a point, or pick up a thread someone else started."),
 ("research-publications.html", "Open access preprints and peer-reviewed publications", "Preprints and papers, free to read, each with its date and its data."),
 ("references.html", "Comprehensive Bibliography & Citations", "Every source the book and this site rely on, in one place."),
 ("appendix.html", "Supporting Technical Documentation and Mathematical Derivations", "The derivations and technical detail behind each Element, for readers who want the working."),
]

texts, missing = {}, []
for page, old, new in E:
    p = os.path.join(ROOT, page)
    t = texts.get(page) or open(p, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        missing.append((page, n, old[:70]))
        continue
    texts[page] = t.replace(old, new)
for page, t in texts.items():
    if "--write" in sys.argv:
        open(os.path.join(ROOT, page), "w", encoding="utf-8", newline="").write(t)
print(f"{len(E) - len(missing)} of {len(E)} applied to {len(texts)} pages" + ("" if "--write" in sys.argv else " (dry run)"))
for m in missing:
    print("NOT APPLIED:", m)
