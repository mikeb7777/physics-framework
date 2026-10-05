# -*- coding: utf-8 -*-
"""Burn the provenance watermark into the Visualizations preview tiles (sim-thumbs/*.mp4 and *.jpg), so a
saved or reposted preview still says it is an Ic² visual and what kind (Michael, 6 Oct 2026: "Each should
carry a watermark that it's an IC2 model, or simulation, etc. in case it's used off-site").
Run once, and again only on freshly recorded tiles (tools/record_sim_thumbs.py writes unmarked files)."""
import os, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "sim-thumbs")
KIND = {"c-field": "Concept", "c-ent": "Model", "c-rot": "Concept", "c-four": "Model", "c-scram": "Model",
        "c-bang": "Concept", "c-bamboo": "Concept", "c-bell": "Model", "c-subplanck": "Concept",
        "c-chamber": "Simulated", "c-nowwin": "Model", "c-phi": "Model"}
FONT = "C\\:/Windows/Fonts/arialbd.ttf"
FF = shutil.which("ffmpeg")

for name, kind in KIND.items():
    text = f"Ic² Research Institute · {kind}"
    vf = (f"drawbox=x=iw-tw-18:y=ih-th-14:w=0:h=0:c=black@0,"  # placeholder keeps the chain simple
          f"drawtext=fontfile='{FONT}':text='{text}':fontsize=12:fontcolor=white@0.85:"
          f"box=1:boxcolor=0x0a0f1e@0.55:boxborderw=4:x=w-tw-10:y=h-th-9")
    vf = vf.split(",", 1)[1]
    for ext in ("mp4", "jpg"):
        src = os.path.join(D, f"{name}.{ext}"); tmp = os.path.join(D, f"_{name}.{ext}")
        args = [FF, "-y", "-loglevel", "error", "-i", src, "-vf", vf]
        args += (["-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart"] if ext == "mp4" else ["-q:v", "3"])
        subprocess.run(args + [tmp], check=True)
        os.replace(tmp, src)
    print(name, kind)
