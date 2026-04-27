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
    # Remove font preload - competes with LCP image bandwidth on slow 4G
    c = re.sub(
        r'\s*<link rel="preload" href="(?:\.\./)?fonts/Graphie-[A-Za-z]+\.woff2" as="font" type="font/woff2" crossorigin>',
        '',
        c
    )
    if c != o:
        open(p, 'w').write(c)
        count += 1
print('Removed font preload from ' + str(count) + ' files')
