#!/usr/bin/env python3
"""Round 8b: remove preloader DOM entirely.

Two patterns exist:
- index.html: <div class="preloader" id="preloader">...3 dots...</div>
- other pages: <div class="preloader" id="preloader"><div class="preloader-brand" ...>...</div></div>

Both block LCP. Just remove them. The hero already has background:#0C233F so no FOUC.

Also neutralise the preloader-fade scripts (they reference removed element):
- "window.addEventListener('load', () => { setTimeout(() => { ... preloader ... }) })"
- "window.addEventListener('load', function() { setTimeout(function() { ... is-hidden ... }) })"
"""
import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# Match the preloader div (greedy until matching </div> at same indent depth).
# Both patterns are simple: <div class="preloader" id="preloader"> ... </div>
# where "..." may contain nested <div> tags but only 1-2 levels.
PRELOADER_RE = re.compile(
    r'\n?\s*(?:<!--\s*Preloader\s*-->\s*\n?\s*)?'
    r'<div class="preloader" id="preloader">.*?</div>\s*</div>\s*',
    re.S,
)
PRELOADER_SIMPLE_RE = re.compile(
    r'\n?\s*(?:<!--\s*Preloader\s*-->\s*\n?\s*)?'
    r'<div class="preloader" id="preloader">.*?</div>\s*',
    re.S,
)

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    # Try complex (nested) pattern first; fall back to simple
    if '<div class="preloader-brand"' in c or '<div class="preloader-dots"' in c:
        # has nested div, count closing tags
        m = re.search(r'<div class="preloader" id="preloader">', c)
        if m:
            start = m.start()
            # walk forward counting <div> open/close from start
            i = m.end()
            depth = 1
            while depth > 0 and i < len(c):
                next_open = c.find('<div', i)
                next_close = c.find('</div>', i)
                if next_close == -1:
                    break
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    i = next_open + 4
                else:
                    depth -= 1
                    i = next_close + 6
            # also strip leading comment + whitespace
            seg_start = start
            preceding = c[:start]
            m2 = re.search(r'(\n\s*<!--\s*Preloader\s*-->\s*\n?\s*)$', preceding)
            if m2:
                seg_start = m2.start()
            c = c[:seg_start] + '\n' + c[i:].lstrip('\n')

    if c == o:
        c = PRELOADER_RE.sub('\n', c)
    if c == o:
        c = PRELOADER_SIMPLE_RE.sub('\n', c)

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
print(f'Removed preloader from {count} files')

# Now sanity check - any pages still containing preloader div?
remaining = []
for p in paths:
    with open(p) as fh:
        if '<div class="preloader"' in fh.read():
            remaining.append(p)
print(f'Pages still with preloader div: {len(remaining)}')
for r in remaining[:5]:
    print(' -', r)
