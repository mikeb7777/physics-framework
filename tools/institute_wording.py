# -*- coding: utf-8 -*-
"""Michael, 29 Sep 2026: "We are a research institute for others to affiliate
with... overstating it is almost saying that we aren't a research institute.
Our wording should match that of any other institute." Formalization comes
after the videos and the book rewrite; until then the pages describe the
Institute plainly and keep the one fact donors need (not tax-deductible)."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOOTER_OLD = "No gatekeeping. No institutional barriers."
FOOTER_NEW = "Open to anyone. The work is the only standard."
NATURE = ("The Ic&sup2; Research Institute is an independent research institute founded by Michael K. Baines. "
          "It develops the COSMIC Framework, registers its predictions before the data that tests them, and "
          "welcomes researchers who wish to affiliate with it.")
EXACT = {
    "legal.html": [
        ("Ic² Research Institute is an independent research platform operated by Michael K. Baines as a sole proprietor. It is not a registered corporation, LLC, partnership, or non-profit organization. We operate as a transparent, community-driven initiative focused on consciousness and computation research. Legal entity formation is planned for a future date as the platform grows.", NATURE),
        ("<strong>Important:</strong> Ic² Research Institute is NOT a registered 501(c)(3) or any other tax-exempt organization. Financial contributions are not charitable donations and are not tax-deductible. See the Financial Disclosures section for full details.",
         "<strong>Contributions:</strong> Contributions to the Institute are not charitable donations and are not tax-deductible. See the Financial Disclosures section for details."),
        ("There are no fees, no gatekeeping, and no institutional barriers to participation.", "There are no fees, and participation is open to anyone."),
    ],
    "terms-conditions.html": [
        ("Ic² Research Institute is an independent research platform operated by Michael K. Baines as a sole proprietor. It is not a registered corporation, LLC, partnership, or non-profit organization. Legal entity formation is planned for a future date as the platform grows.", NATURE),
        ("<strong>Important:</strong> Ic² Research Institute is NOT a registered 501(c)(3) or any other tax-exempt organization. Financial contributions are not charitable donations and are not tax-deductible. See Section 10 for full financial disclosures.",
         "<strong>Contributions:</strong> Contributions to the Institute are not charitable donations and are not tax-deductible. See Section 10 for details."),
        ("There are no fees, no gatekeeping, and no institutional barriers.", "There are no fees, and participation is open to anyone."),
    ],
    "privacy-policy.html": [
        ("This Privacy Policy applies to the Ic² Research Institute website operated by <strong>Michael K. Baines</strong> as a sole proprietor. The institute is not a registered corporation or non-profit entity.",
         "This Privacy Policy applies to the website of the Ic² Research Institute (eequalsicsquared.com). The Institute&rsquo;s founder, <strong>Michael K. Baines</strong>, is responsible for the personal information collected through it."),
    ],
    "quest-map.html": [
        (">No institution behind the work<", ">Self-funded, no university or company<"),
    ],
    "unsubscribe.html": [
        ("No gatekeeping. No institutional barriers. Just honest pursuit of knowledge.", FOOTER_NEW),
    ],
}

changed = []
for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    name = os.path.basename(p)
    t = open(p, encoding="utf-8").read()
    u = t
    for old, new in EXACT.get(name, []):
        assert u.count(old) == 1, (name, old[:50])
        u = u.replace(old, new)
    u = u.replace(FOOTER_OLD, FOOTER_NEW)
    if name in ("legal.html", "terms-conditions.html", "privacy-policy.html"):
        u = re.sub(r"(Last [Uu]pdated:?\s*)(?:January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{0,2},?\s*20\d\d",
                   r"\g<1>September 2026", u, count=1)
    if u != t:
        open(p, "w", encoding="utf-8", newline="").write(u)
        changed.append(name)
print(len(changed), "pages:", ", ".join(changed))
left = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html"))
        if re.search(r"sole proprietor|institutional barriers|NOT a registered", open(p, encoding="utf-8").read())]
print("still present:", left)
