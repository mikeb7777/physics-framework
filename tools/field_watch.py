# -*- coding: utf-8 -*-
"""Field Watch: a weekly search of new research that bears on the institute's tests.

Reads tools/field-watch-topics.json, asks arXiv (physics, plus q-bio) and Crossref
(journals arXiv does not cover) for recent papers on each topic, scores each title and
abstract against the topic's terms, and merges the matches into field-watch.json at the
site root, which media.html renders. Standard library only, so the GitHub Action needs
no installs.

Nothing here judges a paper. Reading a paper and recording whether it is consistent,
in tension, an independent test, a method or context belongs in field-watch-notes.json,
which only people edit; the page shows a relation only from that file.

Run: python tools/field_watch.py [--days N] [--new-md path]
  --days    how far back to look (default 21; 60 on the first run)
  --new-md  also write a Markdown list of this run's new items (the Action posts it as an issue)
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS = os.path.join(ROOT, "tools", "field-watch-topics.json")
OUT = os.path.join(ROOT, "field-watch.json")
UA = "Ic2-Field-Watch/1.0 (+https://eequalsicsquared.com/media.html#field-watch)"
KEEP_DAYS, KEEP_MAX = 180, 400
NS = {"a": "http://www.w3.org/2005/Atom"}


def get(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:                      # one bad call should not stop the run
            print(f"  retry {k + 1}: {e}", file=sys.stderr); time.sleep(5 * (k + 1))
    return None


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


def score(text, terms):
    return sum(1 for w in terms if w in text)


def arxiv(q, since):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 50})
    raw = get(url); time.sleep(3.1)                 # arXiv asks for 3 s between calls
    if not raw: return []
    out = []
    for e in ET.fromstring(raw).findall("a:entry", NS):
        pub = e.findtext("a:published", "", NS)[:10]
        if pub < since: continue
        aid = e.findtext("a:id", "", NS).rsplit("/abs/", 1)[-1]
        aid = re.sub(r"v\d+$", "", aid)
        out.append({"id": "arXiv:" + aid, "source": "arXiv", "url": f"https://arxiv.org/abs/{aid}",
                    "title": clean(e.findtext("a:title", "", NS)), "abstract": clean(e.findtext("a:summary", "", NS)),
                    "authors": [clean(a.findtext("a:name", "", NS)) for a in e.findall("a:author", NS)],
                    "date": pub, "venue": "arXiv preprint"})
    return out


def crossref(q, since):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": q, "filter": f"from-pub-date:{since},type:journal-article,has-abstract:true",
        "rows": 40, "select": "DOI,title,author,abstract,published,container-title,URL"})
    raw = get(url); time.sleep(1)
    if not raw: return []
    out = []
    for w in json.loads(raw)["message"]["items"]:
        parts = (w.get("published") or {}).get("date-parts", [[None]])[0]
        if not parts or not parts[0]: continue
        date = "-".join(f"{p:02d}" for p in (parts + [1, 1])[:3])
        out.append({"id": "doi:" + w["DOI"].lower(), "source": "Crossref", "url": f"https://doi.org/{w['DOI']}",
                    "title": clean((w.get("title") or [""])[0]), "abstract": clean(w.get("abstract")),
                    "authors": [clean(f"{a.get('given', '')} {a.get('family', '')}") for a in w.get("author", [])],
                    "date": date, "venue": clean((w.get("container-title") or ["Journal"])[0])})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int); ap.add_argument("--new-md")
    a = ap.parse_args()
    cfg = json.load(open(TOPICS, encoding="utf-8"))
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"items": []}
    items = {i["id"]: i for i in old["items"]}
    today = dt.date.today()
    since = (today - dt.timedelta(days=a.days or (21 if old["items"] else 60))).isoformat()
    new = []
    for t in cfg["topics"]:
        found = []
        if t.get("arxiv"): found += arxiv(t["arxiv"], since)
        if t.get("crossref"): found += crossref(t["crossref"], since)
        kept = 0
        for p in found:
            text = (p["title"] + " " + p["abstract"]).lower()
            if not p["title"] or any(x in text for x in t.get("exclude", [])): continue
            if not all(any(w in text for w in group) for group in t.get("require", [])): continue
            s = score(text, t["terms"])
            if s < t.get("min_score", 3): continue
            kept += 1
            cur = items.get(p["id"])
            if cur:
                if t["id"] not in cur["topics"]:
                    cur["topics"].append(t["id"]); cur["tests"] = sorted(set(cur["tests"]) | set(t["tests"]))
                cur["score"] = max(cur["score"], s)
                continue
            authors = p["authors"]
            p.update({"authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
                      "abstract": p["abstract"][:420].rsplit(" ", 1)[0] + ("…" if len(p["abstract"]) > 420 else ""),
                      "topics": [t["id"]], "tests": list(t["tests"]), "score": s, "first_seen": today.isoformat()})
            items[p["id"]] = p; new.append(p)
        print(f"{t['id']}: {len(found)} found, {kept} kept")
    cutoff = (today - dt.timedelta(days=KEEP_DAYS)).isoformat()
    keep = sorted((i for i in items.values() if i["date"] >= cutoff), key=lambda i: (i["date"], i["score"]), reverse=True)[:KEEP_MAX]
    out = {"updated": today.isoformat(), "since": since,
           "topics": [{k: t[k] for k in ("id", "label", "tests")} for t in cfg["topics"]], "items": keep}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(new)} new, {len(keep)} kept in field-watch.json")
    if a.new_md:
        labels = {t["id"]: t["label"] for t in cfg["topics"]}
        lines = [f"Field Watch found {len(new)} new item(s) on {today.isoformat()}. "
                 "Read the ones that matter and record a relation in `field-watch-notes.json` "
                 "(consistent, tension, independent-test, method, context or contact).", ""]
        for t in cfg["topics"]:
            mine = [p for p in new if p["topics"][0] == t["id"]]
            if not mine: continue
            lines.append(f"### {labels[t['id']]} ({', '.join(t['tests'])})")
            lines += [f"- [{p['title']}]({p['url']}), {p['authors']}, {p['venue']}, {p['date']} (`{p['id']}`)" for p in mine]
            lines.append("")
        open(a.new_md, "w", encoding="utf-8").write("\n".join(lines))
        print("NEW_COUNT", len(new))


if __name__ == "__main__":
    main()
