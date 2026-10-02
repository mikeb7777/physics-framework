# -*- coding: utf-8 -*-
"""Validation rack: DESI DR3 becomes the first working test-bench module (2 Oct 2026).
Michael: make the rack look exactly like what it does and make the displays useful.
rack-bench.js draws the module; this adds the hook, styles and script tag. Run once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "validation.html")
s = open(P, encoding="utf-8").read()
assert "rack-bench.js" not in s


def sub(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


sub('<div class="rcard" id="rc1">', '<div class="rcard" id="rc1" data-bench="desi">')
# a bench module replaces the decorative display; the rack bar stays
sub("    if (head && badges) {\n      var disp=document.createElement('div');",
    "    if (head && badges && !card.hasAttribute('data-bench')) {\n      var disp=document.createElement('div');")

CSS = """
    /* ── Test-bench modules (rack-bench.js) ── */
    .bench { padding:.2rem 1rem 1rem; }
    .bench-plate { flex:1; font:600 .62rem 'IBM Plex Mono', monospace; letter-spacing:.12em; color:#c8d0dc; text-align:center; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
                   background:linear-gradient(#2a3140,#1b212c); border:1px solid #0a0d12; border-radius:2px; padding:1px 6px; box-shadow:inset 0 1px 0 rgba(255,255,255,.08); }
    .bench-screens { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,.9fr); gap:.6rem; align-items:stretch; }
    .bench-screen { background:#040d04; border:1px solid #0a200a; border-radius:4px; box-shadow:inset 0 2px 8px rgba(0,0,0,.9), inset 0 0 14px rgba(0,80,0,.18); padding:.3rem .35rem .2rem; min-width:0; }
    .bench-screen svg { display:block; width:100%; height:auto; }
    .bench-cap { display:flex; justify-content:space-between; font:600 .55rem 'IBM Plex Mono', monospace; letter-spacing:.08em; color:#7dffa0; opacity:.85; margin-bottom:.1rem; }
    .bench-lamps { display:flex; flex-direction:column; justify-content:space-around; gap:.35rem; background:#11161d; border:1px solid #0a0d12; border-radius:4px; padding:.45rem .5rem; }
    .bench-lamp-row { display:flex; align-items:center; gap:.45rem; }
    .bench-lamp { flex:0 0 auto; width:18px; height:18px; border-radius:50%; border:2px solid #0a0d12; box-shadow:inset 0 2px 4px rgba(0,0,0,.6); }
    .bench-lamp.green { background:radial-gradient(circle at 35% 30%, #4b6b50, #1c2a1e); }
    .bench-lamp.yellow { background:radial-gradient(circle at 35% 30%, #6e6436, #2a2614); }
    .bench-lamp.red { background:radial-gradient(circle at 35% 30%, #6e3a36, #2a1614); }
    .bench-lamp.on.green { background:radial-gradient(circle at 35% 30%, #d6ffdc, #3ddc5a 45%, #138a2a); box-shadow:0 0 12px #3ddc5a; }
    .bench-lamp.on.yellow { background:radial-gradient(circle at 35% 30%, #fff6c8, #ffd21f 45%, #a88600); box-shadow:0 0 12px #ffd21f; }
    .bench-lamp.on.red { background:radial-gradient(circle at 35% 30%, #ffd6d3, #ff3b30 45%, #9c1a12); box-shadow:0 0 12px #ff3b30; }
    .bench-rule { font:500 .62rem/1.25 'IBM Plex Sans', sans-serif; color:rgba(255,255,255,.78); }
    .bench-rule b { font-family:'IBM Plex Mono', monospace; font-size:.58rem; letter-spacing:.08em; color:#fff; }
    .bench-strip { display:flex; flex-wrap:wrap; align-items:center; gap:.5rem .6rem; margin-top:.6rem; }
    .bench-knob { all:unset; cursor:pointer; width:26px; height:26px; border-radius:50%; position:relative; flex:0 0 auto;
                  background:radial-gradient(circle at 35% 35%, #c8d0dc 0%, #8090a0 45%, #3a4050 100%); border:1px solid #0e1218; box-shadow:inset 0 1px 2px rgba(255,255,255,.25), 0 2px 4px rgba(0,0,0,.7); }
    .bench-knob span { position:absolute; left:50%; top:3px; width:2px; height:9px; margin-left:-1px; background:#0e1218; border-radius:1px; transform-origin:1px 10px; transform:rotate(var(--rot, -45deg)); transition:transform .25s; }
    .bench-knob:focus-visible { outline:2px solid #7dffa0; outline-offset:2px; }
    .bench-led { width:9px; height:9px; border-radius:50%; flex:0 0 auto; background:#333; }
    .bench-led.waiting { background:#ffb020; box-shadow:0 0 6px #ffb020; }
    .bench-led.window { background:#ffb020; box-shadow:0 0 6px #ffb020; animation:benchBlink 1.2s steps(2, start) infinite; }
    .bench-led.green { background:#3ddc5a; box-shadow:0 0 6px #3ddc5a; } .bench-led.yellow { background:#ffd21f; box-shadow:0 0 6px #ffd21f; } .bench-led.red { background:#ff3b30; box-shadow:0 0 6px #ff3b30; }
    @keyframes benchBlink { to { visibility:hidden; } }
    .bench-stage { font:600 .66rem 'IBM Plex Sans', sans-serif; color:rgba(255,255,255,.85); flex:1 1 9rem; }
    .bench-lcd { display:inline-flex; align-items:baseline; gap:.3rem; background:#1a2a12; border:1px solid #0a0d12; border-radius:3px; padding:.2rem .45rem; text-decoration:none;
                 font-family:'IBM Plex Mono', monospace; color:#b8ff6a; box-shadow:inset 0 1px 4px rgba(0,0,0,.8); }
    .bench-lcd .lbl, .bench-lcd .u { font-size:.5rem; letter-spacing:.08em; opacity:.75; }
    .bench-lcd .n7, .bench-lcd .n30 { font-size:.85rem; font-weight:600; }
    .bench-lcd.fresh .n7 { text-shadow:0 0 6px #b8ff6a; }
    .bench-lcd:hover { border-color:#b8ff6a; }
    .bench-btn { font:700 .58rem 'IBM Plex Mono', monospace; letter-spacing:.1em; color:#0e1218; text-decoration:none; padding:.3rem .55rem; border-radius:3px;
                 background:linear-gradient(#e2e7ee, #aab4c0); border:1px solid #0e1218; box-shadow:inset 0 1px 0 #fff, 0 2px 3px rgba(0,0,0,.6); }
    .bench-btn:hover { background:linear-gradient(#fff, #c8d0dc); }
    .bench-btn:active { transform:translateY(1px); box-shadow:inset 0 1px 0 #fff, 0 1px 1px rgba(0,0,0,.6); }
    @media (max-width:560px) { .bench-screens { grid-template-columns:1fr 1fr; } .bench-lamps { grid-column:1 / -1; } }
"""
sub("    /* ── Rack instrument panel styling ── */", CSS.strip("\n") + "\n\n    /* ── Rack instrument panel styling ── */")
sub("</body>", '<script src="rack-bench.js" defer></script>\n</body>')
open(P, "w", encoding="utf-8").write(s)
print("validation.html: DESI bench module wired")
