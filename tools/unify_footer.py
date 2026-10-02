# -*- coding: utf-8 -*-
"""One footer for the site (2 Oct 2026). Michael: balance the footer links sitewide;
sometimes one column is longer than the others; padding and text are a little random;
maybe some color variation.

The institute pages had about 25 footer variants (16 to 27 links, columns of 7, 9 and 11,
duplicates such as Archive = Publications). They now share one footer: the description
and contact buttons, then four columns of seven links (six in the last), headings with an
accent bar in the spinner's color charges plus yellow, and the legal links in the bottom
line. Styles live in site-consistency.css (.site-footer). The Book and Quest pages keep
their own public footer (.pub-footer), rebalanced to 6 / 6 / 7. Run once."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

COLS = [
    ("Research", [("framework.html", "Framework"), ("validation.html", "Validation"), ("testing-schedule.html", "Testing"),
                  ("results.html", "Results"), ("programs-gateway.html", "Programs"), ("research-publications.html", "Publications"),
                  ("simulations.html", "Simulations")]),
    ("Explore", [("book.html", "The Big TOE"), ("quest-map.html", "The Quest"), ("mission-log.html", "Mission Log"),
                 ("media.html", "Horizon Scanner"), ("blog.html", "Blog"), ("gallery.html", "Gallery"), ("search.html", "Search")]),
    ("Institute", [("about-page.html", "About"), ("members.html", "Our Members"), ("events.html", "Events"),
                   ("discussions-page.html", "Discussions"), ("faq-page.html", "FAQ"),
                   ("https://www.michaelkbaines.com", "Author's Website"), ("about-page.html#contact", "Contact")]),
    ("Take Part", [("subscribe.html", "Subscribe"), ("join.html", "Join"), ("contribute.html", "Contribute"),
                   ("support.html", "Support Our Research"), ("become-member.html", "Work With Us"), ("shop.html", "Shop (opening soon)")]),
]
for _, links in COLS:
    for href, _t in links:
        if not href.startswith("http"):
            assert os.path.exists(href.split("#")[0]), href

IG = '<svg viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'
YT = '<svg viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
EM = '<svg viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>'


def col(title, links):
    lis = "".join(f'<li><a href="{h}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""}>{t}</a></li>' for h, t in links)
    return f'<div class="sf-col"><h3>{title}</h3><ul>{lis}</ul></div>'


FOOTER = f'''<footer class="site-footer">
    <div class="sf-inner">
      <div class="sf-about">
        <p class="sf-name">Ic&sup2; Research Institute</p>
        <p>An independent research institute advancing theoretical physics through open science. We develop falsifiable predictions across cosmology, quantum mechanics and consciousness research, and we publish every result.</p>
        <p>Every contributor keeps full ownership of their work. All findings are freely available. Open to anyone.</p>
        <div class="sf-social">
          <a href="https://www.instagram.com/eequalsicsquared?igsh=ZWFidnFyNTBheG4z" target="_blank" rel="noopener" class="instagram">{IG}Instagram</a>
          <a href="https://www.youtube.com/@IC2ResearchInstitute" target="_blank" rel="noopener" class="youtube">{YT}YouTube</a>
          <a href="mailto:ic2.info@proton.me" class="email">{EM}ic2.info@proton.me</a>
        </div>
      </div>
      <nav class="sf-links" aria-label="Site links">{"".join(col(t, l) for t, l in COLS)}</nav>
    </div>
    <div class="sf-bottom"><p>&copy; 2026 Ic&sup2; Research Institute. All rights reserved. | <a href="legal.html">Legal</a> | <a href="privacy-policy.html">Privacy Policy</a> | <a href="terms-conditions.html">Terms &amp; Conditions</a> | <a href="unsubscribe.html">Unsubscribe</a></p></div>
  </footer>'''

done, skipped = [], []
for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    ms = [m for m in re.finditer(r"<footer\b[^>]*>", s) if "pub-footer" not in m.group(0) and "article-footer" not in m.group(0)]
    if not ms:
        continue
    m = ms[-1]
    end = s.find("</footer>", m.start())
    inner = s[m.start():end]
    if "<footer" in inner[7:]:          # a nested footer inside: leave the page for a manual look
        skipped.append(f); continue
    s = s[:m.start()] + FOOTER + s[end + len("</footer>"):]
    open(f, "w", encoding="utf-8").write(s); done.append(f)
print("site footer on", len(done), "pages; skipped", skipped)

# the Book and Quest footer: 6 / 6 / 7
PUB = ('<nav class="pub-links" aria-label="Site links">'
       '<div><h3>The Book</h3><ul><li><a href="book.html">Overview</a></li><li><a href="download.html">Download</a></li><li><a href="conversion.html">Formats</a></li><li><a href="references.html">References</a></li><li><a href="appendix.html">Appendices</a></li><li><a href="glossary.html">Glossary</a></li></ul></div>'
       '<div><h3>The Quest</h3><ul><li><a href="quest-map.html">Quest Map</a></li><li><a href="instruments.html">The Instruments</a></li><li><a href="mission-log.html">Mission Log</a></li><li><a href="media.html">Horizon Scanner</a></li><li><a href="quest-follow.html#episodes">Episodes</a></li><li><a href="quest-follow.html">Follow the Quest</a></li></ul></div>'
       '<div><h3>Ic&sup2; Institute</h3><ul><li><a href="index.html">Home</a></li><li><a href="framework.html">The Framework</a></li><li><a href="validation.html">Validation</a></li><li><a href="testing-schedule.html">Testing Schedule</a></li><li><a href="faq-page.html">FAQ</a></li><li><a href="about-page.html">About</a></li><li><a href="about-page.html#contact">Contact</a></li></ul></div>'
       '</nav>')
n = 0
for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    t = re.sub(r'<nav class="pub-links" aria-label="Site links">.*?</nav>', PUB, s, count=1, flags=re.S)
    if t != s:
        open(f, "w", encoding="utf-8").write(t); n += 1
print("public footer rebalanced on", n, "pages")
