#!/usr/bin/env python3
"""Round 10: shrink mobile LCP hero.

Lighthouse Moto G Power has DPR 1.75 + viewport 412px = needs ~720px image.
With srcset "600w, 1200w" the browser picks 1200w (138KB) - too big.

Fix:
1. Re-encode the LCP hero (1513635269975-59663e0ac1ad) at lower quality
2. Add a 900w intermediate to srcset so mobile picks ~50KB instead of 138KB
"""
import os, glob, re
from PIL import Image

HERO_DIR = 'images/hero'

# Get original full-res webp files (no -sm suffix)
fulls = sorted(p for p in glob.glob(f'{HERO_DIR}/*.webp')
               if '-sm' not in p and '-md' not in p)

print(f'Processing {len(fulls)} hero images')
total_saved = 0
for p in fulls:
    base = p[:-5]  # strip .webp
    img = Image.open(p)
    w, h = img.size
    # Create 900w intermediate (-md)
    md_path = f'{base}-md.webp'
    new_w = 900
    new_h = int(h * new_w / w)
    md_img = img.resize((new_w, new_h), Image.LANCZOS)
    md_img.save(md_path, 'WEBP', quality=68, method=6)
    md_size = os.path.getsize(md_path)
    full_size = os.path.getsize(p)
    print(f'  {os.path.basename(p)}: {w}x{h} {full_size//1024}KB -> md {new_w}x{new_h} {md_size//1024}KB')

# Re-encode -sm at quality 60 (was default 80)
sms = sorted(glob.glob(f'{HERO_DIR}/*-sm.webp'))
print(f'\nRe-encoding {len(sms)} -sm at q=60')
for p in sms:
    before = os.path.getsize(p)
    img = Image.open(p)
    img.save(p, 'WEBP', quality=60, method=6)
    after = os.path.getsize(p)
    total_saved += before - after
print(f'-sm saved {total_saved//1024}KB total')
