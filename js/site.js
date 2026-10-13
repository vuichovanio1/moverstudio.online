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
    if (href.indexOf('#contact') !== -1 || href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0 || href.indexOf('wa.me') !== -1) {
      trackConversion('contact_cta_click', { href: href, text: (el.textContent || '').trim() });
    }
  });

  /* Lead forms → composed mailto (static hosting, no backend) */
  document.querySelectorAll('form.lead-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name="name"]') || {}).value || '';
      var phone = (form.querySelector('[name="phone"]') || {}).value || '';
      var msg = (form.querySelector('[name="body"], textarea') || {}).value || '';
      var subjectEl = form.querySelector('[name="subject"]');
      var subject = (subjectEl && subjectEl.value) || 'Запитване от сайта';
      var body = 'Име/фирма: ' + name + '\nТелефон: ' + phone + '\n\n' + msg;
      trackConversion('lead_form_submit', { subject: subject });
      window.location.href = 'mailto:admin@moverstudio.online?subject=' +
        encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  });

  window.moverStudio = window.moverStudio || {};
  window.moverStudio.trackConversion = trackConversion;
})();
