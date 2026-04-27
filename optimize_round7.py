#!/usr/bin/env python3
"""Round 7: minify the inline <style> block in every HTML file.

The inline critical CSS is ~47KB unminified per page.
A simple regex-based minifier:
- Strip /* ... */ comments
- Collapse whitespace between/after CSS rules
- Remove space around { } : ; , > + ~
- Drop trailing ;}
"""
import os, re

def minify_css(css: str) -> str:
    # strip comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    # newlines/tabs -> space, then collapse
    css = re.sub(r'\s+', ' ', css)
    # remove space around special chars
    css = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css)
    css = css.replace(';}', '}').strip()
    return css

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# Match each <style> ... </style> block (not <style scoped>)
STYLE_RE = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.S)

# Skip JSON-LD <script type="application/ld+json"> already untouched
total_saved = [0]
count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    def repl(m):
        before = m.group(2)
        after = minify_css(before)
        total_saved[0] += len(before) - len(after)
        return m.group(1) + after + m.group(3)

    c = STYLE_RE.sub(repl, c)

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1

print(f'Minified styles in {count} files. Saved {total_saved[0]//1024}KB total.')
