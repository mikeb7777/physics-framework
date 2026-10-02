# -*- coding: utf-8 -*-
"""Horizon Scanner (2 Oct 2026). Michael: blue and yellow (QCD pair B+Yw) only for the two
summary boxes, "Gaining the most attention…" (#ft-rising) and the Around the World
insight (#rg-insight); everything else was fine as it was. Reverses the card and chart
colors from tools/horizon_bw_cards.py and keeps both sections non-collapsing. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:80])
    s = s.replace(a, b)


a = s[s.index("        /* Trends and Around the World cards: QCD pair B+Yw"):s.index("        /* Field Watch */")]
sub(a, """        /* Summary boxes: QCD pair B+Yw, as the Living Review cards */
        .ft-rising, .rg-insight { background:#005ba5 !important; color:#fff; border:0 !important; border-left:5px solid #f1e303 !important; }
        .ft-rising strong, .rg-insight strong { color:#f1e303; }
""")

# chart and card colors back to the navy, blue and gray set
sub("bars(qk.map(q => qs[q]), qk, '#f1e303', !lastQFull)", "bars(qk.map(q => qs[q]), qk, '#005ba5', !lastQFull)")
sub("bars(v, ys, '#f1e303', true)", "bars(v, ys, '#005ba5', true)")
sub("[['nsf', 'NSF', '#ffffff'], ['nih', 'NIH', '#8fa0b0']]", "[['nsf', 'NSF', '#1a1d33'], ['nih', 'NIH', '#5a6878']]")
sub("d3.interpolateRgbBasis(['#4a5868', '#e8eef5', '#f1e303'])", "d3.interpolateRgbBasis(['#8fa0b0', '#f3f5f8', '#005ba5'])")
sub(".clamp(true).unknown('rgba(255,255,255,.16)');", ".clamp(true).unknown('#e3e6ea');")
sub("['#3f80bf', M === 'fund' ? '#ffffff' : '#f1e303']", "['#eef2f6', M === 'fund' ? '#1a1d33' : '#005ba5']")
sub("return v == null ? 'rgba(255,255,255,.16)' : col(v);", "return v == null ? '#e3e6ea' : col(v);")
sub("linear-gradient(90deg,#4a5868,#e8eef5,#f1e303)", "linear-gradient(90deg,#8fa0b0,#f3f5f8,#005ba5)")
sub("linear-gradient(90deg,#3f80bf,${M === 'fund' ? '#ffffff' : '#f1e303'})", "linear-gradient(90deg,#eef2f6,${M === 'fund' ? '#1a1d33' : '#005ba5'})")
sub("M === 'fund' ? '#ffffff' : '#f1e303'}\"></span>", "M === 'fund' ? '#1a1d33' : '#005ba5'}\"></span>")
sub(" style=\"background:rgba(255,255,255,.14)\"' : ''}><span class=\"n\">", " style=\"background:#eef2f6\"' : ''}><span class=\"n\">")
sub("const pal = ['#f1e303', '#ffffff', '#f1e303', '#ffffff', '#8fa0b0', '#8fa0b0'],", "const pal = ['#005ba5', '#1a1d33', '#005ba5', '#1a1d33', '#5a6878', '#8fa0b0'],")
sub(".attr('text-anchor', 'end').attr('font-size', 13).attr('fill', '#ffffff').text(k);", ".attr('text-anchor', 'end').attr('font-size', 13).attr('fill', '#2d4053').text(k);")
sub(".attr('width', x(b[i]) - m.l).attr('fill', '#f1e303');", ".attr('width', x(b[i]) - m.l).attr('fill', '#005ba5');")
sub(".attr('font-size', 12).attr('fill', '#ffffff').text((b[i] * 100).toFixed(0) + '%');", ".attr('font-size', 12).attr('fill', '#1a1d33').text((b[i] * 100).toFixed(0) + '%');")
sub(".attr('font-size', 11).attr('fill', 'rgba(255,255,255,.8)').text(`gray ${y0} · yellow ${Y}`);", ".attr('font-size', 11).attr('fill', '#5a6878').text(`gray ${y0} · blue ${Y}`);")

open(P, "w", encoding="utf-8").write(s)
print("media.html: B+Yw only on the two summary boxes")
