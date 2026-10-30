# Smart Organizational Solutions, LLC

Professional website for SOS — a two-person high-tech consultancy (mobile, AI, and organizational effectiveness).

## How the site is built

The site is plain, pre-rendered HTML. A small Python build step turns the page template and the Markdown articles into static files in `dist/`. Visitors (and search engines and LinkedIn/X link previews) get the full page content immediately; there is no React or Babel compile step in the browser.

The build also converts the main-site images to resized WebP, publishes Andrew's portfolio under `/andrew/`, writes `sitemap.xml`, `robots.txt`, Open Graph tags and schema.org data, and copies `config.json` if it exists.

## Running the website locally

Run these commands from the repository root. Python 3 is required.

```bash
# Install build dependencies (only needed once)
python3 -m pip install markdown Pillow

# Generate the static website in dist/
python3 scripts/build_site.py

# Serve dist/ at http://localhost:8080
python3 -m http.server 8080 --directory dist
```

Open the following URLs in a browser:

- Main website: <http://localhost:8080/>
- Andrew's portfolio: <http://localhost:8080/andrew/>

Keep the terminal running while viewing the site. Press **Ctrl+C** to stop the web server. Re-run the build command after changing source files.

## Project layout

| Path | Purpose |
|------|---------|
| `src/index.template.html` | Home page sections (hero, services, articles, team, contact) |
| `src/site.js` | Navbar scroll effect and contact form (no framework) |
| `style.css` | Styles, including the article reader and backgrounds |
| `articles.json` | Article list (title, author, date, excerpt, Markdown path) |
| `articles/` | Markdown sources and per-article images |
| `portfolio website/` | Andrew's portfolio source; published under `/andrew/` by the main build |
| `images/` | Original, full-size site images (the build makes web copies) |
| `scripts/build_site.py` | Static site build |
| `scripts/build_article_*.py` | Utilities to generate article backgrounds |
| `config.json` | Contact email and form endpoint (copied into `dist/`) |
| `dist/` | Build output, not committed; this is what gets uploaded |

## Adding an article

1. Create a folder without spaces, for example `articles/andrew/my_article_slug/`, containing `draft.md` and its images.
2. Write Markdown. The first `#` heading is removed from the body (the title is shown in the page header). Obsidian-style embeds such as `![[figure-one.png]]` are converted to optimized images automatically.
3. Add an entry to `articles.json`:

```json
{
  "id": "my-article-slug",
  "title": "My Article Title",
  "author": "Andrew Baughns",
  "publishedAt": "2025-05-21",
  "excerpt": "Short summary for the Articles section.",
  "markdownPath": "articles/andrew/my_article_slug/draft.md",
  "backgroundImage": "images/article_tile.png"
}
```

4. Run `python3 scripts/build_site.py`. The article is published at `/articles/my-article-slug/index.html` (links use the explicit `index.html` so they work on CloudFront without extra URL rewriting). Old links of the form `/#article/<id>` redirect there automatically.

## Article backgrounds

Each article can optionally set `backgroundImage` in `articles.json`. When set, the reader page uses class `article-page-with-background` and CSS variable `--article-bg`.

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

## Contact form

Submissions POST to **API Gateway + Lambda + SES**. Configure the API URL and display email in `config.json`:

```json
{
  "contact": {
    "email": "contact@smartyorg.com",
    "subjectPrefix": "SOS Website Contact",
    "formEndpoint": "https://YOUR_API.execute-api.us-east-1.amazonaws.com/development/contact"
  }
}
```

| Field | Purpose |
|-------|---------|
| `email` | Shown as mailto on the page (should match Lambda `TO_EMAIL` / SES recipient) |
| `formEndpoint` | Full API URL including stage and `/contact` path |
| `subjectPrefix` | Passed to Lambda for the email subject |

The form sends `interest` (display label), `interestSlug`, and `message` to Lambda. The notification email includes **Topic of interest** in the subject and body. Redeploy the Lambda after pulling handler changes from `aws/contact-form/`.

Deploy and test: see [aws/README.md](aws/README.md).

## Deploying

Build, then upload `dist/` to the S3 bucket behind CloudFront and invalidate the cache:

```bash
python3 scripts/build_site.py
aws s3 sync dist/ s3://<bucket-name>/ --delete --exclude config.json
aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
```

`--exclude config.json` keeps the live config in place if it is not in your working copy. Any static host (S3, GitHub Pages, Netlify, nginx) works; just upload `dist/`.
