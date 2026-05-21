#!/usr/bin/env python3
"""Normalize the footer-nav block across every page."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FOOTER_NAV_TEMPLATE = '''<div class="footer-nav">
                <a href="{P}about.html">About Us</a>
                <a href="{P}services.html">Services</a>
                <a href="{P}services.html">What We Do</a>
                <a href="{P}projects.html">Projects</a>
                <a href="{P}careers.html">Careers</a>
                <a href="{P}news.html">News</a>
                <a href="{P}contact.html">Contact</a>
            </div>'''

# Capture the entire <div class="footer-nav"> ... </div> block (one level).
FOOTER_NAV_RE = re.compile(r'<div class="footer-nav">.*?</div>', re.DOTALL)

def prefix_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return '../' * depth

def migrate(path: Path):
    src = path.read_text(encoding='utf-8')
    p = prefix_for(path)
    new_block = FOOTER_NAV_TEMPLATE.replace('{P}', p)
    if not FOOTER_NAV_RE.search(src):
        return False, 'no footer-nav block'
    out = FOOTER_NAV_RE.sub(lambda m: new_block, src, count=1)
    if out == src:
        return False, 'no change'
    path.write_text(out, encoding='utf-8')
    return True, 'updated'

def main():
    targets = []
    for p in ROOT.glob('*.html'):
        if p.name.endswith('.backup') or 'wireframes' in p.name:
            continue
        targets.append(p)
    for sub in ('sectors', 'services'):
        for p in (ROOT / sub).glob('*.html'):
            if p.name.endswith('.backup'):
                continue
            targets.append(p)

    updated = 0
    for path in sorted(targets):
        ok, msg = migrate(path)
        if ok:
            updated += 1
        print(f"  [{'OK' if ok else '--'}] {path.relative_to(ROOT)}: {msg}")
    print(f'\nUpdated {updated}/{len(targets)}')

if __name__ == '__main__':
    main()
