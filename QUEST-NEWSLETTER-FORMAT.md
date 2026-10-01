# The Quest Newsletter: Format

Each issue is the written companion to an episode of the Quest. It lives at
`quest-issue-N.html` and is reached from a footprint on the Quest Map
(`quest-map.html`, "The Route of a Result").

## On the map

- Each issue sits on one footprint, at the point on the trail the issue is about.
  Issue 1 is on the Independent lane between *Self-funding* and *Falsifiability
  and public deposit*; Issue 2 is between *Falsifiability and public deposit* and
  *Test against public data*.
- Each issue footprint is a `<g class="qfoot" data-issue="N" data-live="YYYY-MM-DD">`
  group near the end of the map's SVG. `data-live` is the publication date.
- **Before its date**, the next issue's footprint pulses and shows its month and
  year. Later issues look like ordinary footprints.
- **From its date**, the footprint carries the issue menu. It is invisible until
  the footprint is hovered, focused or tapped; the footprint then glows and
  dissolves, and the menu appears in its place.
- Add `?preview` to the map's URL to open every issue's menu before its date.

## The menu (the same five items in every issue)

1. **Newsletter**: view (`#newsletter`) or download (`?print=1`, which opens
   the browser's Save as PDF)
2. **What the data says** (`#data`): the figures at this point on the trail
3. **Important links** (`#links`)
4. **Options** (`#options`): what someone standing at this gate can do
5. **Sources and references** (`#sources`)

## The newsletter: the same chapters every time

These follow the "Same Chapters, Every Time" list on `quest-follow.html`:

1. Previously on the Quest: where the story stands, in a minute
2. Where we stand: each lane, and what changed on it
3. The main story: the one thing that moved the Quest since last time
4. Feature: a story from science, or a reader's contribution
5. People: the travellers (see below)
6. From readers: questions answered, corrections made
7. What we are waiting for: the next dates
8. What we learned: new entries in the running list, numbered on from the last issue

## The travellers

A small group, one or more on each lane, followed through the same gates from
issue to issue.

- **Real** travellers take part with their consent, and are tagged *Real*.
- **Composite** travellers are not real people. Each is built from the published
  figures for someone of that background on that lane, and is always tagged
  *Composite*.
- Record for each traveller: lane, who they are (age band, country, background,
  how the work is funded), the gate they have reached, what usually happens
  next, and what may be lost there.
- Every figure comes from a cited source in section 5. The travellers illustrate
  the figures; they are not where the figures come from.

## Publishing an issue

1. Fill in every "To write" box. Remove the red draft bar and the
   `<meta name="robots" content="noindex">` line.
2. Check the `data-live` date on the issue's footprint in `quest-map.html`.
3. Add the issue to "The Series So Far" on `quest-follow.html`, and to `sitemap.xml`.
4. For the next issue: copy the last issue page, change the number, date, title,
   position and content, and add its footprint group to the map.
