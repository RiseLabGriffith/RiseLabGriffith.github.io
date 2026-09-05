---
title: Research
permalink: /research/
description: The RISE framework connects four research layers, fourteen topics and the cybersecurity lifecycle.
eyebrow: Research
headline: Cybersecurity across the full system lifecycle
intro: The RISE framework organises our work into four connected layers. R defines responsible security practice and resilience outcomes, I develops intelligence and automation for cyber defence, S provides secure and privacy-preserving foundations, and E connects them through engineering, evaluation and continuous operation.
---

<p class="research-hint">Select a layer to see its keywords and topics, or scroll to explore each layer in detail. Every topic links to related members, publications and projects.</p>

{% include framework-stack.html mode="full" %}

<div class="research-layout">
<nav class="toc" data-scrollspy aria-label="Layers on this page">
<p class="toc__label">On this page</p>
<ol>
{%- for layer in site.data.research.layers -%}
<li><a class="toc__link toc__link--{{ layer.id }}" href="#layer-{{ layer.id }}"><span class="toc__letter">{{ layer.letter }}</span><span>{{ layer.short }}</span></a></li>
{%- endfor -%}
</ol>
</nav>

<div class="research-main">
{%- for layer in site.data.research.layers -%}
{%- assign L = layer.id -%}
<section class="layer-section layer-section--{{ L }}" id="layer-{{ L }}" data-layer="{{ L }}">
<header class="layer-section__head">
<span class="layer-section__letter" aria-hidden="true">{{ layer.letter }}</span>
<div>
<p class="eyebrow eyebrow--{{ L }}">Layer {{ layer.letter }}</p>
<h2>{{ layer.name }}</h2>
<p class="lede">{{ layer.tagline }}</p>
</div>
</header>
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
{%- for pr in layer_projects -%}<a class="chip chip--link" href="{{ pr.url | relative_url }}">{{ pr.title }}</a>{%- endfor -%}
</div>
{%- endif -%}
</div>
{%- endif -%}
<div class="topic-grid">
{%- for topic in layer.topics -%}
<article class="topic card rail-{{ L }}" id="{{ topic.id }}">
<h3 class="topic__name">{{ topic.name }}</h3>
<p class="topic__summary">{{ topic.summary }}</p>
<ul class="topic__keywords tag-row" aria-label="Keywords">
{%- for k in topic.keywords -%}<li class="tag">{{ k }}</li>{%- endfor -%}
</ul>
{%- assign topic_pubs = site.data.publications | where_exp: "pub", "pub.topics contains topic.id" | sort: "year" | reverse -%}
{%- if topic_pubs.size > 0 -%}
<div class="topic__pubs">
<p class="meta">Recent publications</p>
<ul>
{%- for pub in topic_pubs limit: 3 -%}
<li><a href="{{ '/publications/#' | append: pub.id | relative_url }}">{{ pub.title }}</a> <span class="meta">{{ pub.venue }} {{ pub.year }}</span></li>
{%- endfor -%}
</ul>
<a class="topic__more" href="{{ '/publications/?topic=' | append: topic.id | relative_url }}">All {{ topic_pubs.size }} publication{% if topic_pubs.size != 1 %}s{% endif %} on this topic</a>
</div>
{%- endif -%}
{%- assign topic_projects = site.projects | where_exp: "pr", "pr.topics contains topic.id" -%}
{%- if topic_projects.size > 0 -%}
<div class="topic__projects">
<p class="meta">Projects</p>
<ul>{%- for pr in topic_projects -%}<li><a href="{{ pr.url | relative_url }}">{{ pr.title }}</a></li>{%- endfor -%}</ul>
</div>
{%- endif -%}
</article>
{%- endfor -%}
</div>
</section>
{%- endfor -%}
</div>
</div>
