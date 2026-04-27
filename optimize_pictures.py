#!/usr/bin/env python3
"""Optimize W13 - Pictures images and logo to WebP for mobile speed."""
import os
from PIL import Image

PICS = 'images/W13 - Pictures'
MAX_W = 1600
QUALITY = 80

# Convert lowercase-named copies (the ones referenced in HTML)
files = [f for f in os.listdir(PICS) if f.endswith('.jpg') and f.islower() or f.lower() == f]
# Actually, just take the lowercase variants
lowercase = [f for f in os.listdir(PICS) if f == f.lower() and f.endswith('.jpg')]

total_orig = 0
total_new = 0
for fname in lowercase:
    src = os.path.join(PICS, fname)
    dst = os.path.join(PICS, fname.rsplit('.', 1)[0] + '.webp')
    orig = os.path.getsize(src)
    total_orig += orig
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
        total_new += os.path.getsize(dst)
        continue
    im = Image.open(src).convert('RGB')
    if im.width > MAX_W:
        ratio = MAX_W / im.width
        im = im.resize((MAX_W, int(im.height * ratio)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=QUALITY, method=6)
    new = os.path.getsize(dst)
    total_new += new
    print(f'{fname}: {orig // 1024}KB -> {new // 1024}KB')

print(f'\nW13 Pictures: {total_orig // 1024}KB -> {total_new // 1024}KB')

# Logo: 2298x1141 served at 141x70 max — make 360x179 (2x for retina)
for logo in ['W13_Logo_White.png', 'W13_Logo_full_White.png']:
    src = f'images/{logo}'
    dst = f'images/{logo.rsplit(".", 1)[0]}.webp'
    if not os.path.exists(src):
        continue
    im = Image.open(src)
    # keep transparent
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    if im.width > 480:
        ratio = 480 / im.width
        im = im.resize((480, int(im.height * ratio)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=85, method=6)
    print(f'{logo}: {os.path.getsize(src)//1024}KB -> {os.path.getsize(dst)//1024}KB ({im.width}x{im.height})')
