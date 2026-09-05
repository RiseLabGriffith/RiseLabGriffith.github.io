# RISE Lab website

This website is hosted with GitHub Pages and powered by Jekyll.

## Content files

- `index.md` — Home
- `research.md` — Research
- `people.md` — People
- `projects.md` — Projects
- `publications.md` — Publications
- `join.md` — Join Us

Homepage news is maintained in `_data/news.yml`; add new items at the top. Shared navigation is in `_data/navigation.yml`, the page template is in `_layouts/default.html`, and styling is in `assets/css/main.scss`.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```
