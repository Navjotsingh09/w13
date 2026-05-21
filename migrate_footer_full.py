#!/usr/bin/env python3
"""Replace the entire <footer class="site-footer">...</footer> block on every
HTML page with the canonical version from index.html, adjusting relative paths
for files in sub-directories (sectors/, services/)."""
import re
import glob
import os

CANONICAL = '''<footer class="site-footer">
        <div class="footer-main">
            <div class="footer-brand">
                <img src="{P}images/W13_Logo_full_White.webp" alt="W13 Group" loading="lazy" width="200" height="100" decoding="async">
                <a href="{P}contact.html" class="footer-cert" title="Cyber Essentials Certified">
                    <img src="{P}images/ncsc-cyber-essentials.svg" alt="NCSC Cyber Essentials" loading="lazy" width="150" height="38" decoding="async">
                </a>
                <p class="footer-tagline">Building communities, creating value, and delivering excellence across property development.</p>
            </div>
            <div class="footer-nav">
                <a href="{P}about.html">About Us</a>
                <a href="{P}services.html">Services</a>
                <a href="{P}services.html">What We Do</a>
                <a href="{P}projects.html">Projects</a>
                <a href="{P}careers.html">Careers</a>
                <a href="{P}news.html">News</a>
                <a href="{P}contact.html">Contact</a>
            </div>
            <div class="footer-office">
                <div class="footer-office-label">Birmingham Office</div>
                <div class="footer-office-addr">Beech House, Greenfield Crescent<br>Birmingham, B15 3BE</div>
                <div class="footer-office-contact"><a href="tel:+441216630006">+44 (0)121 663 0006</a></div>
                <div class="footer-office-contact"><a href="mailto:info@w13uk.com">info@w13uk.com</a></div>
                <div class="footer-social-row">
                    <a href="https://www.linkedin.com/company/w13-group/" target="_blank" rel="noopener" class="footer-social-icon" aria-label="Visit W13 Group on LinkedIn"><i class="fab fa-linkedin-in" aria-hidden="true"></i></a>
                    <a href="https://x.com/W13Group" target="_blank" rel="noopener" class="footer-social-icon" aria-label="Visit W13 Group on X"><i class="fab fa-x-twitter" aria-hidden="true"></i></a>
                    <a href="https://www.instagram.com/w13group/" target="_blank" rel="noopener" class="footer-social-icon" aria-label="Visit W13 Group on Instagram"><i class="fab fa-instagram" aria-hidden="true"></i></a>
                </div>
            </div>
        </div>
        <div class="footer-bottom-bar">
            <div class="footer-legal-links">
                <a href="{P}terms.html">T&amp;C's</a>
                <a href="{P}privacy-policy.html">Privacy Policy</a>
            </div>
            <span class="footer-copy">&copy;2026 W13 Group. All rights reserved</span>
        </div>
    </footer>'''

FOOTER_RE = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)

files = sorted(
    [f for f in glob.glob('*.html') + glob.glob('sectors/*.html') + glob.glob('services/*.html')
     if 'backup' not in f and 'wireframes' not in f]
)

updated = 0
for f in files:
    depth = f.count('/')
    prefix = '../' * depth
    new_footer = CANONICAL.replace('{P}', prefix)
    src = open(f).read()
    if not FOOTER_RE.search(src):
        print(f'[SKIP] {f}: no <footer class="site-footer"> block')
        continue
    new_src = FOOTER_RE.sub(lambda m: new_footer, src, count=1)
    if new_src != src:
        open(f, 'w').write(new_src)
        updated += 1
        print(f'[OK]   {f}')
    else:
        print(f'[==]   {f}: already canonical')

print(f'\nUpdated {updated}/{len(files)}')
