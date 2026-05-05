#!/usr/bin/env python3
"""
optimize_round19.py
====================
1. Fix hero <img>: loading="lazy" → loading="eager" fetchpriority="high"
   for all non-index pages that have an <img> as the LCP hero element.
2. Add <link rel="preload" as="image"> in <head> for each hero image.
3. Localize NCSC Cyber Essentials badge: replace external URL with local
   images/ncsc-cyber-essentials.svg on all HTML pages.

Requires: images/ncsc-cyber-essentials.svg already downloaded locally.
"""

import os
import re

BASE = '/Users/navjotsinghhundal/W13Uk'

# ── Hero pages to fix ─────────────────────────────────────────────────────────
# (relative_path, hero_src, srcset_or_None, sizes_or_None)
HERO_FIXES = [
    (
        'projects.html',
        'images/hero/1486406146926-c627a92ad1ab.webp',
        'images/hero/1486406146926-c627a92ad1ab-sm.webp 600w, '
        'images/hero/1486406146926-c627a92ad1ab-md.webp 750w, '
        'images/hero/1486406146926-c627a92ad1ab.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'about.html',
        'images/W13 - Pictures/about-us-main.webp',
        None, None,
    ),
    (
        'services/architecture-design.html',
        '../images/hero/1503387762-592deb58ef4e.webp',
        '../images/hero/1503387762-592deb58ef4e-sm.webp 600w, '
        '../images/hero/1503387762-592deb58ef4e-md.webp 750w, '
        '../images/hero/1503387762-592deb58ef4e.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'services/asset-management.html',
        '../images/hero/1486406146926-c627a92ad1ab.webp',
        '../images/hero/1486406146926-c627a92ad1ab-sm.webp 600w, '
        '../images/hero/1486406146926-c627a92ad1ab-md.webp 750w, '
        '../images/hero/1486406146926-c627a92ad1ab.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'services/consultancy.html',
        '../images/hero/1449157291145-7efd050a4d0e.webp',
        '../images/hero/1449157291145-7efd050a4d0e-sm.webp 600w, '
        '../images/hero/1449157291145-7efd050a4d0e-md.webp 750w, '
        '../images/hero/1449157291145-7efd050a4d0e.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'services/land-development.html',
        '../images/W13 - Pictures/our-services-land-dev.webp',
        None, None,
    ),
    (
        'services/master-developer.html',
        '../images/hero/1541888946425-d81bb19240f5.webp',
        '../images/hero/1541888946425-d81bb19240f5-sm.webp 600w, '
        '../images/hero/1541888946425-d81bb19240f5-md.webp 750w, '
        '../images/hero/1541888946425-d81bb19240f5.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'sectors/architects-planning.html',
        '../images/hero/1503387762-592deb58ef4e.webp',
        '../images/hero/1503387762-592deb58ef4e-sm.webp 600w, '
        '../images/hero/1503387762-592deb58ef4e-md.webp 750w, '
        '../images/hero/1503387762-592deb58ef4e.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'sectors/commercial.html',
        '../images/hero/1486406146926-c627a92ad1ab.webp',
        '../images/hero/1486406146926-c627a92ad1ab-sm.webp 600w, '
        '../images/hero/1486406146926-c627a92ad1ab-md.webp 750w, '
        '../images/hero/1486406146926-c627a92ad1ab.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
    (
        'sectors/residential.html',
        '../images/W13 - Pictures/residential-main.webp',
        None, None,
    ),
    (
        'sectors/urban-regeneration.html',
        '../images/hero/1517089596392-fb9a9033e05b.webp',
        '../images/hero/1517089596392-fb9a9033e05b-sm.webp 600w, '
        '../images/hero/1517089596392-fb9a9033e05b-md.webp 750w, '
        '../images/hero/1517089596392-fb9a9033e05b.webp 1200w',
        '(max-width: 768px) 100vw, 1200px',
    ),
]

NCSC_EXTERNAL = 'https://www.ncsc.gov.uk/sites/default/files/2026-02/300x75-ce.svg'


def ncsc_local_path(rel_path):
    """Return local relative path to NCSC SVG adjusted for page directory depth."""
    depth = rel_path.replace('\\', '/').count('/')
    prefix = '../' * depth
    return f'{prefix}images/ncsc-cyber-essentials.svg'


def process_hero(rel_path, src, srcset, sizes):
    filepath = os.path.join(BASE, rel_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # ── Fix loading attribute ─────────────────────────────────────────────────
    old_loading = f'loading="lazy" src="{src}"'
    new_loading  = f'loading="eager" fetchpriority="high" src="{src}"'
    already_fixed = f'loading="eager" fetchpriority="high" src="{src}"' in content

    if already_fixed:
        print(f'  ↩ Hero already eager+fetchpriority: {rel_path}')
    elif old_loading in content:
        content = content.replace(old_loading, new_loading, 1)
        changed = True
        print(f'  ✓ Fixed hero loading: {rel_path}')
    else:
        # Try without quotes match — maybe attributes are in different order
        # Fall back: just replace the first loading="lazy" inside the hero src context
        pattern = re.compile(
            r'(src="' + re.escape(src) + r'"[^>]*?)(\bloading="lazy"\b)'
        )
        if pattern.search(content):
            content = pattern.sub(r'\1loading="eager" fetchpriority="high"', content, count=1)
            changed = True
            print(f'  ✓ Fixed hero loading (alt pattern): {rel_path}')
        else:
            print(f'  ✗ Hero img NOT matched in {rel_path} — check manually')

    # ── Add preload hint ──────────────────────────────────────────────────────
    preload_marker = f'rel="preload" as="image" href="{src}"'
    if preload_marker in content:
        print(f'  ↩ Preload already present: {rel_path}')
    else:
        if srcset and sizes:
            preload_tag = (
                f'    <link rel="preload" as="image" href="{src}"'
                f' imagesrcset="{srcset}"'
                f' imagesizes="{sizes}">\n'
            )
        else:
            preload_tag = f'    <link rel="preload" as="image" href="{src}">\n'

        if '</head>' in content:
            content = content.replace('</head>', preload_tag + '</head>', 1)
            changed = True
            print(f'  ✓ Added preload hint: {rel_path}')
        else:
            print(f'  ✗ </head> not found in {rel_path}')

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def fix_ncsc_all():
    """Replace the external NCSC badge URL with a local path on every HTML page."""
    for dirpath, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d != 'home1']  # skip React subfolder
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            fullpath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(fullpath, BASE)
            with open(fullpath, 'r', encoding='utf-8') as f:
                content = f.read()
            if NCSC_EXTERNAL not in content:
                continue
            local = ncsc_local_path(rel_path)
            content = content.replace(NCSC_EXTERNAL, local)
            with open(fullpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  ✓ NCSC badge → {local}  ({rel_path})')


# ── Main ──────────────────────────────────────────────────────────────────────
print('=== optimize_round19.py ===\n')

print('--- Step 1: Hero fetchpriority + preload ---')
for args in HERO_FIXES:
    process_hero(*args)

print('\n--- Step 2: Localize NCSC badge ---')
ncsc_svg = os.path.join(BASE, 'images', 'ncsc-cyber-essentials.svg')
if not os.path.exists(ncsc_svg):
    print(f'  ⚠  NCSC SVG missing: {ncsc_svg}')
    print('     Download: https://www.ncsc.gov.uk/sites/default/files/2026-02/300x75-ce.svg')
    print('     Save to:  images/ncsc-cyber-essentials.svg')
else:
    fix_ncsc_all()

print('\n✅ Done.')
