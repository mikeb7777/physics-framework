# -*- coding: utf-8 -*-
"""Michael, 29 Sep 2026: "Once you see it, you begin to see how often it's
repeated. Publishing everything covers it." Replaces the repeated qualifiers
("whichever way it goes", "including the ones that do not hold", the
holds / has to change / does not hold triad) with plain statements."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITS = {
    "about-page.html": [
        ("and every result, whichever way it goes, joins the public record.", "and every result joins the public record."),
        ("and the record keeps every outcome, including the ones that do not hold.", "and every result is published."),
        ("Every revision is logged, including the September 2026 correction of earlier priority claims. Results that do not hold are recorded beside those that do, and the record is never quietly edited.",
         "Every revision is logged, including the September 2026 correction of earlier priority claims, and the record is never quietly edited."),
        ("Every outcome belongs in the record. A prediction that holds, one that has to change and one that does not hold each add something that was not known before, and the Quest counts what was learned, not who was right.",
         "Every result adds to what is known, and the Quest counts what was learned."),
        ("All data, hypotheses, and results are public, including results that do not hold and every revision. Nothing is withheld to protect a narrative.",
         "All data, hypotheses, results and revisions are public."),
    ],
    "validation.html": [
        ("<strong>Every result, whichever way it goes, moves the needle.</strong>", "<strong>Every result moves the needle.</strong>"),
        ("\"Every result, whichever way it goes, improves the model.\"", "\"Every result improves the model.\""),
    ],
    "quest-map.html": [
        ("Publish every outcome, including the ones against you.", "Publish every result."),
    ],
    "quest-follow.html": [
        ("<h3>Learning, not winning</h3><p>A prediction that holds, one that has to change and one that does not hold are all reported the same way: as what was learned.</p>",
         "<h3>Learning, not winning</h3><p>Every result is reported the same way: as what was learned.</p>"),
    ],
    "legal.html": [
        ("<strong>Knowledge is the quest.</strong> A prediction that holds, one that has to change and one that does not hold are all reported the same way: as what was learned.",
         "<strong>Knowledge is the quest.</strong> Every result is reported the same way: as what was learned."),
    ],
    "testing-schedule.html": [
        ("records every result, whichever way it goes.", "records every result."),
    ],
}
for name, pairs in EDITS.items():
    p = os.path.join(ROOT, name)
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:60])
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", name)
