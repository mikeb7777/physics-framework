# -*- coding: utf-8 -*-
"""Convergence watch (Michael, 7 Oct 2026): as physics takes up consciousness and information, mainstream work
may come to predict what the framework already registered. The Field Watch gains a relation, "convergent",
for a paper that reaches the same specific, numerical prediction by an independent route. Each such review
records our earliest dated record beside theirs, so the dates sit side by side on the Horizon Scanner.
A shared theme ("information is fundamental") is not convergence. Run once."""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

p = os.path.join(ROOT, "field-watch-notes.json")
d = json.load(io.open(p, encoding="utf-8"))
old = "relation is one of: consistent, tension, independent-test, method, context, contact."
assert old in d["_about"]
d["_about"] = d["_about"].replace(old,
    "relation is one of: consistent, tension, independent-test, convergent, method, context, contact. "
    "convergent means the paper reaches the same specific, numerical prediction as one of ours by an independent route "
    "(a shared theme is not enough); add our_record with the date and DOI or URL of our earliest dated record of that "
    "prediction, and their_date, the date their work first appeared.")
d["_example_convergent"] = {
    "doi:10.0000/example": {
        "relation": "convergent",
        "test": "COSMIC-005",
        "note": "Derives the same w0 and wa band from a different starting point.",
        "our_record": {"date": "2026-09-14", "ref": "https://doi.org/10.5281/zenodo.00000000"},
        "their_date": "2027-03-02",
        "reviewed": "2027-03-10"
    }
}
io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

m = os.path.join(ROOT, "media.html")
s = io.open(m, encoding="utf-8").read()
a = "const REL = { 'consistent': 'Consistent', 'tension': 'In tension', 'independent-test': 'Independent test',"
assert s.count(a) == 1
s = s.replace(a, "const REL = { 'consistent': 'Consistent', 'tension': 'In tension', 'independent-test': 'Independent test', 'convergent': 'Convergent',")
a = "      ${n && n.note ? `<p class=\"fw-note\">${esc(n.note)}</p>` : ''}"
assert s.count(a) == 1
s = s.replace(a, a + "\n      ${n && n.relation === 'convergent' && n.our_record ? `<p class=\"fw-note fw-dates\">Our earlier record: <a href=\"${esc(n.our_record.ref)}\" target=\"_blank\" rel=\"noopener\">${esc(n.our_record.date)}</a>${n.their_date ? ` &nbsp;·&nbsp; This work: ${esc(n.their_date)}` : ''}</p>` : ''}")
a = "        .fw-rel { font-size:.72rem;"
assert s.count(a) == 1
s = s.replace(a, "        .fw-rel.convergent { background:#1a1d33; color:#ffffff; }\n        .fw-dates { font-size:.85rem; color:#4a5868; }\n" + a)
io.open(m, "w", encoding="utf-8").write(s)
print("ok")
