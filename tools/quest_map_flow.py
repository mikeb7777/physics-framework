# -*- coding: utf-8 -*-
"""Builds the Quest Map flow ("The Route of a Result") into quest-map.html.

The map is data: every step, decision and ending is one entry in STEPS, with the
short text shown on the map and the full text shown in the on-screen window when
the step is selected. Add a step here, run the script, and the map, the footprint
menus, the previous/next order and the plain-text version all follow.

    python3 tools/quest_map_flow.py

It replaces everything between <!-- FLOW:START --> and <!-- FLOW:END --> in
quest-map.html, and between <!-- ASK:START --> and <!-- ASK:END -->.
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "quest-map.html")

# lane: (name, subtitle, quark colour, antiquark colour) from the QCD pairs in docs/style-guide.md
LANES = {
    "a": ("Affiliated", "University or national laboratory", "#8B0000", "#00838f"),
    "i": ("Industry", "Corporate research laboratory", "#005ba5", "#f1e303"),
    "u": ("Independent", "No university or company behind you", "#1a5c2a", "#b01558"),
    "s": ("The shared road", "Every lane meets here", "#005f6e", "#c62828"),
    "e": ("Endings", "What counts as a result", "#7a5000", "#1565c0"),
    "m": ("Before any lane", "Where the money comes from", "#8e0c45", "#1a7a36"),
}

def src(*links):
    return "<p class='src'>" + " &middot; ".join(links) + "</p>"

def a(href, text):
    ext = href.startswith("http")
    return f"<a href='{href}'" + (" target='_blank' rel='noopener'" if ext else "") + f">{text}</a>"

# kind: step | decision | ending
# branches: list of (label, target id)
# more: footprint-menu extras after this step: list of (label, href)
STEPS = [
  # ---------------- money ----------------
  dict(id="m1", lane="m", kind="step", title="Where the money comes from",
       line="Three quarters of all US research money is business money, spent on products.",
       who="Companies, government, foundations",
       more=[("Who funds research, and why", "#ask-funders")],
       body=f"""<p>In 2022 the United States spent about <strong>$886 billion</strong> on research and development. Businesses paid for <strong>76 percent</strong> of it. The federal government paid for <strong>18 percent</strong>. Foundations, universities and states paid for the rest.</p>
<p><strong>What that means.</strong> Most people who do research for a living are making something: a drug, a chip, a battery, a better product. That is useful work. But it means the questions this site asks, about what the universe is made of at the bottom, are a small corner of the field, paid for mostly by government and a handful of foundations.</p>
<p><strong>Basic research</strong>, the kind with no product in view, is where government still leads: about 40 percent of it was federally funded in 2022, down from about 60 percent around 2000. Business now funds about 37 percent.</p>
{src(a('https://ncses.nsf.gov/pubs/nsb20246', 'NSB, Research and Development: U.S. Trends (2024)'), a('https://ncses.nsf.gov/pubs/nsf24332', 'NCSES InfoBrief 24-332'))}"""),

  # ---------------- affiliated ----------------
  dict(id="a1", lane="a", kind="step", title="The question",
       line="Shaped by the group you sit in and the grant you are paid from.",
       who="A professor (the PI), often with a student",
       body="""<p>A <strong>principal investigator</strong>, or PI, is the faculty member or staff scientist who runs a research group and holds its grants. The questions a group works on come from the PI's program, from the last grant, and increasingly from the students' own results.</p>
<p>That is not a criticism. It is why the work is fundable on day one and why it connects to what the field is already arguing about.</p>
<p><strong>The trade.</strong> You inherit a running start, and you inherit the direction with it.</p>"""),
  dict(id="a2", lane="a", kind="step", title="Write the proposal",
       line="Fifteen pages of science, plus a budget, a data plan and CVs.",
       who="The PI, with postdocs drafting sections",
       body=f"""<p>An NSF proposal allows fifteen pages to describe the science, and then needs a budget, a budget justification, a data management plan, biographical sketches, letters from collaborators and a statement of facilities. Writing one well takes weeks to months.</p>
<p><strong>Who actually submits it.</strong> Not the scientist. The university's sponsored research office submits it on the institution's behalf, because the award goes to the institution, which then employs the people paid from it.</p>
<p><strong>Who pays.</strong> At this step, the federal agencies most physics depends on: the NSF, the Department of Energy's Office of Science (the largest federal sponsor of basic research in the physical sciences, about $8.2 billion in 2024), NASA, and for some work the NIH and the Department of Defense. Private foundations fund a smaller share. {a('#ask-funders', 'Who funds research, and why')}.</p>
{src(a('https://www.nsf.gov/policies/pappg', 'NSF Proposal and Award Policies (PAPPG)'), a('https://www.everycrsreport.com/reports/IF12692.html', 'CRS, DOE Office of Science'))}"""),
  dict(id="a3", lane="a", kind="decision", title="Panel review: funded?",
       line="NSF funds about one proposal in four. NIH funded 13 percent of R01s in 2025.",
       who="A panel of outside scientists, then a program officer",
       branches=[("Not funded: rewrite for the next cycle", "a2"), ("Funded", "a4")],
       body=f"""<p>Proposals are scored by a panel of scientists from outside the applicant's institution, and a program officer at the agency makes the decision.</p>
<ul><li><strong>NSF</strong>: about 27 percent of competitive proposals funded in 2024; roughly a quarter for research grants alone.</li><li><strong>NIH</strong>: 13.0 percent of R01 applications funded in 2025.</li><li><strong>Time</strong>: most of a year from submission to money, and most proposals are rewritten and resubmitted at least once.</li></ul>
<p><strong>The part rarely mentioned.</strong> A large share never reaches the research. Negotiated overhead rates have commonly run 50 to 65 percent; across NIH-funded institutions the negotiated average was about 58 percent, with roughly 42 percent effectively paid. In May 2025 the NSF capped its rate at 15 percent for universities; a federal court struck the cap down that June. The attempt shows how much was riding on that number.</p>
{src(a('https://www.nsf.gov/about/budget', 'NSF funding rates'), a('https://report.nih.gov/funding/nih-budget-and-spending-data-past-fiscal-years/success-rates', 'NIH success rates'), a('https://www.forbes.com/sites/michaeltnietzel/2025/06/22/judge-sides-with-universities-blocks-nsfs-15--indirect-cost-cap/', 'NSF 15% cap, vacated June 2025'))}"""),
  dict(id="a4", lane="a", kind="step", title="Hire the people",
       line="Most hands-on research is done by graduate students and postdocs paid from the grant.",
       who="Graduate students, postdocs, technicians, undergraduates",
       more=[("Who actually does the research", "#ask-people"), ("What Most People Think Science Is", "blog.html")],
       body=f"""<p>The grant buys people. Most of the experiments, calculations and code behind a physics paper are done by people early in their careers.</p>
<ul><li><strong>Graduate students</strong> usually start as undergraduates helping in a lab, often through a summer research program, then apply to a PhD program and choose an advisor in their first or second year. Most are paid as research assistants from the advisor's grant, as teaching assistants, or by a fellowship. US physics departments granted about 1,900 PhDs in 2018–19, and the degree took about six years on average.</li>
<li><strong>Postdocs</strong> have a PhD and work on fixed contracts of two or three years, often several in a row, hoping for a permanent post. There were about 65,850 postdocs in US science, engineering and health in 2023.</li>
<li><strong>Technicians, engineers and staff scientists</strong> build and run the equipment and keep the data flowing. Their names appear on papers less often than their work does.</li></ul>
<p><strong>What it costs them.</strong> In a 2018 survey of 2,279 graduate students in 26 countries, 41 percent scored moderate to severe anxiety and 39 percent moderate to severe depression, against about 6 percent in the general population on the same scales. It was a self-selected sample, so the true rate may be lower, but the gap is large. {a('#ask-people', 'More on who does the work')}.</p>
{src(a('https://www.aip.org/statistics/reports/trends-physics-phds-171819', 'AIP, physics PhDs 2018–19'), a('https://ncses.nsf.gov/pubs/nsf25317', 'NCSES, postdocs 2023'), a('https://doi.org/10.1038/nbt.4089', 'Evans et al., Nature Biotechnology 36 (2018) 282'))}"""),
  dict(id="a5", lane="a", kind="step", title="Pre-registration (optional)",
       line="Physics rarely writes the prediction down before the data. Most groups skip it.",
       who="The group, if it chooses to",
       body=f"""<p>Physics rarely pre-registers. The practice grew in medicine and psychology, where it was introduced to stop the analysis being chosen after the result is known, and it is spreading into data-heavy physics.</p>
<p><strong>Why it matters here.</strong> Without it, a claim's date is the date it was published, not the date it was thought of. Every argument about priority on this site turns on that distinction.</p>
{src(a('https://www.cos.io/initiatives/prereg', 'Center for Open Science, preregistration'))}"""),
  dict(id="a6", lane="a", kind="step", title="Instrument time and the work",
       line="Time on the telescope or beamline is the scarcest thing, and it goes to teams.",
       who="Students and postdocs run it; a committee allocates it",
       body=f"""<p>Money is not the scarcest resource. Time on the instrument is, and it is allocated by committee to teams with institutions behind them.</p>
<p><strong>The competition.</strong> For JWST Cycle 5, 2,639 proposals asked for 101,751 hours against roughly 8,000 available: about thirteen requests for every hour on offer.</p>
<p><strong>Who is at the instrument.</strong> Usually a student or postdoc, often overnight, often for weeks. The analysis that follows is theirs too.</p>
{src(a('https://www.stsci.edu/jwst/science-execution/approved-programs', 'STScI, JWST programs'))}"""),
  dict(id="a7", lane="a", kind="step", title="Group review and authorship",
       line="Whose name goes first, and whose goes last, is decided here.",
       who="The PI and co-authors",
       more=[("Is most cited work really someone else's?", "#ask-credit")],
       body=f"""<p>Before a paper leaves the group, the co-authors read it and the group decides the author list. In most of physics outside the very large collaborations, the <strong>first author</strong> is usually the person who did most of the work, often a student or postdoc, and the <strong>last author</strong> is usually the PI who runs the group. Particle physics collaborations list hundreds or thousands of names alphabetically.</p>
<p><strong>What studies of who did what show.</strong> When journals began asking authors to state their contributions, the pattern was clear: first and last authors do most of the work between them, middle authors the least, and as teams grow each author takes on fewer tasks.</p>
{src(a('https://doi.org/10.1177/0306312716650046', 'Larivière et al., Social Studies of Science 46 (2016) 417'), a('https://credit.niso.org/', 'CRediT contributor roles'))}"""),

  # ---------------- industry ----------------
  dict(id="i1", lane="i", kind="step", title="The question",
       line="Chosen where the physics and the product roadmap overlap.",
       who="Research managers and senior scientists",
       body="""<p>The subject is chosen where the physics and the roadmap overlap. Google Quantum AI works on error correction because a useful quantum computer cannot exist without it, and genuine physics gets done on the way to a product.</p>
<p><strong>The trade.</strong> Enormous resources, aimed only where they pay.</p>"""),
  dict(id="i2", lane="i", kind="step", title="Budget decision",
       line="Internal, fast, and with no public record of what was declined.",
       who="Company management",
       body=f"""<p>The decision is internal and can be made in a week. There is no panel, no resubmission, no overhead argument, and no public record of what was declined.</p>
<p><strong>What it buys.</strong> Speed, and hardware nobody else has.</p>
<p><strong>What it costs.</strong> The funder chooses the question, and the record shows that matters: across 75 studies, industry-funded drug and device research was about twice as likely to report favorable results and about two and a half times as likely to reach favorable conclusions.</p>
{src(a('https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.MR000033.pub3/full', 'Cochrane, industry sponsorship and research outcome'))}"""),
  dict(id="i3", lane="i", kind="step", title="Staff scientists and engineers",
       line="Salaried employees. What they discover usually belongs to the company.",
       who="PhD scientists, engineers, interns",
       body="""<p>Industry researchers are employees, hired for their skills, often straight from a PhD or a postdoc. Many come through internships during graduate school.</p>
<p><strong>The difference from a university.</strong> The pay is usually better and the contracts longer. In return, employment agreements normally assign inventions made on the job to the employer, and what may be published is the company's decision.</p>"""),
  dict(id="i4", lane="i", kind="step", title="IP and patent clearance",
       line="Protect first, publish second.",
       who="Patent lawyers and the research team",
       body="""<p>In most countries a public disclosure before filing can destroy the right to a patent, so the paper waits for the lawyers. Applications publish about eighteen months after filing, which is why competitors' filings are readable long before their products ship.</p>
<p><strong>The hard edge.</strong> In the United States a patent application can be placed under a secrecy order, and the work disappears from public science entirely.</p>"""),
  dict(id="i5", lane="i", kind="step", title="The work, on company hardware",
       line="No queue and no committee. Also no duty to release the raw data.",
       who="Staff scientists and engineers",
       body=f"""<p>No allocation committee and no queue. Also no obligation to release the raw data, which is the reason some industry results cannot be independently replicated even in principle.</p>
<p><strong>Worked example.</strong> The Willow quantum error-correction result was published in <em>Nature</em> in December 2024, on hardware only Google has.</p>
{src(a('https://www.nature.com/articles/s41586-024-08449-y', 'Willow, Nature 2024'))}"""),
  dict(id="i6", lane="i", kind="decision", title="Publish, or keep it?",
       line="Companies publish when it helps them. Otherwise the result stays inside.",
       who="Management and legal",
       branches=[("Keep it: trade secret or product", "e3"), ("Publish", "s1")],
       body="""<p>A company publishes when publishing helps it: to recruit, to establish credibility with customers and investors, to set a standard, or once the patents are filed. Otherwise a result can stay a trade secret indefinitely.</p>
<p><strong>What that means for the rest of us.</strong> The published record of industry research is a selection, chosen by the company, from a much larger body of work nobody outside will see.</p>"""),

  # ---------------- independent ----------------
  dict(id="u1", lane="u", kind="step", title="The question",
       line="Nobody has to approve it. That is the one real advantage.",
       who="You",
       body="""<p>Nobody has to approve the question. No roadmap constrains it, no committee scores it, no supervisor has to be persuaded first. This is real, and it is the reason independent work exists at all.</p>
<p><strong>The other side of it.</strong> Nobody is assigned to tell you it has been done before, or that it is wrong. Finding that out is now your job.</p>"""),
  dict(id="u2", lane="u", kind="step", title="Write it down",
       line="In the form the field reads: equations, references, a clear claim.",
       who="You",
       more=[("A Quest for The Big TOE", "book.html")],
       body=f"""<p>A physics idea is read as a paper: a stated claim, the derivation, the references, and what would prove it wrong. The field writes in LaTeX, which is free, and journals provide templates for it.</p>
<p><strong>What it costs.</strong> Nothing but time. Get an ORCID iD at this step as well. It is free, it is the identifier journals and funders ask for, and it keeps your work attached to your name.</p>
{src(a('https://orcid.org/', 'ORCID'), a('book.html', 'our framework, written in full'), a('download.html', 'every version, dated'))}"""),
  dict(id="u3", lane="u", kind="decision", title="Fund it: do you need an institution?",
       line="Most grants must be paid to an organisation. The form has no box for you.",
       who="You, or an organisation that will host you",
       branches=[("Self-funded: carry on", "u4"), ("Need a grant: find a host (fiscal sponsor)", "u4")],
       more=[("Who funds research, and why", "#ask-funders")],
       body=f"""<p>Almost every research grant requires an institution to receive the money. The NSF states that, unless a solicitation says otherwise, unaffiliated individuals are ineligible to receive its funding directly, and it encourages them to affiliate with an organisation that can meet federal grant rules. Academic researchers without an affiliation must speak to a program officer before applying.</p>
<p><strong>Note what kind of wall this is.</strong> It is administrative, not intellectual. Nobody has judged the work; the form simply has no box for you.</p>
<p><strong>The ways through.</strong></p>
<ul><li><strong>Self-funding</strong>, which is what most independents do.</li>
<li><strong>A fiscal sponsor</strong>: a nonprofit that applies for and holds the grant on your behalf and handles the reporting, for a fee, typically somewhere between 5 and 15 percent.</li>
<li><strong>Small foundation grants and crowdfunding</strong>, for modest amounts.</li></ul>
<p><strong>What the institute intends.</strong> After incorporation, Ic² plans to become an institution independent researchers can affiliate with for their grant applications.</p>
{src(a('https://www.nsf.gov/policies/pappg', 'NSF PAPPG, unaffiliated individuals'), a('https://opengrants.io/encyclopedia/readiness/fiscal-sponsorship/', 'fiscal sponsorship, how it works'))}"""),
  dict(id="u4", lane="u", kind="step", title="Public, dated deposit",
       line="With nobody to vouch for you, a record that cannot be edited is your proof.",
       who="You, and a repository such as Zenodo",
       body=f"""<p>With no institution to vouch for you, a dated public deposit is the only thing separating a prediction from a story told afterward. Zenodo, run by CERN, issues a permanent DOI and a date that cannot be edited later. It is free.</p>
<p><strong>What has to be in it.</strong> A number, an uncertainty, a named instrument that could contradict it, and the outcome you will accept either way.</p>
<p><strong>Where we are.</strong> Three missions are registered and waiting.</p>
{src(a('https://zenodo.org', 'Zenodo'), a('testing-schedule.html', 'our registered missions'))}"""),
  dict(id="u5", lane="u", kind="step", title="Find readers and collaborators",
       line="Nobody is assigned to check your work. You have to find them.",
       who="Other independents, retired academics, students, volunteers",
       more=[("The discussion forum", "discussions-page.html")],
       body="""<p>In a university the first readers come with the job: co-authors, the group, the seminar. An independent researcher starts with none. The people who end up helping are usually other independents, retired academics with time to read, students, and specialists who answer an email because the question is precise.</p>
<p><strong>What works.</strong> Write to authors whose work you build on, with one specific question. Show the derivation so someone can check it in an afternoon. Thank and credit everyone who helps, by name.</p>
<p><strong>Why this step matters later.</strong> The endorser arXiv requires, the colleague who checks the units, and the first person to cite you will all come from here.</p>"""),
  dict(id="u6", lane="u", kind="step", title="Test against public data",
       line="Predict what a big survey will measure anyway, then accept the answer.",
       who="You, using data the large collaborations release",
       body=f"""<p>No instrument time, so the strategy is to predict something a major survey is going to measure anyway, and then accept the answer.</p>
<p>This only works because the large collaborations publish. DESI, Rubin and the Simons Observatory all release data to anyone, which is the single policy that makes independent cosmology possible.</p>
<p><strong>Where we are.</strong> First deciding data expected in 2027.</p>
{src(a('https://data.desi.lbl.gov/public/', 'DESI public data'), a('https://rubinobservatory.org/for-scientists/data-products', 'Rubin data products'), a('instruments.html', 'the instruments'))}"""),

  # ---------------- shared road ----------------
  dict(id="s1", lane="s", kind="decision", title="Internal check",
       line="Do the units balance? Has this been refuted already? Could it be proven wrong?",
       who="Co-authors, a review board, or whoever you can persuade to read it",
       branches=[("Fails: back to the work", "u6"), ("Passes", "s2")],
       body="""<p>Before anything goes out, someone checks it: a co-author, a review board, or in the independent case only you and whoever you can persuade to read it.</p>
<p><strong>This is where the lanes stop being equal.</strong> Industry has a formal technical review. A university group has co-authors and a seminar. An independent researcher has no one by default, which is exactly the gap an adversarial pre-check is meant to fill: do the units balance, does the derivation close, has this already been refuted, could the prediction be proven wrong.</p>"""),
  dict(id="s2", lane="s", kind="decision", title="arXiv: are you endorsed?",
       line="A new author needs an established author in the field to vouch for them.",
       who="An established arXiv author; about 300 volunteer moderators",
       branches=[("Not endorsed: deposit on Zenodo and keep looking", "u5"), ("Endorsed", "s3")],
       body=f"""<p>arXiv was launched on 14 August 1991 by Paul Ginsparg. It is free to read and free to post, and it passed two million papers by the end of 2021. Physics runs on it: most papers appear here before, or instead of, a journal.</p>
<p><strong>Who may post.</strong> A new author must be endorsed by an established author in that subject area. About 300 volunteer moderators screen submissions; roughly 6 percent are held and about 2 percent rejected.</p>
<p><strong>Changed January 2026.</strong> arXiv no longer accepts an institutional email address as the qualifier for endorsement, after a rise in non-scientific submissions. Affiliation alone will not open this door any more; only a person who reads the work will.</p>
<p><strong>Why the wall exists.</strong> arXiv is run by a small staff and volunteers, and it is flooded with submissions. Endorsement is how it keeps moderation possible. For an independent author the way through is a reader from the previous step.</p>
{src(a('https://info.arxiv.org/help/endorsement.html', 'arXiv endorsement'), a('https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/', 'the 2026 change'))}"""),
  dict(id="s3", lane="s", kind="step", title="Post the preprint",
       line="Free, public within days, and it fixes the date of your claim.",
       who="You",
       body="""<p>Posting is free. The paper appears in the next daily announcement after moderation, and from then on it carries a public date and a permanent identifier.</p>
<p><strong>What it is not.</strong> A preprint has been screened, not reviewed. It establishes when you said something, not that it is right.</p>
<p><strong>Why most physicists post before submitting.</strong> It gets the work read months before a journal would publish it, and readers' comments often improve it before review.</p>"""),
  dict(id="s4", lane="s", kind="step", title="Choose a journal",
       line="Fit first. Then speed, reach and cost.",
       who="You and your co-authors",
       more=[("How an independent submits, and what it costs", "#ask-submit")],
       body="""<p><strong>Fit matters most.</strong> Most rejections happen because a paper does not suit the journal, so read a few recent issues first. In foundations and cosmology, for example: the <em>Physical Review</em> family (American Physical Society), <em>Classical and Quantum Gravity</em> (IOP), <em>Foundations of Physics</em> (Springer).</p>
<p><strong>Then cost.</strong> Many society journals publish free on the subscription route and charge only for open access. Gold open-access journals charge every author.</p>
<p><strong>Avoid predatory journals.</strong> If a journal emails you first, promises fast acceptance and asks for a fee, it is selling publication, not review. A paper there can count against you.</p>"""),
  dict(id="s5", lane="s", kind="step", title="Submit",
       line="An online form, a formatted paper and a cover letter. Usually free to submit.",
       who="You",
       more=[("Step by step, with costs", "#ask-submit")],
       body=f"""<p><strong>How an independent researcher does it.</strong></p>
<ul><li>Format the paper with the journal's template (for APS journals, REVTeX).</li>
<li>Give your affiliation honestly as <em>Independent researcher</em>, with a postal address and your ORCID iD.</li>
<li>Write a one-page cover letter: what the paper claims, why it suits this journal, and that it is not under review elsewhere.</li>
<li>Suggest qualified reviewers who are not your collaborators, and name any you want excluded, with a reason.</li>
<li>Declare funding (self-funded is a valid answer) and any competing interests.</li></ul>
<p><strong>What it costs.</strong> Submission to most physics journals is free. Payment comes at acceptance, and only for open access: at APS in 2025, $2,840 for <em>Physical Review</em> A to E and $3,980 for <em>Physical Review Letters</em>. The subscription route costs nothing. Most high-energy physics articles are covered by the SCOAP3 consortium.</p>
{src(a('https://journals.aps.org/authors/open-access-physical-review-physical-review-letters', 'APS publication charges'))}"""),
  dict(id="s6", lane="s", kind="decision", title="The editor's desk",
       line="Most papers are turned back here before any reviewer sees them.",
       who="One editor",
       branches=[("Desk rejection: choose another journal", "s4"), ("Sent to reviewers", "s7")],
       body=f"""<p>An editor reads the submission first and desk-rejects most of what arrives before any reviewer sees it, usually for fit, sometimes for presentation, and sometimes because the claim looks too large for the evidence.</p>
<p><strong>Who the editors are.</strong> Working scientists, often part-time, with their own interests. A 2017 study of 713 editors at 52 influential US medical journals found 51 percent had received general payments from industry in 2014.</p>
{src('Liu et al., <em>BMJ</em> 359 (2017) j4619')}"""),
  dict(id="s7", lane="s", kind="step", title="Peer review",
       line="Two or three unpaid specialists, chosen by the editor, advise on the paper.",
       who="Two or three reviewers, usually anonymous",
       body=f"""<p>Peer review is two or three unpaid specialists, chosen by an editor, usually from the same small field as the author, sometimes competitors for the same grants. It has no investigators, no subpoena power and no budget. It runs on the assumption that a reviewer's interests are disclosed.</p>
<p><strong>Who those people are.</strong> A 2024 study of 1,962 physician peer reviewers at the BMJ, NEJM, JAMA and the Lancet found more than half had received industry payments between 2020 and 2022, totalling 1.06 billion dollars.</p>
<p><strong>What it does not catch.</strong> Both of physics's famous fabrication cases passed peer review repeatedly at the most selective journals. What caught them was replications that could not reproduce the results, and independent researchers reading the figures.</p>
{src('<em>JAMA</em> (2024), payments to peer reviewers')}"""),
  dict(id="s8", lane="s", kind="decision", title="The decision",
       line="Reject, revise, or accept. Rejection is the normal case.",
       who="The editor, on the reviewers' advice",
       branches=[("Rejected: choose another journal", "s4"), ("Revise", "s9"), ("Accepted", "s10")],
       body=f"""<p>Most submissions to a selective journal are rejected. An address that reads <em>Independent</em> starts further back: the 1982 Peters and Ceci experiment resubmitted already-published papers under unknown names and affiliations, and most were rejected.</p>
<p><strong>Measured version.</strong> In a randomized trial at a 2017 conference, reviewers who could see author identities were significantly more likely to recommend acceptance for famous authors (odds multiplier 1.63), top universities (1.58) and top companies (2.10), on the same papers.</p>
{src('Tomkins, Zhang and Heavlin, <em>PNAS</em> 114 (2017) 12708')}"""),
  dict(id="s9", lane="s", kind="step", title="Revise and resubmit",
       line="Answer every point, change the paper, send it back. Two or three rounds is ordinary.",
       who="You, answering the reviewers",
       branches=[("Back to the reviewers", "s7")],
       body="""<p>Answer every reviewer point in a reply letter, say what you changed and where, and argue politely where you disagree. Two or three rounds is ordinary, and a year can pass.</p>
<p><strong>Why the loop matters to us.</strong> Every pass through it is time in which the dated public record is the only thing establishing when the claim was made.</p>"""),
  dict(id="s10", lane="s", kind="step", title="Accepted: publication and the bill",
       line="Free on the subscription route. Open access is paid by the author.",
       who="The publisher",
       body=f"""<p>Acceptance is not the end. Open access is paid by the author: about 12,850 US dollars at <em>Nature</em>, 7,350 at <em>Nature Communications</em>, 2,850 at <em>Scientific Reports</em>, and commonly 2,000 to 6,000 elsewhere.</p>
<p><strong>Who feels it.</strong> A university pays from a grant or a library deal, so the author never sees the invoice. A company pays without noticing. An independent researcher pays personally, chooses the free subscription route, or asks for a waiver.</p>
<p><strong>And then it is paid for twice.</strong> Libraries subscribe as well. RELX, Elsevier's parent, reported about 1.17 billion pounds of adjusted operating profit on 3.05 billion of revenue in its scientific division, a margin near 38 percent. Authors and peer reviewers are paid nothing.</p>
{src(a('https://www.nature.com/nature/for-authors/publishing-options', 'Nature charges'))}"""),
  dict(id="s11", lane="s", kind="step", title="What publishing gets you",
       line="A version of record, a permanent DOI, indexing, and the currency careers count.",
       who="The field",
       more=[("What is gained by publishing", "#ask-gains")],
       body="""<ul><li><strong>A version of record</strong>: the final, citable text, preserved by the publisher and by archives even if the journal closes.</li>
<li><strong>A documented review</strong>: proof that specialists read it and did not find it wrong.</li>
<li><strong>Indexing</strong>: the paper enters the databases researchers search and that citations are counted in.</li>
<li><strong>Currency</strong>: hiring committees, promotion panels and grant panels count peer-reviewed papers. For an independent author it is the strongest answer to "who checked this?"</li></ul>
<p><strong>What it does not get you.</strong> It does not make the result true, and it does not guarantee anyone reads it.</p>"""),
  dict(id="s12", lane="s", kind="step", title="Cited, or not",
       line="Credit flows to famous names, and many citations are copied, not read.",
       who="Everyone who reads, or does not read, the paper",
       more=[("Is most cited work really someone else's?", "#ask-credit")],
       body=f"""<p>A citation is a pointer to the work a paper builds on. Two well-documented effects shape who gets them.</p>
<p><strong>The Matthew effect.</strong> Robert Merton showed in 1968 that well-known scientists receive more credit than lesser-known colleagues for comparable work. A famous co-author's name draws the citations.</p>
<p><strong>Copied citations.</strong> By tracing how misprints in references spread, Simkin and Roychowdhury estimated that only about one citer in five had read the paper they cited; the rest copied the reference from another paper's list. It is a model-based estimate, but it explains why a few papers collect most of the citations.</p>
{src(a('https://doi.org/10.1126/science.159.3810.56', 'Merton, Science 159 (1968) 56'), a('https://arxiv.org/abs/cond-mat/0212043', 'Simkin and Roychowdhury, Complex Systems 14 (2003)'))}"""),
  dict(id="s13", lane="s", kind="decision", title="Replication and the sigma bar",
       line="Has anyone else found it? Is it strong enough to count as discovery?",
       who="Other groups, other instruments",
       branches=[("Not met: more data", "s14"), ("Met", "e1")],
       body=f"""<p>A result counts when someone else can reproduce it, and when the evidence clears the field's bar. Particle physics sets its bar explicitly, which most fields do not.</p>
<ul><li><strong>3 sigma</strong> is called evidence: roughly a 1 in 740 chance of arising from noise.</li><li><strong>5 sigma</strong> is called discovery: roughly 1 in 3.5 million. The Higgs boson was announced in July 2012 at 5 sigma.</li></ul>
<p><strong>Where our own tests sit.</strong> DESI's evolving dark energy runs about 2.8 to 4.2 sigma depending on which supernova compilation is combined. That is evidence, and it is not discovery, and saying so plainly is the whole discipline.</p>
{src(a('https://home.cern/science/physics/higgs-boson', 'CERN on the Higgs'), a('validation.html', 'our record'))}"""),
  dict(id="s14", lane="s", kind="step", title="Addendum or further testing",
       line="Below the bar is not wasted. It goes back for more data or a narrower claim.",
       who="The original authors, and anyone else",
       branches=[("Back to the work", "u6")],
       body="""<p>A result below the bar is routed back: more data, a tighter analysis, or a narrower claim. Most results in physics live here for years.</p>
<p><strong>The honest risk.</strong> This is also where a result can be quietly reshaped until it agrees with the data. The protection is the same one this institute relies on everywhere: the prediction was registered, with a date, before the data existed.</p>"""),

  # ---------------- endings ----------------
  dict(id="e1", lane="e", kind="ending", title="Accepted",
       line="Replicated, cited, built on.",
       body="""<p>The result enters the field: replicated, cited and built on, until something better replaces it. That is the ending everyone means by a result.</p>"""),
  dict(id="e2", lane="e", kind="ending", title="Modified",
       line="Partly right. The claim changes and the work goes on.",
       body="""<p>Most ideas that survive do so changed. A narrower claim, a corrected number, a different mechanism. This is a result too, and it is the most common good one.</p>"""),
  dict(id="e3", lane="e", kind="ending", title="Set aside",
       line="Wrong, unpublished, or kept private. Still a result.",
       body="""<p>A result that cannot find a venue is not necessarily wrong, and it is not necessarily right either. It stops being part of the conversation, which in practice is the same as not existing. Industry results kept as trade secrets end here too.</p>
<p>Where a public deposit exists, the record survives even when the paper does not. A clear negative result is also a result: it tells everyone where not to look.</p>"""),
]

# the order the window's previous / next buttons follow
ORDER = ["m1", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "i1", "i2", "i3", "i4", "i5", "i6",
         "u1", "u2", "u3", "u4", "u5", "u6", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8",
         "s9", "s10", "s11", "s12", "s13", "s14", "e1", "e2", "e3"]
BY = {s["id"]: s for s in STEPS}
assert sorted(ORDER) == sorted(BY), set(ORDER) ^ set(BY)

# The questions people ask, answered at length below the map.
ASK = [
  ("ask-people", "Who actually does the research", f"""
<p>The name on a grant is one person. The work is done by a team, and most of the team is early in their careers.</p>
<p><strong>Graduate students.</strong> Most begin as undergraduates helping in a lab, often through a summer research program, which is how they find out whether they like the work and get the letters of recommendation a PhD application needs. In the first year or two of a PhD they choose an advisor, and from then on they are usually paid as research assistants from that advisor's grant, as teaching assistants, or by a fellowship such as the NSF Graduate Research Fellowship, which pays a $37,000 stipend for three years. US physics departments granted about 1,900 PhDs in 2018–19. The degree took about six years on average.</p>
<p><strong>Not everyone finishes.</strong> The Council of Graduate Schools followed students who began PhDs in the early 1990s: in mathematics and the physical sciences about 55 percent had finished within ten years, and most of those who left did so by their third year.</p>
<p><strong>What it costs them.</strong> In a 2018 survey of 2,279 graduate students in 26 countries, 41 percent scored moderate to severe anxiety and 39 percent moderate to severe depression, against about 6 percent in the general population measured with the same scales. In <em>Nature</em>'s 2019 survey of 6,300 PhD students, 36 percent said they had sought help for anxiety or depression caused by their studies. Both samples chose to respond, so the true rates may be lower, but no reading of them is reassuring.</p>
<p><strong>Postdocs</strong> hold a PhD and work on contracts of two or three years, often several in a row, hoping for one of the few permanent posts. There were about 65,850 in US science, engineering and health in 2023.</p>
<p><strong>Everyone else.</strong> Technicians, engineers and staff scientists who build and run the instruments. Undergraduates on summer projects. And volunteers: citizen-science projects have had members of the public classify galaxies and search telescope data, and some have been co-authors on the results.</p>
<p><strong>Why this matters to the Quest.</strong> These people are the system. Any honest account of how an idea meets the world has to include who carries it.</p>
{src(a('https://www.aip.org/statistics/reports/trends-physics-phds-171819', 'AIP'), a('https://doi.org/10.1038/nbt.4089', 'Evans et al. 2018'), a('https://group.springernature.com/fr/group/media/press-releases/nature-phd-survey-puts-spotlight-on-mental-health/17372858', 'Nature PhD survey 2019'), a('https://ncses.nsf.gov/pubs/nsf25317', 'NCSES 2023'), 'Council of Graduate Schools, Ph.D. Completion Project')}"""),
  ("ask-credit", "Is most cited work really someone else's?", f"""
<p>It is something people say, and it is partly true, in three different senses.</p>
<p><strong>1. The hands-on work is mostly done by juniors.</strong> True for most of physics outside the giant collaborations. The experiments, code and calculations are usually done by graduate students and postdocs. They are normally listed as authors, often first, so the paper itself is not hiding them. Studies of the contribution statements journals now require show first and last authors doing most of the work between them, and middle authors the least.</p>
<p><strong>2. The recognition goes up the ladder.</strong> True, and it has a name. Robert Merton called it the Matthew effect in 1968: well-known scientists receive more credit than lesser-known colleagues for comparable work. Talks, prizes and press tend to name the head of the lab. A paper becomes known as the PI's paper.</p>
<p><strong>3. Many citations are copied, not read.</strong> Probably true. By tracing how misprints in references spread from paper to paper, Simkin and Roychowdhury estimated that only about one citer in five had read the work they cited. It is a model-based estimate, not a survey, but it fits the way a small number of papers collect most citations.</p>
<p><strong>What is not true.</strong> A citation is not taking someone's work. It is the opposite: the formal way of saying whose work you are building on. The problem is the credit around it, not the citation itself.</p>
<p><strong>Why it happens.</strong> Careers are measured in papers and citations, so the incentives reward volume and visibility. Teams have grown, so individual roles are hidden. And reading every cited paper takes time nobody is paid for.</p>
<p><strong>What we do.</strong> Every contributor to the institute's work is named with what they did, using the CRediT contributor roles, and contributors keep ownership of their work.</p>
{src(a('https://doi.org/10.1126/science.159.3810.56', 'Merton 1968'), a('https://arxiv.org/abs/cond-mat/0212043', 'Simkin and Roychowdhury 2003'), a('https://doi.org/10.1177/0306312716650046', 'Larivière et al. 2016'), a('https://credit.niso.org/', 'CRediT'))}"""),
  ("ask-funders", "Who funds research, and why", f"""
<p><strong>Businesses: about three quarters of all US research money</strong> ($673 billion of $886 billion in 2022). They fund research because it leads to products. That is most of the research done in the country, and most of the people doing it.</p>
<p><strong>Government: about 18 percent overall, and about 40 percent of basic research.</strong> The reasons are national security, economic competitiveness and health, and the modern system dates from Vannevar Bush's 1945 report to the President, <em>Science, the Endless Frontier</em>, which argued that basic research pays the nation back in ways no company will fund. For physics the main federal funders are the Department of Energy's Office of Science (the largest federal sponsor of basic research in the physical sciences, about $8.2 billion in 2024), the NSF, NASA, and parts of the Department of Defense.</p>
<p><strong>Private foundations: small in total, important at the edges.</strong> The Simons Foundation, the Gordon and Betty Moore Foundation, the John Templeton Foundation, the Alfred P. Sloan Foundation, the Kavli Foundation and others fund questions government panels find too risky or too unusual. They give because a founder cares about a field, for legacy, and because the law requires it: a US private foundation must pay out about 5 percent of its assets every year, or pay a tax on the shortfall.</p>
<p><strong>Universities</strong> also spend their own money, mostly from endowments, tuition and state budgets.</p>
<p><strong>Why the money goes to institutions, not people.</strong> Public money must be accounted for under federal grant rules, so it is paid to an organisation that can keep the books, run the audits and employ the staff. That is the reason an independent researcher cannot simply apply, and why the institute plans to become an organisation independents can affiliate with.</p>
{src(a('https://ncses.nsf.gov/pubs/nsb20246', 'NSB 2024'), a('https://ncses.nsf.gov/pubs/nsf24332', 'NCSES 24-332'), a('https://www.nsf.gov/about/history/vbush1945.htm', 'Bush, 1945'), a('https://www.everycrsreport.com/reports/IF12692.html', 'CRS on DOE Office of Science'), a('https://www.law.cornell.edu/uscode/text/26/4942', '26 U.S.C. § 4942'))}"""),
  ("ask-submit", "How an independent submits to a journal, and what it costs", f"""
<ol class="ask-steps">
<li><strong>Get an ORCID iD.</strong> Free, and asked for by most journals.</li>
<li><strong>Post the preprint if you can</strong> (see the arXiv step on the map). If you cannot yet, deposit it on Zenodo for a dated record.</li>
<li><strong>Choose the journal</strong> by fit: read recent issues and the journal's scope statement.</li>
<li><strong>Format with the journal's template.</strong> APS journals use REVTeX; most others provide LaTeX and Word templates.</li>
<li><strong>Affiliation:</strong> write <em>Independent researcher</em>, with a postal address. Do not invent an institution.</li>
<li><strong>Cover letter:</strong> one page. The claim, why this journal, and a statement that it is not under review elsewhere.</li>
<li><strong>Reviewers:</strong> suggest three to five qualified people who are not your collaborators. You may ask that named people be excluded, with a reason.</li>
<li><strong>Declarations:</strong> funding (self-funded is a valid answer), competing interests, data availability.</li>
<li><strong>Submit</strong> through the journal's online system, then wait: weeks for a desk decision, months for review.</li></ol>
<p><strong>What it costs.</strong> Submitting is free at most physics journals. On the subscription route, publishing is free too. Open access is charged on acceptance: at APS in 2025, $2,840 for <em>Physical Review</em> A to E and $3,980 for <em>Physical Review Letters</em>; about 12,850 US dollars at <em>Nature</em>. Most high-energy physics articles are covered by the SCOAP3 consortium. Some journals waive charges on request; ask before you submit, not after.</p>
<p><strong>Warning signs.</strong> A journal that invites you by email, promises acceptance in days, or asks for a fee before review is not a journal you want.</p>
{src(a('https://journals.aps.org/authors/open-access-physical-review-physical-review-letters', 'APS charges'), a('https://www.nature.com/nature/for-authors/publishing-options', 'Nature charges'), a('https://orcid.org/', 'ORCID'))}"""),
  ("ask-gains", "What is gained by publishing", f"""
<p><strong>For the work.</strong> A version of record that will not change, a permanent DOI, preservation in archives that outlive the journal, and a place in the databases researchers search and citations are counted in.</p>
<p><strong>For the claim.</strong> A documented review: two or three specialists read it and did not find it wrong. That is less than proof, and more than nothing.</p>
<p><strong>For the person.</strong> Peer-reviewed papers are the currency of science. Hiring, promotion and grant panels count them, and for someone without an institution a published paper is the strongest answer to the question "who checked this?"</p>
<p><strong>What a preprint already gives you.</strong> A public date and readers. Many physicists are read on arXiv long before, or without, a journal.</p>
<p><strong>What publishing does not give you.</strong> Truth, and attention. Most papers are cited rarely. A result becomes knowledge only when others replicate it and build on it.</p>"""),
]

FOOT = ('<svg class="fp-svg" viewBox="0 0 110 150" aria-hidden="true"><path class="fp-sole" d="M20 62 C19 46 38 39 57 41 C77 43 91 53 89 71 C87 90 83 104 81 118 C79 134 66 143 54 141 C41 139 36 127 40 115 C44 103 50 95 46 85 C42 77 21 78 20 62 Z"/>'
        '<ellipse class="fp-big" cx="30" cy="30" rx="11.5" ry="13.5" transform="rotate(-10 30 30)"/>'
        '<ellipse class="fp-toe" cx="51" cy="27" rx="7.2" ry="8.6" transform="rotate(-2 51 27)"/><ellipse class="fp-toe" cx="65" cy="30" rx="6.2" ry="7.2" transform="rotate(8 65 30)"/>'
        '<ellipse class="fp-toe" cx="77" cy="37" rx="5.3" ry="6.2" transform="rotate(18 77 37)"/><ellipse class="fp-toe" cx="86" cy="47" rx="4.4" ry="5.2" transform="rotate(26 86 47)"/></svg>')

def esc(t):
    return html.escape(t, quote=True)

def label(s):
    return s["id"].upper() if s["lane"] not in "me" else ""

def card(s):
    name, sub, bg, edge = LANES[s["lane"]]
    num = label(s)
    cls = {"step": "fs", "decision": "fs fs-dec", "ending": "fs fs-end"}[s["kind"]]
    who = f'<span class="fs-who">{esc(s["who"])}</span>' if s.get("who") else ""
    out = [f'<div class="fs-wrap" id="step-{s["id"]}">',
           f'<button type="button" class="{cls}" data-n="{s["id"]}" style="--bg:{bg};--edge:{edge}" aria-haspopup="dialog">',
           (f'<span class="fs-num">{num}</span>' if num else ''),
           f'<span class="fs-title">{esc(s["title"])}</span>',
           f'<span class="fs-line">{esc(s["line"])}</span>', who, '</button>']
    if s.get("branches"):
        out.append('<div class="fs-br">' + "".join(
            f'<a class="br" href="#step-{t}" data-go="{t}"><span class="br-arrow" aria-hidden="true">&#8627;</span> {esc(l)}</a>'
            for l, t in s["branches"]) + '</div>')
    out.append('</div>')
    return "".join(out)

def nxt(sid):
    i = ORDER.index(sid)
    return ORDER[i + 1] if i + 1 < len(ORDER) else None

def prints(frm, to, extra=None):
    """A footprint between two steps. Its menu is built by the page script from these attributes."""
    more = extra if extra is not None else BY[frm].get("more", [])
    data = "|".join(f"{l}::{h}" for l, h in more)
    return (f'<div class="fp-row"><button type="button" class="fp" data-from="{frm}" data-to="{to}"'
            f' data-more="{esc(data)}" aria-haspopup="menu" aria-label="Footprint between {esc(BY[frm]["title"])} and {esc(BY[to]["title"])}: options">'
            f'{FOOT}</button></div>')

def lane(code, ids):
    name, sub, bg, edge = LANES[code]
    parts = [f'<div class="lane" data-lane="{code}" style="--bg:{bg};--edge:{edge}">',
             f'<div class="lane-head"><span class="lane-name">{name}</span><span class="lane-sub">{sub}</span></div>']
    for k, sid in enumerate(ids):
        parts.append(card(BY[sid]))
        if k + 1 < len(ids):
            parts.append(prints(sid, ids[k + 1]))
    if code == "u":
        parts.append(ISSUES)
    parts.append('</div>')
    return "".join(parts)

ISSUES = ('<div class="flow-here"><span class="here-pin">Ic&sup2; is here</span> registered, waiting for data in 2027</div>'
  '<div class="issue-row">'
  '<button type="button" class="fp fp-issue" data-issue="1" data-live="2026-11-01" data-title="Issue 1 &#183; Setting Out" data-month="November 2026" data-page="quest-issue-1.html" aria-haspopup="menu" aria-label="Quest newsletter, Issue 1, November 2026">' + FOOT + '<span class="fp-date">November 2026</span></button>'
  '<button type="button" class="fp fp-issue" data-issue="2" data-live="2027-01-01" data-title="Issue 2 &#183; Testing and marketing" data-month="January 2027" data-page="quest-issue-2.html" aria-haspopup="menu" aria-label="Quest newsletter, Issue 2, January 2027">' + FOOT + '<span class="fp-date">January 2027</span></button>'
  '</div>')

def build_flow():
    road = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14"]
    road_html = []
    for k, sid in enumerate(road):
        road_html.append(card(BY[sid]))
        if k + 1 < len(road):
            road_html.append(prints(sid, road[k + 1]))
    content = "".join(
        f'<article class="sc" id="c-{s["id"]}" data-tag="{esc((label(s) + " · " if label(s) else "") + LANES[s["lane"]][0])}" data-edge="{LANES[s["lane"]][3]}">'
        f'<h4>{esc(s["title"])}</h4>' + (f'<p class="sc-who"><strong>Who:</strong> {esc(s["who"])}</p>' if s.get("who") else "") +
        s["body"].strip() + '</article>' for s in (BY[i] for i in ORDER))
    return f"""<!-- FLOW:START (generated by tools/quest_map_flow.py; edit the script, not this block) -->
    <section class="q-section" id="route">
      <div class="q-inner">
        <p class="eyebrow">The map</p>
        <h2>The Route of a Result</h2>
        <p class="lede">The road a physics result travels, step by step, from the first thought to a tested result. Find the lane you start in and follow the footprints down. <strong>Select any step</strong> to read what it involves, who does the work, what it costs and where to go next. <strong>Select a footprint</strong> for the ways on from there. Every gate in detail is in the <a href="quest-guide.html">Quest Guide</a>.</p>

        <div class="flow">
          <div class="flow-top">{card(BY['m1'])}</div>
          {prints('m1', 'a1', [("Affiliated lane", "#step-a1"), ("Industry lane", "#step-i1"), ("Independent lane", "#step-u1"), ("Who funds research, and why", "#ask-funders")])}
          <div class="lane-pick" role="group" aria-label="Show one lane">
            <button type="button" data-show="a" style="--bg:#8B0000;--edge:#00838f">Affiliated</button>
            <button type="button" data-show="i" style="--bg:#005ba5;--edge:#f1e303">Industry</button>
            <button type="button" data-show="u" style="--bg:#1a5c2a;--edge:#b01558" aria-pressed="true">Independent</button>
          </div>
          <div class="lanes">
            {lane('a', ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'])}
            {lane('i', ['i1', 'i2', 'i3', 'i4', 'i5', 'i6'])}
            {lane('u', ['u1', 'u2', 'u3', 'u4', 'u5', 'u6'])}
          </div>
          <svg class="merge" viewBox="0 0 1200 110" preserveAspectRatio="none" aria-hidden="true"><path d="M200 0 C200 70 600 40 600 110"/><path d="M600 0 L600 110"/><path d="M1000 0 C1000 70 600 40 600 110"/></svg>
          <p class="merge-label">All three lanes meet on the shared road</p>
          <div class="flow-road" style="--bg:#005f6e;--edge:#c62828">{"".join(road_html)}</div>
          {prints('s14', 'e1', [("Accepted", "#step-e1"), ("Modified", "#step-e2"), ("Set aside", "#step-e3")])}
          <div class="endings"><p class="end-label">What counts as an ending</p><div class="end-row">{card(BY['e1'])}{card(BY['e2'])}{card(BY['e3'])}</div><p class="end-note">All three are results. Only the first is usually called one.</p></div>
        </div>

        <div class="flow-legend">
          <span><i class="lk lk-box"></i> a step</span>
          <span><i class="lk lk-dia"></i> a decision, with its branches below it</span>
          <span><i class="lk lk-end"></i> an ending</span>
          <span><i class="lk lk-foot"></i> a footprint: select it for the ways on</span>
        </div>

        <details class="all-steps">
          <summary>Read every step as plain text</summary>
          <div class="sc-list">{content}</div>
        </details>
      </div>
    </section>

    <dialog class="stepdlg" id="stepDlg" aria-labelledby="dlgTitle">
      <div class="dlg-head"><p class="dlg-tag" id="dlgTag"></p><button type="button" class="dlg-x" data-close aria-label="Close">&times;</button></div>
      <h3 id="dlgTitle"></h3>
      <div class="dlg-body" id="dlgBody"></div>
      <div class="dlg-br" id="dlgBr"></div>
      <div class="dlg-nav"><button type="button" class="dlg-prev" id="dlgPrev"></button><button type="button" class="dlg-next" id="dlgNext"></button></div>
    </dialog>
    <div class="fp-menu" id="fpMenu" role="menu" hidden></div>
    <script type="application/json" id="flowData">{flow_json()}</script>
    <!-- FLOW:END -->"""

def flow_json():
    import json
    d = {"order": ORDER,
         "steps": {s["id"]: {"t": s["title"], "lane": s["lane"], "br": s.get("branches", [])} for s in STEPS}}
    return json.dumps(d, ensure_ascii=False).replace("</", "<\\/")

def build_ask():
    cards = "".join(f'<article class="ask" id="{i}"><h3>{esc(t)}</h3>{b.strip()}</article>' for i, t, b in ASK)
    return f"""<!-- ASK:START (generated by tools/quest_map_flow.py) -->
    <section class="q-section q-light" id="ask">
      <div class="q-inner">
        <p class="eyebrow">What people ask</p>
        <h2>The Questions Behind the Map</h2>
        <p class="lede">The map shows the road. These are the questions people ask about the people and the money on it.</p>
        <nav class="ask-nav" aria-label="Questions">{"".join(f'<a href="#{i}">{esc(t)}</a>' for i, t, b in ASK)}</nav>
        <div class="asks">{cards}</div>
      </div>
    </section>
    <!-- ASK:END -->"""

s = open(PAGE, encoding="utf-8").read()
for name, block in (("FLOW", build_flow()), ("ASK", build_ask())):
    pat = re.compile(r"<!-- %s:START.*?<!-- %s:END -->" % (name, name), re.S)
    assert len(pat.findall(s)) == 1, name
    s = pat.sub(lambda m: block, s)
open(PAGE, "w", encoding="utf-8").write(s)
print("quest-map.html: %d steps, %d questions" % (len(STEPS), len(ASK)))
