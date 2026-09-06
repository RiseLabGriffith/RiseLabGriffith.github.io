#!/usr/bin/env bash
# Render the social preview card and square logo from their SVG sources in scripts/social/.
# Needs rsvg-convert (macOS: brew install librsvg; Debian/Ubuntu: apt install librsvg2-bin).
set -euo pipefail
cd "$(dirname "$0")/.."
rsvg-convert -w 1200 -h 630 scripts/social/og-image.svg -o assets/img/og-image.png
rsvg-convert -w 512 -h 512 scripts/social/logo.svg -o assets/img/logo.png
echo "Wrote assets/img/og-image.png and assets/img/logo.png"
