#!/usr/bin/env python3
"""Round 4: target LCP & remove render-blocking 3rd party CSS.

1. Add preconnect to images.unsplash.com + cdnjs.cloudflare.com on every page
2. Preload the first hero <img> (the one with fetchpriority="high") on each page
3. Defer Font Awesome CSS load until after window.load (was preload-onload, now JS-injected)
"""
import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# Snippet to inject in <head>
PRECONNECT = (
    '<link rel="preconnect" href="https://images.unsplash.com" crossorigin>\n'
    '    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>\n    '
)

# JS to inject Font Awesome after load
FA_JS = """<script>window.addEventListener('load',function(){var l=document.createElement('link');l.rel='stylesheet';l.href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';document.head.appendChild(l);});</script>"""

# regex to find FA preload line and remove it (we move FA to JS after load)
FA_LINE = re.compile(
    r'\s*<link rel="preload" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+" as="style" onload="[^"]*"><noscript><link rel="stylesheet" href="[^"]+"></noscript>'
)

# preload hero image: prefer the unsplash one (real LCP), fallback to any eager+fetchpriority
HERO_UNSPLASH_RE = re.compile(r'<img\s+loading="eager"\s+fetchpriority="high"[^>]*src="(https://images\.unsplash\.com/[^"]+)"', re.I)
HERO_ANY_RE = re.compile(r'<img\s+loading="eager"\s+fetchpriority="high"[^>]*src="([^"]+)"', re.I)

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    # 1) Add preconnects (only if not already added) — insert after first <link rel="preload" ... Graphie-Regular.woff2 ...>
    if 'preconnect" href="https://images.unsplash.com"' not in c:
        c = c.replace(
            '<link rel="preload" href="fonts/Graphie-Regular.woff2"',
            PRECONNECT + '<link rel="preload" href="fonts/Graphie-Regular.woff2"',
            1,
        )

    # 2) Preload hero image
    if 'rel="preload" as="image"' not in c:
        m = HERO_UNSPLASH_RE.search(c) or HERO_ANY_RE.search(c)
        if m:
            hero_src = m.group(1)
            preload = f'<link rel="preload" as="image" href="{hero_src}" fetchpriority="high">\n    '
            # insert just after preconnect block (or before the FA line / shared.css)
            c = c.replace(
                '<link rel="preload" href="fonts/Graphie-Regular.woff2"',
                preload + '<link rel="preload" href="fonts/Graphie-Regular.woff2"',
                1,
            )

    # 3) Replace FA preload line with JS-after-load
    if FA_LINE.search(c):
        c = FA_LINE.sub('\n    ' + FA_JS, c, count=1)

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
print(f'Updated {count} files')
