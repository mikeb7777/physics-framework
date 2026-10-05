# -*- coding: utf-8 -*-
"""Visualizations: brain and cosmic web, and Laniakea (Michael, 6 Oct 2026): "We don't need to recreate
that image. We need to explain that it's not an image but data. Then we can show Laniakea or an actual brain
image... The book can only display 2D images. The visualizations on the site can go farther."
- The brain card no longer shows the side-by-side picture. It explains that the finding is a comparison of
  measurements (power spectrum and network statistics), not of looks, and links the paper's own figures.
- Laniakea plays the publisher's official video (Nature, YouTube), loaded only on click from the
  privacy-enhanced domain so the page stays cookieless until a visitor chooses to play it. Run once."""
import os, re

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "visualizations.html")
s = open(P, encoding="utf-8").read()

a = s.index('<article class="viz-card" data-prov="observed">\n        <button class="viz-frame" type="button" aria-label="Enlarge: cerebellum')
b = s.index("</article>", a) + len("</article>")
BRAIN = """<article class="viz-card" data-prov="observed" id="brain-cosmic-web">
        <div class="viz-body">
          <div class="viz-tags"><span class="tag tag-observed">Observed</span><span class="tag tag-simulated">Simulated</span></div>
          <h3>The brain and the cosmic web: a comparison of data, not pictures</h3>
          <p>A famous pair of images sets a slice of human cerebellum beside a slice of a simulated cosmic web, and they look alike. The look is not the finding. Branching shapes are everywhere in nature, and resemblance alone proves nothing.</p>
          <p>What Vazza and Feletti compared were measurements. They took the <strong>power spectrum</strong> of each network, a standard cosmology tool that records how much structure there is at each scale, and a set of <strong>network statistics</strong>: how many connections each node has, how clustered the nodes are, and how the connections are spread. Fluctuations in the cerebellum network from 1 micrometer to 0.1 millimeter follow the same progression as matter in the cosmic web from 5 to 500 million light-years, and several network statistics agree closely. Their paper shows the spectra themselves.</p>
          <p>A book can only print the two pictures. Here the aim is to show the measurement: an interactive that computes a power spectrum, so you can see what is being compared, is in preparation. Element 7 of <em>A Quest for The Big TOE</em> asks what the shared statistics might mean.</p>
          <dl class="viz-meta">
            <div><dt>Paper: </dt><dd>Vazza and Feletti (2020), &ldquo;The quantitative comparison between the neuronal network and the cosmic web,&rdquo; <em>Frontiers in Physics</em> 8. <a href="https://doi.org/10.3389/fphy.2020.525731" target="_blank" rel="noopener">doi.org/10.3389/fphy.2020.525731</a> (open access, CC BY 4.0)</dd></div>
            <div><dt>Tissue: </dt><dd>Human cerebellum and cortex, light microscopy. Simulation: Vazza et al. (2019), <em>Astronomy &amp; Astrophysics</em>.</dd></div>
            <div><dt>In the book: </dt><dd>Figure 7-1, Element 7</dd></div>
          </dl>
        </div>
      </article>"""
s = s[:a] + BRAIN + s[b:]

a = s.index('<article class="viz-card" data-prov="observed">\n        <div class="viz-frame missing" data-missing="The Laniakea')
b = s.index("</article>", a) + len("</article>")
LANIAKEA = """<article class="viz-card" data-prov="observed" id="laniakea">
        <div class="viz-video">
          <button class="viz-play" type="button" data-yt="rENyyRwxpHo" aria-label="Play the video Laniakea: Our home supercluster, by Nature, from YouTube">
            <img src="https://i.ytimg.com/vi/rENyyRwxpHo/hqdefault.jpg" alt="" loading="lazy">
            <span class="viz-play-btn" aria-hidden="true">&#9654;</span>
            <span class="viz-play-note">Plays from YouTube (Nature video)</span>
          </button>
        </div>
        <div class="viz-body">
          <div class="viz-tags"><span class="tag tag-observed">Observed</span></div>
          <h3>Laniakea, our home supercluster</h3>
          <p>Laniakea is the region of space whose galaxies, including the Milky Way, flow toward a shared gravitational basin. Its boundary was traced from the measured motions of thousands of galaxies, not their positions alone. In the video, white streamlines follow those flows, and an envelope marks where Laniakea ends and its neighbors begin.</p>
          <p>This is the real cosmic web, mapped from measurement, and it moves in three dimensions in a way a printed page cannot.</p>
          <dl class="viz-meta">
            <div><dt>Source: </dt><dd>Tully, Courtois, Hoffman and Pomar&egrave;de (2014), <em>Nature</em> 513, 71. Visualization by D. Pomar&egrave;de. Video: Nature video (official channel).</dd></div>
            <div><dt>Paper: </dt><dd><a href="https://doi.org/10.1038/nature13674" target="_blank" rel="noopener">doi.org/10.1038/nature13674</a></dd></div>
            <div><dt>Rights: </dt><dd>&copy; Springer Nature. Embedded from the publisher's channel, not reproduced.</dd></div>
          </dl>
        </div>
      </article>"""
s = s[:a] + LANIAKEA + s[b:]

CSS = """    .viz-video { position:relative; background:#0a0f1e; aspect-ratio:16/9; }
    .viz-video iframe { position:absolute; inset:0; width:100%; height:100%; border:0; }
    .viz-play { position:absolute; inset:0; width:100%; height:100%; border:0; padding:0; background:#0a0f1e; cursor:pointer; }
    .viz-play img { width:100%; height:100%; object-fit:cover; opacity:.8; display:block; }
    .viz-play-btn { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:68px; height:48px; border-radius:12px; background:#cc0000; color:#fff; font-size:22px; line-height:48px; text-align:center; }
    .viz-play-note { position:absolute; left:10px; bottom:8px; font:600 11px/1.2 'IBM Plex Sans',system-ui,sans-serif; color:#fff; background:rgba(10,15,30,.65); padding:3px 7px; border-radius:3px; }
    .viz-play:focus-visible { outline:3px solid #005ba5; outline-offset:-3px; }
"""
s = s.replace("    /* Watermark: names the Institute", CSS + "    /* Watermark: names the Institute", 1)

JS = """
  document.querySelectorAll('.viz-play').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.yt + '?autoplay=1&rel=0';
      f.title = 'Laniakea: Our home supercluster (Nature video)';
      f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });
})();
</script>"""
i = s.index("  function close() { lb.classList.remove('open'); if (last) last.focus(); }")
j = s.index("})();\n</script>", i)
s = s[:j] + JS.lstrip("\n").replace("})();\n</script>", "", 0) + s[j + len("})();\n</script>"):]
assert s.count("viz-play") >= 6 and "brain-cosmic-web-vazza-feletti.jpg" not in s
open(P, "w", encoding="utf-8").write(s)
print("ok")
