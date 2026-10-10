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

## Every issue opens with "In this issue"

A box at the top, before anything else:

- **The one thing**: one or two sentences a reader could stop after.
- **Three points**: what is in the issue.
- **Reading time**: worked out automatically from the length.
- **Corrections to earlier issues**: always present, even when it says "None".

Readers scan before they read. A reader who stops here should still know what
happened.

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

The main story opens with a one-sentence **Why it matters**.

**Length.** An issue comes out every two months, so it can run long, but
aim for 1,000 to 1,500 words in the newsletter itself, about a six-minute read.
*Feature* and *From readers* can be left out of an issue that has nothing for
them. The other chapters always appear, so readers know where to look.

**Writing.** Short paragraphs of two or three sentences. Each figure written
once, with its source. Links say where they go ("the Testing Schedule"), never
"click here".

## The travellers

A small group, one or more on each lane, followed through the same gates from
issue to issue.

- **Real** travellers take part with their consent, and are tagged *Real*.
- **Composite** travellers are not real people. Each is built from the published
  figures for someone of that background on that lane, and is always tagged
  *Composite · not a real person*.
- Record for each traveller: lane, who they are (age band, country, background,
  how the work is funded), the gate they have reached, what usually happens
  next, and what may be lost there.
- Every figure comes from a cited source in section 5. The travellers illustrate
  the figures; they are not where the figures come from.
- **Why the composite rules are strict.** News journalism rules composites out
  entirely: the Society of Professional Journalists' guidance is "We don't use
  pseudonyms, composite characters or fictional names". The Quest uses them only
  because no data exists on real individuals at every gate, so the disclosure
  has to be impossible to miss: the label goes on every appearance, not just the
  first. A composite keeps the same name in every issue.
- Real travellers read what is said about them before it is published, and
  can reply in the next issue.
- **Stories that touch on mental health** carry the help line under the table.
  Follow the safe-messaging guidelines for suicide and self-harm: no method
  details, and no framing that presents it as an answer.

## What the data says

Each figure is entered in a table with five columns: the figure, who it covers,
the year, the source, and **what it does not tell you**. That last column stops a
figure being read as more than it is.

## The record of each issue

Every issue ends with its own record: date published, version, a dated list of
changes, and a citation. An issue is never edited quietly after it goes out,
for the same reason a registered prediction is not. Optionally, deposit each
published PDF on Zenodo and add the DOI, so the issue carries a permanent date.
The record also holds the one call to action: reply to this issue, or subscribe.

## The email edition

`quest-email-template.html` is the email that goes out with each issue: a short
note with the one thing, three points and a single link to the full issue, as
promised on `quest-follow.html`. It follows the usual rules for email:

- One column, 600 pixels wide, styles written into each element, and no
  images needed, so it reads the same in dark mode, with images off and in a
  screen reader.
- A preheader: the line the inbox shows next to the subject.
- A plain-text version, at the bottom of the file, to send alongside it.
- **US law (CAN-SPAM) requires a working unsubscribe link and a valid postal
  address in every email.** The address is a placeholder until the Institute
  is incorporated.

## Publishing an issue

1. Fill in every "To write" box and every [bracket]. Remove the red draft bar and the
   `<meta name="robots" content="noindex">` line.
2. Check the `data-live` date on the issue's footprint in `quest-map.html`.
3. Add the issue to "The Series So Far" on `quest-follow.html`, and to `sitemap.xml`.
4. Fill in a copy of `quest-email-template.html` and send it with its plain-text version.
5. For the next issue: copy the last issue page, change the number, date, title,
   position and content, and add its footprint group to the map.
