#!/usr/bin/env python3
"""Sync shared header/footer chrome across all HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "_partials"
HEADER = (PARTIALS / "header.html").read_text(encoding="utf-8")
FOOTER = (PARTIALS / "footer.html").read_text(encoding="utf-8")

# Pathname (as served) → nav data-nav key
ACTIVE_MAP = {
    "/": None,
    "/index.html": None,
    "/services/": "services",
    "/services/index.html": "services",
    "/calculator.html": "calculator",
    "/case-studies.html": "cases",
    "/blog/": "blog",
    "/blog/index.html": "blog",
    "/faq.html": "faq",
    "/about.html": "about",
}

# Commercial pages that get breadcrumb + related block if missing
COMMERCIAL = {
    "html-sait.html": {
        "label": "Нов сайт",
        "related": [
            ("/izrabotka-na-landing-page.html", "Страница за реклами"),
            ("/sait-vizitka.html", "Малък сайт / визитка"),
            ("/wordpress-alternativa.html", "Сайт без WordPress"),
        ],
    },
    "izrabotka-na-landing-page.html": {
        "label": "Страница за реклами",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/sait-vizitka.html", "Малък сайт / визитка"),
            ("/migratsiya-na-sait.html", "Смяна от WordPress"),
        ],
    },
    "sait-vizitka.html": {
        "label": "Малък сайт",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/izrabotka-na-landing-page.html", "Страница за реклами"),
            ("/korporativen-sait.html", "По-голям фирмен сайт"),
        ],
    },
    "migratsiya-na-sait.html": {
        "label": "Смяна от WordPress",
        "related": [
            ("/wordpress-alternativa.html", "Сайт без WordPress"),
            ("/html-sait.html", "Нов сайт"),
            ("/seo-optimizacia.html", "Да те намират в Google"),
        ],
    },
    "wordpress-alternativa.html": {
        "label": "Без WordPress",
        "related": [
            ("/migratsiya-na-sait.html", "Смяна от WordPress"),
            ("/html-sait.html", "Нов сайт"),
            ("/sait-vizitka.html", "Малък сайт / визитка"),
        ],
    },
    "izrabotka-na-sait.html": {
        "label": "Пакети и цени",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/sait-vizitka.html", "Малък сайт / визитка"),
            ("/korporativen-sait.html", "По-голям фирмен сайт"),
        ],
    },
    "korporativen-sait.html": {
        "label": "Фирмен сайт",
        "related": [
            ("/sait-vizitka.html", "Малък сайт / визитка"),
            ("/html-sait.html", "Нов сайт"),
            ("/seo-optimizacia.html", "Да те намират в Google"),
        ],
    },
    "seo-optimizacia.html": {
        "label": "Google",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/migratsiya-na-sait.html", "Смяна от WordPress"),
            ("/izrabotka-na-sait-sofia.html", "София"),
        ],
    },
    "izrabotka-na-sait-sofia.html": {
        "label": "София",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/izrabotka-na-sait-plovdiv.html", "Пловдив"),
            ("/izrabotka-na-sait-varna.html", "Варна"),
        ],
    },
    "izrabotka-na-sait-plovdiv.html": {
        "label": "Пловдив",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/izrabotka-na-sait-sofia.html", "София"),
            ("/izrabotka-na-sait-varna.html", "Варна"),
        ],
    },
    "izrabotka-na-sait-varna.html": {
        "label": "Варна",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/izrabotka-na-sait-sofia.html", "София"),
            ("/izrabotka-na-sait-burgas.html", "Бургас"),
        ],
    },
    "izrabotka-na-sait-burgas.html": {
        "label": "Бургас",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/izrabotka-na-sait-sofia.html", "София"),
            ("/izrabotka-na-sait-varna.html", "Варна"),
        ],
    },
    "services/index.html": {
        "label": "Услуги",
        "related": [
            ("/html-sait.html", "Нов сайт"),
            ("/migratsiya-na-sait.html", "Смяна от WordPress"),
            ("/calculator.html", "Пресметни цена"),
        ],
        "breadcrumb_only_home": True,
    },
}

SKIP_RE = re.compile(
    r'(?:<a\s+href="#main"\s+class="skip-link">.*?</a>\s*)?'
    r'(?:<div\s+class="site-fx"[^>]*>.*?</div>\s*)?'
    r'<header\s+class="site-header">.*?</header>',
    re.DOTALL | re.IGNORECASE,
)
FOOTER_RE = re.compile(
    r'<footer\s+class="site-footer">.*?</footer>',
    re.DOTALL | re.IGNORECASE,
)
MAIN_OPEN_RE = re.compile(r'(<main\b[^>]*>)', re.IGNORECASE)
RELATED_RE = re.compile(
    r'<section\s+class="related-services"[^>]*>.*?</section>\s*',
    re.DOTALL | re.IGNORECASE,
)
BREADCRUMB_RE = re.compile(
    r'<nav\s+class="breadcrumbs"[^>]*>.*?</nav>\s*',
    re.DOTALL | re.IGNORECASE,
)
CSS_VER_RE = re.compile(r'/css/site\.css\?v=[^"\']+')
JS_VER_RE = re.compile(r'/js/site\.js\?v=[^"\']+')

CSS_VER = "20261124fx3"
JS_VER = "20261124fx3"


def served_path(rel: Path) -> str:
    parts = rel.as_posix()
    if parts.endswith("/index.html"):
        return "/" + parts[: -len("index.html")]
    if parts == "index.html":
        return "/"
    return "/" + parts


def is_homepage(rel: Path) -> bool:
    return rel.as_posix() in ("index.html",)


def contact_href(rel: Path, page_html: str = "") -> str:
    if is_homepage(rel):
        return "#contact"
    # Prefer in-page contact when the page has its own form/section
    if re.search(r'id=["\']contact["\']', page_html, re.IGNORECASE):
        return "#contact"
    return "/#contact"


def active_key(rel: Path) -> str | None:
    sp = served_path(rel)
    if sp in ACTIVE_MAP:
        return ACTIVE_MAP[sp]
    if sp.startswith("/blog/"):
        return "blog"
    if sp.startswith("/services"):
        return "services"
    # Commercial pages highlight Services
    name = rel.name if rel.parent == ROOT else rel.as_posix()
    if name in COMMERCIAL or rel.as_posix() in COMMERCIAL:
        return "services"
    # Root commercial-ish pages
    if rel.parent == ROOT and rel.name in COMMERCIAL:
        return "services"
    return None


def render_header(rel: Path, page_html: str = "") -> str:
    html = HEADER.replace("{{CONTACT_HREF}}", contact_href(rel, page_html))
    key = active_key(rel)
    if key:
        html = re.sub(
            rf'(<a href="[^"]*" data-nav="{key}")',
            r'\1 class="is-active" aria-current="page"',
            html,
            count=1,
        )
    return html.strip() + "\n"


def render_footer(rel: Path, page_html: str = "") -> str:
    return FOOTER.replace("{{CONTACT_HREF}}", contact_href(rel, page_html)).strip() + "\n"


def breadcrumb_html(rel: Path, meta: dict) -> str:
    label = meta["label"]
    if meta.get("breadcrumb_only_home"):
        return (
            '<nav class="breadcrumbs" aria-label="Breadcrumb">\n'
            '  <a href="/">Начало</a>\n'
            '  <span class="breadcrumbs__sep" aria-hidden="true">/</span>\n'
            f'  <span aria-current="page">{label}</span>\n'
            "</nav>\n"
        )
    return (
        '<nav class="breadcrumbs" aria-label="Breadcrumb">\n'
        '  <a href="/">Начало</a>\n'
        '  <span class="breadcrumbs__sep" aria-hidden="true">/</span>\n'
        '  <a href="/services/">Услуги</a>\n'
        '  <span class="breadcrumbs__sep" aria-hidden="true">/</span>\n'
        f'  <span aria-current="page">{label}</span>\n'
        "</nav>\n"
    )


def related_html(meta: dict) -> str:
    links = "\n".join(
        f'      <a class="related-services__link" href="{href}">{text}</a>'
        for href, text in meta["related"]
    )
    return (
        '<section class="related-services" aria-labelledby="related-heading">\n'
        '  <div class="container">\n'
        '    <h2 id="related-heading" class="related-services__title">Още нещо полезно</h2>\n'
        '    <div class="related-services__grid">\n'
        f"{links}\n"
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
    )


def commercial_key(rel: Path) -> str | None:
    posix = rel.as_posix()
    if posix in COMMERCIAL:
        return posix
    if rel.name in COMMERCIAL and rel.parent == ROOT:
        return rel.name
    return None


def inject_breadcrumb_related(html: str, rel: Path) -> str:
    key = commercial_key(rel)
    if not key:
        return html
    meta = COMMERCIAL[key]

    # Strip existing then re-insert after <main>
    html = BREADCRUMB_RE.sub("", html)
    html = RELATED_RE.sub("", html)

    crumb = breadcrumb_html(rel, meta)
    m = MAIN_OPEN_RE.search(html)
    if m:
        insert_at = m.end()
        html = html[:insert_at] + "\n" + crumb + html[insert_at:]

    related = related_html(meta)
    # Insert related before footer
    fm = FOOTER_RE.search(html)
    if fm:
        html = html[: fm.start()] + related + "\n" + html[fm.start() :]
    return html


def process(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    original = text

    if not SKIP_RE.search(text):
        print(f"SKIP (no header): {rel}")
        return False
    if not FOOTER_RE.search(text):
        print(f"SKIP (no footer): {rel}")
        return False

    text = SKIP_RE.sub(lambda _: render_header(rel, original), text, count=1)
    # Inject breadcrumb/related before replacing footer so markers stay findable
    text = inject_breadcrumb_related(text, rel)
    text = FOOTER_RE.sub(lambda _: render_footer(rel, original), text, count=1)

    text = CSS_VER_RE.sub(f"/css/site.css?v={CSS_VER}", text)
    text = JS_VER_RE.sub(f"/js/site.js?v={JS_VER}", text)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"OK  {rel}")
        return True
    print(f"—   {rel} (unchanged)")
    return False


def main() -> None:
    files = sorted(ROOT.rglob("*.html"))
    # Skip partials themselves
    files = [f for f in files if "_partials" not in f.parts]
    changed = 0
    for f in files:
        if process(f):
            changed += 1
    print(f"\nDone. {changed}/{len(files)} files updated.")


if __name__ == "__main__":
    main()
