# -*- coding: utf-8 -*-
"""Citation audit: where the book's references are published, and in what language.

Reads references.html (the site copy of the book's reference lists), removes repeats,
and counts each reference by the region of its journal or publisher. Run after every
book revision and record the numbers in the audit file, so the trend is on the record:

    python3 tools/citation_audit.py            # summary
    python3 tools/citation_audit.py --list     # every reference with its label

What this measures, and what it does not: a journal's home is not its authors' home.
A Chinese team publishing in Physical Review counts as North America here. Author
affiliations need a bibliographic database; OpenAlex (openalex.org, free) gives them
per DOI, and is the next step when it can be reached. First run: 10 October 2026,
GLOBAL-RESEARCH-AUDIT-2026-10.md.
"""
import collections, html, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (pattern, publisher label, region of the publisher), first match wins
V=[
 (r'Chinese Physics|Science China|Sci\. China|Acta Physica Sinica|Chinese Academy','China','Asia (non-Western)'),
 (r'Pramana|Current Science|Indian Academy','India','Asia (non-Western)'),
 (r'JETP|Soviet|Doklady|Uspekhi|Russian Academy|Zhurnal','Russia/USSR','Eastern Europe & Russia'),
 (r'Progress of Theoretical|PTEP|Astronomical Society of Japan','Japan','East Asia (established)'),
 (r'Physical Review|Phys\. Rev|Rev\. Mod\. Phys|Reviews of Modern Physics|PRX|Physics\b, 1\(3\)|Physics Today|AIP|Journal of Mathematical Physics|Journal of Chemical Physics|American Journal of Physics|Applied Physics Letters','APS/AIP','North America'),
 (r'Astrophysical Journal|ApJ|Astronomical Journal|Annual Review|IBM Journal|Bell System|PNAS|Proceedings of the National Academy|PLOS|PLoS|IEEE|Science Advances|\bScience\b,? ?\d|\bScience\b\.|Journal of Neuroscience|Neuron\b|Cognition|Advances in Theoretical and Mathematical|Communications in Pure|NeuroReport|Lippincott|Psychological|American','US society/journal','North America'),
 (r'MIT Press|Princeton University Press|Harvard University Press|University of Chicago Press|Yale University Press|Basic Books|Norton|Penguin|Random House|Viking|Knopf|Simon|Harper|Bantam|Free Press|Vintage|Little, Brown|Houghton|Dutton|Riverhead|Crown|Doubleday|Farrar|Dover|Addison|Freeman|Westview|Broadway|St\. Martin|Academic Press|McGraw|Cengage|Wiley|Prentice|Benjamin|Perseus|Holt|Scribner|Avery|Hay House|Ballantine|Tarcher|Shambhala|Bradford|Cold Spring|Pearson|University of California Press|Columbia University Press|Stanford University Press|Johns Hopkins|Hampton Roads|Inner Traditions|New World Library|Sounds True|Rodale|Grand Central|Back Bay|Hachette|Twelve|Pantheon|Anchor|Belknap|Plenum|Kluwer','US/international book publisher','North America'),
 (r'Nature|Scientific Reports|npj |Cambridge|Oxford|Monthly Notices|MNRAS|IOP|Journal of Physics|New Journal of Physics|Classical and Quantum Gravity|Reports on Progress|JCAP|Journal of Cosmology|Royal Society|Phil\. Trans|Philosophical Transactions|Proc\. R\. Soc|Journal of Consciousness Studies|Imprint|Jonathan Cape|Allen Lane|Bloomsbury|Routledge|Palgrave|Taylor & Francis|Faber|Hutchinson|Heinemann|Butterworth|BMC |Brain\b|Studies in History|Contemporary Physics|Edinburgh|London|Macmillan|Weidenfeld|Bodley|Penguin UK|Allen & Unwin|Pergamon|Philosophical Magazine|Lancet|BMJ|Mind\b','UK publisher','Western Europe'),
 (r'Springer|Foundations of Physics|European Physical Journal|Eur\. Phys\. J|Journal of High Energy|JHEP|Living Reviews|International Journal of Theoretical Physics|Communications in Mathematical Physics|Zeitschrift|Annalen|Göttingen|Preußischen|Sitzungsberichte|Barth|Vieweg|Teubner|Fortschritte|Naturwissenschaften|de Gruyter|Birkhäuser','German/Springer','Western Europe'),
 (r'Elsevier|Physics Letters|Phys\. Lett|Nuclear Physics|Cell\b|NeuroImage|Trends in|Physics Reports|Annals of Physics|Current Biology|BioSystems|Biosystems|Neuroscience & Biobehavioral|Current Opinion|Consciousness and Cognition|Neuropsychologia|Brain Research|Journal of Theoretical Biology|Physica|Progress in|Neuroscience\b|Behavioural Brain|International Journal of Psychophysiology|Medical Hypotheses|Journal of Molecular Biology|FEBS|Icarus|Chaos, Solitons|Neural Networks','Elsevier (NL)','Western Europe'),
 (r'Astronomy & Astrophysics|Astronomy and Astrophysics|A&A|EDP|Bousquet|Lausanne|Geneva|MDPI|Entropy\b|Frontiers|Europhysics|EPL|IUBMB|Gauthier|Paris|Comptes|Hermann','European publisher','Western Europe'),
 (r'Journal of Neurophysiology|Journal of Comparative Neurology|Publications of the Astronomical Society of the Pacific|Chemical Reviews|Biological Bulletin|ACM Symposium','US society/journal','North America'),
 (r'General Relativity and Gravitation|Selecta Mathematica','German/Springer','Western Europe'),
 (r'Experimental Mathematics|Advances in Physics|Journal of Experimental Biology','UK publisher','Western Europe'),
 (r'Vision Research|Journal of Magnetic Resonance','Elsevier (NL)','Western Europe'),
 (r'Quantum, \d|QISS','European publisher','Western Europe'),
 (r'World Scientific','World Scientific (SG)','Asia (non-Western)'),
 (r'arXiv','arXiv preprint','Preprint (global)'),
 (r'Zenodo|Ic² Research|Ic2 Research|eequalsicsquared','Zenodo / Ic²','Institute and archives'),
 (r'Archimedes|Euclid|Plato|Aristotle|Ptolemy|BCE','Classical text','Classical antiquity'),
 (r'DESI|Planck Collaboration|LIGO|Event Horizon|Euclid Consortium|Rubin|LSST|ALMA|JWST|Collaboration|NASA|ESA|CERN','Collaboration / agency','International collaboration'),
]


def classify(ref):
    for pat, lab, reg in V:
        if re.search(pat, ref):
            return lab, reg
    return "unclassified", "Unclassified"


def references():
    s = io.open(os.path.join(ROOT, "references.html"), encoding="utf-8").read()
    items = re.findall(r'<div class="reference-item">\s*<p>(.*?)</p>', s, re.S)
    seen, out = set(), []
    for it in items:
        t = html.unescape(re.sub(r"<[^>]+>", "", it)).strip()
        t = re.sub(r"\s*View Source\s*$", "", t)
        key = re.sub(r"^\[\d+\]\s*", "", t)
        if t and key not in seen:
            seen.add(key)
            out.append(t)
    return out


NON_ENGLISH = r"Invariante|Feldgleichungen|Trägheit|Vorlesungen|Zur Quantenmechanik|Nachweis|Über |Uber die|Introductio"

if __name__ == "__main__":
    refs = references()
    regions = collections.Counter(classify(r)[1] for r in refs)
    print(f"{len(refs)} unique references")
    for k, v in regions.most_common():
        print(f"{v:5d}  {100 * v / len(refs):5.1f}%  {k}")
    ne = [r for r in refs if re.search(NON_ENGLISH, r)]
    print(f"{len(ne):5d}  references with a title not in English (all German or Latin)")
    if "--list" in sys.argv:
        for r in refs:
            print(f"{classify(r)[1]:28s} | {r[:140]}")
