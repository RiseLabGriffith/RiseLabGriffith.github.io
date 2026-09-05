#!/usr/bin/env python3
"""Validate the RISE Lab content data (_data/*.yml and _projects/*.md).

Usage: python3 scripts/check_data.py [ROOT]
Exits 1 and prints one line per problem when the data is invalid.
Only the standard library and PyYAML are required.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys

import yaml

LAYERS = ["R", "I", "S", "E"]
ROLES = {"director", "academic", "student", "visitor", "joint", "alumni"}
PUB_TYPES = {"conference", "journal", "preprint", "workshop", "thesis", "book", "chapter"}
NEWS_KINDS = {"paper", "award", "grant", "people", "event", "media", "general"}
EVENT_KINDS = {"seminar", "reading-group", "workshop", "visit", "talk", "other"}
OPENING_KINDS = {"phd", "postdoc", "visiting", "honours", "masters", "intern"}
PROJECT_KINDS = {"direction", "funded", "software"}
PROJECT_STATUS = {"active", "proposed", "completed"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- helpers
def load(path: pathlib.Path):
    """Load a YAML file. Returns (data, error) where error is None on success."""
    if not path.exists():
        return None, f"{path.name}: file is missing"
    try:
        with path.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh), None
    except yaml.YAMLError as exc:  # pragma: no cover - exercised manually
        return None, f"{path.name}: YAML error: {exc}"


def as_date(value):
    """Return a datetime.date for YAML dates, datetimes or ISO strings; None otherwise."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and ISO_DATE.match(value):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return None
    return None


def require(item: dict, fields, where: str, errors: list):
    for f in fields:
        if f not in item or item[f] in (None, "", [], {}):
            errors.append(f"{where}: missing required field '{f}'")


def check_layers(value, where: str, errors: list, required=False):
    if value is None:
        if required:
            errors.append(f"{where}: missing 'layers'")
        return
    if not isinstance(value, list):
        errors.append(f"{where}: 'layers' must be a list of layer letters")
        return
    bad = [v for v in value if v not in LAYERS]
    if bad:
        errors.append(f"{where}: unknown layer(s) {bad}; expected a subset of {LAYERS}")


def check_refs(value, field: str, known: set, where: str, errors: list):
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{where}: '{field}' must be a list")
        return
    for ref in value:
        if ref not in known:
            errors.append(f"{where}: '{field}' references unknown id '{ref}'")


def expect_list(data, name: str, errors: list):
    if data is None:
        return []
    if not isinstance(data, list):
        errors.append(f"{name}: top level must be a list")
        return []
    return data


# --------------------------------------------------------------------------- per-file checks
def check_research(data, errors: list) -> set:
    """Validate research.yml and return the set of topic ids."""
    topics: set = set()
    if not isinstance(data, dict):
        errors.append("research.yml: top level must be a mapping with 'lifecycle' and 'layers'")
        return topics
    lifecycle = data.get("lifecycle")
    if not isinstance(lifecycle, list) or not lifecycle or not all(isinstance(s, str) for s in lifecycle):
        errors.append("research.yml: 'lifecycle' must be a non-empty list of stage names")
    layers = data.get("layers")
    if not isinstance(layers, list):
        errors.append("research.yml: 'layers' must be a list")
        return topics
    ids = [layer.get("id") if isinstance(layer, dict) else None for layer in layers]
    if ids != LAYERS:
        errors.append(f"research.yml: layer ids must be exactly {LAYERS} in order, got {ids}")
    for layer in layers:
        if not isinstance(layer, dict):
            errors.append("research.yml: each layer must be a mapping")
            continue
        where = f"research.yml layer {layer.get('id', '?')}"
        require(layer, ["id", "letter", "name", "short", "tagline", "keywords", "description", "topics"], where, errors)
        if not isinstance(layer.get("keywords", []), list):
            errors.append(f"{where}: 'keywords' must be a list")
        for topic in layer.get("topics") or []:
            if not isinstance(topic, dict):
                errors.append(f"{where}: each topic must be a mapping")
                continue
            twhere = f"{where} topic {topic.get('id', '?')}"
            require(topic, ["id", "name", "summary", "keywords"], twhere, errors)
            tid = topic.get("id")
            if tid is not None:
                if not SLUG.match(str(tid)):
                    errors.append(f"{twhere}: id must be a lowercase slug")
                if tid in topics:
                    errors.append(f"{twhere}: duplicate topic id '{tid}'")
                topics.add(tid)
    return topics


def check_people(data, root: pathlib.Path, errors: list) -> set:
    """Validate people.yml and return the set of person ids."""
    ids: set = set()
    people = expect_list(data, "people.yml", errors)
    for i, person in enumerate(people):
        if not isinstance(person, dict):
            errors.append(f"people.yml[{i}]: entry must be a mapping")
            continue
        pid = person.get("id")
        where = f"people.yml '{pid or person.get('name') or i}'"
        require(person, ["id", "name", "role", "position"], where, errors)
        if pid is not None:
            if not SLUG.match(str(pid)):
                errors.append(f"{where}: id must be a lowercase slug like 'leo-zhang'")
            if pid in ids:
                errors.append(f"{where}: duplicate person id '{pid}'")
            ids.add(pid)
        role = person.get("role")
        if role is not None and role not in ROLES:
            errors.append(f"{where}: role '{role}' not in {sorted(ROLES)}")
        check_layers(person.get("layers"), where, errors, required=role in {"director", "academic"})
        aliases = person.get("aliases")
        if aliases is not None and not isinstance(aliases, list):
            errors.append(f"{where}: 'aliases' must be a list of names")
        photo = person.get("photo")
        if photo and not (root / "assets" / "img" / "people" / str(photo)).exists():
            errors.append(f"{where}: photo '{photo}' not found in assets/img/people/")
        links = person.get("links")
        if links is not None and not isinstance(links, dict):
            errors.append(f"{where}: 'links' must be a mapping of label to URL")
    # Supervisor references are checked after all ids are known.
    for person in people:
        if not isinstance(person, dict):
            continue
        sup = person.get("supervisors", person.get("supervisor"))
        if sup is None:
            continue
        for s in (sup if isinstance(sup, list) else [sup]):
            if s not in ids:
                errors.append(f"people.yml '{person.get('id')}': supervisor '{s}' is not a known person id")
    return ids


def check_publications(data, people: set, topics: set, errors: list):
    pubs = expect_list(data, "publications.yml", errors)
    ids: set = set()
    for i, pub in enumerate(pubs):
        if not isinstance(pub, dict):
            errors.append(f"publications.yml[{i}]: entry must be a mapping")
            continue
        pid = pub.get("id")
        where = f"publications.yml '{pid or i}'"
        require(pub, ["id", "title", "authors", "venue", "year", "type"], where, errors)
        if pid is not None:
            if pid in ids:
                errors.append(f"{where}: duplicate publication id '{pid}'")
            ids.add(pid)
        year = pub.get("year")
        if year is not None and (not isinstance(year, int) or isinstance(year, bool) or not 1990 <= year <= 2100):
            errors.append(f"{where}: 'year' must be an integer year, got {year!r}")
        ptype = pub.get("type")
        if ptype is not None and ptype not in PUB_TYPES:
            errors.append(f"{where}: type '{ptype}' not in {sorted(PUB_TYPES)}")
        authors = pub.get("authors")
        if authors is not None and (not isinstance(authors, list) or not authors or not all(isinstance(a, str) and a.strip() for a in authors)):
            errors.append(f"{where}: 'authors' must be a non-empty list of names")
        check_layers(pub.get("layers"), where, errors, required=True)
        check_refs(pub.get("members"), "members", people, where, errors)
        check_refs(pub.get("topics"), "topics", topics, where, errors)
        if "selected" in pub and not isinstance(pub["selected"], bool):
            errors.append(f"{where}: 'selected' must be true or false")
        links = pub.get("links")
        if links is not None and not isinstance(links, dict):
            errors.append(f"{where}: 'links' must be a mapping of label to URL")


def check_news(data, people: set, errors: list):
    items = expect_list(data, "news.yml", errors)
    previous = None
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"news.yml[{i}]: entry must be a mapping")
            continue
        where = f"news.yml[{i}] '{str(item.get('title', ''))[:40]}'"
        require(item, ["date", "title", "text"], where, errors)
        date = as_date(item.get("date"))
        if item.get("date") is not None and date is None:
            errors.append(f"{where}: 'date' must be an ISO date YYYY-MM-DD")
        if date is not None:
            if previous is not None and date > previous:
                errors.append(f"{where}: news must be sorted newest first ({date} appears after {previous})")
            previous = date
        kind = item.get("kind")
        if kind is not None and kind not in NEWS_KINDS:
            errors.append(f"{where}: kind '{kind}' not in {sorted(NEWS_KINDS)}")
        check_refs(item.get("members"), "members", people, where, errors)


def check_events(data, errors: list):
    items = expect_list(data, "events.yml", errors)
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"events.yml[{i}]: entry must be a mapping")
            continue
        where = f"events.yml[{i}] '{str(item.get('title', ''))[:40]}'"
        require(item, ["date", "kind", "title"], where, errors)
        if item.get("date") is not None and as_date(item.get("date")) is None:
            errors.append(f"{where}: 'date' must be an ISO date YYYY-MM-DD")
        kind = item.get("kind")
        if kind is not None and kind not in EVENT_KINDS:
            errors.append(f"{where}: kind '{kind}' not in {sorted(EVENT_KINDS)}")


def check_openings(data, people: set, errors: list):
    items = expect_list(data, "openings.yml", errors)
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"openings.yml[{i}]: entry must be a mapping")
            continue
        where = f"openings.yml[{i}] '{str(item.get('title', ''))[:40]}'"
        require(item, ["title", "kind", "summary"], where, errors)
        kind = item.get("kind")
        if kind is not None and kind not in OPENING_KINDS:
            errors.append(f"{where}: kind '{kind}' not in {sorted(OPENING_KINDS)}")
        check_refs(item.get("supervisors"), "supervisors", people, where, errors)
        check_layers(item.get("layers"), where, errors)
        if "open" in item and not isinstance(item["open"], bool):
            errors.append(f"{where}: 'open' must be true or false")


def front_matter(text: str):
    """Return the parsed YAML front matter of a Markdown file, or None when absent."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1]) or {}


def check_projects(root: pathlib.Path, people: set, errors: list):
    folder = root / "_projects"
    if not folder.is_dir():
        return
    for path in sorted(folder.glob("*.md")):
        if path.name.startswith("_"):
            continue
        where = f"_projects/{path.name}"
        try:
            fm = front_matter(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{where}: front matter YAML error: {exc}")
            continue
        if not isinstance(fm, dict):
            errors.append(f"{where}: missing YAML front matter")
            continue
        require(fm, ["title", "summary", "kind", "status", "layers"], where, errors)
        if fm.get("kind") is not None and fm["kind"] not in PROJECT_KINDS:
            errors.append(f"{where}: kind '{fm['kind']}' not in {sorted(PROJECT_KINDS)}")
        if fm.get("status") is not None and fm["status"] not in PROJECT_STATUS:
            errors.append(f"{where}: status '{fm['status']}' not in {sorted(PROJECT_STATUS)}")
        check_layers(fm.get("layers"), where, errors)
        check_refs(fm.get("members"), "members", people, where, errors)
        if "featured" in fm and not isinstance(fm["featured"], bool):
            errors.append(f"{where}: 'featured' must be true or false")


# --------------------------------------------------------------------------- entry points
def validate(root: pathlib.Path) -> list[str]:
    """Validate all content under ROOT. Returns a list of error strings (empty when valid)."""
    root = pathlib.Path(root)
    data_dir = root / "_data"
    errors: list[str] = []
    loaded = {}
    for name in ["research", "people", "publications", "news", "events", "openings"]:
        data, err = load(data_dir / f"{name}.yml")
        if err:
            errors.append(err)
        loaded[name] = data

    topics = check_research(loaded["research"], errors) if loaded["research"] is not None else set()
    people = check_people(loaded["people"], root, errors) if loaded["people"] is not None else set()
    check_publications(loaded["publications"], people, topics, errors)
    check_news(loaded["news"], people, errors)
    check_events(loaded["events"], errors)
    check_openings(loaded["openings"], people, errors)
    check_projects(root, people, errors)
    return errors


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = pathlib.Path(argv[0]) if argv else pathlib.Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print(f"Found {len(errors)} problem(s) in the content data:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("Content data OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
