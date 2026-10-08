# -*- coding: utf-8 -*-
"""Media page: add the Field Watch section (2 Oct 2026). Michael: the Media page does
little work; a system that searches the field for advances that affect us keeps us
current, places the institute inside the field, and may surface people whose results
or testing bear on ours. Renders field-watch.json (tools/field_watch.py, weekly Action)
with reviews from field-watch-notes.json. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()
assert 'id="field-watch"' not in s

OLD_HERO = "<p>News coverage, conference appearances, press resources, and the growing story of independent physics research done differently.</p>"
NEW_HERO = ("<p>What the field is finding that bears on our tests, updated every week, alongside news coverage, "
            "conference appearances and press resources.</p>")
assert s.count(OLD_HERO) == 1
s = s.replace(OLD_HERO, NEW_HERO)

CSS = """
        /* Field Watch */
        .fw-meta { font-size:.85rem; color:var(--text-light); margin:-1rem 0 1.5rem; }
        .fw-list { display:grid; gap:1rem; }
        .fw-item { background:#fff; border:1px solid #e3e6ea; border-left:4px solid #8fa0b0; border-radius:10px; padding:1rem 1.25rem; }
        .fw-item.reviewed { border-left-color:#005ba5; }
        .fw-top { display:flex; flex-wrap:wrap; gap:.4rem .75rem; align-items:center; font-size:.8rem; color:var(--text-light); margin-bottom:.35rem; }
        .fw-title { display:block; font-weight:700; font-size:1.02rem; line-height:1.35; color:#1a1d33; text-decoration:none; }
        .fw-title:hover { color:#8B0000; text-decoration:underline; }
        .fw-authors { font-size:.85rem; color:var(--text-light); margin:.25rem 0 .4rem; }
        .fw-tags { display:flex; flex-wrap:wrap; gap:.4rem; }
        .fw-tag { font-size:.75rem; font-weight:600; padding:.15rem .6rem; border-radius:20px; background:#eef2f6; color:#2d4053; text-decoration:none; }
        a.fw-tag:hover { background:#1a1d33; color:#fff; }
        .fw-rel { font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; padding:.15rem .6rem; border-radius:20px; color:#fff; }
        .fw-rel.consistent { background:#2e7d32; } .fw-rel.tension { background:#c62828; } .fw-rel.independent-test { background:#005ba5; }
        .fw-rel.method, .fw-rel.context, .fw-rel.contact { background:#5a6878; }
        .fw-unread { font-size:.72rem; font-weight:600; color:#5a6878; }
        .fw-note { font-size:.92rem; margin:.5rem 0 .2rem; color:#1a1d33; }
        .fw-item details { margin-top:.4rem; font-size:.88rem; color:#4a5868; }
        .fw-item summary { cursor:pointer; font-weight:600; color:#2d4053; }
        .fw-more { margin-top:1.5rem; }
        @media (max-width:640px) {
            #fw-filters { flex-wrap:nowrap; overflow-x:auto; margin-bottom:1.5rem; padding-bottom:.4rem; scrollbar-width:thin; }
            #fw-filters .filter-btn { flex:0 0 auto; padding:.35rem .9rem; font-size:.82rem; }
        }
        .fw-cta { margin-top:2rem; padding:1.25rem 1.5rem; border-radius:10px; background:#fff; border:1px solid #e3e6ea; }
    </style>"""
i = s.index("</style>")
s = s[:i] + CSS[:-len("    </style>")].rstrip() + "\n" + s[i:]

SECTION = """
<!-- ── Field Watch ── -->
<section class="section bg-light" id="field-watch">
    <div class="section-inner">
        <p class="section-label eyebrow">Field Watch</p>
        <h2 class="section-title">What the Field Is Finding</h2>
        <p class="section-subtitle">Every week an automated search reads new papers on arXiv and in journals for work that bears on our registered tests. Other groups are testing the same questions, and their results can support, challenge or sharpen ours. Papers are listed as they are found; a relation appears only after one of us has read the paper.</p>
        <p class="fw-meta" id="fw-meta">Loading the latest search&hellip;</p>
        <div class="filter-bar" id="fw-filters"></div>
        <div class="fw-list" id="fw-list"></div>
        <button class="filter-btn fw-more" id="fw-more" hidden>Show more</button>
        <div class="fw-cta">
            <strong>Working on one of these questions?</strong> If your measurements or analysis bear on one of our tests, we would like to compare notes and cite your work.
            <a href="about-page.html#contact" class="news-card-link">Get in touch &rarr;</a>
        </div>
    </div>
</section>
"""
anchor = "<!-- ── Featured Story ── -->"
assert s.count(anchor) == 1
s = s.replace(anchor, SECTION.strip() + "\n\n" + anchor)

JS = """
<script>
/* Field Watch: field-watch.json is written weekly by tools/field_watch.py; reviews come from field-watch-notes.json. */
(function () {
  const REL = { 'consistent': 'Consistent', 'tension': 'In tension', 'independent-test': 'Independent test',
                'method': 'Method', 'context': 'Context', 'contact': 'In contact' };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const testLink = t => /^COSMIC-/.test(t) ? `<a class="fw-tag" href="testing-schedule.html#${t}">${t}</a>` : '';
  const STEP = 12; let shown = STEP, filter = 'all', items = [], topics = {};
  function card(i) {
    const n = i.note;
    const rel = n ? `<span class="fw-rel ${esc(n.relation)}">${esc(REL[n.relation] || n.relation)}</span>` : '<span class="fw-unread">Found by search, not yet reviewed</span>';
    const tags = i.topics.map(t => `<span class="fw-tag">${esc(topics[t] ? topics[t].label : t)}</span>`).join('')
               + [...new Set([...(n && n.test ? [n.test] : []), ...i.tests])].map(testLink).join('');
    return `<article class="fw-item${n ? ' reviewed' : ''}">
      <div class="fw-top"><span>${esc(i.date)}</span><span>${esc(i.venue)}</span>${rel}</div>
      <a class="fw-title" href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a>
      <div class="fw-authors">${esc(i.authors)}</div>
      ${n && n.note ? `<p class="fw-note">${esc(n.note)}</p>` : ''}
      <div class="fw-tags">${tags}</div>
      ${i.abstract ? `<details><summary>Abstract</summary><p>${esc(i.abstract)}</p></details>` : ''}
    </article>`;
  }
  function draw() {
    const list = items.filter(i => filter === 'all' || (filter === 'reviewed' ? i.note : i.topics.includes(filter)));
    document.getElementById('fw-list').innerHTML = list.slice(0, shown).map(card).join('') || '<p>Nothing in this group yet.</p>';
    const more = document.getElementById('fw-more'); more.hidden = list.length <= shown;
  }
  Promise.all([fetch('field-watch.json').then(r => r.json()),
               fetch('field-watch-notes.json').then(r => r.json()).catch(() => ({ items: {} }))]).then(([d, notes]) => {
    d.topics.forEach(t => topics[t.id] = t);
    items = d.items.map(i => Object.assign({}, i, { note: (notes.items || {})[i.id] }))
                   .sort((a, b) => (!!b.note - !!a.note) || b.date.localeCompare(a.date));
    const nRev = items.filter(i => i.note).length;
    document.getElementById('fw-meta').textContent =
      `Last search ${d.updated} \\u00b7 ${items.length} papers from the last six months \\u00b7 ${nRev} reviewed`;
    const bar = document.getElementById('fw-filters');
    const btn = (id, label) => `<button class="filter-btn${id === 'all' ? ' active' : ''}" data-f="${id}">${esc(label)}</button>`;
    bar.innerHTML = btn('all', 'All') + (nRev ? btn('reviewed', 'Reviewed') : '')
      + d.topics.filter(t => items.some(i => i.topics.includes(t.id))).map(t => btn(t.id, t.label)).join('');
    bar.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      bar.querySelectorAll('button').forEach(x => x.classList.toggle('active', x === b));
      filter = b.dataset.f; shown = STEP; draw();
    });
    document.getElementById('fw-more').addEventListener('click', () => { shown += STEP; draw(); });
    draw();
  }).catch(() => { document.getElementById('fw-meta').textContent = 'The latest search could not be loaded.'; });
})();
</script>
</body>"""
assert s.count("</body>") == 1
s = s.replace("</body>", JS.strip("\n"))
open(P, "w", encoding="utf-8").write(s)
print("media.html: Field Watch section added")
