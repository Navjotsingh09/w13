#!/usr/bin/env python3
"""Round 5: self-host Unsplash images and remove FA preconnect once not needed."""
import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# 404'd image -> use a similar urban substitute
SUBSTITUTE = {'1582407947092-50b6ef26d700': '1486406146926-c627a92ad1ab'}

# Pattern: any unsplash photo URL with optional query params
URL_RE = re.compile(r'https://images\.unsplash\.com/photo-([a-z0-9-]+)\?[^"\']*')

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    depth = '../' if '/' in p[2:] else ''  # files in subdir need ../

    def repl(m):
        pid = m.group(1)
        pid = SUBSTITUTE.get(pid, pid)
        return f'{depth}images/hero/{pid}.webp'

    c = URL_RE.sub(repl, c)

    # Remove unsplash preconnect (no longer needed)
    c = c.replace('    <link rel="preconnect" href="https://images.unsplash.com" crossorigin>\n', '')

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
print(f'Updated {count} files')
