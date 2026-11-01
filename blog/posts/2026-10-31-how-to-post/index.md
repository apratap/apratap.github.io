---
title: "How to add a post to this site"
date: 2026-10-31
description: "A starter post: how Markdown and notebook posts work here. Edit or delete it."
categories: [meta]
pinned: true
draft: true  # kept for reference; left out of the published site
---

This is a starter post. Replace it with your own writing, or delete its folder.

## Writing a post

Each post is a folder inside `blog/posts/`, named `YYYY-MM-DD-short-title/`. Inside it, add **one** of:

- `index.md`: plain Markdown
- `index.ipynb`: a Jupyter notebook (its saved outputs are shown; it isn't re-run)
- `index.qmd`: Quarto Markdown with runnable code cells

Images and data files go in the same folder, and you link them by relative path, e.g. `![](figure.png)`.

## Front matter

The block at the top of the file (or the first *raw* cell of a notebook) sets the post's details:

```yaml
---
title: "My post"
date: 2026-11-02
description: "One-line summary shown in listings."
categories: [digital health, ml]
image: cover.png      # optional thumbnail
pinned: true          # optional: show under "Pinned" on the home page
draft: true           # optional: hide from the published site
---
```

## Publishing

Commit and push to `main`. GitHub Actions rebuilds the site and it's live a minute or two later.
