#!/usr/bin/env python3
"""Build the static Smart Organizational Solutions website into ./dist.

Pages are rendered to plain HTML, so search engines and link previews see the
full content and there is no in-browser React/Babel compile step.

    pip install markdown Pillow
    python3 scripts/build_site.py
    python3 -m http.server -d dist 8080      # preview
    aws s3 sync dist/ s3://<bucket> --delete  # deploy (then invalidate CloudFront)

To add an article: put the Markdown and its images in articles/<author>/<slug>/
(Obsidian-style ![[image.png]] embeds work), add an entry to articles.json, rebuild.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

import markdown
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PORTFOLIO_SRC = ROOT / "portfolio website"
SITE_URL = "https://www.smartyorg.com"
CONTACT_EMAIL = "contact@smartyorg.com"
DEFAULT_ANDREW_EMAIL = "abaughns12@gmail.com"
YEAR = date.today().year

INTEREST_OPTIONS = [
    ("android-ai", "Android & AI on mobile"),
    ("org-development-talent", "Organizational Development and Talent"),
    ("org-leadership-coaching", "Organizational Leadership and Coaching"),
    ("project-transformational-leadership", "Project and Transformational Leadership"),
    ("other", "Other"),
]


# --------------------------------------------------------------------------- images
def webp(src: Path, dest: Path, max_w: int, quality: int = 78) -> str:
    """Write an EXIF-corrected, resized WebP copy of src to dest (relative to DIST)."""
    out = DIST / dest
    out.parent.mkdir(parents=True, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(src))
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(out, "WEBP", quality=quality, method=6)
    return dest.as_posix()


def og_jpeg(src: Path, dest: Path) -> str:
    """Social-preview image: JPEG on a white 1200x630 canvas (LinkedIn/X do not all accept WebP)."""
    logo = Image.open(src).convert("RGBA")
    logo.thumbnail((560, 560), Image.LANCZOS)
    canvas = Image.new("RGB", (1200, 630), "white")
    canvas.paste(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2), logo)
    canvas.save(DIST / dest, "JPEG", quality=85, optimize=True)
    return dest.as_posix()


def build_images() -> dict[str, str]:
    img = ROOT / "images"
    return {
        "hero": webp(img / "hero_background.png", Path("images/hero_background.webp"), 1600, 60),
        "logo": webp(img / "sos_large_logo_3.png", Path("images/sos_logo_nav.webp"), 160, 90),
        "logo_og": og_jpeg(img / "sos_full_large_logo.png", Path("images/sos_og.jpg")),
        "aprill": webp(img / "aprill_prof_full.jpg", Path("images/aprill-baughns.webp"), 900, 80),
        "andrew": webp(img / "ugly_andrew.jpg", Path("images/andrew-baughns.webp"), 900, 78),
        "tile": shutil.copy(img / "article_tile.png", DIST / "images/article_tile.png") and "images/article_tile.png",
        "favicon": webp(img / "sos_large_logo_3.png", Path("images/favicon.webp"), 64, 90),
    }


# --------------------------------------------------------------------------- shared chrome
def head(title: str, description: str, canonical: str, prefix: str, og_image: str, extra: str = "") -> str:
    t, d = html.escape(title), html.escape(description)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}/{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/webp" href="{prefix}images/favicon.webp">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
  <link href="{prefix}style.css" rel="stylesheet">
{extra}</head>
<body>
"""


def navbar(prefix: str, logo: str) -> str:
    home = prefix or ""
    links = [("home", "Home"), ("features", "Services"), ("articles", "Articles"), ("about", "About"), ("contact", "Contact")]
    items = "\n".join(
        f'            <li class="nav-item"><a class="nav-link" href="{home}#{a}">{label}</a></li>' for a, label in links
    )
    return f"""  <nav class="navbar navbar-expand-lg navbar-dark fixed-top navbar-custom" id="site-nav">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="{home}#home">
        <img src="{prefix}{logo}" alt="Smart Organizational Solutions logo" class="navbar-logo me-2" width="30" height="30">
        <span>SOS</span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
{items}
        </ul>
      </div>
    </div>
  </nav>
"""


def footer(prefix: str) -> str:
    home = prefix or ""
    return f"""  <footer class="footer">
    <div class="container">
      <div class="row">
        <div class="col-md-6 mb-4 mb-md-0">
          <span class="navbar-brand text-white">Smart Organizational Solutions, LLC</span>
          <p class="mt-2 mb-3">High-tech consultancy: mobile, AI, and organizational excellence.</p>
          <div class="social-links">
            <a href="#" aria-label="LinkedIn"><i class="bi bi-linkedin"></i></a>
            <a href="#" aria-label="X (Twitter)"><i class="bi bi-twitter-x"></i></a>
            <a href="#" aria-label="GitHub"><i class="bi bi-github"></i></a>
          </div>
        </div>
        <div class="col-md-3 col-6">
          <h6 class="text-white mb-3">Quick links</h6>
          <ul class="list-unstyled">
            <li><a href="{home}#home">Home</a></li>
            <li><a href="{home}#features">Services</a></li>
            <li><a href="{home}#articles">Articles</a></li>
            <li><a href="{home}#about">About</a></li>
            <li><a href="{home}#contact">Contact</a></li>
          </ul>
        </div>
        <div class="col-md-3 col-6">
          <h6 class="text-white mb-3">Legal</h6>
          <ul class="list-unstyled">
            <li><a href="#">Privacy</a></li>
            <li><a href="#">Terms</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom text-center text-md-start">
        &copy; {YEAR} Smart Organizational Solutions, LLC. All rights reserved.
      </div>
    </div>
  </footer>
"""


def scripts(prefix: str, with_contact: bool) -> str:
    contact = f'\n  <script src="{prefix}site.js" defer></script>' if with_contact else f'\n  <script src="{prefix}site.js" defer></script>'
    return f"""  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" defer></script>{contact}
</body>
</html>
"""


def fmt_date(iso: str) -> str:
    if not iso:
        return ""
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


# --------------------------------------------------------------------------- articles
def render_markdown(md_text: str, md_path: Path, out_dir: Path) -> str:
    md_text = re.sub(r"^#\s+.+\n+", "", md_text, count=1)  # title lives in the page header

    def embed(m: re.Match) -> str:
        name = m.group(1).strip()
        src = md_path.parent / name
        stem = Path(name).stem
        rel = webp(src, out_dir.relative_to(DIST) / f"{stem}.webp", 1200, 78)
        alt = stem.replace("_", " ").replace("-", " ")
        return f"![{alt}]({Path(rel).name})"

    md_text = re.sub(r"!\[\[([^\]]+)\]\]", embed, md_text)
    body = markdown.markdown(md_text, extensions=["extra", "sane_lists", "smarty"])
    return body.replace("<img ", '<img loading="lazy" decoding="async" ')


def build_article(a: dict, imgs: dict) -> None:
    out_dir = DIST / "articles" / a["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = ROOT / a["markdownPath"]
    body = render_markdown(md_path.read_text(encoding="utf-8"), md_path, out_dir)
    prefix = "../../"
    canonical = f"{SITE_URL}/articles/{a['id']}/index.html"
    ld = {
        "@context": "https://schema.org", "@type": "Article", "headline": a["title"],
        "author": {"@type": "Person", "name": a["author"]}, "datePublished": a.get("publishedAt"),
        "publisher": {"@type": "Organization", "name": "Smart Organizational Solutions, LLC"},
        "description": a["excerpt"], "mainEntityOfPage": canonical,
    }
    extra = f'  <script type="application/ld+json">{json.dumps(ld)}</script>\n'
    bg = a.get("backgroundImage")
    section_cls = "article-page article-page-with-background" if bg else "article-page"
    style = f" style=\"--article-bg: url('{prefix}{bg}')\"" if bg else ""
    date_html = f'          <p class="text-muted small mb-2"><time datetime="{a["publishedAt"]}">{fmt_date(a["publishedAt"])}</time></p>\n' if a.get("publishedAt") else ""
    page = (
        head(f"{a['title']} | Smart Organizational Solutions", a["excerpt"], canonical, prefix, imgs["logo_og"], extra)
        + navbar(prefix, imgs["logo"])
        + f"""  <main>
    <section class="{section_cls}"{style}>
      <div class="container">
        <div class="article-panel">
          <a href="{prefix}#articles" class="article-back-link small text-decoration-none mb-4 d-inline-block"><i class="bi bi-arrow-left me-1"></i> Back to articles</a>
          <header class="article-header mb-4">
            <p class="text-primary small fw-semibold mb-1">{html.escape(a['author'])}</p>
{date_html}            <h1 class="article-title h2 fw-bold">{html.escape(a['title'])}</h1>
          </header>
          <article class="article-body">
{body}
          </article>
        </div>
      </div>
    </section>
  </main>
"""
        + footer(prefix)
        + scripts(prefix, with_contact=False)
    )
    (out_dir / "index.html").write_text(page, encoding="utf-8")


# --------------------------------------------------------------------------- home page
def build_index(articles: list[dict], imgs: dict) -> None:
    template = (ROOT / "src" / "index.template.html").read_text(encoding="utf-8")
    cards = []
    for a in articles:
        d = f'\n                <p class="text-muted small mb-2"><time datetime="{a["publishedAt"]}">{fmt_date(a["publishedAt"])}</time></p>' if a.get("publishedAt") else ""
        cards.append(f"""            <div class="col-md-10 col-lg-8">
              <div class="article-card card border-0 shadow-sm h-100">
                <div class="card-body p-4">
                  <p class="text-primary small fw-semibold mb-1">{html.escape(a['author'])}</p>{d}
                  <h3 class="h5 fw-bold mb-2">{html.escape(a['title'])}</h3>
                  <p class="text-secondary mb-3">{html.escape(a['excerpt'])}</p>
                  <a href="articles/{a['id']}/index.html" class="btn btn-outline-primary btn-sm">Read article <i class="bi bi-arrow-right ms-1"></i></a>
                </div>
              </div>
            </div>""")
    options = "\n".join(f'                      <option value="{v}">{html.escape(l)}</option>' for v, l in INTEREST_OPTIONS)
    ld = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Smart Organizational Solutions, LLC", "url": SITE_URL + "/", "email": CONTACT_EMAIL,
        "description": "Two-person high-tech consultancy combining mobile & AI expertise with organizational effectiveness and change management.",
        "founder": [{"@type": "Person", "name": "Aprill Baughns"}, {"@type": "Person", "name": "Andrew Baughns"}],
        "areaServed": "US",
    }
    desc = ("A two-person high-tech consultancy combining Android, mobile and on-device AI expertise "
            "with organizational effectiveness and change management.")
    extra = (f'  <link rel="preload" as="image" href="{imgs["hero"]}">\n'
             f'  <script type="application/ld+json">{json.dumps(ld)}</script>\n'
             "  <script>/* old #article/<id> links -> static article pages */\n"
             "  (function(){var m=location.hash.match(/^#article\\/([^/]+)/);if(m)location.replace('articles/'+m[1]+'/index.html');})();</script>\n")
    page = (
        head("Smart Organizational Solutions, LLC | High-Tech Consultancy", desc, SITE_URL + "/", "", imgs["logo_og"], extra)
        + navbar("", imgs["logo"])
        + template.replace("{{ARTICLE_CARDS}}", "\n".join(cards))
                  .replace("{{INTEREST_OPTIONS}}", options)
                  .replace("{{CONTACT_EMAIL}}", CONTACT_EMAIL)
                  .replace("{{IMG_APRILL}}", imgs["aprill"])
                  .replace("{{IMG_ANDREW}}", imgs["andrew"])
        + footer("")
        + scripts("", with_contact=True)
    )
    (DIST / "index.html").write_text(page, encoding="utf-8")


def build_portfolio(andrew_email: str) -> None:
    """Publish Andrew's standalone portfolio as the /andrew section of SOS."""
    out = DIST / "andrew"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(PORTFOLIO_SRC / "index.html", out / "index.html")
    shutil.copytree(PORTFOLIO_SRC / "assets", out / "assets")
    shutil.copytree(PORTFOLIO_SRC / "apps", out / "apps")

    # Keep the portfolio independently publishable at evolved-automata.com.
    # Rewrite canonical URLs only in the SOS build and add a local route home.
    for page_path in out.rglob("*.html"):
        page = page_path.read_text(encoding="utf-8")
        page = page.replace("https://evolved-automata.com/", f"{SITE_URL}/andrew/")
        if page_path == out / "index.html":
            page = page.replace("{{ANDREW_EMAIL}}", html.escape(andrew_email, quote=True))
            page = page.replace(
                '<li class="hide-sm"><a class="link" href="#about">About</a></li>',
                '<li class="hide-sm"><a class="link" href="#about">About</a></li>\n'
                '      <li class="hide-sm"><a class="link" href="../index.html">SOS Home</a></li>',
            )
            page = page.replace(
                '<a href="https://www.smartyorg.com/" target="_blank" rel="noopener">Smart Organizational Solutions</a>',
                '<a href="../index.html">Smart Organizational Solutions</a>',
            )
            page = page.replace(
                '<a href="https://www.smartyorg.com/" target="_blank" rel="noopener">Consultancy <span>smartyorg.com</span></a>',
                '<a href="../index.html">Consultancy <span>SOS home</span></a>',
            )
        page_path.write_text(page, encoding="utf-8")


def build_sitemap(articles: list[dict]) -> None:
    urls = [SITE_URL + "/"] + [f"{SITE_URL}/articles/{a['id']}/index.html" for a in articles]
    urls.extend(
        f"{SITE_URL}/{page.relative_to(DIST).as_posix()}"
        for page in sorted((DIST / "andrew").rglob("*.html"))
    )
    body = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "images").mkdir(parents=True)
    imgs = build_images()
    css = (ROOT / "style.css").read_text(encoding="utf-8").replace("images/hero_background.png", "images/hero_background.webp")
    (DIST / "style.css").write_text(css, encoding="utf-8")
    shutil.copy(ROOT / "src" / "site.js", DIST / "site.js")
    config_path = ROOT / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    if config_path.exists():  # deployed config (not committed)
        shutil.copy(config_path, DIST / "config.json")
    andrew_email = config.get("andrew", {}).get("email", DEFAULT_ANDREW_EMAIL).strip()
    if not andrew_email:
        andrew_email = DEFAULT_ANDREW_EMAIL
    articles = json.loads((ROOT / "articles.json").read_text(encoding="utf-8"))
    for a in articles:
        build_article(a, imgs)
    build_index(articles, imgs)
    build_portfolio(andrew_email)
    build_sitemap(articles)
    total = sum(p.stat().st_size for p in DIST.rglob("*") if p.is_file())
    print(f"Built {len(articles)} article(s) into {DIST} ({total/1024:.0f} KB total)")


if __name__ == "__main__":
    main()
