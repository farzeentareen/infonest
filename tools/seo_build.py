# -*- coding: utf-8 -*-
"""Rebuild sitemap + inject OG tags and JSON-LD."""
from __future__ import annotations

import json
import re
import struct
import zlib
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "https://infonest.page"
LASTMOD = "2026-08-18"
OG = f"{HOST}/assets/images/og-home.png"
LOGO = f"{HOST}/assets/images/logo.svg"

CATS = {
    "technology": "Technology",
    "ai": "Artificial Intelligence",
    "programming": "Programming",
    "finance": "Finance",
    "health-wellness": "Health & Wellness",
    "education": "Education",
    "career": "Career",
    "business": "Business",
    "productivity": "Productivity",
    "travel": "Travel",
    "lifestyle": "Lifestyle",
}

SKIP = {"author", "tools"}


def write_og_png():
    w, h = 1200, 630
    # navy + teal bar
    row_navy = b"\x00" + (bytes([13, 27, 42]) * w)
    row_teal = b"\x00" + (bytes([20, 184, 166]) * w)
    rows = []
    for y in range(h):
        rows.append(row_teal if 250 <= y <= 380 else row_navy)
    raw = b"".join(rows)
    comp = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b"")
    out = ROOT / "assets" / "images" / "og-home.png"
    out.write_bytes(png)


def page_url(rel: Path) -> str:
    parts = rel.as_posix()
    if parts == "index.html":
        return HOST + "/"
    folder = str(rel.parent).replace("\\", "/")
    if folder == ".":
        return HOST + "/"
    return HOST + "/" + folder.strip("/") + "/"


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", unescape(s)).strip()


def meta(html: str, name: str) -> str:
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', html, re.I)
    if m:
        return unescape(m.group(1))
    m = re.search(rf'<meta\s+content="([^"]*)"\s+name="{name}"', html, re.I)
    return unescape(m.group(1)) if m else ""


def title_text(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    return strip_tags(m.group(1)) if m else "InfoNest"


def h1_text(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    return strip_tags(m.group(1)) if m else title_text(html)


def collect_urls():
    urls = []
    # core
    for p in [
        "index.html",
        "about/index.html",
        "contact/index.html",
        "privacy-policy/index.html",
        "terms/index.html",
        "disclaimer/index.html",
        "editorial-policy/index.html",
        "sitemap-page/index.html",
    ]:
        urls.append(page_url(Path(p)))
    for cat in CATS:
        urls.append(f"{HOST}/{cat}/")
        catdir = ROOT / cat
        if not catdir.is_dir():
            continue
        for child in sorted(catdir.iterdir()):
            if child.is_dir() and (child / "index.html").exists():
                urls.append(f"{HOST}/{cat}/{child.name}/")
    # unique preserve order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def write_sitemap(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == HOST + "/" else ("0.9" if u.count("/") == 4 else "0.8")
        if any(x in u for x in ("privacy", "terms", "disclaimer", "sitemap-page")):
            pri = "0.5"
        lines.append(
            f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>"
        )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_faqs(html: str) -> list[tuple[str, str]]:
    m = re.search(r'<h2[^>]*id="faq"[^>]*>.*?</h2>(.*?)(?:<div class="key-takeaways"|<div class="article-footer")', html, re.I | re.S)
    if not m:
        return []
    block = m.group(1)
    faqs = []
    for q, a in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", block, re.I | re.S):
        faqs.append((strip_tags(q), strip_tags(a)))
    return faqs[:8]


def article_dates(html: str) -> tuple[str, str]:
    pub, mod = LASTMOD, LASTMOD
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    if m:
        pub = m.group(1)
    m = re.search(r'"dateModified"\s*:\s*"([^"]+)"', html)
    if m:
        mod = m.group(1)
    return pub, mod


def json_ld_scripts(html: str) -> str:
    return re.sub(r'\s*<script type="application/ld\+json">[\s\S]*?</script>', "", html, flags=re.I)


def inject_after_title(html: str, block: str) -> str:
    if "</title>" in html.lower():
        # case-sensitive replace first title close
        return re.sub(r"</title>", "</title>\n" + block, html, count=1, flags=re.I)
    return html


def ensure_og(html: str, url: str, is_article: bool) -> str:
    title = title_text(html)
    desc = meta(html, "description") or title
    og_type = "article" if is_article else "website"
    # strip existing og/twitter to avoid duplicates
    html = re.sub(r'\s*<meta\s+property="og:[^"]+"\s+content="[^"]*"\s*/?>', "", html, flags=re.I)
    html = re.sub(r'\s*<meta\s+name="twitter:[^"]+"\s+content="[^"]*"\s*/?>', "", html, flags=re.I)
    if 'rel="canonical"' not in html.lower():
        html = inject_after_title(html, f'  <link rel="canonical" href="{url}" />')
    else:
        html = re.sub(
            r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>',
            f'<link rel="canonical" href="{url}" />',
            html,
            count=1,
            flags=re.I,
        )
    og = f'''  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:image" content="{OG}" />
  <meta property="og:site_name" content="InfoNest" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{OG}" />'''
    return inject_after_title(html, og)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def org_publisher():
    return {
        "@type": "Organization",
        "name": "InfoNest",
        "url": HOST,
        "logo": {"@type": "ImageObject", "url": LOGO},
        "email": "hello@infonest.page",
    }


def article_ld(html: str, url: str, cat: str, slug: str) -> list[dict]:
    desc = meta(html, "description")
    headline = h1_text(html)
    pub, mod = article_dates(html)
    cat_label = CATS.get(cat, cat)
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": desc,
        "datePublished": pub,
        "dateModified": mod,
        "image": OG,
        "author": {"@type": "Organization", "name": "InfoNest Editorial", "url": HOST + "/about/"},
        "publisher": org_publisher(),
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": HOST + "/"},
            {"@type": "ListItem", "position": 2, "name": cat_label, "item": f"{HOST}/{cat}/"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": url},
        ],
    }
    out = [article, crumbs]
    faqs = extract_faqs(html)
    if faqs:
        out.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })
    return out


def category_ld(html: str, cat: str) -> dict:
    hrefs = re.findall(rf'href="(/{cat}/[^"]+/)"', html)
    seen = []
    for h in hrefs:
        if h not in seen and h != f"/{cat}/":
            seen.append(h)
    elements = [
        {"@type": "ListItem", "position": i + 1, "url": HOST + h}
        for i, h in enumerate(seen)
    ]
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": CATS.get(cat, cat) + " — InfoNest",
        "url": f"{HOST}/{cat}/",
        "isPartOf": {"@type": "WebSite", "name": "InfoNest", "url": HOST},
        "mainEntity": {"@type": "ItemList", "itemListElement": elements},
    }


def ld_html(objs) -> str:
    if not isinstance(objs, list):
        objs = [objs]
    parts = []
    for o in objs:
        parts.append(
            '  <script type="application/ld+json">\n  '
            + json.dumps(o, ensure_ascii=False)
            + "\n  </script>"
        )
    return "\n".join(parts)


def process_file(path: Path):
    rel = path.relative_to(ROOT)
    if "tools" in rel.parts or rel.parts[0] == "author":
        return
    html = path.read_text(encoding="utf-8")
    url = page_url(rel)
    parts = rel.parts
    is_article = len(parts) >= 3 and parts[-1] == "index.html" and parts[0] in CATS
    is_cat = len(parts) == 2 and parts[0] in CATS and parts[1] == "index.html"

    html = json_ld_scripts(html)
    html = ensure_og(html, url, is_article)

    if is_article:
        cat, slug = parts[0], parts[1]
        html = inject_after_title(html, ld_html(article_ld(html, url, cat, slug)))
    elif is_cat:
        html = inject_after_title(html, ld_html(category_ld(html, parts[0])))
    elif rel.as_posix() == "index.html":
        html = inject_after_title(html, ld_html([
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "InfoNest",
                "url": HOST,
                "description": "Practical how-to articles on work, money, health, and technology.",
                "publisher": org_publisher(),
            },
            dict({"@context": "https://schema.org"}, **org_publisher()),
        ]))
    elif rel.as_posix() == "about/index.html":
        html = inject_after_title(html, ld_html(dict({"@context": "https://schema.org"}, **org_publisher())))

    path.write_text(html, encoding="utf-8")


def main():
    write_og_png()
    urls = collect_urls()
    write_sitemap(urls)
    n = 0
    for path in ROOT.rglob("index.html"):
        if "tools" in path.parts:
            continue
        process_file(path)
        n += 1
    print("pages", n, "sitemap", len(urls))


if __name__ == "__main__":
    main()
