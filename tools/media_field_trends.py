# -*- coding: utf-8 -*-
"""Media page: add "How the Field Is Moving" after Field Watch (2 Oct 2026). Michael:
"we should track how funding and interest in the field move over time." Renders
field-trends.json (tools/field_trends.py, weekly in the Field Watch Action): papers
per quarter with share of the topic's arXiv area, and new NSF/NIH awards per year.
Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()
assert 'id="field-trends"' not in s

CSS = """        /* Field Trends */
        .ft-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:1.25rem; }
        .ft-card { background:#fff; border:1px solid #e3e6ea; border-radius:10px; padding:1.1rem 1.2rem 1rem; }
        .ft-card h3 { font-size:1.02rem; margin:0 0 .2rem; color:#1a1d33; }
        .ft-tests { font-size:.75rem; margin-bottom:.6rem; }
        .ft-tests a { color:#005ba5; font-weight:600; text-decoration:none; margin-right:.5rem; }
        .ft-row { margin-top:.55rem; }
        .ft-k { display:flex; justify-content:space-between; align-items:baseline; font-size:.78rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:#5a6878; }
        .ft-v { font-size:.8rem; font-weight:700; letter-spacing:0; text-transform:none; }
        .ft-up { color:#2e7d32; } .ft-down { color:#c62828; } .ft-flat { color:#5a6878; }
        .ft-sub { font-size:.78rem; color:var(--text-light); margin-top:.15rem; }
        .ft-card svg { display:block; width:100%; height:56px; margin-top:.3rem; }
        .ft-rising { background:#fff; border:1px solid #e3e6ea; border-left:4px solid #005ba5; border-radius:10px; padding:1rem 1.25rem; margin-bottom:1.5rem; font-size:.95rem; }
        .ft-notes { font-size:.8rem; color:var(--text-light); margin-top:1.25rem; line-height:1.5; }
"""
i = s.index("        /* Field Watch */")
s = s[:i] + CSS + s[i:]

SECTION = """<!-- ── Field Trends ── -->
<section class="section" id="field-trends">
    <div class="section-inner">
        <p class="section-label eyebrow">Field Trends</p>
        <h2 class="section-title">How the Field Is Moving</h2>
        <p class="section-subtitle">Interest and funding for each question we test, followed over time: how many papers each year, what share of their field they make up, and how much new public funding goes to the work.</p>
        <div class="ft-rising" id="ft-rising" hidden></div>
        <div class="ft-grid" id="ft-grid"><p>Loading the trends&hellip;</p></div>
        <p class="ft-notes" id="ft-notes"></p>
    </div>
</section>

"""
anchor = "<!-- ── Featured Story ── -->"
assert s.count(anchor) == 1
s = s.replace(anchor, SECTION + anchor)

JS = """<script>
/* Field Trends: field-trends.json is refreshed weekly by tools/field_trends.py. */
(function () {
  const grid = document.getElementById('ft-grid'); if (!grid) return;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const money = v => v >= 1e9 ? '$' + (v / 1e9).toFixed(1) + 'B' : v >= 1e6 ? '$' + (v / 1e6).toFixed(1) + 'M' : v >= 1e3 ? '$' + Math.round(v / 1e3) + 'K' : '$' + v;
  const pct = (a, b) => b ? Math.round((a - b) / b * 100) : null;
  const chg = p => p === null ? '' : `<span class="ft-v ${p > 4 ? 'ft-up' : p < -4 ? 'ft-down' : 'ft-flat'}">${p > 0 ? '+' : ''}${p}%</span>`;
  function bars(vals, labels, color, last) {
    const W = 300, H = 56, n = vals.length, max = Math.max(...vals, 1), bw = W / n;
    return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="${esc(labels[0] + ' to ' + labels[n - 1])}">` +
      vals.map((v, i) => `<rect x="${(i * bw + 1).toFixed(1)}" y="${(H - v / max * (H - 4)).toFixed(1)}" width="${Math.max(bw - 2, 1).toFixed(1)}" height="${(v / max * (H - 4)).toFixed(1)}" fill="${color}" opacity="${last && i === n - 1 ? .45 : 1}"><title>${esc(labels[i])}: ${v.toLocaleString()}</title></rect>`).join('') + '</svg>';
  }
  fetch('field-trends.json').then(r => r.json()).then(d => {
    const now = new Date(d.updated || Date.now()), thisYear = now.getFullYear();
    const rising = [];
    grid.innerHTML = Object.entries(d.topics).filter(([id, t]) => Object.keys(t.papers || {}).length >= 24 || Object.keys(t.papers_yearly || {}).length || Object.keys(t.nsf || {}).length > 1).map(([id, t]) => {
      let html = `<article class="ft-card"><h3>${esc(t.label)}</h3><div class="ft-tests">` +
        (t.tests || []).filter(x => /^COSMIC-/.test(x)).map(x => `<a href="testing-schedule.html#${x}">${x}</a>`).join('') + '</div>';
      const months = Object.keys(t.papers || {}).sort();
      if (months.length >= 24) {
        const v = months.map(k => t.papers[k]);
        const last12 = v.slice(-12).reduce((a, b) => a + b, 0), prev12 = v.slice(-24, -12).reduce((a, b) => a + b, 0);
        const qs = {}; months.forEach(k => { const [y, m] = k.split('-'); const q = `${y} Q${Math.ceil(m / 3)}`; qs[q] = (qs[q] || 0) + t.papers[k]; });
        const qk = Object.keys(qs); const lastQFull = months[months.length - 1].endsWith('-03') || months[months.length - 1].endsWith('-06') || months[months.length - 1].endsWith('-09') || months[months.length - 1].endsWith('-12');
        let share = '';
        const base = t.baseline && d.baselines[t.baseline];
        if (base) {
          const b12 = months.slice(-12).reduce((a, k) => a + (base[k] || 0), 0), bp12 = months.slice(-24, -12).reduce((a, k) => a + (base[k] || 0), 0);
          const s1 = b12 ? last12 / b12 * 100 : 0, s0 = bp12 ? prev12 / bp12 * 100 : 0;
          share = `<div class="ft-sub">Share of its arXiv area: ${s1.toFixed(1)}% (a year earlier ${s0.toFixed(1)}%)</div>`;
          if (s0) rising.push([t.label, pct(s1, s0)]);
        }
        html += `<div class="ft-row"><div class="ft-k">Papers, last 12 months ${chg(pct(last12, prev12))}</div>` +
          bars(qk.map(q => qs[q]), qk, '#005ba5', !lastQFull) +
          `<div class="ft-sub">${last12.toLocaleString()} on arXiv in the last 12 months, by quarter since ${qk[0].slice(0, 4)}</div>${share}</div>`;
      } else if (t.papers_yearly && Object.keys(t.papers_yearly).length) {
        const ys = Object.keys(t.papers_yearly).sort(), v = ys.map(y => t.papers_yearly[y]);
        const full = ys.filter(y => +y < thisYear), a = t.papers_yearly[full[full.length - 1]], b = t.papers_yearly[full[full.length - 2]];
        html += `<div class="ft-row"><div class="ft-k">Papers, ${full[full.length - 1]} ${chg(pct(a, b))}</div>` +
          bars(v, ys, '#005ba5', true) + `<div class="ft-sub">${(a || 0).toLocaleString()} in PubMed in ${full[full.length - 1]}, by year since ${ys[0]}</div></div>`;
      }
      for (const [src, name, col] of [['nsf', 'NSF', '#2e7d32'], ['nih', 'NIH', '#8B0000']]) {
        const f = t[src]; if (!f || !Object.keys(f).length) continue;
        const ys = Object.keys(f).sort(), full = ys.filter(y => +y < thisYear);
        const a = f[full[full.length - 1]], b = f[full[full.length - 2]];
        html += `<div class="ft-row"><div class="ft-k">New ${name} funding, ${full[full.length - 1]} ${chg(pct(a.usd, b && b.usd))}</div>` +
          bars(ys.map(y => f[y].usd), ys.map(y => `${y} (${f[y].awards} awards)`), col, true) +
          `<div class="ft-sub">${money(a.usd)} across ${a.awards} awards in ${full[full.length - 1]}, by year since ${ys[0]}</div></div>`;
      }
      return html + '</article>';
    }).join('');
    rising.sort((x, y) => y[1] - x[1]);
    if (rising.length) {
      const el = document.getElementById('ft-rising'); el.hidden = false;
      const say = ([l, p]) => `${esc(l)} (share ${p >= 0 ? 'up' : 'down'} ${Math.abs(p)}%)`;
      const up = rising.filter(r => r[1] > 0).slice(0, 3), down = rising.filter(r => r[1] < 0).slice(-2).reverse();
      el.innerHTML = (up.length ? `<strong>Gaining the most attention:</strong> ${up.map(say).join(' &middot; ')}.` : '')
        + (down.length ? ` <strong>Cooling the most:</strong> ${down.map(say).join(' &middot; ')}.` : '');
      el.hidden = !(up.length || down.length);
    }
    document.getElementById('ft-notes').textContent = `Updated ${d.updated || ''}. ${d.notes || ''} Faded bars are periods still in progress.`;
  }).catch(() => { grid.innerHTML = '<p>The trends could not be loaded.</p>'; });
})();
</script>
"""
i = s.index("<script>\n/* Field Watch:")
s = s[:i] + JS + s[i:]
open(P, "w", encoding="utf-8").write(s)
print("media.html: Field Trends section added")
