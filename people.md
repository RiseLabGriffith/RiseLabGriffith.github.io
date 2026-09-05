---
title: People
permalink: /people/
description: The director, academic members, PhD students, visitors and collaborators of RISE Lab at Griffith University.
eyebrow: People
headline: A collaborative cybersecurity community
intro: RISE brings together complementary expertise in trustworthy AI, applied cryptography, privacy-preserving computation, LLM and agent security, and secure software engineering. Members keep their own research identities and share themes, students, infrastructure and a common profile.
---

{%- assign people = site.data.people -%}
{%- assign directors = people | where: "role", "director" -%}
{%- assign academics = people | where: "role", "academic" -%}
{%- assign students = people | where: "role", "student" -%}
{%- assign visitors = people | where: "role", "visitor" -%}
{%- assign joint = people | where: "role", "joint" -%}
{%- assign alumni = people | where: "role", "alumni" -%}

<div class="chip-row people-filters" data-people-filters role="group" aria-label="Filter members by framework layer">
<span class="chip-row__label">Filter by layer</span>
<button class="chip" type="button" data-people-filter="all" aria-pressed="true">All</button>
{%- for layer in site.data.research.layers -%}
<button class="chip chip--{{ layer.id }}" type="button" data-people-filter="{{ layer.id }}" aria-pressed="false" title="{{ layer.name }}"><strong>{{ layer.letter }}</strong> {{ layer.short }}</button>
{%- endfor -%}
<span class="people-filters__count meta" data-people-count aria-live="polite"></span>
</div>

<section class="people-group" data-people-group>
<h2 class="people-group__title">Director</h2>
<div class="people-grid people-grid--detail">
{%- for p in directors -%}{% include person-card.html person=p detail=true %}{%- endfor -%}
</div>
</section>

<section class="people-group" data-people-group>
<h2 class="people-group__title">Academic members <span class="people-group__count">{{ academics.size }}</span></h2>
<div class="people-grid people-grid--detail">
{%- for p in academics -%}{% include person-card.html person=p detail=true %}{%- endfor -%}
</div>
</section>

<section class="people-group" data-people-group>
<h2 class="people-group__title">PhD students <span class="people-group__count">{{ students.size }}</span></h2>
<p class="people-group__note">Higher Degree by Research students based at Griffith University.</p>
<div class="people-grid">
{%- for p in students -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</section>

{%- if visitors.size > 0 -%}
<section class="people-group" data-people-group>
<h2 class="people-group__title">Visiting researchers <span class="people-group__count">{{ visitors.size }}</span></h2>
<div class="people-grid">
{%- for p in visitors -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</section>
{%- endif -%}

{%- if joint.size > 0 -%}
<section class="people-group" data-people-group>
<details class="fold">
<summary>Jointly supervised students at partner institutions <span class="people-group__count">{{ joint.size }}</span></summary>
<p class="people-group__note">Students enrolled elsewhere and co-supervised by RISE members.</p>
<div class="people-grid">
{%- for p in joint -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</details>
</section>
{%- endif -%}

{%- if alumni.size > 0 -%}
<section class="people-group" data-people-group>
<h2 class="people-group__title">Alumni <span class="people-group__count">{{ alumni.size }}</span></h2>
<div class="people-grid">
{%- for p in alumni -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</section>
{%- endif -%}

<p class="people-join">Interested in joining? See <a href="{{ '/join/' | relative_url }}">Join Us</a> for PhD scholarships, postdoctoral and visiting opportunities.</p>
