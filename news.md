---
title: News & Events
permalink: /news/
description: News from RISE Lab at Griffith University, with upcoming seminars, reading groups and workshops.
headline: What the lab is doing
intro: Papers, grants, people and events from the RISE community. Seminars and reading groups are open to Griffith staff and students.
wide: true
---

{%- assign news = site.data.news -%}
{%- assign by_year = news | group_by_exp: "n", "n.date | date: '%Y'" -%}
{%- assign today = site.time | date: "%Y-%m-%d" -%}
{%- assign events = site.data.events | sort: "date" -%}
{%- assign upcoming_count = 0 -%}{%- assign past_count = 0 -%}
{%- for e in events -%}{%- assign d = e.date | date: "%Y-%m-%d" -%}{%- if d >= today -%}{%- assign upcoming_count = upcoming_count | plus: 1 -%}{%- else -%}{%- assign past_count = past_count | plus: 1 -%}{%- endif -%}{%- endfor -%}

<div class="news-layout">
<section class="timeline" aria-labelledby="news-heading">
<h2 id="news-heading" class="visually-hidden">News</h2>
{%- for group in by_year -%}
<div class="chapter{% if forloop.first %} chapter--open{% endif %}">
<div class="rail"><h3 class="timeline__year" id="news-{{ group.name }}">{{ group.name }}</h3></div>
<div class="chapter__body">
{%- for n in group.items -%}{% include news-item.html item=n %}{%- endfor -%}
</div>
</div>
{%- endfor -%}
</section>

<aside class="events" aria-labelledby="events-heading">
<h2 id="events-heading" class="events__title">Upcoming events<span class="count">{{ upcoming_count }}</span></h2>
{%- if upcoming_count > 0 -%}
<div class="events__list">
{%- for e in events -%}{%- assign d = e.date | date: "%Y-%m-%d" -%}{%- if d >= today -%}{% include event-item.html event=e %}{%- endif -%}{%- endfor -%}
</div>
{%- else -%}
<p class="events__empty">No events are scheduled at the moment. Seminars and reading groups will be announced here.</p>
{%- endif -%}
{%- if past_count > 0 -%}
<details class="fold events__past">
<summary>Past events<span class="count">{{ past_count }}</span></summary>
<div class="events__list">
{%- for e in events reversed -%}{%- assign d = e.date | date: "%Y-%m-%d" -%}{%- if d < today -%}{% include event-item.html event=e past=true %}{%- endif -%}{%- endfor -%}
</div>
</details>
{%- endif -%}
<p class="events__note meta">Times are Australian Eastern Standard Time (AEST, UTC+10).</p>
</aside>
</div>
