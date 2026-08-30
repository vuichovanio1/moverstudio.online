#!/usr/bin/env python3
"""Capture homepage + Google SERP screenshots for portfolio projects."""

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "portfolio-2026"
OUT.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    {
        "slug": "roadassistancesofia",
        "url": "https://roadassistancesofia.bg",
        "query": "пътна помощ София roadassistancesofia",
    },
    {
        "slug": "patna-pomosht-kostinbrod",
        "url": "https://patna-pomosht-kostinbrod.bg",
        "query": "пътна помощ Костинброд",
    },
    {
        "slug": "matiyhelp",
        "url": "https://matiyhelp.bg",
        "query": "пътна помощ Годеч matiyhelp",
    },
    {
        "slug": "nikoautogaz",
        "url": "https://nikoautogaz.github.io",
        "query": "niko autogaz София",
    },
    {
        "slug": "re-peat",
        "url": "https://re-peat.store",
        "query": "re-peat store София",
    },
    {
        "slug": "bdinhost",
        "url": "https://bdinhost.com",
        "query": "bdinhost хостинг",
    },
    {
        "slug": "minibagerkb",
        "url": "https://minibagerkb.eu",
        "query": "минибагер Костинброд",
    },
]

VIEWPORT = {"width": 1280, "height": 800}
MOBILE = {"width": 390, "height": 844}


def dismiss_cookies(page) -> None:
    for sel in [
        'button:has-text("Приемам")',
        'button:has-text("Accept")',
        'button:has-text("I agree")',
        'button:has-text("Съгласен")',
        "#L2AGLb",
        '[aria-label="Accept all"]',
    ]:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=1500):
                btn.click(timeout=2000)
                page.wait_for_timeout(500)
                return
        except Exception:
            pass


def shot_site(page, url: str, path: Path) -> bool:
    try:
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(path), full_page=False)
        return True
    except Exception as exc:
        print(f"  site FAIL {url}: {exc}")
        return False


def shot_search(page, query: str, path: Path) -> bool:
    """Use DuckDuckGo HTML — Google blocks headless bots with CAPTCHA."""
    import urllib.parse

    q = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={q}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(path), full_page=False)
        return True
    except Exception as exc:
        print(f"  search FAIL {query}: {exc}")
        return False


def main() -> None:
    ok = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport=VIEWPORT, locale="bg-BG")
        page = ctx.new_page()

        for proj in PROJECTS:
            slug = proj["slug"]
            print(f"-> {slug}")
            site_path = OUT / f"{slug}-site.png"
            google_path = OUT / f"{slug}-search.png"
            if shot_site(page, proj["url"], site_path):
                ok += 1
                print(f"  site OK: {site_path.name}")
            if shot_search(page, proj["query"], google_path):
                ok += 1
                print(f"  search OK: {google_path.name}")

            # mobile hero for key projects
            if slug in ("minibagerkb", "patna-pomosht-kostinbrod", "roadassistancesofia"):
                mobile_path = OUT / f"{slug}-mobile.png"
                page.set_viewport_size(MOBILE)
                if shot_site(page, proj["url"], mobile_path):
                    ok += 1
                    print(f"  mobile OK: {mobile_path.name}")
                page.set_viewport_size(VIEWPORT)

        browser.close()

    print(f"\nDone: {ok} screenshots in {OUT}")


if __name__ == "__main__":
    main()
