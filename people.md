---
title: People
permalink: /people/
description: The director, academic members, PhD students, visitors and collaborators of RISE Lab at Griffith University.
headline: A collaborative cybersecurity community
intro: Six academics with complementary expertise, their PhD students, visitors and collaborators. Members keep their own research identities and share themes, students and infrastructure.
---

{%- assign people = site.data.people -%}
{%- assign directors = people | where: "role", "director" -%}
{%- assign academics = people | where: "role", "academic" -%}
{%- assign students = people | where: "role", "student" -%}
{%- assign visitors = people | where: "role", "visitor" -%}
{%- assign joint = people | where: "role", "joint" -%}
{%- assign alumni = people | where: "role", "alumni" -%}

<div class="chip-row people-filters" data-people-filters role="group" aria-label="Filter members by framework layer">
<span class="chip-row__label">Show</span>
<button class="chip" type="button" data-people-filter="all" aria-pressed="true">Everyone</button>
{%- for layer in site.data.research.layers -%}
<button class="chip chip--{{ layer.id }}" type="button" data-people-filter="{{ layer.id }}" aria-pressed="false" title="{{ layer.name }}"><strong>{{ layer.letter }}</strong> {{ layer.short }}</button>
{%- endfor -%}
<span class="people-filters__count meta" data-people-count aria-live="polite"></span>
</div>

<section class="chapter" id="director" data-people-group>
<div class="rail"><h2>Director</h2></div>
<div class="chapter__body people-list">
{%- for p in directors -%}{% include person-card.html person=p detail=true %}{%- endfor -%}
</div>
</section>

<section class="chapter" id="academics" data-people-group>
<div class="rail"><h2>Academic members<span class="count">{{ academics.size }}</span></h2></div>
<div class="chapter__body people-list">
{%- for p in academics -%}{% include person-card.html person=p detail=true %}{%- endfor -%}
</div>
</section>

<section class="chapter" id="students" data-people-group>
<div class="rail"><h2>PhD students<span class="count">{{ students.size }}</span></h2><p class="rail__note meta">Higher Degree by Research candidates based at Griffith.</p></div>
<div class="chapter__body">
<div class="people-grid">
{%- for p in students -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</div>
</section>

{%- if visitors.size > 0 -%}
<section class="chapter" id="visitors" data-people-group>
<div class="rail"><h2>Visiting researchers<span class="count">{{ visitors.size }}</span></h2></div>
<div class="chapter__body">
<div class="people-grid">
{%- for p in visitors -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</div>
</section>
{%- endif -%}

{%- if joint.size > 0 -%}
<section class="chapter" id="joint" data-people-group>
<div class="rail"><h2>Jointly supervised<span class="count">{{ joint.size }}</span></h2><p class="rail__note meta">Students enrolled at partner institutions and co-supervised by RISE members.</p></div>
<div class="chapter__body">
<details class="fold">
<summary>Show students at partner institutions</summary>
<div class="people-grid">
{%- for p in joint -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</details>
</div>
</section>
{%- endif -%}

{%- if alumni.size > 0 -%}
<section class="chapter" id="alumni" data-people-group>
<div class="rail"><h2>Alumni<span class="count">{{ alumni.size }}</span></h2></div>
<div class="chapter__body">
<div class="people-grid">
{%- for p in alumni -%}{% include person-card.html person=p %}{%- endfor -%}
</div>
</div>
</section>
{%- endif -%}

<p class="people-join">Interested in joining? See <a href="{{ '/join/' | relative_url }}">Join Us</a> for PhD scholarships, postdoctoral and visiting opportunities.</p>
