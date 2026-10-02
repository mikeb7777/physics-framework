# -*- coding: utf-8 -*-
"""Horizon Scanner: add "Around the World" after Trends (2 Oct 2026). Michael: a regional
comparison of research and investment around the world (for example, is China doing more
consciousness research?), the charts that turn the page from media into data analysis,
and avoid Western bias. Renders field-regions.json (tools/field_regions.py, OpenAlex):
world map, ranking, share over time, continents, and top funders. d3 and the map load
only when the section comes into view. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()
assert 'id="field-regions"' not in s

CSS = """        /* Around the World */
        .rg-controls { display:flex; flex-wrap:wrap; gap:.75rem 1.25rem; align-items:center; margin-bottom:1rem; }
        .rg-controls label { font-size:.8rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:#5a6878; display:flex; flex-direction:column; gap:.3rem; }
        .rg-controls select { font:600 .95rem 'IBM Plex Sans', sans-serif; padding:.45rem .7rem; border:1px solid #cfd6de; border-radius:8px; background:#fff; color:#1a1d33; max-width:100%; }
        .rg-seg { display:inline-flex; border:1px solid #cfd6de; border-radius:8px; overflow:hidden; flex-wrap:wrap; }
        .rg-seg button { font:600 .85rem 'IBM Plex Sans', sans-serif; padding:.45rem .8rem; border:0; background:#fff; color:#2d4053; cursor:pointer; }
        .rg-seg button.on { background:#1a1d33; color:#fff; }
        .rg-insight { background:#fff; border:1px solid #e3e6ea; border-left:4px solid #005ba5; border-radius:10px; padding:1rem 1.25rem; margin-bottom:1.25rem; font-size:.98rem; line-height:1.55; }
        .rg-layout { display:grid; grid-template-columns:minmax(0, 1.7fr) minmax(0, 1fr); gap:1.25rem; }
        .rg-panel { background:#fff; border:1px solid #e3e6ea; border-radius:10px; padding:1rem 1.1rem; min-width:0; }
        .rg-panel h3 { font-size:.8rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#5a6878; margin:0 0 .6rem; }
        #rg-map svg { display:block; width:100%; height:auto; }
        #rg-map path.c { stroke:#fff; stroke-width:.4; cursor:pointer; }
        #rg-map path.c:hover, #rg-map path.c.sel { stroke:#1a1d33; stroke-width:1.2; }
        .rg-legend { display:flex; align-items:center; gap:.5rem; font-size:.75rem; color:#5a6878; margin-top:.4rem; flex-wrap:wrap; }
        .rg-legend .bar { height:10px; width:160px; border-radius:3px; }
        .rg-tip { font-size:.88rem; margin-top:.5rem; min-height:2.6em; color:#1a1d33; }
        .rg-rank { list-style:none; margin:0; padding:0; font-size:.85rem; }
        .rg-rank li { display:grid; grid-template-columns:1.6rem minmax(0, 8rem) 1fr 3.4rem; gap:.4rem; align-items:center; padding:.18rem 0; cursor:pointer; }
        .rg-rank li:hover { background:#f3f5f8; }
        .rg-rank .n { color:#8fa0b0; font-size:.75rem; text-align:right; }
        .rg-rank .nm { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
        .rg-rank .b { height:9px; border-radius:2px; }
        .rg-rank .v { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }
        .rg-lower { display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1.25rem; margin-top:1.25rem; }
        .rg-lower svg { display:block; width:100%; height:auto; }
        .rg-funders { font-size:.85rem; margin:0; padding-left:1.1rem; }
        .rg-funders li { margin:.15rem 0; }
        @media (max-width:820px) { .rg-layout { grid-template-columns:1fr; } }
"""
i = s.index("        /* Field Trends */")
s = s[:i] + CSS + s[i:]

SECTION = """<!-- ── Around the World ── -->
<section class="section bg-light" id="field-regions">
    <div class="section-inner">
        <p class="section-label eyebrow">Around the World</p>
        <h2 class="section-title">Who Is Researching What</h2>
        <p class="section-subtitle">Research and investment in each of our fields, country by country, from OpenAlex: an open index of scholarly work in every language. Specialization shows how strongly a country focuses on a field compared with its research overall, so smaller and non-Western countries that lead a field stand out, not only the largest producers.</p>
        <div class="rg-controls">
            <label>Field <select id="rg-field"></select></label>
            <label>Year <select id="rg-year"></select></label>
            <label>Measure <span class="rg-seg" id="rg-metric">
                <button data-m="share" class="on">Share of papers</button><button data-m="spec">Specialization</button><button data-m="fund">Funding</button>
            </span></label>
        </div>
        <div class="rg-insight" id="rg-insight">Loading the world data&hellip;</div>
        <div class="rg-layout">
            <div class="rg-panel"><h3 id="rg-map-title">Map</h3><div id="rg-map" role="img" aria-label="World map of the selected measure"></div>
                <div class="rg-legend" id="rg-legend"></div><div class="rg-tip" id="rg-tip">Select a country on the map or in the list.</div></div>
            <div class="rg-panel"><h3 id="rg-rank-title">Leading countries</h3><ol class="rg-rank" id="rg-rank"></ol></div>
        </div>
        <div class="rg-lower">
            <div class="rg-panel"><h3>Share of the world&rsquo;s papers over time</h3><div id="rg-lines"></div></div>
            <div class="rg-panel"><h3 id="rg-cont-title">By continent</h3><div id="rg-cont"></div></div>
            <div class="rg-panel"><h3 id="rg-fund-title">Funders acknowledged most</h3><ol class="rg-funders" id="rg-funders"></ol></div>
        </div>
        <p class="ft-notes" id="rg-notes"></p>
    </div>
</section>

"""
anchor = "<!-- ── Featured Story ── -->"
assert s.count(anchor) == 1
s = s.replace(anchor, SECTION + anchor)

JS = r"""<script>
/* Around the World: field-regions.json from tools/field_regions.py (OpenAlex). d3 and the map load when the section is near. */
(function () {
  const sec = document.getElementById('field-regions'); if (!sec) return;
  const load = src => new Promise((ok, no) => { const e = document.createElement('script'); e.src = src; e.onload = ok; e.onerror = no; document.head.appendChild(e); });
  let started = false;
  const go = () => { if (started) return; started = true;
    Promise.all([load('https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js').then(() => load('https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js')),
                 fetch('field-regions.json').then(r => r.json()),
                 fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then(r => r.json())])
      .then(([, D, world]) => init(D, world))
      .catch(() => { document.getElementById('rg-insight').textContent = 'The world data could not be loaded.'; }); };
  if ('IntersectionObserver' in window) new IntersectionObserver((es, o) => { if (es.some(e => e.isIntersecting)) { o.disconnect(); go(); } }, { rootMargin: '600px' }).observe(sec); else go();

  function init(D, world) {
    const $ = id => document.getElementById(id);
    const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const MIN = 30;                                         // fewer papers than this: too few to rank on specialization
    const NAME = D.countries, NUM = D.iso_numeric, A2 = Object.fromEntries(Object.entries(NUM).map(([a, n]) => [String(+n), a]));
    const years = D.years.map(String), fundYears = years.filter(y => D.fields[0].years[y].funded_by_country);
    let F = D.fields[0], Y = years[years.length - 1], M = 'share', SEL = null;
    $('rg-field').innerHTML = D.fields.map((f, i) => `<option value="${i}">${esc(f.label)}</option>`).join('');
    const setYears = () => { const ys = M === 'fund' ? fundYears : years; if (!ys.includes(Y)) Y = ys[ys.length - 1];
      $('rg-year').innerHTML = ys.map(y => `<option${y === Y ? ' selected' : ''}>${y}</option>`).join(''); };
    function stats(f, y) {
      const fy = f.years[y], w = D.world[y], out = {};
      for (const [c, n] of Object.entries(fy.countries)) {
        const share = n / fy.known, ws = (w.countries[c] || 0) / w.known;
        out[c] = { n, share, spec: ws ? share / ws : null };
      }
      const fb = fy.funded_by_country || {}, ft = Object.values(fb).reduce((a, b) => a + b, 0);
      for (const [c, n] of Object.entries(fb)) { out[c] = out[c] || { n: 0, share: 0, spec: null }; out[c].fund = n / ft; out[c].fundN = n; }
      return out;
    }
    const val = (s, c) => { const r = s[c]; if (!r) return null;
      if (M === 'share') return r.share; if (M === 'fund') return r.fund ?? null; return r.n >= MIN ? r.spec : null; };
    const fmt = v => v == null ? 'n/a' : M === 'spec' ? v.toFixed(2) + '×' : (v * 100).toFixed(v < .01 ? 2 : 1) + '%';
    const colorFor = () => {
      if (M === 'spec') return d3.scaleDiverging([0.25, 1, 4], t => d3.interpolateRgbBasis(['#b26a00', '#f3efe6', '#005ba5'])(t)).clamp(true).unknown('#e3e6ea');
      return d3.scaleSqrt([0, 0.25], ['#eef2f6', M === 'fund' ? '#2e7d32' : '#005ba5']).clamp(true);
    };
    const feats = topojson.feature(world, world.objects.countries).features.filter(f => f.id !== '010');
    const W = 800, H = 400, proj = d3.geoNaturalEarth1().fitSize([W, H], { type: 'FeatureCollection', features: feats }), path = d3.geoPath(proj);
    const svg = d3.select('#rg-map').append('svg').attr('viewBox', `0 0 ${W} ${H}`);
    const paths = svg.selectAll('path').data(feats).join('path').attr('class', 'c').attr('d', path)
      .on('click', (e, f) => pick(A2[String(+f.id)])).on('mousemove', (e, f) => tip(A2[String(+f.id)]));
    function tip(c) {
      if (!c) return; const s = stats(F, Y), r = s[c] || {};
      $('rg-tip').innerHTML = `<strong>${esc(NAME[c] || c)}</strong>, ${Y}: ${(r.n || 0).toLocaleString()} papers, ${((r.share || 0) * 100).toFixed(1)}% of the world&rsquo;s` +
        (r.spec != null && r.n >= MIN ? `, specialization ${r.spec.toFixed(2)}×` : r.n ? ' (too few papers to rate specialization)' : '') +
        (r.fund != null ? `, ${(r.fund * 100).toFixed(1)}% of funding acknowledgments` : '');
    }
    function pick(c) { if (!c) return; SEL = c; tip(c); draw(); }
    function insight(s) {
      const f = F, y0 = years[0], s0 = stats(f, y0);
      const lead = Object.entries(s).sort((a, b) => b[1].share - a[1].share)[0];
      const gains = Object.keys(s).filter(c => s[c].n >= 30 && s0[c]).map(c => [c, s[c].share - s0[c].share]).sort((a, b) => b[1] - a[1]);
      const spec = Object.entries(s).filter(([, r]) => r.n >= 30 && r.spec).sort((a, b) => b[1].spec - a[1].spec).slice(0, 3);
      const fy = fundYears[fundYears.length - 1], fs = stats(f, fy), topF = Object.entries(fs).filter(([, r]) => r.fund).sort((a, b) => b[1].fund - a[1].fund).slice(0, 2);
      const p = c => esc(NAME[c] || c);
      return `In ${Y}, <strong>${p(lead[0])}</strong> wrote the most ${esc(f.label.toLowerCase())} papers (${(lead[1].share * 100).toFixed(1)}% of the world&rsquo;s). ` +
        (gains.length ? `Since ${y0} the largest gain in share is <strong>${p(gains[0][0])}</strong> (${gains[0][1] >= 0 ? '+' : ''}${(gains[0][1] * 100).toFixed(1)} points). ` : '') +
        (spec.length ? `Most specialized: ${spec.map(([c, r]) => `<strong>${p(c)}</strong> (${r.spec.toFixed(1)}×)`).join(', ')}. ` : '') +
        (topF.length ? `Funding acknowledged in ${fy}: ${topF.map(([c, r]) => `${p(c)} ${(r.fund * 100).toFixed(0)}%`).join(', ')}.` : '');
    }
    function draw() {
      setYears();
      const s = stats(F, Y), col = colorFor();
      paths.attr('fill', f => { const c = A2[String(+f.id)], v = c ? val(s, c) : null; return v == null ? '#e3e6ea' : col(v); })
           .classed('sel', f => A2[String(+f.id)] === SEL);
      const label = { share: 'Share of the world’s papers', spec: 'Specialization (1× = world average)', fund: 'Share of funding acknowledgments, by funder country' }[M];
      $('rg-map-title').textContent = `${label}, ${Y}`;
      $('rg-legend').innerHTML = M === 'spec'
        ? `<span>0.25×</span><span class="bar" style="background:linear-gradient(90deg,#b26a00,#f3efe6,#005ba5)"></span><span>4×</span><span>&middot; gray: fewer than ${MIN} papers</span>`
        : `<span>0%</span><span class="bar" style="background:linear-gradient(90deg,#eef2f6,${M === 'fund' ? '#2e7d32' : '#005ba5'})"></span><span>25%+</span>`;
      const rows = Object.keys(s).map(c => [c, val(s, c)]).filter(r => r[1] != null).sort((a, b) => b[1] - a[1]).slice(0, 15);
      const mx = Math.max(...rows.map(r => r[1]), 1e-9);
      $('rg-rank-title').textContent = M === 'spec' ? `Most specialized, ${Y}` : `Leading countries, ${Y}`;
      $('rg-rank').innerHTML = rows.map(([c, v], i) => `<li data-c="${c}"${c === SEL ? ' style="background:#eef2f6"' : ''}><span class="n">${i + 1}</span><span class="nm">${esc(NAME[c] || c)}</span>` +
        `<span class="b" style="width:${Math.max(v / mx * 100, 2)}%;background:${M === 'spec' ? col(v) : M === 'fund' ? '#2e7d32' : '#005ba5'}"></span><span class="v">${fmt(v)}</span></li>`).join('');
      $('rg-insight').innerHTML = insight(s);
      lines(); continents(); funders();
    }
    function lines() {
      const s = stats(F, years[years.length - 1]);
      let top = Object.entries(s).sort((a, b) => b[1].share - a[1].share).slice(0, 6).map(r => r[0]);
      if (SEL && !top.includes(SEL)) top = top.slice(0, 5).concat(SEL);
      const series = top.map(c => years.map(y => (F.years[y].countries[c] || 0) / F.years[y].known));
      const W = 420, H = 230, m = { l: 40, r: 104, t: 8, b: 22 }, x = d3.scalePoint(years, [m.l, W - m.r]), y = d3.scaleLinear([0, d3.max(series.flat()) * 1.08], [H - m.b, m.t]);
      const pal = ['#005ba5', '#c62828', '#2e7d32', '#7a5000', '#5a6878', '#8B0000'];
      const el = d3.select('#rg-lines').html('').append('svg').attr('viewBox', `0 0 ${W} ${H}`);
      el.append('g').attr('transform', `translate(0,${H - m.b})`).call(d3.axisBottom(x).tickValues(years.filter((_, i) => i % 2 === 0))).attr('font-size', 12);
      el.append('g').attr('transform', `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(4).tickFormat(d3.format('.0%'))).attr('font-size', 12);
      const ly = series.map((v, i) => [i, y(v[v.length - 1]) + 4]).sort((p, q) => p[1] - q[1]);   // keep end labels 12px apart
      for (let k = 1; k < ly.length; k++) ly[k][1] = Math.max(ly[k][1], ly[k - 1][1] + 14);
      const labelY = Object.fromEntries(ly);
      series.forEach((v, i) => {
        const c = top[i], w = c === SEL ? 3.5 : 2;
        el.append('path').attr('d', d3.line((d, j) => x(years[j]), d => y(d))(v)).attr('fill', 'none').attr('stroke', pal[i % 6]).attr('stroke-width', w);
        el.append('text').attr('x', W - m.r + 4).attr('y', labelY[i]).attr('font-size', 13).attr('font-weight', c === SEL ? 700 : 500).attr('fill', pal[i % 6]).text(NAME[c] || c);
      });
    }
    function continents() {
      const y0 = years[0], cs = ['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania'];
      const sh = y => { const c = F.years[y].continents, t = cs.reduce((a, k) => a + (c[k] || 0), 0) || 1; return cs.map(k => (c[k] || 0) / t); };
      const a = sh(y0), b = sh(Y), W = 420, H = 230, m = { l: 112, r: 40, t: 6, b: 6 }, bh = (H - m.t - m.b) / cs.length;
      const x = d3.scaleLinear([0, Math.max(...a, ...b)], [m.l, W - m.r]);
      $('rg-cont-title').textContent = `By continent, ${y0} and ${Y}`;
      const el = d3.select('#rg-cont').html('').append('svg').attr('viewBox', `0 0 ${W} ${H}`);
      cs.forEach((k, i) => {
        const yy = m.t + i * bh;
        el.append('text').attr('x', m.l - 6).attr('y', yy + bh / 2 + 4).attr('text-anchor', 'end').attr('font-size', 13).attr('fill', '#2d4053').text(k);
        el.append('rect').attr('x', m.l).attr('y', yy + 3).attr('height', bh / 2 - 4).attr('width', x(a[i]) - m.l).attr('fill', '#8fa0b0');
        el.append('rect').attr('x', m.l).attr('y', yy + bh / 2).attr('height', bh / 2 - 4).attr('width', x(b[i]) - m.l).attr('fill', '#005ba5');
        el.append('text').attr('x', x(b[i]) + 4).attr('y', yy + bh - 6).attr('font-size', 12).attr('fill', '#1a1d33').text((b[i] * 100).toFixed(0) + '%');
      });
      el.append('text').attr('x', W - 4).attr('y', H - 4).attr('text-anchor', 'end').attr('font-size', 9).attr('fill', '#5a6878').text(`gray ${y0} · blue ${Y}`);
    }
    function funders() {
      const fy = fundYears.includes(Y) ? Y : fundYears[fundYears.length - 1];
      $('rg-fund-title').textContent = `Funders acknowledged most, ${fy}`;
      $('rg-funders').innerHTML = (F.years[fy].top_funders || []).map(([nm, c, n]) => `<li>${esc(nm)}${c ? ` <span style="color:#8fa0b0">(${esc(NAME[c] || c)})</span>` : ''}: ${n.toLocaleString()} papers</li>`).join('');
    }
    $('rg-field').addEventListener('change', e => { F = D.fields[+e.target.value]; draw(); });
    $('rg-year').addEventListener('change', e => { Y = e.target.value; draw(); });
    $('rg-rank').addEventListener('click', e => { const li = e.target.closest('li'); if (li) pick(li.dataset.c); });
    $('rg-metric').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; M = b.dataset.m;
      $('rg-metric').querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); draw(); });
    $('rg-notes').textContent = `Updated ${D.updated}. ${D.notes}`;
    draw();
  }
})();
</script>
"""
i = s.index("<script>\n/* Field Trends:")
s = s[:i] + JS + s[i:]
open(P, "w", encoding="utf-8").write(s)
print("media.html: Around the World section added")
