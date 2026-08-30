#!/usr/bin/env python3
"""Insert project showcase block into case-studies.html."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "case-studies.html"

PROJECTS = [
    {
        "id": "roadassistancesofia",
        "name": "roadassistancesofia.bg",
        "url": "https://roadassistancesofia.bg",
        "badges": ["Корпоративен", "14 локации", "Multi-location SEO"],
        "metric": "14 HTML страници",
        "desc": "Пътна помощ София — отделна страница за всеки район, без WordPress.",
        "slug": "roadassistancesofia",
        "anchor": "#portfolio-detailed",
    },
    {
        "id": "patna-pomosht",
        "name": "patna-pomosht-kostinbrod.bg",
        "url": "https://patna-pomosht-kostinbrod.bg",
        "badges": ["Калкулатор", "11 локации", "5.0 / 106 отзива"],
        "metric": "460 клика · GSC",
        "desc": "Най-силният органичен резултат — 35+ хил. импресии, позиция 6.7.",
        "slug": "patna-pomosht-kostinbrod",
        "anchor": "#portfolio-detailed",
    },
    {
        "id": "matiyhelp",
        "name": "matiyhelp.bg",
        "url": "https://matiyhelp.bg",
        "badges": ["4 езика", "12 локации", "hreflang"],
        "metric": "13,4 хил. импресии",
        "desc": "BG/EN/RO/TR — отделни HTML файлове, без i18n библиотеки.",
        "slug": "matiyhelp",
        "anchor": "#portfolio-detailed",
    },
    {
        "id": "nikoautogaz",
        "name": "nikoautogaz.github.io",
        "url": "https://nikoautogaz.github.io",
        "badges": ["GitHub Pages", "Автогаз", "96+ reviews"],
        "metric": "270 клика · CTR 7.1%",
        "desc": "Поддомейн github.io — позиция 5.9 без собствен домейн.",
        "slug": "nikoautogaz",
        "anchor": "#portfolio-detailed",
    },
    {
        "id": "re-peat",
        "name": "re-peat.store",
        "url": "https://re-peat.store",
        "badges": ["Локален магазин", "PageSpeed 100", "Conversion"],
        "metric": "180 клика · GSC",
        "desc": "Физически обект в София — не e-commerce, а локално откриване.",
        "slug": "re-peat",
        "anchor": "#portfolio-detailed",
    },
    {
        "id": "bdinhost",
        "name": "bdinhost.com",
        "url": "https://bdinhost.com",
        "badges": ["WP → HTML", "Миграция", "PageSpeed 100"],
        "metric": "75 → 100 PageSpeed",
        "desc": "WordPress срещу HTML на един хост — structured data 3 → 13.",
        "slug": "bdinhost",
        "anchor": "#graphs",
    },
    {
        "id": "minibagerkb",
        "name": "minibagerkb.eu",
        "url": "https://minibagerkb.eu",
        "badges": ["Собствен домейн", "Локално SEO", "Наш екип"],
        "metric": "CTR 15.8% · GSC",
        "desc": "Минибагер Костинброд — районни страници, ранен органичен старт.",
        "slug": "minibagerkb",
        "anchor": "#minibagerkb",
    },
]

MARKER = '      <section id="results" style="margin-top: 2.5rem;">'

BLOCK = """
      <section id="projects-overview" style="margin-top: 2.5rem;">
        <h2>Проекти накратко — сайт и Google</h2>
        <p style="text-align:center;max-width:52rem;margin:0 auto 1.5rem;">
          За всеки проект: актуален скрийншот на сайта и резултат от Google (август 2026).
          Пълни технически детайли — по-долу в страницата.
        </p>
        <div class="projects-showcase">
"""

for p in PROJECTS:
    badges = "".join(f'<span class="project-badge">{b}</span>' for b in p["badges"])
    BLOCK += f"""
          <article class="project-card-v2" id="{p['id']}">
            <div class="project-card-v2__head">
              <div class="project-card-v2__meta">{badges}</div>
              <h3><a href="{p['url']}" target="_blank" rel="noopener">{p['name']}</a></h3>
              <p class="project-card-v2__metric">{p['metric']}</p>
              <p class="project-card-v2__desc">{p['desc']}</p>
            </div>
            <div class="project-card-v2__shots">
              <figure>
                <img src="/images/portfolio-2026/{p['slug']}-site.webp" alt="Скрийншот на {p['name']}" loading="lazy" width="1280" height="800">
                <figcaption>Сайт</figcaption>
              </figure>
              <figure>
                <img src="/images/portfolio-2026/{p['slug']}-search.webp" alt="Търсене за {p['name']}" loading="lazy" width="1280" height="800">
                <figcaption>DuckDuckGo търсене</figcaption>
              </figure>
            </div>
            <div class="project-card-v2__foot">
              <a href="{p['url']}" class="cta-secondary" target="_blank" rel="noopener">Отвори сайта</a>
              <a href="{p['anchor']}" class="cta-primary">Технически детайли</a>
            </div>
          </article>
"""

BLOCK += """
        </div>
      </section>

"""

MINIBAGER_SECTION = """
        <div class="proof" id="minibagerkb" style="margin-bottom: 2rem;">
          <h3><a href="https://minibagerkb.eu">minibagerkb.eu</a> – Минибагер Костинброд (наш свързан бизнес)</h3>
          <div class="portfolio-grid" style="margin-bottom: 1.25rem;">
            <figure class="portfolio-item">
              <img src="/images/portfolio-2026/minibagerkb-site.webp" alt="Начална страница на minibagerkb.eu" loading="lazy" width="1280" height="800">
              <figcaption>Начална страница</figcaption>
            </figure>
            <figure class="portfolio-item">
              <img src="/images/portfolio-2026/minibagerkb-mobile.webp" alt="Мобилен изглед на minibagerkb.eu" loading="lazy" width="390" height="844">
              <figcaption>Мобилен изглед</figcaption>
            </figure>
            <figure class="portfolio-item">
              <img src="/images/gsc-minibagerkb.webp" alt="Search Console за minibagerkb.eu" loading="lazy" width="1400" height="788">
              <figcaption>Search Console</figcaption>
            </figure>
            <figure class="portfolio-item">
              <img src="/images/portfolio-2026/minibagerkb-google.webp" alt="Google резултати за минибагер Костинброд" loading="lazy" width="1280" height="800">
              <figcaption>Google търсене</figcaption>
            </figure>
          </div>
          <p><strong>Какво показва проектът:</strong></p>
          <ul>
            <li>Собствен домейн <strong>minibagerkb.eu</strong> — районни landing pages за изкопни услуги</li>
            <li>Multi-location SEO архитектура — отделни HTML страници по населени места</li>
            <li>Dual sitemap (txt + xml), Google Maps и Facebook sameAs в schema</li>
            <li>Бърз hero с ясен CTA (Viber, телефон) — mobile-first</li>
          </ul>
          <p><strong>Search Console (реални данни):</strong> CTR 15.8% · 22 клика / 139 импресии за 7 дни · средна позиция 5.8.</p>
          <p><em>Google 5.0 / 106 отзива принадлежат на Пътна помощ Костинброд — не на minibagerkb.eu.</em></p>
        </div>

"""

EASTER = """<!-- Easter Egg: Mouse Coordinates Over H1 -->
<script>
(function() {
  const h1 = document.querySelector('h1');
  if (!h1) return;
  
  // Create coordinate display element
  const coordDisplay = document.createElement('div');
  coordDisplay.style.cssText = `
    position: fixed;
    display: none;
    background: rgba(242, 238, 227, 0.95);
    border: 1px solid #1a1e22;
    padding: 0.5rem 0.75rem;
    font-family: 'Share Tech Mono', 'Courier New', monospace;
    font-size: 0.75rem;
    color: #1a1e22;
    pointer-events: none;
    z-index: 9999;
    letter-spacing: 0.05em;
    box-shadow: 2px 2px 8px rgba(26, 30, 34, 0.15);
    white-space: nowrap;
  `;
  document.body.appendChild(coordDisplay);
  
  // Track mouse position when hovering over H1
  h1.addEventListener('mouseenter', function() {
    coordDisplay.style.display = 'block';
  });
  
  h1.addEventListener('mouseleave', function() {
    coordDisplay.style.display = 'none';
  });
  
  h1.addEventListener('mousemove', function(event) {
    const x = Math.round(event.clientX);
    const y = Math.round(event.clientY);
    coordDisplay.textContent = `X: ${x} | Y: ${y}`;
    
    // Position the display near the cursor (offset by a few pixels)
    coordDisplay.style.left = (x + 12) + 'px';
    coordDisplay.style.top = (y - 32) + 'px';
  });
})();
</script>

"""

text = PATH.read_text(encoding="utf-8")

if "id=\"projects-overview\"" not in text:
    if MARKER not in text:
        raise SystemExit("Marker not found")
    text = text.replace(MARKER, BLOCK + MARKER, 1)
    print("Inserted projects-overview")

if 'id="minibagerkb"' not in text:
    anchor = '        <div class="proof">\n          <h3>MOVER Studio Methodology:'
    if anchor in text:
        text = text.replace(anchor, MINIBAGER_SECTION + anchor, 1)
        print("Inserted minibagerkb section")

if EASTER in text:
    text = text.replace(EASTER, "", 1)
    print("Removed easter egg")

PATH.write_text(text, encoding="utf-8")
print("Done.")
