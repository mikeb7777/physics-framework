# -*- coding: utf-8 -*-
"""references.html rebuilt to match Book Version 6D (6 Oct 2026; Michael approved the full rebuild).
The site's lists had drifted from the book's numbering (built from an earlier draft): Element 7 [12] pointed to a
paper on neuronal communication instead of the dark matter simulation the sentence cites, Element 5 had five
unnumbered entries for 21 citations, Element 8 stopped at 35 while the book cites [58], and so on.
For every citation [n] in 6D, the citing sentence was read and matched to its source. Existing entries were kept
where they fit ("site:N" in the maps); new or corrected entries were taken from the publisher's record (Crossref or
DataCite). Invented or garbled entries were removed. Where the book reuses one number for two claims, both sources
are listed. Where no source could be found, the entry says so; those sentences are listed for the next book version.
Maps: Book-Drafts/refs/map/*.txt; worksheet: Book-Drafts/refs/worksheet.json. Uncited old entries are dropped.
Run once."""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(os.path.dirname(ROOT), "Book-Drafts", "refs")
P = os.path.join(ROOT, "references.html")
ws = json.load(open(os.path.join(REFS, "worksheet.json"), encoding="utf-8"))
ORDER = [w["part"] for w in ws]


def load_map(part):
    out = []
    for line in open(os.path.join(REFS, "map", part + ".txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        n, val = line.split(" | ", 1)
        out.append((int(n), val))
    return out


def resolve(val, site):
    val = val.replace(" ||| ", " ")
    return re.sub(r"site:(\d+)", lambda m: site[m.group(1)], val)


def render(n, text):
    note = text.startswith("NOTE: ")
    if note:
        text = text[6:]
    t = html.escape(text, quote=False).replace('"', "&quot;")
    links = []
    for m in re.finditer(r"doi:\s*(10\.\S+?)(?=[.,;)]?(?:\s|$))", text):
        links.append("https://doi.org/" + m.group(1))
    for m in re.finditer(r"(?<!doi\.org/)(https?://\S+?)(?=[.,;)]?(?:\s|$))", text):
        if "doi.org" not in m.group(1):
            links.append(m.group(1))
    t = re.sub(r"(https?://\S+?)(?=[.,;)]?(?:\s|$))", lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>', t)
    btn = ""
    if links:
        btn = f' <a href="{links[0]}" target="_blank" rel="noopener" class="ref-src">View Source</a>'
    body = f"<em>{t}</em>" if note else t
    return f'                <div class="reference-item{" ref-note" if note else ""}">\n                    <p><strong>[{n}]</strong> {body}{btn}</p>\n                </div>\n'


s = open(P, encoding="utf-8").read()
sections = list(re.finditer(r'<div class="references-section">\s*<div class="section-header"[^>]*>\s*<h2>(.*?)</h2>.*?<div class="references-list">', s, re.S))
assert len(sections) == len(ORDER), (len(sections), len(ORDER))
out, pos, count = [], 0, 0
for m, part in zip(sections, ORDER):
    site = next(w for w in ws if w["part"] == part)["site_entries"]
    start = m.end()
    # the list ends where its closing </div> balances
    depth, i = 1, start
    while depth:
        a, b = s.find("<div", i), s.find("</div>", i)
        if a != -1 and a < b:
            depth += 1; i = a + 4
        else:
            depth -= 1; i = b + 6
    end = i - len("</div>")
    items = "".join(render(n, resolve(v, site)) for n, v in load_map(part))
    count += len(load_map(part))
    out.append(s[pos:start] + "\n" + items + "            ")
    pos = end
s = "".join(out) + s[pos:]

INTRO = ("<p><strong>Matched to Version 6D (October 2026).</strong> The numbers below are the numbers printed in the book. "
         "Each entry was checked against the sentence that cites it and against the publisher&rsquo;s record. Where the book "
         "uses one number for two claims, both sources are given; where no source has been found yet, the entry says so, and "
         "the sentence is being corrected in the next version.</p>\n        ")
a = '<h2>About This Reference List</h2>\n        '
assert s.count(a) == 1
s = s.replace(a, a + INTRO)
CSS = ("    .ref-src { display:inline-block; background:#4a5868; color:#fff; font-size:.78rem; font-weight:700; padding:.15rem .65rem; "
       "border-radius:20px; text-decoration:none; margin-left:.4rem; letter-spacing:.03em; } .reference-item a.ref-src, .reference-item a.ref-src:visited { color:#ffffff !important; }\n"
       "    .ref-note p { color:#5a6878; }\n  </style>")
i = s.find("</style>")
s = s[:i] + CSS[:-len("  </style>")] + s[i:]
open(P, "w", encoding="utf-8").write(s)
print("sections:", len(sections), "entries:", count)
