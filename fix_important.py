content = open('services.html').read()
# Fix \!important -> !important in the CSS
import re
fixed = re.sub(r'\\!important', '!important', content)
if fixed != content:
    open('services.html', 'w').write(fixed)
    n = content.count('\\!important')
    print(f'Fixed {n} occurrences')
else:
    print('No change - check manually')
    import subprocess
    result = subprocess.run(['grep', '-o', r'\\!important', 'services.html'], capture_output=True, text=True)
    print(repr(result.stdout[:200]))
