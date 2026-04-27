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
    c = re.sub(r'\.footer-brand img\{height:48px;margin-bottom:20px\}', '.footer-brand img{height:48px;width:auto;margin-bottom:20px}', c)
    c = re.sub(r'\.footer-cert img\{height:44px\}', '.footer-cert img{height:44px;width:auto}', c)
    if c != o:
        open(p, 'w').write(c)
        count += 1
print('Updated ' + str(count) + ' files')
