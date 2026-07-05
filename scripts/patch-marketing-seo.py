#!/usr/bin/env python3
"""Marketing/SEO patches: hero CTAs, Sofia, FAQ snippets, korporativen guarantee."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
VIZ = "\u0432\u0438\u0437\u0438\u0442\u043a\u0430"


def patch(path: pathlib.Path, replacements: list[tuple[str, str]]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


# sait-vizitka hero
viz = ROOT / "sait-vizitka.html"
t = viz.read_text(encoding="utf-8")
marker = '<div class="price-hero">400€</div>'
if marker in t and "5% компенсация при закъснение" not in t:
    start = t.index(marker) + len(marker)
    end = t.index('<div class="quick-answer"', start)
    new_block = f"""
    <div>
      <a href="/calculator.html" class="cta-primary">Виж ориентировъчна цена</a>
      <a href="mailto:admin@moverstudio.online?subject=%D0%97%D0%B0%D0%BF%D0%B8%D1%82%D0%B2%D0%B0%D0%BD%D0%B5%3A%20%D1%81%D0%B0%D0%B9%D1%82%20%D0%B2%D0%B8%D0%B7%D0%B8%D1%82%D0%BA%D0%B0%20~400%E2%82%AC%20%E2%80%94%20%5B%D1%84%D0%B8%D1%80%D0%BC%D0%B0%5D" class="cta-primary">✉ Изпрати запитване</a>
      <a href="tel:+359877845569" class="cta-primary">☎ Обади се</a>
    </div>
    <div class="trust-signals">
      <span>✓ 1-5 страници</span>
      <span>✓ Цел 95–100 PageSpeed</span>
      <span>✓ SEO оптимизация</span>
      <span>✓ 5% компенсация при закъснение</span>
    </div>
    <div style="margin-top: 1rem; padding: 1rem 1.25rem; background: rgba(143, 71, 34, 0.08); border-left: 4px solid var(--brand); text-align: left; max-width: 52rem; margin-left: auto; margin-right: auto;">
      <p style="margin: 0; font-size: 0.95rem;"><strong>Изработка на HTML сайт от 400€</strong>, без WordPress, без месечни такси — цел 95–100 PageSpeed. Отговор на запитване ≤24h.</p>
    </div>
"""
    viz.write_text(t[:start] + new_block + t[end:], encoding="utf-8")
    print("sait-vizitka hero")

# korporativen guarantee strip
korp = ROOT / "korporativen-sait.html"
kt = korp.read_text(encoding="utf-8")
guarantee = """
    <div style="margin: 2rem 0; padding: 1rem 1.25rem; background: rgba(143, 71, 34, 0.08); border-left: 4px solid var(--brand);">
      <p style="margin: 0;"><strong>Изработка на HTML сайт от 400€ / корпоративен от 1000€</strong> — без WordPress, без месечни такси, цел 95–100 PageSpeed. При просрочен срок от наша страна: <strong>5% компенсация за всеки просрочен ден</strong>. Отговор ≤24h.</p>
    </div>
"""
if "5% компенсация за всеки просрочен ден" not in kt and "<!-- PRICING DETAILS -->" in kt:
    kt = kt.replace("  <!-- PRICING DETAILS -->", guarantee + "  <!-- PRICING DETAILS -->")
    korp.write_text(kt, encoding="utf-8")
    print("korporativen guarantee")

# Sofia page
sofia = ROOT / "izrabotka-na-sait-sofia.html"
if patch(sofia, [
    (
        "Фокусът ни е върху <strong>100 PageSpeed</strong>, ясна структура и силно SEO",
        "Фокусът ни е върху <strong>цел 95–100 PageSpeed</strong>, ясна структура и локално SEO за София",
    ),
    (
        """    <div>
      <a href="/calculator.html" class="cta-primary">Виж цена</a>
      <a href="tel:+359877845569" class="cta-primary">Заяви сайт</a>
    </div>""",
        """    <div>
      <a href="/calculator.html" class="cta-primary">Виж ориентировъчна цена</a>
      <a href="mailto:admin@moverstudio.online?subject=%D0%97%D0%B0%D0%BF%D0%B8%D1%82%D0%B2%D0%B0%D0%BD%D0%B5%3A%20%D0%B8%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%BD%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%20%D0%A1%D0%BE%D1%84%D0%B8%D1%8F%20~400%E2%82%AC%20%E2%80%94%20%5B%D1%84%D0%B8%D1%80%D0%BC%D0%B0%5D" class="cta-primary">✉ Изпрати запитване</a>
      <a href="tel:+359877845569" class="cta-primary">☎ Обади се</a>
    </div>""",
    ),
    (
        "Сайтът е пример за multi-location SEO архитектура без WordPress.",
        "Кейс с добавка multi-location (+200€) — не е част от базовите 1000€ корпоративен пакет.",
    ),
]):
    print("sofia page")

st = sofia.read_text(encoding="utf-8")
remote_note = """
    <p style="margin-top: 1.5rem; max-width: 52rem; margin-left: auto; margin-right: auto; font-size: 0.95rem; color: var(--text-muted);">
      <strong>Работим дистанционно за цяла България</strong> — процесът е онлайн; физическа среща в София не е задължителна.
      Пълен преглед на пакети: <a href="/izrabotka-na-sait.html">изработка на сайт</a> (hub).
    </p>
"""
anchor = "    </div>\n  </section>\n\n  <section>\n    <h2>Изработка на сайтове в София"
if "Работим дистанционно за цяла България" not in st and anchor in st:
    st = st.replace(anchor, "    </div>" + remote_note + "  </section>\n\n  <section>\n    <h2>Изработка на сайтове в София")
    sofia.write_text(st, encoding="utf-8")
    print("sofia remote note")

# FAQ featured snippets
faq = ROOT / "faq.html"
ft = faq.read_text(encoding="utf-8")
if "Колко струва изработка на сайт в България през 2026?" not in ft:
    new_faq_items = f"""
    <details class="faq-item">
      <summary>Колко струва изработка на сайт в България през 2026?</summary>
      <div class="faq-answer">
        {VIZ.capitalize()} или landing page: <strong>400€</strong> еднократно. Корпоративен сайт (база): <strong>1000€</strong>. Добавки: разширено SEO +100€, multi-location +200€, многоезичност +300€. Годишно: 23–48€ хостинг + домейн.
      </div>
    </details>

    <details class="faq-item">
      <summary>HTML или WordPress за малък бизнес?</summary>
      <div class="faq-answer">
        За {VIZ}, локален бизнес и фиксиран бюджет — <strong>HTML</strong>: еднократна цена, цел 95–100 PageSpeed, 23–48€/год. WordPress при чести самостоятелни публикации или e-commerce с backend.
      </div>
    </details>

    <details class="faq-item">
      <summary>Колко време отнема изработката на сайт?</summary>
      <div class="faq-answer">
        <strong>{VIZ.capitalize()}:</strong> 3–5 работни дни след съдържание. <strong>Корпоративен:</strong> 10–14 работни дни. С добавки (multi-location, SEO) — по договаряне.
      </div>
    </details>
"""
    ft = ft.replace(
        '    <p class="section-label">// 01 — Цени и бизнес модел</p>\n',
        '    <p class="section-label">// 01 — Цени и бизнес модел</p>\n' + new_faq_items,
    )
    entries = [
        {
            "@type": "Question",
            "name": "Колко струва изработка на сайт в България през 2026?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"{VIZ.capitalize()} или landing: 400€. Корпоративен база: 1000€. Добавки SEO +100€, multi-location +200€. Годишно 23–48€.",
            },
        },
        {
            "@type": "Question",
            "name": "HTML или WordPress за малък бизнес?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"HTML за {VIZ} и фиксиран бюджет: еднократна цена, 95–100 PageSpeed цел, 23–48€/год.",
            },
        },
        {
            "@type": "Question",
            "name": "Колко време отнема изработката на сайт?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"{VIZ.capitalize()}: 3–5 работни дни. Корпоративен: 10–14 работни дни.",
            },
        },
    ]
    for entry in reversed(entries):
        ft = ft.replace('"mainEntity": [', '"mainEntity": [\n      ' + json.dumps(entry, ensure_ascii=False) + ',', 1)
    faq.write_text(ft, encoding="utf-8")
    print("faq snippets")

# index meta
patch(ROOT / "index.html", [
    ("100 PageSpeed, без WordPress", "цел 95–100 PageSpeed, без WordPress"),
])

# izrabotka-na-landing-page 5% if missing
landing = ROOT / "izrabotka-na-landing-page.html"
lt = landing.read_text(encoding="utf-8")
if "5% компенсация" not in lt and "<main" in lt:
    strip = """
  <div style="max-width: var(--max-width); margin: 0 auto 2rem; padding: 1rem 1.25rem; background: rgba(143, 71, 34, 0.08); border-left: 4px solid var(--brand);">
    <p style="margin: 0; font-size: 0.95rem;"><strong>От 400€</strong> · без месечни такси · цел 95–100 PageSpeed · <strong>5% компенсация</strong> при просрочен срок · отговор ≤24h</p>
  </div>
"""
    lt = lt.replace("<main", strip + "<main", 1)
    landing.write_text(lt, encoding="utf-8")
    print("landing guarantee strip")

fa_count = sum(1 for p in ROOT.rglob("*.html") if "fontawesome" in p.read_text(encoding="utf-8"))
print(f"fontawesome refs remaining: {fa_count}")
