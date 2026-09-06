"""Editorial rules for the content data: short copy, and news that reflects the whole lab rather than one member.

These checks read the YAML and page files directly, so they run without building the site.
"""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ["index.md", "about.md", "research.md", "people.md", "publications.md", "projects.md", "news.md", "join.md"]


def _load(name):
    return yaml.safe_load((ROOT / "_data" / name).read_text(encoding="utf-8"))


def _words(text):
    return len(re.findall(r"\S+", str(text or "")))


def _front_matter(path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1]) or {}


def _academics():
    return [p["id"] for p in _load("people.yml") if p["role"] in ("director", "academic")]


# ---- Copy length ------------------------------------------------------------------
def test_page_intros_are_one_sentence():
    for name in PAGES:
        fm = _front_matter(ROOT / name)
        intro = fm.get("intro")
        if intro:
            assert _words(intro) <= 28, f"{name}: intro is {_words(intro)} words"


def test_news_texts_are_short():
    for item in _load("news.yml"):
        assert _words(item["text"]) <= 40, f"news '{item['title']}' is {_words(item['text'])} words"


def test_academic_bios_are_two_sentences():
    for p in _load("people.yml"):
        if p.get("bio"):
            assert _words(p["bio"]) <= 55, f"{p['id']} bio is {_words(p['bio'])} words"


def test_research_descriptions_are_short():
    data = _load("research.yml")
    for layer in data["layers"]:
        assert _words(layer["description"]) <= 45, f"layer {layer['id']} description is {_words(layer['description'])} words"
        for topic in layer["topics"]:
            assert _words(topic["summary"]) <= 45, f"topic {topic['id']} summary is {_words(topic['summary'])} words"


def test_opening_summaries_are_short():
    for o in _load("openings.yml"):
        assert _words(o["summary"]) <= 32, f"opening '{o['title']}' summary is {_words(o['summary'])} words"


# ---- Balance across members ---------------------------------------------------------
def test_news_mentions_every_academic_more_than_once():
    news = _load("news.yml")
    for pid in _academics():
        hits = [n for n in news if pid in (n.get("members") or [])]
        assert len(hits) >= 2, f"{pid} appears in only {len(hits)} news items"


def test_news_is_not_dominated_by_one_member():
    news = _load("news.yml")
    solo = [n for n in news if (n.get("members") or []) == ["yi-liu"]]
    assert len(solo) <= 1, [n["title"] for n in solo]
    with_yi = [n for n in news if "yi-liu" in (n.get("members") or [])]
    assert len(with_yi) * 4 <= len(news), f"Yi Liu appears in {len(with_yi)} of {len(news)} items"


def test_featured_projects_are_led_by_different_members():
    featured = []
    for path in sorted((ROOT / "_projects").glob("*.md")):
        if path.name.startswith("_"):
            continue
        fm = _front_matter(path)
        if fm.get("featured"):
            featured.append((path.stem, fm))
    assert 2 <= len(featured) <= 3, [f[0] for f in featured]
    firsts = [fm["members"][0] for _, fm in featured]
    assert len(set(firsts)) == len(firsts), firsts
    assert "yi-liu" not in firsts, firsts
    assert "pentestgpt" not in [slug for slug, _ in featured]
