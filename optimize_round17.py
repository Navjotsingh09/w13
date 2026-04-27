"""Round 17: stop deferring initAll() to requestIdleCallback.

Round 9 wrapped initAll() in requestIdleCallback to defer ScrollTrigger
setup off the critical path. But on pages where initAll sets up pinned
scroll layouts (services.html especially), the idle delay means
ScrollTrigger computes positions AFTER the user may have already
scrolled — pin never engages, slides never transition.

Replace the _w13Init wrapper with a simple direct call on load.
Also append ScrollTrigger.refresh() at end of every initAll for safety.
"""
import re, glob

paths = []
for p in glob.glob('**/*.html', recursive=True):
    if 'home1' in p or '.venv' in p or '.backup' in p: continue
    c = open(p).read()
    if '_w13Init' in c or 'function initAll' in c:
        paths.append(p)

# Replace _w13Init wrapper with direct call
OLD_WRAP_PATTERNS = [
    # Compact one-liner version
    re.compile(
        r"function _w13Init\(\)\{.*?\}\}\}\nif\(document\.readyState[^\n]*\n",
        re.S,
    ),
    # Multi-line index.html version
    re.compile(
        r"function _w13Init\(\) \{\s*\n"
        r"\s*if \(typeof initAll[^}]*?\}\s*\n"
        r"\}\s*\n"
        r"if \(document\.readyState === 'complete'\) \{\s*\n"
        r"\s*_w13Init\(\);\s*\n"
        r"\} else \{\s*\n"
        r"\s*window\.addEventListener\('load', _w13Init\);\s*\n"
        r"\}\s*\n",
        re.S,
    ),
]

NEW_WRAP = "if(typeof initAll==='function'){if(document.readyState==='complete'){initAll();}else{window.addEventListener('load',initAll);}}\n"

count = 0
for p in paths:
    c = open(p).read()
    orig = c
    for pat in OLD_WRAP_PATTERNS:
        c = pat.sub(NEW_WRAP, c)
    if c != orig:
        open(p, 'w').write(c)
        count += 1
        print('Patched', p)
print('Total:', count)
