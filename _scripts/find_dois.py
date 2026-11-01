"""Look up a DOI for each paper on papers.qmd via the Crossref API.

Usage: python3 find_dois.py <papers.qmd> <out.json>
Writes {citation_text: {"doi", "title", "score"}} for review.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

items = re.findall(r"^\d+\. (.*)$", Path(sys.argv[1]).read_text(encoding="utf-8"), re.M)


def words(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def lookup(cite):
    plain = re.sub(r"\*\*|\\", "", cite)
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": plain[:400], "rows": 5, "select": "DOI,title,container-title,issued"})
    req = urllib.request.Request(url, headers={"User-Agent": "personal-site-doi-lookup/1.0"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                found = json.load(r)["message"]["items"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(2 ** attempt)
    cite_words = set(words(plain))
    best = None
    for it in found:
        title = (it.get("title") or [""])[0]
        tw = words(title)
        if not tw:
            continue
        score = sum(w in cite_words for w in tw) / len(tw)
        if best is None or score > best["score"]:
            best = {"doi": it["DOI"], "title": title, "score": round(score, 2),
                    "venue": (it.get("container-title") or [""])[0]}
    return cite, best


with ThreadPoolExecutor(2) as ex:
    results = dict(ex.map(lookup, items))

Path(sys.argv[2]).write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
for cite, best in results.items():
    s = best["score"] if best else 0
    flag = "OK " if s >= 0.9 else "?? "
    print(flag, s, (best or {}).get("doi"), "|", re.sub(r"\*\*", "", cite)[:70], "||", (best or {}).get("title", "")[:60])
