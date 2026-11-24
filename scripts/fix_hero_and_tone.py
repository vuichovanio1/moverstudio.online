#!/usr/bin/env python3
"""Remove bleed hero screenshots + emoji headings; shorten dense SEO walls."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMERCIAL = [
    "html-sait.html",
    "izrabotka-na-landing-page.html",
    "sait-vizitka.html",
    "migratsiya-na-sait.html",
    "wordpress-alternativa.html",
    "izrabotka-na-sait.html",
    "korporativen-sait.html",
    "seo-optimizacia.html",
    "izrabotka-na-sait-sofia.html",
    "izrabotka-na-sait-plovdiv.html",
    "izrabotka-na-sait-varna.html",
    "izrabotka-na-sait-burgas.html",
    "services/index.html",
    "index.html",
]

# Emoji / symbol prefixes on headings
EMOJI_H_RE = re.compile(
    r"(<(?:h[1-6])[^>]*>)\s*(?:[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]+|\u26A1|\u2694|\u2699|\u2705|\u274C|\u2753|\u2757|\u2B50)\s*",
)

HERO_MEDIA_RE = re.compile(
    r'\s*<div class="hero__media"[^>]*>.*?</div>\s*',
    re.DOTALL | re.IGNORECASE,
)

# Long technical wall under first card on html-sait
HTML_SAIT_WALL = re.compile(
    r'(<h2>Защо HTML сайт\?</h2>\s*<ul>.*?</ul>\s*)'
    r'<p style="margin-top: 1rem; font-size: 0\.9rem; color: var\(--muted\);">.*?</p>',
    re.DOTALL,
)

HTML_SAIT_WALL_REPL = (
    r"\1"
    r'<p style="margin-top: 1rem;">По-бърз сайт. По-евтин дългосрочно. Без месечни WordPress такси.</p>'
)


def strip_emoji_headings(text: str) -> str:
    # Repeatedly strip common emoji/symbols right after opening heading tags
    def repl(m: re.Match) -> str:
        return m.group(1)

    # broader: any emoji sequence after > of h2/h3
    text = re.sub(
        r"(<(?:h[2-3])[^>]*>)\s*(?:[\U0001F300-\U0001FAFF\u2600-\u27BF\ufe0f\u200d\u23f1\u23f3\u2702-\u27b0]+)\s*",
        repl,
        text,
    )
    # Explicit leftover symbols used on this site
    for sym in ("⚡", "💰", "🏗️", "📊", "⚔️", "❓", "🔗", "🧑‍💼", "🎨", "🚀", "🛡️", "⏱️", "🛠️", "🤝", "📋"):
        text = text.replace(f">{sym} ", "")
        text = text.replace(sym, "")
    return text


def simplify_html_sait(text: str) -> str:
    text = HTML_SAIT_WALL.sub(HTML_SAIT_WALL_REPL, text, count=1)
    # Process section — keep short bullets, drop overly technical jargon lines tone
    text = text.replace(
        "<li><strong>Разработка:</strong> Чист HTML5, CSS3 и Vanilla JavaScript — без библиотеки</li>",
        "<li><strong>Разработка:</strong> Чист, бърз код — без тежки системи</li>",
    )
    text = text.replace(
        "<li><strong>Оптимизация:</strong> Inline CSS, WebP изображения, lazy loading, schema markup</li>",
        "<li><strong>Оптимизация:</strong> Леки снимки и бързо зареждане на телефон</li>",
    )
    text = text.replace(
        "<li><strong>Тестване:</strong> PageSpeed Insights, Core Web Vitals, mobile responsiveness</li>",
        "<li><strong>Тестване:</strong> Проверка на скорост и мобилен вид</li>",
    )
    text = text.replace(
        "<li>Zero external dependencies — всичко е inline</li>",
        "<li>Лек сайт — без излишни добавки</li>",
    )
    text = text.replace(
        "<li>Vanilla JS калкулатор без React/Vue overhead</li>",
        "<li>Калкулатор за оферти — работи бързо в браузъра</li>",
    )
    text = text.replace(
        "<li>Client-side изчисления — никакви API calls</li>",
        "<li>Без бавни външни услуги</li>",
    )
    text = text.replace(
        "<li>AggregateRating микроразметка за доверие</li>",
        "<li>Google отзиви — видими на сайта</li>",
    )
    text = text.replace(
        "<li>11 локационни страници с unique H1/title/meta</li>",
        "<li>Отделни страници по населени места</li>",
    )
    return text


def simplify_sait_vizitka(text: str) -> str:
    # Soften the heavy SEO paragraph block in examples
    text = re.sub(
        r"(<div class=\"quick-answer\">.*?<p>\s*Допълнителен пример:.*?</p>\s*)"
        r"<p>\s*SEO слоят е ориентиран към local intent.*?</p>\s*",
        r"\1",
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = text.replace(
        "Проектът използва optimized lightweight external stylesheets/JS, custom SVG renderer и HTML-first архитектура\n"
        "        без външни библиотеки или CDN зависимости.",
        "Лек и бърз сайт — направен за реални посещения в обекта, не за онлайн магазин.",
    )
    return text


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = HERO_MEDIA_RE.sub("\n", text)
    text = strip_emoji_headings(text)
    if path.name == "html-sait.html":
        text = simplify_html_sait(text)
    if path.name == "sait-vizitka.html":
        text = simplify_sait_vizitka(text)
    text = re.sub(r"/css/site\.css\?v=[^\"']+", "/css/site.css?v=20261124fx3", text)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("OK ", path.as_posix())
        return True
    print("—  ", path.as_posix())
    return False


def main() -> None:
    n = 0
    for rel in COMMERCIAL:
        p = ROOT / rel
        if p.exists() and process(p):
            n += 1
    # also scrub emoji on homepage why cards if any remain
    print(f"Done. {n} files changed.")


if __name__ == "__main__":
    main()
