import os
import pathlib
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PATH="/opt/homebrew/opt/ruby/bin:" + os.environ.get("PATH", ""))


@pytest.fixture(scope="session")
def built_site():
    """Build the site once per test session and return a reader for rendered files."""
    subprocess.run(["bundle", "exec", "jekyll", "build", "--quiet"], cwd=ROOT, env=ENV, check=True)
    site = ROOT / "_site"

    def read(path):
        p = site / path.lstrip("/")
        if p.is_dir():
            p = p / "index.html"
        return p.read_text(encoding="utf-8")

    return read
