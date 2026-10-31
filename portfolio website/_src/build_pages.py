#!/usr/bin/env python3
"""Render standalone pages (apps hub, app pages, privacy policies) from _src/pages/*.md.

Each file has front matter with `title`, `out` (path from the site root) and `description`.
Uses the same header, theme toggle and image viewer as the guide (see build_guide.py).

    python3 _src/build_guide.py && python3 _src/build_pages.py
"""
import html
import re
import shutil
from pathlib import Path

import markdown

import build_guide as g

ROOT = g.ROOT


def main() -> None:
    shutil.copy(g.SRC / "guide.css", ROOT / "assets" / "pages.css")
    for f in sorted((ROOT / "_src" / "pages").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, body = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S).groups()
        meta = dict(l.split(":", 1) for l in fm.splitlines() if ":" in l)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        out = ROOT / meta["out"]
        depth = len(Path(meta["out"]).parts) - 1
        up = "../" * depth
        head = (g.HEAD.replace("../../../", up)
                .replace('href="guide.css"', f'href="{up}assets/pages.css"')
                .replace('href="index.html">Noetic Journal guide', f'href="{up}apps/index.html">Apps'))
        canonical = f"{g.SITE}/{meta['out']}".replace("/index.html", "/")
        h1 = re.search(r"^#\s+(.+)$", body, re.M).group(1)
        body = re.sub(r"^#\s+.+$", lambda m: f"<h1>{html.escape(h1)}</h1>", body, count=1, flags=re.M)
        content = markdown.markdown(body, extensions=["tables", "sane_lists", "md_in_html"])
        content = g.label_tables(content)
        page = (head.format(title=html.escape(meta["title"]), desc=html.escape(meta["description"]), canonical=canonical)
                .replace(" · Noetic Journal guide</title>", " · Andrew Baughns</title>")
                + f'<main class="wrap p-layout" id="content"><article class="g-article">{content}</article></main>\n'
                + f'<footer class="wrap g-foot"><span>Andrew Baughns · Orlando, FL</span><span><a href="{up}apps/index.html">Apps</a> · <a href="{up}index.html">Portfolio</a></span></footer>'
                + g.TAIL)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print("wrote", meta["out"])


if __name__ == "__main__":
    main()
