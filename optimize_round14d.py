"""Round 14d: parse with string-aware brace counter."""
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

def find_matching_close(s, open_idx):
    """Given index of '(' in s, return index of matching ')' tracking strings."""
    depth = 0
    i = open_idx
    n = len(s)
    while i < n:
        ch = s[i]
        if ch in ("'", '"', '`'):
            quote = ch
            i += 1
            while i < n:
                if s[i] == '\\':
                    i += 2
                    continue
                if s[i] == quote:
                    break
                i += 1
            i += 1
            continue
        if ch == '/' and i+1 < n and s[i+1] == '/':
            # line comment
            while i < n and s[i] != '\n':
                i += 1
            continue
        if ch == '/' and i+1 < n and s[i+1] == '*':
            i += 2
            while i+1 < n and not (s[i] == '*' and s[i+1] == '/'):
                i += 1
            i += 2
            continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1

count = 0
for p in paths:
    c = open(p).read()
    # Try with PRELOADER comment marker first
    m = re.search(r"/\*\s*=+\s*PRELOADER\s*=+\s*\*/\s*\n\s*window\.addEventListener\b", c)
    if not m:
        # Fallback: find any window.addEventListener('load' that contains gsap.to(p ... initAll
        for cand in re.finditer(r"window\.addEventListener\(\s*['\"]load['\"]", c):
            # peek next 400 chars for initAll() and gsap.to
            snippet = c[cand.start():cand.start()+600]
            if 'initAll()' in snippet and 'gsap.to' in snippet and 'preloader' in snippet:
                m = cand
                break
        if not m:
            continue
    start = m.start()
    open_paren = c.find('(', m.start())
    close = find_matching_close(c, open_paren)
    if close < 0:
        print('FAIL', p); continue
    end = close + 1
    if end < len(c) and c[end] == ';':
        end += 1
    if end < len(c) and c[end] == '\n':
        end += 1
    new_c = c[:start] + NEW + c[end:]
    open(p, 'w').write(new_c)
    count += 1
print('Patched ' + str(count) + ' files')

# verify
remaining = []
for p in paths:
    c = open(p).read()
    if "gsap.to(preloader" in c or "getElementById('preloader')" in c:
        remaining.append(p)
print('Files still referencing preloader element:', len(remaining))
for r in remaining:
    print(' -', r)
