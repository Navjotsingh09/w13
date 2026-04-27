import os, re

paths = []
for root, dirs, fs in os.walk('.'):
    if any(x in root for x in ['./home1','./node_modules','./.git','./.venv']): continue
    for f in fs:
        if f.endswith('.html') and not f.endswith('.backup'):
            paths.append(os.path.join(root, f))

count = 0
for p in paths:
    c = open(p).read()
    o = c
    c = re.sub(
        r'((?:\.\./)?images/hero/[a-z0-9-]+)-sm\.webp 600w,\s*((?:\.\./)?images/hero/[a-z0-9-]+)\.webp 1200w',
        lambda m: m.group(1) + '-sm.webp 600w, ' + m.group(2) + '-md.webp 750w, ' + m.group(2) + '.webp 1200w',
        c
    )
    if c != o:
        open(p, 'w').write(c)
        count += 1
print('Updated ' + str(count) + ' files')
