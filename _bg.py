import re, json

with open("projects.html", encoding="utf-8") as f:
    src = f.read()

# Extract components
style = re.search(r"<style>(.*?)</style>", src, re.DOTALL).group(1)
preloader = re.search(r"(<!-- Preloader -->.*?</div>\s*</div>)", src, re.DOTALL).group(1).strip()
navbar = re.search(r"(<!-- Navbar -->.*?</nav>)", src, re.DOTALL).group(1).strip()
fsmenu = re.search(r"(<!-- Fullscreen Menu -->.*?<!-- Page Hero -->)", src, re.DOTALL).group(1).strip()
fsmenu = fsmenu.replace("<!-- Page Hero -->", "").strip()
footer = re.search(r"(<footer.*?</footer>)", src, re.DOTALL).group(1).strip()

