# Social media

Instagram reels, 1080 × 1920, 30 fps. Each reel is a page (`reel.html`) that
draws every frame from a time value, so it renders the same every time.

```
python3 -m http.server 8765 &
node social/render-reel.js social/rubin-reel/reel.html social/rubin-reel/rubin-reel.mp4
node social/render-reel.js social/rubin-reel/reel.html check.mp4 --stills   # one PNG per scene
```

Needs Playwright and ffmpeg. Fonts (Anton, Inter, Source Serif 4; SIL Open Font
License) are in `fonts/`, so rendering needs no network.

Text stays clear of the top 250 px and bottom 420 px, where Instagram puts the
caption, buttons and profile name. Add music in Instagram or CapCut from their
licensed libraries.

## rubin-reel: COSMIC-007 and the Rubin Observatory (31 s)

Rebuilt from the September 2025 carousel in `rubin-carousel/source`, with the
record brought up to date:

- The Zenodo deposit of 31 July 2025 made the general claim (directional
  asymmetry beyond 100 Mpc). The direction (l, b) ≈ (210°, −20°) was first
  written on the website in May 2026, and the pass mark was tightened in
  September 2026 (more than 3σ, along that axis). The reel shows all three dates.
- The carousel's "1.65 m focal plane" was wrong: the LSST Camera's focal plane
  is about 64 cm across. Its "DP2: now" is out of date. Neither is in the reel.
- Rubin Data Release 1 is expected by the end of June 2028.

**Caption** (paste into Instagram):

> We made a prediction. The Rubin Observatory will check it.
>
> COSMIC-007: on the largest scales, beyond 100 megaparsecs, galaxies should lean toward one direction in the sky, (l, b) ≈ (210°, −20°). Every step is dated, including the ones we added later: filed on Zenodo in July 2025, direction stated in May 2026, bar raised in September 2026. Rubin's first data release, expected mid-2028, decides it. Whatever it shows, we publish it.
>
> Follow the test: eequalsicsquared.com
> Registered: doi.org/10.5281/zenodo.16639922
>
> Images: NSF–DOE Vera C. Rubin Observatory/NOIRLab/SLAC/AURA/P. Horálek (Institute of Physics in Opava); NSF–DOE Vera C. Rubin Observatory/NOIRLab/SLAC/AURA/H. Stockebrand. CC BY 4.0. Independent research; not affiliated with, or endorsed by, Rubin Observatory or NOIRLab.
>
> #RubinObservatory #LSST #cosmology #astronomy #physics #openscience

## framework-reel: the COSMIC Framework (25.5 s)

Landauer's limit as the hook, information as physical, time as changing
relationships, a registered test walking to DESI DR3 in 2027, and the Quest.
