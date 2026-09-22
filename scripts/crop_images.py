# -*- coding: utf-8 -*-
from PIL import Image
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(base, "assets", "img")
os.makedirs(out, exist_ok=True)

# explicit (top_start, top_end, after_start, after_end) pixel boxes per source file,
# chosen by inspection to exclude baked-in "До"/"После" captions and watermarks
BOXES = {
    "до после 2.jpg": (0, 430, 640, 1110),
    "до после 3.jpg": (45, 340, 555, 965),
    "до после 4.jpg": (0, 215, 359, 610),
}

pairs = [
    ("до после 2.jpg", "before-2", "after-2"),
    ("до после 3.jpg", "before-3", "after-3"),
    ("до после 4.jpg", "before-4", "after-4"),
]

def inset(img, frac=0.045):
    w, h = img.size
    dx, dy = int(w * frac), int(h * frac)
    return img.crop((dx, dy, w - dx, h - dy))

for fname, before_name, after_name in pairs:
    path = os.path.join(base, fname)
    im = Image.open(path)
    w, h = im.size
    ts, te, as_, ae = BOXES[fname]

    top = inset(im.crop((0, ts, w, te)))
    bottom = inset(im.crop((0, as_, w, ae)))

    top.save(os.path.join(out, before_name + ".jpg"), quality=92)
    bottom.save(os.path.join(out, after_name + ".jpg"), quality=92)
    print(fname, "->", before_name, top.size, after_name, bottom.size)

print("done")
