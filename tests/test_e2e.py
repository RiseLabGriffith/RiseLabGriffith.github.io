"""Browser tests with Playwright: theme, navigation, framework stack, filters, search, BibTeX copy, counters.

Skipped automatically when Playwright or its Chromium build is not installed:
    pip install playwright && python -m playwright install chromium
"""
import functools
import http.server
import pathlib
import socketserver
import threading

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ["/", "/research/", "/people/", "/publications/", "/projects/", "/projects/pentestgpt/", "/news/", "/about/", "/join/", "/404.html"]
MOBILE = {"viewport": {"width": 390, "height": 844}, "device_scale_factor": 2, "is_mobile": True, "has_touch": True}


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep pytest output clean
        pass


@pytest.fixture(scope="module")
def server(built_site):
    handler = functools.partial(_Quiet, directory=str(ROOT / "_site"))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as exc:  # browser binaries missing
            pytest.skip(f"Chromium for Playwright is not installed: {exc}")
        yield b
        b.close()


@pytest.fixture
def page(browser, request):
    options = getattr(request, "param", {}) or {}
    context = browser.new_context(**options)
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    pg = context.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errors.append(f"console: {m.text}") if m.type == "error" and "net::ERR" not in m.text and "Failed to load resource" not in m.text else None)
    pg.errors = errors
    yield pg
    context.close()


def test_every_page_loads_without_script_errors(server, page):
    for path in PAGES:
        page.goto(server + path)
        page.wait_for_load_state("load")
        assert page.locator("main").count() == 1, path
    assert page.errors == [], page.errors


@pytest.mark.parametrize("page", [MOBILE], indirect=True)
def test_no_horizontal_overflow_on_mobile(server, page):
    for path in PAGES:
        page.goto(server + path)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 0, f"{path} overflows by {overflow}px"


@pytest.mark.parametrize("page", [MOBILE], indirect=True)
def test_mobile_nav_toggle(server, page):
    page.goto(server + "/")
    toggle = page.locator("[data-nav-toggle]")
    assert toggle.is_visible()
    menu = page.locator("#site-nav")
    assert not menu.locator("a").first.is_visible()
    toggle.click()
    assert toggle.get_attribute("aria-expanded") == "true"
    assert menu.locator("a").first.is_visible()
    toggle.click()
    assert toggle.get_attribute("aria-expanded") == "false"


def test_theme_toggle_persists_across_reload(server, page):
    page.goto(server + "/")
    initial = page.evaluate("document.documentElement.getAttribute('data-theme')")
    page.locator("[data-theme-toggle]").click()
    after = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert after in ("light", "dark") and after != initial
    assert page.evaluate("localStorage.getItem('rise-theme')") == after
    page.reload()
    assert page.evaluate("document.documentElement.getAttribute('data-theme')") == after
    background = page.evaluate("getComputedStyle(document.body).backgroundColor")
    assert background == ("rgb(14, 20, 28)" if after == "dark" else "rgb(250, 249, 246)")


@pytest.mark.parametrize("page", [{"color_scheme": "dark"}], indirect=True)
def test_dark_scheme_is_honoured_without_a_stored_choice(server, page):
    page.goto(server + "/")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(14, 20, 28)"


def test_framework_stack_click_and_keyboard(server, page):
    page.goto(server + "/research/")
    heads = page.locator("[data-stack] .stack__head")
    assert heads.count() == 4
    assert all(heads.nth(i).get_attribute("aria-expanded") == "false" for i in range(4))
    heads.nth(0).click()
    assert heads.nth(0).get_attribute("aria-expanded") == "true"
    assert page.locator("#stack-R").is_visible()
    heads.nth(0).press("ArrowDown")
    assert page.evaluate("document.activeElement.id") == "stack-head-I"
    page.keyboard.press("Enter")
    assert heads.nth(1).get_attribute("aria-expanded") == "true"
    assert heads.nth(0).get_attribute("aria-expanded") == "false", "only one layer open at a time"
    heads.nth(1).press("End")
    assert page.evaluate("document.activeElement.id") == "stack-head-E"


def test_people_layer_filter(server, page):
    page.goto(server + "/people/")
    total = page.locator(".person").count()
    page.locator('[data-people-filter="S"]').click()
    visible = page.locator(".person:visible").count()
    assert 0 < visible < total
    hidden_without_s = page.evaluate("Array.from(document.querySelectorAll('.person')).filter(p => !p.hidden && !(' ' + p.dataset.layers + ' ').includes(' S ')).length")
    assert hidden_without_s == 0
    assert "of" in page.locator("[data-people-count]").inner_text()
    page.locator('[data-people-filter="all"]').click()
    assert page.locator(".person:visible").count() == total


def test_publications_search_filters_and_url_state(server, page):
    page.goto(server + "/publications/")
    total = page.locator(".pub").count()
    assert page.locator("[data-pub-toolbar]").is_visible()
    search = page.locator("[data-pub-search]")
    search.fill("jailbreak")
    shown = page.locator(".pub:visible").count()
    assert 0 < shown < total
    assert page.evaluate("Array.from(document.querySelectorAll('.pub')).filter(p => !p.hidden && !p.dataset.search.includes('jailbreak')).length") == 0
    assert f"{shown} of {total}" in page.locator("[data-pub-count]").inner_text()
    assert "q=jailbreak" in page.url
    search.press("Escape")
    assert page.locator(".pub:visible").count() == total
    page.locator('[data-pub-filter-layer="S"]').click()
    assert page.evaluate("Array.from(document.querySelectorAll('.pub')).filter(p => !p.hidden && !(' ' + p.dataset.layers + ' ').includes(' S ')).length") == 0
    page.locator('[data-pub-filter-type="journal"]').click()
    assert page.evaluate("Array.from(document.querySelectorAll('.pub')).filter(p => !p.hidden && p.dataset.type !== 'journal').length") == 0
    assert "layer=S" in page.url and "type=journal" in page.url
    page.locator("[data-pub-reset]").first.click()
    assert page.locator(".pub:visible").count() == total
    page.select_option("[data-pub-filter-member]", "qinyi-li")
    assert page.evaluate("Array.from(document.querySelectorAll('.pub')).filter(p => !p.hidden && !(' ' + p.dataset.members + ' ').includes(' qinyi-li ')).length") == 0
    page.locator("[data-pub-selected]").check()
    assert page.evaluate("Array.from(document.querySelectorAll('.pub')).filter(p => !p.hidden && p.dataset.selected !== 'true').length") == 0
    # Empty-year sections collapse; the empty state appears when nothing matches.
    search.fill("zzzz-no-such-paper")
    assert page.locator("[data-pub-empty]").is_visible()
    assert page.locator("[data-pub-year]:visible").count() == 0


def test_publications_deep_links_from_research_page(server, page):
    page.goto(server + "/publications/?topic=llm-agent-security")
    total = page.locator(".pub").count()
    assert page.locator('[data-pub-topic="llm-agent-security"]').is_visible()
    assert 0 < page.locator(".pub:visible").count() < total
    page.locator('[data-pub-topic="llm-agent-security"]').click()
    assert page.locator(".pub:visible").count() == total
    page.goto(server + "/publications/?member=wei-song&selected=1")
    assert page.locator("[data-pub-filter-member]").input_value() == "wei-song"
    assert page.locator("[data-pub-selected]").is_checked()


def test_slash_focuses_search_and_bibtex_copies(server, page):
    page.goto(server + "/publications/")
    page.keyboard.press("/")
    assert page.evaluate("document.activeElement === document.querySelector('[data-pub-search]')")
    page.keyboard.press("Escape")
    page.locator("body").click()
    first = page.locator("[data-bibtex]").first
    first.click()
    toast = page.locator("[data-toast]")
    toast.wait_for(state="visible")
    assert "BibTeX copied" in toast.inner_text()
    clip = page.evaluate("navigator.clipboard.readText()")
    assert clip.startswith("@inproceedings{" + first.get_attribute("data-id") + ",")
    assert "title = {{" in clip and "author = {" in clip and " and " in clip and "year = {" in clip


def test_home_counters_animate_to_their_targets(server, page):
    page.goto(server + "/")
    stats = page.locator("[data-count]")
    assert stats.count() == 4
    stats.first.scroll_into_view_if_needed()
    page.wait_for_function("Array.from(document.querySelectorAll('[data-count]')).every(el => el.textContent === el.getAttribute('data-count'))", timeout=5000)


def test_hero_letters_link_to_layers(server, page):
    page.goto(server + "/")
    letters = page.locator("[data-letter]")
    assert letters.count() == 4
    letters.nth(1).hover()
    page.wait_for_function("getComputedStyle(document.querySelector('[data-letter=\"I\"] .wordmark__phrase')).opacity === '1'", timeout=3000)
    letters.nth(1).click()
    assert page.url.endswith("/research/#layer-I")
