"""Search and social metadata: preview image, descriptions, structured data, sitemap and indexing hints."""
import html
import json
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE_URL = "https://riselabgriffith.github.io"
PAGES = ["/", "/research/", "/people/", "/publications/", "/projects/", "/news/", "/about/", "/join/"]
PROJECTS = sorted(p.stem for p in (ROOT / "_projects").glob("*.md") if not p.name.startswith("_"))
ACADEMICS = ["leo-zhang", "yanjun-zhang", "qinyi-li", "he-zhang", "yi-liu", "wei-song"]


def _front_matter(path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])


def _meta(html_text, attr, name):
    m = re.search(rf'<meta [^>]*?{attr}="{re.escape(name)}"[^>]*content="([^"]*)"', html_text)
    return html.unescape(m.group(1)) if m else None


def _json_ld(html_text):
    blocks = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html_text)
    return [json.loads(b) for b in blocks]


def _all_paths():
    return PAGES + [f"/projects/{slug}/" for slug in PROJECTS]


# ---- Social preview image ---------------------------------------------------------------
def test_social_images_exist_with_expected_dimensions():
    from PIL import Image

    with Image.open(ROOT / "assets/img/og-image.png") as im:
        assert im.size == (1200, 630)
    with Image.open(ROOT / "assets/img/logo.png") as im:
        assert im.size == (512, 512)


def test_every_page_advertises_the_preview_image(built_site):
    for path in _all_paths():
        page = built_site(path)
        assert _meta(page, "property", "og:image") == f"{SITE_URL}/assets/img/og-image.png", path
        assert _meta(page, "property", "og:image:width") == "1200", path
        assert _meta(page, "property", "og:image:height") == "630", path
        assert _meta(page, "property", "og:image:alt"), path
        assert _meta(page, "name", "twitter:card") == "summary_large_image", path


# ---- Descriptions -----------------------------------------------------------------------
def test_page_descriptions_are_unique_and_fit_a_search_snippet():
    # Source-level check: page descriptions are the meta description and should fit Google's ~160 char cut-off.
    seen = {}
    for name in ["index.md", "about.md", "research.md", "people.md", "publications.md", "projects.md", "news.md", "join.md"]:
        desc = _front_matter(ROOT / name)["description"]
        assert 50 <= len(desc) <= 160, (name, len(desc))
        assert desc not in seen, (name, seen.get(desc))
        seen[desc] = name


def test_project_meta_description_is_the_curated_summary(built_site):
    for slug in PROJECTS:
        summary = _front_matter(ROOT / "_projects" / f"{slug}.md")["summary"].strip()
        page = built_site(f"/projects/{slug}/")
        assert _meta(page, "name", "description") == summary, slug
        assert _meta(page, "property", "og:description") == summary, slug


# ---- Structured data --------------------------------------------------------------------
def test_all_structured_data_blocks_are_valid_json(built_site):
    for path in _all_paths():
        blocks = _json_ld(built_site(path))
        assert blocks, path
        for block in blocks:
            assert block.get("@context") == "https://schema.org", path


def test_home_describes_the_lab_as_a_research_organisation(built_site):
    org = next(b for b in _json_ld(built_site("/")) if b.get("@type") == "ResearchOrganization")
    site_data = yaml.safe_load((ROOT / "_data/site.yml").read_text(encoding="utf-8"))
    assert org["name"] == "RISE Lab"
    assert org["alternateName"] == site_data["full_name"]
    assert org["url"] == f"{SITE_URL}/"
    assert org["logo"] == f"{SITE_URL}/assets/img/logo.png"
    assert org["email"] == site_data["email"]
    assert org["parentOrganization"]["name"] == site_data["school"]
    assert org["parentOrganization"]["parentOrganization"]["name"] == "Griffith University"
    assert org["address"]["@type"] == "PostalAddress"
    assert org["address"]["addressLocality"] == "Southport"
    assert org["address"]["addressCountry"] == "AU"
    assert site_data["github"] in org["sameAs"]
    assert sorted(m["name"] for m in org["member"]) == sorted(
        p["name"] for p in yaml.safe_load((ROOT / "_data/people.yml").read_text(encoding="utf-8")) if p["id"] in ACADEMICS
    )


def test_people_page_describes_each_academic_as_a_person(built_site):
    people = {p["id"]: p for p in yaml.safe_load((ROOT / "_data/people.yml").read_text(encoding="utf-8"))}
    persons = [b for b in _json_ld(built_site("/people/")) if b.get("@type") == "Person"]
    by_name = {p["name"]: p for p in persons}
    for pid in ACADEMICS:
        src = people[pid]
        person = by_name[src["name"]]
        assert person["url"] == f"{SITE_URL}/people/#{pid}", pid
        assert person["jobTitle"] == src["position"], pid
        assert person["affiliation"]["name"] == "Griffith University", pid
        assert person["image"] == f"{SITE_URL}/assets/img/people/{src['photo']}", pid
        for link in src.get("links", {}).values():
            assert link in person["sameAs"], (pid, link)


def test_project_pages_are_web_pages_with_a_fixed_publication_date(built_site):
    for slug in PROJECTS:
        date = _front_matter(ROOT / "_projects" / f"{slug}.md")["date"]
        blocks = _json_ld(built_site(f"/projects/{slug}/"))
        page = next(b for b in blocks if b.get("@type") == "WebPage")
        assert not any(b.get("@type") == "BlogPosting" for b in blocks), slug
        assert page["datePublished"].startswith(date.isoformat()), slug
        assert "dateModified" in page, slug


def test_project_pages_carry_breadcrumbs(built_site):
    blocks = _json_ld(built_site("/projects/pentestgpt/"))
    crumbs = next(b for b in blocks if b.get("@type") == "BreadcrumbList")["itemListElement"]
    assert [c["name"] for c in crumbs] == ["RISE Lab", "Projects", "PentestGPT"]
    assert [c["item"] for c in crumbs] == [f"{SITE_URL}/", f"{SITE_URL}/projects/", f"{SITE_URL}/projects/pentestgpt/"]
    assert [c["position"] for c in crumbs] == [1, 2, 3]


# ---- Indexing hints ---------------------------------------------------------------------
def test_only_the_404_page_is_noindex(built_site):
    assert '<meta name="robots" content="noindex">' in built_site("/404.html")
    for path in _all_paths():
        assert 'name="robots"' not in built_site(path), path


def test_sitemap_lists_every_page_with_a_last_modified_date_and_no_assets(built_site):
    sitemap = built_site("/sitemap.xml")
    entries = re.findall(r"<url>([\s\S]*?)</url>", sitemap)
    locs = [re.search(r"<loc>(.*?)</loc>", e).group(1) for e in entries]
    assert sorted(locs) == sorted(f"{SITE_URL}{p}" for p in _all_paths())
    for entry in entries:
        assert "<lastmod>" in entry, entry
    assert "/assets/" not in sitemap
    assert "404" not in sitemap
