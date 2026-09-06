---
title: Research
permalink: /research/
description: The RISE framework connects four research layers, fourteen topics and the cybersecurity lifecycle.
headline: Cybersecurity across the full system lifecycle
intro: Four connected layers organise the lab's work, from responsible practice and resilience through intelligent defence and secure foundations to the engineering that turns them into deployed systems.
---

<div class="research-frame">
<p class="research-hint">Open a layer for its keywords and topics, or scroll to each layer in detail. Every topic links to related members, publications and projects.</p>
{% include framework-stack.html mode="full" %}
</div>

{%- for layer in site.data.research.layers -%}
{%- assign L = layer.id -%}
<section class="chapter layer-section layer-section--{{ L }}" id="layer-{{ L }}" data-layer="{{ L }}">
<div class="rail">
<span class="layer-rail__letter" aria-hidden="true">{{ layer.letter }}</span>
<h2>{{ layer.name }}</h2>
<p class="layer-rail__tagline">{{ layer.tagline }}</p>
</div>
<div class="chapter__body">
<p class="layer-section__desc">{{ layer.description }}</p>
{%- assign layer_people = site.data.people | where_exp: "p", "p.layers contains L" | where_exp: "p", "p.role == 'director' or p.role == 'academic'" -%}
{%- assign layer_projects = site.projects | where_exp: "pr", "pr.layers contains L" | sort: "order" -%}
{%- if layer_people.size > 0 or layer_projects.size > 0 -%}
<div class="layer-section__links">
{%- if layer_people.size > 0 -%}
<div class="link-row"><span class="link-row__label">People</span>
{%- for p in layer_people -%}<a class="chip chip--link" href="{{ '/people/#' | append: p.id | relative_url }}">{{ p.name }}</a>{%- endfor -%}
</div>
{%- endif -%}
{%- if layer_projects.size > 0 -%}
<div class="link-row"><span class="link-row__label">Projects</span>
{%- for pr in layer_projects -%}<a class="chip chip--link" href="{{ pr.url | relative_url }}">{{ pr.title | truncatewords: 6 }}</a>{%- endfor -%}
</div>
{%- endif -%}
</div>
{%- endif -%}
<div class="topics">
{%- for topic in layer.topics -%}
<article class="topic layer-{{ L }}" id="{{ topic.id }}">
<div>
<h3 class="topic__name">{{ topic.name }}</h3>
<p class="topic__summary">{{ topic.summary }}</p>
<p class="topic__keywords">{{ topic.keywords | join: ", " }}</p>
</div>
<div class="topic__refs">
{%- assign topic_pubs = site.data.publications | where_exp: "pub", "pub.topics contains topic.id" | sort: "year" | reverse -%}
{%- if topic_pubs.size > 0 -%}
<p class="label">Recent publications</p>
<ul>
{%- for pub in topic_pubs limit: 3 -%}
<li><a href="{{ '/publications/#' | append: pub.id | relative_url }}">{{ pub.title }}</a> <span class="meta">{{ pub.venue }} {{ pub.year }}</span></li>
{%- endfor -%}
</ul>
<a class="topic__more" href="{{ '/publications/?topic=' | append: topic.id | relative_url }}">All {{ topic_pubs.size }} publication{% if topic_pubs.size != 1 %}s{% endif %} on this topic</a>
{%- endif -%}
{%- assign topic_projects = site.projects | where_exp: "pr", "pr.topics contains topic.id" -%}
{%- if topic_projects.size > 0 -%}
<p class="label"{% if topic_pubs.size > 0 %} style="margin-top: 14px"{% endif %}>Projects</p>
<ul>{%- for pr in topic_projects -%}<li><a href="{{ pr.url | relative_url }}">{{ pr.title }}</a></li>{%- endfor -%}</ul>
{%- endif -%}
</div>
</article>
{%- endfor -%}
</div>
</div>
</section>
{%- endfor -%}
