import re

PAGES = ["/", "/research/", "/people/", "/publications/", "/projects/", "/news/", "/about/", "/join/", "/404.html"]


def test_all_pages_build(built_site):
    for p in PAGES:
        html = built_site(p)
        assert "<main" in html, p


def test_nav_links_are_root_relative(built_site):
    html = built_site("/")
    nav = re.findall(r'class="nav-links"[\s\S]*?</ul>', html)[0]
    assert "/RiseLabGriffith/" not in nav
    for target in ["/research/", "/people/", "/publications/", "/projects/", "/news/", "/about/", "/join/"]:
        assert f'href="{target}"' in nav, target


def test_theme_toggle_and_footer(built_site):
    html = built_site("/")
    assert "data-theme-toggle" in html
    assert "acknowledge" in html.lower()
    assert "Last updated" in html


def test_research_page_lists_four_layers_and_fourteen_topics(built_site):
    html = built_site("/research/")
    for L in "RISE":
        assert f'id="layer-{L}"' in html, L
    assert html.count('class="topic ') == 14


def test_framework_stack_is_keyboard_accessible(built_site):
    html = built_site("/research/")
    assert html.count('class="stack__head"') == 4
    assert 'aria-expanded="false"' in html
    assert 'data-stack' in html


def test_people_page_groups_and_members(built_site):
    html = built_site("/people/")
    for name in ["Leo Zhang", "Yanjun Zhang", "Qinyi Li", "He Zhang", "Yi Liu", "Wei Song"]:
        assert name in html, name
    assert html.count('class="person"') >= 20
    assert 'data-people-filter="I"' in html
    assert 'src="/assets/img/people/leo-zhang.jpg"' in html
    assert 'class="person__avatar"' in html  # students without photos get initials


def test_publications_page_has_entries_and_tools(built_site):
    html = built_site("/publications/")
    assert html.count('class="pub ') >= 60
    assert "data-pub-search" in html and "data-bibtex" in html and "data-pub-count" in html
    assert "<strong>Leo Zhang</strong>" in html or "<strong>Leo Yu Zhang</strong>" in html
    assert 'id="y2026"' in html


def test_projects_index_and_detail(built_site):
    html = built_site("/projects/")
    assert html.count('class="project card') >= 8
    for heading in ["Research directions", "Funded projects", "Software"]:
        assert heading in html, heading
    detail = built_site("/projects/secure-auditable-ai-agents/")
    assert "Status" in detail and 'class="tag tag--I"' in detail
    assert 'class="facts"' in detail


def test_news_page_timeline_and_events(built_site):
    html = built_site("/news/")
    assert html.count('class="news-item') >= 12
    assert "Upcoming" in html and 'class="timeline__year"' in html
    assert 'class="event' in html


def test_home_sections(built_site):
    html = built_site("/")
    for marker in ['class="hero"', "data-stack", 'class="stats"', "Latest news", "Selected publications", "Featured projects", "/join/"]:
        assert marker in html, marker
    assert html.count('class="pub ') <= 6
    assert html.count('data-letter=') == 4


def test_about_and_join(built_site):
    about = built_site("/about/")
    join = built_site("/join/")
    assert "Vision" in about and "How we work" in about and "TrustAGI" not in about
    assert "GUPRS" in join and "Open positions" in join and "mailto:" in join
    assert join.count('class="opening') >= 6


# ---- Editorial redesign ---------------------------------------------------------------
def test_site_loads_no_monospace_font(built_site):
    home = built_site("/")
    css = built_site("/assets/css/main.css")
    assert "Plex+Mono" not in home and "Plex Mono" not in home
    assert "Plex Mono" not in css and "monospace" not in css.split("[data-bibtex]")[0].replace("ui-monospace", "")


def test_home_hero_has_layer_bands_and_wordmark(built_site):
    html = built_site("/")
    assert 'class="hero"' in html
    assert html.count('class="band band--') == 4
    assert html.count('data-letter=') == 4


def test_home_introduces_every_academic_with_a_photo(built_site):
    html = built_site("/")
    section = re.search(r'<section class="[^"]*home-people[^"]*">([\s\S]*?)</section>', html).group(1)
    for photo in ["leo-zhang", "yanjun-zhang", "qinyi-li", "he-zhang", "yi-liu", "wei-song"]:
        assert f'src="/assets/img/people/{photo}.jpg"' in section, photo


def test_home_news_is_a_short_list(built_site):
    html = built_site("/")
    assert html.count('class="news-line ') == 5
    assert 'class="news-card' not in html


def test_home_selected_publications_cover_every_academic(built_site):
    html = built_site("/")
    members = re.findall(r'data-members="([^"]*)"', html)
    assert len(members) <= 6
    covered = set(" ".join(members).split())
    for pid in ["leo-zhang", "yanjun-zhang", "qinyi-li", "he-zhang", "yi-liu", "wei-song"]:
        assert pid in covered, pid


def test_home_featured_projects_do_not_include_pentestgpt(built_site):
    html = built_site("/")
    assert 'href="/projects/pentestgpt/"' not in html
    assert html.count('class="project card') == 3


def test_pages_use_section_rails_instead_of_eyebrows(built_site):
    for path in ["/about/", "/join/", "/projects/", "/news/"]:
        html = built_site(path)
        assert 'class="rail"' in html, path
        assert 'class="eyebrow"' not in html, path
