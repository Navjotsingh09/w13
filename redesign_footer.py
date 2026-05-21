#!/usr/bin/env python3
"""
Footer redesign script for W13 Group website.
Updates footer CSS and HTML across all 29 pages.
"""
import re
import os
import glob

BASE = '/Users/navjotsinghhundal/W13Uk'

# ── NEW FOOTER CSS (unminified, for shared.css) ────────────────────────────────
NEW_FOOTER_CSS_FORMATTED = """\
/* ===== FOOTER ===== */
.site-footer { background: #091c33; padding: 0; border-top: 3px solid #44C0C0; }
.footer-main { max-width: 1400px; margin: 0 auto; padding: 72px 60px 0; display: grid; grid-template-columns: 240px 1fr 300px; gap: 64px; align-items: start; }
.footer-brand img { height: 48px; width: auto; margin-bottom: 20px; }
.footer-cert { display: inline-block; margin-bottom: 24px; opacity: 0.7; transition: opacity 0.3s; }
.footer-cert:hover { opacity: 1; }
.footer-cert img { height: 44px; width: auto; }
.footer-tagline { font-size: 14px; color: rgba(234,234,234,0.55); line-height: 1.7; max-width: 220px; }
.footer-nav { display: grid; grid-template-columns: 1fr 1fr; gap: 24px 40px; }
.footer-nav-label { font-size: 11px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #44C0C0; margin-bottom: 16px; }
.footer-nav a { display: block; font-family: 'Graphie', sans-serif; font-size: 15px; font-weight: 500; color: rgba(234,234,234,0.65); padding: 10px 0; border-bottom: 1px solid rgba(234,234,234,0.07); transition: all 0.25s; text-decoration: none; }
.footer-nav a:hover { color: #44C0C0; padding-left: 6px; }
.footer-office-label { font-size: 11px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #44C0C0; margin-bottom: 24px; }
.footer-office-addr { font-size: 14px; color: rgba(234,234,234,0.55); line-height: 1.8; margin-bottom: 24px; }
.footer-office-contact { font-size: 14px; margin-bottom: 8px; }
.footer-office-contact a { color: rgba(234,234,234,0.7); text-decoration: none; transition: color 0.3s; }
.footer-office-contact a:hover { color: #44C0C0; }
.footer-social-row { display: flex; gap: 8px; margin-top: 28px; }
.footer-social-icon { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(234,234,234,0.15); border-radius: 6px; color: rgba(234,234,234,0.55); font-size: 14px; text-decoration: none; transition: all 0.25s; }
.footer-social-icon:hover { color: #44C0C0; border-color: #44C0C0; background: rgba(68,192,192,0.1); }
.footer-bottom-bar { max-width: 1400px; margin: 56px auto 0; padding: 22px 60px; border-top: 1px solid rgba(234,234,234,0.08); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }
.footer-legal-links { display: flex; gap: 24px; }
.footer-legal-links a { font-size: 12px; color: rgba(234,234,234,0.45); text-decoration: none; transition: color 0.3s; }
.footer-legal-links a:hover { color: #44C0C0; }
.footer-copy { font-size: 12px; color: rgba(234,234,234,0.4); }
.footer-dot { text-align: center; padding: 32px 0 28px; }
.footer-dot span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #44C0C0; opacity: 0.5; }"""

# Responsive additions (go into the existing @media blocks in shared.css)
FOOTER_1024_CSS = """\
    .footer-main { grid-template-columns: 1fr 1fr; gap: 40px; padding: 60px 40px 0; }
    .footer-office { grid-column: 1 / -1; }"""

FOOTER_768_CSS = """\
    .footer-main { grid-template-columns: 1fr; gap: 40px; padding: 48px 24px 0; }
    .footer-nav { grid-template-columns: 1fr 1fr; }
    .footer-nav a { font-size: 14px; padding: 9px 0; }
    .footer-bottom-bar { padding: 20px 24px; flex-direction: column; align-items: flex-start; }"""

# ── NEW FOOTER CSS (minified, for inline <style> and shared.min.css) ──────────
NEW_FOOTER_CSS_MIN = (
    ".site-footer{background:#091c33;padding:0;border-top:3px solid #44C0C0}"
    ".footer-main{max-width:1400px;margin:0 auto;padding:72px 60px 0;display:grid;grid-template-columns:240px 1fr 300px;gap:64px;align-items:start}"
    ".footer-brand img{height:48px;width:auto;margin-bottom:20px}"
    ".footer-cert{display:inline-block;margin-bottom:24px;opacity:0.7;transition:opacity 0.3s}"
    ".footer-cert:hover{opacity:1}"
    ".footer-cert img{height:44px;width:auto}"
    ".footer-tagline{font-size:14px;color:rgba(234,234,234,0.55);line-height:1.7;max-width:220px}"
    ".footer-nav{display:grid;grid-template-columns:1fr 1fr;gap:24px 40px}"
    ".footer-nav-label{font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#44C0C0;margin-bottom:16px}"
    ".footer-nav a{display:block;font-family:'Graphie',sans-serif;font-size:15px;font-weight:500;color:rgba(234,234,234,0.65);padding:10px 0;border-bottom:1px solid rgba(234,234,234,0.07);transition:all 0.25s;text-decoration:none}"
    ".footer-nav a:hover{color:#44C0C0;padding-left:6px}"
    ".footer-office-label{font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#44C0C0;margin-bottom:24px}"
    ".footer-office-addr{font-size:14px;color:rgba(234,234,234,0.55);line-height:1.8;margin-bottom:24px}"
    ".footer-office-contact{font-size:14px;margin-bottom:8px}"
    ".footer-office-contact a{color:rgba(234,234,234,0.7);text-decoration:none;transition:color 0.3s}"
    ".footer-office-contact a:hover{color:#44C0C0}"
    ".footer-social-row{display:flex;gap:8px;margin-top:28px}"
    ".footer-social-icon{width:40px;height:40px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(234,234,234,0.15);border-radius:6px;color:rgba(234,234,234,0.55);font-size:14px;text-decoration:none;transition:all 0.25s}"
    ".footer-social-icon:hover{color:#44C0C0;border-color:#44C0C0;background:rgba(68,192,192,0.1)}"
    ".footer-bottom-bar{max-width:1400px;margin:56px auto 0;padding:22px 60px;border-top:1px solid rgba(234,234,234,0.08);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}"
    ".footer-legal-links{display:flex;gap:24px}"
    ".footer-legal-links a{font-size:12px;color:rgba(234,234,234,0.45);text-decoration:none;transition:color 0.3s}"
    ".footer-legal-links a:hover{color:#44C0C0}"
    ".footer-copy{font-size:12px;color:rgba(234,234,234,0.4)}"
    ".footer-dot{text-align:center;padding:32px 0 28px}"
    ".footer-dot span{display:inline-block;width:8px;height:8px;border-radius:50%;background:#44C0C0;opacity:0.5}"
    "@media (max-width:1024px){.footer-main{grid-template-columns:1fr 1fr;gap:40px;padding:60px 40px 0}.footer-office{grid-column:1/-1}}"
    "@media (max-width:768px){.footer-main{grid-template-columns:1fr;gap:40px;padding:48px 24px 0}.footer-nav{grid-template-columns:1fr 1fr}.footer-nav a{font-size:14px;padding:9px 0}.footer-bottom-bar{padding:20px 24px;flex-direction:column;align-items:flex-start}}"
)

# ── FOOTER HTML TEMPLATES ─────────────────────────────────────────────────────
def make_footer_nav(prefix=''):
    """Generate footer-nav HTML with the given path prefix ('' or '../')."""
    p = prefix
    return (
        '            <div class="footer-nav">\n'
        '                <div class="footer-nav-col">\n'
        '                    <div class="footer-nav-label">Company</div>\n'
        f'                    <a href="{p}about.html">About Us</a>\n'
        f'                    <a href="{p}careers.html">Careers</a>\n'
        f'                    <a href="{p}news.html">News</a>\n'
        f'                    <a href="{p}contact.html">Contact</a>\n'
        '                </div>\n'
        '                <div class="footer-nav-col">\n'
        '                    <div class="footer-nav-label">What We Do</div>\n'
        f'                    <a href="{p}services.html">Services</a>\n'
        f'                    <a href="{p}projects.html">Projects</a>\n'
        f'                    <a href="{p}sectors/residential.html">Sectors</a>\n'
        '                </div>\n'
        '            </div>'
    )

FOOTER_DOT_HTML = '        <div class="footer-dot"><span></span></div>\n    </footer>'

# ── 1. UPDATE shared.css ──────────────────────────────────────────────────────
def update_shared_css():
    path = os.path.join(BASE, 'shared.css')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace footer section (from marker to .footer-copy line)
    old_footer = re.search(
        r'/\* ===== FOOTER ===== \*/.*?\.footer-copy \{ font-size: 12px; color: rgba\(234,234,234,0\.25\); \}',
        content, re.DOTALL
    )
    if old_footer:
        content = content[:old_footer.start()] + NEW_FOOTER_CSS_FORMATTED + content[old_footer.end():]
        print('  shared.css: footer section replaced')
    else:
        print('  shared.css: WARNING - footer section not found')

    # Update responsive blocks
    # 1024px: replace footer rules
    content = re.sub(
        r'(\.footer-main \{ grid-template-columns: 1fr 1fr; gap: 40px; padding: 0 40px; \}\s*\.footer-office \{ grid-column: 1 / -1; \})',
        FOOTER_1024_CSS,
        content
    )
    # 768px: replace footer rules
    content = re.sub(
        r'\.footer-main \{ grid-template-columns: 1fr; gap: 40px; padding: 0 24px; \}\s*\.footer-nav \{ grid-template-columns: 1fr 1fr; \}\s*\.footer-nav a \{ font-size: 17px; padding: 14px 0; \}\s*\.footer-bottom-bar \{ padding: 20px 24px; flex-direction: column; align-items: flex-start; \}',
        FOOTER_768_CSS,
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  shared.css: saved')

# ── 2. UPDATE shared.min.css ──────────────────────────────────────────────────
def update_shared_min_css():
    path = os.path.join(BASE, 'shared.min.css')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace from .site-footer{ to end of footer responsive block
    pattern = re.compile(
        r'\.site-footer\{background:#091c33;padding:80px 0 0\}.*?'
        r'\.footer-bottom-bar\{padding:20px 24px;flex-direction:column;align-items:flex-start\}\}',
        re.DOTALL
    )
    new_content, n = pattern.subn(NEW_FOOTER_CSS_MIN, content)
    if n:
        print(f'  shared.min.css: replaced {n} footer block(s)')
    else:
        print('  shared.min.css: WARNING - footer block not found, appending')
        # fallback: append before end
        new_content = content.rstrip() + NEW_FOOTER_CSS_MIN

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('  shared.min.css: saved')

# ── 3. UPDATE ALL HTML FILES ──────────────────────────────────────────────────
def is_subdir_file(filepath):
    """Returns True if the file is in sectors/ or services/ subdirectory."""
    rel = os.path.relpath(filepath, BASE)
    return rel.startswith('sectors/') or rel.startswith('services/')

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    prefix = '../' if is_subdir_file(filepath) else ''
    changed = []

    # ── 3a. Update inline footer CSS ─────────────────────────────────────────
    css_pattern = re.compile(
        r'\.site-footer\{background:#091c33;padding:80px 0 0\}.*?'
        r'\.footer-bottom-bar\{padding:20px 24px;flex-direction:column;align-items:flex-start\}\}',
        re.DOTALL
    )
    content, n = css_pattern.subn(NEW_FOOTER_CSS_MIN, content)
    if n:
        changed.append(f'inline CSS ({n})')

    # ── 3b. Replace footer-nav HTML ───────────────────────────────────────────
    nav_pattern = re.compile(
        r'<div class="footer-nav">.*?</div>(?=\s*<div class="footer-office">)',
        re.DOTALL
    )
    new_nav = make_footer_nav(prefix)
    content, n = nav_pattern.subn(new_nav, content)
    if n:
        changed.append('footer-nav HTML')

    # ── 3c. Add footer-dot before </footer> ──────────────────────────────────
    if 'class="footer-dot"' not in content:
        content = content.replace('        </div>\n    </footer>', FOOTER_DOT_HTML, 1)
        if FOOTER_DOT_HTML in content:
            changed.append('footer-dot added')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  {os.path.relpath(filepath, BASE)}: {", ".join(changed)}')
    else:
        print(f'  {os.path.relpath(filepath, BASE)}: no changes needed')

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('=== Step 1: Update shared.css ===')
    update_shared_css()

    print('\n=== Step 2: Update shared.min.css ===')
    update_shared_min_css()

    print('\n=== Step 3: Update HTML files ===')
    html_files = (
        glob.glob(os.path.join(BASE, '*.html')) +
        glob.glob(os.path.join(BASE, 'sectors', '*.html')) +
        glob.glob(os.path.join(BASE, 'services', '*.html'))
    )
    # Skip backup files
    html_files = [f for f in html_files if '.backup' not in f]
    for f in sorted(html_files):
        update_html_file(f)

    print(f'\nDone. Processed {len(html_files)} HTML files.')
