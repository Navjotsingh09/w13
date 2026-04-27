#!/usr/bin/env python3
"""Optimize HTML for mobile speed:
1. Replace Unsplash w=2400&q=90 with mobile-sized auto-format (w=1200&q=75&auto=format).
2. Switch W13-Pictures jpg refs to webp.
3. Switch logo png refs to webp where appropriate.
4. Add loading=lazy + width/height to cyber-essentials iframe.
5. Defer Font Awesome CSS (load async).
6. Remove width/height=2400/1600 from Unsplash hero imgs (they were misleading).
"""
import os
import re

def process(path, content):
    orig = content

    # 1. Unsplash: w=2400 -> w=1200, q=90 -> q=75, add &auto=format
    def unsplash_sub(m):
        url = m.group(0)
        # parse query
        url = url.replace('w=2400', 'w=1200').replace('q=90', 'q=75')
        if 'auto=' not in url:
            url += '&auto=format'
        return url
    content = re.sub(r'https://images\.unsplash\.com/[^"\'\s)]+', unsplash_sub, content)

    # 2. Replace explicit width="2400" height="1600" on Unsplash imgs with width="1200" height="800"
    content = re.sub(
        r'(<img[^>]*?)width="2400"\s+height="1600"([^>]*?images\.unsplash)',
        r'\1width="1200" height="800"\2',
        content,
    )

    # 3. W13 - Pictures jpg -> webp
    content = re.sub(
        r'(images/W13(?:%20|\s|\s)-(?:%20|\s)Pictures/[a-z0-9\-]+)\.jpg',
        r'\1.webp',
        content,
        flags=re.IGNORECASE,
    )

    # 4. Logo PNG -> WebP for inline images (not og:image meta)
    # Only replace W13_Logo_White.png and W13_Logo_full_White.png in <img src=
    content = re.sub(
        r'(<img[^>]*src="[^"]*?W13_Logo(?:_full)?_White)\.png',
        r'\1.webp',
        content,
    )

    # 5. cyber-essentials iframe -> loading="lazy"
    def iframe_sub(m):
        s = m.group(0)
        if 'loading=' in s:
            return s
        return s.replace('<iframe ', '<iframe loading="lazy" ', 1)
    content = re.sub(r'<iframe[^>]*cyber-essentials-certificate\.pdf[^>]*>', iframe_sub, content)

    # 6. Defer Font Awesome (cdnjs all.min.css) — async via media trick
    fa_old = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">'
    fa_new = ('<link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" '
              'as="style" onload="this.onload=null;this.rel=\'stylesheet\'">'
              '<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>')
    content = content.replace(fa_old, fa_new)

    # 7. Reduce font preloads from Light/Regular/Bold to just Regular (Bold can come later)
    # Remove preload of Graphie-Bold and Graphie-Light to reduce critical chain
    content = re.sub(
        r'\s*<link rel="preload" href="(?:\.\./)?fonts/Graphie-(?:Bold|Light|SemiBold|LightItalic)\.otf" as="font" type="font/otf"[^>]*>',
        '',
        content,
    )
    # Ensure preloaded Regular has crossorigin
    content = re.sub(
        r'<link rel="preload" href="((?:\.\./)?fonts/Graphie-Regular\.otf)" as="font" type="font/otf"(?!\s+crossorigin)>',
        r'<link rel="preload" href="\1" as="font" type="font/otf" crossorigin>',
        content,
    )

    return content, content != orig

# Walk all html files
html_files = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            html_files.append(os.path.join(root, f))

changed = 0
for path in html_files:
    with open(path) as fh:
        content = fh.read()
    new, did = process(path, content)
    if did:
        with open(path, 'w') as fh:
            fh.write(new)
        print(f'Updated: {path}')
        changed += 1
print(f'\n{changed} files updated.')
