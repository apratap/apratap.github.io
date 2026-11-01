"""Build papers.qmd from the CV (converted to Markdown with pandoc).

Usage: python3 build_papers.py <cv.md> <papers.qmd> [paper_links.json]
"""
import json
import re
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
OPEN = set()  # group titles to show expanded; all others start collapsed

start = lines.index("Peer-Reviewed Publications")
end = lines.index("Invited Talks & Presentations")  # talks and abstracts are left off the site
top_sections = {
    "Peer-Reviewed Publications": "Peer-reviewed publications",
    "Invited Talks & Presentations": "Invited talks and presentations",
    "Conference Abstracts & Posters": "Conference abstracts and posters",
}

# groups: list of (top_section, group_title, [items])
groups = []
top = None
for line in lines[start:end]:
    s = line.strip()
    if not s:
        continue
    if s in top_sections:
        top = top_sections[s]
        if top != "Peer-reviewed publications":
            groups.append((top, None, []))
        continue
    m = re.fullmatch(r"\*([^*].*[^*])\*", s)
    if m and top == "Peer-reviewed publications":
        groups.append((top, m.group(1), []))
        continue
    item = re.match(r"^\d+\.\s+(.*)$", s)
    if item:
        groups[-1][2].append(item.group(1))
    elif groups and groups[-1][2]:
        groups[-1][2][-1] += " " + s


def clean(text):
    # Drop the CV's italic role notes, e.g. "(*senior author*)", and the joint-first "\*" markers.
    text = re.sub(r"\s*\(\*.*?\*\)", "", text)
    text = text.replace("\\*", "")
    return text.strip()


for g in groups:
    g[2][:] = [clean(t) for t in g[2]]

# Publisher links (DOI, PubMed Central or arXiv), keyed by the cleaned citation text.
LINKS = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))["links"] if len(sys.argv) > 3 else {}
missing = [t for g in groups for t in g[2] if t not in LINKS]
if LINKS and missing:
    sys.exit("No link for:\n" + "\n".join(missing))
for g in groups:
    g[2][:] = [f"{t} [link]({LINKS[t]}){{.paper-link}}" if t in LINKS else t for t in g[2]]


def details(title, items, level_class):
    is_open = " open" if title in OPEN else ""
    out = [f'<details class="paper-group {level_class}"{is_open}>',
           f'<summary>{title} <span class="count">{len(items)}</span></summary>', ""]
    out += [f"{i}. {text}" for i, text in enumerate(items, 1)]
    out += ["", "</details>", ""]
    return "\n".join(out)


body = []
current_top = None
for top, title, items in groups:
    if top != current_top:
        current_top = top
        n = sum(len(g[2]) for g in groups if g[0] == top)
        body.append(f"## {top} [{n}]{{.count}}\n")
    if title:
        body.append(details(title, items, "sub"))
    else:
        label = {"Invited talks and presentations": "All talks",
                 "Conference abstracts and posters": "All abstracts and posters"}[top]
        body.append(details(label, items, "solo"))

header = """---
title: "Papers"
description: "Peer-reviewed publications, grouped by theme."
toc: false
---

<!-- Generated from the CV (202610_CV_Abhi_Pratap.docx). Groups and order follow the CV. -->

[[google scholar](https://scholar.google.com/citations?user=abhipratap) · [expand all](#){.expand-all} · [collapse all](#){.collapse-all}]{.label-links}

"""

script = """
```{=html}
<script>
document.addEventListener("DOMContentLoaded", () => {
  const set = (open) => (e) => {
    e.preventDefault();
    document.querySelectorAll("details.paper-group").forEach((d) => (d.open = open));
  };
  document.querySelectorAll(".expand-all").forEach((a) => a.addEventListener("click", set(true)));
  document.querySelectorAll(".collapse-all").forEach((a) => a.addEventListener("click", set(false)));
});
</script>
```
"""

Path(sys.argv[2]).write_text(header + "\n".join(body) + script, encoding="utf-8")
for top, title, items in groups:
    print(f"{top:35} | {title or '-':75} | {len(items)}")
