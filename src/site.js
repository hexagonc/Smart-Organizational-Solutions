// Smart Organizational Solutions: small progressive-enhancement script.
// Replaces the former in-browser React/Babel app. Pages are pre-rendered HTML.
(function () {
  'use strict';

  // Navbar shadow on scroll
  var nav = document.getElementById('site-nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 50); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Collapse the mobile menu after a link is tapped
  document.querySelectorAll('#navbarNav .nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      var menu = document.getElementById('navbarNav');
      if (menu && menu.classList.contains('show') && window.bootstrap) {
        window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  });

  // ===== Contact form (config.json -> API Gateway + Lambda + SES) =====
  var form = document.getElementById('contact-form');
  if (!form) return;

  var $ = function (id) { return document.getElementById(id); };
  var fields = ['cf-name', 'cf-email', 'cf-interest', 'cf-message', 'cf-submit'].map($);
  var submitBtn = $('cf-submit');
  var errorBox = $('contact-error');
  var config = null;

  function setEnabled(on) { fields.forEach(function (el) { el.disabled = !on; }); }
  function showError(msg) {
    errorBox.textContent = msg;
    errorBox.classList.toggle('d-none', !msg);
  }

  fetch('config.json', { cache: 'no-cache' })
    .then(function (res) { if (!res.ok) throw new Error(); return res.json(); })
    .then(function (cfg) {
      config = (cfg && cfg.contact) || {};
      if (config.email) {
        var a = $('contact-email');
        a.href = 'mailto:' + config.email;
        a.textContent = config.email;
      }
      if (config.formEndpoint) setEnabled(true);
      else $('contact-config-error').classList.remove('d-none');
    })
    .catch(function () { $('contact-config-error').classList.remove('d-none'); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!config || !config.formEndpoint) return;
    if (!form.reportValidity()) return;

    var data = {
      name: $('cf-name').value,
      email: $('cf-email').value,
      interestSlug: $('cf-interest').value,
      message: $('cf-message').value,
      company: $('company').value
    };

    // Honeypot: bots fill the hidden field; pretend success.
    if (data.company.trim()) { done(); return; }

    var select = $('cf-interest');
    var label = select.value ? select.options[select.selectedIndex].text : '';
    if (!label) { showError('Please select a topic of interest.'); return; }

    showError('');
    setEnabled(false);
    submitBtn.textContent = 'Sending…';

    fetch(config.formEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: data.name,
        email: data.email,
        interest: label,
        interestLabel: label,
        interestSlug: data.interestSlug,
        message: data.message,
        company: data.company,
        subjectPrefix: config.subjectPrefix || 'SOS Website Contact'
      })
    })
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (body) {
          if (!res.ok || !body.success) throw new Error(body.message || 'Submission failed');
        });
      })
      .then(done)
      .catch(function (err) {
        showError(err && err.message
          ? 'We could not send your message: ' + err.message
          : 'We could not send your message. Please try again or email us directly using the address below.');
        setEnabled(true);
      })
      .finally(function () { submitBtn.textContent = 'Send message'; });
  });

  function done() {
    form.reset();
    form.classList.add('d-none');
    $('contact-success').classList.remove('d-none');
  }
})();
