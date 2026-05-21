#!/usr/bin/env python3
"""Strip all OLD nav-related CSS rules from the pre-canonical zone on outlier
pages, so only the canonical block (matching index.html) governs nav styling."""
import re
from pathlib import Path

OUTLIERS = [
    '404.html', 'careers.html', 'privacy-policy.html', 'terms.html',
    'news.html', 'news-delivering-net-zero.html',
    'news-housing-market-outlook.html', 'news-rise-of-btr.html',
    'services/architecture-design.html', 'services/asset-management.html',
    'services/consultancy.html', 'services/land-development.html',
    'services/master-developer.html',
]

# Selectors whose top-level (and stray) rules in the pre-canonical zone we strip
# Use word boundary in regex
STRIP_SELECTOR_RE = re.compile(
    r'(?<![A-Za-z0-9_-])'
    r'(\.(?:navbar(?:\.scrolled)?|nav-(?:links|link|inner|logo|center|cta(?:-dot)?|dropdown(?:-toggle)?)|mega-menu(?:-[a-z-]+)?|menu-[a-z-]+))'
    r'\{[^{}]+\}',
    re.IGNORECASE,
)

root = Path('/Users/navjotsinghhundal/W13Uk')

for rel in OUTLIERS:
    p = root / rel
    txt = p.read_text()
    marker = '===NAV-CANONICAL-START==='
    idx = txt.find(marker)
    if idx < 0:
        print(f'  {rel}: NO CANONICAL MARKER, skipping')
        continue

    pre = txt[:idx]
    post = txt[idx:]

    # Count matches before stripping
    matches = list(STRIP_SELECTOR_RE.finditer(pre))
    if not matches:
        print(f'  {rel}: no old nav rules to strip')
        continue

    # Strip
    new_pre = STRIP_SELECTOR_RE.sub('', pre)
    new_txt = new_pre + post
    delta = len(txt) - len(new_txt)
    p.write_text(new_txt)
    sels = sorted({m.group(1) for m in matches})
    print(f'  {rel}: stripped {len(matches)} old rules ({delta} bytes); selectors: {sels}')

print('\nDone.')
