# -*- coding: utf-8 -*-
"""Simulations page becomes the Visualizations page (Michael, 6 Oct 2026): "It's the same page. But I had to
rename it because not everything is a simulation." Built from the Big TOE chat handoff
(Downloads/CLAUDE_CODE_BRIEF_Visualizations.md), merged into the existing page rather than replacing it.

- Five provenance sections, most to least data-grounded: Mapping (Observed), Simulations (Simulated),
  Models (Model), Concepts (Concept), Artist and AI Renderings (Illustration). Filter buttons, deep links
  (visualizations.html#models), and a legend. Tag colors from the site palette (no purple).
- Every existing interactive keeps its id and code, gets a provenance tag, and moves to its section.
- Every visual carries a watermark naming the Institute and the kind of visual, so it stays labeled if it
  is copied off the site.
- Corrections: pi chart carries the book's caveats and no longer reads as evidence; Element numbers fixed;
  four forces treat gravity as spacetime geometry (book Table 5); "purple" wording gone.
- New cards: the brain and cosmic web (Vazza and Feletti 2020, CC BY 4.0) and Laniakea (link only).
simulations.html becomes a redirect that keeps the #anchor. Run once, after `git mv simulations.html
visualizations.html`."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "visualizations.html")
s = open(P, encoding="utf-8").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


# ---- head and hero ----
rep("<title>Simulations. Ic² Research Institute</title>", "<title>Visualizations. Ic² Research Institute</title>")
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Maps, simulations, models, concepts and renderings of the COSMIC Framework and the physics behind it. Every visual is labeled by what kind of picture it is and where it comes from.">',
           s, count=1)
rep('<p class="eyebrow page-label">Simulations</p>', '<p class="eyebrow page-label">Visualizations</p>')
rep("<p>Interactive visualizations of the COSMIC Framework. Canvas models, 3D explorers, and interactive parameter tools across cosmology, quantum mechanics, and information theory.</p>",
    "<p>Maps, simulations, models, concepts and renderings, across cosmology, quantum mechanics and information theory. Most of them move, and you can turn them in your hands.</p>")
rep("<p>The charts below present observational and theoretical material behind the COSMIC Framework. Each is drawn from real data, from a testable prediction, or, where labeled, from the framework's equations as an illustration.</p>",
    "<p>A striking picture can look like evidence whether or not it is. Every visual here is labeled by what kind of picture it is, so you can see at a glance how much evidence stands behind it.</p>")
rep('<div class="sim-gallery" aria-label="Simulations at a glance">', '<div class="sim-gallery" aria-label="Interactive visuals at a glance">')
rep('<h2 style="margin:.25rem 0 .5rem;">Every simulation, running</h2>', '<h2 style="margin:.25rem 0 .5rem;">Every interactive, running</h2>')

# ---- extract the accordions ----
start = s.index('<div class="section-divider"><h2>Part I. Data Visualizations</h2></div>')
end_marker = '\n  </section>\n\n  <section class="content-section" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);'
end = s.index(end_marker)
region = s[start:end]
WRAP = re.compile(r"^\s*</div><!-- /\.[\w-]+ -->\s*$|^</section>\s*$", re.M)


JUNK = [r"\n\s*<!-- ═+.*?═+\s*-->", r"\n\s*<!-- ── .*? ── -->", r'\n\s*<hr class="section-rule">',
        r'\n\s*<h2 style="margin-top:8px;">.*?</h2>', r'\n\s*<p class="lead">.*?</p>',
        r'\n\s*<div class="equation">.*?</div>', r'\n\s*<div class="highlight">\s*<h3>Visualization Features:</h3>.*?</div>']


def clean(b):
    """The old page put group headings between a card's figure and its closing tags; drop them."""
    for pat in JUNK:
        b = re.sub(pat, "", b, flags=re.S)
    return b


def block(text, i):
    depth, pos = 0, i
    tok = re.compile(r"<div\b|</div>(?:<!-- /\.)?")
    for m in tok.finditer(text, i):
        if m.group(0).startswith("</div><!--"):
            continue
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return clean(WRAP.sub("", text[i:m.end()]))
    raise ValueError("unbalanced")


acc = {}
for m in re.finditer(r'<div class="foundation-accordion"[^>]*data-lazy-sim="(\w+)"', region):
    acc[m.group(1)] = block(region, m.start())
assert len(acc) == 21, sorted(acc)

TAGS = {"observed": "Observed", "simulated": "Simulated", "model": "Model", "concept": "Concept", "illustration": "Illustration"}
PROV = {"fig1": "observed", "chamber": "simulated",
        "four3d": "model", "ent3d": "model", "scram3d": "model", "bell": "model", "fig7": "model", "nowwin": "model", "phimotion": "model",
        "fig2": "concept", "fig3": "concept", "fig4": "concept", "fig5": "concept", "fig6": "concept", "peg3d": "concept",
        "rot3d": "concept", "bang3d": "concept", "bamboo": "concept", "subplanck": "concept", "nbi": "concept", "cmb": "concept"}
assert set(PROV) == set(acc)


def wm(kind, extra=""):
    return f'<div class="viz-wm" aria-hidden="true">Ic&sup2; Research Institute &middot; {TAGS[kind]}{extra}</div>'


for k, b in acc.items():
    kind = PROV[k]
    b = b.replace('class="foundation-accordion"', f'class="foundation-accordion" data-prov="{kind}"', 1)
    b = re.sub(r"(\s*</h3>)", f' <span class="tag tag-{kind}">{TAGS[kind]}</span>\\1', b, count=1)
    b = re.sub(r'(<div class="plot-container"[^>]*>)', lambda m: m.group(1) + wm(kind), b)
    assert "viz-wm" in b, k
    acc[k] = b


def edit(k, a, b):
    assert acc[k].count(a) == 1, (k, a[:70], acc[k].count(a))
    acc[k] = acc[k].replace(a, b)


# Element numbers (6C): the CMB analysis is Elements 10 and 11; quantization is Element 9; the brain-cosmos comparison is Element 7
edit("fig1", ">Element 14<", ">Elements 10 &amp; 11<")
edit("fig5", ">Element 2<", ">Element 9<")
edit("fig7", ">Elements 6 &amp; 17<", ">Element 7<") if ">Elements 6 &amp; 17<" in acc["fig7"] else edit("fig7", ">Elements 6 & 17<", ">Element 7<")

# pi chart: the book's caveats, and no reading as evidence
edit("fig1", "The COSMIC Framework interprets this systematic trend as evidence that mathematical constants are not fixed universal quantities but are coupled to the information density of their local substrate, varying measurably with the energy scale of observation.",
     "The framework's question is whether mathematical constants are coupled to the information density of their local substrate, so that they vary with the energy scale of observation. Every individual deviation is under 1&sigma;; what stands out is the trend across frequencies.")
edit("fig1", "which is a systematic trend that no established theory predicts. Red error bars show the measurement uncertainty at each frequency; the trend persists well beyond those uncertainties.",
     "a trend that no established theory predicts. Red error bars show the measurement uncertainty at each frequency.")
CAVEATS = """
      <div class="viz-caveat"><strong>Read with care.</strong> This is a preliminary, single-investigator analysis of public WMAP data. The &pi; frequency correlation is r = 0.91 (p &lt; 0.05), and the Monte Carlo false-positive rate is 0.15%, but the estimate of about 91% non-random does not account for systematic errors, and independent replication is needed. The book also records an unresolved tension between the CMB and the framework's core prediction (Element 10). Paper: <a href="https://doi.org/10.5281/zenodo.16376121" target="_blank" rel="noopener">10.5281/zenodo.16376121</a>. Data and code: <a href="https://doi.org/10.5281/zenodo.16703266" target="_blank" rel="noopener">10.5281/zenodo.16703266</a>.</div>"""
acc["fig1"] = re.sub(r'(<div class="figure-caption">.*?</div>)', lambda m: m.group(1) + CAVEATS, acc["fig1"], count=1, flags=re.S)

# four forces: gravity as spacetime geometry (book Table 5)
edit("four3d", "Gravity (gold mesh): organizes all information into hierarchical spacetime structure. The framework's claim is that these are not four separate coincidences but one information-processing architecture.",
     "Gravity (gold mesh) is drawn apart from the other three: general relativity describes it as the geometry of spacetime rather than a force. The framework proposes that it organizes information, and may emerge from information-density patterns (Element 8). The forces are established physics; the information roles are the framework's interpretation, offered to generate testable questions.")
edit("four3d", "Sim D: Strong (Store) · EM (Transmit) · Weak (Transform) · Gravity (Organize)",
     "Sim D: Strong (Store) · EM (Transmit) · Weak (Transform) · Spacetime Geometry (Organize)") if "Sim D: Strong (Store) · EM (Transmit) · Weak (Transform) · Gravity (Organize)" in acc["four3d"] else None

for k in acc:
    acc[k] = acc[k].replace("the purple torus", "the magenta torus")


# ---- new static cards ----
def card(kind_tags, title, body, meta, frame):
    tags = "".join(f'<span class="tag tag-{t}">{TAGS[t]}</span>' for t in kind_tags)
    return f"""
      <article class="viz-card" data-prov="{kind_tags[0]}">
        {frame}
        <div class="viz-body">
          <div class="viz-tags">{tags}</div>
          <h3>{title}</h3>
          {body}
          <dl class="viz-meta">{meta}</dl>
        </div>
      </article>"""


BRAIN = card(["observed", "simulated"], "The brain and the cosmic web, side by side",
    """<p>The left panel is real tissue: a section of human cerebellum under a light microscope at 40&times; magnification. The right panel is simulated: a slice of a cosmological simulation 300 million light-years across. Neither is a map of the other, which is what makes the comparison interesting.</p>
          <p>Vazza and Feletti compared the two quantitatively. Using the power spectrum, a standard cosmology tool for describing how structure is spread across scales, they found that fluctuations in the cerebellum network from 1 micrometer to 0.1 millimeter follow the same progression as matter in the cosmic web from 5 to 500 million light-years. Network measures, such as connections per node and clustering, also agreed closely. Element 7 of <em>A Quest for The Big TOE</em> asks what this shared architecture might mean.</p>""",
    """<div><dt>Source: </dt><dd>Cerebellum image: Dr. E. Zunarelli, University Hospital of Modena. Simulation: Vazza et al. (2019), <em>Astronomy &amp; Astrophysics</em>. Image via the University of Bologna.</dd></div>
            <div><dt>Paper: </dt><dd>Vazza and Feletti (2020), <em>Frontiers in Physics</em> 8. <a href="https://doi.org/10.3389/fphy.2020.525731" target="_blank" rel="noopener">doi.org/10.3389/fphy.2020.525731</a></dd></div>
            <div><dt>Rights: </dt><dd>CC BY 4.0</dd></div>
            <div><dt>In the book: </dt><dd>Figure 7-1, Element 7</dd></div>""",
    """<button class="viz-frame" type="button" aria-label="Enlarge: cerebellum tissue beside a cosmic web simulation">
          <img src="images/viz/brain-cosmic-web-vazza-feletti.jpg" alt="Left, a slice of human cerebellum tissue showing a branching network of neurons. Right, a simulated slice of the cosmic web showing dark matter filaments." data-caption="Left: human cerebellum, 40&times; light microscopy. Right: simulated cosmic web, 300 million light-years per side. Vazza and Feletti (2020), CC BY 4.0.">
          <div class="viz-wm viz-wm-credit" aria-hidden="true">Vazza &amp; Feletti 2020, CC BY 4.0 &middot; shown by Ic&sup2;</div>
        </button>""")

LANIAKEA = card(["observed"], "Laniakea, our home supercluster",
    """<p>Laniakea is the region of space whose galaxies, including the Milky Way, flow toward a shared gravitational basin. Its boundary was traced by measuring the motions of thousands of galaxies, not their positions alone. In the published visualizations, white streamlines show those flows and an envelope marks where Laniakea ends and its neighbors begin.</p>
          <p>The simulated cosmic web shows what the web looks like in general. Laniakea is the part of it we live inside.</p>""",
    """<div><dt>Source: </dt><dd>Tully, Courtois, Hoffman and Pomar&egrave;de (2014), <em>Nature</em> 513, 71. Visualization by D. Pomar&egrave;de.</dd></div>
            <div><dt>Paper: </dt><dd><a href="https://doi.org/10.1038/nature13674" target="_blank" rel="noopener">doi.org/10.1038/nature13674</a></dd></div>
            <div><dt>Rights: </dt><dd>&copy; Nature Publishing Group. Linked, not reproduced.</dd></div>""",
    '<div class="viz-frame missing" data-missing="The Laniakea visualization is on the publisher\'s site (link below)."></div>')


def section(cid, title, intro, items, empty=None):
    inner = "".join(items) if items else ""
    grid = f'<div class="viz-stack">{inner}\n      </div>' if items else ""
    note = f'<p class="empty-note">{empty}</p>' if empty else ""
    return f"""
    <div class="viz-category" id="{cid}" data-category="{cid}">
      <h2 class="category-title">{title}</h2>
      <p class="category-intro">{intro}</p>
      {note}
      {grid}
    </div>
"""


LEGEND = """
    <div class="viz-legend" id="how-to-read">
      <h2>How to read the labels</h2>
      <p>Each visual carries a tag showing where it comes from, and the same label is printed on the image itself. The sections run from pictures built directly from measurement down to pictures made only to illustrate an idea.</p>
      <ul class="legend">
        <li><span class="tag tag-observed">Observed</span><span>Built from real measurements, such as telescope surveys, galaxy motions or published data.</span></li>
        <li><span class="tag tag-simulated">Simulated</span><span>Computed from established physical laws. Realistic, but not a picture of any actual place.</span></li>
        <li><span class="tag tag-model">Model</span><span>A diagram or demonstration of structure or mechanism. It organizes ideas; the caption says whether they are established physics or the framework's interpretation.</span></li>
        <li><span class="tag tag-concept">Concept</span><span>A picture of a COSMIC Framework proposal that has not yet been tested.</span></li>
        <li><span class="tag tag-illustration">Illustration</span><span>Artist or AI rendering, made for explanation only. It is not data, and the tool is named.</span></li>
      </ul>
    </div>

    <div class="category-nav" role="group" aria-label="Show one kind of visual">
      <button class="category-btn active" type="button" data-category="all">All</button>
      <button class="category-btn" type="button" data-category="mapping">Mapping</button>
      <button class="category-btn" type="button" data-category="simulations">Simulations</button>
      <button class="category-btn" type="button" data-category="models">Models</button>
      <button class="category-btn" type="button" data-category="concepts">Concepts</button>
      <button class="category-btn" type="button" data-category="renderings">Artist and AI Renderings</button>
    </div>
"""

new = LEGEND
new += section("mapping", "Mapping",
               "Pictures built from observation. These carry the most evidential weight here, though every map still involves choices about how raw measurements become a picture.",
               [acc["fig1"], LANIAKEA])
new += section("simulations", "Simulations",
               "Computed forward from established physics. They are realistic in their statistics or their mechanics, not portraits of a specific place. The chamber model uses established acoustics only and makes no framework assumptions.",
               [acc["chamber"], BRAIN])
new += section("models", "Models",
               "Diagrams and demonstrations that organize ideas: how parts relate and what maps onto what. Some show established physics; others show the framework's interpretation of it. Each caption says which.",
               [acc[k] for k in ["four3d", "ent3d", "scram3d", "bell", "fig7", "nowwin", "phimotion"]])
new += section("concepts", "Concepts",
               "Pictures of proposals that are still open investigations. They show what the framework suggests might be true, not what has been confirmed. Each is tied to a prediction on the <a href=\"testing-schedule.html\">Testing Schedule</a> where one exists.",
               [acc[k] for k in ["fig2", "fig3", "fig4", "fig5", "fig6", "peg3d", "rot3d", "bang3d", "bamboo", "subplanck", "nbi", "cmb"]])
new += section("renderings", "Artist and AI Renderings",
               "Images made to help you picture something, not to record it. AI renderings in particular can look photographic, so every one here is labeled and credited with the tool used to make it.",
               [], empty="The first rendering, an annotated anatomy of a spinning black hole, is in preparation. The artwork will be labeled as illustration; its labels will follow general relativity.")
s = s[:start] + new + "\n    </div>" + s[end:]

# invented gradient on the equation band -> site navy
rep('<section class="content-section" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);', '<section class="content-section" style="background:#1a1d33;')

CSS = """
  <style id="viz-provenance">
    /* Provenance labels (Visualizations, 6 Oct 2026). Palette only: no purple. */
    :root { --tag-observed:#2e7d32; --tag-simulated:#005ba5; --tag-model:#7a5000; --tag-concept:#8e0c45; --tag-illustration:#8B0000; }
    .tag { display:inline-block; padding:.18rem .6rem; border-radius:4px; font-size:.74rem; font-weight:700; color:#fff; letter-spacing:.02em; vertical-align:middle; margin-left:.4rem; font-family:'IBM Plex Sans',system-ui,sans-serif; }
    .viz-tags .tag, .legend .tag { margin-left:0; }
    .foundation-header .tag { box-shadow:0 0 0 1.5px rgba(255,255,255,.9); }
    .tag-observed { background:var(--tag-observed); } .tag-simulated { background:var(--tag-simulated); }
    .tag-model { background:var(--tag-model); } .tag-concept { background:var(--tag-concept); } .tag-illustration { background:var(--tag-illustration); }
    .viz-legend { background:#1a1d33; color:#fff; border-radius:10px; padding:1.75rem 2rem; margin:0 0 2rem; }
    .viz-legend h2 { color:#f1e303; font-size:1.35rem; margin:0 0 .6rem; }
    .viz-legend p { color:rgba(255,255,255,.88); max-width:780px; margin:0 0 1.1rem; }
    .legend { list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr)); gap:.9rem 1.5rem; }
    .legend li { display:flex; gap:.7rem; align-items:flex-start; font-size:.92rem; color:rgba(255,255,255,.88); }
    .legend .tag { flex-shrink:0; margin-top:2px; }
    .category-nav { display:flex; gap:.6rem; margin:0 0 2.5rem; flex-wrap:wrap; justify-content:center; }
    .category-btn { padding:.6rem 1.1rem; background:#fff; border:2px solid #d0d5dd; border-radius:8px; font-weight:600; font-size:.92rem; cursor:pointer; color:#1a1d33; font-family:inherit; }
    .category-btn:hover { border-color:#8B0000; color:#8B0000; }
    .category-btn.active { background:#8B0000; color:#fff; border-color:#8B0000; }
    .category-btn:focus-visible, .viz-frame:focus-visible { outline:3px solid #005ba5; outline-offset:2px; }
    .viz-category { margin-bottom:3rem; scroll-margin-top:90px; }
    .category-title { font-size:1.8rem; margin:0 0 .4rem; padding-bottom:.6rem; border-bottom:3px solid var(--cat-color,#8B0000); }
    .viz-category[data-category="mapping"] { --cat-color:var(--tag-observed); }
    .viz-category[data-category="simulations"] { --cat-color:var(--tag-simulated); }
    .viz-category[data-category="models"] { --cat-color:var(--tag-model); }
    .viz-category[data-category="concepts"] { --cat-color:var(--tag-concept); }
    .viz-category[data-category="renderings"] { --cat-color:var(--tag-illustration); }
    .category-intro { color:#5a6878; max-width:820px; margin:.9rem 0 1.5rem; }
    .viz-stack > * { margin-bottom:1.25rem; }
    .empty-note { background:#fff; border:2px dashed #d0d5dd; border-radius:10px; padding:1.5rem; color:#5a6878; max-width:820px; }
    .viz-card { background:#fff; border-radius:10px; overflow:hidden; border-top:5px solid var(--cat-color,#8B0000); box-shadow:0 2px 10px rgba(0,0,0,.06); }
    .viz-frame { display:block; width:100%; background:#0a0f1e; border:none; padding:0; cursor:zoom-in; position:relative; }
    .viz-frame img { display:block; width:100%; height:auto; }
    .viz-frame.missing { cursor:default; min-height:200px; display:flex; align-items:center; justify-content:center; }
    .viz-frame.missing::after { content:attr(data-missing); color:rgba(255,255,255,.75); font-size:.92rem; padding:1.5rem; text-align:center; }
    .viz-body { padding:1.3rem 1.5rem 1.5rem; }
    .viz-body h3 { font-size:1.2rem; margin:.6rem 0; }
    .viz-body p { color:#4a5868; font-size:.95rem; margin:0 0 .75rem; }
    .viz-tags { display:flex; gap:.4rem; flex-wrap:wrap; }
    .viz-meta { margin:.9rem 0 0; padding-top:.8rem; border-top:1px solid #e0e0e0; font-size:.84rem; color:#4a5868; }
    .viz-meta dt { font-weight:700; display:inline; color:#1a1d33; } .viz-meta dd { display:inline; margin:0; }
    .viz-meta div { margin-bottom:.25rem; } .viz-meta a { color:#005ba5; }
    .viz-caveat { margin:1rem 0 0; padding:1rem 1.25rem; background:#fff8e1; border-left:4px solid #f1e303; border-radius:0 6px 6px 0; color:#1a1d33; font-size:.9rem; line-height:1.7; }
    .viz-caveat a { color:#005ba5; }
    /* Watermark: names the Institute and the kind of visual, on the image itself */
    .viz-wm { position:absolute; right:10px; bottom:8px; z-index:5; pointer-events:none; font:600 11px/1.2 'IBM Plex Sans',system-ui,sans-serif; letter-spacing:.04em; color:rgba(255,255,255,.82); background:rgba(10,15,30,.55); padding:3px 7px; border-radius:3px; }
    .viz-lightbox { position:fixed; inset:0; background:rgba(10,15,30,.94); display:none; align-items:center; justify-content:center; z-index:2000; padding:2rem; }
    .viz-lightbox.open { display:flex; }
    .viz-lightbox figure { max-width:1400px; width:100%; margin:0; position:relative; }
    .viz-lightbox img { width:100%; max-height:80vh; object-fit:contain; display:block; }
    .viz-lightbox figcaption { color:rgba(255,255,255,.85); margin-top:1rem; text-align:center; font-size:.95rem; }
    .viz-lightbox-close { position:absolute; top:1rem; right:1.25rem; background:none; border:none; color:#fff; font-size:2.2rem; cursor:pointer; line-height:1; }
    @media (max-width:600px) { .viz-legend { padding:1.25rem; } .category-title { font-size:1.45rem; } .viz-wm { font-size:10px; } }
  </style>
"""
rep("</head>", CSS + "</head>")

JS = """
<div class="viz-lightbox" role="dialog" aria-modal="true" aria-label="Enlarged image">
  <button class="viz-lightbox-close" type="button" aria-label="Close">&times;</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
</div>
<script>
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var btns = document.querySelectorAll('.category-btn');
  function show(cat) {
    btns.forEach(function (b) { b.classList.toggle('active', b.dataset.category === cat); b.setAttribute('aria-pressed', b.dataset.category === cat); });
    document.querySelectorAll('.viz-category').forEach(function (sec) { sec.style.display = (cat === 'all' || sec.dataset.category === cat) ? '' : 'none'; });
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      show(b.dataset.category);
      history.replaceState(null, '', b.dataset.category === 'all' ? location.pathname : '#' + b.dataset.category);
    });
  });
  function applyHash() {
    var id = location.hash.replace('#', '');
    if (!id) return;
    if (document.querySelector('.category-btn[data-category="' + id + '"]')) {
      show(id);
      document.getElementById(id).scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
      return;
    }
    var el = document.getElementById(id);                 /* an old link to one visual: open it */
    var a = el && el.closest('.foundation-accordion');
    if (a && !a.classList.contains('active')) { var h = a.querySelector('.foundation-header'); if (h) h.click(); }
  }
  window.addEventListener('hashchange', applyHash);
  window.addEventListener('load', applyHash);

  document.querySelectorAll('.viz-frame img').forEach(function (img) {
    function missing() {
      var f = img.closest('.viz-frame');
      f.classList.add('missing'); f.dataset.missing = 'Image to be added'; f.disabled = true; img.remove();
      var w = f.querySelector('.viz-wm'); if (w) w.remove();
    }
    if (img.complete && img.naturalWidth === 0) missing(); else img.addEventListener('error', missing);
  });
  var lb = document.querySelector('.viz-lightbox'), lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption'), last = null;
  document.querySelectorAll('button.viz-frame').forEach(function (f) {
    f.addEventListener('click', function () {
      var img = f.querySelector('img'); if (!img) return;
      last = f; lbImg.src = img.src; lbImg.alt = img.alt; lbCap.textContent = img.dataset.caption || '';
      lb.classList.add('open'); lb.querySelector('.viz-lightbox-close').focus();
    });
  });
  function close() { lb.classList.remove('open'); if (last) last.focus(); }
  lb.querySelector('.viz-lightbox-close').addEventListener('click', close);
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && lb.classList.contains('open')) close(); });
})();
</script>
"""
i = s.rindex("</body>")
s = s[:i] + JS + s[i:]
s = s.replace('<meta property="og:url" content="https://eequalsicsquared.com/simulations.html">', '<meta property="og:url" content="https://eequalsicsquared.com/visualizations.html">')
s = s.replace('<meta property="og:title" content="Simulations. Ic² Research Institute">', '<meta property="og:title" content="Visualizations. Ic² Research Institute">')
s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Maps, simulations, models, concepts and renderings, each labeled by what kind of picture it is and where it comes from.">', s, count=1)
for k in ("4D Framework", "3D Framework Simulations", "Visualization Features", "Total Framework Equation"):
    assert k not in s, k
open(P, "w", encoding="utf-8").write(s)

REDIRECT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Visualizations. Ic² Research Institute</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="https://eequalsicsquared.com/visualizations.html">
  <script>location.replace('visualizations.html' + location.hash);</script>
  <meta http-equiv="refresh" content="0; url=visualizations.html">
</head>
<body>
  <p>The Simulations page is now <a href="visualizations.html">Visualizations</a>.</p>
</body>
</html>
"""
open(os.path.join(ROOT, "simulations.html"), "w", encoding="utf-8").write(REDIRECT)
print("ok", len(acc), "visuals")
