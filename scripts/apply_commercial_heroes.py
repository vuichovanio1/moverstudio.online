#!/usr/bin/env python3
"""Inject visual hero--page blocks into commercial pages (idempotent)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# file -> (image, eyebrow, h1_html, lead_html, contact_href, h1_id optional)
PAGES = {
    "html-sait.html": {
        "img": "/images/portfolio-2026/roadassistancesofia-site.webp",
        "eyebrow": "Ти си тук, ако искаш нов сайт",
        "h1": "Изработка на HTML сайт от 400€ — без WordPress",
        "h1_id": "main-heading",
        "lead": "Правим <strong>бърз HTML сайт</strong>. Лесен за ползване. Без WordPress. Без месечни такси.",
        "contact": "#contact",
        "extra": (
            '<p class="hero__lead" style="margin-top:-0.5rem;">'
            'Може и: <a href="/sait-vizitka.html">малък сайт / визитка</a> · '
            '<a href="/izrabotka-na-landing-page.html">страница за реклами</a> · '
            '<a href="/services/">всички услуги</a>.</p>'
        ),
    },
    "izrabotka-na-landing-page.html": {
        "img": "/images/portfolio-2026/re-peat-site.webp",
        "eyebrow": "Ти си тук, ако плащаш за реклами",
        "h1": "Изработка на landing page от 400€ — лендинг за Ads",
        "h1_id": "main-heading",
        "lead": "Бавната страница губи парите ти. Ние правим бърза страница за кликовете. От 400€.",
        "contact": "/#contact",
        "extra": (
            '<p class="hero__lead" style="margin-top:-0.5rem;">'
            'Още: <a href="/blog/baven-lending-krade-ads-byudzhet-2026.html">защо губиш пари</a> · '
            '<a href="/services/">всички услуги</a>.</p>'
        ),
    },
    "sait-vizitka.html": {
        "img": "/images/portfolio-2026/nikoautogaz-site.webp",
        "eyebrow": "Ти си тук, ако искаш малък сайт",
        "h1": "Изработка на портфолио и сайт визитка от 400€",
        "h1_id": "main-heading",
        "lead": "Да те намират. Да ти пишат. Без WordPress. От <strong>400€</strong>.",
        "contact": "/#contact",
        "extra": "",
    },
    "migratsiya-na-sait.html": {
        "img": "/images/portfolio-2026/bdinhost-site.webp",
        "eyebrow": "Ти си тук, ако искаш смяна от WordPress",
        "h1": "Миграция от WordPress към HTML от 200€ — без downtime",
        "h1_id": "main-heading",
        "lead": "Взимаме стария сайт. Правим нов, бърз. Старите линкове продължават да работят. Обикновено <strong>200–500€</strong>.",
        "contact": "#contact",
        "extra": (
            '<p class="hero__lead" style="margin-top:-0.5rem;">'
            'Не искаш WordPress изобщо? Виж '
            '<a href="/wordpress-alternativa.html">сайт без WordPress</a>.</p>'
        ),
    },
    "wordpress-alternativa.html": {
        "img": "/images/portfolio-2026/bdinhost-site.webp",
        "eyebrow": "Ти си тук, ако не искаш WordPress",
        "h1": "Алтернатива на WordPress — HTML сайт без месечни такси",
        "h1_id": "main-heading-wp",
        "lead": "Правим бърз сайт без WordPress. Без месечни такси. От 400€. Не си сигурен? Пиши ни.",
        "contact": "/#contact",
        "extra": "",
    },
    "izrabotka-na-sait.html": {
        "img": "/images/portfolio-2026/patna-pomosht-kostinbrod-site.webp",
        "eyebrow": "Пакети и цени на едно място",
        "h1": None,  # keep existing H1 from page via capture
        "contact": "/#contact",
        "lead": "Избери пакет. Или ни пиши — ще ти кажем кое е за теб.",
        "extra": "",
    },
    "korporativen-sait.html": {
        "img": "/images/portfolio-2026/patna-pomosht-kostinbrod-site.webp",
        "eyebrow": "Ти си тук, ако искаш по-голям фирмен сайт",
        "h1": None,
        "contact": "/#contact",
        "lead": "Повече страници, повече доверие, същата бързина. Без WordPress.",
        "extra": "",
    },
    "seo-optimizacia.html": {
        "img": "/images/portfolio-2026/matiyhelp-site.webp",
        "eyebrow": "Ти си тук, ако искаш да те намират в Google",
        "h1": None,
        "contact": "/#contact",
        "lead": "Техническо и локално SEO. Ясни стъпки. От 100€.",
        "extra": "",
    },
    "izrabotka-na-sait-sofia.html": {
        "img": "/images/portfolio-2026/roadassistancesofia-site.webp",
        "eyebrow": "Изработка на сайт · София",
        "h1": None,
        "contact": "/#contact",
        "lead": "Бърз HTML сайт за бизнес в София. От 400€. Без месечни такси.",
        "extra": "",
    },
    "izrabotka-na-sait-plovdiv.html": {
        "img": "/images/portfolio-2026/re-peat-site.webp",
        "eyebrow": "Изработка на сайт · Пловдив",
        "h1": None,
        "contact": "/#contact",
        "lead": "Бърз HTML сайт за бизнес в Пловдив. От 400€. Без месечни такси.",
        "extra": "",
    },
    "izrabotka-na-sait-varna.html": {
        "img": "/images/portfolio-2026/nikoautogaz-site.webp",
        "eyebrow": "Изработка на сайт · Варна",
        "h1": None,
        "contact": "/#contact",
        "lead": "Бърз HTML сайт за бизнес във Варна. От 400€. Без месечни такси.",
        "extra": "",
    },
    "izrabotka-na-sait-burgas.html": {
        "img": "/images/portfolio-2026/minibagerkb-site.webp",
        "eyebrow": "Изработка на сайт · Бургас",
        "h1": None,
        "contact": "/#contact",
        "lead": "Бърз HTML сайт за бизнес в Бургас. От 400€. Без месечни такси.",
        "extra": "",
    },
}

BREADCRUMB_RE = re.compile(
    r'(<nav\s+class="breadcrumbs"[^>]*>.*?</nav>)',
    re.DOTALL | re.IGNORECASE,
)
EXISTING_HERO_PAGE_RE = re.compile(
    r'<section\s+class="hero hero--visual hero--page"[^>]*>.*?</section>\s*',
    re.DOTALL | re.IGNORECASE,
)
H1_RE = re.compile(r"<h1([^>]*)>(.*?)</h1>", re.DOTALL | re.IGNORECASE)


def build_hero(meta: dict, h1_text: str, h1_attrs: str = "") -> str:
    h1_id = meta.get("h1_id")
    attrs = h1_attrs.strip()
    if h1_id and "id=" not in attrs:
        attrs = (attrs + f' id="{h1_id}"').strip()
    attr_part = f" {attrs}" if attrs else ""
    extra = meta.get("extra") or ""
    return f'''<section class="hero hero--visual hero--page" aria-labelledby="{(h1_id or "page-heading")}">
  <div class="hero__content container">
    <p class="hero__eyebrow">{meta["eyebrow"]}</p>
    <h1{attr_part}>{h1_text}</h1>
    <p class="hero__lead">{meta["lead"]}</p>
    {extra}
    <div class="hero__actions">
      <a href="{meta["contact"]}" class="btn btn--primary">Пиши ни</a>
      <a href="/calculator.html" class="btn btn--secondary">Колко струва?</a>
    </div>
  </div>
</section>
'''


def strip_old_top(html: str, filename: str) -> str:
    """Remove obsolete banners / old heroes before content body starts."""
    # Remove notice/banner blocks that sit right after breadcrumbs (once)
    html = re.sub(
        r'(</nav>\s*)'
        r'(?:<div class="container"[^>]*>\s*<p class="notice"[^>]*>.*?</p>\s*</div>\s*)',
        r"\1",
        html,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Old brand strip banners before/inside main
    html = re.sub(
        r'<div style="max-width: var\(--max-width\);[^"]*"[^>]*>\s*<p[^>]*>.*?</p>\s*</div>\s*',
        "",
        html,
        count=2,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Remove first classic .hero section (not hero--visual) for pages that had blueprint hero
    if filename in {
        "izrabotka-na-landing-page.html",
        "sait-vizitka.html",
        "migratsiya-na-sait.html",
    }:
        html = re.sub(
            r'<section class="hero">.*?</section>\s*',
            "",
            html,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )
    return html


def process(path: Path, meta: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if "hero--visual hero--page" in text:
        # refresh in place
        text = EXISTING_HERO_PAGE_RE.sub("", text, count=1)

    text = strip_old_top(text, path.name)

    m = BREADCRUMB_RE.search(text)
    if not m:
        print(f"SKIP no breadcrumbs: {path.name}")
        return False

    h1_match = H1_RE.search(text[m.end() : m.end() + 4000])
    if meta.get("h1"):
        h1_text = meta["h1"]
        h1_attrs = f'id="{meta["h1_id"]}"' if meta.get("h1_id") else ""
        # remove the old first h1 after breadcrumb so we don't duplicate
        if h1_match:
            abs_start = m.end() + h1_match.start()
            abs_end = m.end() + h1_match.end()
            text = text[:abs_start] + text[abs_end:]
            # also drop leftover lead/actions that followed old h1 for html-sait
            if path.name == "html-sait.html":
                text = re.sub(
                    r'(</nav>\s*)'
                    r'(?:\s*<p[^>]*>.*?</p>\s*){0,3}'
                    r'(?:<div class="hero__actions"[^>]*>.*?</div>\s*)?',
                    r"\1",
                    text,
                    count=1,
                    flags=re.DOTALL | re.IGNORECASE,
                )
            if path.name == "wordpress-alternativa.html":
                # remove duplicate quick-answer block that repeated the same message
                text = re.sub(
                    r'<div class="quick-answer"[^>]*>.*?</div>\s*',
                    "",
                    text,
                    count=1,
                    flags=re.DOTALL | re.IGNORECASE,
                )
                # remove leftover article>h1 if still present near top
                text = re.sub(
                    r'(<article>\s*)<h1[^>]*>.*?</h1>\s*',
                    r"\1",
                    text,
                    count=1,
                    flags=re.DOTALL | re.IGNORECASE,
                )
    else:
        if not h1_match:
            print(f"SKIP no h1: {path.name}")
            return False
        h1_text = h1_match.group(2).strip()
        h1_attrs = h1_match.group(1).strip()
        abs_start = m.end() + h1_match.start()
        abs_end = m.end() + h1_match.end()
        text = text[:abs_start] + text[abs_end:]

    # Re-find breadcrumb after edits
    m = BREADCRUMB_RE.search(text)
    if not m:
        print(f"SKIP breadcrumb lost: {path.name}")
        return False

    hero = build_hero(meta, h1_text, h1_attrs)
    text = text[: m.end()] + "\n" + hero + text[m.end() :]

    # cache bust css if present
    text = re.sub(r"/css/site\.css\?v=[^\"']+", "/css/site.css?v=20261124fx2", text)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"OK  {path.name}")
        return True
    print(f"—   {path.name}")
    return False


def main() -> None:
    n = 0
    for name, meta in PAGES.items():
        if process(ROOT / name, meta):
            n += 1
    print(f"Done. {n}/{len(PAGES)} updated.")


if __name__ == "__main__":
    main()
