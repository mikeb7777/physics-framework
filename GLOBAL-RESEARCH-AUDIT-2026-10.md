<!--
Global research audit of A Quest for The Big TOE and the website.
Run 10 October 2026 against Version 6E and references.html.
Repeat after every book revision with tools/citation_audit.py and add a dated
section below; do not overwrite the earlier numbers.
-->

# Global research audit, October 2026

**Status:** first run complete. Book changes proposed in
`6F-PROPOSED-CHANGES.md`, awaiting Michael's decision. Site changes made in the
same commit as this file.

**Why this exists.** Michael, 10 October 2026: the site and the book favor
Western research and practice, while China has made large strides and research
from Africa, Latin America and elsewhere is little known. The aim is to find
what reduces that bias and add it: to the book, the Quest Map, the site, and a
blog article that also explains the corrections.

The framing used throughout: the divide is not West against East. Japan and
Korea publish through the same journals, databases and conferences as the
United States and Europe. The useful line is between **research that is easy
to see from an English-language search and research that is not**.

---

## 1. What was measured, and the limits

`tools/citation_audit.py` reads every reference list on `references.html`
(the site copy of the book's references), removes repeats, and counts each
work by where its **journal or publisher** is based.

That is a proxy, and it understates the problem in one direction and
overstates it in another:

- **It misses non-Western authors in Western journals.** A team at the
  University of Science and Technology of China publishing in *Physical
  Review X* counts as North America. The book cites at least two such papers.
- **It cannot see what was never found.** A literature search that only uses
  English-language indexes will not turn up a Chinese, Russian or Portuguese
  paper, so it never reaches the reference list to be counted.

The proper measure is author affiliation by country, which needs a
bibliographic database. OpenAlex (openalex.org, free) gives it per DOI. It
could not be reached from the environment this audit ran in, so that pass is
listed under next steps.

## 2. Results

**368 unique works** cited across the book's reference lists.

| Region of the journal or publisher | Works | Share |
|---|---|---|
| Western Europe (UK, Germany, Netherlands, Switzerland, France) | 181 | 49.2% |
| North America | 174 | 47.3% |
| The institute's own Zenodo deposits | 6 | 1.6% |
| arXiv preprints | 3 | 0.8% |
| Russia and the USSR (*JETP Letters*, *Soviet Journal of Experimental and Theoretical Physics*) | 2 | 0.5% |
| Japan (*Progress of Theoretical Physics*) | 1 | 0.3% |
| Classical antiquity (Archimedes) | 1 | 0.3% |
| China, India, the rest of Asia, Africa, Latin America, the Middle East | **0** | **0%** |

**96.5 percent** of the works are published in North America or Western
Europe. **Twenty** have titles in a language other than English, and every one
is German or Latin: Einstein, Born, Heisenberg, Boltzmann, Noether, Stern and
Gerlach, Euler. No work in Chinese, Japanese, Russian, Spanish, Portuguese,
Arabic or any other language is cited.

**Work from outside North America and Western Europe that is in the book**,
found by reading rather than by the script:

| Work | Where the research was done | Element |
|---|---|---|
| Yin et al. (2017), satellite entanglement distribution over 1,200 km (*Science*) | China, the Micius satellite | Element 13 |
| Li et al. (2017), out-of-time-order correlators on an NMR simulator (*PRX*) | China | Element 20 |
| Super-Kamiokande proton decay search (2020) | Japan | Element 5 |
| Kobayashi and Maskawa (1973), CP violation | Japan | Element 5 |
| Sakharov (1967); Belinskii, Khalatnikov and Lifshitz (1970); Larkin and Ovchinnikov (1969) | USSR | Elements 5, 19, 20 |
| HERA (2017); the Square Kilometre Array (2009) | Instruments sited in South Africa (the SKA also in Australia) | Element 11; Conclusion |

So the book is not empty of this work, but what it cites from outside the
West is either Japanese, Soviet-era, or Chinese work that happened to appear
in an American journal.

## 2a. Second run: Version 6F (10 October 2026)

Same script, same method. 6F adds eight reference entries (Singh; Imhausen,
twice; Martzloff; Plofker; Berggren, twice; He et al.).

| | 6E | 6F |
|---|---|---|
| Reference entries counted | 368 | 376 |
| Published in North America or Western Europe | 96.5% | 96.5% |

The share did not move, and that is the measure's limit, not a failure of the
revision. Every new reference is about mathematics or physics done outside the
West, by Egyptian, Chinese, Indian and Persian mathematicians and a Chinese
quantum computing team, but each is published by a Western press or journal
(Princeton, Springer, Elsevier, the American Physical Society). The venue count
cannot see whose work is being credited. The affiliation pass in section 8 is
what can.

## 3. History credits

The book was searched for every passage that names who discovered or first
described something. Most are correctly credited and need no change (Euclid,
Plato and the Platonic solids, Newton, Boltzmann, Euler's *e*). Two passages
are worth widening. Neither is a misattribution; both tell only the European
half of a longer story.

| Passage | What it says | What it leaves out |
|---|---|---|
| "The Binary Condition and Conservation", p. 28; Element 14, p. 292 | Names the Fibonacci sequence | The sequence was described in Indian studies of poetic meter centuries before Leonardo of Pisa's *Liber Abaci* (1202): Pingala, then Virahanka (c. 700) and Gopala and Hemachandra (c. 1135 to 1150). Singh, *Historia Mathematica* 12 (1985). |
| Element 1, p. 51; reference [13] Archimedes | Cites Archimedes alone for π | Liu Hui (3rd century) and Zu Chongzhi (5th century) took the polygon method to 3.1415926 < π < 3.1415927 and the ratio 355/113, about a thousand years before Europe had it. Madhava of Sangamagrama found an infinite series for π around 1400, nearly three centuries before Gregory and Leibniz. |

The draft blog suggested two more: Madhava against Leibniz, and Ibn al-Haytham
on optics and experimental method. Madhava is covered above. The book does not
discuss the history of optics or of the experimental method, so there is
nothing to correct; Ibn al-Haytham goes in the blog article instead.

### 3a. Persia, Egypt, Ethiopia and Babylon (added 10 October 2026)

Michael asked whether early mathematics from Persia, Egypt and Ethiopia had
been checked. It had not: the first pass only examined passages that name a
discoverer, and the book names none from these traditions. A second pass
looked for places where their work bears on what the book discusses.

| Tradition | Finding | Where it bears on the book | Outcome |
|---|---|---|---|
| Egypt | The Rhind papyrus (copied c. 1550 BCE from a text of about 1850 BCE; British Museum EA10057) works with π ≈ 256/81 ≈ 3.16, within 1%; Egyptian multiplication is by repeated doubling, which decomposes a number into powers of two | The π passage (Element 1); "The Binary Condition and Conservation" | Proposed for 6F (A2, A3) |
| Persia | al-Kashi, Samarkand, July 1424: 2π to nine sexagesimal places, sixteen decimal places, unbeaten for nearly two centuries (MacTutor, Britannica). "Algorithm" comes from the Latinized name of al-Khwarizmi, and "algebra" from his *al-jabr* | The π passage; the book's frequent use of "algorithm" | Proposed for 6F (A2, and A4 as optional) |
| Ethiopia | Halving-and-doubling multiplication, still taught in Ethiopia and Eritrea; its origin is not documented in any scholarly source found. Bahre Hasab, the Ethiopian Orthodox calendar computation kept in Ge'ez manuscripts, subject of a University of Münster project (2025–2030), which notes that many of its elements came from Hellenistic, Arabic or European sources | The binary passage, as a living tradition only | Mentioned in A3 without claiming a date or a first; Bahre Hasab in the blog and on the site |
| Babylon | YBC 7289 (Old Babylonian): √2 as 1;24,51,10 in base 60, off by about 4 parts in 10 million (Fowler and Robson, *Historia Mathematica* 25, 1998) | No direct passage in the book | Blog, Global Research page and appendix only |

## 4. Where relevant work from outside the West exists and the book does not cite it

| Book passage | Missing work | Status |
|---|---|---|
| Element 21, Quantum Error Correction, built on Google's Willow (December 2024) | USTC's Zuchongzhi 3.2 processor reported error correction below the surface-code threshold, a distance-7 code with a suppression factor of about 1.4, in *Physical Review Letters*, December 2025. It is the **second independent demonstration** of the result the element rests on, which matters more to the framework than the first. | Proposed for 6F. Confirm the exact citation against PRL before it goes in. |
| Element 21 | USTC's 2022 distance-3 surface code on Zuchongzhi 2.1, *PRL* 129, 030501, an earlier step on the same road | Optional |
| The book's two passages on neutrinos | JUNO (Jiangmen, China) began taking data on 26 August 2025; its first result, *Nature*, June 2026, improved the precision of the two solar oscillation parameters by a factor of 1.6 over all previous experiments combined | Not proposed for the book: neither passage depends on oscillation parameters. Used in the blog article. |

## 5. Fact-check of the draft article

The draft came from a separate chat. Every factual claim was checked on 10
October 2026. Outcomes:

| Claim | Outcome |
|---|---|
| Nature Index 2026: China first; output up 22.4% from 2024 to 2025; only top-10 country with double-digit growth; first in physical sciences, chemistry, biological, applied, earth and environmental sciences; US first in health and social sciences | Confirmed (RTHK, CGTN, Research Information, June 2026). Note the 2026 index changed its method, so year-on-year comparisons are rough. |
| Nature Index counts "178 selective journals, mostly from Western publishers" | Corrected: 177 journals and one conference, chosen through a survey of more than 4,000 researchers. "Mostly Western" is not what the source says; it says 84% are published outside Springer Nature. |
| JUNO 700 m underground; data from 26 August 2025; first results in *Nature*, June 2026; uncertainty on two parameters reduced by a factor of about 1.6 | Confirmed (IHEP, CAS, IIHE). The two parameters are θ₁₂ and Δm²₂₁, the solar ones. |
| JUNO the first of three next-generation neutrino experiments to be completed; Hyper-Kamiokande 2028; DUNE beam 2031 | Softened: Hyper-K is expected in the late 2020s and DUNE's beam in the early 2030s. The specific years were not confirmed. |
| China: 16.5% of output, more than 52% of retractions across ten publishers, paper mills | Confirmed with a precision fix: the 52% counts affiliations on retracted papers across ten publishers, and the 16.5% is China's share of those publishers' output. The analysis is an arXiv preprint (2602.19197), not yet peer reviewed. |
| China's 2023 change to physician evaluation | **Not confirmed. Dropped.** |
| AJOL the world's largest collection of African-published, peer-reviewed journals; JPPS quality assessment | JPPS confirmed (AJOL, INASP). "Largest" not confirmed by an independent source: dropped; AJOL hosts over 500 journals. |
| MeerKAT a precursor of the SKA | Confirmed (SKAO). |
| Latin America "the region with the greatest adoption of open access" | **Not confirmed. Softened** to "often held up as the model". The SciELO and Redalyc study (1,720 journals, 15 countries, 908,982 documents, mostly diamond) is confirmed. |
| ALMA in Chile; Pierre Auger Observatory in Argentina | Well established. |
| CNKI ending access outside mainland China, March 2023 | Corrected: from 1 April 2023 CNKI suspended some databases for some overseas institutions, mainly theses and conference proceedings; scope varied, and some university libraries abroad kept access. |
| SESAME: Jordan, modeled on CERN; members Cyprus, Egypt, Iran, Israel, Jordan, Pakistan, Palestine, Turkey; first fully renewable-powered | Confirmed (Physics World, CERN, Royal Hashemite Court). Solar plant inaugurated February 2019. |
| DergiPark; SID | Confirmed, with a note: DergiPark is a hosting platform, not an index (TR Dizin is the index). |
| Ulugh Beg's Samarkand catalog among the most accurate of its era | Confirmed (MacTutor; about 1,000 stars, 1437; not surpassed until Taqi ad-Din and Tycho Brahe). |
| Maidanak Observatory, exceptionally steady skies | Confirmed: median seeing 0.69 arcseconds, 2018 to 2021 (*JATIS* 8, 047002). |
| Tien Shan high-altitude cosmic ray station near Almaty | Confirmed: 3,340 m, Lebedev Physical Institute. |
| Lithuania's first laser in 1966 | **Not confirmed. Dropped.** |
| Lithuania supplies more than half the world's ultrashort-pulse scientific lasers; Light Conversion and Ekspla built ELI systems; lasers at CERN and NASA | Confirmed as the Lithuanian government's figure; CORDIS gives a product-by-product split. Attributed to the source rather than stated flat. |
| ThaiJO; Thai synchrotron; Thai National Observatory | ThaiJO confirmed (TCI Centre). The facilities are well established. |
| Garuda the national index; SINTA the better quality guide | Confirmed: Garuda indexes for discovery only, and accreditation ranks are reported through SINTA. |
| Shodhganga; CyberLeninka; JINR harder to follow since 2022 | Confirmed. CERN suspended JINR's observer status in 2022 and stopped new passes for Russian institutions; the CERN-JINR agreement continued. |
| Madhava's series around the 14th century, before Leibniz | Confirmed (MacTutor, c. 1400). |

## 6. Changes made to the site with this audit

- **`global-research.html`, new:** where research from each region is published, how to reach it and whether you can, how we weigh any source, and how to read a paper in another language. It asks readers who can reach a restricted database, through a library abroad, a home university, or because they live in the region, to say so.
- **The blog article** "Reading the Whole Map", with the corrections in its own section.
- **The Quest Map:** the International path now names instruments outside Europe and North America, and a new section covers the half of the map an English-language search does not show.
- **`references.html`:** a note on the reach of the list, with the numbers above and a link to this work, and a separate section listing the references proposed for 6F, marked as not yet in the book.
- **`appendix.html`:** the independent Zuchongzhi 3.2 replication in Element 21, and a supplement on independent routes to π and to binary arithmetic, both marked as website notes not yet in the book.
- **`glossary.html`:** new terms: Algorithm, Diamond Open Access, Fibonacci Sequence, Neutrino Oscillation, Paper Mill, Pi (π), Preprint, Retraction, Sexagesimal.

## 7. Practices adopted

1. **Rerun this audit at every book revision** and add a dated section here.
2. **Search beyond the default tools.** OpenAlex as well as Google Scholar, and the regional databases on the Global Research page, for any literature search behind a book revision or a test.
3. **Check who got there first** for every historical credit in a revision.
4. **One standard in both directions.** Overlooked research is not better for being overlooked. The same checks apply to every source, including the retraction check.
5. **Treat AI summaries of a region's research as a starting point.** The assistant that drafted this work learned mostly from English-language sources and said so; that is why every claim above was checked.

## 8. Next steps

| Step | Owner | Note |
|---|---|---|
| Decide the 6F proposals | Michael | `6F-PROPOSED-CHANGES.md` |
| Affiliation audit through OpenAlex | Anyone who can reach it | `tools/citation_audit.py` documents the step; it needs a machine that can reach api.openalex.org |
| Outside readers from other regions for chapters and site pages | Institute | Fits the outreach planned for the incorporated institute |
| Translate the key pages outward: Chinese, Spanish, Arabic, Thai | Michael to decide | Machine translation reviewed by a native reader, labelled as such |
