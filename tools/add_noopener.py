"""Add rel="noopener" to every link that opens a new tab without it.
Without it, the opened page can reach back and redirect ours (tab-nabbing)."""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
total = 0
for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    t = open(p, encoding="utf-8").read()

    def fix(m):
        tag = m.group(0)
        if 'target="_blank"' not in tag and "target='_blank'" not in tag:
            return tag
        rel = re.search(r'\brel=(["\'])(.*?)\1', tag)
        if rel:
            if re.search(r"\bno(opener|referrer)\b", rel.group(2)):
                return tag
            return tag[:rel.start(2)] + (rel.group(2) + " noopener").strip() + tag[rel.end(2):]
        return tag[:-1].rstrip() + ' rel="noopener">' if not tag.endswith("/>") else tag[:-2] + ' rel="noopener"/>'

    new, n = re.subn(r"<a\b[^>]*>", fix, t)
    changed = sum(1 for a, b in zip(re.findall(r"<a\b[^>]*>", t), re.findall(r"<a\b[^>]*>", new)) if a != b)
    if changed:
        total += changed
        if "--write" in sys.argv:
            open(p, "w", encoding="utf-8", newline="").write(new)
        print(f"{changed:4d}  {os.path.basename(p)}")
print("total links fixed:", total, "" if "--write" in sys.argv else "(dry run)")
