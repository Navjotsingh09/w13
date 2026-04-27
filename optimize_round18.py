"""Round 18: fix broken onload escaping in shared.min.css preload link.

Old (broken):  onload="this.onload=null;this.rel=\\'stylesheet\\'"
New (works):   onload="this.onload=null;this.rel='stylesheet'"

The `\\'` is a literal backslash in HTML which makes JS see SyntaxError
and never activates the stylesheet, leaving the page unstyled (FOUC).
"""
import glob

OLD = "this.onload=null;this.rel=\\'stylesheet\\'"
NEW = "this.onload=null;this.rel='stylesheet'"

count = 0
for p in glob.glob('**/*.html', recursive=True):
    if 'home1' in p or '.venv' in p or '.backup' in p: continue
    c = open(p).read()
    if OLD in c:
        c = c.replace(OLD, NEW)
        open(p, 'w').write(c)
        count += 1
        print('Patched', p)
print('Total:', count)
