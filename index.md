---
layout: default
title: RISE Lab
permalink: /
description: RISE Lab is a researcher-led cybersecurity lab at Griffith University engineering responsible, intelligent and secure systems across the full lifecycle.
body_class: home
---

{%- assign layers = site.data.research.layers -%}
{%- assign people = site.data.people -%}
{%- assign academics = people | where_exp: "p", "p.role == 'director' or p.role == 'academic'" -%}
{%- assign students = people | where: "role", "student" -%}
{%- assign topic_count = 0 -%}
{%- for layer in layers -%}{%- assign topic_count = topic_count | plus: layer.topics.size -%}{%- endfor -%}
{%- assign featured_projects = site.projects | where: "featured", true | sort: "order" -%}

{%- comment -%} Selected publications for the home page: the newest selected paper of each academic, then the newest remaining ones, six in all. {%- endcomment -%}
{%- assign selected_pubs = site.data.publications | where: "selected", true | sort: "year" | reverse -%}
{%- assign home_pubs = "" | split: "" -%}
{%- for a in academics -%}
  {%- assign picked = false -%}
  {%- for pub in selected_pubs -%}
    {%- if picked == false and pub.members contains a.id -%}
      {%- assign dup = false -%}
      {%- for h in home_pubs -%}{%- if h.id == pub.id -%}{%- assign dup = true -%}{%- endif -%}{%- endfor -%}
      {%- if dup == false -%}{%- assign home_pubs = home_pubs | push: pub -%}{%- assign picked = true -%}{%- endif -%}
    {%- endif -%}
  {%- endfor -%}
{%- endfor -%}
{%- for pub in selected_pubs -%}
  {%- if home_pubs.size < 6 -%}
    {%- assign dup = false -%}
    {%- for h in home_pubs -%}{%- if h.id == pub.id -%}{%- assign dup = true -%}{%- endif -%}{%- endfor -%}
    {%- if dup == false -%}{%- assign home_pubs = home_pubs | push: pub -%}{%- endif -%}
  {%- endif -%}
{%- endfor -%}

<section class="hero">
  <div class="container hero__grid">
    <div class="hero__copy">
      <h1 class="wordmark" aria-label="RISE Lab">
        <span class="wordmark__word" aria-hidden="true">
          {%- for layer in layers -%}
          <a class="wordmark__letter" href="{{ '/research/#layer-' | append: layer.id | relative_url }}" data-letter="{{ layer.letter }}" tabindex="-1"><span class="wordmark__glyph">{{ layer.letter }}</span><span class="wordmark__phrase">{{ layer.short }}</span></a>
          {%- endfor -%}
        </span>
        <span class="wordmark__lab" aria-hidden="true">Lab</span>
      </h1>
      <p class="hero__vision">Cybersecurity engineered across the whole lifecycle of intelligent systems.</p>
      <p class="hero__where">A researcher-led lab in the School of Information and Communication Technology at Griffith University, Gold Coast and Brisbane.</p>
      <div class="button-row hero__buttons">
        <a class="button" href="{{ '/research/' | relative_url }}">Explore the research</a>
        <a class="button button--ghost" href="{{ '/join/' | relative_url }}">Join the lab</a>
      </div>
    </div>
    <ul class="hero__bands" aria-label="The four RISE layers">
      {%- for layer in layers -%}
      <li class="band band--{{ layer.id }}" style="--i: {{ forloop.index0 }}"><a href="{{ '/research/#layer-' | append: layer.id | relative_url }}"><span class="band__letter" aria-hidden="true">{{ layer.letter }}</span><span class="band__name">{{ layer.name }}</span></a></li>
      {%- endfor -%}
    </ul>
  </div>
</section>

<section class="band-section home-stack">
  <div class="container chapter">
    <div class="rail">
      <h2>The RISE framework</h2>
      <p class="rail__note meta">Four layers, one lifecycle. Open a layer to see its keywords and topics.</p>
    </div>
    <div class="chapter__body">
      {% include framework-stack.html mode="compact" %}
      <p class="home-more"><a href="{{ '/research/' | relative_url }}">All {{ topic_count }} research topics</a></p>
    </div>
  </div>
</section>

<section class="stats" aria-label="RISE Lab in numbers">
  <div class="container stats__grid">
    {% include stat.html value=academics.size label="Academic members" href="/people/" %}
    {% include stat.html value=students.size label="PhD students at Griffith" href="/people/#students" %}
    {% include stat.html value=topic_count label="Research topics" href="/research/" %}
    {% include stat.html value=site.data.publications.size label="Publications since 2022" href="/publications/" %}
  </div>
</section>

<section class="band-section home-news">
  <div class="container chapter">
    <div class="rail">
      <h2>Latest news</h2>
      <a class="rail__link" href="{{ '/news/' | relative_url }}">All news and events</a>
    </div>
    <div class="chapter__body">
      <ol class="news-lines">
        {%- for n in site.data.news limit: 5 -%}{% include news-line.html item=n %}{%- endfor -%}
      </ol>
    </div>
  </div>
</section>

<section class="band-section home-people">
  <div class="container chapter">
    <div class="rail">
      <h2>People</h2>
      <p class="rail__note meta">Six academics, their PhD students, visitors and collaborators.</p>
      <a class="rail__link" href="{{ '/people/' | relative_url }}">Everyone in the lab</a>
    </div>
    <div class="chapter__body">
      <ul class="faces">
        {%- for p in academics -%}
        <li class="face">
          <a href="{{ '/people/#' | append: p.id | relative_url }}">
            <img class="face__photo" src="{{ '/assets/img/people/' | append: p.photo | relative_url }}" alt="Portrait of {{ p.name }}" width="300" height="300" loading="lazy">
            <span class="face__name">{{ p.name }}</span>
            <span class="face__role">{% if p.role == "director" %}Lab Director{% else %}{{ p.position }}{% endif %}</span>
            <span class="face__focus">{{ p.interests | slice: 0, 2 | join: ", " }}</span>
          </a>
        </li>
        {%- endfor -%}
      </ul>
    </div>
  </div>
</section>

<section class="band-section home-pubs">
  <div class="container chapter">
    <div class="rail">
      <h2>Selected publications</h2>
      <a class="rail__link" href="{{ '/publications/?selected=1' | relative_url }}">All selected publications</a>
    </div>
    <div class="chapter__body">
      <div class="pub-list pub-list--compact">
        {%- for pub in home_pubs limit: 6 -%}{% include pub-item.html pub=pub compact=true %}{%- endfor -%}
      </div>
      <p class="home-more"><a href="{{ '/publications/' | relative_url }}">Browse all {{ site.data.publications.size }} publications</a></p>
    </div>
  </div>
</section>

<section class="band-section band-section--cloud home-projects">
  <div class="container chapter">
    <div class="rail">
      <h2>Featured projects</h2>
      <a class="rail__link" href="{{ '/projects/' | relative_url }}">All projects</a>
    </div>
    <div class="chapter__body">
      <div class="card-grid">
        {%- for pr in featured_projects limit: 3 -%}{% include project-card.html project=pr %}{%- endfor -%}
      </div>
    </div>
  </div>
</section>

<section class="band-section band-section--navy cta">
  <div class="container chapter">
    <div class="rail"><h2>Join RISE</h2></div>
    <div class="chapter__body">
      <h2 class="cta__title">Study, research or partner with us</h2>
      <p class="cta__text">PhD scholarships, postdoctoral and visiting positions, honours and capstone projects, and partnerships with industry and government.</p>
      <div class="button-row cta__buttons">
        <a class="button" href="{{ '/join/' | relative_url }}">See the opportunities</a>
        <a class="button button--onnavy" href="mailto:{{ site.data.site.email }}">Email the lab</a>
      </div>
    </div>
  </div>
</section>
