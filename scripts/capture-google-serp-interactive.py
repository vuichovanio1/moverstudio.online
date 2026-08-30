#!/usr/bin/env python3
"""
Interactive Google SERP screenshots for portfolio projects.

Google blocks headless bots — this opens a REAL Chrome window.
You solve CAPTCHA / cookies once; a persistent profile helps for later searches.

Usage:
  python scripts/capture-google-serp-interactive.py
  python scripts/capture-google-serp-interactive.py --only patna-pomosht-kostinbrod
  python scripts/capture-google-serp-interactive.py --start 3   # skip first 2

Controls (in terminal after each page loads):
  ENTER  = save screenshot
  s      = skip this project
  q      = quit
"""

from __future__ import annotations

import argparse
import sys
import urllib.parse
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "portfolio-2026"
PROFILE = ROOT / ".playwright-google-profile"
OUT.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    ("roadassistancesofia", "пътна помощ София"),
    ("patna-pomosht-kostinbrod", "пътна помощ Костинброд"),
    ("matiyhelp", "пътна помощ Годеч"),
    ("nikoautogaz", "автогаз София niko"),
    ("re-peat", "re-peat store София"),
    ("bdinhost", "bdinhost хостинг"),
    ("minibagerkb", "минибагер Костинброд"),
]

VIEWPORT = {"width": 1280, "height": 900}


def to_webp(png: Path) -> Path:
    webp = png.with_suffix(".webp")
    Image.open(png).save(webp, "WEBP", quality=86, method=6)
    return webp


def google_url(query: str) -> str:
    q = urllib.parse.quote_plus(query)
    return f"https://www.google.com/search?q={q}&hl=bg&gl=bg&pws=0"


def prompt(msg: str) -> str:
    try:
        return input(msg).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nStopped.")
        sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive Google SERP capture")
    parser.add_argument("--only", help="Single project slug")
    parser.add_argument("--start", type=int, default=1, help="Start from project N (1-based)")
    args = parser.parse_args()

    items = PROJECTS
    if args.only:
        items = [x for x in PROJECTS if x[0] == args.only]
        if not items:
            print(f"Unknown slug: {args.only}")
            sys.exit(1)
    else:
        items = PROJECTS[args.start - 1 :]

    print("=" * 62)
    print("  GOOGLE SERP — интерактивен режим")
    print("=" * 62)
    print("  • Ще се отвори Chrome (не headless)")
    print("  • Реши CAPTCHA / бисквитки ако се появят")
    print("  • Когато видиш резултатите → ENTER в терминала")
    print("  • s = пропусни | q = изход")
    print(f"  • Профил (запомня сесия): {PROFILE}")
    print(f"  • Изход: {OUT}")
    print("=" * 62)

    PROFILE.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            headless=False,
            viewport=VIEWPORT,
            locale="bg-BG",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        saved = 0
        for slug, query in items:
            png = OUT / f"{slug}-google.png"
            webp = png.with_suffix(".webp")

            print(f"\n[{slug}]")
            print(f"  Търсене: {query}")
            print(f"  URL: {google_url(query)}")

            if webp.exists():
                ans = prompt("  WebP вече съществува. Презапис? (y/n): ")
                if ans != "y":
                    print("  skipped (exists)")
                    continue

            page.goto(google_url(query), wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(800)

            cmd = prompt("  ENTER=скрийншот | s=пропусни | q=изход: ")
            if cmd == "q":
                break
            if cmd == "s":
                continue

            page.screenshot(path=str(png), full_page=False)
            out = to_webp(png)
            print(f"  OK: {out.name}")
            saved += 1

        ctx.close()

    print(f"\nГотово: {saved} Google SERP файла в {OUT}")
    print("След това кажи на агента да ги вкара в case-studies.html")


if __name__ == "__main__":
    main()
