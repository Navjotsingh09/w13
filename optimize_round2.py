#!/usr/bin/env python3
"""Round 2 speed fixes:
1. Swap Graphie .otf references -> .woff2 in all HTML and shared.css.
2. Update font-face format() to 'woff2'.
3. Reduce Unsplash quality further (q=75 -> q=60).
"""
import os
import re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith(('.html', '.css')) and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    # Swap OTF -> WOFF2 (Graphie-Xxx.otf -> Graphie-Xxx.woff2)
    c = re.sub(r"(Graphie-[A-Za-z]+)\.otf", r"\1.woff2", c)
    # format('opentype') / format("opentype") -> format('woff2')
    c = re.sub(r"format\((['\"])opentype\1\)", r"format(\1woff2\1)", c)
    # type="font/otf" -> type="font/woff2"
    c = c.replace('type="font/otf"', 'type="font/woff2"')

    # Reduce Unsplash q=75 -> q=60
    c = c.replace('q=75&auto=format', 'q=60&auto=format')

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
        print('Updated:', p)
print(f'\n{count} files')
