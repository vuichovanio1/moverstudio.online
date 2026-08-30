#!/usr/bin/env python3
"""Build redesigned index.html v2."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
old = (ROOT / "index.html").read_text(encoding="utf-8")
start = old.index("  <!-- Schema: @graph markup -->")
end = old.index("</head>")
schema_block = old[start:end]

body = r'''<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f0e8">
  <meta name="author" content="MOVER Studio">
  <meta name="last-modified" content="2026-08-30">

  <link rel="llms-txt" href="https://moverstudio.online/llms-full.txt">
  <link rel="alternate" type="text/plain" href="https://moverstudio.online/llms-faq.txt" title="llms-faq">

  <title>MOVER Studio — бърз HTML сайт от 400€</title>
  <meta name="description" content="MOVER Studio — бърз HTML сайт от 400€, цел 95–100 PageSpeed, без WordPress и месечни такси. Виж услуги, цени и реални проекти.">
  <meta name="keywords" content="mover studio, html сайт, изработка на сайт, сайт без wordpress, pagespeed, бърз сайт">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="https://moverstudio.online/">
  <link rel="alternate" hreflang="bg" href="https://moverstudio.online/">

  <link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
  <link rel="icon" href="/images/favicon.ico?v=2" sizes="48x48">
  <link rel="icon" href="/images/favicon-32.png?v=2" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/images/apple-touch-icon.png?v=2">

  <link rel="preload" href="/fonts/share-tech-mono-v16-latin-regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/site.css">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="MOVER Studio — бърз HTML сайт от 400€">
  <meta name="twitter:description" content="MOVER Studio — бърз HTML сайт от 400€, цел 95–100 PageSpeed, без WordPress. Виж услуги, цени и реални проекти.">
  <meta name="twitter:image" content="https://moverstudio.online/og-image.png?v=2">
  <meta name="twitter:site" content="@moverstudio_bg">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://moverstudio.online/">
  <meta property="og:title" content="MOVER Studio — бърз HTML сайт от 400€">
  <meta property="og:description" content="MOVER Studio — бърз HTML сайт от 400€, цел 95–100 PageSpeed, без WordPress. Виж услуги, цени и реални проекти.">
  <meta property="og:image" content="https://moverstudio.online/og-image.png?v=2">
  <meta property="og:locale" content="bg_BG">
  <meta property="og:site_name" content="MOVER Studio">

'''

out = body + schema_block + '''
  <meta name="mobile-web-app-capable" content="yes">
</head>
<body>

<a href="#main" class="skip-link">Прескочи към съдържанието</a>

<header class="site-header">
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
      <a href="#contact" class="nav-cta">Контакт</a>
    </nav>
  </div>
</header>

<main id="main">

  <section class="hero container">
    <h1 class="hero__title reveal" id="main-heading">Бърз <em>HTML сайт</em> от 400€</h1>
    <p class="hero__lead reveal">Изработка на сайт без WordPress и без месечни такси — цел 95–100 PageSpeed. София и цяла България.</p>
    <div class="hero__actions reveal">
      <a href="/izrabotka-na-sait.html" class="btn btn--primary">Изработка на сайт →</a>
      <a href="/calculator.html" class="btn btn--secondary">Калкулатор</a>
      <a href="tel:+359877845569" class="btn btn--ghost">☎ Обади се</a>
      <a href="mailto:admin@moverstudio.online?subject=%D0%97%D0%B0%D0%BF%D0%B8%D1%82%D0%B2%D0%B0%D0%BD%D0%B5%20%D0%B7%D0%B0%20HTML%20%D1%81%D0%B0%D0%B9%D1%82" class="btn btn--ghost">✉ Запитване</a>
    </div>
    <div class="hero__trust reveal">
      <span>От 400€ еднократно</span>
      <span>3–5 дни визитка</span>
      <span>5% гаранция при закъснение</span>
      <span>23–48€/год хостинг</span>
    </div>
  </section>

  <section class="section section--alt" id="solutions">
    <div class="container">
      <div class="section__head reveal">
        <span class="section__label">Пакети</span>
        <h2>Избери тип сайт</h2>
        <p>Три ясни опции — пълни детайли в <a href="/izrabotka-na-sait.html">hub страницата</a> и <a href="/calculator.html">калкулатора</a>.</p>
      </div>
      <div class="grid grid--3 reveal">
        <article class="card">
          <h3>Landing page</h3>
          <p class="card__price">400€</p>
          <p>За Google/Meta Ads — висока конверсия и PageSpeed.</p>
          <a href="/izrabotka-na-landing-page.html" class="btn btn--secondary" style="margin-top:1rem;">Детайли</a>
        </article>
        <article class="card card--highlight">
          <h3>Сайт визитка / портфолио</h3>
          <p class="card__price">400€</p>
          <p>1–5 страници · локален бизнес · 3–5 работни дни.</p>
          <a href="/sait-vizitka.html" class="btn btn--primary" style="margin-top:1rem;">Детайли</a>
        </article>
        <article class="card">
          <h3>Корпоративен сайт</h3>
          <p class="card__price">1000€</p>
          <p>5–15 страници · review integration · 10–14 дни.</p>
          <a href="/korporativen-sait.html" class="btn btn--secondary" style="margin-top:1rem;">Детайли</a>
        </article>
      </div>
    </div>
  </section>

  <section class="section" id="portfolio">
    <div class="container">
      <div class="section__head reveal">
        <span class="section__label">Портфолио</span>
        <h2>Реални проекти</h2>
      </div>
      <div class="notice reveal">
        <p><strong>Реални бизнеси от нашия екип</strong> — зад
          <a href="https://patna-pomosht-kostinbrod.bg/" target="_blank" rel="noopener">Пътна помощ Костинброд</a>
          (<a href="https://g.co/kgs/p32TnaT" target="_blank" rel="noopener">5.0 / 106 отзива</a>)
          и <a href="https://minibagerkb.eu/" target="_blank" rel="noopener">Минибагер Костинброд</a>
          стои същият екип — <strong>Иван Иванов</strong>.</p>
      </div>
      <div class="portfolio-grid reveal">
        <figure class="portfolio-card">
          <a href="/case-studies.html"><img src="/images/115453_roadassistancesofia.bg.webp" alt="roadassistancesofia.bg" loading="lazy" width="1853" height="881"><figcaption>Пътна помощ София</figcaption></a>
        </figure>
        <figure class="portfolio-card">
          <a href="/case-studies.html"><img src="/images/121338_patna-pomosht-kostinbrod.bg.webp" alt="patna-pomosht-kostinbrod.bg" loading="lazy" width="1853" height="881"><figcaption>Пътна помощ Костинброд</figcaption></a>
        </figure>
        <figure class="portfolio-card">
          <a href="/case-studies.html"><img src="/images/115814_nikoautogaz-home.webp" alt="Niko Autogaz" loading="lazy" width="1853" height="881"><figcaption>Niko Autogaz</figcaption></a>
        </figure>
        <figure class="portfolio-card">
          <a href="/case-studies.html"><img src="/images/120023_re-peat.store.webp" alt="re-peat.store" loading="lazy" width="1853" height="881"><figcaption>re-peat.store</figcaption></a>
        </figure>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="proven-efficiency">
    <div class="container">
      <div class="section__head reveal">
        <span class="section__label">TCO</span>
        <h2>HTML срещу WordPress — месечни разходи</h2>
        <p>Ориентировъчни данни за България, 2026 · <a href="/wordpress-alternativa.html">пълно сравнение</a></p>
      </div>
      <div class="price-grid reveal">
        <div class="price-item price-item--best">
          <span class="price-item__name">HTML сайт (автономен)</span>
          <span class="price-item__val">0–3 €</span>
          <span class="price-item__note">Хостинг 0–8 €/мес. (често безплатен); без плъгини и ъпдейти.</span>
        </div>
        <div class="price-item">
          <span class="price-item__name">WordPress (базов)</span>
          <span class="price-item__val">3–8 €</span>
          <span class="price-item__note">Споделен хостинг + домейн; риск от уязвимости.</span>
        </div>
        <div class="price-item">
          <span class="price-item__name">WordPress (самостоятелна поддръжка)</span>
          <span class="price-item__val">5–15 €</span>
          <span class="price-item__note">Хостинг + плъгини + време за ъпдейти.</span>
        </div>
        <div class="price-item">
          <span class="price-item__name">WordPress (агенция)</span>
          <span class="price-item__val">50–150+ €</span>
          <span class="price-item__note">Поддръжка, бекъп, сигурност, корекции.</span>
        </div>
      </div>
      <p class="reveal" style="margin:1.5rem auto 0;text-align:center;max-width:52ch;font-size:0.9rem;">
        <strong>HTML спестява до 90% дългосрочно</strong> — годишно 23–48€ домейн+хостинг vs стотици € при WordPress.
      </p>
    </div>
  </section>

  <section class="section" id="social-proof">
    <div class="container">
      <div class="section__head reveal">
        <span class="section__label">Search Console</span>
        <h2>Реални органични резултати</h2>
        <p>Проекти на ~5–6 месеца · 6 от 9 със средна позиция под 10</p>
      </div>
      <div class="grid grid--4 reveal">
        <div class="stat"><div class="stat__num">460</div><div class="stat__label">клика · Пътна помощ Костинброд</div></div>
        <div class="stat"><div class="stat__num">270</div><div class="stat__label">клика · Niko Autogaz</div></div>
        <div class="stat"><div class="stat__num">180</div><div class="stat__label">клика · Re-Peat</div></div>
        <div class="stat"><div class="stat__num">0→✓</div><div class="stat__label">видимост · BdinHost</div></div>
      </div>
      <div class="hero__actions reveal" style="margin-top:1.5rem;">
        <a href="/case-studies.html#search-console" class="btn btn--secondary">Search Console доказателства</a>
        <a href="/blog/html-saitove-google-search-console-2026.html" class="btn btn--secondary">Статия в блога</a>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="section__head reveal">
        <span class="section__label">Защо ние</span>
        <h2>Защо HTML сайт при MOVER Studio</h2>
      </div>
      <div class="grid grid--2 reveal">
        <article class="card"><h3>⏱️ Бърза изработка</h3><p>3–5 дни визитка, 10–14 корпоративен — без месеци чакане.</p></article>
        <article class="card"><h3>🛠️ Чист код</h3><p>HTML/CSS best practices, schema, Core Web Vitals.</p></article>
        <article class="card"><h3>🤝 Гаранция</h3><p>Цел 95–100 PageSpeed · 30 дни корекции · 5% компенсация при закъснение.</p></article>
        <article class="card"><h3>📋 Без скрити такси</h3><p>Еднократна цена. <a href="/faq.html">Виж всички условия</a>.</p></article>
      </div>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="container">
      <div class="section__head reveal">
        <span class="section__label">ЧЗВ</span>
        <h2>Често задавани въпроси</h2>
      </div>
      <div class="grid grid--2 faq-grid reveal">
        <article class="card"><h3>Колко струва изработка на сайт?</h3><p>От <strong>400€</strong> до <strong>1000€+</strong>. Годишно 23–48€. <a href="/izrabotka-na-sait.html">Ценова разбивка</a> · <a href="/blog/kolko-struva-izrabotka-na-sait-2026.html">подробна статия</a>.</p></article>
        <article class="card"><h3>Защо HTML вместо WordPress?</h3><p>По-бързо, по-сигурно, без месечни такси. <a href="/wordpress-alternativa.html">Алтернатива</a> · <a href="/blog/zashto-wordpress-e-baven.html">защо WP е бавен</a>.</p></article>
        <article class="card"><h3>Колко време отнема?</h3><p>Визитка: 3–5 дни. Корпоративен: 10–14 дни.</p></article>
        <article class="card"><h3>Работите ли от София?</h3><p>Да — дистанционно за цяла България. <a href="/izrabotka-na-sait-sofia.html">София</a>.</p></article>
        <article class="card"><h3>Има ли месечни такси?</h3><p>Не. Само домейн + хостинг 23–48€/год.</p></article>
      </div>
      <p class="reveal" style="text-align:center;margin-top:1.5rem;"><a href="/faq.html">Всички въпроси →</a></p>
    </div>
  </section>

  <section class="section" id="contact">
    <div class="container reveal">
      <div class="contact-block">
        <h2>Запитване за проект</h2>
        <p>Опишете бизнеса си — ще отговорим в рамките на 24 часа с ясна посока и цена.</p>
        <div class="hero__actions" style="margin:1.5rem 0 1rem;">
          <a href="mailto:admin@moverstudio.online?subject=%D0%97%D0%B0%D0%BF%D0%B8%D1%82%D0%B2%D0%B0%D0%BD%D0%B5%20%D0%B7%D0%B0%20HTML%20%D1%81%D0%B0%D0%B9%D1%82" class="btn btn--primary">✉ Изпрати запитване</a>
          <a href="tel:+359877845569" class="btn btn--secondary">☎ +359 877 845 569</a>
        </div>
        <p style="font-size:0.85rem;">admin@moverstudio.online · Работим с клиенти от цяла България</p>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
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
</footer>

<script src="/js/site.js" defer></script>
</body>
</html>
'''

(ROOT / "index.html").write_text(out, encoding="utf-8")
print("index.html v2 written", len(out), "bytes")

# backup old
backup = ROOT / "index.html.bak-pre-redesign"
if not backup.exists():
    backup.write_text(old, encoding="utf-8")
    print("backup saved to index.html.bak-pre-redesign")
