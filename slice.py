"""Kollaj rasmni (masalan 4x2) alohida sahifalarga kesadi va WebP qilib saqlaydi.

Ishlatish:
  python slice.py kollaj.png 1            # 1-chapter, 4 ustun x 2 qator
  python slice.py kollaj.png 2 --cols 4 --rows 3

Natija: manga/ch01/01.webp, 02.webp ...
Agar sahifalar allaqachon alohida fayl bo'lsa: python slice.py papka/ 2 --files
"""
import argparse, os, glob
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("chapter", type=int)
ap.add_argument("--cols", type=int, default=4)
ap.add_argument("--rows", type=int, default=2)
ap.add_argument("--trim", type=int, nargs=4, default=[4, 3, 4, 14],
                metavar=("L", "T", "R", "B"), help="har katakdan kesib tashlanadigan piksellar")
ap.add_argument("--files", action="store_true", help="src ichidagi rasmlarni tartib bilan olish")
ap.add_argument("--quality", type=int, default=88)
a = ap.parse_args()

out = f"manga/ch{a.chapter:02d}"
os.makedirs(out, exist_ok=True)

pages = []
if a.files:
    for f in sorted(glob.glob(os.path.join(a.src, "*"))):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            pages.append(Image.open(f).convert("RGB"))
else:
    im = Image.open(a.src).convert("RGB")
    w, h = im.size
    cw, ch = w / a.cols, h / a.rows
    l, t, r, b = a.trim
    for row in range(a.rows):
        for col in range(a.cols):
            box = (round(col * cw + l), round(row * ch + t),
                   round((col + 1) * cw - r), round((row + 1) * ch - b))
            pages.append(im.crop(box))

for i, p in enumerate(pages, 1):
    p.save(f"{out}/{i:02d}.webp", "WEBP", quality=a.quality)
print(f"{len(pages)} sahifa -> {out}/")
