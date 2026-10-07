# -*- coding: utf-8 -*-
"""Publish the held October post "How Often Does Physics Actually Change Its Mind?" (Michael, 7 Oct 2026:
"Since it's October we can upload it"). Source: Downloads/blog-post-HOLD-for-October-changing-its-mind.html.
Dates set to the publication day. Two phrases changed to the house rule "we publish every result" without
qualifiers (the heading "Against Our Own Interest" and "the outcome either way"); "flavour" -> "flavor".
Run once."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), "blog-post-HOLD-for-October-changing-its-mind.html")
h = io.open(SRC, encoding="utf-8").read()

for a, b in [
    ("September 22, 2026", "October 7, 2026"),
    ("<h3>Why We Are Saying This Against Our Own Interest</h3>", "<h3>Why We Do Not Count It as a Prediction</h3>"),
    ("publishes the outcome either way,", "publishes every result,"),
    ("lepton flavour universality", "lepton flavor universality"),
]:
    assert a in h, a
    h = h.replace(a, b)

index = h.split("<!-- INDEX ITEM -->", 1)[1].split("<!-- ARTICLE -->", 1)[0].strip()
article = h.split("<!-- ARTICLE -->", 1)[1].strip()
assert index.startswith('<div class="index-item">') and index.endswith("</div>"), index[-40:]
assert article.startswith("<!-- Blog Post:") and article.endswith("</article>"), article[-40:]

p = os.path.join(ROOT, "blog.html")
s = io.open(p, encoding="utf-8").read()
assert 'id="changing-its-mind"' not in s
a = '      <h2>Recent Articles</h2>\n\n'
assert s.count(a) == 1
s = s.replace(a, a + "      " + index + "\n\n")
a = "    <!-- Blog Post: You Never Experience the Present -->"
assert s.count(a) == 1
s = s.replace(a, "    " + article + "\n\n" + a)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
