# -*- coding: utf-8 -*-
"""The new book cover on the site (Michael, 16 Oct 2026: "make the actual book cover available for
download above the poster, with the print instructions. We should compare the price to self print +
paper and ink, as opposed to purchase a bound copy at books.by").

  contribute.html  a "Print Your Own Copy" block above the poster: the cover preview, the print-ready
                   cover PDF, print-shop instructions, and what printing at home costs
  book.html        the cover image on the book page is the new front
  shop.html        the cover PDF in "Available to download now"
  download.html    the 6D changelog gains a line for the new cover (added by hand on 16 Oct, see git)

The cost figures (sources checked 16 Oct 2026):
  paper   Business Source 20 lb letter, 2,500 sheets, $42.05 (pfstar.com)  -> $0.0168 a sheet
  ink     castleink.com 2026 guide: ink tank 1-2 cents, laser 3-6 cents, cartridge inkjet 8-15 cents a black page
  464 inside pages (the 6D PDF's 465 counted the cover) double-sided = 232 sheets = $3.90 of paper
  bound   BookSpace (books.by) 6 x 9 black and white: $1.26 + $0.016 a page = $8.68, plus $5 flat shipping
          (bookspace.com/guides/print-cost-comparison, bookspace.com/how-much-can-i-earn)
A bound copy at cost ($13.70 delivered) is cheaper than printing at home on any printer but an ink tank.
Michael: note it when bound copies are available. The note is in place as an HTML comment,
BOUND-COPY-NOTE, ready to switch on.

Run once:  python3 tools/site_cover_download_2026_10_16.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = "A%20Quest%20for%20The%20Big%20TOE%20Cover%206x9%20Print.pdf"
BOOK = "A%20Quest%20for%20The%20Big%20TOE%20Version%206D.pdf"


def edit(name, fn):
    path = os.path.join(ROOT, name)
    s = open(path, encoding="utf-8").read()
    t = fn(s)
    assert t != s, name
    open(path, "w", encoding="utf-8").write(t)
    print("edited", name)


def once(s, old, new):
    assert s.count(old) == 1, (old[:70], s.count(old))
    return s.replace(old, new)


LI = ('<li style="color:rgba(255,255,255,0.9); font-size:0.92rem; padding:0.3rem 0 0.3rem 1.2rem; position:relative; '
      'line-height:1.7;"><span style="position:absolute; left:0; color:#f1e303; font-weight:700;">&rsaquo;</span>'
      '<strong style="color:white;"> {k}:</strong> {v}</li>')
TD = 'style="padding:0.45rem 0.6rem; border-bottom:1px solid #d5dbe1; text-align:{a};"'


def row(cells, head=False):
    tag = "th" if head else "td"
    out = []
    for i, c in enumerate(cells):
        a = "left" if i == 0 else "right"
        w = ' scope="col"' if head else ""
        out.append(f'<{tag}{w} {TD.format(a=a)}>{c}</{tag}>')
    return "<tr>" + "".join(out) + "</tr>"


BLOCK = f'''
    <!-- BOOK COVER DOWNLOAD -->
    <section class="band" style="background:white; padding-left: 2rem; padding-right: 2rem;">
      <div style="max-width:860px; margin:0 auto;" data-aos="fade-up">

        <h2 style="font-size:1.75rem; font-weight:700; color:#1a1a2e; margin-bottom:0.5rem;">Print Your Own Copy</h2>
        <p style="font-size:0.85rem; font-weight:700; color:#8B0000; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:1.25rem;">Free Download: The Book Cover</p>
        <p style="font-size:1.05rem; line-height:1.85; color:#2c3e50; margin-bottom:2rem;">The book is free to read as a PDF. If you would rather hold a copy, here is the full printed cover: back, spine and front in one print-ready file. Take it to a print shop with the <a href="download.html" style="color:#8B0000; font-weight:600;">book PDF</a> and they can bind you a paperback.</p>

        <div style="display:flex; gap:2rem; align-items:flex-start; flex-wrap:wrap; margin-bottom:2rem;">
          <div style="flex-shrink:0;">
            <img src="cover/front-thumb.jpg" width="520" height="780" loading="lazy" style="display:block; width:260px; height:auto; border-radius:6px; box-shadow:0 4px 16px rgba(0,0,0,.18);" alt="The front cover of A Quest for The Big TOE: the title in large white letters on a starry night sky, beside a footprint filled with a pink and blue nebula whose big toe is a glowing gold sphere.">
            <p style="font-size:0.75rem; color:#5a6878; text-align:center; margin-top:0.4rem;">Front cover</p>
          </div>
          <div style="flex:1; min-width:200px;">
            <h3 style="margin-top:0; color:#8B0000; font-size:1.05rem;">A Quest for The Big TOE: Cover</h3>
            <p style="font-size:0.9rem; line-height:1.65; color:#2c3e50;">The full wrap for a 6&Prime; &times; 9&Prime; paperback of Version 6D, 464 pages inside.</p>
            <ul style="font-size:0.88rem; line-height:1.8; padding-left:1.2rem; color:#444; margin-bottom:1.25rem;">
              <li>Back, spine and front on one sheet, 13.30&Prime; &times; 9.25&Prime;</li>
              <li>Spine sized for 464 pages on standard 60 lb book paper</li>
              <li>300 DPI, with 1/8&Prime; bleed on every side</li>
            </ul>
            <a href="{PDF}" download style="display:inline-block; padding:0.75rem 2rem; background:#8B0000; color:white; text-decoration:none; border-radius:50px; font-weight:600; transition:all 0.3s ease;">Download Cover (PDF)</a>
            <p style="color:#2c3e50; font-size:0.9rem; margin-top:0.6rem;">Free to download and print for your own copy. No sign-up required.</p>
          </div>
        </div>

        <div style="background:#005ba5; border-left:5px solid #7a5000; border-radius:6px; padding:1.5rem 2rem; margin-bottom:2rem; box-shadow:0 3px 12px rgba(0,0,0,0.1);">
          <p style="color:white; font-weight:700; font-size:1rem; margin-bottom:1rem;">Print Shop Instructions</p>
          <ul style="list-style:none; padding:0; margin:0;">
            {LI.format(k="Two files", v="The cover PDF above and the <a href=\"" + BOOK + "\" style=\"color:#f1e303;\">book PDF</a>. The book PDF opens and closes with the cover pictures for reading on screen; ask the shop to leave out its first and last pages when printing the inside.")}
            {LI.format(k="Inside pages", v="Double-sided, black and white, 6 x 9 inches, at actual size. Ordinary 60 lb (90 gsm) book or copy paper. A few figures are in colour; they print well in grey.")}
            {LI.format(k="Cover", v="Colour, on one side of 100 lb (270 gsm) cover stock, at actual size. The sheet is 13.30 x 9.25 inches including 1/8 inch of bleed; trim to 13.05 x 9 inches. Matte or soft-touch lamination keeps the dark background clean.")}
            {LI.format(k="Binding", v="Ask for perfect binding (glued spine). The spine is sized for 464 pages on 60 lb paper; if the shop uses thicker or thinner paper, ask them to adjust the spine to match. For coil or comb binding, the spine is not needed.")}
            {LI.format(k="Where to print", v="FedEx Office, Staples, Office Depot, UPS Store, or any local print shop that binds books from PDF files.")}
          </ul>
        </div>

        <div style="border:1px solid #d5dbe1; border-radius:6px; padding:1.5rem 2rem; margin-bottom:2rem;">
          <h3 style="margin-top:0; color:#1a1a2e; font-size:1.05rem;">What printing it yourself costs</h3>
          <p style="font-size:0.92rem; line-height:1.7; color:#2c3e50;">Printed double-sided, the 464 inside pages take 232 sheets of paper, about $3.90 at $42 for 2,500 sheets. Ink or toner is the larger cost and depends on the printer. These are estimates for the inside pages only, before the cover and binding.</p>
          <div style="overflow-x:auto;">
          <table style="width:100%; border-collapse:collapse; font-size:0.9rem; color:#2c3e50;">
            <caption style="text-align:left; font-size:0.82rem; color:#5a6878; padding-bottom:0.4rem;">Home printing, 464 pages, black and white</caption>
            <thead>{row(["Printer", "Cost per page", "Paper", "Ink or toner", "Total"], head=True)}</thead>
            <tbody>
              {row(["Ink tank (refillable)", "1&ndash;2&cent;", "$3.90", "$4.64&ndash;$9.28", "<strong>about $9&ndash;$13</strong>"])}
              {row(["Laser", "3&ndash;6&cent;", "$3.90", "$14&ndash;$28", "<strong>about $18&ndash;$32</strong>"])}
              {row(["Inkjet with cartridges", "8&ndash;15&cent;", "$3.90", "$37&ndash;$70", "<strong>about $41&ndash;$74</strong>"])}
            </tbody>
          </table>
          </div>
          <p style="font-size:0.78rem; line-height:1.6; color:#5a6878; margin:0.75rem 0 0;">Paper: Business Source 20 lb letter, 2,500 sheets, $42.05 (October 2026). Cost per page: typical ranges for home printers in Castle Ink&rsquo;s 2026 buyer&rsquo;s guide.</p>
          <!-- BOUND-COPY-NOTE: switch on when bound copies can be ordered.
          <p style="font-size:0.92rem; line-height:1.7; color:#2c3e50; margin:1rem 0 0;"><strong>A bound copy may cost less.</strong> Printing and binding one paperback through our print partner costs about $8.70, and shipping $5, so a finished copy at cost comes to about $13.70, less than printing the pages at home on most printers. <a href="shop.html" style="color:#8B0000; font-weight:600;">Order a bound copy</a>.</p>
          -->
        </div>

      </div>
    </section>

'''


def contribute(s):
    return once(s, "\n    <!-- POSTER DOWNLOAD -->\n", BLOCK + "    <!-- POSTER DOWNLOAD -->\n")


edit("contribute.html", contribute)
edit("book.html", lambda s: once(s, '<img src="bookcover.png" alt="A Quest for The Big TOE Book Cover" class="book-cover">',
                                 '<img src="cover/front-700.jpg" width="700" height="1050" alt="A Quest for The Big TOE book cover: the title in white on a starry night sky, beside a footprint filled with a nebula, its big toe a glowing gold sphere" class="book-cover">'))
edit("shop.html", lambda s: once(s, '<li><a href="cosmic-framework-poster.pdf" download download>Download the framework poster</a>',
                                 f'<li><a href="{PDF}" download>Download the book cover</a>: print-ready PDF, back, spine and front, for a 6&nbsp;&times;&nbsp;9&nbsp;inch paperback</li>\n'
                                 '            <li><a href="cosmic-framework-poster.pdf" download download>Download the framework poster</a>'))
