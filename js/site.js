(function () {
  'use strict';

  /* Mobile navigation */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
      nav.classList.toggle('is-open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        document.body.style.overflow = '';
      });
    });
  }

  /* Scroll reveal — respects reduced motion */
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var els = document.querySelectorAll('.reveal');
    if (els.length && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      els.forEach(function (el) { io.observe(el); });
    } else {
      els.forEach(function (el) { el.classList.add('is-visible'); });
    }
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.add('is-visible');
    });
  }

  /* Conversion tracking */
  window.dataLayer = window.dataLayer || [];
  function trackConversion(name, details) {
    try { window.dataLayer.push({ event: name, details: details }); } catch (e) { /* noop */ }
  }
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('a');
    if (!el) return;
    var href = el.getAttribute('href') || '';
    if (
      href.indexOf('#contact') !== -1 ||
      href.indexOf('mailto:') === 0 ||
      href.indexOf('tel:') === 0 ||
      href.indexOf('wa.me') !== -1 ||
      href.indexOf('viber:') === 0
    ) {
      trackConversion('contact_cta_click', { href: href, text: (el.textContent || '').trim() });
    }
  });

  function ensureStatus(form) {
    var status = form.querySelector('.lead-form__status');
    if (!status) {
      status = document.createElement('p');
      status.className = 'lead-form__status';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      form.appendChild(status);
    }
    return status;
  }

  function setStatus(form, type, text) {
    var status = ensureStatus(form);
    status.className = 'lead-form__status lead-form__status--' + type;
    status.textContent = text;
  }

  function mailtoFallback(name, phone, msg, subject) {
    var body = 'Име/фирма: ' + name + '\nТелефон: ' + phone + '\n\n' + msg;
    window.location.href = 'mailto:admin@moverstudio.online?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  /* Lead forms → /lead.php (primary), mailto fallback */
  document.querySelectorAll('form.lead-form').forEach(function (form) {
    form.setAttribute('action', '/lead.php');
    form.setAttribute('method', 'post');

    if (!form.querySelector('[name="company_url"]')) {
      var hp = document.createElement('input');
      hp.type = 'text';
      hp.name = 'company_url';
      hp.value = '';
      hp.tabIndex = -1;
      hp.autocomplete = 'off';
      hp.className = 'hp-field';
      hp.setAttribute('aria-hidden', 'true');
      form.appendChild(hp);
    }

    if (!form.querySelector('[name="page"]')) {
      var page = document.createElement('input');
      page.type = 'hidden';
      page.name = 'page';
      page.value = window.location.pathname || '/';
      form.appendChild(page);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name="name"]') || {}).value || '';
      var phone = (form.querySelector('[name="phone"]') || {}).value || '';
      var msg = (form.querySelector('[name="body"], textarea') || {}).value || '';
      var subjectEl = form.querySelector('[name="subject"]');
      var subject = (subjectEl && subjectEl.value) || 'Запитване от сайта';
      var honeypot = (form.querySelector('[name="company_url"]') || {}).value || '';
      var submitBtn = form.querySelector('button[type="submit"]');

      if (!name.trim() || !phone.trim() || !msg.trim()) {
        setStatus(form, 'error', 'Моля попълнете име, телефон и кратко описание.');
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
      }
      setStatus(form, 'pending', 'Изпращане…');

      var payload = {
        name: name.trim(),
        phone: phone.trim(),
        body: msg.trim(),
        subject: subject,
        company_url: honeypot,
        page: window.location.pathname || '/'
      };

      trackConversion('lead_form_submit', { subject: subject, channel: 'lead.php' });

      fetch('/lead.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'same-origin'
      }).then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok && data && data.ok, data: data, status: res.status };
        }).catch(function () {
          return { ok: false, data: null, status: res.status };
        });
      }).then(function (result) {
        if (result.ok) {
          setStatus(form, 'success', 'Получихме запитването. Отговаряме до 24 часа — или пишете ни директно във WhatsApp/Viber.');
          form.reset();
          var pageInput = form.querySelector('[name="page"]');
          if (pageInput) pageInput.value = window.location.pathname || '/';
          trackConversion('lead_form_success', { subject: subject });
          return;
        }
        trackConversion('lead_form_fallback_mailto', { subject: subject, status: result.status });
        setStatus(form, 'error', 'Сървърната изпратка не успя — отваряме имейл клиента като резервен канал.');
        mailtoFallback(name, phone, msg, subject);
      }).catch(function () {
        trackConversion('lead_form_fallback_mailto', { subject: subject, reason: 'network' });
        setStatus(form, 'error', 'Няма връзка към сървъра — отваряме имейл клиента като резервен канал.');
        mailtoFallback(name, phone, msg, subject);
      }).finally(function () {
        if (submitBtn) submitBtn.disabled = false;
      });
    });
  });

  window.moverStudio = window.moverStudio || {};
  window.moverStudio.trackConversion = trackConversion;
})();
