import pathlib
import textwrap

from scripts.check_data import validate

ROOT = pathlib.Path(__file__).resolve().parents[1]


def write(tmp, rel, text):
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text), encoding="utf-8")
    return p


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
    write(tmp, "_data/publications.yml",
          "- {id: x2026, title: T, authors: [Leo Zhang], venue: V, year: 2026, type: conference, layers: [R], members: [leo-zhang]}\n")
    write(tmp, "_data/news.yml",
          "- {date: 2026-09-01, kind: general, title: t, text: x}\n- {date: 2026-08-01, kind: general, title: t, text: x}\n")
    write(tmp, "_data/events.yml", "[]\n")
    write(tmp, "_data/openings.yml", "[]\n")
    write(tmp, "_projects/a.md", "---\ntitle: A\nsummary: s\nkind: direction\nstatus: active\nlayers: [R]\nmembers: [leo-zhang]\n---\nbody\n")


def test_valid_data_has_no_errors(tmp_path):
    minimal(tmp_path)
    assert validate(tmp_path) == []


def test_unknown_member_reference_is_reported(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/publications.yml",
          "- {id: x2026, title: T, authors: [A], venue: V, year: 2026, type: conference, layers: [R], members: [nobody]}\n")
    assert any("nobody" in e for e in validate(tmp_path))


def test_news_must_be_newest_first(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/news.yml",
          "- {date: 2026-08-01, kind: general, title: t, text: x}\n- {date: 2026-09-01, kind: general, title: t, text: x}\n")
    assert any("newest first" in e for e in validate(tmp_path))


def test_bad_layer_is_reported(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/people.yml", "- {id: leo-zhang, name: Leo Zhang, role: director, position: AP, layers: [Q]}\n")
    assert any("layer" in e.lower() for e in validate(tmp_path))


def test_duplicate_ids_are_reported(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_data/people.yml",
          "- {id: leo-zhang, name: Leo Zhang, role: director, position: AP, layers: [R]}\n"
          "- {id: leo-zhang, name: Other, role: academic, position: L, layers: [I]}\n")
    assert any("duplicate" in e.lower() for e in validate(tmp_path))


def test_project_front_matter_is_checked(tmp_path):
    minimal(tmp_path)
    write(tmp_path, "_projects/a.md", "---\ntitle: A\nsummary: s\nkind: bogus\nstatus: active\nlayers: [R]\nmembers: [leo-zhang]\n---\nbody\n")
    assert any("kind" in e for e in validate(tmp_path))


def test_real_repo_data_is_valid():
    assert validate(ROOT) == []
