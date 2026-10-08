# -*- coding: utf-8 -*-
"""Horizon Scanner, Living Review (2 Oct 2026). Michael: the paper cards should sit on a
QCD color-anticolor pair instead of white, one pair rather than all the QCD colors.
Pair B+Yw from the style guide's nine (docs/style-guide.md): quark #005ba5 as the card,
antiquark #f1e303 as the edge and accents; white text. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "media.html")
s = open(P, encoding="utf-8").read()
a = s[s.index("        .fw-item { background:#fff;"):s.index("        .fw-more { margin-top:1.5rem; }")]
b = """        /* Paper cards: QCD pair B+Yw (quark #005ba5, antiquark #f1e303) */
        .fw-item { background:#005ba5; color:#fff; border:0; border-left:5px solid #f1e303; border-radius:10px; padding:1rem 1.25rem; }
        .fw-item.reviewed { box-shadow:inset 0 0 0 2px #f1e303; }
        .fw-top { display:flex; flex-wrap:wrap; gap:.4rem .75rem; align-items:center; font-size:.8rem; color:rgba(255,255,255,.82); margin-bottom:.35rem; }
        .fw-title { display:block; font-weight:700; font-size:1.02rem; line-height:1.35; color:#fff; text-decoration:none; }
        .fw-title:hover { color:#f1e303; text-decoration:underline; }
        .fw-authors { font-size:.85rem; color:rgba(255,255,255,.85); margin:.25rem 0 .4rem; }
        .fw-tags { display:flex; flex-wrap:wrap; gap:.4rem; }
        .fw-tag { font-size:.75rem; font-weight:600; padding:.15rem .6rem; border-radius:20px; background:rgba(255,255,255,.14); color:#fff; text-decoration:none; }
        a.fw-tag { color:#f1e303; box-shadow:inset 0 0 0 1px rgba(241,227,3,.55); background:transparent; }
        a.fw-tag:hover { background:#f1e303; color:#1a1d33; }
        .fw-rel { font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; padding:.15rem .6rem; border-radius:20px; background:#f1e303; color:#1a1d33; }
        .fw-unread { font-size:.72rem; font-weight:600; color:#f1e303; }
        .fw-note { font-size:.92rem; margin:.5rem 0 .2rem; color:#fff; }
        .fw-item details { margin-top:.4rem; font-size:.88rem; color:rgba(255,255,255,.9); }
        .fw-item summary { cursor:pointer; font-weight:600; color:#fff; }
        .fw-item summary:hover { color:#f1e303; }
        .fw-item summary:focus-visible, .fw-title:focus-visible, a.fw-tag:focus-visible { outline:2px solid #f1e303; outline-offset:2px; }
"""
s = s.replace(a, b)
open(P, "w", encoding="utf-8").write(s)
print("media.html: Living Review cards on B+Yw")
