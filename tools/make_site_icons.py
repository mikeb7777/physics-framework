# -*- coding: utf-8 -*-
"""apple-touch-icon.png and favicon.ico from the current Spinner
(#c62828 / #2e7d32 / #005ba5). Both still carried the old yellow one.
Source: Ic2-Logo-Pack/spinner/spinner-transparent-1024.png (build_logo_pack.py).
apple-touch-icon.png is also the Organization logo in the index JSON-LD."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPIN = Image.open(os.path.join(os.path.dirname(ROOT), "Ic2-Logo-Pack", "spinner", "spinner-transparent-1024.png")).convert("RGBA")

# iOS fills transparency with black, so the touch icon sits on white with a margin
icon = Image.new("RGBA", (180, 180), (255, 255, 255, 255))
s = 140
icon.alpha_composite(SPIN.resize((s, s), Image.LANCZOS), ((180 - s) // 2, (180 - s) // 2))
icon.convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"), optimize=True)

# favicon.ico: transparent, the Spinner filling the square, 16/32/48
SPIN.resize((256, 256), Image.LANCZOS).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote apple-touch-icon.png, favicon.ico")
