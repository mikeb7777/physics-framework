# -*- coding: utf-8 -*-
"""Horizon Scanner (2 Oct 2026). Michael: "The panels at the top should be accordion-
collapsible. Rather than using all of the QCD colors, just pick one set of colors."

1. Living Review, Trends and Around the World become collapsible panels (heading button
   with aria-expanded; the description stays visible when closed). Living Review starts
   open, the others closed; each opens independently; a link to a panel's #id opens it;
   the open/closed choice is remembered per visitor.
2. One color set in those panels: navy #1a1d33, blue #005ba5 and the flat grays
   #8fa0b0 / #5a6878 / #4a5868 (no red, green or amber). Press is unchanged. Run once."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()
assert "hs-toggle" not in s


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


# ---- 1. accordion markup
for sid, title, is_open in (("field-watch", "What the Field Is Finding", True),
                            ("field-trends", "How the Field Is Moving", False),
                            ("field-regions", "Who Is Researching What", False)):
    start = s.index(f'id="{sid}"')
    end = s.index("</section>", start)
    block = s[start:end]
    h2 = f'<h2 class="section-title">{title}</h2>'
    assert block.count(h2) == 1
    sub_end = block.index("</p>", block.index('class="section-subtitle"')) + len("</p>")
    body_start = sub_end
    inner_close = block.rindex("</div>")                      # closes .section-inner
    new = (block[:block.index(h2)]
           + f'<h2 class="section-title hs-head"><button class="hs-toggle" aria-expanded="{str(is_open).lower()}" aria-controls="{sid}-body">'
           + f'{title}<span class="hs-chev" aria-hidden="true"></span></button></h2>'
           + block[block.index(h2) + len(h2):body_start]
           + f'\n        <div class="hs-body" id="{sid}-body"{"" if is_open else " hidden"}>'
           + block[body_start:inner_close].rstrip() + "\n        </div>\n    "
           + block[inner_close:])
    s = s[:start] + new + s[end:]

CSS = """        /* Horizon Scanner panels */
        .hs-head { margin-bottom:.5rem; }
        .hs-toggle { all:unset; box-sizing:border-box; display:flex; width:100%; align-items:center; justify-content:space-between; gap:1rem; cursor:pointer; font:inherit; color:inherit; }
        .hs-toggle:focus-visible { outline:3px solid #005ba5; outline-offset:4px; border-radius:4px; }
        .hs-chev { flex:0 0 auto; width:36px; height:36px; border-radius:50%; border:2px solid #cfd6de; position:relative; transition:transform .2s, border-color .2s; }
        .hs-chev::before { content:""; position:absolute; left:50%; top:45%; width:10px; height:10px; border-right:2.5px solid #1a1d33; border-bottom:2.5px solid #1a1d33; transform:translate(-50%, -50%) rotate(45deg); }
        .hs-toggle[aria-expanded="true"] .hs-chev { transform:rotate(180deg); border-color:#005ba5; }
        .hs-toggle:hover .hs-chev { border-color:#005ba5; }
        .hs-body { padding-top:.5rem; }
        #field-watch .section-subtitle, #field-trends .section-subtitle, #field-regions .section-subtitle { margin-bottom:.5rem; }
        #field-trends, #field-regions { padding-top:2.5rem; padding-bottom:2.5rem; }
        #field-watch { padding-bottom:2.5rem; }
"""
i = s.index("        /* Around the World */")
s = s[:i] + CSS + s[i:]

JS = """<script>
/* Horizon Scanner panels: open and close; a link to a panel opens it; the choice is remembered. */
(function () {
  const KEY = 'hs-panels';
  let saved = {}; try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  const set = (btn, open) => { btn.setAttribute('aria-expanded', String(open)); document.getElementById(btn.getAttribute('aria-controls')).hidden = !open; };
  document.querySelectorAll('.hs-toggle').forEach(btn => {
    const id = btn.getAttribute('aria-controls');
    if (id in saved) set(btn, saved[id]);
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true'; set(btn, open);
      saved[id] = open; try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {}
    });
  });
  const fromHash = () => { const sec = location.hash && document.querySelector(location.hash + ' .hs-toggle'); if (sec) set(sec, true); };
  fromHash(); window.addEventListener('hashchange', fromHash);
})();
</script>
"""
i = s.index("<script>\n/* Around the World:")
s = s[:i] + JS + s[i:]

# ---- 2. one color set
sub(".ft-up { color:#2e7d32; } .ft-down { color:#c62828; } .ft-flat { color:#5a6878; }",
    ".ft-up { color:#005ba5; } .ft-down { color:#4a5868; } .ft-flat { color:#8fa0b0; }")
sub(".fw-title:hover { color:#8B0000; text-decoration:underline; }", ".fw-title:hover { color:#005ba5; text-decoration:underline; }")
sub(".fw-rel.consistent { background:#2e7d32; } .fw-rel.tension { background:#c62828; } .fw-rel.independent-test { background:#005ba5; }",
    ".fw-rel.consistent { background:#005ba5; } .fw-rel.tension { background:#4a5868; } .fw-rel.independent-test { background:#1a1d33; }")
sub(".fw-rel.method, .fw-rel.context, .fw-rel.contact { background:#5a6878; }", ".fw-rel.method, .fw-rel.context, .fw-rel.contact { background:#8fa0b0; }")
sub("`<span class=\"ft-v ${p > 4 ? 'ft-up' : p < -4 ? 'ft-down' : 'ft-flat'}\">${p > 0 ? '+' : ''}${p}%</span>`",
    "`<span class=\"ft-v ${p > 4 ? 'ft-up' : p < -4 ? 'ft-down' : 'ft-flat'}\">${p > 4 ? '\\u25b2 ' : p < -4 ? '\\u25bc ' : ''}${p > 0 ? '+' : ''}${p}%</span>`")
sub("[['nsf', 'NSF', '#2e7d32'], ['nih', 'NIH', '#8B0000']]", "[['nsf', 'NSF', '#1a1d33'], ['nih', 'NIH', '#5a6878']]")
sub("d3.interpolateRgbBasis(['#b26a00', '#f3efe6', '#005ba5'])", "d3.interpolateRgbBasis(['#8fa0b0', '#f3f5f8', '#005ba5'])")
sub("['#eef2f6', M === 'fund' ? '#2e7d32' : '#005ba5']", "['#eef2f6', M === 'fund' ? '#1a1d33' : '#005ba5']")
sub("linear-gradient(90deg,#b26a00,#f3efe6,#005ba5)", "linear-gradient(90deg,#8fa0b0,#f3f5f8,#005ba5)")
sub("linear-gradient(90deg,#eef2f6,${M === 'fund' ? '#2e7d32' : '#005ba5'})", "linear-gradient(90deg,#eef2f6,${M === 'fund' ? '#1a1d33' : '#005ba5'})")
sub("M === 'fund' ? '#2e7d32' : '#005ba5'}\"></span>", "M === 'fund' ? '#1a1d33' : '#005ba5'}\"></span>")
# line chart: navy, blue and grays, told apart by dashes as well as shade
sub("const pal = ['#005ba5', '#c62828', '#2e7d32', '#7a5000', '#5a6878', '#8B0000'];",
    "const pal = ['#005ba5', '#1a1d33', '#005ba5', '#1a1d33', '#5a6878', '#8fa0b0'], dash = ['', '', '6 4', '6 4', '', '2 3'];")
sub(".attr('fill', 'none').attr('stroke', pal[i % 6]).attr('stroke-width', w);",
    ".attr('fill', 'none').attr('stroke', pal[i % 6]).attr('stroke-dasharray', dash[i % 6]).attr('stroke-width', w);")

left = [m for m in re.findall(r"#(?:2e7d32|c62828|8B0000|7a5000|b26a00)", s[s.index('id="field-watch"'):s.index("<!-- ── Featured Story ── -->")])]
assert not left, left
open(P, "w", encoding="utf-8").write(s)
print("media.html: panels collapsible, one color set")
