import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1','./node_modules','./.git','./.venv']): continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

# Inject a minimal skip-link rule at the start of the inline <style> if missing.
RULE = ".skip-link{position:absolute;top:-100%;left:16px;z-index:100001;padding:12px 24px;background:#44C0C0;color:#0C233F;font-family:'Graphie',sans-serif;font-weight:600;font-size:14px;border-radius:0 0 8px 8px;transition:top 0.3s}.skip-link:focus{top:0}"

count = 0
for p in paths:
    c = open(p).read()
    if '.skip-link{' in c:
        continue
    if 'skip-link' not in c:
        continue
    o = c
    c = c.replace('<style>', '<style>' + RULE, 1)
    if c != o:
        open(p, 'w').write(c)
        count += 1
print('Added skip-link rule to ' + str(count) + ' files')
