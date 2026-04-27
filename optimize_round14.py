"""Round 14: fix initAll never running on subpages.

Round 8 removed the preloader div from all pages, but only patched
index.html's preloader-fade JS. Other pages still call
gsap.to(document.getElementById('preloader'), ...) which throws because
the element is gone, so initAll() never fires and reveal-up elements
stay invisible (opacity:0).

Replace any block matching:
  window.addEventListener('load', () => {
      setTimeout(() => {
          const preloader = document.getElementById('preloader');
          gsap.to(preloader, { ... onComplete: () => { ...; initAll(); } });
      }, N);
  });
with the safe version that just calls initAll() when ready.
"""
import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1','./node_modules','./.git','./.venv']): continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# Match the preloader-fade pattern (greedy across multi-line)
PATTERN = re.compile(
    r"window\.addEventListener\(\s*['\"]load['\"]\s*,\s*"
    r"(?:function\s*\(\s*\)|\(\s*\)\s*=>)\s*\{\s*"
    r"setTimeout\(\s*"
    r"(?:function\s*\(\s*\)|\(\s*\)\s*=>)\s*\{\s*"
    r"(?:const|var|let)\s+preloader\s*=\s*document\.getElementById\(\s*['\"]preloader['\"]\s*\)\s*;\s*"
    r"gsap\.to\([^;]*?initAll\(\)[^;]*?\}\s*\)\s*;\s*"
    r"\}\s*,\s*\d+\s*\)\s*;\s*"
    r"\}\s*\)\s*;",
    re.S,
)

NEW = """function _w13Init(){if(typeof initAll!=='function')return;if('requestIdleCallback' in window){requestIdleCallback(initAll,{timeout:1500});}else{setTimeout(initAll,1);}}
if(document.readyState==='complete'){_w13Init();}else{window.addEventListener('load',_w13Init);}"""

count = 0
for p in paths:
    c = open(p).read()
    o = c
    c = PATTERN.sub(NEW, c)
    if c != o:
        open(p, 'w').write(c)
        count += 1
print('Patched ' + str(count) + ' files')

# Sanity: any remaining gsap.to with preloader?
remaining = []
for p in paths:
    c = open(p).read()
    if re.search(r"gsap\.to\(\s*preloader", c) or re.search(r"getElementById\(\s*['\"]preloader['\"]\s*\)", c):
        remaining.append(p)
print('Files still referencing preloader:', len(remaining))
for r in remaining:
    print(' -', r)
