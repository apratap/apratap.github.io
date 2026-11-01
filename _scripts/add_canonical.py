"""Post-render step: add a <link rel="canonical"> to every page in _site.

Quarto runs this after each render (see project.post-render in _quarto.yml).
The AID4MH paper pages exist in several sections; their copies under
conferences/ and posters/ point at the journal-articles/ version so search
engines treat them as one page.
"""
import re
from pathlib import Path

SITE_URL = "https://apratap.me/"
SITE = Path("_site")
DUPLICATE_SECTIONS = ("aid4mh/conferences/", "aid4mh/posters/")
PRIMARY_SECTION = "aid4mh/journal-articles/"


def canonical_path(rel: str) -> str:
    for section in DUPLICATE_SECTIONS:
        if rel.startswith(section):
            primary = PRIMARY_SECTION + rel[len(section):]
            if (SITE / primary).exists():
                rel = primary
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("index.html")]
    return rel


for page in SITE.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    if "</head>" not in html or 'rel="canonical"' in html:
        continue  # draft placeholders have no head; already-tagged pages are skipped
    rel = page.relative_to(SITE).as_posix()
    tag = f'<link rel="canonical" href="{SITE_URL}{canonical_path(rel)}">\n'
    page.write_text(re.sub(r"</head>", tag + "</head>", html, count=1), encoding="utf-8")
