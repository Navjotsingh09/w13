"""Round 16: add dot-cursor DOM + JS to pages missing it.

Pages without the custom cursor: news, news-*, privacy-policy, terms,
services/* (5 files). CSS already lives in shared.min.css.
"""
import re

PAGES = [
    'news.html',
    'news-housing-market-outlook.html',
    'news-rise-of-btr.html',
    'news-delivering-net-zero.html',
    'privacy-policy.html',
    'terms.html',
    'services/architecture-design.html',
    'services/asset-management.html',
    'services/consultancy.html',
    'services/land-development.html',
    'services/master-developer.html',
]

DOT_DIV = '<div class="dot-cursor" id="dotCursor"></div>\n'
DOT_JS = """\n<script>\n/* DOT CURSOR */\n(function(){var c=document.getElementById('dotCursor');if(!c)return;document.addEventListener('mousemove',function(e){c.style.left=e.clientX+'px';c.style.top=e.clientY+'px';});document.addEventListener('mouseleave',function(){c.style.left='-100px';c.style.top='-100px';});document.querySelectorAll('a,button,.menu-close,.nav-link,.cta-btn').forEach(function(el){el.addEventListener('mouseenter',function(){c.classList.add('hovering');});el.addEventListener('mouseleave',function(){c.classList.remove('hovering');});});})();\n</script>\n"""

count = 0
for p in PAGES:
    c = open(p).read()
    if 'dotCursor' in c:
        print('Skip (already has cursor):', p)
        continue
    # Insert DOM div right after <body> (or first <body...>)
    new = re.sub(r"(<body[^>]*>\s*\n?)", r"\1" + DOT_DIV, c, count=1)
    # Insert JS just before </body>
    new = re.sub(r"</body>", DOT_JS + "</body>", new, count=1)
    if new != c:
        open(p, 'w').write(new)
        count += 1
        print('Patched', p)
print('Total patched:', count)
