# -*- coding: utf-8 -*-
"""Horizon Scanner (2 Oct 2026). Michael: "How the Field Is Moving and Who Is Researching
What should not collapse. Just make the card in each section also blue and yellow."

1. Trends and Around the World are fixed sections again (Living Review keeps its toggle).
2. Their cards use QCD pair B+Yw like the Living Review cards: quark #005ba5 card,
   antiquark #f1e303 edge, white text. Data on the blue cards is drawn in yellow first,
   then white and the flat grays, so nothing is blue on blue. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:80])
    s = s.replace(a, b)


# ---- 1. no toggle on Trends and Around the World
for sid, title in (("field-trends", "How the Field Is Moving"), ("field-regions", "Who Is Researching What")):
    sub(f'<h2 class="section-title hs-head"><button class="hs-toggle" aria-expanded="false" aria-controls="{sid}-body">{title}<span class="hs-chev" aria-hidden="true"></span></button></h2>',
        f'<h2 class="section-title">{title}</h2>')
    sub(f'<div class="hs-body" id="{sid}-body" hidden>', f'<div id="{sid}-body">')

# ---- 2. B+Yw cards
CSS = """        /* Trends and Around the World cards: QCD pair B+Yw, as the Living Review cards */
        .ft-card, .ft-rising, .rg-panel, .rg-insight { background:#005ba5 !important; color:#fff; border:0 !important; border-left:5px solid #f1e303 !important; }
        .ft-card h3 { color:#fff; }
        .ft-tests a { color:#f1e303; }
        .ft-k, .rg-panel h3 { color:rgba(255,255,255,.82) !important; }
        .ft-sub, .ft-notes-on-card { color:rgba(255,255,255,.85) !important; }
        .ft-up { color:#f1e303 !important; } .ft-down { color:#cfd8e2 !important; } .ft-flat { color:rgba(255,255,255,.7) !important; }
        .ft-rising strong, .rg-insight strong { color:#f1e303; }
        .rg-legend, .rg-tip { color:rgba(255,255,255,.88) !important; }
        .rg-tip strong { color:#f1e303; }
        .rg-rank li:hover { background:rgba(255,255,255,.1) !important; }
        .rg-rank .n { color:rgba(255,255,255,.6) !important; }
        #rg-map path.c { stroke:#005ba5 !important; }
        #rg-map path.c:hover, #rg-map path.c.sel { stroke:#f1e303 !important; stroke-width:1.6 !important; }
        .rg-panel .domain, .rg-panel .tick line { stroke:rgba(255,255,255,.55); }
        .rg-panel .tick text { fill:rgba(255,255,255,.85); }
        .rg-funders li span { color:#f1e303 !important; }
"""
i = s.index("        /* Field Watch */")
s = s[:i] + CSS + s[i:]

# Trends data colors
sub("bars(qk.map(q => qs[q]), qk, '#005ba5', !lastQFull)", "bars(qk.map(q => qs[q]), qk, '#f1e303', !lastQFull)")
sub("bars(v, ys, '#005ba5', true)", "bars(v, ys, '#f1e303', true)")
sub("[['nsf', 'NSF', '#1a1d33'], ['nih', 'NIH', '#5a6878']]", "[['nsf', 'NSF', '#ffffff'], ['nih', 'NIH', '#8fa0b0']]")

# Around the World data colors
sub("d3.interpolateRgbBasis(['#8fa0b0', '#f3f5f8', '#005ba5'])", "d3.interpolateRgbBasis(['#4a5868', '#e8eef5', '#f1e303'])")
sub(".clamp(true).unknown('#e3e6ea');", ".clamp(true).unknown('rgba(255,255,255,.16)');")
sub("['#eef2f6', M === 'fund' ? '#1a1d33' : '#005ba5']", "['#3f80bf', M === 'fund' ? '#ffffff' : '#f1e303']")
sub("return v == null ? '#e3e6ea' : col(v);", "return v == null ? 'rgba(255,255,255,.16)' : col(v);")
sub("linear-gradient(90deg,#8fa0b0,#f3f5f8,#005ba5)", "linear-gradient(90deg,#4a5868,#e8eef5,#f1e303)")
sub("linear-gradient(90deg,#eef2f6,${M === 'fund' ? '#1a1d33' : '#005ba5'})", "linear-gradient(90deg,#3f80bf,${M === 'fund' ? '#ffffff' : '#f1e303'})")
sub("M === 'fund' ? '#1a1d33' : '#005ba5'}\"></span>", "M === 'fund' ? '#ffffff' : '#f1e303'}\"></span>")
sub(" style=\"background:#eef2f6\"' : ''}><span class=\"n\">", " style=\"background:rgba(255,255,255,.14)\"' : ''}><span class=\"n\">")
sub("const pal = ['#005ba5', '#1a1d33', '#005ba5', '#1a1d33', '#5a6878', '#8fa0b0'], dash = ['', '', '6 4', '6 4', '', '2 3'];",
    "const pal = ['#f1e303', '#ffffff', '#f1e303', '#ffffff', '#8fa0b0', '#8fa0b0'], dash = ['', '', '6 4', '6 4', '', '2 3'];")
sub(".attr('text-anchor', 'end').attr('font-size', 13).attr('fill', '#2d4053').text(k);", ".attr('text-anchor', 'end').attr('font-size', 13).attr('fill', '#ffffff').text(k);")
sub(".attr('width', x(a[i]) - m.l).attr('fill', '#8fa0b0');", ".attr('width', x(a[i]) - m.l).attr('fill', '#8fa0b0');")
sub(".attr('width', x(b[i]) - m.l).attr('fill', '#005ba5');", ".attr('width', x(b[i]) - m.l).attr('fill', '#f1e303');")
sub(".attr('font-size', 12).attr('fill', '#1a1d33').text((b[i] * 100).toFixed(0) + '%');", ".attr('font-size', 12).attr('fill', '#ffffff').text((b[i] * 100).toFixed(0) + '%');")
sub(".attr('font-size', 9).attr('fill', '#5a6878').text(`gray ${y0} · blue ${Y}`);", ".attr('font-size', 11).attr('fill', 'rgba(255,255,255,.8)').text(`gray ${y0} · yellow ${Y}`);")

open(P, "w", encoding="utf-8").write(s)
print("media.html: Trends and Around the World fixed open, cards on B+Yw")
