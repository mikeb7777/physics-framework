# -*- coding: utf-8 -*-
"""3 Oct 2026, approved by Michael: 501(c)(3) is the legal standing of the Institute's
autonomy, not a threat to independence (status pending); his title is Senior Researcher;
US spelling on the Quest Map. Run once."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def edit(name, pairs):
    p = os.path.join(ROOT, name); s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:60]); s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)

edit("legal.html", [
    ('<h2>Financial Disclosures</h2><span class="last-updated">Last Updated: March 2026</span>',
     '<h2>Financial Disclosures</h2><span class="last-updated">Last Updated: October 2026</span>'),
    ("We disclose this transparently because your financial decisions deserve accurate information. We have not sought 501(c)(3) status in order to preserve full independence and operational flexibility during the institute's current phase of development. Legal entity formation is planned for a future date. If and when our tax status changes, we will update this disclosure immediately and notify all registered users and subscribers.",
     "We disclose this transparently because your financial decisions deserve accurate information. <strong>Status: pending.</strong> The Institute is preparing to incorporate as a US nonprofit corporation and to apply for recognition as a 501(c)(3) public charity. That status is the legal standing of the Institute's autonomy: the Institute is governed by its own board, for its own stated purposes, and answers to no outside owner. It also makes donated money go further, because gifts become tax-deductible and the Institute can apply for grants that are open only to charities. Until then, the notice above applies. When our status changes, we will update this disclosure immediately and notify all registered users and subscribers."),
])
edit("about-page.html", [("<strong>Founder and Principal Researcher:</strong> Michael K. Baines.", "<strong>Senior Researcher:</strong> Michael K. Baines.")])
edit("members.html", [('<p class="member-title">Founder & Lead Researcher</p>', '<p class="member-title">Senior Researcher</p>')])
edit("quest-map.html", [("page charges and colour charges", "page charges and color charges")])
print("done")
