# -*- coding: utf-8 -*-
"""One main menu (2 Oct 2026). The site survey found more than a dozen header menus on
the institute pages (different items, different orders, the current page dropped).
Michael approved one menu for all of them:
  Framework · Big TOE · Validation · Testing · Quest · Programs · Blog · Discussion ·
  About · Contribute · Join · Member Login
The current page is marked with aria-current="page" instead of being left out. Rewrites
every list in nav.main-navigation, nav.logo-navbar and div.mobile-menu. The Book and
Quest headers (.bigtoe-header) keep their own menus. Rerun after adding a page."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MENU = [("framework.html", "Framework"), ("book.html", "Big TOE"), ("validation.html", "Validation"),
        ("testing-schedule.html", "Testing"), ("quest-map.html", "Quest"), ("programs-gateway.html", "Programs"),
        ("blog.html", "Blog"), ("discussions-page.html", "Discussion"), ("about-page.html", "About"),
        ("contribute.html", "Contribute"), ("join.html", "Join")]
LOGIN = '<li><a href="https://eequalsicsquared.zulipchat.com" target="_blank" rel="noopener" class="login-link"><span class="ml-word">Member </span>Login</a></li>'
SKIP = {"googleffcd006f464d7481.html", "cookie-consent-banner.html", "auth_callback.html", "cosmic_poster.html", "404.html"}


def current_for(page):
    if page.startswith(("program-", "results-")) and page != "results.html":
        return "programs-gateway.html"
    if page.startswith("blog-"):
        return "blog.html"
    return page


def menu_html(page, indent):
    cur = current_for(page)
    lis = [f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in MENU] + [LOGIN]
    return "\n" + "".join(indent + li + "\n" for li in lis) + indent[:-2]


done = []
for f in sorted(glob.glob("*.html")):
    if f in SKIP:
        continue
    s = open(f, encoding="utf-8").read()
    if "bigtoe-header" in s[:s.find("</header>") + 9 if "</header>" in s else 0]:
        continue
    n = 0
    def rewrite(m):
        global n
        indent = re.search(r"\n([ \t]*)<li", m.group(2))
        return m.group(1) + menu_html(f, (indent.group(1) if indent else "        ")) + m.group(3)
    t, k = re.subn(r'(?s)(<(?:nav class="main-navigation"[^>]*|nav class="logo-navbar"[^>]*|div class="mobile-menu"[^>]*)>\s*<ul>)(.*?)(</ul>)', rewrite, s)
    if k:
        open(f, "w", encoding="utf-8").write(t); done.append((f, k))
print(len(done), "pages;", sum(k for _, k in done), "menus")
for f, k in done:
    print(" ", f, k)
