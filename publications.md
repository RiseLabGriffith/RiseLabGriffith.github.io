---
title: Publications
permalink: /publications/
description: Publications by RISE Lab members at Griffith University, searchable and filterable by framework layer, type and member, with BibTeX export.
headline: Papers, preprints and artefacts
intro: Peer-reviewed papers and preprints by RISE members since 2022. Search, filter by layer, type or member, and copy a BibTeX entry for any item.
---

{%- assign pubs = site.data.publications -%}
{%- assign years = pubs | map: "year" | uniq | sort | reverse -%}
{%- assign name_list = "" -%}
{%- for p in site.data.people -%}{%- assign name_list = name_list | append: p.name | append: "|" -%}{%- for a in p.aliases -%}{%- assign name_list = name_list | append: a | append: "|" -%}{%- endfor -%}{%- endfor -%}
{%- assign member_names = name_list | split: "|" -%}
{%- assign academics = site.data.people | where_exp: "p", "p.role == 'director' or p.role == 'academic'" -%}
{%- assign types = "conference,journal,preprint,workshop,thesis" | split: "," -%}

<div class="pub-toolbar" data-pub-toolbar hidden>
<div class="pub-toolbar__search">
<label class="visually-hidden" for="pub-search">Search publications</label>
<input id="pub-search" class="pub-toolbar__input" type="search" data-pub-search placeholder="Search title, author or venue" autocomplete="off" spellcheck="false">
<kbd class="pub-toolbar__kbd" aria-hidden="true">/</kbd>
</div>
<div class="chip-row" role="group" aria-label="Filter by framework layer">
<span class="chip-row__label">Layer</span>
{%- for layer in site.data.research.layers -%}
<button class="chip chip--{{ layer.id }}" type="button" data-pub-filter-layer="{{ layer.id }}" aria-pressed="false" title="{{ layer.name }}"><strong>{{ layer.letter }}</strong> {{ layer.short }}</button>
{%- endfor -%}
</div>
<div class="chip-row" role="group" aria-label="Filter by publication type">
<span class="chip-row__label">Type</span>
{%- for t in types -%}
<button class="chip" type="button" data-pub-filter-type="{{ t }}" aria-pressed="false">{{ t | capitalize }}</button>
{%- endfor -%}
</div>
<div class="pub-toolbar__row">
<label class="pub-toolbar__select">Member
<select data-pub-filter-member>
<option value="">All members</option>
{%- for p in academics -%}<option value="{{ p.id }}">{{ p.name }}</option>{%- endfor -%}
</select>
</label>
<label class="pub-toolbar__check"><input type="checkbox" data-pub-selected> Selected only</label>
{%- for layer in site.data.research.layers -%}{%- for topic in layer.topics -%}
<button class="chip chip--{{ layer.id }}" type="button" data-pub-topic="{{ topic.id }}" aria-pressed="true" hidden title="Remove topic filter">Topic: {{ topic.name }} ×</button>
{%- endfor -%}{%- endfor -%}
<span class="pub-toolbar__count meta" data-pub-count aria-live="polite">{{ pubs.size }} publications</span>
<button class="chip chip--link" type="button" data-pub-reset hidden>Clear filters</button>
</div>
</div>

<nav class="year-nav" aria-label="Jump to year"><span class="chip-row__label">Year</span>{% for y in years %}<a href="#y{{ y }}">{{ y }}</a>{% endfor %}</nav>

<div class="pub-list" data-pub-list>
{%- for year in years -%}
{%- assign in_year = pubs | where: "year", year -%}
{%- assign featured = in_year | where: "selected", true -%}
{%- assign others = in_year | where_exp: "p", "p.selected != true" -%}
<section class="pub-year" data-pub-year="{{ year }}">
<h2 class="year" id="y{{ year }}">{{ year }}<span class="count" data-year-count>{{ in_year.size }}</span></h2>
{%- for pub in featured -%}{% include pub-item.html pub=pub member_names=member_names %}{%- endfor -%}
{%- for pub in others -%}{% include pub-item.html pub=pub member_names=member_names %}{%- endfor -%}
</section>
{%- endfor -%}
</div>

<p class="pub-empty" data-pub-empty hidden>No publications match these filters. <button class="chip chip--link" type="button" data-pub-reset>Clear filters</button></p>

<p class="pub-note">RISE members are shown in bold and selected papers carry a red mark. This list covers 2022 onward; complete records are on each member's DBLP and Google Scholar profiles, linked from the <a href="{{ '/people/' | relative_url }}">People</a> page.</p>
