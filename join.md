---
title: Join Us
permalink: /join/
description: PhD scholarships, postdoctoral and visiting positions, student projects and industry partnerships at RISE Lab, Griffith University.
eyebrow: Join Us
headline: Study, research or partner with RISE
intro: We welcome students, researchers and partners whose interests touch any of the four RISE layers. Open positions are listed first; the sections below explain how to apply for each pathway.
---

{%- assign openings = site.data.openings | where: "open", true -%}
{%- assign email = site.data.site.email -%}

{%- if openings.size > 0 -%}
<section class="join-section" id="openings">
<h2>Open positions <span class="people-group__count">{{ openings.size }}</span></h2>
<div class="openings">
{%- for o in openings -%}
{%- assign primary = o.layers | first | default: "R" -%}
<article class="opening card rail-{{ primary }}">
<p class="opening__kind meta">{{ o.kind | replace: "-", " " }}</p>
<h3 class="opening__title">{% if o.link %}<a href="{{ o.link }}" rel="noopener">{{ o.title }}</a>{% else %}{{ o.title }}{% endif %}</h3>
<p class="opening__summary">{{ o.summary }}</p>
<div class="opening__foot">
{%- if o.layers %}<div class="tag-row">{% for L in o.layers %}{% include layer-tag.html letter=L %}{% endfor %}</div>{% endif -%}
{%- if o.supervisors -%}
<p class="opening__supervisors meta">With
{%- for sid in o.supervisors -%}
{%- assign sup = site.data.people | where: "id", sid | first -%}
{%- if sup %} <a href="{{ '/people/#' | append: sup.id | relative_url }}">{{ sup.name }}</a>{% unless forloop.last %},{% endunless %}{% endif -%}
{%- endfor -%}
</p>
{%- endif -%}
</div>
</article>
{%- endfor -%}
</div>
</section>
{%- endif -%}

<section class="join-section" id="phd">
<h2>PhD and MPhil</h2>
<div class="about-columns">
<div>
<p>Griffith offers PhD and MPhil degrees by research. Each candidate has a principal supervisor from RISE and usually a second RISE supervisor from another layer, so projects naturally cross the framework. Candidates take part in the lab's reading groups, seminars and demonstrator projects.</p>
<p><strong>How to apply.</strong> Email the RISE member whose work best matches your interests. A good enquiry includes:</p>
<ul class="check-list">
<li>a CV with your degrees, results and any publications;</li>
<li>academic transcripts (a GPA above 80 out of 100 is typical for scholarship success);</li>
<li>a valid English test result, if English is not your first language;</li>
<li>a one-page statement of the problem you want to work on and why it fits RISE;</li>
<li>links to code, papers or a thesis you are proud of.</li>
</ul>
</div>
<div class="card card--flat scholarships">
<p class="eyebrow">Scholarships</p>
<ul>
<li><strong>GUPRS</strong> · Griffith University Postgraduate Research Scholarship, with an expression-of-interest stage and three rounds a year; the August round accepts international applicants.</li>
<li><strong>GUIPRS</strong> · Griffith University International Postgraduate Research Scholarship, a tuition scholarship usually paired with GUPRS.</li>
<li><strong>CSC–Griffith</strong> · China Scholarship Council and Griffith University joint funding, with the Griffith stage normally opening in November.</li>
<li><strong>AUHEPS</strong> · Australian University Honours Entry Postgraduate Research Scholarship for recent Griffith honours graduates.</li>
<li><strong>Industry PhD</strong> · Griffith Industry PhD and National Industry PhD Program places co-designed with partners, including CSIRO Industry PhD projects for domestic candidates.</li>
</ul>
<p class="meta">Scholarship rules change; check the Griffith Graduate Research School for current conditions.</p>
</div>
</div>
</section>

<section class="join-section" id="postdocs">
<h2>Postdocs and research fellows</h2>
<p>Research fellow positions are advertised on the Griffith careers site when funded projects open. We also support strong candidates applying for externally funded fellowships hosted at Griffith. If you have a fellowship idea that fits a RISE layer, contact the relevant member well before the scheme deadline so we can develop it together.</p>
</section>

<section class="join-section" id="visiting">
<h2>Visiting researchers and students</h2>
<p>RISE members host visiting academics, visiting PhD students and China Scholarship Council visiting scholars, typically for six to twelve months. A visit needs a host member, a topic aligned with one of the four layers, and funding from your home institution or a scholarship scheme. Email your proposed host with a CV and a short plan for the visit.</p>
</section>

<section class="join-section" id="students">
<h2>Honours, Masters and capstone projects</h2>
<p>Griffith students can complete honours theses, Masters research projects and capstone projects with RISE members, often linked to funded projects on secure AI for energy systems, content authenticity, agent security tooling and applied cryptography. Projects are listed each trimester; you are also welcome to propose your own.</p>
</section>

<section class="join-section" id="partners">
<h2>Industry and government partnership</h2>
<div class="about-columns">
<p>RISE co-designs research with partners and turns it into deployable methods and guidance. We can carry out security and assurance evaluations of software, infrastructure and AI-enabled systems; build demonstrators that integrate privacy-preserving computation, threat analytics and continuous monitoring; and co-supervise industry PhD candidates working on your problems.</p>
<ul class="check-list">
<li>Adversarial evaluation and red-teaming of AI models, agents and software.</li>
<li>Privacy-preserving analytics and secure computation across organisations.</li>
<li>Cryptographic and post-quantum protocol design and review.</li>
<li>Supply-chain, provenance and content-authenticity assurance.</li>
<li>Joint grant proposals, industry PhDs and student projects.</li>
</ul>
</div>
</section>

<section class="join-section contact" id="contact">
<h2>Contact</h2>
<div class="contact__grid">
<div class="card card--flat">
<p class="eyebrow">Email</p>
<p><a href="mailto:{{ email }}">{{ email }}</a><br><span class="meta">Lab director, until a shared lab mailbox is established</span></p>
<p class="eyebrow">Online</p>
<p><a href="{{ site.data.site.github }}" rel="noopener">GitHub</a> · <a href="{{ site.data.site.school_url }}" rel="noopener">School of ICT</a></p>
</div>
<div class="card card--flat">
<p class="eyebrow">Gold Coast campus</p>
<p>{{ site.data.site.school }}<br>{{ site.data.site.address_gc }}<br><a href="https://www.google.com/maps/search/?api=1&query=Griffith+University+Gold+Coast+campus+Parklands+Drive+Southport" rel="noopener">Map</a></p>
<p class="eyebrow">Nathan campus</p>
<p>{{ site.data.site.address_nathan }}<br><a href="https://www.google.com/maps/search/?api=1&query=Griffith+University+Nathan+campus+170+Kessels+Road" rel="noopener">Map</a></p>
</div>
</div>
</section>
