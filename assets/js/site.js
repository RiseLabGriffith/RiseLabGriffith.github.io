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

  // ---- Framework stack ----------------------------------------------------
  $$('[data-stack]').forEach(function (stack) {
    var heads = $$('.stack__head', stack);
    function setOpen(btn, open) {
      btn.setAttribute('aria-expanded', String(open));
      var layer = btn.closest('.stack__layer');
      if (layer) { layer.classList.toggle('is-open', open); }
    }
    heads.forEach(function (btn, i) {
      setOpen(btn, false);
      btn.addEventListener('click', function () {
        var wasOpen = btn.getAttribute('aria-expanded') === 'true';
        heads.forEach(function (h) { setOpen(h, false); });
        setOpen(btn, !wasOpen);
      });
      btn.addEventListener('keydown', function (e) {
        var j = null;
        if (e.key === 'ArrowDown') { j = (i + 1) % heads.length; }
        else if (e.key === 'ArrowUp') { j = (i - 1 + heads.length) % heads.length; }
        else if (e.key === 'Home') { j = 0; }
        else if (e.key === 'End') { j = heads.length - 1; }
        if (j === null) { return; }
        e.preventDefault();
        heads[j].focus();
      });
    });
  });

  // ---- Research page scrollspy -------------------------------------------
  var toc = $('[data-scrollspy]');
  if (toc && 'IntersectionObserver' in window) {
    var tocLinks = $$('a[href^="#"]', toc);
    var byId = {};
    tocLinks.forEach(function (l) { byId[l.getAttribute('href').slice(1)] = l; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) { return; }
        tocLinks.forEach(function (l) { l.removeAttribute('aria-current'); });
        var link = byId[en.target.id];
        if (link) { link.setAttribute('aria-current', 'true'); }
      });
    }, { rootMargin: '-25% 0px -60% 0px', threshold: 0 });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) { spy.observe(el); }
    });
  }

  // ---- People layer filter -----------------------------------------------
  var peopleFilters = $('[data-people-filters]');
  if (peopleFilters) {
    var pChips = $$('[data-people-filter]', peopleFilters);
    var pCount = $('[data-people-count]', peopleFilters);
    var cards = $$('.person[data-layers]');
    function applyPeopleFilter(layer) {
      var shown = 0;
      cards.forEach(function (card) {
        var ok = layer === 'all' || (' ' + card.getAttribute('data-layers') + ' ').indexOf(' ' + layer + ' ') !== -1;
        card.hidden = !ok;
        if (ok) { shown += 1; }
      });
      $$('[data-people-group]').forEach(function (group) {
        var visible = $$('.person', group).some(function (c) { return !c.hidden; });
        group.hidden = !visible;
        var fold = $('details', group);
        if (fold && layer !== 'all' && visible) { fold.open = true; }
      });
      pChips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-people-filter') === layer)); });
      if (pCount) { pCount.textContent = layer === 'all' ? '' : shown + ' of ' + cards.length + ' members'; }
    }
    pChips.forEach(function (chip) {
      chip.addEventListener('click', function () { applyPeopleFilter(chip.getAttribute('data-people-filter')); });
    });
    var initialLayer = new URLSearchParams(location.search).get('layer');
    if (initialLayer && /^[RISE]$/.test(initialLayer)) { applyPeopleFilter(initialLayer); }
  }

  window.RISE = { $: $, $$: $$, reducedMotion: reducedMotion };
})();
