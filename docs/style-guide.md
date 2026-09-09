# Ic² Research Institute: Website Style Guide

**Version 1.2** · 9 September 2026
**Governs:** eequalsicsquared.com, the static site served from this repository
**Changed in this revision:** the contraction rule now allows them where the
full form reads stiffly, and names the three places they are still expanded.

> ### No silent amendments
>
> This guide follows the same convention as the book. Every change bumps the
> version, says what changed in the header above, and adds a row to the revision
> history at the end. Nothing is altered without a record.
>
> **If a rule here contradicts the site, do not assume the guide is right.**
> The two have drifted twice already: the em dash rule was written more
> absolutely than intended, and the pair table said six when it listed nine.
> Check the revision history and the git log for this file, then fix whichever
> is actually wrong and record it.
>
> This document is the single source of truth. Any copy outside this repository
> is stale.

---

## 1. Typography

**Em dashes** — Legitimate when used sparingly and doing work no other mark can
do: a sharp reversal, or a genuine interruption of the sentence. `That uncertainty
is not a failure—it is an invitation.`

What is not legitimate is the em dash as a default connector, standing in for
punctuation that already exists for the job. This is the failure mode to watch
for, because drafting tools reach for it constantly and a page can end up with an
em dash in almost every paragraph. When the dash is replacing one of these, use
the real mark instead:

| Doing the work of | Use |
|---|---|
| Parentheses, around an aside | Parentheses, or a pair of commas |
| A comma, around an appositive | Commas: `the sequence, forced arithmetic, produces` |
| A colon, before an elaboration | Colon: `properties: not by luck` |
| A semicolon, between contrasting clauses | Semicolon: `works; it is` |
| A connecting word (`and`, `but`, `because`, `so`) | The connecting word, or a new sentence |

Two practical tests. If the sentence reads the same with a comma or a colon, it
wanted a comma or a colon. If a page has more than two or three em dashes, they
have stopped being emphasis and become a tic.

Paired dashes around a phrase that itself contains a list are a special case: do
not convert them to commas, because the list and its frame blur together. Recast
the sentence instead.

This rule governs prose. Em dashes remain fine as label separators in headings,
tables, timelines, and reference lines, including in this document.

**Contractions** — Allowed where avoiding one makes the sentence stilted. The
test is whether the full form is doing work or just sounding stiff: *"it is not a
metaphor"* earns the expansion, *"that is not what is happening"* does not, and
reads better as *"that's not what's happening"*.

Expand them in three places, where the precision is the point:

| Where | Why |
|---|---|
| A stated prediction | It goes on the record and gets quoted back |
| A falsification standard | The condition has to be unambiguous |
| A claim about what the evidence shows | The register should be flatter than the surrounding prose |

Everywhere else, including blog posts, reels, captions and calls to action, use
whichever reads naturally aloud. A page with no contractions anywhere sounds
translated, which costs more credibility than the formality buys.

**Paragraph text** — `font-size: 1.125rem; line-height: 1.8; color: var(--text-dark)` on light backgrounds. `color: rgba(255,255,255,0.88)` on dark.

**Section titles** — `.section-title` class. White (`color: white`) on dark section backgrounds; default (`var(--text-dark)`) on white/light.

**Uppercase labels** — `font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700` — used sparingly for attribution lines and category tags only.

---

## 2. Color System

### CSS Variables
```css
--primary-color: #8B0000    /* dark red */
--accent-blue:   #005ba5
--accent-red:    #e33d2f
--accent-green:  #a1cd5f
--accent-orange: #f58b2b
--accent-yellow: #f1e303
--text-dark:     #2c3e50
--text-light:    #666
--bg-light:      #f8f9fa
--max-width:     1200px
```

### QCD Meson Color System (Easter Egg)
Nine combinations only — each is a quark color paired with its specific antiquark. Never mix across pairs.

| Name | Primary (quark) | Accent/stroke (antiquark) | Usage |
|---|---|---|---|
| **R+Cy** | `#8B0000` dark red | `#00838f` cyan | Information accordion, Pre-Registration card, deep instances |
| **R+Cy bright** | `#c62828` scarlet | `#00bcd4` bright cyan | Time accordion, tonal variation |
| **G+Mg** | `#1a5c2a` forest green | `#b01558` rose | Computation accordion, Falsifiability card |
| **G+Mg bright** | `#2e7d32` mid-green | `#e91e63` vivid magenta | Dimensionality accordion, tonal variation |
| **B+Yw** | `#005ba5` navy blue | `#f1e303` yellow | Consciousness accordion, Multi-Domain card |
| **Cy+R** | `#005f6e` dark teal | `#c62828` red | Relational accordion, Independent card |
| **Cy+R bright** | `#00838f` teal | `#e53935` vivid red | Arrow of Time accordion, tonal variation |
| **Mg+G** | `#8e0c45` dark rose | `#1a7a36` green | Consciousness (universe) accordion, Open Data card |
| **Yw+B** | `#7a5000` dark amber | `#1565c0` blue | Measurement accordion, Statistical card |

**Rule:** Each accordion's Core Claim box uses the flipped pair of its header (so Information R+Cy header → Cy+R core claim).

**Do not create new color combinations.** All cards, accordions, and callout boxes must use one of the nine entries above.

> **Resolved 2026-09-09, Mg+G.** The pages had been rendering the antiquark as
> `#2e7d32`, which is also G+Mg bright's quark color, so two of the nine pairs
> had collapsed onto the same green. Settled in favor of this table: the accent
> is `#1a7a36`, corrected in twelve places across seven files. If you find
> `#8e0c45` paired with `#2e7d32` anywhere, it is a regression.

### Adjacent Color Rule
Two same or near-identical colors must not sit directly against each other without reason. Use complementary or clearly contrasting pairs. Established working pairs:
- Beige/cream on red
- Blue with gunmetal
- Orange adjacent to red
- Green with gold/yellow
- Cyan with red

### Specific Named Colors
- **Gunmetal:** `#5a6878` — core mid-tone. Section separator gradient: `linear-gradient(135deg, #8fa0b0 0%, #5a6878 100%)`
- **Dark navy (header/footer/CTA):** `#0d0d1f`
- **Validation banner / dark section:** `linear-gradient(135deg, #2c3e50 0%, #34495e 100%)`
- **Pull quote dark:** `#0a0f1e`
- **Void gradient (timeline card):** `radial-gradient(ellipse at 60% 15%, #4a5e7a 0%, #354866 40%, #243252 70%, #18243e 100%)`

---

## 3. Section Backgrounds

| Section type | Background |
|---|---|
| White content section | `background: white` (explicit) |
| Light content section | `class="content-section bg-light"` |
| Dark header/CTA | `#0d0d1f` |
| Validation/callout banner | `linear-gradient(135deg, #2c3e50 0%, #34495e 100%)` |
| Open Science / gunmetal | `linear-gradient(135deg, #5a6878 0%, #4a5868 100%)` |
| Pull quote | `#0a0f1e` |

---

## 4. Card Components

### Solid Color Card (intro-card)
Used in: Investment section, overview, Research Opportunity.
```html
<div class="intro-card" style="background: [quark-color]; box-shadow: 0 4px 20px rgba(...); border-bottom: 4px solid [antiquark-color];">
    <h3>Title</h3>
    <p>White text, rgba(255,255,255,0.85), 0.92rem, line-height 1.7.</p>
</div>
```
Grid: `class="intro-cards-grid"` — `repeat(auto-fit, minmax(260px, 1fr))`, gap 1.5rem.

### Split Header+Body Card (methodology cards)
Used in: Open Science section, Note on Coverage.
```html
<div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 18px rgba(0,0,0,0.18);">
    <div style="background: [quark]; padding: 0.75rem 1.25rem; display: flex; align-items: center; gap: 0.6rem;">
        <span class="material-symbols-outlined" style="font-size: 1.15rem; color: [antiquark];">icon_name</span>
        <h3 style="color: white; font-size: 0.95rem; font-weight: 700; margin: 0;">Title</h3>
    </div>
    <div style="background: white; padding: 1.25rem 1.5rem;">
        <p style="color: [quark]; font-size: 0.92rem; line-height: 1.75; margin: 0;">Body text in quark color.</p>
    </div>
</div>
```

### Origin Sequence Card (red header + body)
```html
<div style="border-radius: 8px; overflow: hidden;">
    <div style="background: #8B0000; padding: 0.875rem 1.75rem;">
        <h3 style="color: white; font-size: 1.15rem; font-weight: 700; margin: 0;">Card Title</h3>
    </div>
    <div class="timeline-section" style="background: [color]; border-radius: 0 0 8px 8px;">
        ...content...
    </div>
</div>
```

### Foundation Accordion
Uses CSS custom property `--acc-color` on the wrapper div for the header background. Toggle indicator and h3 title inherit white from CSS. Core Claim box styled inline.

**Accordion header CSS:**
```css
.foundation-accordion { --acc-color: #4a5568; /* default */ }
.foundation-header { background: var(--acc-color); }
.foundation-header h3 { color: white; }
.toggle-indicator { color: rgba(255,255,255,0.75); }
.foundation-header:hover { filter: brightness(1.1); }
```

**Internal callout boxes** — use tinted background matching the accordion's QCD pair, not pure white:
- R+Cy accordion boxes: `background: #e0f7fa; border-left: 4px solid #00838f;`
- G+Mg accordion boxes: `background: #fce4ec; border-left: 4px solid #b01558;`
- B+Yw accordion boxes: `background: #fff9c4; border-left: 4px solid #f1e303;`
- Cy+R accordion boxes: `background: #fce4ec; border-left: 4px solid #c62828;`
- Mg+G accordion boxes: `background: #fce4ec; border-left: 4px solid #2e7d32;`

---

## 5. Buttons

```css
/* Primary — dark red, white text */
.btn.btn-primary { background: var(--primary-color); color: white; }

/* Outline — transparent, white border (dark backgrounds only) */
.btn.btn-outline { background: transparent; color: white; border: 2px solid white; }
.btn.btn-outline:hover { background: white; color: var(--text-dark); }

/* Login pill (nav only) */
.login-link { background: dark red gradient; color: yellow; border-radius: 25px; }
```

---

## 6. Icons

**Icon set:** Google Material Symbols (web font, single CDN link).  
**Usage:** `<span class="material-symbols-outlined">icon_name</span>`  
**No PNG icons** — all PNG icon files in project are deprecated. Use Material Symbols exclusively.  
**Color:** Inherit from parent, or set explicitly via `style="color: [antiquark-color];"` in headers.

Established icon assignments:
- `database` — Information / substrate
- `hub` — Relational / connected
- `cycle` — Computation / process  
- `psychology` — Consciousness (SR)
- `bolt` — Information is Physical
- `functions` — Mathematical structures
- `self_improvement` — Consciousness (universe)
- `trip_origin` — Black holes
- `crisis_alert` — Singularity
- `trending_up` — Arrow of Time
- `analytics` — Measurement
- `schedule` — Time
- `grid_on` — Dimensionality
- `blur_on` — Consciousness types
- `verified` — Validation / confirmed
- `science` — Generic science fallback
- `event_available` — Pre-registration
- `check_circle` — Falsifiability
- `group` — Independent validation
- `cloud_download` — Open data
- `stacks` — Statistical rigor
- `info` — Note / coverage

---

## 7. Navigation

**Desktop nav:** Logo left, links center, Login pill right, hamburger hidden.  
**Mobile nav:** Hamburger toggles full-width dropdown.  
**Active state:** `color: var(--primary-color)` on current page link.  
**Login pill:** Dark red gradient, yellow text, 25px border-radius.

---

## 8. Specific Components

### Page Header (framework.html)
- Background: SVG nebula on `#0d0d1f`
- White plasma cloud: `cy ≈ 125-130` in 380-unit viewBox (tracks logo position)
- COSMIC logo: 80px height, centered
- Subtitle: `1.25rem`, white, `opacity: 0.9`
- COSMIC acronym line: `1rem`, `rgba(255,255,255,0.65)`, separated by `border-top: 1px solid rgba(255,255,255,0.1)`, `margin-top: 2.5rem`

### Big TOE Logo (tilt animation)
```css
.hero-bigtoe-logo { height: 60px; transition: all 0.4s ease; }
.hero-logo-button:hover .hero-bigtoe-logo { transform: scale(1.1) rotate(2deg); filter: drop-shadow(0 8px 16px rgba(255,255,0,0.4)); }
```

### Timeline Dot Animation
- Initial: dots light up sequentially (staggered CSS `animation-delay`)
- Loop: `IntersectionObserver` at `threshold: 0.5, rootMargin: '0px 0px -60px 0px'` triggers `.tl-animate`
- After 3.2s: JS replaces animation with synchronized `smPulse`/`cfPulse` at 4s cycle
- Keyframe: hold bright 30% → dim 25% → hold dim 25% → bright 20% (pause-based, no wave)
- Down arrows: `::before` CSS triangles pointing down between each step

### Pull Quote (dark)
```html
<section style="background: #0a0f1e; padding: 2.5rem 2rem;">
    <div style="max-width: 780px; margin: 0 auto; text-align: center;">
        <div style="width: 60px; height: 3px; background: #f1e303; margin: 0 auto 2rem;"></div>
        <p style="font-size: 1.25rem; line-height: 1.75; color: rgba(255,255,255,0.88); font-style: italic;">Quote text.</p>
        <div style="width: 60px; height: 3px; background: #f1e303; margin: 2rem auto 0;"></div>
    </div>
</section>
```
The pull quote section touches the section above it (no whitespace gap — section above has `padding-bottom: 0`).

### Section Title Formatting
Element titles: `Element N: Title` (colon, not dash).  
No "Looking Forward" section headings — use genuine conceptual bridge passages.  
Lists converted to flowing prose where items require connective language.

### Note on Coverage Card
Appears once only — at the end of Framework Foundations, after the last accordion.
Uses split header+body with R+Cy: red header, cyan `info` icon, white body, red text.

---

## 9. Content Rules

- **No "coming soon"** — all sections must have real book content or be omitted
- **References** format: `Element N, A Quest for the Big TOE` — inline, at end of accordion body
- **Book attribution label:** `font-size: 0.7rem; uppercase; letter-spacing: 2px; color: rgba(255,255,255,0.35)`
- **Contractions** — see Typography. Allowed where the full form reads stiffly; expanded in predictions, falsification standards, and claims about evidence
- **Section heading "Looking Forward"** — forbidden; write a proper conceptual bridge
- Equations removed from main text (accessible only in appendix)

---

## 10. File Structure

```
eequalsicsquared.com (GitHub Pages)
├── index.html          ✓ complete
├── framework.html      ✓ complete (current session)
├── validation.html     pending
├── testing-schedule.html  pending
├── blog.html           stub
├── contribute.html     stub
├── references.html     stub
└── appendix.html       stub
```

**Working copies:** `/home/claude/` (container, resets between sessions)  
**Outputs:** `/mnt/user-data/outputs/`  
**Project files (read-only):** `/mnt/project/`  
**Recovery pattern:** When build script is lost, use `python-docx` to read/modify existing `.docx` directly.

---

## 11. Pending Work (resuming next chat)

- [ ] validation.html — build out
- [ ] testing-schedule.html — build out
- [ ] Remaining framework.html sections review (if any)
- [ ] Upload revised files to GitHub Pages
- [ ] Blog and video channel development
- [ ] index.html — check for any remaining issues

---

## Revision history

Newest first. Add a row here in the same commit that changes a rule.

| Version | Date | Change |
|---|---|---|
| 1.2 | 2026-09-09 | Contractions no longer banned in body text. They are allowed wherever the full form reads stiffly, and expanded only in stated predictions, falsification standards, and claims about what the evidence shows, where the phrasing gets quoted back. The previous absolute wording was producing prose that read as translated. Stated twice in the guide, in Typography and in Content Rules; both updated, and Content Rules now points at Typography rather than restating it. |
| 1.1 | 2026-09-09 | Brought under version control and into the repository. Em dash rule rewritten to target the misuse, an em dash standing in for parentheses, a comma, a colon, a semicolon or a connecting word, rather than banning the mark outright; the previous wording had produced a scorched-earth pass over the blog. Pair table heading corrected from "Six combinations only" to nine, which is what it lists and what the rule below it already said. Mg+G resolved in favor of this table: the antiquark is `#1a7a36`, not the `#2e7d32` the pages had drifted to, which duplicated G+Mg bright’s quark. Corrected in twelve places. Spelling normalized to US English. |
| 1.0 | before 2026-09-09 | Original guide, unversioned, kept outside the repository. Header recorded only "Last updated: Session ending framework.html v1". |

### How to amend

1. Change the rule.
2. Bump the version at the top: a rule change is a minor bump, a rewrite of a
   whole section is a major one.
3. Rewrite **Changed in this revision** in the header to describe only this
   revision.
4. Add a row above, with enough detail that someone can tell why the change was
   made without reading the diff.
5. Commit the guide together with any site changes the new rule required, so the
   history shows the rule and its consequences arriving as one change.

### Related documents

`StyleGuide_Amendment_v1.4.md` is a separate document with its own numbering. It
governs the writing philosophy for *A Quest for the Big TOE*, not this site, and
is filed with the book revision instructions. Do not merge the two version
sequences.
