#!/usr/bin/env python3
"""Round 8: kill the LCP-blocking preloader.

The preloader is a full-screen #0C233F div with z-index 100000.
It hides until window.load + 400ms + GSAP 600ms fade.
Mobile LCP can't register the hero image until preloader fades out.

Fix: hide preloader immediately on DOMContentLoaded (instead of window.load
+ setTimeout + GSAP fade), and call initAll() right away.
"""
import os, re

OLD = """window.addEventListener('load', () => {
    setTimeout(() => {
        const preloader = document.getElementById('preloader');
        gsap.to(preloader, {
            opacity: 0, duration: 0.6, ease: 'power2.inOut',
            onComplete: () => {
                preloader.style.display = 'none';
                initAll();
            }
        });
    }, 400);
});"""

NEW = """function _w13Init() {
    var p = document.getElementById('preloader');
    if (p) p.style.display = 'none';
    if (typeof initAll === 'function') initAll();
}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _w13Init);
} else {
    _w13Init();
}"""

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1', './node_modules', './.git', './.venv']):
        continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

count = 0
for p in paths:
    with open(p) as fh:
        c = fh.read()
    o = c
    if OLD in c:
        c = c.replace(OLD, NEW)
    if c != o:
        with open(p, 'w') as fh:
            fh.write(c)
        count += 1
print(f'Patched {count} files')
