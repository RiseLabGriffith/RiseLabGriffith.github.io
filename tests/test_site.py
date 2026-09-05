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
