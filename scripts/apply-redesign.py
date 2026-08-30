#!/usr/bin/env python3
"""Apply v2 header/footer + shared CSS to all HTML pages except index.html."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_LINK = '<a href="#main" class="skip-link">Прескочи към съдържанието</a>'

HEADER = """<header class="site-header">
  <div class="site-header__inner">
    <a href="/" class="site-logo">MOVER Studio</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Меню">
      <span></span><span></span><span></span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Основна навигация">
      <a href="/izrabotka-na-sait.html">Услуги</a>
      <a href="/calculator.html">Калкулатор</a>
      <a href="/case-studies.html">Case Studies</a>
      <a href="/blog/">Блог</a>
      <a href="/faq.html">ЧЗВ</a>
      <a href="/about.html">За нас</a>
      <a href="/#contact" class="nav-cta">Контакт</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-links">
      <a href="/izrabotka-na-sait.html">Изработка на сайт</a>
      <a href="/sait-vizitka.html">Визитка</a>
      <a href="/korporativen-sait.html">Корпоративен</a>
      <a href="/calculator.html">Калкулатор</a>
      <a href="/blog/">Блог</a>
      <a href="/faq.html">ЧЗВ</a>
      <a href="/about.html">За нас</a>
      <a href="/wordpress-alternativa.html">WordPress алтернатива</a>
      <a href="/seo-optimizacia.html">SEO</a>
    </div>
    <p class="footer-terminal" style="margin-top:1.5rem;">
      © 2026 MOVER Studio · HTML без WordPress · цел 95–100 PageSpeed<br>
      Хостинг: <a href="https://bdinhost.com" target="_blank" rel="noopener">BDinHost</a> ·
      <a href="https://patna-pomosht-kostinbrod.bg/" target="_blank" rel="noopener">Пътна помощ Костинброд</a> ·
      <a href="https://minibagerkb.eu/" target="_blank" rel="noopener">Минибагер Костинброд</a>
    </p>
  </div>
</footer>"""

STYLE_RE = re.compile(r"<style>.*?</style>", re.DOTALL | re.IGNORECASE)
SKIP_LINK_RE = re.compile(
    r'<a href="#main" class="skip-link"[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE
)
HEADER_RE = re.compile(r"<header[^>]*>.*?</header>", re.DOTALL | re.IGNORECASE)
FOOTER_RE = re.compile(r"<footer[^>]*>.*?</footer>", re.DOTALL | re.IGNORECASE)


def css_block(is_calculator: bool) -> str:
    lines = [
        '  <link rel="preload" href="/fonts/share-tech-mono-v16-latin-regular.woff2" as="font" type="font/woff2" crossorigin>',
        '  <link rel="stylesheet" href="/css/site.css">',
        '  <link rel="stylesheet" href="/css/pages.css">',
    ]
    if is_calculator:
        lines.append('  <link rel="stylesheet" href="/css/calculator.css">')
    return "\n".join(lines)


def process(path: Path) -> bool:
    if path.name == "index.html" and path.parent == ROOT:
        return False

    text = path.read_text(encoding="utf-8")
    original = text
    is_calculator = path.name == "calculator.html"

    text = STYLE_RE.sub("", text)

    if "/css/site.css" not in text:
        anchor = '<link rel="apple-touch-icon" href="/images/apple-touch-icon.png?v=2">'
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + css_block(is_calculator))
        else:
            # fallback: after last favicon link
            m = re.search(r'<link rel="icon"[^>]+>\s*', text)
            if m:
                insert_at = m.end()
                text = text[:insert_at] + "\n" + css_block(is_calculator) + text[insert_at:]

    if SKIP_LINK_RE.search(text):
        text = SKIP_LINK_RE.sub(SKIP_LINK, text)
    elif "<body>" in text:
        text = text.replace("<body>", "<body>\n\n" + SKIP_LINK + "\n", 1)

    if HEADER_RE.search(text):
        text = HEADER_RE.sub(HEADER, text, count=1)

    if FOOTER_RE.search(text):
        text = FOOTER_RE.sub(FOOTER, text, count=1)

    if "/js/site.js" not in text:
        text = text.replace("</body>", '<script src="/js/site.js" defer></script>\n</body>')

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name.endswith(".bak-pre-redesign"):
            continue
        if process(path):
            updated.append(path.relative_to(ROOT))

    print(f"Updated {len(updated)} files:")
    for p in updated:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
