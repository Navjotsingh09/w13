#!/usr/bin/env python3
"""Port canonical nav + mega-menu CSS from index.html into 13 outlier pages."""
import re
import sys

with open('index.html') as f:
    t = f.read()

m = re.search(r'<style[^>]*>(.*?)</style>', t, re.DOTALL)
assert m, "no inline style in index.html"
css = m.group(1)


def iter_rules(s):
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i] in ' \t\n\r':
            i += 1
        if i >= n:
            break
        sel_start = i
        while i < n and s[i] != '{':
            i += 1
        if i >= n:
            break
        sel = s[sel_start:i].strip()
        i += 1
        body_start = i
        depth = 1
        while i < n and depth > 0:
            if s[i] == '{':
                depth += 1
            elif s[i] == '}':
                depth -= 1
            i += 1
        body = s[body_start:i - 1]
        yield sel, body


NAV_PREFIXES = (
    '.navbar', '.nav-inner', '.nav-logo', '.nav-center', '.nav-link',
    '.nav-cta', '.nav-dropdown', '.nav-mobile', '.nav-spacer',
    '.mega-menu', '.lifecycle-mini',
    '.menu-overlay', '.menu-panel', '.menu-nav', '.menu-close', '.menu-toggle',
    '.menu-focusable', '.menu-left', '.menu-right', '.menu-image',
    '.top-nav-link',
)
EXCLUDE = ('.footer-nav', '.hero-nav', '.services-nav', '.menu-cta-bar', '.mobile-cta')


def is_nav_selector(sel):
    parts = [p.strip() for p in sel.split(',')]
    has_nav = False
    for p in parts:
        m2 = re.match(r'([.#][a-zA-Z][a-zA-Z0-9_-]*)', p)
        if not m2:
            continue
        first = m2.group(1)
        if any(first.startswith(x) for x in EXCLUDE):
            return False
        if any(first == x or first.startswith(x + '-') or first.startswith(x + '.') or first == x for x in NAV_PREFIXES):
            has_nav = True
        if first in NAV_PREFIXES:
            has_nav = True
    return has_nav


kept = []
for sel, body in iter_rules(css):
    if sel.startswith('@media') or sel.startswith('@supports'):
        inner = []
        for sub_sel, sub_body in iter_rules(body):
            if is_nav_selector(sub_sel):
                inner.append(f'{sub_sel}{{{sub_body}}}')
        if inner:
            kept.append(f'{sel}{{{"".join(inner)}}}')
    else:
        if is_nav_selector(sel):
            kept.append(f'{sel}{{{body}}}')

CANON_NAV_CSS = ''.join(kept)
MARKER_START = '/* ===NAV-CANONICAL-START=== */'
MARKER_END = '/* ===NAV-CANONICAL-END=== */'
INJECTION = MARKER_START + CANON_NAV_CSS + MARKER_END

print(f'Extracted {len(kept)} rules/media blocks, {len(CANON_NAV_CSS)} chars of canonical nav CSS')

with open('/tmp/nav_canonical.css', 'w') as fh:
    fh.write(CANON_NAV_CSS)

# Target pages
OUTLIERS = [
    '404.html', 'careers.html', 'privacy-policy.html', 'terms.html',
    'news.html', 'news-delivering-net-zero.html', 'news-housing-market-outlook.html', 'news-rise-of-btr.html',
    'services/architecture-design.html', 'services/asset-management.html',
    'services/consultancy.html', 'services/land-development.html',
    'services/master-developer.html',
]

if '--inject' in sys.argv:
    for path in OUTLIERS:
        with open(path) as fh:
            src = fh.read()
        if MARKER_START in src:
            # Replace existing injected block
            new_src = re.sub(
                re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END),
                INJECTION,
                src, count=1, flags=re.DOTALL,
            )
            action = 'updated'
        else:
            # Inject right before closing </style> of the FIRST <style> block
            sm = re.search(r'</style>', src)
            if not sm:
                print(f'  {path}: NO </style> — skipped')
                continue
            new_src = src[:sm.start()] + INJECTION + src[sm.start():]
            action = 'injected'
        if new_src == src:
            print(f'  {path}: no change')
        else:
            with open(path, 'w') as fh:
                fh.write(new_src)
            print(f'  {path}: {action} ({len(new_src) - len(src):+d} bytes)')
else:
    print('Dry run. Re-run with --inject to apply.')
