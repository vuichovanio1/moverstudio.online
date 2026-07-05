#!/usr/bin/env python3
"""Generate Priority 1 blog articles from shared blueprint CSS."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
TEMPLATE = BLOG / "sait-vizitka-portfolio-malk-biznes-2026.html"
DATE = "2026-07-05"
OG_IMAGE = "https://moverstudio.online/og-image.png?v=1"


def load_css() -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", text, re.DOTALL)
    if not match:
        raise RuntimeError("Could not extract CSS from template")
    return match.group(1)


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = []
    for q, a in faqs:
        items.append(
            f"""        <details class="faq-item">
          <summary class="faq-question">{q}</summary>
          <div class="faq-answer">
            <p>{a}</p>
          </div>
        </details>"""
        )
    return "\n".join(items)


def faq_json_ld(url: str, faqs: list[tuple[str, str]]) -> list[dict]:
    return [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)},
        }
        for q, a in faqs
    ]


def toc_html(items: list[tuple[str, str]]) -> str:
  lines = [f'          <li><a href="#{aid}">{label}</a></li>' for aid, label in items]
  return "\n".join(lines)


def render(article: dict, css: str) -> str:
    slug = article["slug"]
    url = f"https://moverstudio.online/blog/{slug}"
    keywords_json = json.dumps(article["keywords"], ensure_ascii=False)
    faqs = article["faqs"]
    graph = [
        {
            "@type": "BlogPosting",
            "@id": f"{url}#blogposting",
            "headline": article["headline"],
            "description": article["meta_description"],
            "url": url,
            "inLanguage": "bg",
            "image": OG_IMAGE,
            "keywords": article["keywords"],
            "articleSection": article["section"],
            "datePublished": DATE,
            "dateModified": DATE,
            "author": {"@type": "Organization", "name": "MOVER Studio", "url": "https://moverstudio.online"},
            "publisher": {
                "@type": "Organization",
                "name": "MOVER Studio",
                "url": "https://moverstudio.online",
                "logo": {"@type": "ImageObject", "url": OG_IMAGE},
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        },
        {
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": faq_json_ld(url, faqs),
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Начало", "item": "https://moverstudio.online/"},
                {"@type": "ListItem", "position": 2, "name": "Блог", "item": "https://moverstudio.online/blog/"},
                {"@type": "ListItem", "position": 3, "name": article["breadcrumb"], "item": url},
            ],
        },
    ]
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

    footer_links = article.get("footer_links", "")
    cta_block = article.get("cta_block", "")

    return f"""<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f2eee3">
  <meta name="last-modified" content="{DATE}">

  <link rel="llms-txt" href="https://moverstudio.online/llms-full.txt">
  <link rel="alternate" type="text/plain" href="https://moverstudio.online/llms-faq.txt" title="llms-faq">

  <title>{article["title"]}</title>
  <meta name="description" content="{article["meta_description"]}">
  <meta name="keywords" content="{article["meta_keywords"]}">

  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="bg" href="{url}">

  <meta property="og:title" content="{article["headline"]}">
  <meta property="og:description" content="{article["meta_description"]}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:secure_url" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{article["og_image_alt"]}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="bg_BG">
  <meta property="og:site_name" content="MOVER Studio">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{article["headline"]}">
  <meta name="twitter:description" content="{article["meta_description"]}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="twitter:image:alt" content="{article["og_image_alt"]}">
  <meta name="twitter:site" content="@moverstudio_bg">
  <meta property="article:author" content="https://moverstudio.online/about.html">
  <meta property="article:section" content="{article["section"]}">
  <meta name="author" content="MOVER Studio">

  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/fontawesome-free-7.1.0-web/css/all.min.css">
<style>{css}</style>

  <script type="application/ld+json">
{ld_json}
  </script>
</head>
<body>

<a href="#main" class="skip-link" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;z-index:9999;padding:1rem;background:var(--ink);color:var(--paper);font-size:1rem;text-decoration:none;" onfocus="this.style.cssText='position:fixed;left:0;top:0;width:auto;height:auto;overflow:visible;z-index:9999;padding:1rem;background:var(--ink);color:var(--paper);font-size:1rem;text-decoration:none;'" onblur="this.style.cssText='position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;'">Прескочи към съдържанието</a>

<header>
  <nav aria-label="Основна навигация">
    <a href="../index.html" style="border-bottom: none;"><strong>MOVER_STUDIO</strong></a>
    <span class="terminal">{article["nav_tag"]}</span>
    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.9rem;">
      <a href="../index.html">Начало</a>
      <a href="../izrabotka-na-sait.html">Услуги</a>
      <a href="../izrabotka-na-landing-page.html">Изработка на landing page</a>
      <a href="../calculator.html">Калкулатор</a>
      <a href="../case-studies.html">Доказателства</a>
      <a href="../about.html">За Нас</a>
    </div>
  </nav>
</header>

<main id="main">
  <article>
    <div class="breadcrumb">
      <a href="../index.html">Начало</a> &gt; <a href="./">Блог</a> &gt; {article["breadcrumb"]}
    </div>

    <h1>{article["headline"]}</h1>
    <p><em>Време за четене: ~{article["read_min"]} минути</em></p>

    <div>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;">
        📅 Публикувано: <time datetime="{DATE}">5 юли 2026</time> • От: MOVER Studio
      </p>

{article["intro"]}

      <div class="quick-answer">
        <p><strong>Бърз отговор:</strong> {article["quick_answer"]}</p>
      </div>

      <nav aria-label="Съдържание на статията" style="margin: 2rem auto; max-width: 52rem; text-align: left; padding: 1.25rem 1.5rem; background: rgba(143, 71, 34, 0.06); border: 1px solid var(--line);">
        <p style="margin: 0 0 0.75rem; font-weight: 700;">Съдържание</p>
        <ul style="margin: 0; padding-left: 1.25rem; line-height: 1.8;">
{toc_html(article["toc"])}
        </ul>
      </nav>
    </div>

{article["body"]}

    <section style="margin: 2rem 0; padding: 1.5rem; background: rgba(143, 71, 34, 0.08); border-left: 4px solid var(--brand);">
      <h2 style="border-left: none; padding-left: 0;">Следваща стъпка</h2>
      {cta_block}
    </section>

    <section id="faq">
      <h2>Често задавани въпроси</h2>
      <div class="faq-container">
{faq_html(faqs)}
      </div>
    </section>

    <p><strong>Накратко:</strong> {article["summary"]}</p>

    <div style="text-align: center; padding: 2rem 0;">
      {article["bottom_ctas"]}
      <a href="./" class="cta-primary">Още статии →</a>
    </div>

  </article>
</main>

<footer>
  <p class="terminal">
    &copy; 2026 MOVER_STUDIO<br>
    &gt; Built without WordPress<br>
    &gt; Built with HTML and a lot of stubbornness<br>
    &gt; 99 PageSpeed е силен резултат, но ние често гоним 100<br>
    &gt; <span class="cursor">_</span>
  </p>
  <p style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.85;">
    "Free your mind" - Morpheus
  </p>
  <p style="margin-top: 1rem;">
    {footer_links}
  </p>
</footer>

</body>
</html>
"""


ARTICLES: list[dict] = []

# --- Article 1: Landing page ---
ARTICLES.append({
    "slug": "landing-page-google-ads-facebook-2026.html",
    "title": "Landing page за Google Ads и Facebook: цена и структура (2026) | MOVER Studio",
    "meta_description": "Landing page за Google Ads и Facebook: структура, цена от 400€, PageSpeed и реален пример — отделна страница за реклами до основен сайт.",
    "meta_keywords": "landing page цена, изработка на landing page, landing page google ads, landing page facebook, landing page за реклами",
    "headline": "Landing page за Google Ads и Facebook: цена, структура и защо скоростта вдига конверсиите",
    "og_image_alt": "Landing page за Google Ads и Facebook — цена и структура",
    "section": "Landing page",
    "breadcrumb": "Landing page за реклами",
    "nav_tag": "[ BLOG | LANDING PAGE | РЕКЛАМИ ]",
    "read_min": "8",
    "keywords": ["landing page цена", "изработка на landing page", "landing page google ads", "landing page facebook"],
    "intro": """      <p>Пускаш Google Ads или Facebook кампания и трафикът отива на началната страница на сайта ти? Губиш пари. <strong>Landing page</strong> е отделна страница с един фокус: обаждане, форма или заявка — без меню, без разсейване.</p>
      <p class="power-sentence">При нас <strong>само landing page</strong> (без основен сайт) е <strong>400€</strong>. Ако основният сайт е изработен от нас — ads страница е <strong>150–250€</strong> допълнение.</p>
      <p>В тази статия: структура за реклами, цена през 2026, защо PageSpeed влияе на CPC, най-добрият модел (основен сайт + ads страница) и реален кейс от практиката.</p>""",
    "quick_answer": "Най-добрият модел за реклами: <strong>пълен основен сайт</strong> + <strong>отделен landing</strong> само за обявите. Цени: <strong>400€</strong> (само landing, + хостинг) или <strong>150–250€</strong> ads страница при сайт от MOVER (без допълнителен хостинг). Виж <a href=\"../izrabotka-na-landing-page.html\">изработка на landing page</a>.",
    "toc": [
        ("kakvo", "Какво е landing page за реклами"),
        ("struktura", "Задължителна структура"),
        ("cena", "Цена през 2026"),
        ("osnoven-plus-ads", "Основен сайт + ads страница"),
        ("pagespeed", "PageSpeed и Google Ads"),
        ("matiyhelp-ads", "Кейс: matiyhelp.bg/ads.html"),
        ("faq", "Често задавани въпроси"),
    ],
    "body": """
    <section id="kakvo">
      <h2>Какво е landing page за реклами (и защо не е homepage)</h2>
      <p>Homepage представя целия бизнес. <strong>Landing page за Google Ads</strong> или Facebook продава <em>едно</em> предложение: услуга, оферта, събитие. Посетителят идва от реклама с конкретно очакване — страницата трябва да го изпълни за секунди.</p>
      <ul>
        <li>Без пълно меню — само лого и един CTA</li>
        <li>Същото послание като в рекламата (message match)</li>
        <li>Телефон, форма или Messenger — един избор</li>
        <li>Зареждане под 1 секунда на мобилен</li>
      </ul>
    </section>

    <section id="struktura">
      <h2>Структура на landing page, която конвертира</h2>
      <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>Блок</th><th>Цел</th><th>Задължително</th></tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Блок"><strong>Hero + заглавие</strong></td>
            <td data-label="Цел">Message match с рекламата</td>
            <td data-label="Задължително">Да</td>
          </tr>
          <tr>
            <td data-label="Блок"><strong>Ползи / булети</strong></td>
            <td data-label="Цел">Защо да действат сега</td>
            <td data-label="Задължително">Да</td>
          </tr>
          <tr>
            <td data-label="Блок"><strong>Доверие</strong></td>
            <td data-label="Цел">Отзиви, лого, гаранции</td>
            <td data-label="Задължително">Препоръчително</td>
          </tr>
          <tr>
            <td data-label="Блок"><strong>CTA</strong></td>
            <td data-label="Цел">Обаждане / форма</td>
            <td data-label="Задължително">Да — sticky на мобилен</td>
          </tr>
        </tbody>
      </table>
      </div>
      <p>Пълна оферта: <a href="../izrabotka-na-landing-page.html">изработка на landing page от 400€</a>.</p>
    </section>

    <section id="cena">
      <h2>Landing page цена през 2026</h2>
      <p>Цената не е фиксирана за всеки — зависи дали вече имаш сайт при нас:</p>
      <ul>
        <li><strong>Нямаш сайт</strong> — изработваме само една landing page. Тя е целият ти уеб; отделно ти трябват домейн и хостинг. <strong>400€</strong> еднократно.</li>
        <li><strong>Имаш основен сайт от MOVER Studio</strong> — добавяме отделна страница за реклами на същия домейн (напр. <code>firmata.bg/ads.html</code>). Дизайнът и хостингът вече са налице — плащаш само новата страница. <strong>150–250€</strong>.</li>
      </ul>
      <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>Вариант</th><th>Цена</th><th>Подходящ за</th></tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Вариант">Само landing page (без основен сайт)</td>
            <td data-label="Цена"><strong>400€</strong></td>
            <td data-label="Подходящ за">Стартираш онлайн от нула; нужен е домейн и хостинг</td>
          </tr>
          <tr>
            <td data-label="Вариант">Ads страница при сайт от MOVER Studio</td>
            <td data-label="Цена"><strong>150–250€</strong></td>
            <td data-label="Подходящ за">Пускаш Google Ads или Facebook към отделен URL на същия домейн</td>
          </tr>
          <tr>
            <td data-label="Вариант">WordPress + page builder</td>
            <td data-label="Цена">500–1200€+</td>
            <td data-label="Подходящ за">Чести промоции с CMS (по-бавно)</td>
          </tr>
          <tr>
            <td data-label="Вариант">A/B вариант (втора ads страница)</td>
            <td data-label="Цена">+150–250€</td>
            <td data-label="Подходящ за">Тест на заглавие или оферта</td>
          </tr>
        </tbody>
      </table>
      </div>
      <p><strong>Годишни разходи:</strong> при пакета от <strong>400€</strong> (само landing) — <strong>23–48€/година</strong> за домейн и хостинг, без месечни такси за CMS. При ads страница към съществуващ сайт от нас — качваме я на същия хостинг, <strong>без допълнителни годишни разходи</strong>.</p>
    </section>

    <section id="osnoven-plus-ads">
      <h2>Най-добрият модел: основен сайт + отделна страница за реклами</h2>
      <p>За бизнес с платена реклама оптималното решение не е една страница, която прави всичко, а <strong>две отделни роли</strong> онлайн — не два задължителни ценови пакета, а два различни уеб актива:</p>
      <ul>
        <li><strong>Основен сайт</strong> — услуги, локации, за нас, контакти; пълна навигация; органично SEO и дългосрочно доверие</li>
        <li><strong>Отделен URL за реклами</strong> — една страница без меню, един CTA (телефон или форма), същото послание като в обявата; sticky бутон на мобилен</li>
      </ul>
      <p>Не насочвай Google Ads към homepage с пълна навигация — посетителят се разсейва и конверсиите падат. И не ползвай ads страницата като основен сайт — губиш SEO, дълбочина на съдържанието и професионалния образ. Ads URL-ът е <em>само</em> за платен трафик; основният домейн остава лицето на бизнеса.</p>
    </section>

    <section id="pagespeed">
      <h2>PageSpeed, Quality Score и по-евтини кликове</h2>
      <p>Google Ads оценява <strong>Landing Page Experience</strong>. Бавна страница = по-нисък Quality Score = по-висок CPC. Статичен HTML landing page с 100 PageSpeed дава на алгоритъма сигнал, че посетителят няма да чака — особено на мобилен, където идва повечето платен трафик.</p>
      <p>Facebook също наказва бавни страници с по-висока цена на резултат. Затова <a href="../html-sait.html">изработка на HTML сайт</a> за реклами не е „техническа прищявка“ — директно влияе на разхода за реклама.</p>
    </section>

    <section id="matiyhelp-ads">
      <h2>Реален пример: matiyhelp.bg/ads.html</h2>
      <p><a href="https://matiyhelp.bg" target="_blank" rel="noopener">matiyhelp.bg</a> е пълният корпоративен сайт за пътна помощ — услуги, локации, SEO. <a href="https://matiyhelp.bg/ads.html" target="_blank" rel="noopener">matiyhelp.bg/ads.html</a> е отделна HTML страница <strong>само за Google Ads</strong>: без меню, 24/7 badge, голям телефон, Google отзиви, sticky „Обади се“ на мобилен.</p>
      <figure class="portfolio-item" style="max-width: 420px; margin: 1.5rem auto;">
        <img src="../images/landing.mat.png" alt="Мобилен изглед на matiyhelp.bg/ads.html — landing page за пътна помощ с телефон и sticky CTA" loading="lazy" width="390" height="844">
        <figcaption>matiyhelp.bg/ads.html — мобилен изглед за реклами</figcaption>
      </figure>
      <p>Точно този модел — основен сайт + фокусирана ads страница — дава и дългосрочно SEO, и висока конверсия от платения трафик. Още кейсове: <a href="../case-studies.html">case studies</a>.</p>
    </section>""",
    "cta_block": """      <p>Искаш landing page, готова за Google Ads или Facebook? Изпрати кратко запитване или виж цената за 30 секунди.</p>
      <p style="margin-bottom: 0;"><a href="../calculator.html" class="cta-primary">Изчисли цена →</a> <a href="../izrabotka-na-landing-page.html" class="cta-primary">Виж пакета landing page →</a></p>""",
    "bottom_ctas": """      <a href="../izrabotka-na-landing-page.html" class="cta-primary">Изработка на landing page →</a>
      <a href="../calculator.html" class="cta-primary">Калкулатор →</a>""",
    "footer_links": """    <a href="../index.html">Начало</a> |
    <a href="../izrabotka-na-landing-page.html">Landing page</a> |
    <a href="../calculator.html">Калкулатор</a> |
    <a href="./">Блог</a>""",
    "summary": "За реклами: пълен основен сайт + отделен landing само за обявите — две различни роли. Цени: 400€ (само landing, + хостинг) или 150–250€ ads страница при сайт от MOVER (без допълнителен хостинг).",
    "faqs": [
        ("Колко струва landing page?", "<strong>400€</strong>, ако изработваме само landing page без основен сайт. <strong>150–250€</strong>, ако основният сайт е от MOVER и добавяме ads страница. Виж <a href=\"../izrabotka-na-landing-page.html\">изработка на landing page</a>."),
        ("Има ли годишни разходи за ads страницата?", "При пакета от <strong>400€</strong> (само landing) — <strong>23–48€/година</strong> за домейн и хостинг. При ads страница към сайт от нас — <strong>няма</strong> допълнителни годишни разходи."),
        ("Трябва ли ми основен сайт и ads страница?", "За бизнес с реклами — <strong>да</strong>. Основният сайт държи SEO и доверието; отделната ads страница с един CTA конвертира платения трафик."),
        ("Каква е разликата между landing page и сайт визитка?", "Визитката има 1–5 страници и пълна навигация. Landing page е <strong>една</strong> страница за платен трафик с един CTA."),
        ("Защо PageSpeed е важен за Google Ads?", "По-бързата страница подобрява Landing Page Experience и Quality Score — често намалява CPC."),
        ("Може ли A/B тест с две landing страници?", "Да — втора HTML страница за тест на заглавие или оферта обикновено е +150–250€."),
        ("Колко време отнема изработката?", "<strong>3–5 работни дни</strong> след получаване на текст и снимки."),
    ],
})

ARTICLES.append({
    "slug": "korporativen-sait-vs-vizitka-2026.html",
    "title": "Корпоративен сайт или визитка: разлика, цена и кой пакет (2026) | MOVER Studio",
    "meta_description": "Корпоративен сайт от 1000€ или сайт визитка от 400€? Сравнение по страници, SEO, multi-location и кога кой пакет е правилният избор.",
    "meta_keywords": "корпоративен сайт, сайт визитка, корпоративен сайт цена, изработка на корпоративен сайт, фирмен сайт",
    "headline": "Корпоративен сайт или сайт визитка: кога какво и колко струва през 2026",
    "og_image_alt": "Корпоративен сайт vs сайт визитка — сравнение и цена",
    "section": "Корпоративен сайт",
    "breadcrumb": "Корпоративен vs визитка",
    "nav_tag": "[ BLOG | КОРПОРАТИВЕН | ВИЗИТКА ]",
    "read_min": "7",
    "keywords": ["корпоративен сайт", "сайт визитка", "корпоративен сайт цена", "фирмен сайт"],
    "intro": """      <p>Търсиш <strong>изработка на корпоративен сайт</strong> или достатъчна ли е <strong>сайт визитка</strong>? Грешният избор струва пари и месеци — или плащаш за 15 страници, които няма да ползваш, или оставаш тесен, когато бизнесът расте.</p>
      <p class="power-sentence"><strong>Визитка: 400€</strong> (1–5 стр.) · <strong>Корпоративен: 1000€</strong> (5–15 стр., сложна структура)</p>
      <p>Тук сравняваме двата пакета по страници, SEO, срок и типични сценарии — за да избереш правилния, преди да пишеш на агенция.</p>""",
    "quick_answer": "Визитка <strong>400€</strong> за 1–5 страници и локален бизнес. Корпоративен <strong>1000€</strong> за 5–15 страници, review integration и базово on-page SEO. Multi-location (+200€) и разширено SEO (+100€) — добавки. Виж <a href=\"../korporativen-sait.html\">корпоративен сайт</a> и <a href=\"../sait-vizitka.html\">сайт визитка</a>.",
    "toc": [
        ("sravnenie", "Сравнение на пакетите"),
        ("vizitka", "Кога е достатъчна визитка"),
        ("korporativen", "Кога ти трябва корпоративен"),
        ("cena", "Цени през 2026"),
        ("faq", "Често задавани въпроси"),
    ],
    "body": """
    <section id="sravnenie">
      <h2>Сравнение: корпоративен сайт vs сайт визитка</h2>
      <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>Критерий</th><th>Сайт визитка (400€)</th><th>Корпоративен (1000€)</th></tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Критерий"><strong>Страници</strong></td>
            <td data-label="Сайт визитка (400€)">1–5</td>
            <td data-label="Корпоративен (1000€)">5–15</td>
          </tr>
          <tr>
            <td data-label="Критерий"><strong>SEO</strong></td>
            <td data-label="Сайт визитка (400€)">On-page + 4 schema типа</td>
            <td data-label="Корпоративен (1000€)">On-page + 6 schema типа (+100€ разширено SEO add-on)</td>
          </tr>
          <tr>
            <td data-label="Критерий"><strong>Навигация</strong></td>
            <td data-label="Сайт визитка (400€)">Проста</td>
            <td data-label="Корпоративен (1000€)">Многостранична, локации, екип</td>
          </tr>
          <tr>
            <td data-label="Критерий"><strong>Срок</strong></td>
            <td data-label="Сайт визитка (400€)">5–7 дни</td>
            <td data-label="Корпоративен (1000€)">10–14 дни</td>
          </tr>
          <tr>
            <td data-label="Критерий"><strong>Годишни разходи</strong></td>
            <td data-label="Сайт визитка (400€)">23–48€</td>
            <td data-label="Корпоративен (1000€)">23–48€</td>
          </tr>
        </tbody>
      </table>
      </div>
    </section>

    <section id="vizitka">
      <h2>Кога е достатъчна сайт визитка (400€)</h2>
      <ul>
        <li>Една локация, един основен фокус (услуги + контакт)</li>
        <li>Фрийлансър, занаятчия, малък екип до 5 души</li>
        <li>Няма нужда от отделни страници за всеки квартал или град</li>
        <li>Искаш бърз старт с минимален бюджет</li>
      </ul>
      <p>Подробности: <a href="../sait-vizitka.html">изработка на сайт визитка и портфолио</a> · <a href="sait-vizitka-portfolio-malk-biznes-2026.html">примери по ниши</a></p>
    </section>

    <section id="korporativen">
      <h2>Кога ти трябва корпоративен сайт (1000€)</h2>
      <ul>
        <li>5+ услуги или продуктови линии с отделни страници</li>
        <li>Multi-location SEO — няколко града или квартала (добавка +200€; пример: <a href="https://roadassistancesofia.bg" target="_blank" rel="noopener">roadassistancesofia.bg</a>)</li>
        <li>Страници „Екип“, „Кариери“, „Локации“, разширено доверие</li>
        <li>Review integration и по-сложна schema структура</li>
      </ul>
      <p>Пълен пакет: <a href="../korporativen-sait.html">изработка на корпоративен сайт</a> · <a href="../case-studies.html">case studies</a></p>
    </section>

    <section id="cena">
      <h2>Цени през 2026 — без скрити такси</h2>
      <p>И при двата пакета плащаш <strong>веднъж</strong>. Няма месечни такси за WordPress, плъгини или „поддръжка на CMS“. След пускане: домейн + хостинг <strong>23–48€/година</strong> (директно към доставчик).</p>
      <p>Не си сигурен? <a href="../calculator.html">Калкулаторът</a> дава ориентир за добавки (multi-location +200€, многоезичен +300€).</p>
    </section>""",
    "cta_block": """      <p>Не знаеш кой пакет ти трябва? Изпрати кратко описание на бизнеса — ще насочим към визитка или корпоративен без излишни страници.</p>
      <p style="margin-bottom: 0;"><a href="../calculator.html" class="cta-primary">Калкулатор →</a> <a href="../korporativen-sait.html" class="cta-primary">Корпоративен сайт →</a> <a href="../sait-vizitka.html" class="cta-primary">Сайт визитка →</a></p>""",
    "bottom_ctas": """      <a href="../korporativen-sait.html" class="cta-primary">Корпоративен сайт →</a>
      <a href="../sait-vizitka.html" class="cta-primary">Сайт визитка →</a>""",
    "footer_links": """    <a href="../index.html">Начало</a> |
    <a href="../korporativen-sait.html">Корпоративен сайт</a> |
    <a href="../sait-vizitka.html">Сайт визитка</a> |
    <a href="./">Блог</a>""",
    "summary": "Визитка за старт и локален фокус; корпоративен за растеж и много страници. Multi-location и разширено SEO — добавки. И двата — HTML, без месечни CMS такси.",
    "faqs": [
        ("Колко струва корпоративен сайт?", "От <strong>1000€</strong> еднократно за 5–15 страници и 6 schema типа. Multi-location (+200€) и разширено SEO (+100€) — опционални добавки. Виж <a href=\"../korporativen-sait.html\">корпоративен сайт</a>."),
        ("Колко струва сайт визитка?", "<strong>400€</strong> за 1–5 страници. Виж <a href=\"../sait-vizitka.html\">сайт визитка</a>."),
        ("Мога ли да започна с визитка и после да разширя?", "Да — HTML архитектурата позволява добавяне на страници. По-голям пакет или допълнителни страници се договарят отделно."),
        ("Включено ли е multi-location SEO във визитката?", "Не — multi-location (+200€) е добавка към корпоративен или друг пакет, не е част от базовите 1000€."),
        ("Има ли месечни такси?", "Не. Само домейн и хостинг 23–48€/година след пускане."),
    ],
})

ARTICLES.append({
    "slug": "multi-location-seo-html-2026.html",
    "title": "Multi-location SEO без WordPress: кейс roadassistancesofia.bg (2026) | MOVER Studio",
    "meta_description": "Локално SEO с отделни HTML страници за всеки район: как roadassistancesofia.bg използва 14 локации без WordPress и защо това работи.",
    "meta_keywords": "multi-location seo, локално seo, изработка на сайт софия, корпоративен сайт seo, html локални страници",
    "headline": "Multi-location SEO без WordPress: как 14 HTML страници носят локален трафик",
    "og_image_alt": "Multi-location SEO с HTML — кейс roadassistancesofia.bg",
    "section": "Локално SEO",
    "breadcrumb": "Multi-location SEO",
    "nav_tag": "[ BLOG | LOCAL SEO | HTML ]",
    "read_min": "8",
    "keywords": ["multi-location seo", "локално seo", "корпоративен сайт", "html локални страници"],
    "intro": """      <p>Искаш да се класираш за „услуга + квартал“ в София (или друг град)? Един homepage не стига. <strong>Multi-location SEO</strong> изисква отделна, индексируема страница за всяка локация — с уникален title, H1 и съдържание.</p>
      <p class="power-sentence">При <a href="https://roadassistancesofia.bg" target="_blank" rel="noopener">roadassistancesofia.bg</a> това са <strong>14 HTML страници</strong> — без WordPress, без бавни плъгини.</p>
      <p>Обясняваме модела, защо статичен HTML го прави по-евтино и по-бързо от CMS, и кога ти трябва такава архитектура.</p>""",
    "quick_answer": "Multi-location = отделен URL за всяка локация, canonical структура, schema LocalBusiness. Добавка <strong>+200€</strong> (не е в базовите 1000€ корпоративен пакет). Виж <a href=\"../korporativen-sait.html\">корпоративен сайт</a> и <a href=\"../seo-optimizacia.html\">SEO оптимизация</a>.",
    "toc": [
        ("model", "Какво е multi-location SEO"),
        ("html", "Защо HTML, не WordPress"),
        ("keis", "Кейс roadassistancesofia.bg"),
        ("kogato", "Кога ти трябва"),
        ("faq", "Често задавани въпроси"),
    ],
    "body": """
    <section id="model">
      <h2>Какво е multi-location SEO архитектура</h2>
      <p>Вместо една страница „Контакти“ с адрес, правиш:</p>
      <ul>
        <li><strong>Хъб страница</strong> — общ преглед на услугата в целия град</li>
        <li><strong>Локални landing страници</strong> — „пътна помощ Младост“, „пътна помощ Люлин“ и т.н.</li>
        <li>Уникален meta title, H1, текст и schema за всяка URL</li>
        <li>Вътрешно свързване: хъб → локални → контакт</li>
      </ul>
      <p>Google индексира всяка страница отделно. Търсенето „услуга + квартал“ попада на релевантен URL — не на общ homepage.</p>
    </section>

    <section id="html">
      <h2>Защо статичен HTML бие WordPress за локални страници</h2>
      <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>Фактор</th><th>HTML (статичен)</th><th>WordPress</th></tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Фактор"><strong>Скорост</strong></td>
            <td data-label="HTML (статичен)">Цел 100 PageSpeed на всяка страница</td>
            <td data-label="WordPress">Често 40–70 mobile</td>
          </tr>
          <tr>
            <td data-label="Фактор"><strong>14 локации</strong></td>
            <td data-label="HTML (статичен)">14 леки файла, еднакъв шаблон</td>
            <td data-label="WordPress">14 записа + DB заявки + плъгини</td>
          </tr>
          <tr>
            <td data-label="Фактор"><strong>Поддръжка</strong></td>
            <td data-label="HTML (статичен)">Управлявани ъпдейти от екипа</td>
            <td data-label="WordPress">Актуализации, сигурност, плъгини</td>
          </tr>
        </tbody>
      </table>
      </div>
    </section>

    <section id="keis">
      <h2>Кейс: roadassistancesofia.bg</h2>
      <p>Проект за пътна помощ в София с <strong>14 локационни страници</strong> — всяка оптимизирана за конкретен район. Резултат: покритие на long-tail заявки без един претрупан homepage.</p>
      <div class="portfolio-grid">
        <figure class="portfolio-item">
          <img src="../images/115453_roadassistancesofia.bg.webp" alt="Начална страница на roadassistancesofia.bg" loading="lazy" width="1853" height="881">
          <figcaption>Общ хъб</figcaption>
        </figure>
        <figure class="portfolio-item">
          <img src="../images/121300_roadassistancesofia.bg.webp" alt="Локална страница roadassistancesofia.bg" loading="lazy" width="1853" height="881">
          <figcaption>Локална страница</figcaption>
        </figure>
        <figure class="portfolio-item">
          <img src="../images/120747_roadassistancesofia.bg.webp" alt="Мобилен изглед roadassistancesofia.bg" loading="lazy" width="1853" height="881">
          <figcaption>Мобилен CTA</figcaption>
        </figure>
      </div>
      <p>Пълен разбор: <a href="../case-studies.html">case studies</a> · <a href="../izrabotka-na-sait-sofia.html">изработка на сайтове София</a></p>
    </section>

    <section id="kogato">
      <h2>Кога ти трябва multi-location SEO</h2>
      <ul>
        <li>Услуга с търсене по квартал/град (пътна помощ, ВиК, климатици, доставка)</li>
        <li>Повече от един физически обект или зона на обслужване</li>
        <li>Искаш да мащабираш видимостта без да плащаш за отделни домейни</li>
      </ul>
      <p>Не ти трябва, ако имаш един магазин и един адрес — достатъчна е <a href="../sait-vizitka.html">сайт визитка</a>.</p>
    </section>""",
    "cta_block": """      <p>Искаш локални страници за София или цяла България? Виж корпоративния пакет или питай за multi-location добавка.</p>
      <p style="margin-bottom: 0;"><a href="../korporativen-sait.html" class="cta-primary">Корпоративен сайт →</a> <a href="../calculator.html" class="cta-primary">Калкулатор →</a></p>""",
    "bottom_ctas": """      <a href="../korporativen-sait.html" class="cta-primary">Корпоративен сайт →</a>
      <a href="../seo-optimizacia.html" class="cta-primary">SEO оптимизация →</a>""",
    "footer_links": """    <a href="../index.html">Начало</a> |
    <a href="../korporativen-sait.html">Корпоративен сайт</a> |
    <a href="../case-studies.html">Case Studies</a> |
    <a href="./">Блог</a>""",
    "summary": "Multi-location SEO = много леки HTML страници, всяка за една локация. По-бързо и по-евтино за поддръжка от WordPress мрежа от landing страници.",
    "faqs": [
        ("Колко локационни страници мога да имам?", "Типично 5–15 в корпоративен пакет; при roadassistancesofia.bg — 14. Повече се договаря индивидуално."),
        ("Колко струва multi-location SEO?", "Добавка <strong>+200€</strong> към проект. Не е включена в базовия корпоративен пакет от 1000€."),
        ("Работи ли за извън София?", "Да — отделен URL на град или квартал, независимо от локацията в България."),
        ("Нужен ли е WordPress за много страници?", "Не. Статичен HTML е по-бърз и по-евтин за поддръжка при много локални URL."),
        ("Колко време до индексация?", "Техническата основа е готова при пускане; органични позиции — седмици до месеци според конкуренцията."),
    ],
})

ARTICLES.append({
    "slug": "migratsiya-wordpress-kam-html-2026.html",
    "title": "Миграция от WordPress към HTML: цена, стъпки и 301 redirects (2026) | MOVER Studio",
    "meta_description": "Преминаване от WordPress към статичен HTML: процес, цена 200–500€, запазване на SEO с 301 redirects и реален пример с PageSpeed преди/след.",
    "meta_keywords": "миграция wordpress към html, преминаване от wordpress, wordpress към статичен сайт, 301 redirect, wordpress алтернатива",
    "headline": "Миграция от WordPress към HTML: цена, стъпки и как да запазиш SEO",
    "og_image_alt": "Миграция от WordPress към HTML — цена и процес",
    "section": "WordPress миграция",
    "breadcrumb": "WordPress → HTML миграция",
    "nav_tag": "[ BLOG | МИГРАЦИЯ | HTML ]",
    "read_min": "8",
    "keywords": ["миграция wordpress", "wordpress към html", "301 redirect", "wordpress алтернатива"],
    "intro": """      <p>WordPress сайтът ти е бавен, чуплив или скъп за поддръжка? <strong>Миграция към HTML</strong> премахва базата данни, плъгините и риска от хак — и често вдига PageSpeed от 40–60 на 95–100.</p>
      <p class="power-sentence">Типична <strong>миграция WordPress → HTML</strong> при нас: <strong>200–500€</strong> — съдържание, SEO и 301 пренасочвания.</p>
      <p>Стъпка по стъпка: какво се случва, какво запазваш от SEO, и измерим пример от тестова WordPress vs HTML среда.</p>""",
    "quick_answer": "Миграция <strong>200–500€</strong> според обхвата: експорт на съдържание, HTML реализация, 301 redirects, schema. Нов сайт от нула: от 400€. Виж <a href=\"../wordpress-alternativa.html\">алтернатива на WordPress</a>.",
    "toc": [
        ("zashto", "Защо да мигрираш"),
        ("stapki", "Стъпки на миграцията"),
        ("seo", "301 redirects и SEO"),
        ("cena", "Цена"),
        ("bdin", "Пример: PageSpeed преди/след"),
        ("faq", "Често задавани въпроси"),
    ],
    "body": """
    <section id="zashto">
      <h2>Защо фирми мигрират от WordPress към HTML</h2>
      <ul>
        <li>PageSpeed и Core Web Vitals — по-добри за SEO и реклами</li>
        <li>Нулеви месечни такси за плъгини и „поддръжка на CMS“</li>
        <li>По-малка повърхност за атака (няма wp-admin, няма DB)</li>
        <li>Предвидими разходи: платено веднъж + 23–48€/година хостинг</li>
      </ul>
      <p>Не мигрираш, ако публикуваш ежедневно блог с много автори — тогава CMS има смисъл. За brochure сайт с рядки промени HTML е по-логичен.</p>
    </section>

    <section id="stapki">
      <h2>Стъпки на миграцията</h2>
      <ol>
        <li><strong>Одит</strong> — URL-и, съдържание, форми, интеграции</li>
        <li><strong>Карта на пренасочванията</strong> — стар URL → нов URL (1:1)</li>
        <li><strong>HTML изработка</strong> — същият дизайн или редизайн</li>
        <li><strong>301 redirects</strong> — в .htaccess или сървърна конфигурация</li>
        <li><strong>Тест</strong> — PageSpeed, Search Console, форми</li>
        <li><strong>Пускане</strong> — превключване на DNS или replace на файлове</li>
      </ol>
      <p>Процесът ни: <a href="../how-we-do-it.html">как работим</a></p>
    </section>

    <section id="seo">
      <h2>Как запазваш SEO при миграция</h2>
      <p>Най-честата грешка: нови URL без 301 от старите. Google губи сигнал; позициите падат.</p>
      <ul>
        <li>Запази slug-овете, където е възможно</li>
        <li>301 redirect за всяка променена URL</li>
        <li>Пренеси title, meta, canonical, schema</li>
        <li>Подай обновен sitemap в Google Search Console</li>
      </ul>
      <p>Още: <a href="../seo-optimizacia.html">SEO оптимизация</a> · <a href="zashto-wordpress-e-baven.html">защо WordPress е бавен</a></p>
    </section>

    <section id="cena">
      <h2>Колко струва миграция WordPress → HTML</h2>
      <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>Обхват</th><th>Цена</th><th>Включено</th></tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Обхват">Малък сайт (до 5 стр.)</td>
            <td data-label="Цена"><strong>200–300€</strong></td>
            <td data-label="Включено">Съдържание, redirects, schema</td>
          </tr>
          <tr>
            <td data-label="Обхват">Среден (5–15 стр.)</td>
            <td data-label="Цена"><strong>300–500€</strong></td>
            <td data-label="Включено">+ multi-location карта</td>
          </tr>
          <tr>
            <td data-label="Обхват">Нов сайт от нула (вместо миграция)</td>
            <td data-label="Цена"><strong>400€+</strong></td>
            <td data-label="Включено">Пълен пакет визитка/корпоративен</td>
          </tr>
        </tbody>
      </table>
      </div>
    </section>

    <section id="bdin">
      <h2>Измерим пример: WordPress vs HTML (PageSpeed)</h2>
      <p>В тестова среда същата концепция е пусната като WordPress и като чист HTML — с ясна разлика в PageSpeed и structured data.</p>
      <div class="portfolio-grid">
        <figure class="portfolio-item">
          <img src="../images/bdinbefore.webp" alt="PageSpeed преди миграция от WordPress" loading="lazy" width="1837" height="776">
          <figcaption>Преди (WordPress)</figcaption>
        </figure>
        <figure class="portfolio-item">
          <img src="../images/bdinafter.webp" alt="PageSpeed след миграция към HTML" loading="lazy" width="1837" height="830">
          <figcaption>След (HTML)</figcaption>
        </figure>
      </div>
      <p>Контекст: <a href="../case-studies.html">case studies</a> · <a href="https://bdinhost.com" target="_blank" rel="noopener">BDinHost</a></p>
    </section>""",
    "cta_block": """      <p>Готов ли си да мигрираш от WordPress? Изпрати URL на текущия сайт — ще дадем ориентир за цена и срок.</p>
      <p style="margin-bottom: 0;"><a href="../wordpress-alternativa.html" class="cta-primary">Алтернатива на WordPress →</a> <a href="../calculator.html" class="cta-primary">Калкулатор →</a></p>""",
    "bottom_ctas": """      <a href="../wordpress-alternativa.html" class="cta-primary">WordPress алтернатива →</a>
      <a href="../html-sait.html" class="cta-primary">HTML сайт →</a>""",
    "footer_links": """    <a href="../index.html">Начало</a> |
    <a href="../wordpress-alternativa.html">WordPress алтернатива</a> |
    <a href="../html-sait.html">HTML сайт</a> |
    <a href="./">Блог</a>""",
    "summary": "Миграция WordPress → HTML запазва SEO с 301, вдига скоростта и спира CMS разходите. 200–500€ типично за съществуващ малък/среден сайт.",
    "faqs": [
        ("Колко струва миграция от WordPress към HTML?", "Обикновено <strong>200–500€</strong> според броя страници и сложността на redirects."),
        ("Ще загубя ли позициите в Google?", "Не, ако 301 redirects са правилни и съдържанието е еквивалентно. Проследявай Search Console 2–4 седмици."),
        ("Колко време отнема?", "5–14 работни дни според обхвата — паралелно с изработка на HTML версията."),
        ("Мога ли да редактирам съдържанието след това?", "Да — чрез управлявани ъпдейти от нашия екип (ти изпращаш, ние публикуваме). Типичен SLA: 24 часа."),
        ("Какво става с блога в WordPress?", "Статичните статии могат да станат HTML страници; активен ежедневен блог е по-подходящ за CMS — казваме честно, ако не е fit."),
    ],
})


def main() -> None:
    css = load_css()
    for article in ARTICLES:
        out = BLOG / article["slug"]
        out.write_text(render(article, css), encoding="utf-8")
        print(f"Wrote {out.name}")


if __name__ == "__main__":
    main()
