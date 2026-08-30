#!/usr/bin/env python3
"""Replace case-studies projects-overview with Google-proof cards."""

import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "case-studies.html"


def g(q: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(q) + "&hl=bg&gl=bg"


def chips(queries: list[str]) -> str:
    lines = [
        f'                <a class="search-chip" href="{g(q)}" target="_blank" rel="noopener noreferrer">{q}</a>'
        for q in queries
    ]
    return "\n".join(lines)


def proof(queries: list[str], note: str = "") -> str:
    note_line = f'\n              <p class="google-proof__note">{note}</p>' if note else ""
    return f"""            <div class="google-proof">
              <p class="google-proof__lead">Провери сам в Google</p>{note_line}
              <div class="google-proof__queries">
{chips(queries)}
              </div>
            </div>"""


def card(
    pid: str,
    badges: list[str],
    title: str,
    url: str,
    metric: str,
    desc: str,
    queries: list[str],
    img: str | None = None,
    img_alt: str = "",
    note: str = "",
    detail_href: str = "#portfolio-detailed",
    external: bool = True,
) -> str:
    badge_html = "".join(f'<span class="project-badge">{b}</span>' for b in badges)
    rel = ' target="_blank" rel="noopener"' if external else ""
    img_block = ""
    if img:
        img_block = f"""
            <div class="project-card-v2__body">
              <figure>
                <img src="{img}" alt="{img_alt}" loading="lazy" width="1280" height="800">
                <figcaption>Сайт</figcaption>
              </figure>
              {proof(queries, note)}
            </div>"""
    else:
        img_block = f"""
            <div class="project-card-v2__body" style="padding:0.75rem;">
              {proof(queries, note)}
            </div>"""

    return f"""
          <article class="project-card-v2" id="{pid}">
            <div class="project-card-v2__head">
              <div class="project-card-v2__meta">{badge_html}</div>
              <h3><a href="{url}"{rel}>{title}</a></h3>
              <p class="project-card-v2__metric">{metric}</p>
              <p class="project-card-v2__desc">{desc}</p>
            </div>{img_block}
            <div class="project-card-v2__foot">
              <a href="{url}" class="cta-secondary"{rel}>{"Отвори сайта" if external else "Виж услугите"}</a>
              <a href="{detail_href}" class="cta-primary">Още информация</a>
            </div>
          </article>"""


SECTION = f"""
      <section id="projects-overview" style="margin-top: 2.5rem;">
        <div class="google-proof-banner" id="proveri-v-google">
          <h2>Провери сам в Google</h2>
          <p>Кликни на фраза — виж проекта <strong>сред резултатите</strong>, не на скрийншот. Search Console данните остават по-долу за любопитни.</p>
          <p class="google-proof-banner__framing">При конкурентни заявки позицията може да варира — важното е, че сме на първа страница, не на петата.</p>
          <a href="{g("mover studio html сайт")}" class="cta-primary" target="_blank" rel="noopener noreferrer">Потърси MOVER Studio в Google</a>
        </div>
        <div class="projects-showcase">
{card(
    "mover-studio",
    ["MOVER Studio", "Услуги"],
    "MOVER Studio — изработка на HTML сайтове",
    "/izrabotka-na-sait.html",
    "От 400€ · без WordPress",
    "Нашите услуги — потърси как стоят в Google преди да поръчаш.",
    [
        "изработка на html сайт",
        "изработка на лендинг страница",
        "алтернатива на wordpress",
        "изработка на сайт софия",
    ],
    note="Търси от телефона или desktop — резултатите може леко да се различават по локация.",
    detail_href="/izrabotka-na-sait.html",
    external=False,
)}
{card(
    "roadassistancesofia",
    ["Корпоративен", "14 локации", "Multi-location"],
    "roadassistancesofia.bg",
    "https://roadassistancesofia.bg",
    "14 HTML страници",
    "Пътна помощ в софийски райони — отделна landing за всеки район (не централна София).",
    [
        "пътна помощ младост",
        "пътна помощ люлин",
        "пътна помощ требич",
        "пътна помощ негован",
        "пътна помощ нови искър",
        "пътна помощ световрачене",
        "пътна помощ студентски град",
    ],
    "/images/portfolio-2026/roadassistancesofia-site.webp",
    "roadassistancesofia.bg",
    "Покрива районите на обслужване — пробвай квартал или село около София.",
)}
{card(
    "patna-pomosht",
    ["Калкулатор", "11 локации", "5.0 / 106 отзива"],
    "patna-pomosht-kostinbrod.bg",
    "https://patna-pomosht-kostinbrod.bg",
    "460 клика · GSC",
    "Пътна помощ Костинброд и региона — най-силният органичен резултат в портфолиото.",
    [
        "пътна помощ костинброд",
        "пътна помощ божурище",
        "пътна помощ сливница",
        "пътна помощ драгоман",
        "пътна помощ годеч",
        "пътна помощ ботевград",
    ],
    "/images/portfolio-2026/patna-pomosht-kostinbrod-site.webp",
    "patna-pomosht-kostinbrod.bg",
)}
{card(
    "matiyhelp",
    ["4 езика", "12 локации", "hreflang"],
    "matiyhelp.bg",
    "https://matiyhelp.bg",
    "13,4 хил. импресии",
    "Пътна помощ на границата и Западна София — отделни HTML файлове по език.",
    [
        "пътна помощ годеч",
        "пътна помощ калотина",
        "пътна помощ петрохан",
        "пътна помощ драгоман",
        "пътна помощ сливница",
    ],
    "/images/portfolio-2026/matiyhelp-site.webp",
    "matiyhelp.bg",
    "Същият екип като PPK — пробвай населено място от зоната на обслужване.",
)}
{card(
    "minibagerkb",
    ["Собствен домейн", "Локално SEO", "Наш екип"],
    "minibagerkb.eu",
    "https://minibagerkb.eu",
    "CTR 15.8% · GSC",
    "Минибагер Костинброд — районни страници за изкопни услуги.",
    [
        "мини багер костинброд",
        "мини багер сливница",
        "мини багер драгоман",
        "мини багер божурище",
        "мини багер годеч",
        "мини багер софия област",
    ],
    "/images/portfolio-2026/minibagerkb-site.webp",
    "minibagerkb.eu",
    detail_href="#minibagerkb-detail",
)}
{card(
    "nikoautogaz",
    ["GitHub Pages", "Автогаз", "96+ reviews"],
    "nikoautogaz.github.io",
    "https://nikoautogaz.github.io",
    "270 клика · CTR 7.1%",
    "Автогаз сервиз в София — силен локален резултат дори на github.io.",
    [
        "ремонт фабричен метан",
        "ремонт на фабричен метан",
        "ремонт на метанова уредба софия",
        "автогаз софия",
        "газова уредба софия",
    ],
    "/images/portfolio-2026/nikoautogaz-site.webp",
    "nikoautogaz.github.io",
)}
{card(
    "re-peat",
    ["Локален магазин", "PageSpeed 100"],
    "re-peat.store",
    "https://re-peat.store",
    "180 клика · GSC",
    "Физически магазин за дрехи втора употреба в София — локално откриване, не онлайн магазин.",
    [
        "дрехи втора ръка софия",
        "дрехи втора употреба софия",
        "употребявани дрехи софия",
    ],
    "/images/portfolio-2026/re-peat-site.webp",
    "re-peat.store",
)}
{card(
    "bdinhost",
    ["WP → HTML", "Миграция", "Хостинг"],
    "bdinhost.com",
    "https://bdinhost.com",
    "75 → 100 PageSpeed",
    "Хостинг + доказана WordPress → HTML миграция на същата инфраструктура.",
    [
        "евтин хостинг",
        "евтин хостинг българия",
        "хостинг българия",
    ],
    "/images/portfolio-2026/bdinhost-site.webp",
    "bdinhost.com",
    detail_href="#graphs",
)}
        </div>
      </section>
"""

text = PATH.read_text(encoding="utf-8")
pattern = re.compile(
    r'      <section id="projects-overview".*?</section>\s*\n      <section id="results"',
    re.DOTALL,
)
if not pattern.search(text):
    raise SystemExit("Section not found")
text = pattern.sub(SECTION + "\n      <section id=\"results\"", text, count=1)
PATH.write_text(text, encoding="utf-8")
print("Updated case-studies.html projects-overview")
