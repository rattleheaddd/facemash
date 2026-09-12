"""Embed current women images into food-showdown.html as Base64 data URIs."""

from __future__ import annotations

import base64
import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "women"
HTML_PATH = PROJECT_DIR / "food-showdown.html"
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def build_image_data() -> dict[str, str]:
    images = sorted(
        path
        for path in IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not images:
        raise RuntimeError(f"No supported images found in {IMAGE_DIR}")

    return {
        image.name: (
            f"data:{MIME_TYPES[image.suffix.lower()]};base64,"
            f"{base64.b64encode(image.read_bytes()).decode('ascii')}"
        )
        for image in images
    }


def update_html(image_data: dict[str, str]) -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    start = html.find("<script>")
    end_marker = "</script>"
    end = html.find(end_marker, start)

    if start == -1 or end == -1:
        raise RuntimeError("IMAGE_DATA script block was not found")

    replacement = (
        "<script>const IMAGE_DATA = "
        + json.dumps(image_data, ensure_ascii=True, separators=(",", ":"))
        + ";</script>"
    )
    updated_html = html[:start] + replacement + html[end + len(end_marker) :]
    HTML_PATH.write_text(updated_html, encoding="utf-8")


def main() -> None:
    image_data = build_image_data()
    update_html(image_data)
    size_mb = HTML_PATH.stat().st_size / (1024 * 1024)
    print(f"Embedded {len(image_data)} images into {HTML_PATH.name}")
    print(f"HTML size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
