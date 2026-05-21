import glob, os

patterns = [
    (
        '<link rel="preload" href="shared.min.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="shared.min.css"></noscript>',
        '<link rel="stylesheet" href="shared.min.css">'
    ),
    (
        '<link rel="preload" href="../shared.min.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="../shared.min.css"></noscript>',
        '<link rel="stylesheet" href="../shared.min.css">'
    ),
]

files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('sectors/*.html')
changed = []
for f in files:
    content = open(f).read()
    new = content
    for old, rep in patterns:
        new = new.replace(old, rep)
    if new != content:
        open(f, 'w').write(new)
        changed.append(f)

print(f'Changed {len(changed)} files:')
for f in sorted(changed):
    print(' ', f)
