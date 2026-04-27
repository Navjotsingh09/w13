#!/usr/bin/env python3
"""Add width/height to footer logo + NCSC images."""
import os
import re

html_files = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            html_files.append(os.path.join(root, f))

count = 0
for p in html_files:
    with open(p) as fh:
        c = fh.read()
    o = c
    c = re.sub(
        r'<img\s+src="([^"]*?W13_Logo_full_White\.webp)"\s+alt="W13 Group"\s+loading="lazy">',
        r'<img src="\1" alt="W13 Group" loading="lazy" width="200" height="100" decoding="async">',
        c,
    )
    c = re.sub(
        r'<img\s+src="(https://www\.ncsc\.gov\.uk/sites/default/files/2026-02/300x75-ce\.svg)"\s+alt="NCSC Cyber Essentials"\s+loading="lazy">',
        r'<img src="\1" alt="NCSC Cyber Essentials" loading="lazy" width="150" height="38" decoding="async">',
        c,
    )
    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
        print('Updated', p)
print(f'\n{count} files')
