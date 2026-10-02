# -*- coding: utf-8 -*-
"""Around the World: research output and funding by country for the institute's fields.

Source: OpenAlex (openalex.org), a free, open index of about 250 million scholarly works
in every language, with each author's institution and country. Chosen over arXiv, which
leans heavily toward Western physics.

For each field and year: papers per country (an author from the country counts the paper
for it), share of the world's papers in the field, a specialization index (the country's
share of the field over its share of all science; 1.0 = world average, so small and
non-Western countries that focus on a field show up, not only the largest producers),
papers per continent, and papers acknowledging funding from each country's agencies.

Caveats, shown on the page: OpenAlex's coverage roughly doubled for 2025, so raw counts
over time mislead and the page shows shares; Chinese-, Russian- and other national-language
journals are only partly indexed, so those countries are likely undercounted; funding is
counted as acknowledgments, not money.

Writes field-regions.json at the site root. Standard library only.
Run: python tools/field_regions.py
"""
import datetime as dt, json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "field-regions.json")
API = "https://api.openalex.org/works"
UA = "Ic2-Horizon-Scanner/1.0 (+https://eequalsicsquared.com/media.html#field-regions)"
YEARS = list(range(2016, 2025))   # through 2024: OpenAlex coverage roughly doubled for 2025; extend once it settles
FUNDER_YEARS = 3                                           # funder breakdown for the latest N years
FIELDS = [
    ("consciousness", "Consciousness", "concepts.id:C186720457", ["COSMIC-013"]),
    ("cosmology", "Cosmology and gravitation", "topics.id:T10095", ["COSMIC-005", "COSMIC-006", "COSMIC-008"]),
    ("quantum-computing", "Quantum computing", "topics.id:T10682", ["COSMIC-002"]),
    ("quantum-foundations", "Quantum information and foundations", "topics.id:T10020|T10622", []),
    ("thermo", "Thermodynamics and statistical mechanics", "topics.id:T11520", []),
    ("sleep", "Sleep and wakefulness", "topics.id:T10985", []),
    ("brain", "Brain dynamics and working memory", "topics.id:T10581", []),
]


def get(url, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90) as r:
                return json.loads(r.read())
        except Exception as e:
            print(f"  retry {k + 1}: {e}", file=sys.stderr); time.sleep(4 * (k + 1))
    raise SystemExit(f"failed: {url}")


def known(filt):
    """Papers with at least one author country recorded: the base for every share."""
    d = get(f"{API}?" + urllib.parse.urlencode({"filter": f"{filt},authorships.countries:!null", "per_page": 1}))
    time.sleep(0.15)
    return d["meta"]["count"]


def group(filt, by):
    d = get(f"{API}?" + urllib.parse.urlencode({"filter": filt, "group_by": by, "per_page": 200}))
    time.sleep(0.15)
    return d["meta"]["count"], {g["key"].rsplit("/", 1)[-1]: (g["key_display_name"], g["count"]) for g in d["group_by"]}


def main():
    names, out = {}, {"fields": [], "years": YEARS, "world": {}, "countries": {}}
    # every country's total output each year: the denominator for specialization
    for y in YEARS:
        tot, by = group(f"publication_year:{y}", "authorships.countries")
        out["world"][y] = {"total": tot, "known": known(f"publication_year:{y}"), "countries": {c: n for c, (_, n) in by.items()}}
        names.update({c: nm for c, (nm, _) in by.items()})
    print("country totals done", flush=True)
    funder_country = {}
    for fid, label, filt, tests in FIELDS:
        rec = {"id": fid, "label": label, "filter": filt, "tests": tests, "years": {}}
        for y in YEARS:
            tot, by = group(f"{filt},publication_year:{y}", "authorships.countries")
            names.update({c: nm for c, (nm, _) in by.items()})
            _, cont = group(f"{filt},publication_year:{y}", "authorships.institutions.continent")
            yr = {"total": tot, "known": known(f"{filt},publication_year:{y}"), "countries": {c: n for c, (_, n) in by.items()},
                  "continents": {nm: n for _, (nm, n) in cont.items() if nm and nm.lower() not in ("unknown", "antarctica")}}
            if y >= YEARS[-FUNDER_YEARS]:
                _, fun = group(f"{filt},publication_year:{y}", "funders.id")
                yr["funders"] = {f: n for f, (_, n) in fun.items()}
                yr["funder_names"] = {f: nm for f, (nm, _) in fun.items()}
            rec["years"][y] = yr
        out["fields"].append(rec)
        print(f"{fid}: done", flush=True)
    # funder countries, resolved 50 at a time
    ids = sorted({f for r in out["fields"] for y in r["years"].values() for f in y.get("funders", {})})
    for i in range(0, len(ids), 50):
        d = get("https://api.openalex.org/funders?" + urllib.parse.urlencode(
            {"filter": "openalex_id:" + "|".join(ids[i:i + 50]), "per_page": 50, "select": "id,country_code"}))
        for f in d["results"]:
            funder_country[f["id"].rsplit("/", 1)[-1]] = f.get("country_code")
        time.sleep(0.15)
    for r in out["fields"]:
        for y in r["years"].values():
            if "funders" not in y: continue
            byc, top = {}, []
            for f, n in y["funders"].items():
                c = funder_country.get(f)
                if c: byc[c] = byc.get(c, 0) + n
                top.append((n, y["funder_names"].get(f, f), c))
            y["funded_by_country"] = byc
            y["top_funders"] = [[nm, c, n] for n, nm, c in sorted(top, reverse=True)[:10]]
            del y["funders"], y["funder_names"]
    out["countries"] = names
    # ISO alpha-2 -> numeric, so the page can join countries to the world-atlas map
    codes = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://cdn.jsdelivr.net/npm/i18n-iso-countries@7/codes.json", headers={"User-Agent": UA}), timeout=60).read())
    out["iso_numeric"] = {a2: num for a2, _, num, *_ in codes if a2 in names}
    out["updated"] = dt.date.today().isoformat()
    out["notes"] = ("Source: OpenAlex, an open index of scholarly works in every language. A paper counts for every country among its authors' "
                    "institutions. Shares are of papers with at least one author country recorded. Specialization is a country's share of the field divided by its share of all research (1.0 = world average). "
                    "Funding counts papers acknowledging a funder from that country, not money. OpenAlex coverage roughly doubled for 2025, so "
                    "the charts stop at 2024 until it settles; national-language journals (for example Chinese and Russian) are only partly indexed, "
                    "so those countries are likely undercounted.")
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"field-regions.json: {os.path.getsize(OUT) // 1024} KB, {len(funder_country)} funders")


if __name__ == "__main__":
    main()
