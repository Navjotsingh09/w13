"""Round 15b: wrap GSAP-using inline scripts in DOMContentLoaded handlers
for project-*.html files. The current scripts call gsap.registerPlugin
at parse time but GSAP loads with defer, so it's undefined.
"""
import os, re, glob

paths = []
for p in glob.glob('**/*.html', recursive=True):
    if 'home1' in p or '.venv' in p or '.backup' in p: continue
    if not p.startswith('project-') or p == 'projects.html': continue
    c = open(p).read()
    if 'gsap.registerPlugin' in c:
        paths.append(p)

# Pattern: a <script> tag (without src, without type=ld+json) that contains gsap.registerPlugin.
# Find the <script> opening just before that line and the </script> after, then wrap inner content
# in DOMContentLoaded handler.

def patch(c):
    # Find span: locate '<script>\n' followed by content containing gsap.registerPlugin, then '</script>'
    pattern = re.compile(r"(<script>)([^<]*?gsap\.registerPlugin[^<]*?)(</script>)", re.S)
    def repl(m):
        inner = m.group(2)
        # If already wrapped, skip
        if "DOMContentLoaded" in inner:
            return m.group(0)
        wrapped = "\ndocument.addEventListener('DOMContentLoaded', function() {\n" + inner.rstrip() + "\n});\n"
        return m.group(1) + wrapped + m.group(3)
    return pattern.sub(repl, c, count=1)

count = 0
for p in paths:
    c = open(p).read()
    n = patch(c)
    if n != c:
        open(p, 'w').write(n)
        count += 1
        print('Patched', p)

print('Total:', count)
