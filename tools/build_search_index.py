"""Rebuild search-index.json (and the sitemap's page list) from the live pages.

Each entry: u (address), t (short title), d (meta description), h (headings,
joined), x (the first 4,000 characters of visible text). Rendered in Chromium,
so text added by scripts is included. The two blog anchors (posts that live
inline in blog.html) are carried over as they are. Run after pages change.
"""
import glob, json, os, re
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOT_PAGES = {"404.html", "auth_callback.html", "cookie-consent-banner.html", "googleffcd006f464d7481.html",
             "member-bio-template.html", "search.html", "unsubscribe.html"}
old = json.load(open(os.path.join(ROOT, "search-index.json"), encoding="utf-8"))
anchors = [e for e in old if "#" in e["u"]]
order = [e["u"] for e in old if "#" not in e["u"]]
pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")) if os.path.basename(p) not in NOT_PAGES)
pages = [u for u in order if u in pages] + [u for u in pages if u not in order]      # keep the old order, new pages last

JS = r"""() => {
  const t = document.title.split(' | ')[0].trim();
  const d = (document.querySelector('meta[name="description"]') || {}).content || '';
  const h = [...document.querySelectorAll('h1,h2,h3')].filter(e => !e.closest('header,footer,nav') && e.offsetParent)
            .map(e => e.innerText.replace(/\s+/g, ' ').trim()).filter(Boolean).join(' | ');
  const main = document.querySelector('main') || document.body;
  const x = (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 4000);
  return {t, d, h, x};
}"""
out = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 900})
    for u in pages:
        pg.goto(f"http://localhost:8765/{u}", wait_until="load", timeout=30000)
        pg.add_style_tag(content="[data-aos]{opacity:1!important;transform:none!important}")
        pg.wait_for_timeout(200)
        r = pg.evaluate(JS)
        out.append({"u": u, **r})
    b.close()
# blog anchors go back where they were: right after blog.html's neighbours, as before
idx = next((i for i, e in enumerate(out) if e["u"] == "blog.html"), len(out))
out = out[:idx] + anchors + out[idx:]
json.dump(out, open(os.path.join(ROOT, "search-index.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "entries written")
