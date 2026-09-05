---
title: Home
permalink: /
---

<section class="hero"><div class="hero-inner">
  <div>
    <p class="eyebrow">Responsible · Intelligent · Secure Engineering</p>
    <h1>RISE Lab</h1>
    <p class="hero-lead">Engineering secure, private and resilient intelligent systems across the cybersecurity lifecycle.</p>
    <p class="hero-lead">RISE is a researcher-led cybersecurity initiative at Griffith University, connecting cyber defence, applied cryptography, privacy-preserving technologies and secure software engineering.</p>
    <p class="button-row"><a class="button" href="{{ '/research/' | relative_url }}">Explore our research</a><a class="button secondary" href="{{ '/people/' | relative_url }}">Meet the team</a></p>
  </div>
  <aside class="news-panel" aria-labelledby="news-title">
    <div class="news-heading"><h2 id="news-title">Latest News</h2><span>Updates</span></div>
    <div class="news-feed" tabindex="0" aria-label="Scrollable lab news">
      {% for item in site.data.news %}<article class="news-item"><time datetime="{{ item.date | date: '%Y-%m-%d' }}">{{ item.date | date: "%B %Y" }}</time><h3>{{ item.title }}</h3><p>{{ item.text }}</p></article>{% endfor %}
    </div>
  </aside>
</div></section>

<section class="home-intro" markdown="1">

## Cybersecurity across the full system lifecycle

RISE connects responsible and resilient cybersecurity, intelligent cyber defence, secure and privacy-preserving foundations, and continuous engineering assurance. Use the six sections above to explore our research, people and opportunities.

</section>

