# apratap.github.io

Personal website of Abhishek Pratap, built with [Quarto](https://quarto.org) and published to GitHub Pages
on every push to `main`.

## Layout

| Path | What it is |
|---|---|
| `index.qmd` | Home page: bio, pinned posts, latest posts |
| `blog/posts/<YYYY-MM-DD-title>/` | One folder per post (`index.md`, `index.ipynb` or `index.qmd`) |
| `aid4mh/` | Past AID4MH group work, migrated from the old Hugo site |
| `_quarto.yml` | Site title, navigation menu, footer |
| `theme.scss`, `theme-dark.scss` | Fonts and colours |
| `.github/workflows/publish.yml` | Builds and deploys the site |

## Writing a post

1. Create `blog/posts/2026-11-02-my-post/index.md` (or `index.ipynb`).
2. Add front matter: `title`, `date`, `description`, `categories`. For notebooks, put it in a first **raw** cell.
3. Add `pinned: true` to feature it on the home page, or `draft: true` to keep it unpublished.
4. Commit and push.

Notebooks are rendered from their saved outputs and never re-executed. `.qmd` posts with code are run
when you render locally, and the results are stored in `_freeze/`; commit that folder.

## Preview locally

```bash
brew install --cask quarto   # once
quarto preview
```

## License

Content (posts, pages, slides, images) is licensed [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/); the site code is MIT. See [LICENSE](LICENSE) for details and exceptions.
