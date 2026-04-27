"""Round 15: fix IIFE pages where gsap.registerPlugin runs at parse time
before deferred GSAP loads, causing ReferenceError and invisible content.

Affected pages: projects.html, project-*.html (8 total).

Approach: replace the leading `(function() { 'use strict';` of the IIFE
with `document.addEventListener('DOMContentLoaded', function() { 'use strict';`
and replace the trailing `})();` with `});`.
Deferred scripts run before DOMContentLoaded so gsap is guaranteed present.

Also remove the obsolete _w13Init block (these pages don't define initAll).
"""
import os, re, glob

paths = []
for p in glob.glob('**/*.html', recursive=True):
    if 'home1' in p or '.venv' in p or '.backup' in p: continue
    c = open(p).read()
    if 'gsap.registerPlugin' in c and 'function initAll' not in c:
        paths.append(p)

count = 0
for p in paths:
    c = open(p).read()
    orig = c

    # 1) Remove the bogus _w13Init block we injected in round 14
    c = re.sub(
        r"\s*/\*\s*=+\s*INIT TRIGGER\s*=+\s*\*/\s*\n"
        r"function _w13Init\(\)\{[^}]*\}\}[^\n]*\n"
        r"if\(document\.readyState[^\n]*\n",
        "\n",
        c,
    )

    # 2) Wrap the IIFE in DOMContentLoaded
    # match: (function() {\n        'use strict';
    c = re.sub(
        r"\(function\(\)\s*\{\s*\n\s*'use strict';",
        "document.addEventListener('DOMContentLoaded', function() {\n        'use strict';",
        c,
        count=1,
    )
    # match the closing })();  (allowing whitespace)
    c = re.sub(
        r"\}\)\(\);\s*</script>",
        "});\n    </script>",
        c,
        count=1,
    )

    if c != orig:
        open(p, 'w').write(c)
        count += 1
        print('Patched', p)

print('Total patched:', count)

# Verify
for p in paths:
    c = open(p).read()
    has_dom = "DOMContentLoaded" in c
    has_iife = "(function() {" in c and "})();" in c
    print(f"{p}: dom={has_dom} iife_remaining={has_iife}")
