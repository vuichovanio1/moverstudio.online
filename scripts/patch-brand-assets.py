#!/usr/bin/env python3
"""Update favicon cache-bust and unify OG image URLs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLACEMENTS = [
    ("og-image.png?v=1", "og-image.png?v=2"),
    ('href="/favicon.svg"', 'href="/favicon.svg?v=2"'),
    ('href="/images/favicon.ico"', 'href="/images/favicon.ico?v=2"'),
    ('href="/images/favicon-32.png"', 'href="/images/favicon-32.png?v=2"'),
    ('href="/images/apple-touch-icon.png"', 'href="/images/apple-touch-icon.png?v=2"'),
    (
        "https://moverstudio.online/images/gsc-patna-pomosht.webp",
        "https://moverstudio.online/og-image.png?v=2",
    ),
]

for pattern in ("**/*.html", "scripts/*.py"):
    for path in ROOT.glob(pattern):
        if path.name == "patch-brand-assets.py":
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
