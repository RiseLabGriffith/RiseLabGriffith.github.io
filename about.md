---
title: About
permalink: /about/
description: About RISE Lab, a researcher-led cybersecurity lab in the School of ICT at Griffith University, its vision, why it matters and how it works.
headline: A researcher-led home for cybersecurity research
intro: RISE brings cyber defence, applied cryptography, privacy-preserving technologies, trustworthy AI and secure software engineering together in one lab at Griffith University.
---

{%- assign layers = site.data.research.layers -%}
{%- assign academics = site.data.people | where_exp: "p", "p.role == 'director' or p.role == 'academic'" -%}
{%- assign topic_count = 0 -%}{%- for layer in layers -%}{%- assign topic_count = topic_count | plus: layer.topics.size -%}{%- endfor -%}

<section class="chapter chapter--open" id="vision">
<div class="rail"><h2>Vision</h2></div>
<div class="chapter__body">
<p class="statement">Intelligent systems that can be adopted with confidence, because security, privacy and assurance are engineered across their whole lifecycle.</p>
<p>Each layer of the RISE framework is a commitment.</p>
<ul class="commitments">
{%- for layer in layers -%}
<li class="commitment layer-{{ layer.id }}">
<p class="commitment__letter" aria-hidden="true">{{ layer.letter }}</p>
<div><h3>{{ layer.name }}</h3><p>{{ layer.tagline }}</p></div>
</li>
{%- endfor -%}
</ul>
<p><a href="{{ '/research/' | relative_url }}">The framework and all {{ topic_count }} research topics</a></p>
</div>
</section>

<section class="chapter" id="why">
<div class="rail"><h2>Why RISE</h2></div>
<div class="chapter__body">
<p class="statement">Security is a property of the whole lifecycle, not of any single control.</p>
<p>Strong encryption does not help when the software around it is insecure, an identity is compromised or a dependency is malicious. AI adds new surfaces of its own, from adversarial manipulation and privacy leakage to unsafe agent actions, so trustworthy AI is now part of cybersecurity. RISE connects foundational research with deployable methods and operational assurance, so that protections keep working after a system leaves the lab.</p>
</div>
</section>

<section class="chapter" id="how">
<div class="rail"><h2>How we work</h2></div>
<div class="chapter__body">
<p>RISE is a researcher-led initiative rather than a separately resourced unit. Members keep their own research identities, groups and projects, and gain a shared framework, joint supervision and shared infrastructure. Academics, research fellows, PhD students, visitors and jointly supervised students at partner institutions all take part, and anyone whose work touches one of the four layers is welcome. The lab studies AI from a security perspective, as a target, a risk and a tool, which makes it a natural partner for the School's AI and health initiatives.</p>
<ul class="how-list">
<li><strong>Research</strong> Collaborative publications, competitive grants and challenge-led projects that demonstrate the lifecycle framework.</li>
<li><strong>PhD training</strong> Cross-supervision, reading groups, seminars, shared datasets and tools, and industry-relevant problems.</li>
<li><strong>Engagement</strong> Co-designed research with industry and government, security and assurance evaluations, and deployable guidance.</li>
<li><strong>Infrastructure</strong> Benchmarks, testbeds, cryptographic and privacy toolkits and red-team environments, released openly where possible.</li>
<li><strong>Community</strong> Seminars and visitors, contributions to standards and policy, and communication to technical and public audiences.</li>
</ul>
</div>
</section>

<section class="chapter" id="at-a-glance">
<div class="rail"><h2>At a glance</h2></div>
<div class="chapter__body">
<dl class="facts facts--inline">
<dt>Established</dt><dd>2026, School of Information and Communication Technology, Griffith University</dd>
<dt>Director</dt><dd>{% assign director = site.data.people | where: "role", "director" | first %}<a href="{{ '/people/#' | append: director.id | relative_url }}">{{ director.title }} {{ director.name }}</a></dd>
<dt>Academic members</dt><dd>{{ academics.size }}, across trustworthy AI, applied cryptography, privacy-preserving computation, LLM and agent security and secure software engineering</dd>
<dt>Framework</dt><dd>Four layers and {{ topic_count }} research topics across a five-stage security lifecycle</dd>
<dt>Campuses</dt><dd>{{ site.data.site.address_gc }}<br>{{ site.data.site.address_nathan }}</dd>
</dl>
</div>
</section>
