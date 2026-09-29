# -*- coding: utf-8 -*-
"""Quest page headers and the footer promise (Michael, 29 Sep 2026).

1. Footer: "We publish every result." with no "including the ones that do not hold".
2. Quest pages: the head section follows the Framework and Testing pages (left
   aligned, logo mark, lead, description, Metatron's Cube turning on the right)
   on a light gray panel, with the Quest logo at the size of the COSMIC logo on
   the Framework page (86 px). The "The Quest is not an argument against
   science" paragraph is removed."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FOOTER = [("We publish every result, including the ones that do not hold.", "We publish every result."),
          ("and we publish every result, including the ones that do not hold.", "and we publish every result.")]

CSS = """  <style id="q-head">
    /* Quest title panel: the Framework page's pattern on light gray. */
    .q-head { background: #f3f4f6; color: #1a252f; padding: 4rem 2rem; text-align: left;
      position: relative; isolation: isolate; overflow: hidden; border-bottom: 1px solid #dfe3e8; }
    .q-head-inner { max-width: var(--max-width, 1200px); margin: 0 auto; }
    .q-head h1.q-head-mark { margin: 0 0 1.25rem; line-height: 1; }
    .q-head h1.q-head-mark img { height: 86px; width: auto; display: block; }
    .q-head .q-head-lead { font-size: 1.25rem; line-height: 1.7; max-width: 820px; margin: 0 0 1rem; color: #1a252f; }
    .q-head .q-head-lead strong { color: #8B0000; }
    .q-head .q-head-body { font-size: 1rem; line-height: 1.8; max-width: 820px; margin: 0; color: #4a5868; }
    .q-head .q-head-updated { font-size: .85rem; color: #5a6878; margin: 1rem 0 0; }
    .q-head-cube { position: absolute; top: 50%; right: clamp(1rem, 6vw, 7rem); z-index: -1;
      width: clamp(150px, 17vw, 230px); height: auto; opacity: .6; pointer-events: none; transform: translateY(-50%); }
    @media (max-width: 1100px) { .q-head-cube { display: none; } }
    @media (max-width: 768px) { .q-head { padding: 2.5rem 1.25rem; } .q-head h1.q-head-mark img { height: 58px; } }
  </style>
"""


def head_section(lead, body, updated=None):
    up = f'\n        <p class="q-head-updated">{updated}</p>' if updated else ""
    return f"""<section class="q-head">
      <img src="metatron-spin.svg" class="q-head-cube" alt="" aria-hidden="true">
      <div class="q-head-inner">
        <h1 class="q-head-mark"><img src="quest-logo-color.svg" alt="The Quest"></h1>
        <p class="q-head-lead">{lead}</p>
        <p class="q-head-body">{body}</p>{up}
      </div>
    </section>"""


HEADS = {
    "quest-map.html": head_section(
        "<strong>The Quest Map</strong> shows where the COSMIC Framework stands on the road every theory travels, from an idea to acceptance, rejection or modification.",
        "Every stage of that road is drawn below with what it really involves: the costs, the success rates and the sources. The map is updated with every episode of the Quest.",
        "Last updated 29 September 2026"),
    "quest-follow.html": head_section(
        "<strong>Follow the Quest</strong>: an honest, ongoing look at how a theory meets the world, through the people, the process and what is learned along the way.",
        "It is told as a video series, with a written companion here for every episode. A new episode arrives every two months, with a short special edition soon after anything significant."),
}

if __name__ == "__main__":
    for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        name = os.path.basename(p)
        t = open(p, encoding="utf-8").read()
        u = t
        for old, new in FOOTER:
            u = u.replace(old, new)
        if name in HEADS:
            u, n = re.subn(r'<section class="q-hero">.*?</section>', HEADS[name], u, count=1, flags=re.S)
            assert n == 1, name
            if 'id="q-head"' not in u:
                u = u.replace("</head>", CSS + "</head>", 1)
        if u != t:
            open(p, "w", encoding="utf-8", newline="").write(u)
            print("ok", name)
    left = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html"))
            if "including the ones that do not hold" in open(p, encoding="utf-8").read()]
    print("footer text left:", left)
