---
title: Projects
permalink: /projects/
description: RISE Lab research directions, cross-layer demonstrators, funded projects and open-source software.
headline: Directions, demonstrators and artefacts
intro: Long-running research directions, funded projects with partners, and open-source tools that connect RISE research to deployable outcomes.
---

{%- assign all = site.projects | sort: "order" -%}
{%- assign directions = all | where: "kind", "direction" -%}
{%- assign funded = all | where: "kind", "funded" -%}
{%- assign software = all | where: "kind", "software" -%}

<section class="chapter chapter--open" id="directions">
<div class="rail"><h2>Research directions and demonstrators<span class="count">{{ directions.size }}</span></h2><p class="rail__note meta">Demonstrators that integrate the R, I, S and E layers, each driven by several members.</p></div>
<div class="chapter__body">
<div class="card-grid">
{%- for pr in directions -%}{% include project-card.html project=pr %}{%- endfor -%}
</div>
</div>
</section>

<section class="chapter" id="funded">
<div class="rail"><h2>Funded projects<span class="count">{{ funded.size }}</span></h2><p class="rail__note meta">Externally funded work with industry and government partners.</p></div>
<div class="chapter__body">
<div class="card-grid">
{%- for pr in funded -%}{% include project-card.html project=pr %}{%- endfor -%}
</div>
</div>
</section>

<section class="chapter" id="software">
<div class="rail"><h2>Software and artefacts<span class="count">{{ software.size }}</span></h2><p class="rail__note meta">Tools, datasets and deployable systems.</p></div>
<div class="chapter__body">
<div class="card-grid">
{%- for pr in software -%}{% include project-card.html project=pr %}{%- endfor -%}
</div>
<p class="people-join">Interested in collaborating on a demonstrator or funded project? See <a href="{{ '/join/' | relative_url }}#partners">industry and government partnership</a>.</p>
</div>
</section>
