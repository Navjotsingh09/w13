"""Round 14b: rewrite ALL preloader blocks across all subpages.

Pages with broken initAll() call:
  about.html, contact.html, services.html, sectors/*, project-*, 404.html, projects.html

Approach: find the line `/* ===== PRELOADER ===== */` and replace from that
line through the next blank line OR end of `});` block with the safe init.
Then ensure initAll() is called when ready.
"""
import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1','./node_modules','./.git','./.venv']): continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

NEW = """/* ===== INIT TRIGGER ===== */
function _w13Init(){if(typeof initAll==='function'){if('requestIdleCallback' in window){requestIdleCallback(initAll,{timeout:1500});}else{setTimeout(initAll,1);}}}
if(document.readyState==='complete'){_w13Init();}else{window.addEventListener('load',_w13Init);}"""

# Match comment marker + the entire window.addEventListener('load', ...); block
# Use balanced approach: find marker, then find next `});` followed by blank/comment.
# Simpler: regex to capture from the comment to first `});\n` after a setTimeout.
PATTERN = re.compile(
    r"/\*\s*=+\s*PRELOADER\s*=+\s*\*/\s*\n"
    r"\s*window\.addEventListener\([^;]*?\}\s*\)\s*;\s*\n",
    re.S,
)

count = 0
for p in paths:
    c = open(p).read()
    o = c
    c = PATTERN.sub(NEW + '\n', c)
    if c != o:
        open(p, 'w').write(c)
        count += 1
print('Patched ' + str(count) + ' files')

# Verify no broken refs remain
remaining = []
for p in paths:
    c = open(p).read()
    if "gsap.to(preloader" in c or "gsap.to(document.getElementById('preloader')" in c:
        remaining.append(p)
print('Files still calling gsap.to on preloader:', len(remaining))
for r in remaining:
    print(' -', r)
