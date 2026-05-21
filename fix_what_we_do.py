import re, glob

files = glob.glob('*.html') + glob.glob('sectors/*.html') + glob.glob('services/*.html')
files = [f for f in files if not f.endswith('.backup')]

pattern = re.compile(r'href="(?:\.\./)?services\.html"([^>]*)>What We Do')

changed = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    new_content = pattern.sub(r'href="javascript:void(0)"\1>What We Do', content)
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        changed.append(f)

print(f"Updated {len(changed)} files:")
for f in sorted(changed):
    print(f"  {f}")
