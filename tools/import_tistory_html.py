#!/usr/bin/env python3
import argparse
import html
import re
import shutil
import urllib.parse
from pathlib import Path

import import_tistory as importer


IMAGES_DIR = Path("assets/img/posts/tistory")


def source_url(text, fallback):
    for prop in ["og:url", "article:pc_url", "article:mobile_url"]:
        value = importer.meta_content(text, prop)
        if value:
            return html.unescape(value)
    match = re.search(r"saved from url=\(\d+\)([^ ]+)\s*-->", text)
    return match.group(1) if match else fallback


def localize_saved_images(body, html_path, post_id):
    urls = []
    for match in re.finditer(r'<img\b[^>]*?\bsrc=["\']([^"\']+)["\']', body, re.I):
        src = html.unescape(match.group(1))
        if src.startswith("http") or src.startswith("//"):
            continue
        if "no-image-v1.png" in src:
            continue
        urls.append(src)

    replacements = {}
    for index, src in enumerate(dict.fromkeys(urls), start=1):
        src_path = Path(urllib.parse.unquote(src))
        if not src_path.is_absolute():
            src_path = html_path.parent / src_path
        src_path = src_path.resolve()

        if not src_path.exists():
            print(f"warn: missing image {src_path}")
            replacements[src] = src
            continue

        suffix = src_path.suffix.lower() or ".png"
        image_path = IMAGES_DIR / f"tistory-{post_id}-{index:02d}{suffix}"
        image_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, image_path)
        replacements[src] = "/" + image_path.as_posix()

    for original, local in replacements.items():
        body = body.replace(original, local)
        body = body.replace(html.escape(original, quote=True), local)

    return body, len(replacements)


def import_html(html_path, post_id, overwrite=False):
    text = html_path.read_text(encoding="utf-8", errors="replace")
    metadata = importer.metadata_from_html(post_id, text)
    body = importer.extract_body(text)
    if not body.strip():
        raise RuntimeError(f"no article body found in {html_path}")

    body, image_count = localize_saved_images(body, html_path, post_id)
    markdown = importer.html_to_markdown(body)
    post = {
        "id": post_id,
        "url": source_url(text, f"https://yeseul7.tistory.com/{post_id}"),
        "title": metadata.get("title") or html_path.stem,
        "date": metadata.get("date"),
        "category": metadata.get("category") or "",
    }
    output_path = importer.output_path(post)
    if output_path.exists() and not overwrite:
        raise RuntimeError(f"{output_path} already exists; use --overwrite")
    output_path.write_text(importer.build_post(post, markdown), encoding="utf-8")
    print(f"imported {post_id}: {output_path} ({image_count} images) {post['title']}")


def main():
    parser = argparse.ArgumentParser(description="Import saved Tistory HTML files.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("items", nargs="+", help="POST_ID=HTML_PATH")
    args = parser.parse_args()

    for item in args.items:
        post_id, path = item.split("=", 1)
        import_html(Path(path).expanduser(), post_id, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
