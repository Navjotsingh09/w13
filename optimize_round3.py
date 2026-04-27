#!/usr/bin/env python3
"""Round 3 mobile speed:
1. Drop Unsplash w=1200/q=60 -> w=800/q=55 (~50% bytes off hero)
2. Add `defer` to GSAP/ScrollTrigger CDN scripts (move out of critical path)
3. Convert <link rel="stylesheet" href="shared.css"> to async preload pattern
4. Minify shared.css (strip comments + collapse whitespace)
"""
import os, re

# ---- 4) minify shared.css ----
with open('shared.css') as f:
    css = f.read()
# strip /* */ comments
css_min = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
# collapse whitespace
css_min = re.sub(r'\s+', ' ', css_min)
css_min = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_min)
css_min = css_min.replace(';}', '}').strip()
with open('shared.min.css', 'w') as f:
    f.write(css_min)
print(f'shared.css: {len(css)//1024}KB -> shared.min.css: {len(css_min)//1024}KB')

# ---- HTML edits ----
paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    # 1) Unsplash: w=1200&q=60 -> w=800&q=55
    c = c.replace('w=1200&q=60&auto=format', 'w=800&q=55&auto=format')
    c = c.replace('w=1200&amp;q=60&amp;auto=format', 'w=800&amp;q=55&amp;auto=format')

    # 2) Add defer to GSAP & ScrollTrigger
    c = re.sub(
        r'<script src="(https://cdnjs\.cloudflare\.com/ajax/libs/gsap/[^"]+)"></script>',
        r'<script defer src="\1"></script>',
        c,
    )

    # 3) shared.css -> async preload pattern + use minified
    # match any indent of <link rel="stylesheet" href="...shared.css">
    c = re.sub(
        r'<link rel="stylesheet" href="((?:\.\./)?)shared(?:\.min)?\.css">',
        r'<link rel="preload" href="\1shared.min.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="\1shared.min.css"></noscript>',
        c,
    )

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
print(f'Updated {count} HTML files')
