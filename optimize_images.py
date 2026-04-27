#!/usr/bin/env python3
"""Convert referenced project images to optimized WebP for mobile speed."""
import os
from PIL import Image

REFERENCED = """images/projects/hilston-park/1.jpg
images/projects/hilston-park/render-1.jpg
images/projects/hilston-park/render-2.jpg
images/projects/hilston-park/render-3.jpg
images/projects/oldbury-gurdwara/1.jpg
images/projects/oldbury-gurdwara/elevations.jpg
images/projects/oldbury-gurdwara/floor-plans.jpg
images/projects/oldbury-gurdwara/renders.jpg
images/projects/oldbury-gurdwara/second-floor.jpg
images/projects/pear-tree-lane/1.jpg
images/projects/pear-tree-lane/render-1.jpg
images/projects/pear-tree-lane/render-2.jpg
images/projects/pear-tree-lane/render-3.jpg
images/projects/pear-tree-lane/render-4.jpg
images/projects/pear-tree-lane/render-5.jpg
images/projects/pear-tree-lane/street-view-1.jpg
images/projects/pear-tree-lane/street-view-2.jpg
images/projects/pear-tree-lane/street-view-3.jpg
images/projects/showell-lane/1.jpg
images/projects/showell-lane/render-1.jpg
images/projects/showell-lane/render-2.jpg
images/projects/showell-lane/render-3.jpg
images/projects/showell-lane/render-4.jpg
images/projects/thornley-street/1.jpg
images/projects/thornley-street/east-elevation.png
images/projects/thornley-street/ground-floor.jpg
images/projects/thornley-street/north-elevation.png
images/projects/thornley-street/south-elevation.png
images/projects/walsall-road/1.jpg
images/projects/walsall-road/image-1.png
images/projects/walsall-road/image-2.png
images/projects/walsall-road/montage.jpg
images/projects/walsall-road/render-1.jpg
images/projects/walsall-road/render-2.jpg
images/projects/walsall-road/render-3.jpg
images/projects/willenhall-gurdwara/floor-plan.png
images/projects/willenhall-gurdwara/photo-1.jpg
images/projects/willenhall-gurdwara/photo-10.jpg
images/projects/willenhall-gurdwara/photo-2.jpg
images/projects/willenhall-gurdwara/photo-3.jpg
images/projects/willenhall-gurdwara/photo-4.jpg
images/projects/willenhall-gurdwara/photo-5.jpg
images/projects/willenhall-gurdwara/photo-6.jpg
images/projects/willenhall-gurdwara/photo-7.jpg
images/projects/willenhall-gurdwara/photo-8.jpg
images/projects/willenhall-gurdwara/photo-9.jpg
images/projects/willenhall-gurdwara/render-1.png
images/projects/willenhall-gurdwara/render-2.png""".strip().splitlines()

MAX_W = 1920
QUALITY = 80

total_orig = 0
total_new = 0
skipped = 0
for src in REFERENCED:
    if not os.path.exists(src):
        print('MISSING:', src)
        continue
    base = os.path.splitext(src)[0]
    dst = base + '.webp'
    orig = os.path.getsize(src)
    total_orig += orig
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
        total_new += os.path.getsize(dst)
        skipped += 1
        continue
    try:
        im = Image.open(src)
        im = im.convert('RGB')
        if im.width > MAX_W:
            ratio = MAX_W / im.width
            im = im.resize((MAX_W, int(im.height * ratio)), Image.LANCZOS)
        im.save(dst, 'WEBP', quality=QUALITY, method=6)
        new = os.path.getsize(dst)
        total_new += new
        pct = 100 - int(new * 100 / orig)
        print(f'{src}: {orig // 1024}KB -> {new // 1024}KB ({pct}% smaller)')
    except Exception as e:
        print('ERR', src, e)

print(f'\nSkipped (already up-to-date): {skipped}')
print(f'TOTAL: {total_orig // 1024 // 1024}MB -> {total_new // 1024 // 1024}MB')
