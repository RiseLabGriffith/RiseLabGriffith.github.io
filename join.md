---
title: Join Us
permalink: /join/
description: PhD scholarships, postdoctoral and visiting positions, student projects and industry partnerships at RISE Lab, Griffith University.
headline: Study, research or partner with RISE
intro: Students, researchers and partners whose interests touch any of the four RISE layers are welcome. Open positions come first; the sections below explain each pathway.
---

{%- assign openings = site.data.openings | where: "open", true -%}
{%- assign email = site.data.site.email -%}

{%- if openings.size > 0 -%}
<section class="chapter chapter--open" id="openings">
<div class="rail"><h2>Open positions<span class="count">{{ openings.size }}</span></h2></div>
<div class="chapter__body">
<div class="openings">
{%- for o in openings -%}
<article class="opening card">
{%- case o.kind -%}{%- when "phd" -%}{%- assign kind_label = "PhD" -%}{%- when "postdoc" -%}{%- assign kind_label = "Postdoc" -%}{%- when "visiting" -%}{%- assign kind_label = "Visiting" -%}{%- when "honours" -%}{%- assign kind_label = "Honours and capstone" -%}{%- when "masters" -%}{%- assign kind_label = "Masters" -%}{%- when "intern" -%}{%- assign kind_label = "Internship" -%}{%- else -%}{%- assign kind_label = o.kind | capitalize -%}{%- endcase -%}
<p class="opening__kind label">{{ kind_label }}</p>
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
</div>
</section>
{%- endif -%}

<section class="chapter" id="phd">
<div class="rail"><h2>PhD and MPhil</h2></div>
<div class="chapter__body">
<p>Each candidate has a principal supervisor from RISE and usually a second supervisor from another layer, so projects cross the framework. To apply, email the member whose work best matches your interests with:</p>
<ul class="check-list">
<li>a CV with your degrees, results and any publications;</li>
<li>academic transcripts (a GPA above 80 out of 100 is typical for scholarship success);</li>
<li>an English test result, if English is not your first language;</li>
<li>a one-page statement of the problem you want to work on and why it fits RISE;</li>
<li>links to code, papers or a thesis you are proud of.</li>
</ul>
<div class="scholarships">
<p class="label">Scholarships</p>
<ul>
<li><strong>GUPRS</strong> Griffith University Postgraduate Research Scholarship, three rounds a year; the August round accepts international applicants.</li>
<li><strong>GUIPRS</strong> Griffith University International Postgraduate Research Scholarship, a tuition scholarship usually paired with GUPRS.</li>
<li><strong>CSC–Griffith</strong> China Scholarship Council and Griffith joint funding; the Griffith stage normally opens in November.</li>
<li><strong>AUHEPS</strong> Australian University Honours Entry Postgraduate Research Scholarship for recent Griffith honours graduates.</li>
<li><strong>Industry PhD</strong> Griffith Industry PhD and National Industry PhD Program places co-designed with partners, including CSIRO.</li>
</ul>
<p class="meta">Scholarship rules change; check the Griffith Graduate Research School for current conditions.</p>
</div>
</div>
</section>

<section class="chapter" id="postdocs">
<div class="rail"><h2>Postdocs and fellows</h2></div>
<div class="chapter__body">
<p>Research fellow positions are advertised on the Griffith careers site when funded projects open. If you have an externally funded fellowship idea that fits a RISE layer, contact the relevant member well before the scheme deadline so we can develop it together.</p>
</div>
</section>

<section class="chapter" id="visiting">
<div class="rail"><h2>Visiting researchers</h2></div>
<div class="chapter__body">
<p>RISE members host visiting academics, visiting PhD students and China Scholarship Council scholars, typically for six to twelve months. Email your proposed host with a CV, a short plan for the visit and your funding arrangement.</p>
</div>
</section>

<section class="chapter" id="students">
<div class="rail"><h2>Honours and capstone</h2></div>
<div class="chapter__body">
<p>Griffith students can complete honours theses, Masters research projects and capstone projects with RISE members, often linked to funded work on secure AI for energy systems, content authenticity, agent security tooling and applied cryptography. Projects are listed each trimester, and you are welcome to propose your own.</p>
</div>
</section>

<section class="chapter" id="partners">
<div class="rail"><h2>Industry and government</h2></div>
<div class="chapter__body">
<p>RISE co-designs research with partners and turns it into deployable methods and guidance. We evaluate the security of software, infrastructure and AI-enabled systems, build demonstrators, and co-supervise industry PhD candidates on your problems.</p>
<ul class="check-list">
<li>Adversarial evaluation and red-teaming of AI models, agents and software.</li>
<li>Privacy-preserving analytics and secure computation across organisations.</li>
<li>Cryptographic and post-quantum protocol design and review.</li>
<li>Supply-chain, provenance and content-authenticity assurance.</li>
<li>Joint grant proposals, industry PhDs and student projects.</li>
</ul>
</div>
</section>

<section class="chapter contact" id="contact">
<div class="rail"><h2>Contact</h2></div>
<div class="chapter__body">
<div class="contact__grid">
<div>
<p class="label">Email</p>
<p><a href="mailto:{{ email }}">{{ email }}</a><br><span class="meta">Lab director, until a shared lab mailbox is set up</span></p>
<p class="label">Online</p>
<p><a href="{{ site.data.site.github }}" rel="noopener">GitHub</a><br><a href="{{ site.data.site.school_url }}" rel="noopener">School of ICT</a></p>
</div>
<div>
<p class="label">Gold Coast campus</p>
<p>{{ site.data.site.school }}<br>{{ site.data.site.address_gc }}<br><a href="https://www.google.com/maps/search/?api=1&query=Griffith+University+Gold+Coast+campus+Parklands+Drive+Southport" rel="noopener">Map</a></p>
<p class="label">Nathan campus</p>
<p>{{ site.data.site.address_nathan }}<br><a href="https://www.google.com/maps/search/?api=1&query=Griffith+University+Nathan+campus+170+Kessels+Road" rel="noopener">Map</a></p>
</div>
</div>
</div>
</section>
