# RISE Lab website

Source for [riselabgriffith.github.io](https://riselabgriffith.github.io), the website of the Responsible, Intelligent and Secure Engineering (RISE) Lab in the School of ICT at Griffith University. The site is a static [Jekyll](https://jekyllrb.com) site built and deployed by GitHub Actions. All content lives in plain YAML and Markdown files, so routine updates need no knowledge of HTML or CSS.

## Where things live

| Path | What it holds |
|---|---|
| `_data/site.yml` | Lab name, addresses, contact email, links, Acknowledgement of Country |
| `_data/navigation.yml` | Header navigation |
| `_data/research.yml` | The RISE framework: lifecycle stages, four layers, fourteen topics |
| `_data/people.yml` | Every member: director, academics, students, visitors, joint supervisions, alumni |
| `_data/publications.yml` | Publications (2022 onward), with layers, topics and member links |
| `_data/news.yml` | News timeline, newest first |
| `_data/events.yml` | Seminars, reading groups and workshops (upcoming and past are split automatically) |
| `_data/openings.yml` | Open positions shown on Join Us |
| `_projects/*.md` | One file per project; the file name becomes the URL |
| `assets/img/people/` | Member photos (square JPEG, 400×400) |
| `index.md`, `about.md`, `research.md`, `people.md`, `publications.md`, `projects.md`, `news.md`, `join.md` | Page shells; most text on Research, People, Publications, Projects and News comes from the data files |
| `_layouts/`, `_includes/`, `_sass/`, `assets/js/site.js` | Templates, components, styles and the single script (developers only) |
| `scripts/check_data.py` | Data validator, run locally and in CI |
| `scripts/import_publications.py` | Imports publications from DBLP or BibTeX into YAML |
| `tests/` | Build and browser tests |

Every data file starts with a comment describing its fields. Member `id`s in `people.yml` are the join key used by publications, projects, news and openings, so keep them stable.

## Everyday updates

Edit the file on GitHub (pencil icon) or clone the repository. Commits to `main` are validated and deployed automatically; the site updates within a few minutes.

### Add a news item

Add an entry at the **top** of `_data/news.yml` (newest first; the validator enforces the order):

```yaml
- date: 2026-10-03
  kind: paper            # paper | award | grant | people | event | media | general
  title: Paper accepted at NDSS 2027
  text: One or two sentences. Member names are linked automatically via the members list.
  link: https://example.org   # optional; internal links such as /projects/pentestgpt/ also work
  members: [yi-liu]           # optional people ids
  precision: month            # optional: "month" or "year" when the exact day is not meaningful
```

The three newest items appear on the home page.

### Add a publication

Either paste an entry into `_data/publications.yml` (the file header lists every field), or let the import script draft it:

```bash
# From DBLP, by author PID (PIDs for each academic are recorded in people.yml under `dblp`)
python3 scripts/import_publications.py --dblp 97/4626-69 --since 2026 --member yi-liu --guess

# From a saved DBLP export or the DBLP search API JSON
python3 scripts/import_publications.py --dblp-file author.xml --member leo-zhang --layers R,I

# From a BibTeX file
python3 scripts/import_publications.py --bib new.bib --member wei-song --layers I,E --topics llm-agent-security
```

The script prints YAML for entries not already in the data file (matched by DOI or title), with `--guess` suggesting layers and topics from the title. Review the output, adjust `layers`, `topics`, `selected` and `members`, and paste it into the file. Mark `selected: true` on papers that should appear on the home page and at the top of their year. Author names that match a member's `name` or `aliases` are shown in bold.

### Add or update a person

Add an entry to `_data/people.yml` under the right group. Required fields are `id`, `name`, `role` (`director | academic | student | visitor | joint | alumni`), `position` and `layers`. Optional fields include `title`, `photo`, `email`, `links`, `interests`, `bio`, `note`, `supervisors`, `affiliation`, `since`, `aliases` and `dblp`. Put the photo in `assets/img/people/` as a square JPEG; on macOS:

```bash
sips -s format jpeg -Z 400 photo.png --out assets/img/people/first-last.jpg
```

Move people to `role: alumni` rather than deleting them so that their publications keep linking.

### Add a project

Copy `_projects/_template.md` to `_projects/my-project.md` and edit the front matter (`title`, `summary`, `kind`, `status`, `layers`, `members`, optional `funder`, `funding`, `years`, `partners`, `links`, `topics`, `featured`, `order`) and the Markdown body. The page appears at `/projects/my-project/` and in the matching group on the Projects page. Set `featured: true` to show it on the home page (the first three by `order`).

### Add an event or an opening

Append to `_data/events.yml` (any order; the page sorts and splits upcoming from past by the build date) or `_data/openings.yml` (set `open: false` when a position is filled). Field lists are in each file's header.

### Change page text

The banner of each page comes from its front matter (`headline`, `intro`). About and Join Us are ordinary Markdown with a little HTML for cards. The framework and topic descriptions are in `_data/research.yml`.

## Checking your changes

The validator catches most mistakes (unknown member ids, bad dates, wrong layer letters, unsorted news):

```bash
pip install pyyaml
python3 scripts/check_data.py
```

It runs in CI on every push, and a failing check stops deployment.

## Local preview

Requires Ruby 3.2+ and Bundler (`brew install ruby` on macOS, then add `/opt/homebrew/opt/ruby/bin` to your `PATH`).

```bash
bundle install
bundle exec jekyll serve --livereload
```

Open <http://localhost:4000>. The site builds into `_site/`, which is ignored by git.

## Tests

```bash
pip install pyyaml pytest
python3 -m pytest tests -q
```

`tests/test_data.py` checks the validator, `tests/test_import.py` the import script, `tests/test_site.py` the rendered HTML of every page and `tests/test_links.py` that every internal link and anchor resolves. Browser tests in `tests/test_e2e.py` cover the theme toggle, mobile navigation, framework stack keyboard support, filters, search, BibTeX copy and counters; they run when Playwright is installed (`pip install playwright && python -m playwright install chromium`) and are skipped otherwise.

## Deployment

`.github/workflows/jekyll.yml` runs on every push to `main`: it validates the data, builds the site with `JEKYLL_ENV=production` and deploys it to GitHub Pages. The repository's Pages setting must be **GitHub Actions** (not "Deploy from a branch"). Site-wide settings such as the title, description and URL are in `_config.yml`; the site is served from the organisation root, so `baseurl` stays empty.

## Design notes

The R/I/S/E layers carry fixed colours (blue, green, red, amber) used for tags, card rails and the framework stack; they are defined once in `_sass/_tokens.scss` together with the light and dark themes. Fonts are Source Serif 4, Inter and IBM Plex Mono from Google Fonts with system fallbacks. Every page works without JavaScript; the script only adds the theme toggle, mobile menu, framework stack folding, filters, search, BibTeX copy and counters. The design specification and implementation plan are in `docs/superpowers/`.
