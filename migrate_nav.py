#!/usr/bin/env python3
"""Roll out the new W13 navbar to every HTML page."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Canonical nav block using {P} as the prefix placeholder (replaced per-file).
NAV_TEMPLATE = '''<!-- NAVBAR -->
<nav class="navbar" id="navbar" aria-label="Main navigation">
    <div class="nav-inner">
    <a href="{P}index.html" class="nav-logo">
        <img loading="eager" fetchpriority="high" width="180" height="40" src="{P}images/W13_Logo_White.webp" alt="W13 Group">
    </a>
    <div class="nav-center">
        <!-- ABOUT US -->
        <div class="nav-dropdown">
            <a href="{P}about.html" class="nav-link">About Us</a>
            <div class="mega-menu">
                <div class="mega-menu-content">
                    <div class="mega-menu-intro">
                        <h2 class="mega-menu-title">About Us</h2>
                        <p class="mega-menu-desc">With over 20 years of experience, W13 Group has established itself as a leader in property development &amp; construction, delivering landmark projects across the UK.</p>
                    </div>
                    <div class="mega-menu-links mega-menu-links--compact">
                        <a href="{P}about.html#history" class="mega-menu-link" data-sector="about-history">Company History</a>
                        <a href="{P}about.html#mission" class="mega-menu-link" data-sector="about-mission">Mission &amp; Ethos</a>
                        <a href="{P}about.html#sustainability" class="mega-menu-link" data-sector="about-sustain">Sustainability</a>
                        <a href="{P}about.html#csr" class="mega-menu-link" data-sector="about-csr">Corporate Social Responsibility</a>
                        <a href="{P}about.html#partners" class="mega-menu-link" data-sector="about-partners">Who We Work With</a>
                        <a href="{P}careers.html" class="mega-menu-link" data-sector="about-careers">Careers</a>
                    </div>
                    <div class="mega-menu-image">
                        <div class="mega-menu-image-container active" data-sector="about-history"><img loading="lazy" src="{P}images/W13 - Pictures/about-us-our-story.webp" alt="Company History"></div>
                        <div class="mega-menu-image-container" data-sector="about-mission"><img loading="lazy" src="{P}images/hero/1504307651254-35680f356dfd.webp" alt="Mission and Ethos"></div>
                        <div class="mega-menu-image-container" data-sector="about-sustain"><img loading="lazy" src="{P}images/hero/1565610222536-ef125c59da2e.webp" alt="Sustainability"></div>
                        <div class="mega-menu-image-container" data-sector="about-csr"><img loading="lazy" src="{P}images/hero/1449157291145-7efd050a4d0e.webp" alt="Corporate Social Responsibility"></div>
                        <div class="mega-menu-image-container" data-sector="about-partners"><img loading="lazy" src="{P}images/hero/1486406146926-c627a92ad1ab.webp" alt="Who We Work With"></div>
                        <div class="mega-menu-image-container" data-sector="about-careers"><img loading="lazy" src="{P}images/hero/1517089596392-fb9a9033e05b.webp" alt="Careers"></div>
                    </div>
                </div>
            </div>
        </div>
        <!-- SERVICES -->
        <div class="nav-dropdown">
            <a href="{P}services.html" class="nav-link">Services</a>
            <div class="mega-menu">
                <div class="mega-menu-content">
                    <div class="mega-menu-intro mega-menu-intro--services">
                        <h2 class="mega-menu-title">Services</h2>
                        <p class="mega-menu-desc">End to end property development, from initial consultancy through to construction handover.</p>
                        <div class="lifecycle-mini" aria-label="Project lifecycle: four stages">
                            <div class="lifecycle-mini-step"><div class="lifecycle-mini-dot">1</div><div class="lifecycle-mini-label">Consultancy</div></div>
                            <div class="lifecycle-mini-bar"></div>
                            <div class="lifecycle-mini-step"><div class="lifecycle-mini-dot">2</div><div class="lifecycle-mini-label">Land</div></div>
                            <div class="lifecycle-mini-bar"></div>
                            <div class="lifecycle-mini-step"><div class="lifecycle-mini-dot">3</div><div class="lifecycle-mini-label">Planning</div></div>
                            <div class="lifecycle-mini-bar"></div>
                            <div class="lifecycle-mini-step"><div class="lifecycle-mini-dot">4</div><div class="lifecycle-mini-label">Build</div></div>
                        </div>
                    </div>
                    <div class="mega-menu-links">
                        <a href="{P}services/consultancy.html" class="mega-menu-link" data-sector="svc-consult">Consultancy</a>
                        <a href="{P}services/land-development.html" class="mega-menu-link" data-sector="svc-land">Land Acquisitions</a>
                        <a href="{P}services/architecture-design.html" class="mega-menu-link" data-sector="svc-arch">Architecture &amp; Planning</a>
                        <a href="{P}services/master-developer.html" class="mega-menu-link" data-sector="svc-construct">Construction / Main Contractor</a>
                    </div>
                    <div class="mega-menu-image">
                        <div class="mega-menu-image-container active" data-sector="svc-consult"><img loading="lazy" src="{P}images/hero/1504307651254-35680f356dfd.webp" alt="Consultancy"></div>
                        <div class="mega-menu-image-container" data-sector="svc-land"><img loading="lazy" src="{P}images/hero/1600585154340-be6161a56a0c.webp" alt="Land Acquisitions"></div>
                        <div class="mega-menu-image-container" data-sector="svc-arch"><img loading="lazy" src="{P}images/hero/1503387762-592deb58ef4e.webp" alt="Architecture and Planning"></div>
                        <div class="mega-menu-image-container" data-sector="svc-construct"><img loading="lazy" src="{P}images/hero/1541888946425-d81bb19240f5.webp" alt="Construction"></div>
                    </div>
                </div>
            </div>
        </div>
        <!-- WHAT WE DO -->
        <div class="nav-dropdown">
            <a href="{P}services.html" class="nav-link">What We Do</a>
            <div class="mega-menu">
                <div class="mega-menu-content">
                    <div class="mega-menu-intro">
                        <h2 class="mega-menu-title">What We Do</h2>
                        <p class="mega-menu-desc">Specialists in complex land led development across brownfield regeneration, environmental projects, build to rent, and social housing.</p>
                    </div>
                    <div class="mega-menu-links">
                        <a href="{P}sectors/urban-regeneration.html" class="mega-menu-link" data-sector="brownfield">Brownfield Regeneration</a>
                        <a href="{P}sectors/urban-regeneration.html" class="mega-menu-link" data-sector="environmental">Environmental</a>
                        <a href="{P}sectors/residential.html" class="mega-menu-link" data-sector="btr">Build to Rent (BTR)</a>
                        <a href="{P}sectors/residential.html" class="mega-menu-link" data-sector="social">Social Housing</a>
                    </div>
                    <div class="mega-menu-image">
                        <div class="mega-menu-image-container active" data-sector="brownfield"><img loading="lazy" src="{P}images/hero/1600585154526-990dced4db0d.webp" alt="Brownfield Regeneration"></div>
                        <div class="mega-menu-image-container" data-sector="environmental"><img loading="lazy" src="{P}images/hero/1565610222536-ef125c59da2e.webp" alt="Environmental"></div>
                        <div class="mega-menu-image-container" data-sector="btr"><img loading="lazy" src="{P}images/W13 - Pictures/residential-main.webp" alt="Build to Rent"></div>
                        <div class="mega-menu-image-container" data-sector="social"><img loading="lazy" src="{P}images/hero/1600596542815-ffad4c1539a9.webp" alt="Social Housing"></div>
                    </div>
                </div>
            </div>
        </div>
        <!-- PROJECTS -->
        <div class="nav-dropdown">
            <a href="{P}projects.html" class="nav-link">Projects</a>
            <div class="mega-menu">
                <div class="mega-menu-content mega-menu-content--compact">
                    <div class="mega-menu-intro">
                        <h2 class="mega-menu-title">Projects</h2>
                        <p class="mega-menu-desc">Explore our portfolio of delivered commercial and residential developments across the UK.</p>
                    </div>
                    <div class="mega-menu-links">
                        <a href="{P}projects.html#commercial" class="mega-menu-link" data-sector="proj-commercial">Commercial</a>
                        <a href="{P}projects.html#residential" class="mega-menu-link" data-sector="proj-residential">Residential / New Builds</a>
                    </div>
                    <div class="mega-menu-image">
                        <div class="mega-menu-image-container active" data-sector="proj-commercial"><img loading="lazy" src="{P}images/hero/1486406146926-c627a92ad1ab.webp" alt="Commercial Projects"></div>
                        <div class="mega-menu-image-container" data-sector="proj-residential"><img loading="lazy" src="{P}images/hero/1565610222536-ef125c59da2e.webp" alt="Residential Projects"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mobile-menu-btn" aria-label="Open menu" aria-expanded="false" onclick="toggleMenu()">
            <span>Menu</span>
            <div class="mobile-menu-lines">
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    <a href="{P}contact.html" class="nav-cta">Contact <span class="nav-cta-dot"><svg viewBox="0 0 16 16" fill="none"><circle cx="4" cy="4" r="1.5" fill="#fff"/><circle cx="8" cy="4" r="1.5" fill="#fff"/><circle cx="12" cy="4" r="1.5" fill="#fff"/><circle cx="4" cy="8" r="1.5" fill="#fff"/><circle cx="8" cy="8" r="1.5" fill="#fff"/><circle cx="12" cy="8" r="1.5" fill="#fff"/><circle cx="4" cy="12" r="1.5" fill="#fff"/><circle cx="8" cy="12" r="1.5" fill="#fff"/><circle cx="12" cy="12" r="1.5" fill="#fff"/></svg></span></a>
    </div>
</nav>'''

NAV_RE = re.compile(r'<!--\s*NAVBAR\s*-->\s*<nav class="navbar[^"]*".*?</nav>', re.DOTALL | re.IGNORECASE)
NAV_RE_NOCMT = re.compile(r'<nav class="navbar[^"]*".*?</nav>', re.DOTALL | re.IGNORECASE)
SHARED_JS_TAG = '<script src="{P}shared.js" defer></script>'
SHARED_JS_RE = re.compile(r'<script[^>]+src="(?:\.\./)*shared\.js"', re.IGNORECASE)

def prefix_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return '../' * depth

def migrate(path: Path) -> tuple[bool, str]:
    src = path.read_text(encoding='utf-8')
    p = prefix_for(path)
    new_nav = NAV_TEMPLATE.replace('{P}', p)

    # Replace nav block
    if NAV_RE.search(src):
        out = NAV_RE.sub(lambda m: new_nav, src, count=1)
    elif NAV_RE_NOCMT.search(src):
        out = NAV_RE_NOCMT.sub(lambda m: new_nav, src, count=1)
    else:
        return False, 'no <nav class="navbar"> block found'

    # Add shared.js if not present
    if not SHARED_JS_RE.search(out):
        tag = SHARED_JS_TAG.replace('{P}', p)
        if '</body>' in out:
            out = out.replace('</body>', f'    {tag}\n</body>', 1)
        else:
            out = out + f'\n{tag}\n'

    if out == src:
        return False, 'no change'
    path.write_text(out, encoding='utf-8')
    return True, 'updated'


def main():
    # Collect all HTML pages except backups and the wireframes file
    targets = []
    for p in ROOT.glob('*.html'):
        if p.name.endswith('.backup') or 'wireframes' in p.name:
            continue
        targets.append(p)
    for p in (ROOT / 'sectors').glob('*.html'):
        if p.name.endswith('.backup'):
            continue
        targets.append(p)
    for p in (ROOT / 'services').glob('*.html'):
        if p.name.endswith('.backup'):
            continue
        targets.append(p)

    print(f'Found {len(targets)} HTML files to process')
    updated = 0
    skipped = 0
    for path in sorted(targets):
        ok, msg = migrate(path)
        marker = 'OK' if ok else '--'
        rel = path.relative_to(ROOT)
        print(f'  [{marker}] {rel}: {msg}')
        if ok:
            updated += 1
        else:
            skipped += 1
    print(f'\nDone. Updated: {updated}, Skipped: {skipped}')

if __name__ == '__main__':
    main()
