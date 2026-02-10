# MOVER Studio — moverstudio.online

> Българска уеб агенция за изработка на статични HTML сайтове с гарантиран **100/100 Google PageSpeed**.  
> Без WordPress. Без CMS. Без месечни такси.

---

## Какво е това

Production-ready уебсайт на MOVER Studio — изцяло статичен, ръчно кодиран с inline CSS, нулеви външни зависимости и пълна SEO оптимизация. Всяка страница постига 100/100 PageSpeed Insights на мобилен и десктоп.

## Структура на проекта

```
moverstudio.online/
├── index.html                          # Начална страница
├── izrabotka-na-sait.html              # Изработка на сайт (hub page)
├── sait-vizitka.html                   # Сайт визитка — пакет от 400€
├── korporativen-sait.html              # Корпоративен сайт — пакет от 1000€
├── wordpress-alternativa.html          # WordPress алтернатива
├── pagespeed-100-html.html             # Защо 100 PageSpeed е важен
├── seo-optimizacia.html                # SEO оптимизация услуга
├── dokazatelstva.html                  # Доказателства и резултати
├── calculator.html                     # Калкулатор: загуби от бавен сайт
├── case-studies.html                   # Case studies
├── how-we-do-it.html                   # Как работим (процес)
├── about.html                          # За нас
├── 404.html                            # Персонализирана 404 страница
│
├── blog/
│   ├── index.html                      # Блог index
│   ├── zashto-wordpress-e-baven.html   # Защо WordPress е бавен?
│   └── 5-prichini-da-napusnesh-wordpress-dnes.html
│
├── .htaccess                           # Apache конфигурация (cPanel)
├── _headers                            # Security headers (Cloudflare Pages)
├── robots.txt                          # Разрешен достъп за всички ботове + AI
├── sitemap.xml                         # XML sitemap (14 URL-а)
├── llms.txt                            # LLMs.txt стандарт — кратък контекст
├── llms-full.txt                       # LLMs.txt — пълно съдържание
├── humans.txt                          # humans.txt стандарт
├── favicon.svg                         # SVG favicon
├── og-image.png                        # Open Graph изображение
└── og-image.svg                        # OG image source
```

## Технологии и оптимизации

### Frontend

| Компонент | Решение |
|-----------|---------|
| Markup | Чист HTML5, семантичен |
| Стилове | Inline CSS (в `<style>` блок), CSS custom properties, `clamp()` типография |
| JavaScript | Минимален inline JS, без frameworks (React, Vue, Angular) |
| Шрифтове | System monospace stack (`ui-monospace, SFMono-Regular, Menlo, Consolas`) |
| Икони | Unicode емоджита вместо FontAwesome |
| Изображения | SVG favicon, PNG Open Graph, `data:` URI където е нужно |

### Performance (100/100 PageSpeed)

- **Zero external dependencies** — нито един външен CSS, JS, font или CDN request
- **Inline CSS** — целият стайлинг е вграден в `<style>` блока на HTML
- **Inline JS** — без външни скриптове
- **System fonts** — нулеви font requests
- **No render-blocking resources** — нищо не блокира рендерирането
- **Minimal DOM** — семантичен HTML без излишни wrapper елементи
- **SVG favicon** — без допълнителни заявки за `.ico`

### Security Headers

Конфигурирани в `.htaccess` (за Apache/cPanel) и `_headers` (за Cloudflare Pages):

| Header | Стойност |
|--------|----------|
| Content-Security-Policy | `default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'` |
| X-Content-Type-Options | `nosniff` |
| X-Frame-Options | `DENY` |
| Strict-Transport-Security | `max-age=31536000; includeSubDomains; preload` |
| Cross-Origin-Opener-Policy | `same-origin` |
| Cross-Origin-Embedder-Policy | `require-corp` |
| Permissions-Policy | `interest-cohort=()` |
| Referrer-Policy | `strict-origin-when-cross-origin` |
| Require-Trusted-Types-For | `'script'` |

### Apache .htaccess оптимизации

- HTTPS принуждаване (301 redirect)
- www → non-www канонизация
- Gzip компресия (`mod_deflate`) за HTML, CSS, JS, SVG, JSON, XML
- Browser caching (`mod_expires`): HTML 1 ден, CSS/JS/images 1 година
- ETag деактивиран (използват се Expires хедъри)
- Блокиране на directory listing (`Options -Indexes`)
- Защита на `.htaccess`, `_headers`, `.git` файлове
- Custom 404 error page
- `/blog` → `/blog/` trailing slash redirect

### SEO оптимизации

- **Schema.org structured data**: Унифициран @graph формат за всички страници (Organization, Service, WebPage, WebSite, Product, HowTo, FAQPage, BreadcrumbList, BlogPosting)
- **Open Graph** meta тагове на всяка страница
- **Twitter Cards** meta тагове
- **Canonical URLs** на всяка страница
- **hreflang** тагове (`bg`)
- **XML Sitemap** с 14 URL-а и приоритети
- **robots.txt** — пълен достъп за всички search engine и AI ботове
- **Quick Answer блокове** — AI-оптимизирани обобщения след H1
- **Стратегическо вътрешно линкване** между всички страници
- **Mobile-first responsive design**

### AI / LLM оптимизации

- **llms.txt** — следва [llmstxt.org](https://llmstxt.org/) стандарта, кратък контекст за AI модели
- **llms-full.txt** — пълно съдържание за задълбочен AI контекст
- **robots.txt** — изрично `Allow: /` за GPTBot, ClaudeBot, Google-Extended, anthropic-ai, PerplexityBot, ChatGPT-User, Bytespider, cohere-ai
- **humans.txt** — стандартизирана информация за екипа

### Дизайн

- **Matrix тема**: черен фон (`#000`), зелени акценти (`#00ff41`), monospace шрифтове
- **WCAG AAA** контраст
- **Responsive**: `clamp()` за типография, mobile-first подход
- **CSS Custom Properties**: централизирани в `:root`

## Ценообразуване

| Пакет | Цена | Страници | Включено |
|-------|------|----------|----------|
| Сайт Визитка | от 400€ | 1–5 | SEO, responsive, 100 PageSpeed |
| Корпоративен | от 1000€ | 5–15 | multi-location SEO, schema markup |
| Custom Project | от 1500€ | без лимит | всичко по заявка |

Годишни разходи за хостинг: от **23€** (домейн + хостинг). Нулеви месечни такси за CMS поддръжка.

## Хостинг

- **Основен**: cPanel (Apache) с `.htaccess` конфигурация
- **Алтернативен**: Cloudflare Pages с `_headers` файл
- **SSL**: Let's Encrypt
- **Домейн**: moverstudio.online

## Локална разработка

```bash
git clone https://github.com/elenarr87/moverstudio.online.git
cd moverstudio.online
# Отвори в VS Code и редактирай HTML файловете директно
# Няма build step — файловете са production-ready
```

Не се изисква Node.js, npm или build process. Файловете се обслужват директно от Apache или друг static file server.

## Deployment

Push към `main` клона → автоматичен deploy. Без build steps.

```bash
git add .
git commit -m "описание на промяната"
git push origin main
```

## SEO ключови думи по страница

| Страница | Целева ключова дума |
|----------|---------------------|
| index.html | изработка на html сайт, изработка на сайтове |
| izrabotka-na-sait.html | изработка на сайт |
| sait-vizitka.html | сайт визитка цена |
| korporativen-sait.html | корпоративен сайт |
| wordpress-alternativa.html | wordpress алтернатива |
| pagespeed-100-html.html | pagespeed 100, бърз сайт |
| seo-optimizacia.html | seo оптимизация цена |
| dokazatelstva.html | html seo резултати |
| calculator.html | колко губя от бавен сайт |
| case-studies.html | case study уеб дизайн |
| how-we-do-it.html | как се прави сайт |
| about.html | уеб агенция България |

## Roadmap

- [x] 14 статични HTML страници
- [x] 100/100 PageSpeed на всички страници
- [x] Пълна SEO имплементация (Schema.org @graph, OG, Twitter Cards)
- [x] Security headers (CSP, HSTS, X-Frame-Options и др.)
- [x] Mobile-first responsive дизайн
- [x] .htaccess оптимизация (компресия, кеширане, HTTPS)
- [x] AI/LLM оптимизация (llms.txt, robots.txt)
- [x] Блог секция (2 статии)
- [x] Case studies страница
- [x] Процес страница (how-we-do-it)
- [x] About страница
- [ ] Разширяване на блог съдържанието
- [ ] Многоезична поддръжка (EN)
- [ ] Analytics интеграция

## Контакт

**MOVER Studio**  
Имейл: admin@moverstudio.online  
Телефон: +359 877 845 569  
Уеб: https://moverstudio.online

## Лиценз

Проектът е собственост на MOVER Studio. Всички права запазени.