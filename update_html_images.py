#!/usr/bin/env python3
"""Update HTML files to use optimized .webp images and fix broken 1.jpg refs."""
import os
import re

# Map missing "1.jpg" to existing representative images (.webp)
MISSING_1_MAP = {
    'hilston-park/1.jpg': 'hilston-park/render-1.webp',
    'oldbury-gurdwara/1.jpg': 'oldbury-gurdwara/renders.webp',
    'pear-tree-lane/1.jpg': 'pear-tree-lane/render-1.webp',
    'showell-lane/1.jpg': 'showell-lane/render-1.webp',
    'thornley-street/1.jpg': 'thornley-street/ground-floor.webp',
    'walsall-road/1.jpg': 'walsall-road/render-1.webp',
    'willenhall-gurdwara/1.jpg': 'willenhall-gurdwara/photo-1.webp',
}

# Find all html files (excluding backups, home1, node_modules)
html_files = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            html_files.append(os.path.join(root, f))

total_changes = 0
for path in html_files:
    with open(path) as fh:
        content = fh.read()
    original = content

    # Step 1: remap broken 1.jpg paths to real images
    for bad, good in MISSING_1_MAP.items():
        content = content.replace('images/projects/' + bad, 'images/projects/' + good)

    # Step 2: convert all images/projects/*.jpg|png references to .webp
    # Match src="...images/projects/foo/bar.jpg" or .png — preserve any ../ prefix
    def to_webp(m):
        return m.group(1) + '.webp'
    content = re.sub(
        r'((?:\.\./)?images/projects/[a-z0-9\-/]+)\.(?:jpg|jpeg|png)',
        to_webp,
        content,
        flags=re.IGNORECASE,
    )

    if content != original:
        with open(path, 'w') as fh:
            fh.write(content)
        # Count differences
        diff = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
        total_changes += diff
        print(f'Updated: {path} ({diff} lines changed)')

print(f'\nTotal lines changed: {total_changes}')
