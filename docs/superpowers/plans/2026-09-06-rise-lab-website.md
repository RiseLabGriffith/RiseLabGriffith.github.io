# RISE Lab Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the RISE Lab GitHub Pages site as a data-driven Jekyll site with eight sections, the R/I/S/E framework as the visual motif, and non-developer maintenance through YAML/Markdown.

**Architecture:** Jekyll 4.4 with all content in `_data/*.yml` and a `_projects` collection; small `_includes` components; Sass split into partials; one dependency-free `assets/js/site.js`. Python scripts validate data and import publications; a Python test suite builds the site and asserts on rendered HTML.

**Tech Stack:** Jekyll 4.4 (Ruby via Homebrew locally, `ruby/setup-ruby` in CI), Sass, vanilla JS, Python 3.11 (PyYAML, pytest) for scripts and tests, headless Chrome for screenshots.

**Spec:** `docs/superpowers/specs/2026-09-06-rise-lab-website-design.md`

## Global Constraints

- `baseurl: ""` and `url: "https://riselabgriffith.github.io"` (org root site).
- Jekyll `~> 4.4`; plugins limited to `jekyll-seo-tag` and `jekyll-sitemap`.
- Fonts: Source Serif 4 (display), Inter (body), IBM Plex Mono (meta) from Google Fonts with fallbacks.
- Colours: paper `#faf9f6`, ink `#101828`, navy `#0b1f3a`, red `#c8102e`; layers R `#2a4d9b`, I `#0e7c5b`, S `#b8232f`, E `#a0561b`; dark theme per spec §4.
- No JS frameworks; `assets/js/site.js` is the only script; every page works without JS except filtering and copy.
- Routine content edits touch only `_data/*.yml`, `_projects/*.md`, or page Markdown.
- Work on branch `website-v2`; commit after each task; never push.
- Local commands use `export PATH="/opt/homebrew/opt/ruby/bin:$PATH"`; build with `bundle exec jekyll build`; tests with `python3 -m pytest tests -q`.
- Scratchpad with gathered source material: `/private/tmp/claude-501/-Users-liuyi-llm-research-code-RiseLabGriffith-github-io/033769d0-82ea-41a6-824f-81c74f48b42a/scratchpad` (proposal.md, photos/, experts/, pubs/, raw/*.txt).

---

## File structure

| Path | Responsibility |
|---|---|
| `_config.yml` | build settings, collections, defaults, excludes |
| `Gemfile` | jekyll 4.4 + plugins + stdlib gems |
| `.github/workflows/jekyll.yml` | build with custom Gemfile and deploy to Pages |
| `_data/site.yml` | lab identity, address, contact, social links, acknowledgement text |
| `_data/navigation.yml` | nav items |
| `_data/research.yml` | lifecycle stages, four layers, fourteen topics |
| `_data/people.yml` | all people |
| `_data/publications.yml` | publications |
| `_data/news.yml`, `_data/events.yml`, `_data/openings.yml` | news, events, openings |
| `_projects/*.md` | project pages (collection) |
| `_layouts/default.html`, `page.html`, `project.html` | shells |
| `_includes/*.html` | components listed in spec §5 plus `brand-mark.html`, `toast.html`, `icons.html` |
| `_sass/_tokens.scss`, `_base.scss`, `_layout.scss`, `_components.scss`, `_pages.scss`, `_utilities.scss` | styles |
| `assets/css/main.scss` | imports partials |
| `assets/js/site.js` | behaviours |
| `assets/img/favicon.svg`, `assets/img/people/*` | images |
| `index.md`, `about.md`, `research.md`, `people.md`, `publications.md`, `projects.md`, `news.md`, `join.md`, `404.html` | pages |
| `scripts/check_data.py` | data validator (stdlib + PyYAML) |
| `scripts/import_publications.py` | DBLP/ORCID/BibTeX → YAML entries |
| `tests/conftest.py`, `tests/test_data.py`, `tests/test_site.py` | tests |
| `README.md` | maintenance guide |

---

### Task 1: Foundation — config, workflow, layouts, header/footer, tokens, theme toggle

**Files:**
- Modify: `_config.yml`, `Gemfile`, `.gitignore`
- Create: `.github/workflows/jekyll.yml`; Delete: `.github/workflows/jekyll-gh-pages.yml`
- Create: `_data/site.yml`; Modify: `_data/navigation.yml`
- Create: `_layouts/default.html`, `_layouts/page.html`
- Create: `_includes/head.html`, `_includes/header.html`, `_includes/footer.html`, `_includes/brand-mark.html`, `_includes/toast.html`
- Create: `_sass/_tokens.scss`, `_sass/_base.scss`, `_sass/_layout.scss`, `_sass/_components.scss`, `_sass/_pages.scss`, `_sass/_utilities.scss`; Modify: `assets/css/main.scss`
- Create: `assets/js/site.js`, `assets/img/favicon.svg`, `404.html`
- Create: `tests/conftest.py`, `tests/test_site.py`

**Interfaces:**
- Produces: `site.data.site` keys `name, short_name, tagline, school, university, address_gc, address_nathan, email, github, scholar, acknowledgement`; CSS class names `container`, `section`, `eyebrow`, `button`, `button--ghost`, `tag`, `tag--R|I|S|E`, `card`; JS init hooks `data-theme-toggle`, `data-nav-toggle`, `data-toast`.
- Test fixture `built_site` (pytest fixture, session scope) that builds into `_site` once and exposes `read(path) -> str`.

- [ ] **Step 1: Write the failing site tests**

`tests/conftest.py`:
```python
import os, subprocess, pathlib, pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PATH="/opt/homebrew/opt/ruby/bin:" + os.environ["PATH"])

@pytest.fixture(scope="session")
def built_site():
    subprocess.run(["bundle", "exec", "jekyll", "build", "--quiet"], cwd=ROOT, env=ENV, check=True)
    site = ROOT / "_site"
    def read(path):
        p = site / path.lstrip("/")
        if p.is_dir(): p = p / "index.html"
        return p.read_text(encoding="utf-8")
    return read
```

`tests/test_site.py` (initial):
```python
import re
PAGES = ["/", "/research/", "/people/", "/publications/", "/projects/", "/news/", "/about/", "/join/", "/404.html"]

def test_all_pages_build(built_site):
    for p in PAGES:
        html = built_site(p)
        assert "<main" in html, p

def test_nav_links_are_root_relative(built_site):
    html = built_site("/")
    hrefs = re.findall(r'class="nav-links"[\s\S]*?</ul>', html)[0]
    assert '/RiseLabGriffith/' not in hrefs
    for target in ["/research/", "/people/", "/publications/", "/projects/", "/news/", "/about/", "/join/"]:
        assert f'href="{target}"' in hrefs, target

def test_theme_toggle_and_footer(built_site):
    html = built_site("/")
    assert 'data-theme-toggle' in html
    assert 'Acknowledgement' in html or 'acknowledge' in html.lower()
    assert 'Last updated' in html
```

- [ ] **Step 2: Run tests, expect failure** — `python3 -m pytest tests -q` fails (pages missing, old baseurl).

- [ ] **Step 3: Implement**

`_config.yml`:
```yaml
title: RISE Lab
tagline: Responsible, Intelligent and Secure Engineering
description: RISE Lab is a researcher-led cybersecurity lab at Griffith University connecting cyber defence, applied cryptography, privacy-preserving technologies and secure software engineering.
url: "https://riselabgriffith.github.io"
baseurl: ""
lang: en
timezone: Australia/Brisbane
markdown: kramdown
permalink: pretty
plugins: [jekyll-seo-tag, jekyll-sitemap]
sass: {style: compressed, sass_dir: _sass}
collections:
  projects: {output: true, permalink: /projects/:name/}
defaults:
  - scope: {path: ""}
    values: {layout: page}
  - scope: {path: "", type: projects}
    values: {layout: project}
exclude: [README.md, Gemfile, Gemfile.lock, vendor, docs, scripts, tests, .idea, "RISE Lab Proposal-v2(1).docx", "*.docx", node_modules]
```

`Gemfile` adds `gem "jekyll-seo-tag"` and `gem "jekyll-sitemap"` to the existing file. `.gitignore` adds `_site/`, `.jekyll-cache/`, `vendor/`, `.idea/`, `*.docx`, `.pytest_cache/`, `__pycache__/`.

`.github/workflows/jekyll.yml`:
```yaml
name: Build and deploy site
on:
  push: {branches: [main]}
  workflow_dispatch:
permissions: {contents: read, pages: write, id-token: write}
concurrency: {group: pages, cancel-in-progress: false}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with: {ruby-version: "3.3", bundler-cache: true}
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install pyyaml && python scripts/check_data.py
      - uses: actions/configure-pages@v5
        id: pages
      - run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env: {JEKYLL_ENV: production}
      - uses: actions/upload-pages-artifact@v3
  deploy:
    environment: {name: github-pages, url: "${{ steps.deployment.outputs.page_url }}"}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```
(`scripts/check_data.py` is created in Task 2; until then the step is present but the file is added before the first push.)

`_data/site.yml`:
```yaml
name: RISE Lab
full_name: Responsible, Intelligent and Secure Engineering Lab
tagline: Responsible · Intelligent · Secure Engineering
school: School of Information and Communication Technology
university: Griffith University
address_gc: Gold Coast campus, Parklands Drive, Southport QLD 4222, Australia
address_nathan: Nathan campus, 170 Kessels Road, Nathan QLD 4111, Australia
email: leo.zhang@griffith.edu.au
github: https://github.com/RiseLabGriffith
school_url: https://www.griffith.edu.au/griffith-sciences/school-information-communication-technology
acknowledgement: >
  Griffith University acknowledges the Traditional Custodians of the lands on which we work,
  and pays respect to Elders past and present.
```

`_layouts/default.html` structure: `<html lang data-theme bootstrap>` → `{% include head.html %}` → skip link → `{% include header.html %}` → `<main id="main">{{ content }}</main>` → `{% include footer.html %}` → `{% include toast.html %}` → `<script src="/assets/js/site.js" defer>`.

`_layouts/page.html`: `layout: default`; banner `<section class="banner"><div class="container"><p class="eyebrow">{{ page.eyebrow | default: page.title }}</p><h1>{{ page.headline | default: page.title }}</h1>{% if page.intro %}<p class="lede">{{ page.intro }}</p>{% endif %}</div></section>` then `<div class="container prose">{{ content }}</div>`.

`_includes/head.html`: charset, viewport, `{% seo %}`, theme-color, favicon link (`/assets/img/favicon.svg`), Google Fonts preconnect + stylesheet `family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap`, `main.css`, and inline bootstrap:
```html
<script>(function(){try{var t=localStorage.getItem('rise-theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>
```

`_includes/header.html`: `<header class="site-header"><div class="container nav-wrap">` brand (`{% include brand-mark.html %}` + text), `<button class="nav-toggle" data-nav-toggle aria-expanded="false" aria-controls="site-nav">`, `<ul class="nav-links" id="site-nav">` loop over `site.data.navigation` with `aria-current="page"` when `page.url == item.url` or `page.url contains item.url` for `/projects/`, theme button `<button class="theme-toggle" data-theme-toggle aria-label="Toggle colour theme">` with sun/moon SVG.

`_includes/brand-mark.html`: inline SVG 32×32: navy rounded rect, four bars (fill R/I/S/E colours) at y=7,13,19,25 (width 18, height 3, x=7).

`assets/img/favicon.svg`: same drawing as a standalone SVG.

`_includes/footer.html`: three columns (identity + address, quick links, contact/social), acknowledgement paragraph, bottom line `© {{ site.time | date: "%Y" }} RISE Lab · Griffith University · Last updated {{ site.time | date: "%-d %B %Y" }}`.

`_includes/toast.html`: `<div class="toast" data-toast role="status" aria-live="polite" hidden></div>`.

`_sass/_tokens.scss`: CSS custom properties for both themes exactly as in spec §4, including `--layer-R`, `--layer-I`, `--layer-S`, `--layer-E` and `--layer-R-soft` etc. Dark block guarded as `:root:not([data-theme="light"])` under `@media (prefers-color-scheme: dark)` and `:root[data-theme="dark"]`.

`_sass/_base.scss`: reset, fonts (`--font-display`, `--font-body`, `--font-mono`), headings, links, focus ring, skip link, `prefers-reduced-motion`.

`_sass/_layout.scss`: `.container`, `.section`, header, nav (desktop + mobile ≤ 880px), banner, footer grid.

`_sass/_components.scss`: `.button`, `.button--ghost`, `.eyebrow`, `.tag` and `.tag--R/I/S/E`, `.card`, `.rail-R/I/S/E` (left colour rail), `.toast`, `.theme-toggle`.

`_sass/_pages.scss` and `_sass/_utilities.scss`: empty scaffolds with a comment (filled in later tasks). `assets/css/main.scss` keeps the two `---` lines and `@import "tokens","base","layout","components","pages","utilities";`.

`assets/js/site.js` (initial):
```js
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // Theme toggle
  const themeBtn = $('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const root = document.documentElement;
      const current = root.getAttribute('data-theme') ||
        (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      const next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('rise-theme', next); } catch (e) {}
    });
  }

  // Mobile nav
  const navBtn = $('[data-nav-toggle]');
  if (navBtn) {
    const menu = document.getElementById(navBtn.getAttribute('aria-controls'));
    navBtn.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      navBtn.setAttribute('aria-expanded', String(open));
    });
  }

  // Toast
  const toast = $('[data-toast]');
  let toastTimer;
  window.riseToast = function (msg) {
    if (!toast) return;
    toast.textContent = msg; toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toast.hidden = true; }, 2200);
  };
})();
```

`404.html`: front matter `layout: default`, `permalink: /404.html`, `sitemap: false`; brand mark, "Page not found", links to the main sections.

Temporary stub pages so the test passes: create `about.md`, `news.md` with `layout: page`, `title`, `permalink` and one sentence (filled in later tasks). Existing `research.md`, `people.md`, `publications.md`, `projects.md`, `join.md`, `index.md` keep building.

- [ ] **Step 4: Run tests** — `python3 -m pytest tests -q` passes; `bundle exec jekyll build` shows no warnings.
- [ ] **Step 5: Commit** — `git add -A && git commit -m "feat: site foundation with theme, layouts, tokens and CI build"`.

---

### Task 2: Data validator `scripts/check_data.py`

**Files:** Create `scripts/check_data.py`, `tests/test_data.py`.

**Interfaces:**
- Produces: `validate(root: Path) -> list[str]` returning error strings (empty list = valid); CLI exits 1 on errors. Rules: people ids unique and slug-like; `role` in the allowed set; `layers` subset of R/I/S/E; publications ids unique, `year` int, `type` allowed, `members` reference people ids, `authors` non-empty; news dates ISO and sorted newest first; events dates ISO; openings `supervisors` reference people; research layer ids exactly R,I,S,E with topics having unique ids; projects front matter `layers`, `members`, `kind`, `status` valid.

- [ ] **Step 1: Write failing tests** in `tests/test_data.py`:
```python
import yaml, pathlib, textwrap
from scripts.check_data import validate
ROOT = pathlib.Path(__file__).resolve().parents[1]

def write(tmp, rel, text):
    p = tmp / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(textwrap.dedent(text)); return p

def minimal(tmp):
    write(tmp, "_data/research.yml", """
      lifecycle: [Risk and Requirements, Design and Build]
      layers:
        - {id: R, letter: R, name: R, short: R, tagline: t, keywords: [k], description: d, topics: [{id: a, name: A, summary: s, keywords: [k]}]}
        - {id: I, letter: I, name: I, short: I, tagline: t, keywords: [k], description: d, topics: [{id: b, name: B, summary: s, keywords: [k]}]}
        - {id: S, letter: S, name: S, short: S, tagline: t, keywords: [k], description: d, topics: [{id: c, name: C, summary: s, keywords: [k]}]}
        - {id: E, letter: E, name: E, short: E, tagline: t, keywords: [k], description: d, topics: [{id: d, name: D, summary: s, keywords: [k]}]}
    """)
    write(tmp, "_data/people.yml", "- {id: leo-zhang, name: Leo Zhang, role: director, position: AP, layers: [R]}\n")
    write(tmp, "_data/publications.yml", "- {id: x2026, title: T, authors: [Leo Zhang], venue: V, year: 2026, type: conference, layers: [R], members: [leo-zhang]}\n")
    write(tmp, "_data/news.yml", "- {date: 2026-09-01, kind: general, title: t, text: x}\n- {date: 2026-08-01, kind: general, title: t, text: x}\n")
    write(tmp, "_data/events.yml", "[]\n"); write(tmp, "_data/openings.yml", "[]\n")
    write(tmp, "_projects/a.md", "---\ntitle: A\nsummary: s\nkind: direction\nstatus: active\nlayers: [R]\nmembers: [leo-zhang]\n---\nbody\n")

def test_valid_data_has_no_errors(tmp_path):
    minimal(tmp_path); assert validate(tmp_path) == []

def test_unknown_member_reference_is_reported(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/publications.yml", "- {id: x2026, title: T, authors: [A], venue: V, year: 2026, type: conference, layers: [R], members: [nobody]}\n")
    assert any("nobody" in e for e in validate(tmp_path))

def test_news_must_be_newest_first(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/news.yml", "- {date: 2026-08-01, kind: general, title: t, text: x}\n- {date: 2026-09-01, kind: general, title: t, text: x}\n")
    assert any("newest first" in e for e in validate(tmp_path))

def test_bad_layer_is_reported(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/people.yml", "- {id: leo-zhang, name: Leo Zhang, role: director, position: AP, layers: [Q]}\n")
    assert any("layer" in e.lower() for e in validate(tmp_path))

def test_real_repo_data_is_valid():
    assert validate(ROOT) == []
```
Add `scripts/__init__.py` and `tests/__init__.py` (empty) so imports work.

- [ ] **Step 2: Run** — fails with ImportError.
- [ ] **Step 3: Implement `scripts/check_data.py`** with `load(path)`, per-file check functions, `validate(root)`, and `main()`; parse project front matter by splitting on `---`.
- [ ] **Step 4: Run** — all pass (the real-repo test passes once Tasks 3–7 land; until then keep the current YAML minimal and valid: temporarily create empty `events.yml`/`openings.yml` and a valid `research.yml` in this task).
- [ ] **Step 5: Commit** — `git commit -m "feat: data validator with tests"`.

---

### Task 3: Research data, framework stack, Research page

**Files:** Create `_data/research.yml`, `_includes/framework-stack.html`, `_includes/layer-tag.html`; Modify `research.md`, `_sass/_components.scss`, `_sass/_pages.scss`, `assets/js/site.js`; Modify `tests/test_site.py`.

**Interfaces:**
- `research.yml` schema from spec §3; topic ids: `robustness-safety-resilience`, `transparency-accountability`, `evaluation-verification-assurance`, `threat-intelligence-analytics`, `llm-agent-security`, `secure-software-engineering`, `privacy-preserving-data`, `secure-computation`, `cryptographic-protocols`, `verifiable-computation`, `cross-layer-demonstrators`, `engineering-toolchains`, `evaluation-red-team`, `operational-assurance`.
- `framework-stack.html` accepts `include.mode` = `compact` (home) or `full` (research). Markup: `<div class="stack" data-stack>` with one `<section class="stack__layer stack__layer--R">` per layer containing `<button class="stack__head" aria-expanded="false" aria-controls="stack-R">` and `<div class="stack__body" id="stack-R" hidden>` with keywords and topic links (`/research/#topic-id`), then `<ol class="lifecycle">` of stages.
- `layer-tag.html`: `{% include layer-tag.html letter="R" %}` → `<a class="tag tag--R" href="/research/#layer-R">R</a>`.

- [ ] **Step 1: Tests** (append to `tests/test_site.py`):
```python
def test_research_page_lists_four_layers_and_fourteen_topics(built_site):
    html = built_site("/research/")
    for L in "RISE": assert f'id="layer-{L}"' in html
    assert html.count('class="topic') == 14

def test_framework_stack_is_keyboard_accessible(built_site):
    html = built_site("/research/")
    assert html.count('class="stack__head"') == 4 and 'aria-expanded="false"' in html
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement** `research.yml` (text adapted from proposal §"RISE Framework and Research Themes": each layer description 2–3 sentences, each topic summary 2–3 sentences, keywords 4–7), the include, `research.md` (front matter `layout: page`, `headline`, `intro`; body: `{% include framework-stack.html mode="full" %}`, then for each layer a `<section class="layer-section" id="layer-R">` with heading band, description, topic grid where each `<article class="topic card rail-R" id="topic-id">` shows name, summary, keywords, and "People" chips from `site.data.people | where_exp: "p", "p.layers contains layer.id"` (academics only), plus a side `<nav class="toc" data-scrollspy>`). Stack JS: click toggles `aria-expanded` + `hidden`; ArrowUp/ArrowDown move focus between heads; only one open at a time. Scrollspy: IntersectionObserver sets `aria-current` on toc links. Styles: stack bands with layer colour left border and soft background on open; lifecycle as a horizontal rail with five nodes; toc sticky at ≥1100px.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: research data, framework stack and research page"`.

---

### Task 4: People data, photos, People page

**Files:** Create `_data/people.yml`, `_includes/person-card.html`, `assets/img/people/*.jpg`; Modify `people.md`, `_sass/_pages.scss`, `_sass/_components.scss`, `assets/js/site.js`, `tests/test_site.py`.

**Interfaces:** `person-card.html` takes `include.person`; renders `<article class="person" data-layers="R I">` with photo or `<div class="person__avatar">LZ</div>`, name link, position, `note` label, interest list, icon links. People page groups by role in order director, academic, student, visitor, joint (inside `<details>`), alumni; filter chips `<button class="chip" data-people-filter="R">`.

- [ ] **Step 1: Tests**:
```python
def test_people_page_groups_and_members(built_site):
    html = built_site("/people/")
    for name in ["Leo Zhang", "Yanjun Zhang", "Qinyi Li", "He Zhang", "Yi Liu", "Wei Song"]:
        assert name in html
    assert html.count('class="person"') >= 20
    assert 'data-people-filter="I"' in html
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement.** Copy/resize photos from scratchpad `photos/` into `assets/img/people/` as 400×400 JPEG (use `sips` on macOS: `sips -Z 400`, crop square with `sips -c`), converting webp via `sips -s format jpeg`. Fill `people.yml` with the six academics (bios from Experts/homepages, layers: Leo R,I,S; Yanjun I,S; Qinyi S; He R,I,S; Yi I,E; Wei I,E), Griffith-based PhD students from Leo's and Yi Liu's pages (Jingming Dai, Jintian Ji, Ziwen Tan, Fang Long, Shujun Wang, Haoqi Zhang, Chenhong Luo, Xiaomei Zhang, Xiaoyan Feng, Zirui Gong, Zhaoxi Zhang, Zhihao Chen, Yujiang Li, Ruoqi Guo), visitors (Taehong Kim, Shuyu Chang), joint external students (Di Mi, Yuhang Zhou, Jiaheng Wei, Lulu Xue, Yuxin Cao, Bangshuo Zhu, Haonan Zhong). Include `dblp` field for academics. Page JS: chips toggle `hidden` on `.person` by `data-layers`.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: people data, photos and people page"`.

---

### Task 5: Publications import script, data, Publications page

**Files:** Create `scripts/import_publications.py`, `tests/test_import.py`, `_data/publications.yml`, `_includes/pub-item.html`; Modify `publications.md`, `assets/js/site.js`, `_sass/_pages.scss`, `tests/test_site.py`.

**Interfaces:**
- `import_publications.py`: `parse_dblp_xml(text) -> list[dict]`, `parse_bibtex(text) -> list[dict]`, `to_entry(rec, layers, member_ids) -> dict` (fields per spec §3), `dedupe(new, existing) -> list[dict]` keyed by lowercased DOI or normalised title, `main()` with `--dblp PID | --dblp-file FILE | --bib FILE`, `--since YEAR`, `--member ID`, `--layers R,I`, prints YAML to stdout. Venue normalisation map for common venues (USENIX Security, NDSS, CCS, S&P, ICSE, FSE, ASE, ACL, ICML, NeurIPS, ICLR, CVPR, AAAI, IJCAI, KDD, WWW, TIFS, TDSC, TKDE, RAID, ACSAC, IMWUT).
- `pub-item.html` takes `include.pub`; renders `<article class="pub rail-X" data-year data-type data-layers data-members data-search="lowercased title authors venue">` with title link, authors (member names wrapped in `<strong>` by comparing against `site.data.people` names+aliases), meta line, badges, links, `<button class="pub__bib" data-bibtex>` whose `data-*` attributes carry id, title, authors (joined by " and "), venue_full or venue, year, type, doi.

- [ ] **Step 1: Tests** `tests/test_import.py`:
```python
from scripts.import_publications import parse_dblp_xml, dedupe, to_entry
XML = '''<dblpperson><r><inproceedings key="conf/uss/Liu26"><author pid="1">Yi Liu 0069</author><author pid="2">Leo Yu Zhang</author><title>Do Not Mention This.</title><year>2026</year><booktitle>USENIX Security Symposium</booktitle><ee>https://doi.org/10.1/x</ee></inproceedings></r></dblpperson>'''
def test_parse_dblp_strips_numeric_suffix_and_period():
    recs = parse_dblp_xml(XML)
    assert recs[0]["authors"] == ["Yi Liu", "Leo Yu Zhang"] and recs[0]["title"] == "Do Not Mention This"
    assert recs[0]["year"] == 2026 and recs[0]["type"] == "conference" and recs[0]["venue"] == "USENIX Security"
def test_dedupe_by_title_case_insensitive():
    a = to_entry(parse_dblp_xml(XML)[0], ["I"], ["yi-liu"]); b = dict(a, id="other", title=a["title"].upper())
    assert dedupe([b], [a]) == []
```
Site tests:
```python
def test_publications_page_has_entries_and_tools(built_site):
    html = built_site("/publications/")
    assert html.count('class="pub ') >= 60 and 'data-pub-search' in html and 'data-bibtex' in html
    assert '<strong>Leo Zhang</strong>' in html or '<strong>Leo Yu Zhang</strong>' in html
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement** script; then generate `_data/publications.yml`: run the importer against scratchpad `pubs/dblp-*.xml` (when available) with `--since 2022` per member, merge with entries transcribed from Yi Liu's and Wei Song's homepage lists (including 2026 preprints), assign `layers`/`topics` by keyword rules (jailbreak/agent/LLM → I/llm-agent-security; federated/poisoning/backdoor/adversarial → R/robustness-safety-resilience; watermark/unlearning/membership inference → R/transparency-accountability or S; MPC/HE/encryption/signature/lattice → S; fuzzing/testing/API → I/secure-software-engineering; CAPTCHA/authentication → S/cryptographic-protocols), review by hand, and mark ~18 `selected: true` (top venues 2024–2026 spanning all members). Add author aliases in `people.yml` (`Leo Yu Zhang`, `Yanjun Zhang`). Page: toolbar (search input `data-pub-search`, layer chips `data-pub-filter-layer`, type chips `data-pub-filter-type`, member `<select data-pub-filter-member>`, checkbox `data-pub-selected`), count `<span data-pub-count>`, year groups `<h2 class="year" id="y2026">`. JS: `applyPubFilters()` reads state, toggles `hidden`, hides empty year headings, updates count; `/` focuses search unless typing in a field; copy BibTeX builds `@inproceedings{id, title={}, author={}, booktitle={}, year={}}` (or `@article` with `journal`, `@misc` for preprints) and calls `riseToast('BibTeX copied')`.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: publication import script, data and publications page"`.

---

### Task 6: Projects collection and pages

**Files:** Create `_layouts/project.html`, `_includes/project-card.html`, `_projects/*.md` (8–10 files), `_projects/_template.md` (excluded via `exclude`); Modify `projects.md`, `_sass/_pages.scss`, `tests/test_site.py`.

**Interfaces:** front matter fields per spec §3. Projects: directions `secure-auditable-ai-agents`, `privacy-preserving-threat-intelligence`, `secure-collaborative-analytics`, `verifiable-provenance-supply-chain`, `continuous-assurance-red-team`, `resilient-critical-infrastructure`; funded `secure-federated-bms` (TRaCE, Lead CI Wei Song, AUD 1.3M), `trustworthy-energy-aware-gpu-network` (AUD 2.6M, theme lead CI Wei Song); software `pentestgpt` (Yi Liu, core contributor), `digital-content-protector` (Wei Song with CSIRO Data61, watermark verification).

- [ ] **Step 1: Tests**:
```python
def test_projects_index_and_detail(built_site):
    html = built_site("/projects/")
    assert html.count('class="project card') >= 8
    detail = built_site("/projects/secure-auditable-ai-agents/")
    assert "Status" in detail and 'class="tag tag--I"' in detail
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement** layout (banner, fact box `<dl class="facts">`, body, related people/publications by `members`/`layers`), card include, index grouped by `kind` with `sort: "order"`.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: projects collection, cards and detail pages"`.

---

### Task 7: News & Events data and page

**Files:** Create `_data/news.yml`, `_data/events.yml`, `_data/openings.yml`, `_includes/news-item.html`, `_includes/event-item.html`; Modify `news.md`, `_sass/_pages.scss`, `tests/test_site.py`.

**Interfaces:** schemas per spec §3. Seed `news.yml` with ≥ 12 dated items from members' news (USENIX Security 2026 ×2, ASE 2026, KDD 2026, ACL 2026, EMNLP 2026, NDSS 2026, TRaCE grant, He Zhang/Yanjun Zhang/Yi Liu/Wei Song joining, lab launch). Seed `events.yml` with a recurring "RISE seminar series" placeholder and a reading group entry with `date` in the future flagged as `tentative: true`. `openings.yml` with PhD openings for Leo Zhang (trustworthy AI, applied cryptography), Yi Liu (LLM/agent security), Wei Song (AI security for energy systems), Qinyi Li (cryptography), He Zhang (security for AI), Yanjun Zhang (trustworthy AI).

- [ ] **Step 1: Tests**:
```python
def test_news_page_timeline_and_events(built_site):
    html = built_site("/news/")
    assert html.count('class="news-item') >= 12 and 'Upcoming' in html and 'class="timeline__year"' in html
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement** timeline (`group_by_exp` on year, sticky `.timeline__year`), events split by `site.time`, kinds as mono labels.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: news timeline and events"`.

---

### Task 8: Home page

**Files:** Modify `index.md`, `_sass/_pages.scss`, `assets/js/site.js`, `tests/test_site.py`; Create `_includes/stat.html`.

- [ ] **Step 1: Tests**:
```python
def test_home_sections(built_site):
    html = built_site("/")
    for marker in ['class="hero"', 'data-stack', 'class="stats"', 'Latest news', 'Selected publications', 'Featured projects', '/join/']:
        assert marker in html, marker
    assert html.count('class="pub ') <= 6
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement** hero (`<h1 class="wordmark"><span data-letter="R">R</span>…` with `data-phrase` revealed via CSS), vision sentence from proposal, buttons; `{% include framework-stack.html mode="compact" %}`; stats via Liquid counts (`site.data.people | where: "role","academic" | size` + director, students, topics 14, layers 4) rendered with `data-count`; news top 3; `selected` pubs top 6; `featured` projects top 3; CTA band. JS counters with IntersectionObserver and reduced-motion guard.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: home page"`.

---

### Task 9: About and Join pages

**Files:** Modify `about.md`, `join.md`, `_sass/_pages.scss`, `tests/test_site.py`.

- [ ] **Step 1: Tests**:
```python
def test_about_and_join(built_site):
    about = built_site("/about/"); join = built_site("/join/")
    assert "Vision" in about and "How we work" in about and "TrustAGI" not in about
    assert "GUPRS" in join and "Open positions" in join and "mailto:" in join
```
- [ ] **Step 2: Run** — fails.
- [ ] **Step 3: Implement** About per spec §6 (four commitment cards with `rail-*`, Why RISE, How we work, Collaboration paragraph, link to research). Join per spec §6 with openings loop, scholarship list, email checklist, partnership offer, contact block with both addresses.
- [ ] **Step 4: Run tests + build.**
- [ ] **Step 5: Commit** — `git commit -m "feat: about and join pages"`.

---

### Task 10: README, polish, visual verification

**Files:** Modify `README.md`, `_sass/*`, any page; Create `docs/screenshots/` (ignored? no — keep out of repo; save to scratchpad).

- [ ] **Step 1: Rewrite README** with structure, recipes (news, publication, person, project, event, opening), local preview, import script usage, validator, deployment notes.
- [ ] **Step 2: Visual pass** — `bundle exec jekyll serve --port 4000 --detach`; headless Chrome screenshots of each page at 1280×900 and 390×844 in light and dark (`--headless=new --screenshot --window-size`); review and fix spacing, contrast, overflow.
- [ ] **Step 3: Link check** — Python script walks `_site/**/*.html`, collects internal `href`/`src`, asserts each resolves to a file in `_site` (add as `tests/test_links.py`).
- [ ] **Step 4: Run** full test suite and validator; build with `JEKYLL_ENV=production`.
- [ ] **Step 5: Commit** — `git commit -m "docs: maintenance guide; polish and link check"`.

---

## Self-review

- Spec coverage: §2 pages → Tasks 1,3,4,5,6,7,8,9; §3 data → 2–7; §4 visual → 1 + per-page tasks; §5 components → 1,3,4,5,6,7,8; §7 interactions → 1 (theme, nav, toast), 3 (stack, scrollspy), 4 (people filter), 5 (search/filter/bibtex), 8 (counters, hero letters); §8 technical → 1; §9 maintenance → 2,5,10; §11 a11y/SEO → 1 (seo-tag, sitemap, skip link) and page tasks; §12 verification → 10.
- Names used consistently: `riseToast`, `applyPubFilters`, `data-stack`, `stack__head`, `rail-R`, `tag--R`, `person`, `pub`, `project card`, `news-item`, `timeline__year`, `data-people-filter`, `data-pub-search`, `data-bibtex`, `built_site`, `validate`, `parse_dblp_xml`, `to_entry`, `dedupe`.
