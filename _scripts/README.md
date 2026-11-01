# Rebuilding the Papers page from the CV

```bash
quarto pandoc path/to/CV.docx -t gfm --wrap=none -o /tmp/cv.md
python3 _scripts/build_papers.py /tmp/cv.md papers.qmd _scripts/paper_links.json
```

`build_papers.py` stops with a list of any paper that has no entry in `paper_links.json`.
For new papers, run `python3 _scripts/find_dois.py papers.qmd /tmp/dois.json` to look up DOIs
in Crossref, check the matches, and add them to `paper_links.json`.

Don't commit the converted CV; it contains contact details.
