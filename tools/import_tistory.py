#!/usr/bin/env python3
import argparse
import email.utils
import html
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


BLOG_URL = "https://yeseul7.tistory.com"
POSTS_DIR = Path("_posts")
IMAGES_DIR = Path("assets/img/posts/tistory")
TIMEZONE = "+0900"


def fetch(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; tistory-importer/1.0)",
            "Referer": BLOG_URL + "/",
        },
    )
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as res:
        return res.read(), res.headers


def fetch_text(url):
    data, headers = fetch(url)
    charset = headers.get_content_charset() or "utf-8"
    return data.decode(charset, errors="replace")


def yaml_string(value):
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values):
    return "[" + ", ".join(yaml_string(v) for v in values) + "]"


def post_id_from_url(url):
    match = re.search(r"/(\d+)(?:$|[?#])", url)
    return match.group(1) if match else None


def parse_rss():
    rss = fetch_text(BLOG_URL + "/rss")
    root = ET.fromstring(rss)
    posts = {}
    for item in root.findall("./channel/item"):
        link = item.findtext("link") or ""
        post_id = post_id_from_url(link)
        if not post_id:
            continue
        posts[post_id] = {
            "id": post_id,
            "url": link,
            "title": item.findtext("title") or f"Tistory {post_id}",
            "date": parse_rss_date(item.findtext("pubDate")),
            "category": (item.findtext("category") or "").strip(),
            "body": item.findtext("description") or "",
        }
    return posts


def parse_rss_date(value):
    if not value:
        return None
    parsed = email.utils.parsedate_to_datetime(value)
    return parsed.strftime("%Y-%m-%d %H:%M:%S %z")


def collect_ids_from_listing(max_pages):
    ids = set()
    for page in range(1, max_pages + 1):
        url = BLOG_URL + ("/" if page == 1 else f"/?page={page}")
        try:
            text = fetch_text(url)
        except urllib.error.URLError:
            continue
        found = set(re.findall(r'href=["\'](?:https://yeseul7\.tistory\.com)?/(\d+)["\']', text))
        before = len(ids)
        ids.update(found)
        if page > 1 and len(ids) == before:
            break
        time.sleep(0.1)
    return ids


def metadata_from_html(post_id, text):
    title = meta_content(text, "og:title") or meta_name(text, "title") or f"Tistory {post_id}"
    title = re.sub(r"\s*::\s*yeseul7 님의 블로그\s*$", "", html.unescape(title)).strip()
    published = meta_content(text, "article:published_time")
    date = None
    if published:
        try:
            date = datetime.fromisoformat(published).strftime("%Y-%m-%d %H:%M:%S %z")
        except ValueError:
            date = published.replace("T", " ")

    category = ""
    tiara = re.search(r"window\.tiara\s*=\s*(\{.*?\})</script>", text, re.S)
    if tiara:
        try:
            entry = json.loads(tiara.group(1)).get("entry") or {}
            category = entry.get("categoryName") or ""
        except json.JSONDecodeError:
            category = ""

    return {"title": title, "date": date, "category": category}


def meta_content(text, prop):
    pattern = rf'<meta\s+[^>]*property=["\']{re.escape(prop)}["\'][^>]*content=["\']([^"\']*)["\']'
    match = re.search(pattern, text, re.I)
    return match.group(1) if match else None


def meta_name(text, name):
    pattern = rf'<meta\s+[^>]*name=["\']{re.escape(name)}["\'][^>]*content=["\']([^"\']*)["\']'
    match = re.search(pattern, text, re.I)
    return match.group(1) if match else None


def extract_body(text):
    start = re.search(r'<div\s+class=["\']tt_article_useless_p_margin contents_style["\'][^>]*>', text)
    if not start:
        return ""
    pos = start.end()
    depth = 1
    tag_re = re.compile(r"</?div\b[^>]*>", re.I)
    for match in tag_re.finditer(text, pos):
        tag = match.group(0)
        if tag.startswith("</"):
            depth -= 1
            if depth == 0:
                return text[pos : match.start()]
        elif not tag.endswith("/>"):
            depth += 1
    return text[pos:]


def normalize_categories(title, category):
    text = f"{title} {category}"
    if any(word in text for word in ["웹해킹", "해초", "포렌식", "리버싱", "Dreamhack", "SQL", "XSS", "CSRF"]):
        return ["CTF/Wargame"]
    if any(word in text for word in ["Devops", "GPT"]):
        return ["Study"]
    if category and category != "카테고리 없음":
        return [category]
    return ["Portfolio"]


def infer_tags(title, category):
    text = f"{title} {category}"
    tags = ["Tistory"]
    checks = [
        ("Writeup", ["과제", "Write-up", "Dreamhack", "해초"]),
        ("Web", ["웹해킹", "XSS", "CSRF", "SQL", "Injection", "Vulnerability"]),
        ("Forensics", ["포렌식", "forensic", "분석"]),
        ("Reversing", ["리버싱", "rev-basic"]),
        ("DevOps", ["Devops"]),
        ("GPT", ["GPT"]),
    ]
    for tag, words in checks:
        if any(word.lower() in text.lower() for word in words):
            tags.append(tag)
    return list(dict.fromkeys(tags))


def image_extension(url, content_type):
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        return suffix
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
    }
    return mapping.get(content_type.split(";")[0].lower(), ".png")


def localize_images(body, post_id, dry_run):
    urls = []
    for match in re.finditer(r'<img\b[^>]*?\bsrc=["\']([^"\']+)["\']', body, re.I):
        src = html.unescape(match.group(1))
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("http") and "no-image-v1.png" not in src:
            urls.append(src)

    replacements = {}
    for index, url in enumerate(dict.fromkeys(urls), start=1):
        if dry_run:
            replacements[url] = url
            continue
        try:
            data, headers = fetch(url)
        except Exception as exc:
            print(f"warn: failed image {url}: {exc}", file=sys.stderr)
            replacements[url] = url
            continue
        ext = image_extension(url, headers.get("Content-Type", ""))
        image_path = IMAGES_DIR / f"tistory-{post_id}-{index:02d}{ext}"
        image_path.parent.mkdir(parents=True, exist_ok=True)
        image_path.write_bytes(data)
        replacements[url] = "/" + image_path.as_posix()
        time.sleep(0.05)

    for original, local in replacements.items():
        body = body.replace(original, local)
        body = body.replace(html.escape(original, quote=True), local)
    return body, len(replacements)


class MarkdownConverter(HTMLParser):
    SAFE_INLINE_TAGS = {"b", "strong", "i", "em", "span", "u", "mark"}
    STRUCTURAL_TAGS = {
        "p",
        "div",
        "figure",
        "blockquote",
        "h1",
        "h2",
        "h3",
        "br",
        "li",
        "ul",
        "ol",
        "pre",
        "code",
        "a",
        "img",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.pre = False
        self.raw_tag_stack = []
        self.link_stack = []

    def format_tag(self, tag, attrs=None, closing=False):
        if closing:
            return f"</{tag}>"
        attrs = attrs or []
        rendered_attrs = []
        for key, value in attrs:
            if value is None:
                rendered_attrs.append(key)
            else:
                rendered_attrs.append(f'{key}="{html.escape(value, quote=True)}"')
        suffix = " " + " ".join(rendered_attrs) if rendered_attrs else ""
        return f"<{tag}{suffix}>"

    def handle_starttag(self, tag, attrs):
        original_attrs = attrs
        attrs = dict(attrs)
        if tag not in self.STRUCTURAL_TAGS and tag not in self.SAFE_INLINE_TAGS:
            self.parts.append(html.escape(self.format_tag(tag, original_attrs)))
            self.raw_tag_stack.append(tag)
            return
        if tag in {"script", "style"}:
            self.parts.append(html.escape(self.format_tag(tag, original_attrs)))
            self.raw_tag_stack.append(tag)
            return
        if self.raw_tag_stack:
            self.parts.append(html.escape(self.format_tag(tag, original_attrs)))
            return
        if tag == "img":
            src = attrs.get("src")
            alt = attrs.get("alt", "")
            if src:
                self.parts.append(f"\n\n![{alt}]({src})\n\n")
        elif tag in {"p", "div", "figure", "blockquote"}:
            self.parts.append("\n\n")
        elif tag in {"h1", "h2"}:
            self.parts.append("\n\n## ")
        elif tag == "h3":
            self.parts.append("\n\n### ")
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "pre":
            self.pre = True
            self.parts.append("\n\n```\n")
        elif tag == "code" and not self.pre:
            self.parts.append("`")
        elif tag == "a":
            self.link_stack.append(attrs.get("href"))

    def handle_endtag(self, tag):
        if self.raw_tag_stack:
            self.parts.append(html.escape(self.format_tag(tag, closing=True)))
            if tag == self.raw_tag_stack[-1]:
                self.raw_tag_stack.pop()
            return
        if tag in {"p", "div", "figure", "blockquote", "h1", "h2", "h3", "li"}:
            self.parts.append("\n\n")
        elif tag == "pre":
            self.pre = False
            self.parts.append("\n```\n\n")
        elif tag == "code" and not self.pre:
            self.parts.append("`")
        elif tag == "a" and self.link_stack:
            href = self.link_stack.pop()
            if href:
                self.parts.append(f" ({href})")

    def handle_data(self, data):
        data = data.replace("\xa0", " ")
        if self.raw_tag_stack:
            self.parts.append(html.escape(data))
        elif self.pre:
            self.parts.append(data)
        else:
            self.parts.append(re.sub(r"[ \t\r\f\v]+", " ", data))

    def markdown(self):
        text = "".join(self.parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        return text.strip() + "\n"


def html_to_markdown(body):
    converter = MarkdownConverter()
    converter.feed(body)
    return escape_raw_html(converter.markdown())


def escape_raw_html(markdown):
    dangerous_tags = (
        "script",
        "iframe",
        "object",
        "embed",
        "form",
        "input",
        "button",
        "svg",
        "math",
        "video",
        "audio",
        "img",
    )
    tag_pattern = "|".join(dangerous_tags)
    markdown = re.sub(
        rf"</?\s*(?:{tag_pattern})\b[^>]*>",
        lambda match: html.escape(match.group(0)),
        markdown,
        flags=re.I,
    )
    markdown = re.sub(
        r"\s(on[a-z]+)\s*=",
        lambda match: f" {html.escape(match.group(1))}=",
        markdown,
        flags=re.I,
    )
    markdown = re.sub(
        r"javascript\s*:",
        "javascript&#58;",
        markdown,
        flags=re.I,
    )
    return markdown


def output_path(post):
    date = post["date"][:10] if post.get("date") else "2026-01-01"
    return POSTS_DIR / f"{date}-tistory-{post['id']}.md"


def build_post(post, markdown):
    title = post["title"]
    category = post.get("category", "")
    categories = normalize_categories(title, category)
    tags = infer_tags(title, category)
    date = post.get("date") or "2026-01-01 09:00:00 +0900"
    source = post["url"]
    front = [
        "---",
        f"title: {yaml_string(title)}",
        f"date: {date}",
        f"categories: {yaml_list(categories)}",
        f"tags: {yaml_list(tags)}",
        "render_with_liquid: false",
        "---",
        "",
        f"> Original: [{source}]({source})",
        "",
    ]
    return "\n".join(front) + "\n" + markdown


def import_posts(args):
    POSTS_DIR.mkdir(exist_ok=True)
    posts = parse_rss()
    ids = collect_ids_from_listing(args.max_pages)
    if args.scan_ids:
        ids.update(str(i) for i in range(1, args.max_id + 1))
    ids.update(posts.keys())

    imported = []
    skipped = []
    for post_id in sorted(ids, key=lambda x: int(x)):
        url = f"{BLOG_URL}/{post_id}"
        try:
            text = fetch_text(url)
        except Exception:
            continue
        if "entryTitle" not in text and 'property="og:title"' not in text:
            continue
        metadata = metadata_from_html(post_id, text)
        body = extract_body(text) or posts.get(post_id, {}).get("body") or ""
        if not body.strip():
            skipped.append((post_id, "no body"))
            continue
        post = {
            "id": post_id,
            "url": url,
            "title": metadata.get("title") or posts.get(post_id, {}).get("title") or f"Tistory {post_id}",
            "date": metadata.get("date") or posts.get(post_id, {}).get("date"),
            "category": metadata.get("category") or posts.get(post_id, {}).get("category", ""),
        }
        body, image_count = localize_images(body, post_id, args.dry_run)
        markdown = html_to_markdown(body)
        path = output_path(post)
        if path.exists() and not args.overwrite:
            skipped.append((post_id, "exists"))
            continue
        if not args.dry_run:
            path.write_text(build_post(post, markdown), encoding="utf-8")
        imported.append((post_id, path.as_posix(), image_count, post["title"]))
        time.sleep(0.1)

    for post_id, path, image_count, title in imported:
        print(f"imported {post_id}: {path} ({image_count} images) {title}")
    for post_id, reason in skipped:
        print(f"skipped {post_id}: {reason}")
    print(f"done: imported={len(imported)} skipped={len(skipped)}")


def main():
    parser = argparse.ArgumentParser(description="Import public Tistory posts into Jekyll.")
    parser.add_argument("--max-pages", type=int, default=8)
    parser.add_argument("--max-id", type=int, default=40)
    parser.add_argument("--scan-ids", action="store_true", default=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    import_posts(args)


if __name__ == "__main__":
    main()
