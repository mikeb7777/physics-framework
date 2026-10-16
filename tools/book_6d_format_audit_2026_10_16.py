# -*- coding: utf-8 -*-
"""Version 6D, formatting audit (Michael, 16 Oct 2026: "I put the book together, which means it's
probably wrong. Actually, I know the formatting on the tables isn't good. Please do an audit of the
formatting throughout the book").

Tables (32: 6 data tables, 23 COSMIC CONNECTIONS boxes, 3 status callouts, 5 prediction boxes)
  T1  Every table spans the text column, 4.8 in (6912 twips). Most were 4.5 in, a few 4.52 to 4.6 in,
      and several had column grids wider than the table itself.
  T2  Data tables: every word measured (Liberation Sans, Arial's metrics) and each column made at least
      as wide as its longest word, so no word breaks across lines (headers read "DEFININ / G",
      "Ban / d", "Superconductin / g"); each table takes the largest size from 8.5 pt down to 7 pt at
      which that fits, header no larger than 8 pt; cell padding 0.05 in a side; header letter-spacing
      removed; rows kept whole across page breaks; one typeface (Arial; Cambria Math and Segoe UI
      Symbol stay where they set symbols); symbol-only cells left at their size.
  T3  COSMIC CONNECTIONS: the three blue boxes (Elements 9, 10, 11) take the dark-red border and pale
      fill of the other twenty.
Text
  X1  "Construct**" -> "Construct" (a leftover markdown marker).
  X2  Thirteen subscripts typed with an underscore set as real subscripts: M_Planck, n_s (5), lambda_Planck (3),
      f_e, E_Planck (2), lambda_scrambling.
  X3  The scrambling bound read "2 pi k2 T / hbar", and the line under it "k2 is Boltzmann's constant";
      the constant is k_B.
  X4  A stray "explain." paragraph (Element 10) and a stray "." (end of Element 3) removed.
  X5  "Figure 12 - The arrow ..." gains its number: "Figure 12 - 1".
  X6  Straight double quotes in running text made curly, as everywhere else in the book.
  X7  Doubled spaces in running text and captions closed up.
  X8  Captions set flush left instead of justified (justified captions opened wide gaps); seven caption
      runs that carried their own font and size return to the caption style.
  X9  Three section headings typed as body text get the heading style (and so join the contents):
      "SYSTEMATIC FREQUENCY EVOLUTION BY CONSTANT TYPE" (Element 11; its first letter was unstyled),
      "EMPIRICAL EVIDENCE: MATHEMATICAL STRUCTURE IN COSMIC OBSERVATIONS" (Element 14),
      "WHAT NEUROSCIENCE HAS DISCOVERED" (Element 17).
Run once:  python3 tools/book_6d_format_audit_2026_10_16.py
"""
import copy, os, re
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "A Quest for The Big TOE Version 6D.docx")
TEXT_W = 6912                      # 4.8 in text column, in twips
d = docx.Document(DOC)
body = d.element.body
log = []


def text(e):
    return "".join(t.text or "" for t in e.iter(qn("w:t")))


def set_attr(parent, tag, **attrs):
    el = parent.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        parent.append(el)
    for k, v in attrs.items():
        el.set(qn("w:" + k), str(v))
    return el


def ensure_pr(el, tag):
    pr = el.find(qn(tag))
    if pr is None:
        pr = OxmlElement(tag)
        el.insert(0, pr)
    return pr


# ------------------------------------------------------------------ tables
SYMBOL_FONTS = {"Cambria Math", "Segoe UI Symbol"}
from PIL import ImageFont                                # Liberation Sans has Arial's metrics
_LS = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf"
_FACES = {(b, i): ImageFont.truetype(_LS % {(0, 0): "Regular", (1, 0): "Bold", (0, 1): "Italic", (1, 1): "BoldItalic"}[(b, i)], 1000)
          for b in (0, 1) for i in (0, 1)}


def measure(word, pt, bold, italic):
    """Width of word in points, set in Arial at pt."""
    return _FACES[(int(bool(bold)), int(bool(italic)))].getlength(word) / 1000 * pt

tables = list(body.iter(qn("w:tbl")))
assert len(tables) == 32, len(tables)


def cells_by_col(t):
    """[(row, tc, first grid col, span)] for every cell."""
    out = []
    for r in t.findall(qn("w:tr")):
        col = 0
        for tc in r.findall(qn("w:tc")):
            tcpr = tc.find(qn("w:tcPr"))
            gs = tcpr.find(qn("w:gridSpan")) if tcpr is not None else None
            span = int(gs.get(qn("w:val"))) if gs is not None else 1
            out.append((r, tc, col, span))
            col += span
    return out


def set_widths(t, widths):
    grid = t.find(qn("w:tblGrid"))
    for g, w in zip(grid.findall(qn("w:gridCol")), widths):
        g.set(qn("w:w"), str(w))
    tblpr = t.find(qn("w:tblPr"))
    set_attr(tblpr, "w:tblW", w=TEXT_W, type="dxa")
    for _, tc, col, span in cells_by_col(t):
        tcpr = ensure_pr(tc, "w:tcPr")
        set_attr(tcpr, "w:tcW", w=sum(widths[col:col + span]), type="dxa")


def word_len(s):
    return max((len(w) for w in re.split(r"[\s/]+", s) if w), default=0)


for t in tables:
    ncols = len(t.find(qn("w:tblGrid")).findall(qn("w:gridCol")))
    first = text(t)
    if ncols == 1:                                       # boxes: full width
        set_widths(t, [TEXT_W])
        if first.startswith("COSMIC CONNECTIONS"):       # T3
            for tc in t.iter(qn("w:tc")):
                tcpr = tc.find(qn("w:tcPr"))
                b = tcpr.find(qn("w:tcBorders"))
                for side in ("top", "left", "bottom", "right"):
                    e = b.find(qn("w:" + side))
                    e.set(qn("w:sz"), "6"); e.set(qn("w:color"), "8B0000")
                tcpr.find(qn("w:shd")).set(qn("w:fill"), "FFF5F5")
                m = tcpr.find(qn("w:tcMar"))
                m.find(qn("w:top")).set(qn("w:w"), "140"); m.find(qn("w:bottom")).set(qn("w:w"), "140")
        continue

    # T2: data table
    rows = t.findall(qn("w:tr"))
    header = rows[0]
    cells = cells_by_col(t)

    def on(rpr, tag):
        e = rpr.find(qn(tag)) if rpr is not None else None
        return e is not None and e.get(qn("w:val")) not in ("0", "false")

    # every word with how it is set: (column, word, bold, italic, header?)
    words = []; total = [0] * ncols; count = [0] * ncols
    for r, tc, col, span in cells:
        s = text(tc)
        if span == 1:
            total[col] += len(s); count[col] += 1
        if span != 1 or (len(s.strip()) <= 2 and r is not header):
            continue
        for run in tc.iter(qn("w:r")):
            rpr = run.find(qn("w:rPr"))
            rs = text(run)
            if on(rpr, "w:caps"):
                rs = rs.upper()
            for w in re.split(r"\s+", rs):
                if w:
                    words.append((col, w, r is header or on(rpr, "w:b"), on(rpr, "w:i"), r is header))
    PAD = 72                                            # cell padding each side, twips (0.05 in)
    for body_pt in (8.5, 8, 7.5, 7):
        head_pt = min(8, body_pt)
        floor = [2 * PAD + 60] * ncols
        for col, w, b, i, h in words:
            need = int(measure(w, head_pt if h else body_pt, b, i) * 20) + 2 * PAD + 60
            floor[col] = max(floor[col], need)
        if sum(floor) <= TEXT_W:
            break
    avg = [total[i] / max(count[i], 1) for i in range(ncols)]
    spare = TEXT_W - sum(floor)
    assert spare >= 0, (first[:30], floor)
    weights = [max(a, 1) ** 0.8 for a in avg]
    widths = [floor[i] + int(spare * weights[i] / sum(weights)) for i in range(ncols)]
    widths[-1] += TEXT_W - sum(widths)
    set_widths(t, widths)
    tblpr = t.find(qn("w:tblPr"))
    cm = tblpr.find(qn("w:tblCellMar"))
    if cm is None:
        cm = OxmlElement("w:tblCellMar"); tblpr.append(cm)
    for side in ("w:left", "w:right"):
        set_attr(cm, side, w=PAD, type="dxa")
    for tc in t.iter(qn("w:tc")):
        m = tc.find(qn("w:tcPr")).find(qn("w:tcMar"))
        if m is not None:
            for side in ("w:left", "w:right", "w:start", "w:end"):
                e = m.find(qn(side))
                if e is not None:
                    e.set(qn("w:w"), str(PAD)); e.set(qn("w:type"), "dxa")

    for r in rows:                                      # rows stay whole across pages
        trpr = ensure_pr(r, "w:trPr")
        if trpr.find(qn("w:cantSplit")) is None:
            trpr.insert(0, OxmlElement("w:cantSplit"))

    for r in rows:
        is_header = r is header
        for run in r.iter(qn("w:r")):
            s = text(run)
            rpr = ensure_pr(run, "w:rPr")
            rf = rpr.find(qn("w:rFonts"))
            if rf is not None and rf.get(qn("w:ascii")) in SYMBOL_FONTS:
                continue
            if rf is None:
                rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
            for a in ("ascii", "hAnsi", "cs"):
                rf.set(qn("w:" + a), "Arial")
            for a in ("asciiTheme", "hAnsiTheme", "cstheme"):
                rf.attrib.pop(qn("w:" + a), None)
            if len(s.strip()) <= 2 and not is_header:      # a symbol on its own (pi, phi, e, alpha, hbar)
                continue
            size = str(int((head_pt if is_header else body_pt) * 2))
            for tag in ("w:sz", "w:szCs"):
                set_attr(rpr, tag, val=size)
            sp = rpr.find(qn("w:spacing"))              # letter-spacing would widen words past the measure
            if sp is not None:
                rpr.remove(sp)
    log.append(f"data table {first[:30]!r}: body {body_pt} pt, header {head_pt} pt, widths {widths}")

# ------------------------------------------------------------------ text
paras = list(body.iter(qn("w:p")))


def runs_of(p):
    return [r for r in p.iter(qn("w:r")) if r.find(qn("w:t")) is not None]


# X1
hits = 0
for p in paras:
    for r in runs_of(p):
        t = r.find(qn("w:t"))
        if t.text and "Construct**" in t.text:
            t.text = t.text.replace("Construct**", "Construct"); hits += 1
assert hits == 1, hits


def split_run(r, pieces):
    """Replace run r by runs for pieces [(text, subscript?)], same formatting."""
    parent = r.getparent(); idx = parent.index(r)
    for k, (s, sub) in enumerate(pieces):
        nr = copy.deepcopy(r)
        for t in nr.findall(qn("w:t")):
            nr.remove(t)
        t = OxmlElement("w:t"); t.text = s
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        nr.append(t)
        rpr = ensure_pr(nr, "w:rPr")
        va = rpr.find(qn("w:vertAlign"))
        if sub:
            if va is None:
                va = OxmlElement("w:vertAlign"); rpr.append(va)
            va.set(qn("w:val"), "subscript")
        parent.insert(idx + k, nr)
    parent.remove(r)


# X2 and X3
SUB = re.compile(r"(?<=[A-Za-zλπ])_(Planck|scrambling|s|e)\b")
subs = 0
for p in paras:
    for r in runs_of(p):
        ts = r.findall(qn("w:t"))
        if len(ts) != 1:
            continue
        s = ts[0].text or ""
        if SUB.search(s) or "k₂T" in s:
            pieces = []; pos = 0
            for m in re.finditer(r"(?<=[A-Za-zλπ])_(Planck|scrambling|s|e)\b|(?<=k)₂(?=T)", s):
                pieces.append((s[pos:m.start()], False))
                pieces.append((m.group(1), True))
                pos = m.end(); subs += 1
            pieces.append((s[pos:], False))
            split_run(r, [x for x in pieces if x[0]])
assert subs == 13, subs

# X3: "2 pi k" and "subscript-2 T" sit in neighbouring runs; the subscript is B (Boltzmann), not 2
kb = 0
for p in list(body.iter(qn("w:p"))):
    rs = runs_of(p)
    for a, b in zip(rs, rs[1:]):
        ta, tb = a.find(qn("w:t")), b.find(qn("w:t"))
        at = ta.text or ""
        if at.endswith("k") and (len(at) == 1 or at[-2] in " \u03c0") and (tb.text or "").startswith("\u2082"):
            rest = tb.text[1:]
            split_run(b, [x for x in [("B", True), (rest, False)] if x[0]])
            kb += 1
assert kb == 2, kb                                     # the formula, and "k_B is Boltzmann's constant"

# X4
explain = [p for p in paras if text(p).strip() == "explain."]
assert len(explain) == 1
assert explain[0].find(".//" + qn("w:sectPr")) is None and explain[0].find(".//" + qn("w:br")) is None
explain[0].getparent().remove(explain[0])
dot = [p for p in paras if text(p).strip() == "."]
assert len(dot) == 1
for t in dot[0].iter(qn("w:t")):
    t.text = (t.text or "").replace(".", "")

# X5
fig12 = [p for p in paras if text(p).startswith("Figure 12 - The arrow")]
assert len(fig12) == 1
for t in fig12[0].iter(qn("w:t")):
    if t.text and "Figure 12 - " in t.text:
        t.text = t.text.replace("Figure 12 - ", "Figure 12 - 1 ", 1); break
else:
    raise SystemExit("Figure 12 caption text not in one run")


# X6, X7: running text and captions only
def pstyle(p):
    pp = p.find(qn("w:pPr")); s = pp.find(qn("w:pStyle")) if pp is not None else None
    return s.get(qn("w:val")) if s is not None else "Normal"


quotes = spaces = 0
for p in paras:
    if pstyle(p) not in ("mainbody", "Caption"):
        continue
    ts = [t for t in p.iter(qn("w:t"))]
    full = "".join(t.text or "" for t in ts)
    if '"' in full:
        out = []; open_q = True
        for t in ts:
            s = t.text or ""
            new = []
            for ch in s:
                if ch == '"':
                    new.append("“" if open_q else "”"); open_q = not open_q; quotes += 1
                else:
                    new.append(ch)
            t.text = "".join(new)
    for t in ts:
        if t.text and "  " in t.text:
            n = len(re.findall(r"(?<=\S)  +(?=\S)", t.text))
            if n:
                t.text = re.sub(r"(?<=\S)  +(?=\S)", " ", t.text); spaces += n

# X8
d.styles["Caption"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
for p in paras:
    if pstyle(p) == "Caption":
        jc = p.find(qn("w:pPr")).find(qn("w:jc")) if p.find(qn("w:pPr")) is not None else None
        if jc is not None and jc.get(qn("w:val")) in ("both", "distribute"):
            jc.set(qn("w:val"), "left")

for p in paras:                                          # X8: caption runs follow the style
    if pstyle(p) == "Caption":
        for r in p.iter(qn("w:r")):
            rpr = r.find(qn("w:rPr"))
            if rpr is None:
                continue
            for tag in ("w:rFonts", "w:sz", "w:szCs"):
                e = rpr.find(qn(tag))
                if e is not None and not (tag == "w:rFonts" and e.get(qn("w:ascii")) in SYMBOL_FONTS):
                    rpr.remove(e)

# X9
HEADINGS = ["SYSTEMATIC FREQUENCY EVOLUTION BY CONSTANT TYPE",
            "EMPIRICAL EVIDENCE: MATHEMATICAL STRUCTURE IN COSMIC OBSERVATIONS",
            "WHAT NEUROSCIENCE HAS DISCOVERED"]
for h in HEADINGS:
    hits = [p for p in paras if text(p).strip() == h and pstyle(p) == "mainbody"]
    assert len(hits) == 1, (h, len(hits))
    p = hits[0]
    ppr = ensure_pr(p, "w:pPr")
    st = ppr.find(qn("w:pStyle"))
    st.set(qn("w:val"), "subchapter")
    for e in list(ppr):                                  # paragraph overrides go; the style decides
        if e.tag not in (qn("w:pStyle"), qn("w:sectPr"), qn("w:rPr")):
            ppr.remove(e)
    for r in p.iter(qn("w:r")):                          # run overrides go too
        rpr = r.find(qn("w:rPr"))
        if rpr is not None:
            r.remove(rpr)

d.save(DOC)
for line in log:
    print(line)
print(f"subscripts {subs}, curly quotes {quotes}, doubled spaces closed {spaces}")
