# Smart Organizational Solutions, LLC

Professional website for SOS — a two-person high-tech consultancy (mobile, AI, and organizational effectiveness).

## Run locally

This site uses React (via CDN) and loads Markdown articles over HTTP. **Do not open `index.html` directly in the browser** (`file://`); use a local server instead:

```bash
cd /path/to/sos
python3 -m http.server 8080
```

Then visit **http://localhost:8080**

## Project layout

| Path | Purpose |
|------|---------|
| `index.html` | Entry page, loads Bootstrap, React, Marked, `script.js` |
| `script.js` | Site UI and article routing (`#article/<id>`) |
| `style.css` | Styles including article reader and backgrounds |
| `images/` | Site assets (logo, hero, article tile) |
| `articles/` | Markdown sources and per-article images |
| `scripts/` | Utilities to generate article background tiles |

## Adding an article

### 1. Create content on disk

Use a folder without spaces in names (recommended):

```
articles/
  andrew/
    my_article_slug/
      draft.md
      figure-one.png
      figure-two.png
```

Put images in the same folder as the Markdown file.

### 2. Write Markdown

- The **first `#` heading** is used as the listing title but is **removed** on the article page (the title is shown in the page header instead).
- For images, Obsidian-style embeds work and are converted automatically:

```markdown
# My Article Title

## Introduction

Your content here.

![[figure-one.png]]
```

### 3. Register the article in `script.js`

Add an entry to the `ARTICLES` array at the top of `script.js`:

```javascript
{
  id: 'my-article-slug',           // URL: #article/my-article-slug
  title: 'My Article Title',       // Shown in listing and article header
  author: 'Andrew Baughns',
  excerpt: 'Short summary for the Articles section.',
  markdownPath: 'articles/andrew/my_article_slug/draft.md',
  imageBase: 'articles/andrew/my_article_slug/',
  backgroundImage: 'images/article_tile.png',  // optional — see below
},
```

### 4. Preview

Restart or refresh the server, open **http://localhost:8080/#articles**, and click **Read article**, or go directly to **http://localhost:8080/#article/my-article-slug**.

## Article backgrounds

Each article can optionally set `backgroundImage` in `ARTICLES`. When set, the reader page uses class `article-page-with-background` and CSS variable `--article-bg`.

### Default tileable background

The site ships with `images/article_tile.png` — a 320×320 seamless tile (grid, linear motifs, perceptron diagram). Regenerate it after editing the generator:

```bash
python3 scripts/build_article_tile.py
```

Requires Python 3 and Pillow (`pip install Pillow`).

Adjust prominence or colors in `scripts/build_article_tile.py`, then re-run the script and hard-refresh the browser.

### Per-article background

Point `backgroundImage` at any image path:

```javascript
backgroundImage: 'images/article_tile.png',
// or
backgroundImage: 'articles/andrew/my_article_slug/custom_bg.png',
```

Omit `backgroundImage` for a plain light gray article page.

### CSS tuning

Background display is controlled in `style.css` under `.article-page-with-background`:

- `background-repeat: repeat` — tileable patterns
- `background-size: 320px 320px` — should match tile dimensions
- Gradient overlay opacity — readability over busy tiles

Change `background-size` or overlay values if you use a non-tiling image (e.g. `cover` / `contain`).

### Optional full-bleed background

`scripts/build_article_background.py` builds a one-off composite (`images/article_background.png`) from the public-domain [Mark I Perceptron](https://en.wikipedia.org/wiki/Mark_I_Perceptron) image. Use with `background-repeat: no-repeat` and `background-size: cover` in CSS if you switch away from the tile.

## Deploying

Commit and push as usual. Host as static files (GitHub Pages, S3, nginx, etc.) — any static host that serves `.md` and images with correct MIME types works. No build step is required unless you add one later.
