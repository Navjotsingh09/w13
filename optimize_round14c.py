"""Round 14c: balanced-brace replacement of broken preloader IIFE."""
import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1','./node_modules','./.git','./.venv']): continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

NEW = """/* ===== INIT TRIGGER ===== */
function _w13Init(){if(typeof initAll==='function'){if('requestIdleCallback' in window){requestIdleCallback(initAll,{timeout:1500});}else{setTimeout(initAll,1);}}}
if(document.readyState==='complete'){_w13Init();}else{window.addEventListener('load',_w13Init);}
"""

count = 0
for p in paths:
    c = open(p).read()
    # Find PRELOADER comment + window.addEventListener('load'
    m = re.search(r"/\*\s*=+\s*PRELOADER\s*=+\s*\*/\s*\n\s*window\.addEventListener\(\s*['\"]load['\"]\s*,", c)
    if not m:
        continue
    # Walk forward from start of window.addEventListener( to find matching closing );
    start = m.start()
    # Locate the opening "(" of addEventListener
    open_paren = c.find('(', m.end() - 2)  # after "addEventListener"
    # Use depth counter
    i = open_paren
    depth = 0
    while i < len(c):
        ch = c[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                # Expect ; after
                end = i + 1
                if end < len(c) and c[end] == ';':
                    end += 1
                # consume trailing newline
                if end < len(c) and c[end] == '\n':
                    end += 1
                new_c = c[:start] + NEW + c[end:]
                open(p, 'w').write(new_c)
                count += 1
                break
        i += 1
print('Patched ' + str(count) + ' files')

# Verify
remaining = []
for p in paths:
    c = open(p).read()
    if "gsap.to(preloader" in c or "gsap.to(document.getElementById('preloader')" in c:
        remaining.append(p)
print('Files still calling gsap.to on preloader:', len(remaining))
for r in remaining:
    print(' -', r)
