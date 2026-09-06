# RISE Lab Website — Design Spec

Date: 2026-09-06
Status: approved in chat (tech option A, all eight sections, light design with dark mode, self-sourced assets, softened positioning text)
Repo: `RiseLabGriffith/RiseLabGriffith.github.io` (GitHub Pages, Jekyll)

## 1. Goals

Build the public website of the RISE (Responsible, Intelligent and Secure Engineering) Lab, School of ICT, Griffith University, from the lab proposal (`RISE Lab Proposal-v2(1).docx`).

- Read like an established academic lab site: research, people, publications, projects, news, opportunities.
- Carry one distinctive identity: the four-layer R/I/S/E lifecycle framework is the visual motif and the index that links every content type.
- Be maintainable by non-developers: routine updates are YAML or Markdown edits, never HTML.
- Elegant with a technical edge: serif display type, generous whitespace, restrained motion, a mono accent for metadata.

Non-goals: CMS, member login, blog engine, bilingual content, per-person profile pages (members have their own homepages).

## 2. Information architecture

| URL | Page | Purpose |
|---|---|---|
| `/` | Home | Vision line, interactive framework stack, latest news, selected publications, featured projects, stats strip, join CTA |
| `/about/` | About | Vision and four commitments, why RISE matters, how we work, collaboration across the School (softened positioning) |
| `/research/` | Research | Framework figure + lifecycle bar, four layers, 14 topics, each topic lists related members, publications and projects |
| `/people/` | People | Director, academic members, PhD students, visitors, jointly supervised (collapsed), alumni (empty until needed) |
| `/publications/` | Publications | Year-grouped list, filter by layer/type/member, search, copy BibTeX |
| `/projects/` + `/projects/<slug>/` | Projects | Research directions and demonstrators; funded projects; software and artefacts |
| `/news/` | News & Events | Timeline of news; upcoming and past seminars/reading groups/workshops |
| `/join/` | Join Us | HDR, postdoc, visiting, honours/masters, industry partnership, contact |
| `/404.html` | Not found | Branded 404 |

Navigation order: Research · People · Publications · Projects · News · About · Join Us. The brand mark links home.

Footer: affiliation line, address, contact email, external links (GitHub, Google Scholar of director), Acknowledgement of Country, "Last updated" build date, copyright.

## 3. Content model (`_data/` and collections)

All lists live in YAML. Members are the join key for everything else.

### `_data/people.yml`

```yaml
- id: leo-zhang            # stable slug; used by publications/projects/openings
  name: Leo Zhang
  aliases: [Leo Yu Zhang]  # extra spellings used to bold names in author lists
  title: A/Prof
  role: director           # director | academic | student | visitor | joint | alumni
  position: Associate Professor · Lab Director
  photo: leo-zhang.jpg     # in assets/img/people/; omit for initials avatar
  email: leo.zhang@griffith.edu.au
  links: {homepage: ..., scholar: ..., griffith: ..., orcid: ..., github: ..., linkedin: ...}
  interests: [Trustworthy AI, Applied cryptography, ...]
  layers: [R, I, S]        # which framework layers this person mainly contributes to
  bio: >                   # 2–4 sentences
  note: Incoming 2026      # optional small label
  supervisor: leo-zhang    # students only; id of primary supervisor
  affiliation: HUST        # joint/visitor only
  since: 2024              # students/visitors: start year
```

### `_data/research.yml`

```yaml
- id: R
  letter: R
  name: Responsible and Resilient Cybersecurity
  short: Responsible & Resilient
  tagline: Define responsibilities, manage cyber risks, and support prevention, recovery and adaptation
  keywords: [Governance, Risk Controls, Resilience, Accountability]
  description: >
  topics:
    - id: robustness-safety-resilience
      name: Robustness, Safety and Resilience
      summary: >
      keywords: [...]
```

Plus a `lifecycle` list (Risk and Requirements → Design and Build → Evaluate and Red Team → Deploy and Operate → Monitor and Improve) at the top of the same file.

### `_data/publications.yml`

```yaml
- id: liu2026malicious     # citation key; unique
  title: "..."
  authors: [Yi Liu, Zhihao Chen, ...]   # plain strings, in order
  venue: USENIX Security   # short display name
  venue_full: 35th USENIX Security Symposium   # optional, used in BibTeX
  year: 2026
  type: conference         # conference | journal | preprint | workshop | thesis
  layers: [I]
  topics: [llm-agent-security]   # optional research topic ids
  members: [yi-liu, yanjun-zhang, leo-zhang]   # optional; derived from authors when omitted
  selected: true           # shows on home page and at the top of the list
  badge: CORE A*           # optional
  links: {pdf: ..., doi: ..., arxiv: ..., code: ..., slides: ...}
```

BibTeX is generated in the browser from these fields; no BibTeX text is stored.

### `_projects/<slug>.md` (collection, `output: true`)

Front matter: `title`, `summary`, `kind` (direction | funded | software), `status` (active | proposed | completed), `layers`, `members`, `funder`, `years`, `partners`, `links`, `featured`, `order`. Body is Markdown.

### `_data/news.yml`, `_data/events.yml`, `_data/openings.yml`

```yaml
# news.yml — newest first
- date: 2026-09-01
  kind: paper              # paper | award | grant | people | event | media | general
  title: ...
  text: ...
  link: ...                # optional
  members: [yi-liu]        # optional

# events.yml — any order; page splits into upcoming/past by date
- date: 2026-10-15
  time: "15:00–16:00 AEST"
  kind: seminar            # seminar | reading-group | workshop | visit
  title: ...
  speaker: ...
  affiliation: ...
  location: ...
  abstract: ...
  link: ...

# openings.yml
- title: PhD scholarships in LLM and agent security
  kind: phd                # phd | postdoc | visiting | honours | intern
  supervisors: [yi-liu, leo-zhang]
  layers: [I, E]
  summary: ...
  link: ...
  open: true
```

### `_data/navigation.yml`, `_data/site.yml`

Navigation unchanged in shape. `site.yml` holds the lab address, contact email, social links and the Acknowledgement of Country text so that `_config.yml` stays about build settings.

## 4. Visual system

### Tokens (`_sass/_tokens.scss`)

Light theme (default):

- Paper `#faf9f6` (page), Surface `#ffffff`, Cloud `#eff1f4` (subtle panels)
- Ink `#101828` (text), Muted `#5b6472`, Line `#e3e6ea`
- Navy `#0b1f3a` (header/footer, display headings on dark)
- Red `#c8102e` (primary accent, links on hover, buttons). Griffith's brand red is close to this; the Experts portal uses `#c02424`.
- Layer colours: R `#2a4d9b` · I `#0e7c5b` · S `#b8232f` · E `#a0561b`. Each has a `-soft` tint for backgrounds.

Dark theme (`prefers-color-scheme: dark` unless `data-theme="light"`; `data-theme="dark"` forces): Paper `#0e141c`, Surface `#141c26`, Cloud `#1a2431`, Ink `#e8ecf1`, Muted `#98a2b3`, Line `#26303d`, Red `#ff5c6c`, layer colours lifted ~20% in lightness.

### Typography

- Display and headings: `"Source Serif 4"`, fallback Georgia/serif. Weights 500/600. Tight letter-spacing on h1.
- Body/UI: `Inter`, fallback system sans. 16px base, line-height 1.65.
- Meta/labels/tags: `"IBM Plex Mono"`, uppercase 11–12px with 0.12em tracking.
- Loaded from Google Fonts with `display=swap`; the page must remain readable with fallbacks.

### Layout

- Container max 1160px, 24px gutters; 12-column grid where needed.
- Section rhythm: 96px desktop / 64px mobile between major sections.
- Cards: 1px line border, 8px radius, no heavy shadows; hover lifts by 2px and darkens border.
- Layer colour rail: a 3px left border in the layer colour on topic cards, publication rows and project cards.

### Brand mark

SVG monogram: a rounded square in navy holding four horizontal bars (R/I/S/E colours, top to bottom) beside the letters "RISE" in the serif face. Used in the header, favicon (`assets/img/favicon.svg`) and Open Graph image (`assets/img/og.png`, generated once).

## 5. Components (`_includes/`)

| Include | Renders |
|---|---|
| `head.html` | meta, fonts, css, theme bootstrap script (prevents flash), OG tags via `jekyll-seo-tag` |
| `header.html` | brand, nav, theme toggle, mobile menu |
| `footer.html` | affiliation, address, links, acknowledgement, last updated |
| `framework-stack.html` | interactive four-layer stack + lifecycle bar (used on Home and Research) |
| `layer-tag.html` | small coloured tag for a layer letter |
| `person-card.html` | photo/initials, name, position, interests, links |
| `pub-item.html` | one publication row with year, title, authors (members bolded), venue, badges, links, copy-bibtex button |
| `project-card.html` | project summary card |
| `news-item.html` | timeline entry |
| `event-item.html` | seminar entry |
| `stat.html` | one number in the stats strip |

Layouts: `default.html` (everything), `page.html` (banner + content), `project.html` (project detail).

## 6. Page specs

### Home

1. Hero: eyebrow "Responsible · Intelligent · Secure Engineering", large serif "RISE Lab" wordmark where each letter is a hover target that reveals its layer phrase; one-sentence vision; two buttons (Research, Join Us). Background: subtle dotted grid plus one thin animated lifecycle line (CSS only; disabled under reduced motion).
2. Framework stack (`framework-stack.html`): four stacked bands; hover/focus/click expands a band to show its keywords and topic links; lifecycle bar beneath.
3. Stats strip: academic members, PhD students, research topics, layers. Numbers are computed from data files at build time; counters animate on first view.
4. Latest news: three most recent from `news.yml` with a link to `/news/`.
5. Selected publications: entries with `selected: true`, newest first, capped at six.
6. Featured projects: `featured: true` project cards, capped at three.
7. Join CTA band.

### About

Sections: Vision (four commitments as four cards with layer colours), Why RISE matters (three short paragraphs), How we work (researcher-led, voluntary, inclusive, members keep their identities), Collaboration across the School (one paragraph replacing the comparison table: RISE studies AI from a cybersecurity perspective and works with AI-centred and health-centred initiatives), Framework figure link.

### Research

Intro + framework stack; then one section per layer with a coloured heading band, layer description, and topic cards. Each topic card shows summary, keywords, and auto-lists members whose `layers` include the layer, publications tagged with the topic (max 5, link to filtered publications), and projects tagged with the layer. A sticky side TOC on wide screens highlights the current layer via IntersectionObserver.

### People

Groups by `role`: Director, Academic Members, PhD Students, Visiting Researchers, Jointly Supervised at Partner Institutions (collapsed `<details>`), Alumni. A layer filter row at the top hides cards whose `layers` do not include the chosen layer. Cards show initials when no photo exists. Names link to homepage or Griffith profile.

### Publications

Toolbar: search box (title/author/venue), layer chips, type chips, member select, "selected only" toggle. Press `/` to focus search. Entries grouped by year with sticky year headers. Member names bolded via `people.yml` names and aliases. Each entry: title (links to best available link), authors, venue and year in mono, badges, link buttons, "BibTeX" button that copies a generated entry and shows a toast. Count of visible entries updates live. No JS: full list still renders.

### Projects

Three groups by `kind`: Research directions and demonstrators, Funded projects, Software and artefacts. Cards link to detail pages that render the Markdown body plus a fact box (status, layers, members, funder, years, partners, links).

### News & Events

Left/main: news timeline with year markers that stick while scrolling; kind shown as a mono label; optional link. Right/aside on wide screens: Upcoming events, then Past events (collapsed). Both derive from `events.yml` and the build date.

### Join Us

Sections: Open positions (from `openings.yml`; hidden when none), PhD and MPhil (how to apply, scholarship names: GUPRS, GUIPRS, CSC–Griffith, AUHEPS, Industry PhD; what to include in an email), Postdocs and research fellows, Visiting researchers and students, Honours/Masters/Capstone projects, Industry and government partnership (what RISE offers), Contact (address, email, map link).

### 404

Brand mark, "Page not found", links to main sections.

## 7. Interaction details

- Theme toggle in header; stored in `localStorage`; bootstrap script in `<head>` applies it before paint.
- Framework stack: `<button aria-expanded>` per layer; arrow keys move between layers; expanded band reveals keyword list and topic links; no band is pre-expanded on load.
- Hero letters: pure CSS `:hover`/`:focus-within` reveal of the phrase beneath the wordmark.
- Stats counters: IntersectionObserver + requestAnimationFrame; skipped when `prefers-reduced-motion`.
- Publications filter/search: single vanilla function that reads chip state, applies `hidden`, updates count; `/` focuses search; copy uses `navigator.clipboard` with a fallback.
- People layer filter: same pattern as publications.
- Research TOC scrollspy: IntersectionObserver on layer sections.
- Toast: one shared element.
- All JavaScript in `assets/js/site.js`, ES2018, no dependencies, under ~300 lines. Everything works without JS except filtering and copy.

## 8. Technical

- Jekyll 4.4 via a custom Gemfile; plugins: `jekyll-seo-tag`, `jekyll-sitemap`. Local build with Homebrew Ruby: `bundle install --path vendor/bundle` then `bundle exec jekyll serve`.
- GitHub Actions: replace `actions/jekyll-build-pages` with `ruby/setup-ruby` (Ruby 3.3, bundler cache) + `bundle exec jekyll build` + `upload-pages-artifact` + `deploy-pages`. This keeps local and CI builds identical and allows plugins.
- `_config.yml`: `baseurl: ""` (org root site), `url: https://riselabgriffith.github.io`, collections `projects`, defaults per collection, `exclude` list including docs, scripts, vendor, the proposal docx, `.idea`.
- Sass: `assets/css/main.scss` imports `_sass/_tokens.scss`, `_base.scss`, `_layout.scss`, `_components.scss`, `_pages.scss`, `_utilities.scss`. Compressed output.
- Images: member photos in `assets/img/people/` (square, 600px max, jpg/webp); project images optional.
- Build date via `site.time`; last-updated in footer.
- No analytics by default; a commented block in `head.html` shows where to add it.

## 9. Maintenance

- `README.md` rewritten with "How to add a news item / publication / person / project / event / opening" recipes, local preview instructions, and the data schema.
- `scripts/import_publications.py`: imports from DBLP (author facet), ORCID (public API), or a BibTeX file into publication YAML entries; dedupes by DOI/title against the existing file; prints the new entries for review. Stdlib only.
- `scripts/check_data.py`: validates required fields, unique ids, member references, layer letters and date formats; run locally and in CI before build.
- Templates: `_projects/_template.md` (excluded from build) and commented example entries at the top of each YAML file.

## 10. Content sourcing

- Text for Vision, Why RISE, layers and topics: adapted from the proposal, tightened for the web.
- Member bios, photos, emails, links: from members' own homepages and Griffith Experts profiles. Wei Song's family name is Song (confirmed on his site). Yi Liu and Wei Song are labelled "Incoming 2026" until they confirm start.
- PhD students and visitors: from Leo Zhang's and Yi Liu's team pages, Griffith-based first; external joint supervisions collapsed.
- Publications: seeded from members' own lists (Yi Liu, Wei Song, He Zhang), DBLP (Leo Zhang, Qinyi Li) and ORCID (Yanjun Zhang, Leo Zhang, He Zhang); filtered to 2022 onward plus older landmark papers; `selected` marked by venue tier and relevance to RISE themes. Members review after launch.
- Contact: School of ICT, Griffith University, Gold Coast campus (Parklands Drive, Southport QLD 4222) and Nathan campus (170 Kessels Road, Nathan QLD 4111); building numbers omitted; director email as the lab contact until a lab mailbox exists.
- Publication sources by member: DBLP author records (Leo Yu Zhang 117/3526, Yanjun Zhang 0002 24/6547-2, Qinyi Li 117/8987, He Zhang 0012 24/2058-12, Yi Liu 0069 97/4626-69, Wei Song 0005 62/1539-5) merged with the members' own homepage lists; DBLP ids are recorded in `people.yml` so the import script can refresh.
- Not published: resourcing model details and the initiative comparison table.

## 11. Accessibility, performance, SEO

- Semantic landmarks, skip link, visible focus rings, colour contrast AA in both themes, `aria-expanded`/`aria-controls` on toggles, reduced-motion respected.
- No external JS; fonts are the only third-party request. Target Lighthouse performance ≥ 95 on Home.
- `jekyll-seo-tag` for titles/OG/Twitter cards; `jekyll-sitemap`; canonical URLs; descriptive alt text.

## 12. Verification

- `bundle exec jekyll build` succeeds with no warnings.
- `scripts/check_data.py` passes.
- Every page rendered headless in Chrome at 1280px and 390px and screenshot-reviewed; keyboard walk-through of framework stack, theme toggle, filters and copy.
- Internal links checked against `_site`.
