# -*- coding: utf-8 -*-
"""quest-guide.html: the Quest Guide, stage 1 (Michael, 29 Sep 2026: the Quest
Map should be more than an illustration; link LaTeX, arXiv, journals and
preprint servers; describe the gates, the workarounds and what notable people
did; "This does something a search can't").

Stage 1: every gate on the route with how it works / the gate / the way
through / where to go; the tools of the trade; where to publish. Later stages
(funding in depth, the academic and graduate route, the industry route, notable
routes, the Institute's own route) are listed as coming.
Facts checked 29 September 2026; sources are the linked pages. Built on the
Quest frame (quest-map.html), like knowledge-tree.html."""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quest_header import head_section

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "quest-map.html"), encoding="utf-8").read()
MAIN = '<main id="main-content" tabindex="-1">'
head = src[: src.index(MAIN) + len(MAIN)]
foot = src[src.index("</main>"):]
TITLE = "The Quest Guide | Ic² Research Institute"
DESC = ("Every gate on the road from an idea to a published physics result: how it works, the way through, "
        "and where to go. arXiv endorsement, journals, preprint servers, public data and the tools of the trade.")
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(DESC)}">', head, count=1)
head = head.replace('href="https://eequalsicsquared.com/quest-map.html"', 'href="https://eequalsicsquared.com/quest-guide.html"')
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\1The Quest Guide', head)
head = head.replace('<li><a href="quest-map.html" aria-current="page">Map</a></li>', '<li><a href="quest-map.html">Map</a></li>')
if 'href="quest-guide.html"' in head:
    head = head.replace('<li><a href="quest-guide.html">Guide</a></li>', '<li><a href="quest-guide.html" aria-current="page">Guide</a></li>')
else:
    head = head.replace('<li><a href="quest-map.html">Map</a></li>',
                        '<li><a href="quest-map.html">Map</a></li>\n            <li><a href="quest-guide.html" aria-current="page">Guide</a></li>', 1)
head = head.replace('<li><a href="quest-map.html?start=1" aria-current="page">', '<li><a href="quest-map.html?start=1">')


def link(label, url):
    ext = url.startswith("http")
    rel = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="qg-go" href="{url}"{rel}>{label}</a>'


# id, title, how it works, the gate, the way through, [(label, url)]
GATES = [
    ("g-idea", "The idea",
     "An idea becomes science when it is written as a claim that data could contradict.",
     "Nobody reviews an idea. Until it is stated as a testable claim, there is nothing for anyone to check, fund or publish.",
     "Write the claim, the data that would decide it, and what each outcome would mean. Date it in a public archive so the order of events can be checked later.",
     [("Zenodo", "https://zenodo.org"), ("OSF Registries", "https://osf.io/registries"), ("The Knowledge Tree", "knowledge-tree.html")]),
    ("g-money", "The money",
     "Research grants are awarded to institutions, which then employ the researcher. Panels judge the applicant as well as the idea.",
     "Most programs require an institution to receive the money, and many require the lead researcher to hold a faculty-level post. FQxI&rsquo;s grants, for example, accept independent researchers only as co-investigators, not as the lead.",
     "Affiliate with a body that accepts independent scholars; join a proposal led by a faculty member as co-investigator; ask for small, specific grants; or work with a fiscal sponsor, a nonprofit that receives a grant on a project&rsquo;s behalf.",
     [("NCIS", "https://www.ncis.org"), ("Ronin Institute", "https://ronininstitute.org"), ("FQxI programs", "https://fqxi.org/programs/")]),
    ("g-prereg", "Registering the prediction",
     "A pre-registration fixes the claim, the measure and the decision rule before the data exists.",
     "There is no gate: physics rarely requires it, so it is easy to skip. The cost of skipping is that nobody can tell a prediction from a story told afterward.",
     "Deposit the record with a permanent DOI before the data arrives. Some journals now accept Registered Reports, where the method is reviewed and accepted before the results exist.",
     [("OSF Registries", "https://osf.io/registries"), ("Zenodo", "https://zenodo.org"), ("Registered Reports", "https://www.cos.io/initiatives/registered-reports")]),
    ("g-data", "The data",
     "Large instruments are run by collaborations. Observing time is awarded by proposal, mostly to members.",
     "Instrument time is the real currency of experimental physics, and an independent cannot usually apply for it.",
     "Predict something a survey will measure anyway, register it before the release, and use the public data when it arrives. Many of the largest experiments publish their data to everyone at once.",
     [("DESI data", "https://data.desi.lbl.gov"), ("LIGO/Virgo/KAGRA open data", "https://gwosc.org"), ("CERN Open Data", "https://opendata.cern.ch"),
      ("Planck Legacy Archive", "https://pla.esac.esa.int"), ("MAST (Hubble, Webb)", "https://archive.stsci.edu"), ("SDSS", "https://www.sdss.org"), ("The Instruments", "instruments.html")]),
    ("g-check", "The internal check",
     "Inside an institution, a result is questioned by colleagues long before a referee sees it.",
     "An independent researcher has no corridor. Errors that a colleague would catch in five minutes reach the journal instead.",
     "Ask narrow questions about one step, not the whole idea; post the derivation where others can check it; recruit a statistician for the analysis. Physics Stack Exchange answers precise questions about established physics and closes posts that promote a personal theory, so ask about a single step.",
     [("Physics Stack Exchange", "https://physics.stackexchange.com"), ("PubPeer", "https://pubpeer.com"), ("Join the Institute", "join.html")]),
    ("g-arxiv", "The preprint server",
     "arXiv is where physics papers appear first, usually before or alongside journal submission. Moderators check that a paper is on topic and scholarly; it is not peer review.",
     "Since 21 January 2026, a university email address alone no longer qualifies a new author. A new submitter needs either prior authorship in that subject area plus an institutional address, or a personal endorsement from an established arXiv author in the same area.",
     "Ask for endorsement from an author whose work you cite and who can see the paper is serious; send the paper, not a request alone. Meanwhile, Zenodo and OSF Preprints give the paper a DOI and a date, though far fewer physicists read them.",
     [("arXiv endorsement", "https://info.arxiv.org/help/endorsement.html"), ("arXiv policy update, 2026", "https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/"), ("OSF Preprints", "https://osf.io/preprints"), ("Zenodo", "https://zenodo.org")]),
    ("g-submit", "Journal submission",
     "An editor reads the paper first and decides whether to send it to referees.",
     "Many papers are returned without review (&ldquo;desk rejection&rdquo;) because of scope, format or an unfamiliar author, sometimes within days.",
     "Choose a journal whose recent issues contain papers like yours; follow its template exactly; write a cover letter that states the claim and why this journal. Journals with open review publish the reports, so the reasoning is visible either way.",
     [("SciPost", "https://scipost.org"), ("Open Journal of Astrophysics", "https://astro.theoj.org"), ("Foundations of Physics", "https://link.springer.com/journal/10701"), ("Think. Check. Submit.", "https://thinkchecksubmit.org")]),
    ("g-review", "Peer review",
     "Two or three referees, usually anonymous, report to the editor, who decides.",
     "The decision rests on a few people, and their reports are usually never seen by anyone else.",
     "Answer every point in writing, change what is right, and explain what is not. Open-review journals publish the reports and replies, which protects both sides.",
     [("SciPost open review", "https://scipost.org"), ("PubPeer", "https://pubpeer.com")]),
    ("g-reject", "Rejection and resubmission",
     "Most papers are rejected at least once. Revise and resubmit is the normal path, not a failure of it.",
     "Each round takes months, and each journal has its own format.",
     "Keep every version public with dates (arXiv versions, Zenodo versions), move to the next journal with the reports addressed, and record what changed and why.",
     [("Zenodo versioning", "https://help.zenodo.org"), ("arXiv", "https://arxiv.org")]),
    ("g-sigma", "How strong is strong enough",
     "Physics reports the strength of a result in sigma. Three sigma is called evidence; five sigma, a chance of about one in 3.5 million of a fluke, is the convention for a discovery.",
     "A result below five sigma is not a discovery, however suggestive.",
     "State the measure and the threshold before the data, as a registered prediction does, and report the significance whichever way it comes out.",
     [("The Validation page", "validation.html")]),
    ("g-open", "Publication and open access",
     "Accepted papers are published either behind a subscription or open to all readers, often for an article processing charge.",
     "Open-access charges run to thousands of dollars per paper, which an unfunded author pays personally.",
     "Publish in a diamond open-access journal, free to authors and readers; ask for a fee waiver; or keep the accepted version open on arXiv or Zenodo where the journal allows.",
     [("DOAJ (filter: no charges)", "https://doaj.org"), ("OpenAPC fees data", "https://treemaps.openapc.net"), ("SciPost", "https://scipost.org"), ("Open Journal of Astrophysics", "https://astro.theoj.org")]),
    ("g-after", "After publication",
     "A published paper is found through indexes, cited, questioned and built on.",
     "A paper nobody can find does not enter the conversation.",
     "Link every paper to an ORCID record; claim it on Google Scholar, and on INSPIRE (high-energy physics) or NASA ADS (astronomy); keep the data and code public with a DOI.",
     [("ORCID", "https://orcid.org"), ("Google Scholar", "https://scholar.google.com"), ("INSPIRE", "https://inspirehep.net"), ("NASA ADS", "https://ui.adsabs.harvard.edu")]),
]

TOOLS = [
    ("LaTeX, in the browser", "Overleaf", "Physics is written in LaTeX. Overleaf runs it online with templates for most journals; a free plan covers single authors.", "https://www.overleaf.com"),
    ("LaTeX, on your computer", "TeX Live or MiKTeX", "Free installations for offline work. arXiv asks for the TeX source of papers written in TeX, not only the PDF.", "https://tug.org/texlive/"),
    ("References", "Zotero", "Free reference manager that exports BibTeX for LaTeX and collects papers from arXiv and journals in one click.", "https://www.zotero.org"),
    ("Your identity", "ORCID", "A permanent researcher ID that journals, arXiv and funders read. Free.", "https://orcid.org"),
    ("Dated records and DOIs", "Zenodo", "Free archive run by CERN. Every upload gets a DOI and a date; versions are kept.", "https://zenodo.org"),
    ("Registrations and projects", "OSF", "Free platform for pre-registration, project files and preprints.", "https://osf.io"),
    ("Code", "GitHub with Zenodo", "Version control for analysis code; linking a repository to Zenodo gives each release a DOI.", "https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content"),
    ("Literature", "INSPIRE and NASA ADS", "The databases physicists and astronomers actually search, with citation tracking.", "https://inspirehep.net"),
]

PREPRINTS = [
    ("arXiv", "Physics, mathematics, computer science", "Endorsement for new authors (2026 rules above)", "The one most physicists read daily.", "https://arxiv.org"),
    ("OSF Preprints", "All fields", "Light moderation", "DOI and date; small physics readership.", "https://osf.io/preprints"),
    ("Zenodo", "All fields, any output", "None beyond basic checks", "DOI, versions and data together; read mainly through links.", "https://zenodo.org"),
    ("viXra", "Any", "No moderation", "Accepts everything; physicists rarely read it, so it does not solve the reach problem.", "https://vixra.org"),
]

JOURNALS = [
    ("SciPost Physics", "All of physics", "Free to publish and to read", "Open: reports and replies are public", "https://scipost.org"),
    ("Open Journal of Astrophysics", "Astrophysics and cosmology", "Free to publish and to read (arXiv overlay)", "Conventional", "https://astro.theoj.org"),
    ("Foundations of Physics", "Foundational and conceptual physics", "Subscription, with an optional open-access charge", "Conventional", "https://link.springer.com/journal/10701"),
    ("Physical Review journals (APS)", "All of physics", "Subscription, with an optional open-access charge", "Conventional", "https://journals.aps.org"),
    ("Journal of Cosmology and Astroparticle Physics", "Cosmology", "Subscription, with an optional open-access charge", "Conventional", "https://iopscience.iop.org/journal/1475-7516"),
]

COMING = [
    ("Funding in depth", "Who funds independent work, how panels decide, fiscal sponsorship, and what an application really costs."),
    ("The academic route", "From a degree to graduate school, the advisor, qualifying exams, research and teaching assistantships, the postdoc and a faculty post, and where graduate students find help."),
    ("The industry route", "Research inside a company: patents before publication, confidentiality, and who owns the result."),
    ("Routes that went another way", "Sourced accounts of people who reached the result by an unusual road, from the patent office to the preprint server."),
    ("The Institute&rsquo;s own route", "Each milestone as it happens: recognition, endorsement, incorporation, the first grant application and its answer."),
]


def gate_html(i, g):
    gid, title, how, gate, way, links = g
    chips = " ".join(link(l, u) for l, u in links)
    return f"""        <article class="qg-gate" id="{gid}">
          <p class="qg-num">Gate {i}</p>
          <h3>{title}</h3>
          <dl>
            <dt>How it works</dt><dd>{how}</dd>
            <dt class="qg-wall">The gate</dt><dd>{gate}</dd>
            <dt class="qg-way">The way through</dt><dd>{way}</dd>
            <dt>Where to go</dt><dd class="qg-links">{chips}</dd>
          </dl>
        </article>"""


gates = "\n".join(gate_html(i + 1, g) for i, g in enumerate(GATES))
jump = " ".join(f'<a href="#{g[0]}">{i + 1}. {g[1]}</a>' for i, g in enumerate(GATES))
TOOL_LABEL = {"TeX Live or MiKTeX": "Get TeX Live", "GitHub with Zenodo": "How to cite code", "INSPIRE and NASA ADS": "Open INSPIRE"}
tools = "\n".join(f"""        <div class="qg-tool"><p class="qg-kind">{k}</p><h3>{n}</h3><p>{d}</p>{link(TOOL_LABEL.get(n, "Open " + n), u)}</div>""" for k, n, d, u in TOOLS)
pre_rows = "\n".join(f"<tr><th scope=\"row\"><a href=\"{u}\" target=\"_blank\" rel=\"noopener\">{n}</a></th><td>{f}</td><td>{m}</td><td>{note}</td></tr>" for n, f, m, note, u in PREPRINTS)
jr_rows = "\n".join(f"<tr><th scope=\"row\"><a href=\"{u}\" target=\"_blank\" rel=\"noopener\">{n}</a></th><td>{s}</td><td>{c}</td><td>{r}</td></tr>" for n, s, c, r, u in JOURNALS)
coming = "\n".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in COMING)

HEAD = head_section(
    "<strong>The Quest Guide</strong>: every gate on the road from an idea to a published result, how it works, the way through, and where to go.",
    "The Quest Map shows the road. This guide walks it, one gate at a time, with the tools, the servers, the journals and the public data an independent researcher can use today.",
    "Checked 29 September 2026")

body = f"""
    {HEAD}

    <section class="q-section">
    <div class="q-inner qg">
      <style>
        .qg > p {{ color: rgba(255,255,255,.86); line-height: 1.75; max-width: 780px; }}
        .qg h2 {{ font-family: 'Source Serif 4', Georgia, serif; color: #fff; font-size: 1.85rem; margin: 3rem 0 .6rem; }}
        .qg-jump {{ display: flex; flex-wrap: wrap; gap: .45rem; margin: 1.25rem 0 0; }}
        .qg-jump a {{ font-size: .88rem; color: #fff; background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.18); border-radius: 999px; padding: .3rem .8rem; text-decoration: none; }}
        .qg-jump a:hover {{ background: rgba(255,255,255,.18); }}
        .qg-gates {{ display: grid; gap: 1rem; margin-top: 1.25rem; }}
        .qg-gate {{ background: #fff; border-radius: 8px; padding: 1.2rem 1.4rem; scroll-margin-top: 110px; }}
        .qg-num {{ margin: 0; font: 700 .75rem 'IBM Plex Sans', sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #8B0000; }}
        .qg-gate h3 {{ font-family: 'Source Serif 4', Georgia, serif; color: #1a252f; font-size: 1.3rem; margin: .1rem 0 .7rem; }}
        .qg-gate dl {{ display: grid; grid-template-columns: 11rem 1fr; gap: .55rem 1.2rem; margin: 0; }}
        .qg-gate dt {{ font: 700 .78rem 'IBM Plex Sans', sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #4a5868; padding-top: .2rem; }}
        .qg-gate dt.qg-wall {{ color: #8B0000; }}
        .qg-gate dt.qg-way {{ color: #2e7d32; }}
        .qg-gate dd {{ margin: 0; color: #2c3e50; line-height: 1.7; }}
        .qg-links {{ display: flex; flex-wrap: wrap; gap: .4rem; }}
        a.qg-go {{ display: inline-block; font-size: .88rem; font-weight: 600; color: #005ba5; border: 1.5px solid #005ba5; border-radius: 999px; padding: .2rem .75rem; text-decoration: none; }}
        a.qg-go:hover {{ background: #005ba5; color: #fff; }}
        .qg-tools {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1.25rem; }}
        .qg-tool {{ background: #fff; border-radius: 8px; padding: 1rem 1.2rem; border-top: 4px solid #005ba5; }}
        .qg-tool:nth-child(3n+2) {{ border-top-color: #2e7d32; }}
        .qg-tool:nth-child(3n) {{ border-top-color: #c62828; }}
        .qg-kind {{ margin: 0; font: 700 .72rem 'IBM Plex Sans', sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #4a5868; }}
        .qg-tool h3 {{ font-size: 1.1rem; color: #1a252f; margin: .15rem 0 .35rem; }}
        .qg-tool p {{ color: #2c3e50; font-size: .95rem; line-height: 1.6; margin: 0 0 .7rem; }}
        .qg-table-wrap {{ overflow-x: auto; margin-top: 1rem; }}
        .qg table {{ width: 100%; min-width: 640px; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; }}
        .qg th, .qg td {{ text-align: left; padding: .7rem .9rem; border-bottom: 1px solid #e3e9ee; color: #2c3e50; font-size: .95rem; line-height: 1.5; vertical-align: top; }}
        .qg thead th {{ background: #2d4053; color: #fff; font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; }}
        .qg tbody th a {{ color: #005ba5; font-weight: 700; }}
        .qg h3.qg-sub {{ color: #fff; font-size: 1.2rem; margin: 1.75rem 0 .2rem; }}
        .qg-check {{ background: #fff; border-left: 5px solid #7a5000; border-radius: 0 8px 8px 0; padding: 1rem 1.3rem; margin-top: 1rem; }}
        .qg-check p, .qg-check li {{ color: #2c3e50; line-height: 1.7; }}
        .qg-check ul {{ margin: .4rem 0 0; padding-left: 1.2rem; }}
        .qg-check a {{ color: #005f6e; }}
        .qg-coming {{ color: rgba(255,255,255,.86); line-height: 1.75; padding-left: 1.2rem; max-width: 780px; }}
        .qg-coming strong {{ color: #fff; }}
        .qg > p a {{ color: #f1e303; }}
        @media (max-width: 700px) {{ .qg-gate dl {{ grid-template-columns: 1fr; gap: .2rem; }} .qg-gate dd {{ margin-bottom: .5rem; }} }}
      </style>

      <p>Every result in physics passes the same gates, whichever road it starts on. Inside a university most of them are opened by the institution without the researcher noticing. Outside, each one has to be opened by hand. For every gate this guide gives four things: how it works, where it stops people, the way through, and where to go next.</p>
      <nav class="qg-jump" aria-label="The gates">{jump}</nav>

      <h2>The gates</h2>
      <div class="qg-gates">
{gates}
      </div>

      <h2>Tools of the trade</h2>
      <p>What working physicists actually use, and what each costs. Everything here is free or has a free tier.</p>
      <div class="qg-tools">
{tools}
      </div>

      <h2>Where to publish</h2>
      <h3 class="qg-sub">Preprint servers</h3>
      <div class="qg-table-wrap"><table>
        <thead><tr><th scope="col">Server</th><th scope="col">Fields</th><th scope="col">Moderation</th><th scope="col">What it gives you</th></tr></thead>
        <tbody>
{pre_rows}
        </tbody>
      </table></div>

      <h3 class="qg-sub">Journals</h3>
      <p>A starting list for foundational physics and cosmology, not a ranking. Read a few recent papers in any journal before submitting; scope matters more than prestige.</p>
      <div class="qg-table-wrap"><table>
        <thead><tr><th scope="col">Journal</th><th scope="col">Scope</th><th scope="col">Cost to authors</th><th scope="col">Review</th></tr></thead>
        <tbody>
{jr_rows}
        </tbody>
      </table></div>

      <div class="qg-check">
        <p><strong>Checking a journal before you submit.</strong> Some publishers take fees without real review. The warning signs:</p>
        <ul>
          <li>An unsolicited email inviting you to submit, often with flattering language.</li>
          <li>A promise of acceptance or of review within days.</li>
          <li>Fees that appear only after acceptance, or no clear statement of them.</li>
          <li>No named editorial board you can verify, or an editor outside the field.</li>
        </ul>
        <p style="margin-top:.6rem">Use the <a href="https://thinkchecksubmit.org" target="_blank" rel="noopener">Think. Check. Submit.</a> checklist, and look the journal up in the <a href="https://doaj.org" target="_blank" rel="noopener">Directory of Open Access Journals</a>.</p>
      </div>

      <h2>Coming to this guide</h2>
      <ul class="qg-coming">
{coming}
      </ul>
      <p>Each section is added as it is checked. <a href="about-page.html#contact">Tell us</a> about a gate, a tool or a way through that belongs here.</p>
    </div>
    </section>

  """
open(os.path.join(ROOT, "quest-guide.html"), "w", encoding="utf-8", newline="").write(head + body + foot)
print("wrote quest-guide.html")
