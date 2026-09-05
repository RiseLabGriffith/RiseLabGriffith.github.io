/* RISE Lab site behaviours. No dependencies. Everything degrades gracefully without JS. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Theme toggle -------------------------------------------------------
  var themeBtn = $('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var root = document.documentElement;
      var current = root.getAttribute('data-theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      var next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('rise-theme', next); } catch (e) { /* storage unavailable */ }
    });
  }

  // ---- Mobile navigation --------------------------------------------------
  var navBtn = $('[data-nav-toggle]');
  if (navBtn) {
    var menu = document.getElementById(navBtn.getAttribute('aria-controls'));
    navBtn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      navBtn.setAttribute('aria-expanded', String(open));
      navBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }

  // ---- Toast --------------------------------------------------------------
  var toast = $('[data-toast]');
  var toastTimer;
  window.riseToast = function (msg) {
    if (!toast) { return; }
    toast.textContent = msg;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.hidden = true; }, 2200);
  };

  window.RISE = { $: $, $$: $$, reducedMotion: reducedMotion };
})();
