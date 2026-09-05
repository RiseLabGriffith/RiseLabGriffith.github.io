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

  // ---- Publications: search, filters, shareable URL ----------------------
  var pubToolbar = $('[data-pub-toolbar]');
  if (pubToolbar) {
    pubToolbar.hidden = false;
    var pubItems = $$('.pub[data-search]');
    var pubSearch = $('[data-pub-search]');
    var layerChips = $$('[data-pub-filter-layer]');
    var typeChips = $$('[data-pub-filter-type]');
    var memberSelect = $('[data-pub-filter-member]');
    var selectedBox = $('[data-pub-selected]');
    var topicChips = $$('[data-pub-topic]');
    var pubCount = $('[data-pub-count]');
    var pubEmpty = $('[data-pub-empty]');
    var resetButtons = $$('[data-pub-reset]');
    var pubState = { q: '', layers: [], types: [], member: '', topic: '', selected: false };

    function hasToken(el, attr, token) {
      return (' ' + (el.getAttribute(attr) || '') + ' ').indexOf(' ' + token + ' ') !== -1;
    }
    function pubMatches(el) {
      if (pubState.q && el.getAttribute('data-search').indexOf(pubState.q) === -1) { return false; }
      if (pubState.layers.length && !pubState.layers.some(function (L) { return hasToken(el, 'data-layers', L); })) { return false; }
      if (pubState.types.length && pubState.types.indexOf(el.getAttribute('data-type')) === -1) { return false; }
      if (pubState.member && !hasToken(el, 'data-members', pubState.member)) { return false; }
      if (pubState.topic && !hasToken(el, 'data-topics', pubState.topic)) { return false; }
      if (pubState.selected && el.getAttribute('data-selected') !== 'true') { return false; }
      return true;
    }
    function applyPubFilters() {
      var shown = 0;
      pubItems.forEach(function (el) {
        var ok = pubMatches(el);
        el.hidden = !ok;
        if (ok) { shown += 1; }
      });
      $$('[data-pub-year]').forEach(function (section) {
        var items = $$('.pub', section);
        var visible = items.filter(function (el) { return !el.hidden; }).length;
        section.hidden = visible === 0;
        var count = $('[data-year-count]', section);
        if (count) { count.textContent = visible === items.length ? String(items.length) : visible + ' of ' + items.length; }
      });
      var active = !!(pubState.q || pubState.layers.length || pubState.types.length || pubState.member || pubState.topic || pubState.selected);
      if (pubCount) { pubCount.textContent = (active ? shown + ' of ' + pubItems.length : pubItems.length) + ' publications'; }
      if (pubEmpty) { pubEmpty.hidden = shown !== 0; }
      resetButtons.forEach(function (b) { b.hidden = !active; });
      layerChips.forEach(function (c) { c.setAttribute('aria-pressed', String(pubState.layers.indexOf(c.getAttribute('data-pub-filter-layer')) !== -1)); });
      typeChips.forEach(function (c) { c.setAttribute('aria-pressed', String(pubState.types.indexOf(c.getAttribute('data-pub-filter-type')) !== -1)); });
      topicChips.forEach(function (c) { c.hidden = c.getAttribute('data-pub-topic') !== pubState.topic; });
      var params = new URLSearchParams();
      if (pubState.q) { params.set('q', pubState.q); }
      if (pubState.layers.length) { params.set('layer', pubState.layers.join(',')); }
      if (pubState.types.length) { params.set('type', pubState.types.join(',')); }
      if (pubState.member) { params.set('member', pubState.member); }
      if (pubState.topic) { params.set('topic', pubState.topic); }
      if (pubState.selected) { params.set('selected', '1'); }
      var qs = params.toString();
      if (window.history && history.replaceState) {
        history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + location.hash);
      }
    }
    function toggleIn(list, value) {
      var i = list.indexOf(value);
      if (i === -1) { list.push(value); } else { list.splice(i, 1); }
    }
    if (pubSearch) {
      pubSearch.addEventListener('input', function () { pubState.q = pubSearch.value.trim().toLowerCase(); applyPubFilters(); });
      pubSearch.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { pubSearch.value = ''; pubState.q = ''; applyPubFilters(); }
      });
      document.addEventListener('keydown', function (e) {
        var t = e.target;
        var typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable);
        if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey) { e.preventDefault(); pubSearch.focus(); pubSearch.select(); }
      });
    }
    layerChips.forEach(function (c) { c.addEventListener('click', function () { toggleIn(pubState.layers, c.getAttribute('data-pub-filter-layer')); applyPubFilters(); }); });
    typeChips.forEach(function (c) { c.addEventListener('click', function () { toggleIn(pubState.types, c.getAttribute('data-pub-filter-type')); applyPubFilters(); }); });
    if (memberSelect) { memberSelect.addEventListener('change', function () { pubState.member = memberSelect.value; applyPubFilters(); }); }
    if (selectedBox) { selectedBox.addEventListener('change', function () { pubState.selected = selectedBox.checked; applyPubFilters(); }); }
    topicChips.forEach(function (c) { c.addEventListener('click', function () { pubState.topic = ''; applyPubFilters(); }); });
    resetButtons.forEach(function (b) {
      b.addEventListener('click', function () {
        pubState = { q: '', layers: [], types: [], member: '', topic: '', selected: false };
        if (pubSearch) { pubSearch.value = ''; }
        if (memberSelect) { memberSelect.value = ''; }
        if (selectedBox) { selectedBox.checked = false; }
        applyPubFilters();
      });
    });

    // Initial state from the URL, so Research and People pages can deep-link into filtered lists.
    var initial = new URLSearchParams(location.search);
    pubState.q = (initial.get('q') || '').trim().toLowerCase();
    pubState.layers = (initial.get('layer') || '').split(',').filter(function (L) { return /^[RISE]$/.test(L); });
    pubState.types = (initial.get('type') || '').split(',').filter(Boolean);
    pubState.member = initial.get('member') || '';
    pubState.topic = initial.get('topic') || '';
    pubState.selected = initial.get('selected') === '1';
    if (pubSearch) { pubSearch.value = initial.get('q') || ''; }
    if (memberSelect && pubState.member) {
      memberSelect.value = pubState.member;
      if (memberSelect.value !== pubState.member) { pubState.member = ''; }
    }
    if (selectedBox) { selectedBox.checked = pubState.selected; }
    applyPubFilters();
    window.applyPubFilters = applyPubFilters;
  }

  // ---- Copy BibTeX (publications page and home) ---------------------------
  function bibtexFor(btn) {
    var d = btn.dataset;
    var kind = { journal: 'article', preprint: 'misc', thesis: 'phdthesis' }[d.type] || 'inproceedings';
    var venueKey = { article: 'journal', misc: 'howpublished', phdthesis: 'school' }[kind] || 'booktitle';
    var fields = [['title', '{' + d.title + '}'], ['author', d.authors]];
    if (d.venue) { fields.push([venueKey, d.venue]); }
    fields.push(['year', d.year]);
    if (d.doi) { fields.push(['doi', d.doi]); }
    if (d.url && !d.doi) { fields.push(['url', d.url]); }
    return '@' + kind + '{' + d.id + ',\n' + fields.map(function (f) { return '  ' + f[0] + ' = {' + f[1] + '}'; }).join(',\n') + '\n}\n';
  }
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-1000px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  function copyText(text, done) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(fallbackCopy(text)); });
    } else {
      done(fallbackCopy(text));
    }
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest ? e.target.closest('[data-bibtex]') : null;
    if (!btn) { return; }
    copyText(bibtexFor(btn), function (ok) {
      window.riseToast(ok ? 'BibTeX copied to clipboard' : 'Could not copy automatically');
    });
  });

  window.RISE = { $: $, $$: $$, reducedMotion: reducedMotion };
})();
