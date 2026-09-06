---
title: About
permalink: /about/
description: About RISE Lab, a researcher-led cybersecurity lab in the School of ICT at Griffith University, its vision, why it matters and how it works.
eyebrow: About
headline: A researcher-led home for cybersecurity research
intro: RISE, the Responsible, Intelligent and Secure Engineering Lab, brings together cyber defence, applied cryptography, privacy-preserving technologies, trustworthy AI and secure software engineering in the School of Information and Communication Technology at Griffith University.
---

{%- assign layers = site.data.research.layers -%}
{%- assign academics = site.data.people | where_exp: "p", "p.role == 'director' or p.role == 'academic'" -%}
{%- assign topic_count = 0 -%}{%- for layer in layers -%}{%- assign topic_count = topic_count | plus: layer.topics.size -%}{%- endfor -%}

<section class="about-section" id="vision">
<p class="eyebrow">Vision</p>
<h2>Intelligent systems that can be adopted with confidence</h2>
<p class="about-lede">RISE envisions a future in which intelligent systems can be adopted with confidence because responsibility, security, privacy and assurance are engineered across their full lifecycle. We pursue that vision through four connected commitments, one for each layer of the RISE framework.</p>
<div class="commitments">
<article class="card rail-R commitment">
<p class="commitment__letter text-R" aria-hidden="true">R</p>
<h3>Responsible and resilient cybersecurity</h3>
<p>Translate responsibility, governance and resilience objectives into measurable security requirements, risk controls and recovery capabilities.</p>
</article>
<article class="card rail-I commitment">
<p class="commitment__letter text-I" aria-hidden="true">I</p>
<h3>Intelligent cyber defence</h3>
<p>Develop threat intelligence, security analytics and carefully governed automation for prevention, detection, response and recovery.</p>
</article>
<article class="card rail-S commitment">
<p class="commitment__letter text-S" aria-hidden="true">S</p>
<h3>Secure and privacy-preserving foundations</h3>
<p>Create practical cryptographic and privacy-enhancing technologies that enable valuable computation and collaboration without unnecessary exposure of sensitive data, models or intellectual property.</p>
</article>
<article class="card rail-E commitment">
<p class="commitment__letter text-E" aria-hidden="true">E</p>
<h3>Engineering, evaluation and continuous operation</h3>
<p>Establish rigorous methods, tools, benchmarks and lifecycle practices for testing, verifying, deploying and monitoring trustworthy intelligent systems in real-world settings.</p>
</article>
</div>
<p class="about-more"><a class="button button--ghost" href="{{ '/research/' | relative_url }}">See the framework and all {{ topic_count }} research topics</a></p>
</section>

<section class="about-section" id="why">
<p class="eyebrow">Why RISE matters</p>
<h2>Security is a property of the whole lifecycle</h2>
<div class="about-columns">
<p>Cybersecurity cannot be achieved through isolated technical controls. A system may use strong encryption yet remain vulnerable because of insecure software, compromised identities, misconfigured infrastructure, malicious dependencies or a weak supply chain. A mechanism that is sound on paper has little value unless it can be implemented, tested, deployed and maintained in a complex operational environment.</p>
<p>AI adds a new dimension. AI-enabled systems are woven into critical services, software development and organisational decisions, and they bring their own vulnerabilities: adversarial manipulation, privacy leakage, unreliable behaviour, insecure agent actions and limited transparency. Trustworthy AI is therefore part of modern cybersecurity. Intelligent systems must be secure, privacy-preserving, robust, explainable and accountable, not only accurate.</p>
<p>Modern digital ecosystems span cloud platforms, distributed data, software supply chains, connected devices and autonomous components, and an adversary can strike at any stage. Security has to extend beyond prevention to continuous risk assessment, detection, response, recovery and adaptation. RISE exists to connect those pieces: foundational research on one side, deployable methods and operational assurance on the other.</p>
</div>
</section>

<section class="about-section" id="how">
<p class="eyebrow">How we work</p>
<h2>Researcher-led, voluntary and open</h2>
<div class="about-columns about-columns--list">
<div>
<p>RISE is a collaborative, researcher-led initiative rather than a separately resourced organisational unit. Participation is voluntary and based on shared interests. Members keep their own research identities, groups and projects, and gain a shared framework, a common profile, joint supervision and shared infrastructure.</p>
<p>The lab is inclusive by design. Academics, research fellows, HDR students, visiting researchers and jointly supervised students at partner institutions all take part, and new members whose work touches any of the four layers are welcome.</p>
</div>
<ul class="how-list">
<li><strong>Research excellence.</strong> Collaborative publications, competitive grants and challenge-led projects that demonstrate the RISE lifecycle framework.</li>
<li><strong>HDR training.</strong> Cross-supervision, reading groups, seminars, technical workshops, shared datasets and tools, and industry-relevant problems.</li>
<li><strong>Engagement.</strong> Co-designed research with industry and government, security and assurance evaluations, demonstrators and deployable guidance.</li>
<li><strong>Infrastructure.</strong> Reusable benchmarks, testbeds, cryptographic and privacy toolkits, red-team environments and evaluation pipelines, released openly where possible.</li>
<li><strong>Community.</strong> Seminars and events, visiting researchers, contributions to standards and policy, and communication of outcomes to technical and public audiences.</li>
</ul>
</div>
</section>

<section class="about-section" id="collaboration">
<p class="eyebrow">Collaboration across the School</p>
<h2>A cybersecurity perspective on intelligent systems</h2>
<p class="about-lede">RISE studies AI-enabled systems from a cybersecurity perspective. AI can be a target that must be protected, a source of new cyber risks, or a tool that supports cyber defence; developing general AI capability is not the lab's purpose. That makes RISE a natural partner for the School's AI-centred and health-centred research initiatives: they contribute machine-learning and domain expertise, and RISE contributes adversarial evaluation, cryptographic protection, privacy engineering, secure integration and operational assurance. Researchers collaborate across initiatives wherever a project benefits from complementary expertise.</p>
</section>

<section class="about-section about-facts" id="at-a-glance">
<p class="eyebrow">At a glance</p>
<dl class="facts facts--inline">
<dt>Established</dt><dd>2026, School of Information and Communication Technology, Griffith University</dd>
<dt>Director</dt><dd>{% assign director = site.data.people | where: "role", "director" | first %}<a href="{{ '/people/#' | append: director.id | relative_url }}">{{ director.title }} {{ director.name }}</a></dd>
<dt>Academic members</dt><dd>{{ academics.size }}, spanning trustworthy AI, applied cryptography, privacy-preserving computation, LLM and agent security and secure software engineering</dd>
<dt>Framework</dt><dd>Four layers (R, I, S, E) and {{ topic_count }} research topics across a five-stage security lifecycle</dd>
<dt>Campuses</dt><dd>{{ site.data.site.address_gc }}; {{ site.data.site.address_nathan }}</dd>
</dl>
</section>
