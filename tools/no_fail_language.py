# -*- coding: utf-8 -*-
"""Remove "fail" framing from the site (Michael, 29 Sep 2026).

"There is no fail... You fail when you do not look. Every result leads to
understanding and insight... It's not a game, war, or competition. It's a
quest." Results are described by what they showed ("does not hold", "is
refuted"); "falsified" stays, being the honest technical word. Left alone on
purpose: citation titles (Woit, 2006) and direct quotations.

Each entry is (file or "*", old, new). Every entry must match at least once;
anything that does not is reported rather than guessed at.
"""
import glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = [
    # the footer line on every institute page
    ("*", "We publish our failures alongside our successes.", "We publish every result, including the ones that do not hold."),
    ("unsubscribe.html", "and we publish our failures alongside our successes.", "and we publish every result, including the ones that do not hold."),
    # how results are reported
    ("*", "one that has to change and one that fails are all reported the same way", "one that has to change and one that does not hold are all reported the same way"),
    ("about-page.html", "one that has to change and one that fails each add something", "one that has to change and one that does not hold each add something"),
    ("about-page.html", "No hidden failures.", "Nothing held back."),
    ("about-page.html", "Failures will be documented alongside passes.", "Results that do not hold will be documented alongside those that do."),
    ("about-page.html", "including failures and iterations.", "including results that do not hold and every revision."),
    ("about-page.html", "A falsified prediction is data, not a failure.", "A falsified prediction is data, reported as fully as any other."),
    ("legal.html", "We openly acknowledge both successes and failures in our research program.", "We openly report every result in our research program, whether or not it holds."),
    ("validation.html", "Every result, pass or fail, moves the needle.", "Every result, whichever way it goes, moves the needle."),
    ("validation.html", "Recorded as a failure</div>", "Recorded as falsified</div>"),
    ("validation.html", "Recorded as a failure. Edition 7 triggered.", "Recorded as falsified. Edition 7 triggered."),
    ("validation.html", "\"Every result, pass or fail, improves the model.\"", "\"Every result, whichever way it goes, improves the model.\""),
    ("validation.html", "This is not a story about failure.", "This is not a story about winning or losing."),
    ("validation.html", "the failing postulate is identified", "the postulate that did not hold is identified"),
    ("validation.html", "The failing postulate is identified", "The postulate that did not hold is identified"),
    ("validation.html", "No result is wasted. No failure is hidden.", "No result is wasted, and none is hidden."),
    ("validation.html", "A failed validation gate initiates", "A validation gate that is not met initiates"),
    ("validation.html", "a failed prediction is a precise diagnostic", "a falsified prediction is a precise diagnostic"),
    ("validation.html", "It was not triggered by a failed prediction;", "It was not triggered by a falsified prediction;"),
    ("testing-schedule.html", "records every result, pass or fail.", "records every result, whichever way it goes."),
    ("testing-schedule.html", "Failure would not disprove the broader framework, but success would provide strong support.", "A negative result would not disprove the broader framework, but a positive one would provide strong support."),
    ("testing-schedule.html", "the survival overhead formalization fails.", "the survival overhead formalization is refuted."),
    ("testing-schedule.html", "A result that cannot fail is not a test.", "A prediction that cannot be proven wrong is not a test."),
    ("*", "Two masses in spatial superposition become entangled through gravity alone. Fails if", "Two masses in spatial superposition become entangled through gravity alone. Refuted if"),
    ("quest-map.html", "could the prediction fail.", "could the prediction be proven wrong."),
    ("quest-map.html", "What caught them was replication failure and independent researchers", "What caught them was replications that could not reproduce the results, and independent researchers"),
    ("quest-map.html", "A result below the bar is not a failure.", "A result below the bar is not wasted."),
    ("quest-map.html", "Derive something specific enough to fail.", "Derive something specific enough to be proven wrong."),
    ("mission-log.html", "as soon as its premise fails,", "as soon as its premise is shown not to hold,"),
    ("instruments.html", "stated sharply enough to pass or fail cleanly.", "stated sharply enough to be settled cleanly either way."),
    ("instruments.html", "and a prediction that could have failed.", "and a prediction that could have been proven wrong."),
    ("instruments.html", "replicated on more criteria than they failed,", "replicated on more criteria than not,"),
    ("instruments.html", "trying to reproduce the results and failing,", "trying to reproduce the results and being unable to,"),
    # other people's work: no competitive framing
    ("index.html", "These are not four separate failures.", "These are not four separate problems."),
    ("blog-post-institution-and-the-idea.html", "He had failed to secure an academic position after graduation.", "He had not secured an academic position after graduation."),
    ("blog-post-institution-and-the-idea.html", "reframing institutional failure as quality control.", "reframing an institutional blind spot as quality control."),
    ("blog-post-institution-and-the-idea.html", "It fails that screen almost by definition.", "That screen rules it out almost by definition."),
    ("blog-post-institution-and-the-idea.html", "The institution is not failing to do science.", "The institution has not simply lost its way in science."),
    ("blog-post-institution-and-the-idea.html", "Einstein in 1905 fails that screen.", "Einstein in 1905 would not have made it through that screen."),
    ("blog-post-institution-and-the-idea.html", "It allows institutional failure to shelter", "It allows institutional shortcomings to shelter"),
    ("blog.html", "The credential test fails too.", "The credential test does not hold up either."),
    ("blog.html", "two documented authorship failure modes", "two documented authorship problems"),
    ("blog.html", "things fail and no one knows why.", "things go wrong and no one knows why."),
    ("blog.html", "why the experiment kept failing to find what the framework required.", "why the experiment never found what the framework required."),
    ("blog.html", "represents a failure of document control, not a failure of the engineer.", "represents a gap in document control, not a fault of the engineer."),
    ("blog.html", "Structures fail. Systems malfunction.", "Structures collapse. Systems malfunction."),
    ("blog.html", "when the local hidden variable theory fails.", "when local hidden variable theories are ruled out."),
    ("blog.html", "<h3>The Counter-Argument (And Why It Fails)</h3>", "<h3>The Counter-Argument (And Why It Does Not Hold)</h3>"),
    ("blog.html", "This counter-argument fails on multiple levels.", "This counter-argument does not hold, on several levels."),
    # figures of speech and plain physics
    ("framework.html", "That result is not a failure of the equations.", "That result is not a flaw in the equations."),
    ("*", "is not a manufacturing failure.", "is not a manufacturing defect."),
    ("program-cognitive-extension-pilot.html", "This is not a failure of the system.", "This is not a flaw in the system."),
    ("program-consciousness-tuning.html", "That is not a failure. It is a prioritization algorithm", "That is not a flaw. It is a prioritization algorithm"),
    ("blog.html", "The scatter isn't a failure of measurement.", "The scatter isn't a flaw in the measurement."),
    ("blog.html", "That is not a failure. It's a boundary condition", "That is not a flaw. It's a boundary condition"),
    ("blog.html", "Distraction is not a personal failing.", "Distraction is not a personal flaw."),
    ("blog.html", "This is not a personal failure.", "This is not a personal flaw."),
    ("blog.html", "not because his brain is failing, but", "not because his brain is declining, but"),
    ("blog.html", "These aren't just failed Jupiter-like gas giants.", "These aren't just would-be Jupiter-like gas giants."),
    ("blog.html", "that uncertainty is not a failure; it's an invitation.", "that uncertainty is not a setback; it's an invitation."),
    ("*", "exposed iron-nickel core of a failed planet,", "exposed iron-nickel core of a planet that never finished forming,"),
    ("glossary.html", "The failure to consciously perceive", "Not consciously perceiving"),
    ("glossary.html", "failed to notice a person in a gorilla suit", "did not notice a person in a gorilla suit"),
    ("glossary.html", "fail to commute when one is evolved", "no longer commute when one is evolved"),
    ("glossary.html", "a pressure vessel that ultimately fails rather than", "a pressure vessel that ultimately gives way rather than"),
    ("glossary.html", "robustness against random failures.", "robustness against the random loss of nodes."),
    ("appendix.html", "Inflation ends when slow-roll conditions fail.", "Inflation ends when the slow-roll conditions stop holding."),
    ("appendix.html", "where traditional perturbative approaches fail.", "where traditional perturbative approaches break down."),
    ("appendix.html", "the self-consistency condition fails:", "the self-consistency condition cannot be met:"),
    ("appendix.html", "not by failure of the equations but by", "not because the equations break down but because of"),
    ("simulations.html", "which is the well-known failure of jet-style", "which is the well-known flaw of jet-style"),
    ("index.html", "all three Spinner colors fail 3:1 on the", "all three Spinner colors fall below 3:1 on the"),
    # messages a visitor can see if sign-in goes wrong
    ("auth_callback.html", "showError(`Authentication failed: ${error}`);", "showError(`Sign-in did not complete: ${error}`);"),
    ("auth_callback.html", "throw new Error('Failed to exchange token');", "throw new Error('Could not exchange token');"),
    ("auth_callback.html", "throw new Error('Failed to fetch user information');", "throw new Error('Could not fetch user information');"),
]

pages = sorted(p for p in glob.glob(os.path.join(ROOT, "*.html")))
texts = {p: open(p, encoding="utf-8").read() for p in pages}
orig = dict(texts)
missing = []
for target, old, new in R:
    hits = 0
    for p in pages:
        if target != "*" and os.path.basename(p) != target:
            continue
        n = texts[p].count(old)
        if n:
            texts[p] = texts[p].replace(old, new)
            hits += n
    if not hits:
        missing.append((target, old))
    else:
        print(f"{hits:3d}  {target:40s} {old[:60]}")

changed = [p for p in pages if texts[p] != orig[p]]
if "--write" in sys.argv:
    for p in changed:
        open(p, "w", encoding="utf-8", newline="").write(texts[p])
print(f"\n{len(changed)} files {'written' if '--write' in sys.argv else 'would change (dry run)'}")
for t, o in missing:
    print("NOT FOUND:", t, "|", o[:80])
