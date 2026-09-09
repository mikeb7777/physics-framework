# gallery/

Images for `gallery.html`. Drop files here, then add an entry to
`gallery-data.json` in the repo root. Nothing else needs editing.

## Reels

One still per Instagram post. The card links out and opens the post in a new tab.

- **Aspect ratio:** cards are 4:5 portrait. Your carousel panels are already
  1080x1350, so they drop in without cropping. A 9:16 reel still will be
  centre-cropped top and bottom, so keep the subject away from the edges.
- **Size:** about 800x1000 is plenty. Cards render around 240 to 320px wide.
- **Format:** JPEG, aim for under 150 KB each.
- **Naming:** `reel-01.jpg`, `reel-02.jpg`, and so on, so the order is obvious.

## Talks, projects, and people

Same folder, same card shape. `url` is optional here: leave it out and the card
is not a link.

Name these for what they are rather than by number, for example
`talk-bangkok-2026.jpg`, so the list stays readable as it grows.

## Adding an entry

Paste into the matching list in `gallery-data.json`:

```json
{
  "url": "https://www.instagram.com/p/XXXXXXXXXXX/",
  "thumb": "gallery/reel-01.jpg",
  "title": "The First Distinction",
  "caption": "Element 01, the framework series",
  "alt": "Panel reading The First Distinction over a starfield"
}
```

`title`, `caption` and `alt` are all optional. `alt` falls back to `title`, so
give at least one of them for screen readers.

Order in the file is the order on the page. An empty list shows that section's
"nothing here yet" message instead, so the page is always safe to publish.
