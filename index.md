---
layout: default
title: RISE Lab
permalink: /
description: RISE Lab is a researcher-led cybersecurity lab in the School of ICT at Griffith University, engineering responsible, intelligent and secure systems across the full lifecycle.
body_class: home
---

{%- assign layers = site.data.research.layers -%}
{%- assign people = site.data.people -%}
{%- assign academics = people | where_exp: "p", "p.role == 'director' or p.role == 'academic'" -%}
{%- assign students = people | where: "role", "student" -%}
{%- assign topic_count = 0 -%}
{%- for layer in layers -%}{%- assign topic_count = topic_count | plus: layer.topics.size -%}{%- endfor -%}
{%- assign selected_pubs = site.data.publications | where: "selected", true | sort: "year" | reverse -%}
{%- assign featured_projects = site.projects | where: "featured", true | sort: "order" -%}
{%- assign latest_news = site.data.news -%}

<section class="hero">
  <div class="hero__line" aria-hidden="true"></div>
  <div class="container hero__inner">
    <p class="eyebrow">Responsible · Intelligent · Secure Engineering</p>
    <h1 class="wordmark" aria-label="RISE Lab">
      <span class="wordmark__word" aria-hidden="true">
        {%- for layer in layers -%}
        <a class="wordmark__letter" href="{{ '/research/#layer-' | append: layer.id | relative_url }}" data-letter="{{ layer.letter }}" tabindex="-1"><span class="wordmark__glyph">{{ layer.letter }}</span><span class="wordmark__phrase">{{ layer.short }}</span></a>
        {%- endfor -%}
      </span>
      <span class="wordmark__lab" aria-hidden="true">Lab</span>
    </h1>
    <p class="hero__hint meta" aria-hidden="true">Hover a letter to see its layer</p>
    <p class="hero__vision">A future in which intelligent systems can be adopted with confidence, because responsibility, security, privacy and assurance are engineered across their full lifecycle.</p>
    <p class="hero__where">A researcher-led cybersecurity lab in the School of Information and Communication Technology, Griffith University.</p>
    <div class="button-row hero__buttons">
      <a class="button" href="{{ '/research/' | relative_url }}">Explore the research</a>
      <a class="button button--ghost" href="{{ '/join/' | relative_url }}">Join us</a>
    </div>
  </div>
</section>

<section class="section section--tight home-stack">
  <div class="container">
    <div class="home-section__head">
      <p class="eyebrow">The RISE framework</p>
      <h2>Four layers across one lifecycle</h2>
      <p class="home-section__lede">Responsible and resilient cybersecurity, intelligent cyber defence and secure foundations feed an engineering layer that turns them into deployed, continuously assured systems. Open a layer to see its keywords and research topics.</p>
    </div>
    {% include framework-stack.html mode="compact" %}
    <p class="home-section__more"><a href="{{ '/research/' | relative_url }}">Explore all {{ topic_count }} research topics</a></p>
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

<section class="section home-news">
  <div class="container">
    <div class="home-section__head home-section__head--row">
      <div><p class="eyebrow">News</p><h2>Latest news</h2></div>
      <a class="home-section__link" href="{{ '/news/' | relative_url }}">All news and events</a>
    </div>
    <div class="news-cards">
      {%- for n in latest_news limit: 3 -%}
      {%- assign kind = n.kind | default: "general" -%}
      <article class="news-card card rail-{% case kind %}{% when 'paper' %}I{% when 'grant' %}E{% when 'people' %}S{% else %}R{% endcase %}">
        <p class="news-item__meta"><time datetime="{{ n.date | date: '%Y-%m-%d' }}">{% if n.precision == "year" %}{{ n.date | date: "%Y" }}{% else %}{{ n.date | date: "%B %Y" }}{% endif %}</time> <span class="news-item__kind">{{ kind }}</span></p>
        <h3 class="news-card__title">{% if n.link %}<a href="{{ n.link | relative_url }}">{{ n.title }}</a>{% else %}<a href="{{ '/news/' | relative_url }}">{{ n.title }}</a>{% endif %}</h3>
        <p class="news-card__text">{{ n.text | truncatewords: 32 }}</p>
      </article>
      {%- endfor -%}
    </div>
  </div>
</section>

<section class="section section--tight home-pubs">
  <div class="container">
    <div class="home-section__head home-section__head--row">
      <div><p class="eyebrow">Publications</p><h2>Selected publications</h2></div>
      <a class="home-section__link" href="{{ '/publications/?selected=1' | relative_url }}">All selected publications</a>
    </div>
    <div class="pub-list pub-list--compact">
      {%- for pub in selected_pubs limit: 6 -%}{% include pub-item.html pub=pub %}{%- endfor -%}
    </div>
    <p class="home-section__more"><a href="{{ '/publications/' | relative_url }}">Browse all {{ site.data.publications.size }} publications</a></p>
  </div>
</section>

<section class="section home-projects">
  <div class="container">
    <div class="home-section__head home-section__head--row">
      <div><p class="eyebrow">Projects</p><h2>Featured projects</h2></div>
      <a class="home-section__link" href="{{ '/projects/' | relative_url }}">All projects</a>
    </div>
    <div class="card-grid">
      {%- for pr in featured_projects limit: 3 -%}{% include project-card.html project=pr %}{%- endfor -%}
    </div>
  </div>
</section>

<section class="cta">
  <div class="container cta__inner">
    <div>
      <p class="eyebrow eyebrow--onnavy">Join RISE</p>
      <h2 class="cta__title">Build secure, private and resilient intelligent systems with us</h2>
      <p class="cta__text">PhD scholarships, postdoctoral and visiting positions, honours and capstone projects, and partnerships with industry and government.</p>
    </div>
    <div class="button-row cta__buttons">
      <a class="button" href="{{ '/join/' | relative_url }}">Opportunities</a>
      <a class="button button--onnavy" href="mailto:{{ site.data.site.email }}">Email the lab</a>
    </div>
  </div>
</section>
