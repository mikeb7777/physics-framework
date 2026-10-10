# -*- coding: utf-8 -*-
"""Calls to action and major-donor language (Michael, 29 Sep 2026).

1. support.html, a new "Support the Research" page for major donors, foundations
   and organizations, in the terms research institutes use (founding supporters,
   restricted gifts, sponsored research, named fellowships, in-kind support, gift
   agreements, stewardship reports, recognition or anonymity, independence of
   results). It sets the stage for the planned nonprofit. Contribute stays the
   reader's honor-system page.
2. The "investor" sections on framework.html and research-opportunities.html
   become support sections linking to support.html.
3. A "Get each result when it arrives" subscribe band ends the content pages;
   each blog post ends with a one-line subscribe link.
4. Vague button labels are renamed; the home page hero keeps one primary action
   and the newsletter card gets a real button.
Run once; each edit asserts its target so a rerun fails loudly instead of doubling."""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda n: open(os.path.join(ROOT, n), encoding="utf-8").read()
W = lambda n, t: open(os.path.join(ROOT, n), "w", encoding="utf-8", newline="").write(t)


def edit(name, pairs):
    t = R(name)
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:70], t.count(old))
        t = t.replace(old, new)
    W(name, t)
    print("ok", name)


# ------------------------------------------------------------------ 1. support.html
src = R("search.html")
head = src[: src.index("<!-- Page Header -->")]
foot = src[src.index("<!-- Unified Footer -->"):]
foot = re.sub(r"<script>\s*\(function \(\) \{\s*var input = document\.getElementById\('q'\);.*?</script>\s*", "", foot, flags=re.S)
DESC = ("Support the Ic² Research Institute: founding supporters, gifts to a specific test, sponsored research, "
        "fellowships for independent researchers and in-kind support. Supporters have no say over results.")
head = head.replace("<title>Search | Ic² Research Institute</title>",
                    "<title>Support the Research | Ic² Research Institute</title>\n"
                    f"  <meta name=\"description\" content=\"{html.escape(DESC)}\">\n"
                    "  <link rel=\"canonical\" href=\"https://eequalsicsquared.com/support.html\">\n"
                    "  <meta property=\"og:title\" content=\"Support the Research\">\n"
                    f"  <meta property=\"og:description\" content=\"{html.escape(DESC)}\">\n"
                    "  <meta property=\"og:image\" content=\"https://eequalsicsquared.com/share-card.jpg?v=rgb\">")

WAYS = [
    ("#8B0000", "Founding Supporters",
     "Individuals and families who back the Institute in its founding years. With your permission, Founding Supporters are named in the Institute&rsquo;s record of its origin; anyone who prefers can give anonymously."),
    ("#005ba5", "Sponsor a test",
     "Fund a specific registered test or research program: the data analysis, the instrument time or the write-up. The gift is restricted to that work, and you receive its reports as it proceeds."),
    ("#2e7d32", "Fellowships for independent researchers",
     "Fund a named fellowship that lets an independent researcher take on a defined piece of work, with the Institute as their home institution and the same rule for everyone: state in advance what would prove the prediction wrong."),
    ("#7a5000", "Foundations and grant makers",
     "The Institute applies for grants for defined pieces of work. Each application states the prediction, the data that decides it, and what each outcome would mean, before any money is spent."),
    ("#005f6e", "Research partners",
     "Organizations can sponsor research on questions of shared interest. Methods and results of sponsored work are published. A partner may review a paper before release only to remove its own confidential information, never to change a result."),
    ("#4a5868", "In-kind support",
     "Computing time, data access, laboratory and instrument time, and professional services such as legal, accounting and design work."),
]
ways = "\n".join(f"""        <div class="sp-way" style="border-top-color:{c}"><h3>{h}</h3><p>{b}</p></div>""" for c, h, b in WAYS)

EXPECT = [
    ("A written gift agreement", "For larger gifts, a short agreement sets out the purpose, any restriction, the reports you receive and how you are recognized."),
    ("Reports on what your support made possible", "What the gift paid for, and what each funded test found, as the results arrive."),
    ("Recognition, or anonymity", "Named in the Institute&rsquo;s record and on this site, or not named at all. Your choice, and it can change later."),
    ("Independence of results", "Supporters have no say over results, what is published or when. This is written into every gift agreement and into the Institute&rsquo;s conflict of interest policy."),
    ("Open accounts", "An annual summary of what came in and what it paid for. After incorporation, the Institute&rsquo;s annual filings are public as well."),
]
expect = "\n".join(f"""          <li><strong>{h}.</strong> {b}</li>""" for h, b in EXPECT)

support_body = f"""<!-- Page Header -->
  <section id="main-content" tabindex="-1" class="page-header tp-center">
    <img src="metatron-spin.svg" class="title-cube" alt="" aria-hidden="true">
      <p class="eyebrow">Support the Research</p>
      <h1>Fund the next answer</h1>
      <p>The Institute registers each prediction before the data that tests it and publishes every result. Support from individuals, foundations and organizations decides how many of those tests can be run, and how soon.</p>
    </section>

    <main class="content-container sp">
      <style>
        .sp {{ max-width: 1000px; }}
        .sp p, .sp li {{ color: var(--text-dark); line-height: 1.75; }}
        .sp h2 {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 1.6rem; color: #1a252f; margin: 2.75rem 0 .75rem; }}
        .sp-lead {{ font-size: 1.1rem; max-width: 780px; }}
        .sp-ways {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1.25rem; }}
        .sp-way {{ background: #fff; border-top: 4px solid #8B0000; border-radius: 8px; padding: 1.2rem 1.35rem; box-shadow: 0 1px 3px rgba(0,0,0,.07); }}
        .sp-way h3 {{ font-size: 1.08rem; color: #1a252f; margin: 0 0 .4rem; }}
        .sp-way p {{ font-size: .96rem; margin: 0; }}
        .sp-expect {{ list-style: none; padding: 0; margin: 1rem 0 0; display: grid; gap: .7rem; }}
        .sp-expect li {{ background: #fff; border-left: 4px solid #005ba5; border-radius: 0 6px 6px 0; padding: .8rem 1.1rem; }}
        .sp-status {{ background: #fff; border: 1px solid #dfe3e8; border-radius: 8px; padding: 1.2rem 1.4rem; }}
        .sp-cta {{ background: #1a1d33; border-radius: 10px; padding: 1.8rem 1.6rem; margin: 2.75rem 0 1rem; text-align: center; }}
        .sp-cta h2 {{ color: #fff; margin: 0 0 .5rem; }}
        .sp-cta p {{ color: rgba(255,255,255,.85); max-width: 60ch; margin: 0 auto 1.2rem; }}
        .sp-cta .btn {{ display: inline-block; background: #8B0000; color: #fff; padding: .85rem 1.8rem; border-radius: 999px; font-weight: 700; text-decoration: none; }}
        .sp-cta .btn:hover {{ background: #a30000; }}
        .sp-cta .sp-alt {{ margin: 1rem auto 0; font-size: .92rem; }}
        .sp-cta .sp-alt a {{ color: #fff; }}
        .sp a {{ color: #005f6e; }}
      </style>

      <p class="sp-lead">Every test the Institute runs starts with a dated public record and ends with a published result. What limits the pace is not ideas but people, data and time. Support at every scale moves that limit, and every supporter can see what their support produced.</p>

      <h2>Ways to support</h2>
      <div class="sp-ways">
{ways}
      </div>

      <h2>What supporters can expect</h2>
      <ul class="sp-expect">
{expect}
      </ul>

      <h2>Tax status</h2>
      <div class="sp-status">
        <p style="margin:0">The Institute is preparing to incorporate as a US nonprofit and to apply for recognition as a 501(c)(3) public charity. Until that recognition, gifts are not tax-deductible. Supporters who would rather give with a deduction, or through a donor-advised fund or foundation, are welcome to make a pledge now; the Institute will ask for the gift once recognition is granted. See the <a href="legal.html">financial disclosures</a>.</p>
      </div>

      <div class="sp-cta">
        <h2>Talk with us about support</h2>
        <p>Tell us what you would like to make possible. We will reply with the tests and programs it could fund, and what you would receive in return.</p>
        <a class="btn" href="mailto:ic2.info@proton.me?subject=Support%20inquiry%3A%20Ic%C2%B2%20Research%20Institute">Start a conversation</a>
        <p class="sp-alt">Paying for the book, or making a smaller contribution? Use the <a href="contribute.html">Contribute page</a>.</p>
      </div>
    </main>

  """
W("support.html", head + support_body + foot)
print("wrote support.html")

# ------------------------------------------------------------------ 2. investor sections
fw = R("framework.html")
a, b = fw.index("        <!-- Why This Matters for Investors Section -->"), fw.index("  <!-- start-here:next -->")
fw = fw[:a] + """        <!-- Supporting the research -->
    <section class="band-rule content-section" id="support" style="background: white;">
    <div class="section-container" data-aos="fade-up">
    <h2 class="section-title">Why Support This Research</h2>
    <p class="content-text">Every major advance in physics has changed what people can build. Quantum mechanics led to semiconductors and MRI; relativity keeps GPS accurate. The COSMIC Framework makes predictions that will be settled by public data on known dates. Support decides how many of those tests the Institute can run, and how soon.</p>
    <div class="intro-cards-grid" style="margin-top: 2.5rem;">
        <div class="intro-card" style="background: var(--primary-color); box-shadow: 0 4px 20px rgba(139,0,0,0.2); border-bottom: 4px solid #00838f;">
            <h3>Registered Tests</h3>
            <p>Each prediction is deposited before its data and decided in public. Support pays for the analysis, the data access and the write-up of each test.</p>
        </div>
        <div class="intro-card" style="background: #1a5c2a; box-shadow: 0 4px 20px rgba(26,92,42,0.2); border-bottom: 4px solid #b01558;">
            <h3>Formalization</h3>
            <p>Deriving numbers rather than directions is skilled theoretical work, and it is what turns a direction into a prediction that can be checked to a decimal place.</p>
        </div>
        <div class="intro-card" style="background: #005ba5; box-shadow: 0 4px 20px rgba(0,91,165,0.2); border-bottom: 4px solid #f1e303;">
            <h3>Independent Researchers</h3>
            <p>Fellowships give researchers without an institution a home for a defined piece of work, held to the same rule: say in advance what would prove it wrong.</p>
        </div>
        <div class="intro-card" style="background: #005f6e; box-shadow: 0 4px 20px rgba(0,95,110,0.2); border-bottom: 4px solid #c62828;">
            <h3>Applications, If It Holds</h3>
            <p>If the predictions hold, candidate applications follow in quantum error correction, efficient computing and energy materials. They are consequences of the research, published openly, not its purpose.</p>
        </div>
    </div>
    <p class="content-text" style="margin-top: 2.5rem; text-align: center;"><a href="support.html" class="btn btn-primary">Support the Research</a></p>
    </div>
    </section>

""" + fw[b:]
assert fw.count('<a href="contribute.html" class="btn btn-outline">Investment Inquiry</a>') == 1
fw = fw.replace('<a href="contribute.html" class="btn btn-outline">Investment Inquiry</a>', '<a href="support.html" class="btn btn-outline">Support the Research</a>')
fw = fw.replace("Whether you are a funder, a researcher interested in collaboration, or simply curious about theoretical physics, we would like to hear from you.",
                "Whether you want to support the research, collaborate on it, or simply follow it, we would like to hear from you.")
W("framework.html", fw)
print("ok framework.html")

ro = R("research-opportunities.html")
a, b = ro.index("        <!-- Investment Section -->"), ro.index("        <!-- Philosophy -->")
ro = ro[:a] + """        <!-- Support Section -->
        <div style="margin-top: 5rem; padding: 3.5rem; background: #f8f9fa; border-radius: 12px; color: var(--text-dark); border: 1px solid #e0e0e0;" data-aos="fade-up">
            <div style="max-width: 800px; margin: 0 auto;">
                <p class="eyebrow eyebrow-center" style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-color); font-weight: 700; margin-bottom: 0.75rem; text-align: center;">For Supporters and Research Partners</p>
                <h2 style="font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 1.5rem; line-height: 1.3; color: var(--text-dark);">Support at the Beginning of a Research Direction</h2>

                <p style="color: var(--text-light); line-height: 1.9; margin-bottom: 1.25rem;">
                    The applications described on this page, new materials, self-healing structures, room-temperature quantum coherence and directed assembly, depend on characterizing organizing processes that biology already uses. The biology is published. The framework for pursuing it is documented, and its first pre-registered predictions are filed. How far and how fast the applications follow is an open question, and resources are what move it.
                </p>

                <p style="color: var(--text-light); line-height: 1.9; margin-bottom: 2rem;">
                    Support at this stage funds foundational research: the tests, the formalization and the people. Supporters and research partners are part of its origin, and every result it produces is published.
                </p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem; padding: 2rem; background: white; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div>
                        <div style="color: var(--primary-color); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Research Pace</div>
                        <p style="color: var(--text-light); font-size: 0.9rem; line-height: 1.6; margin: 0;">The current limit is people and time. Support directly changes how fast the substrate characterization work can proceed.</p>
                    </div>
                    <div>
                        <div style="color: var(--primary-color); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Experimental Access</div>
                        <p style="color: var(--text-light); font-size: 0.9rem; line-height: 1.6; margin: 0;">Several predictions need laboratory access and instrument time. Sponsored research and in-kind support open those doors.</p>
                    </div>
                    <div>
                        <div style="color: var(--primary-color); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Collaborative Capacity</div>
                        <p style="color: var(--text-light); font-size: 0.9rem; line-height: 1.6; margin: 0;">Independent researchers who want to contribute need a home institution. Fellowships provide it.</p>
                    </div>
                    <div>
                        <div style="color: var(--primary-color); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Formalization</div>
                        <p style="color: var(--text-light); font-size: 0.9rem; line-height: 1.6; margin: 0;">The framework needs mathematical formalization to produce the quantitative predictions experimental physics requires. That is skilled theoretical work.</p>
                    </div>
                </div>

                <div style="border-top: 1px solid #e0e0e0; padding-top: 2rem; text-align: center;">
                    <p style="color: var(--text-light); font-size: 0.9rem; margin-bottom: 1.5rem;">
                        Founding supporters, gifts to a specific test, sponsored research, fellowships and in-kind support are all described on the support page.
                    </p>
                    <a href="support.html" class="btn btn-primary" style="margin-right: 1rem;">Support the Research</a>
                    <a href="validation.html" class="btn btn-outline">View the Record</a>
                </div>
            </div>
        </div>

""" + ro[b:]
W("research-opportunities.html", ro)
print("ok research-opportunities.html")

edit("contribute.html", [(
    'Contributions are not tax-deductible. Ic² Research Institute is not a registered 501(c)(3) or other tax-exempt organization. <a href="legal.html" style="color:rgba(255,255,255,0.8);">Financial disclosures</a></small>',
    'Contributions are not tax-deductible. <a href="legal.html" style="color:rgba(255,255,255,0.8);">Financial disclosures</a></small>\n'
    '          <small style="display:block; color:rgba(255,255,255,0.85); font-size:0.85rem; line-height:1.6; margin-top:0.6rem;">Supporting at a larger scale, or on behalf of an organization? See <a href="support.html" style="color:#fff; font-weight:700;">Support the Research</a>.</small>')])

# ------------------------------------------------------------------ 3. subscribe band
BAND = """
  <!-- subscribe-band -->
  <section class="sub-band" aria-labelledby="sub-band-title">
    <style>
      .sub-band { background: #1a1d33; border-top: 4px solid #005ba5; padding: 2.75rem 1.5rem; }
      .sub-band-inner { max-width: 1100px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 1.5rem 3rem; align-items: center; justify-content: space-between; }
      .sub-band-copy { flex: 1 1 380px; min-width: 0; }
      .sub-band-eyebrow { margin: 0 0 .35rem; color: #f1e303; font: 700 .78rem 'IBM Plex Sans', sans-serif; letter-spacing: .14em; text-transform: uppercase; }
      .sub-band h2 { margin: 0 0 .45rem; color: #fff; font-family: 'Source Serif 4', Georgia, serif; font-size: 1.6rem; line-height: 1.25; }
      .sub-band-copy p.sub-band-text { margin: 0; color: rgba(255,255,255,.85); font-size: 1rem; line-height: 1.6; max-width: 56ch; }
      .sub-band form { flex: 1 1 360px; display: flex; flex-wrap: wrap; gap: .6rem; }
      .sub-band input[type=email] { flex: 1 1 220px; min-width: 0; padding: .8rem 1rem; border-radius: 999px; border: 2px solid #8fa0b0; font-size: 1rem; }
      .sub-band button { padding: .8rem 1.6rem; border: 0; border-radius: 999px; background: #8B0000; color: #fff; font-weight: 700; font-size: 1rem; cursor: pointer; }
      .sub-band button:hover { background: #a30000; }
      .sub-band .form-status { flex-basis: 100%; margin: 0; color: #fff; font-size: .9rem; }
      .sub-band .form-status a, .sub-band .sub-band-note a { color: #fff; }
      .sub-band .sub-band-note { flex-basis: 100%; margin: 0; color: rgba(255,255,255,.6); font-size: .8rem; }
      .sub-band .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
    </style>
    <div class="sub-band-inner">
      <div class="sub-band-copy">
        <p class="sub-band-eyebrow">The Quest</p>
        <h2 id="sub-band-title">Get each result when it arrives</h2>
        <p class="sub-band-text">A short update every two months, and a note whenever a test is decided.</p>
      </div>
      <form data-contact-form action="https://formspree.io/f/mnpqkjqo" method="POST" data-success="Thank you. You are subscribed, and the next update will come to the address you gave.">
        <input type="hidden" name="_subject" value="Newsletter subscription from eequalsicsquared.com">
        <input type="hidden" name="request" value="subscribe">
        <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden;">
        <label class="sr-only" for="sub-band-email">Email</label>
        <input type="email" id="sub-band-email" name="email" autocomplete="email" placeholder="Your email" required>
        <button type="submit">Subscribe</button>
        <p class="sub-band-note">Used only for these updates. <a href="privacy-policy.html">Privacy</a> &middot; <a href="unsubscribe.html">Unsubscribe any time</a></p>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>
"""
BAND_PAGES = ["about-page.html", "framework.html", "validation.html", "testing-schedule.html", "results.html",
              "quest-map.html", "instruments.html", "mission-log.html", "blog.html", "book.html",
              "blog-post-institution-and-the-idea.html", "blog-post-isolation-may-be-required.html", "blog-prime-numbers.html"]
for name in BAND_PAGES:
    t = R(name)
    if "<!-- subscribe-band -->" in t:
        print("band already on", name); continue
    i = t.find("<!-- Unified Footer -->")
    if i < 0:
        i = t.find("<footer")
    assert i > 0, name
    t = t[:i] + BAND + "\n  " + t[i:]
    if "contact-form.js" not in t:
        t = t.replace("</body>", '<script src="contact-form.js" defer></script>\n</body>', 1)
    W(name, t)
    print("band", name)

# one-line subscribe at the end of each blog post
t = R("blog.html")
POST_SUB = ('<p class="post-subscribe" style="margin:1.5rem 0 0;padding-top:1rem;border-top:1px solid rgba(0,0,0,.08);font-size:.98rem;">'
            'Get the next post, and each test result, by email. <a href="subscribe.html" style="color:#8B0000;font-weight:700;">Subscribe to The Quest &rarr;</a></p>\n')
if "post-subscribe" not in t:
    n = t.count("</article>")
    t = t.replace("</article>", POST_SUB + "</article>")
    W("blog.html", t)
    print("post subscribe lines", n)

# ------------------------------------------------------------------ 4. labels and home page
edit("index.html", [
    ('<a href="framework.html" class="btn btn-outline">Learn More</a>', '<a href="framework.html" class="btn btn-outline">Read the framework</a>'),
    ('<a href="blog.html" class="btn btn-outline">View Blog</a>', ''),
    ('<a href="subscribe.html" style="color:#8B0000; font-weight:700; text-decoration:none; border-bottom:1px solid rgba(139,0,0,.35);">Subscribe &rarr;</a>',
     '<a href="subscribe.html" style="display:inline-block; background:#005ba5; color:#fff; font-weight:700; text-decoration:none; padding:.55rem 1.3rem; border-radius:999px;">Subscribe</a>'),
])
t = R("programs-gateway.html")
n = len(re.findall(r'>Details</a>', t))
t = re.sub(r'>Details</a>', '>See the program</a>', t)
W("programs-gateway.html", t); print("programs-gateway Details renamed:", n)
edit("gallery.html", [('>Get involved</a>', '>Ways to take part</a>')])
# the index hero now has one primary (Start Here) and one secondary; a subscribe band follows the Quest section
t = R("index.html")
anchor = '<a href="quest-follow.html" class="btn btn-outline" style="color: var(--primary-color); border-color: var(--primary-color);">Follow the Quest</a>'
assert t.count(anchor) == 1
i = t.index("</section>", t.index(anchor)) + len("</section>")
t = t[:i] + BAND + t[i:]
if "contact-form.js" not in t:
    t = t.replace("</body>", '<script src="contact-form.js" defer></script>\n</body>', 1)
W("index.html", t); print("band index.html (after the Quest section)")
