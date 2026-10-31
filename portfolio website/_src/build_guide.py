#!/usr/bin/env python3
"""Build the Noetic Journal user guide pages from the app's in-app help Markdown.

Source:  _src/noetic-guide/pages/   (files exported from the app: YAML front matter + Markdown;
                                     a folder's own note lives in <Folder>_meta.txt)
         _src/noetic-guide/images/  (the app's asset://images/* files)
Output:  apps/noetic-journal/guide/*.html, apps/noetic-journal/guide/img/*.webp, assets/site.css

    pip install markdown Pillow
    python3 _src/build_guide.py

Link handling:
  noetic://document/<title>   -> the matching guide page (unknown titles become plain text)
  noetic://screen/... /dialog -> bold text (they only work inside the app)
  asset://images/<file>       -> optimized WebP copy, click to enlarge
"""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

import markdown
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "noetic-guide"
OUT = ROOT / "apps" / "noetic-journal" / "guide"
SITE = "https://evolved-automata.com"

# Order follows the welcome page's "Optional setup" table.
# Menu groups. Order inside "Set up" follows the welcome page's "Optional setup" table.
GROUPS = [
    ("Start", ["initial experience"]),
    ("Set up", ["Configure AI", "Configure local AI", "camera setup", "configure speech and voice",
                "setup location", "setup music and media", "cloud provider setup",
                "setup notifications", "workspaces", "search your notes"]),
    ("Scripting", ["Welcome — programmable notes", "Scripting overview", "Noetic Lisp and environments",
                   "Macro scripts and the default catalog", "Document managers and collaboration"]),
]
ORDER = [t for _, ts in GROUPS for t in ts]
NAV_LABEL = {
    "initial experience": "Welcome", "Configure AI": "Cloud AI", "Configure local AI": "On-device AI",
    "camera setup": "Camera and photos", "configure speech and voice": "Speech and voice",
    "setup location": "Location reminders", "setup music and media": "Music and media",
    "cloud provider setup": "Dropbox backup and sync", "setup notifications": "Notifications",
    "workspaces": "Workspaces", "search your notes": "Search",
    "Welcome — programmable notes": "Programmable notes", "Scripting overview": "Scripting overview",
    "Noetic Lisp and environments": "Noetic Lisp", "Macro scripts and the default catalog": "Macros",
    "Document managers and collaboration": "Document managers",
}


def slug(title: str) -> str:
    if title == "initial experience":
        return "index"
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            k, _, v = line.strip().partition(":")
            if v.strip():
                meta[k.strip()] = v.strip()
    title = meta.get("title", path.name.replace("_meta.txt", "")).split("/")[-1]
    h1 = re.search(r"^#\s+(.+)$", body, re.M)
    return {"title": title, "body": body, "h1": h1.group(1).strip() if h1 else title,
            "draft": meta.get("draft") == "true", "src": path}


def image(name: str, alt: str) -> str:
    src = SRC / "images" / name
    if not src.exists():
        return f"<!-- missing image {html.escape(name)} -->"
    stem = Path(name).stem
    im = Image.open(src).convert("RGB")
    for w, suf, q in [(480, "", 80), (1080, "-lg", 80)]:
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / "img" / f"{stem}{suf}.webp", "WEBP", quality=q, method=6)
    h = round(480 * im.height / im.width)
    a = html.escape(alt)
    return (f'<figure class="g-shot"><button type="button" data-full="img/{stem}-lg.webp" data-cap="{a}" '
            f'aria-label="Enlarge: {a}"><img src="img/{stem}.webp" alt="{a}" width="480" height="{h}" '
            f'loading="lazy" decoding="async"></button><figcaption>{a}</figcaption></figure>')


def render(page: dict, titles: set[str]) -> str:
    md = re.sub(r"^#\s+.+\n+", "", page["body"], count=1)  # H1 goes in the page header

    # images first: ![alt](<asset://images/x.png>)
    md = re.sub(r"!\[([^\]]*)\]\(<?asset://images/([^)>]+)>?\)",
                lambda m: "\n\n" + image(m.group(2), m.group(1)) + "\n\n", md)

    def link(m: re.Match) -> str:
        text, kind, target = m.group(1), m.group(2), unquote(m.group(3))
        if kind == "document":
            t = target.split("/")[-1]
            return f"[{text}]({slug(t)}.html)" if t in titles else text
        return f"**{text}**" if not text.startswith("**") else text

    md = re.sub(r"\[([^\]]+)\]\(<?noetic://(document|screen|dialog)/([^)>]+)>?\)", link, md)
    out = markdown.markdown(md, extensions=["tables", "sane_lists", "smarty", "md_in_html"])
    # images were inserted as raw HTML blocks; unwrap any <p> markdown put around them
    out = re.sub(r"<p>\s*(<figure class=\"g-shot\">.*?</figure>)\s*</p>", r"\1", out, flags=re.S)
    # group consecutive figures into a row
    out = re.sub(r"((?:<figure class=\"g-shot\">.*?</figure>\s*){2,})",
                 lambda m: f'<div class="g-shots">{m.group(1)}</div>', out, flags=re.S)
    return label_tables(out)


def label_tables(out: str) -> str:
    """Copy each column header into data-label so stacked mobile tables keep their labels."""
    def one(t: re.Match) -> str:
        tbl = t.group(0)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", tbl, re.S)]
        def row(r: re.Match) -> str:
            i = iter(heads)
            return re.sub(r"<td(\s[^>]*)?>", lambda c: f'<td data-label="{html.escape(next(i, ""))}"{c.group(1) or ""}>', r.group(0))
        return re.sub(r"<tr>.*?</tr>", row, tbl, flags=re.S)
    return re.sub(r"<table>.*?</table>", one, out, flags=re.S)


HEAD = """<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Noetic Journal guide</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%232a1f7a'/%3E%3Cpath d='M8 23 L14 9 L20 23 M10.6 18 H17.4' stroke='white' stroke-width='2.4' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3Ccircle cx='24' cy='21' r='2.4' fill='%23f0b44c'/%3E%3C/svg%3E">
<link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@500,700,800&f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../../assets/site.css">
<link rel="stylesheet" href="guide.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site">
  <div class="wrap nav">
    <a class="brand" href="../../../index.html" aria-label="Andrew Baughns, portfolio home">
      <svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="1" y="1" width="30" height="30" rx="8" stroke="currentColor" stroke-width="2"/><path d="M8.5 23 L14 9.5 L19.5 23 M10.8 18 H17.2" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="21" r="2.2" fill="var(--signal)"/></svg>
      Andrew Baughns
    </a>
    <ul>
      <li class="hide-sm"><a class="link" href="../../../index.html#work">Work</a></li>
      <li class="hide-sm"><a class="link" href="index.html">Noetic Journal guide</a></li>
      <li><button class="toggle" data-theme-toggle aria-label="Switch color theme"></button></li>
    </ul>
  </div>
</header>
"""

TAIL = """
<dialog class="lb" id="lb" aria-label="Screenshot viewer"><button type="button" class="lb-x" aria-label="Close">&times;</button><button type="button" class="lb-p" aria-label="Previous screenshot">&larr;</button><figure><img id="lb-img" alt=""><figcaption id="lb-cap"></figcaption></figure><button type="button" class="lb-n" aria-label="Next screenshot">&rarr;</button></dialog>
<script>
(()=>{
  const root=document.documentElement, btn=document.querySelector('[data-theme-toggle]');
  let theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
  const sun='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  const moon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  function set(t){theme=t;root.setAttribute('data-theme',t);btn.innerHTML=t==='dark'?sun:moon;btn.setAttribute('aria-label','Switch to '+(t==='dark'?'light':'dark')+' mode')}
  set(theme); btn.addEventListener('click',()=>set(theme==='dark'?'light':'dark'));
  const hdr=document.querySelector('header.site');
  addEventListener('scroll',()=>hdr.classList.toggle('scrolled',scrollY>8),{passive:true});
  const lb=document.getElementById('lb'),img=document.getElementById('lb-img'),cap=document.getElementById('lb-cap');
  const list=[...document.querySelectorAll('.g-shot button')]; let idx=0;
  const show=i=>{idx=(i+list.length)%list.length;const b=list[idx];img.src=b.dataset.full;img.alt=b.dataset.cap;cap.textContent=b.dataset.cap;};
  list.forEach((b,i)=>b.addEventListener('click',()=>{show(i);lb.showModal();}));
  lb.querySelector('.lb-x').addEventListener('click',()=>lb.close());
  lb.querySelector('.lb-p').addEventListener('click',()=>show(idx-1));
  lb.querySelector('.lb-n').addEventListener('click',()=>show(idx+1));
  lb.addEventListener('click',e=>{if(e.target===lb||e.target.tagName==='FIGURE')lb.close();});
  lb.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1);});
})();
</script>
</body>
</html>
"""


CUR = ' aria-current="page"'


def page_html(p: dict, pages: list[dict], i: int, body: str) -> str:
    have = {q["title"]: q for q in pages}
    nav = ""
    for group, ts in GROUPS:
        items = "".join(
            f'<li><a href="{slug(t)}.html"{CUR if have[t] is p else ""}>{html.escape(NAV_LABEL.get(t, t))}</a></li>'
            for t in ts if t in have)
        if items:
            nav += f'<li class="g-group"><span class="g-group-h">{group}</span><ol>{items}</ol></li>'

    prev_l = f'<a class="pn prev" href="{slug(pages[i-1]["title"])}.html"><span class="mono">Previous</span>{html.escape(NAV_LABEL[pages[i-1]["title"]])}</a>' if i > 0 else "<span></span>"
    next_l = f'<a class="pn next" href="{slug(pages[i+1]["title"])}.html"><span class="mono">Next</span>{html.escape(NAV_LABEL[pages[i+1]["title"]])}</a>' if i + 1 < len(pages) else "<span></span>"
    first_p = re.search(r"<p>(.*?)</p>", body, re.S)
    desc = re.sub(r"<[^>]+>", "", first_p.group(1))[:155] if first_p else p["h1"]
    s = slug(p["title"])
    canonical = f"{SITE}/apps/noetic-journal/guide/{'' if s == 'index' else s + '.html'}"
    draft = '<p class="g-draft mono">Draft page, pending review</p>' if p["draft"] else ""
    return (HEAD.format(title=html.escape(p["h1"]), desc=html.escape(desc), canonical=canonical)
            + f"""<main class="wrap g-layout" id="content">
  <nav class="g-nav" aria-label="Guide pages">
    <div class="eyebrow">Noetic Journal guide</div>
    <ol class="g-groups">{nav}</ol>
  </nav>
  <article class="g-article">
    {draft}<h1>{html.escape(p["h1"])}</h1>
    {body}
    <div class="g-pn">{prev_l}{next_l}</div>
  </article>
</main>
<footer class="wrap g-foot"><span>Noetic Journal is built by Andrew Baughns.</span><a href="../../../index.html">Portfolio</a></footer>"""
            + TAIL)


def site_css() -> None:
    """Share the portfolio's design tokens and base styles with sub-pages."""
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    css = re.search(r"<style>(.*?)</style>", idx, re.S).group(1)
    (ROOT / "assets" / "site.css").write_text("/* generated from index.html by _src/build_guide.py */\n" + css.strip() + "\n")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "img").mkdir(parents=True)
    site_css()
    shutil.copy(SRC / "guide.css", OUT / "guide.css")
    found = {}
    for f in (SRC / "pages").rglob("*"):
        if f.is_file():
            p = parse(f)
            if p["body"].strip() and p["title"] in ORDER:
                found[p["title"]] = p
    pages = [found[t] for t in ORDER if t in found]
    titles = set(found)
    for i, p in enumerate(pages):
        body = render(p, titles)
        (OUT / f"{slug(p['title'])}.html").write_text(page_html(p, pages, i, body), encoding="utf-8")
    missing = [t for t in ORDER if t not in found]
    print(f"Built {len(pages)} pages into {OUT.relative_to(ROOT)}" + (f"; missing: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
