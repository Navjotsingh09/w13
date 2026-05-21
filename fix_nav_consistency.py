#!/usr/bin/env python3
"""
Two fixes:
1. Make navbar transparent (like home page) on all 13 outlier pages — strip the
   solid background/backdrop-filter from their OLD .navbar rule.
2. Revert services.html hero back to WHITE background, but force nav links to
   dark navy so they remain visible on that one page.
"""
import re
import sys

OUTLIERS = [
    '404.html', 'careers.html', 'privacy-policy.html', 'terms.html',
    'news.html', 'news-delivering-net-zero.html', 'news-housing-market-outlook.html', 'news-rise-of-btr.html',
    'services/architecture-design.html', 'services/asset-management.html',
    'services/consultancy.html', 'services/land-development.html',
    'services/master-developer.html',
]

# Patterns of the solid-bg fragment that appears inside the OLD .navbar{...} rule
SOLID_BG_PATTERNS = [
    ';background:rgba(12,35,63,0.95);backdrop-filter:blur(10px)',
    ';backdrop-filter:blur(10px);background:rgba(12,35,63,0.95)',
    'background:rgba(12,35,63,0.95);backdrop-filter:blur(10px);',
    'background:rgba(12,35,63,0.95);backdrop-filter:blur(10px)',
]


def fix_outlier(path):
    with open(path) as f:
        src = f.read()
    new = src
    for pat in SOLID_BG_PATTERNS:
        new = new.replace(pat, '')
    if new == src:
        return f'  {path}: no match (already clean?)'
    with open(path, 'w') as f:
        f.write(new)
    return f'  {path}: stripped solid background ({len(src) - len(new)} bytes removed)'


# ---- services.html fix ----
SVC_LIGHT_NAV_OVERRIDE = (
    '/* ===SVC-LIGHT-NAV-START=== */'
    # On services.html the hero is light, so force navbar contents dark while at top
    '.navbar:not(.scrolled) .nav-link{color:#0C233F}'
    '.navbar:not(.scrolled) .nav-link:hover{color:#44C0C0}'
    '.navbar:not(.scrolled) .nav-cta{background:#0C233F;color:#fff!important}'
    '.navbar:not(.scrolled) .nav-cta:hover{background:#091c33}'
    '.navbar:not(.scrolled) .nav-cta-dot{background:#fff}'
    '.navbar:not(.scrolled) .nav-cta-dot svg{stroke:#0C233F}'
    '/* ===SVC-LIGHT-NAV-END=== */'
)


def fix_services_page():
    path = 'services.html'
    with open(path) as f:
        src = f.read()
    orig = src

    # 1. Revert .page-hero background to light
    src = src.replace(
        '.page-hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:center;background:#0C233F;overflow:hidden;padding:180px 50px 100px',
        '.page-hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:center;background:#EAEAEA;overflow:hidden;padding:180px 50px 100px',
    )
    # 2. Revert .page-hero::before accent back to navy (was teal after my earlier change)
    src = re.sub(
        r'(\.page-hero::before\{[^}]*?background:)#44C0C0',
        r'\1#0C233F',
        src, count=1,
    )
    # 3. Revert .page-hero-title color to navy
    src = re.sub(
        r"(\.page-hero-title\{font-family:'Graphie',sans-serif;font-size:clamp\(38px,5\.5vw,72px\);font-weight:600;line-height:1\.15;color:)#fff",
        r'\1#0C233F',
        src, count=1,
    )
    # 4. Revert .page-hero-intro color to dark
    src = src.replace(
        'color:rgba(234,234,234,0.75)',
        'color:rgba(12,35,63,0.75)',
        1,  # only first occurrence (intro)
    )
    # 5. Switch logo image to dark variant
    src = src.replace(
        'src="images/W13_Logo_White.webp"',
        'src="images/W13_Logo.png"',
    )
    # 6. Inject nav-link colour override (idempotent via markers)
    if '/* ===SVC-LIGHT-NAV-START=== */' in src:
        src = re.sub(
            r'/\* ===SVC-LIGHT-NAV-START=== \*/.*?/\* ===SVC-LIGHT-NAV-END=== \*/',
            SVC_LIGHT_NAV_OVERRIDE, src, count=1, flags=re.DOTALL,
        )
    else:
        # Inject just before the first </style>
        m = re.search(r'</style>', src)
        if m:
            src = src[:m.start()] + SVC_LIGHT_NAV_OVERRIDE + src[m.start():]

    if src == orig:
        print(f'  {path}: NO CHANGE')
        return
    with open(path, 'w') as f:
        f.write(src)
    print(f'  {path}: updated ({len(src) - len(orig):+d} bytes)')


def main():
    print('=== Stripping solid background from 13 outlier .navbar rules ===')
    for p in OUTLIERS:
        print(fix_outlier(p))
    print()
    print('=== services.html: revert hero to light + dark nav override ===')
    fix_services_page()


if __name__ == '__main__':
    main()
