#!/usr/bin/env python3
"""Add a static 'Cookie Policy' link to the footer legal links on every page.
Handles both root pages and subdirectory pages (../ prefix). The Cookie
Settings control is added dynamically by shared.js."""
import glob

ROOT_OLD = '                <a href="privacy-policy.html">Privacy Policy</a>\n'
ROOT_NEW = ('                <a href="privacy-policy.html">Privacy Policy</a>\n'
            '                <a href="cookie-policy.html">Cookie Policy</a>\n')

SUB_OLD = '                <a href="../privacy-policy.html">Privacy Policy</a>\n'
SUB_NEW = ('                <a href="../privacy-policy.html">Privacy Policy</a>\n'
           '                <a href="../cookie-policy.html">Cookie Policy</a>\n')

files = []
for pattern in ("*.html", "services/*.html", "sectors/*.html"):
    files.extend(glob.glob(pattern))

changed = 0
for f in sorted(set(files)):
    if f.endswith(".backup"):
        continue
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    orig = content
    if 'cookie-policy.html">Cookie Policy' in content:
        continue  # already has it
    if SUB_OLD in content:
        content = content.replace(SUB_OLD, SUB_NEW)
    elif ROOT_OLD in content:
        content = content.replace(ROOT_OLD, ROOT_NEW)
    if content != orig:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(content)
        changed += 1
        print(f"updated: {f}")

print(f"\nTotal files updated: {changed}")
