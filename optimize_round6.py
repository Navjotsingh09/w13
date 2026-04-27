#!/usr/bin/env python3
"""Round 6: responsive hero (srcset/sizes) - mobile gets 600w (~32KB) instead of 1200w (~135KB).

1. Update <link rel=preload as=image> for hero with imagesrcset/imagesizes.
2. Update each <img src="images/hero/X.webp"> to include srcset/sizes pointing
   at both the -sm and full versions.
"""
import os, re, glob

# Set of base ids we have -sm variants for
SM_IDS = set()
for f in glob.glob('images/hero/*-sm.webp'):
    SM_IDS.add(os.path.basename(f)[:-8])  # strip "-sm.webp"

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# Match an <img ... src="<prefix>images/hero/<id>.webp" ...>
IMG_RE = re.compile(
    r'<img(?P<pre>[^>]*?)\bsrc="(?P<prefix>(?:\.\./)?)images/hero/(?P<id>[^"./]+)\.webp"(?P<post>[^>]*)>',
    re.I,
)

# Match preload for hero image
PRELOAD_RE = re.compile(
    r'<link rel="preload" as="image" href="(?P<prefix>(?:\.\./)?)images/hero/(?P<id>[^"./]+)\.webp" fetchpriority="high">',
    re.I,
)

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c

    def img_repl(m):
        pid = m.group('id')
        if pid not in SM_IDS:
            return m.group(0)
        pre = m.group('pre'); post = m.group('post'); prefix = m.group('prefix')
        # already has srcset?
        if 'srcset=' in pre or 'srcset=' in post:
            return m.group(0)
        srcset = f'{prefix}images/hero/{pid}-sm.webp 600w, {prefix}images/hero/{pid}.webp 1200w'
        return (
            f'<img{pre}src="{prefix}images/hero/{pid}.webp" '
            f'srcset="{srcset}" sizes="(max-width: 768px) 100vw, 1200px"{post}>'
        )

    c = IMG_RE.sub(img_repl, c)

    def preload_repl(m):
        pid = m.group('id'); prefix = m.group('prefix')
        if pid not in SM_IDS:
            return m.group(0)
        srcset = f'{prefix}images/hero/{pid}-sm.webp 600w, {prefix}images/hero/{pid}.webp 1200w'
        return (
            f'<link rel="preload" as="image" '
            f'href="{prefix}images/hero/{pid}.webp" '
            f'imagesrcset="{srcset}" '
            f'imagesizes="(max-width: 768px) 100vw, 1200px" '
            f'fetchpriority="high">'
        )

    c = PRELOAD_RE.sub(preload_repl, c)

    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
print(f'Updated {count} files')
