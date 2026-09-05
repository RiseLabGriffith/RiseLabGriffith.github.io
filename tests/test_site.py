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
