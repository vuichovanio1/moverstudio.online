#!/usr/bin/env python3
"""Patch hero CTAs, Sofia page, FAQ snippets, calculator mailto."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

# --- sait-vizitka hero ---
viz = ROOT / "sait-vizitka.html"
t = viz.read_text(encoding="utf-8")
old_viz = """      <a href="/calculator.html" class="cta-primary">Изчисли цена за визitka или портфолио</a>
      <a href="tel:+359877845569" class="cta-primary">☎ Обади се за бърза оферта</a>
    </div>
    <div class="trust-signals">
      <span>✓ 1-5 страници</span>
      <span>✓ 100 PageSpeed</span>
      <span>✓ SEO оптимизация</span>
      <span>✓ Годишни разходи: 23-48€</span>
    </div>"""
old_viz = old_viz.replace("визitka", "визitka")
old_viz = old_viz.replace("визitka", "\u0432\u0438\u0437\u0438\u0442\u043a\u0430")
new_viz = """      <a href="/calculator.html" class="cta-primary">Виж ориентировъчна цена</a>
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
    </div>"""
if old_viz in t:
    viz.write_text(t.replace(old_viz, new_viz), encoding="utf-8")
    print("sait-vizitka hero")

# --- calculator sendPrompt ---
calc = ROOT / "calculator.html"
ct = calc.read_text(encoding="utf-8")
old_fn = """function sendPrompt(message) {
  const subject = encodeURIComponent('Запитване от калкулатора — MOVER Studio');
  const body = encodeURIComponent(message + '\\n\\nИме:\\nТелефон за връзка:\\nДопълнителна информация:');
  window.location.href = 'mailto:admin@moverstudio.online?subject=' + subject + '&body=' + body;
}"""
new_fn = """function sendPrompt(message) {
  const total = document.getElementById('total').textContent;
  const subject = encodeURIComponent('Запитване: ' + baseName + ' ~' + total + ' — [фирма]');
  const body = encodeURIComponent(message + '\\n\\nФирма:\\nТелефон:\\nДопълнителна информация:');
  window.location.href = 'mailto:admin@moverstudio.online?subject=' + subject + '&body=' + body;
}"""
if old_fn in ct:
    calc.write_text(ct.replace(old_fn, new_fn), encoding="utf-8")
    print("calculator mailto")
