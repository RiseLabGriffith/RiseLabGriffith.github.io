---
title: Projects
permalink: /projects/
description: RISE Lab research directions, cross-layer demonstrators, funded projects and open-source software.
eyebrow: Projects
headline: Directions, demonstrators and artefacts
intro: Cross-layer work that connects RISE research to deployable outcomes, from long-running research directions to funded projects with partners and open-source tools that others can use.
---

{%- assign all = site.projects | sort: "order" -%}
{%- assign directions = all | where: "kind", "direction" -%}
{%- assign funded = all | where: "kind", "funded" -%}
{%- assign software = all | where: "kind", "software" -%}

<section class="project-group" id="directions">
<h2 class="project-group__title">Research directions and demonstrators <span class="people-group__count">{{ directions.size }}</span></h2>
<p class="people-group__note">Project-supported demonstrators that integrate the R, I, S and E layers. Each direction lists the members driving it and links to related publications.</p>
<div class="card-grid">
{%- for pr in directions -%}{% include project-card.html project=pr %}{%- endfor -%}
</div>
</section>

<section class="project-group" id="funded">
<h2 class="project-group__title">Funded projects <span class="people-group__count">{{ funded.size }}</span></h2>
<p class="people-group__note">Externally funded work led by RISE members with industry and government partners.</p>
<div class="card-grid">
{%- for pr in funded -%}{% include project-card.html project=pr %}{%- endfor -%}
</div>
</section>

<section class="project-group" id="software">
<h2 class="project-group__title">Software and artefacts <span class="people-group__count">{{ software.size }}</span></h2>
<p class="people-group__note">Tools, datasets and deployable systems produced by RISE members.</p>
<div class="card-grid">
{%- for pr in software -%}{% include project-card.html project=pr %}{%- endfor -%}
</div>
</section>

<p class="people-join">Interested in collaborating on a demonstrator or funded project? See <a href="{{ '/join/' | relative_url }}#partners">Industry and government partnership</a>.</p>
