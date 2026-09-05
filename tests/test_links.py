"""Every internal link and asset reference in the built site must resolve, including #fragments."""
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "//", "javascript:")


def _ids(text):
    return set(re.findall(r'\bid="([^"]+)"', text))


def test_internal_links_and_fragments_resolve(built_site):
    site = ROOT / "_site"
    pages = {p: p.read_text(encoding="utf-8") for p in site.rglob("*.html")}
    id_cache = {p: _ids(t) for p, t in pages.items()}
    problems = []
    for html_file, text in pages.items():
        for _attr, url in re.findall(r'\b(href|src)="([^"]+)"', text):
            if url.startswith(SKIP_PREFIXES):
                continue
            parts = urllib.parse.urlsplit(url)
            if parts.path:
                target = site / parts.path.lstrip("/") if parts.path.startswith("/") else html_file.parent / parts.path
                if target.is_dir():
                    target = target / "index.html"
                if not target.exists():
                    problems.append(f"{html_file.relative_to(site)} -> {url} (missing file)")
                    continue
            else:
                target = html_file
            if parts.fragment and target.suffix == ".html":
                ids = id_cache.get(target)
                if ids is None:
                    ids = id_cache[target] = _ids(target.read_text(encoding="utf-8"))
                if parts.fragment not in ids:
                    problems.append(f"{html_file.relative_to(site)} -> {url} (missing #{parts.fragment})")
    assert not problems, "\n".join(sorted(set(problems)))
