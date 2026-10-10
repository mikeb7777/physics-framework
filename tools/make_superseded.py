# -*- coding: utf-8 -*-
"""superseded.html: the record of five withdrawn press releases (Michael,
29 Sep 2026: "keep superseded only"). Built on search.html's frame so the
header and footer match the site; the search script is not carried over."""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "search.html"), encoding="utf-8").read()
head = src[: src.index("<!-- Page Header -->")]
foot = src[src.index("<!-- Unified Footer -->"):]
# drop the search script (the block that reads search-index.json)
foot = re.sub(r"<script>\s*\(function \(\) \{\s*var input = document\.getElementById\('q'\);.*?</script>\s*", "", foot, flags=re.S)

TITLE = "Superseded press releases | Ic² Research Institute"
DESC = ("Five press releases from October 2025 called results validated predictions. No dated record "
        "predates those results, so they are withdrawn. What they said, and what changed.")
head = head.replace("<title>Search | Ic² Research Institute</title>",
                    f"<title>{TITLE}</title>\n  <meta name=\"description\" content=\"{html.escape(DESC)}\">\n"
                    f"  <link rel=\"canonical\" href=\"https://eequalsicsquared.com/superseded.html\">\n"
                    f"  <meta property=\"og:title\" content=\"Superseded press releases\">\n"
                    f"  <meta property=\"og:description\" content=\"{html.escape(DESC)}\">\n"
                    f"  <meta property=\"og:image\" content=\"https://eequalsicsquared.com/share-card.jpg?v=rgb\">")

RELEASES = [
    ("28 October 2025", "The COSMIC Framework Achieves Perfect Validation Score Across Four Independent Breakthrough Discoveries",
     "The score is withdrawn. No dated record of the predictions survives from before the results. The four results it counted "
     "are listed in the <a href=\"results.html\">Results Registry</a> as consistent with the framework and recorded after the data, "
     "not as predictions made in advance."),
    ("28 October 2025", "Prime Number Logic Gates: Framework's Information Architecture Prediction Validated",
     "Not counted as a validated prediction. No dated record survives from before the cited studies, and those studies did not "
     "test what the prediction specified."),
    ("28 October 2025", "Consciousness Signatures Detected in Neural Systems: Framework Threshold Prediction Confirmed",
     "The detection it describes is not counted in the registry of tested predictions."),
    ("28 October 2025", "Computational Boundaries Observed in Quantum Scaling Studies: Framework Limits Confirmed",
     "The observation it describes is not counted in the registry of tested predictions."),
    ("31 October 2025", "Three Framework Predictions Tested by Independent Experiments",
     "The results are consistent with the framework; they were not predictions recorded before the results. The release also "
     "cited earlier dates (5 March 2024, 12 August 2024, 15 January 2025) for which no record survives."),
]
items = "\n".join(
    f"""      <li class="ss-item">
        <p class="ss-date">{d}</p>
        <p class="ss-claim">&ldquo;{html.escape(t)}&rdquo;</p>
        <p class="ss-found"><strong>What the audit found.</strong> {f}</p>
      </li>""" for d, t, f in RELEASES)

body = f"""<!-- Page Header -->
  <section id="main-content" tabindex="-1" class="page-header tp-center">
    <img src="metatron-spin.svg" class="title-cube" alt="" aria-hidden="true">
      <p class="eyebrow">Corrections</p>
      <h1>Superseded press releases</h1>
      <p>Five press releases from October 2025 described results as validated predictions. They were not, and they are withdrawn. This page keeps the record of what they said and why.</p>
    </section>

    <main class="content-container ss">
      <style>
        .ss {{ max-width: 820px; }}
        .ss-lead {{ font-size: 1.1rem; line-height: 1.75; color: var(--text-dark); margin: 0 0 1.75rem; }}
        .ss-list {{ list-style: none; padding: 0; margin: 0 0 2.5rem; }}
        .ss-item {{ background: #fff; border-left: 4px solid #8B0000; border-radius: 0 6px 6px 0; padding: 1.1rem 1.35rem; margin: 0 0 1rem; box-shadow: 0 1px 3px rgba(0,0,0,.06); }}
        .ss-date {{ font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #5a6878; margin: 0 0 .35rem; }}
        .ss-claim {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 1.12rem; line-height: 1.45; color: #1a252f; margin: 0 0 .6rem; text-decoration: line-through; text-decoration-color: rgba(139,0,0,.55); }}
        .ss-found {{ font-size: .98rem; line-height: 1.7; color: var(--text-dark); margin: 0; }}
        .ss-found a, .ss-next a {{ color: #005f6e; }}
        .ss-next {{ background: #005ba5; border-bottom: 4px solid #f1e303; border-radius: 8px; padding: 1.4rem 1.5rem; color: #fff; }}
        .ss-next h2 {{ color: #fff; font-size: 1.35rem; margin: 0 0 .6rem; }}
        .ss-next p {{ color: #fff; line-height: 1.7; margin: 0; }}
        .ss-next a {{ color: #fff; text-decoration: underline; }}
      </style>
      <p class="ss-lead">In September 2026 the Institute audited every earlier claim that a prediction had come before its result. None of the dated records the releases relied on survives from before the results, so none of these results counts as a prediction made in advance. The releases are kept here, struck through, rather than quietly deleted: a claim that is withdrawn in the open stays part of the record.</p>
      <ol class="ss-list">
{items}
      </ol>
      <div class="ss-next">
        <h2>What changed</h2>
        <p>Since September 2026, every prediction is deposited in a dated public archive before its data exists, with a permanent DOI, so the order of events can be checked by anyone. The first two, COSMIC-005 and COSMIC-007, were registered on 12 September 2026. See the <a href="results.html">Results Registry</a>, the <a href="zenodo-papers.html">Zenodo archive</a> and the <a href="legal.html#open-science">Open Science Policy</a>.</p>
      </div>
    </main>

  """
open(os.path.join(ROOT, "superseded.html"), "w", encoding="utf-8", newline="").write(head + body + foot)
print("wrote superseded.html")
