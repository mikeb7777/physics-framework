# -*- coding: utf-8 -*-
"""Field Trends: how interest and funding in each Field Watch topic move over time.

Interest: arXiv papers per month matching each topic's search (the same query Field
Watch uses), and the same month's total for the topic's arXiv area (its "baseline"), so
the page can show share as well as raw growth. PubMed yearly counts for the biology and
cognition topics.
Funding: new US federal awards per year whose title or abstract match the topic's
phrases: NSF Award Search (count and award size) and, for the biology topics, NIH RePORTER.

These are proxies, not totals: they show direction, not the size of the whole field.
Writes field-trends.json at the site root, rendered on media.html. Standard library only.

Run: python tools/field_trends.py            refresh recent months and the last two years
     python tools/field_trends.py --backfill fill everything from 2018 (about an hour, once)
"""
import argparse, datetime as dt, json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS = os.path.join(ROOT, "tools", "field-watch-topics.json")
OUT = os.path.join(ROOT, "field-trends.json")
UA = "Ic2-Field-Watch/1.0 (+https://eequalsicsquared.com/media.html#field-trends)"
START_YEAR = 2018


def fetch(url, data=None, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **({"Content-Type": "application/json"} if data else {})})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except Exception as e:
            print(f"  retry {k + 1}: {e}", file=sys.stderr); time.sleep(6 * (k + 1))
    return None


def arxiv_count(q, y, m):
    last = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    full = f"({q}) AND submittedDate:[{y}{m:02d}010000 TO {y}{m:02d}{last}2359]"
    raw = fetch("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": full, "max_results": 1}))
    time.sleep(3.1)
    if not raw: return None
    s = raw.decode("utf-8", "replace"); i = s.find("<opensearch:totalResults")
    return int(s[s.index(">", i) + 1: s.index("<", i + 1)]) if i >= 0 else None


def pubmed_count(term, y):
    raw = fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": f"({term}) AND {y}[dp]", "rettype": "count", "retmode": "json"}))
    time.sleep(0.4)                                  # NCBI allows 3 calls a second without a key
    return int(json.loads(raw)["esearchresult"]["count"]) if raw else None


def nsf_year(phrases, y):
    seen = {}
    for ph in phrases:
        off = 1
        while True:
            raw = fetch("https://api.nsf.gov/services/v1/awards.json?" + urllib.parse.urlencode(
                {"keyword": ph, "dateStart": f"01/01/{y}", "dateEnd": f"12/31/{y}", "rpp": 25, "offset": off,
                 "printFields": "id,estimatedTotalAmt,fundsObligatedAmt"}))
            if raw is None: return None
            aw = json.loads(raw)["response"].get("award", [])
            for a in aw:
                seen[a["id"]] = float(a.get("estimatedTotalAmt") or a.get("fundsObligatedAmt") or 0)
            if len(aw) < 25 or off > 5000: break
            off += 25
    return {"awards": len(seen), "usd": round(sum(seen.values()))}


def nih_year(phrases, y):
    seen = {}
    for ph in phrases:
        off = 0
        while True:
            body = json.dumps({"criteria": {"advanced_text_search": {"operator": "and", "search_field": "projecttitle,abstracttext", "search_text": ph},
                                            "fiscal_years": [y]}, "include_fields": ["ApplId", "AwardAmount"], "offset": off, "limit": 500}).encode()
            raw = fetch("https://api.reporter.nih.gov/v2/projects/search", body); time.sleep(1.1)
            if raw is None: return None
            d = json.loads(raw)
            for r in d["results"]: seen[r["appl_id"]] = r.get("award_amount") or 0
            off += 500
            if off >= d["meta"]["total"] or off >= 14500: break
    return {"awards": len(seen), "usd": round(sum(seen.values()))}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--backfill", action="store_true"); a = ap.parse_args()
    cfg = json.load(open(TOPICS, encoding="utf-8"))
    data = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"topics": {}, "baselines": {}}
    today = dt.date.today()
    months = [(y, m) for y in range(START_YEAR, today.year + 1) for m in range(1, 13) if (y, m) < (today.year, today.month)]
    recent = set(months[-3:])
    years = list(range(START_YEAR, today.year + 1))

    def due(store, key, is_recent):
        return a.backfill and key not in store or is_recent or key not in store

    for t in cfg["topics"]:
        rec = data["topics"].setdefault(t["id"], {"papers": {}, "papers_yearly": {}, "nsf": {}, "nih": {}})
        rec.update({"label": t["label"], "tests": t["tests"], "baseline": t.get("baseline")})
        if t.get("arxiv"):
            for (y, m) in months:
                k = f"{y}-{m:02d}"
                if due(rec["papers"], k, (y, m) in recent):
                    c = arxiv_count(t["arxiv"], y, m)
                    if c is not None: rec["papers"][k] = c
            if t.get("baseline"):
                b = data["baselines"].setdefault(t["baseline"], {})
                for (y, m) in months:
                    k = f"{y}-{m:02d}"
                    if due(b, k, (y, m) in recent):
                        c = arxiv_count(t["baseline"], y, m)
                        if c is not None: b[k] = c
        if t.get("pubmed"):
            for y in years:
                if due(rec["papers_yearly"], str(y), y >= today.year - 1):
                    c = pubmed_count(t["pubmed"], y)
                    if c is not None: rec["papers_yearly"][str(y)] = c
        for y in years:
            if t.get("nsf") and due(rec["nsf"], str(y), y >= today.year - 1):
                r = nsf_year(t["nsf"], y)
                if r: rec["nsf"][str(y)] = r
            if t.get("nih") and due(rec["nih"], str(y), y >= today.year - 1):
                r = nih_year(t["nih"], y)
                if r: rec["nih"][str(y)] = r
        print(f"{t['id']}: {len(rec['papers'])} months, nsf {len(rec['nsf'])} y, nih {len(rec['nih'])} y", flush=True)
        json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # save as we go
    data["updated"] = today.isoformat()
    data["notes"] = ("Papers: arXiv preprints per month matching each topic's search (PubMed papers per year for the biology and cognition topics); share = that count over all papers in the topic's arXiv area. "
                     "Funding: new NSF awards (estimated total) and NIH projects (fiscal-year amount) whose title or abstract match the topic's phrases. "
                     "US federal funding only. These are proxies that show direction, not the size of the whole field. The current year is partial.")
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("field-trends.json updated")


if __name__ == "__main__":
    main()
