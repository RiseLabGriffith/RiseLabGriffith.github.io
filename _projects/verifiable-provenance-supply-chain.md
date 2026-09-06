---
title: Verifiable Provenance for Software, Data and AI Supply Chains
date: 2026-09-06
summary: Cryptographic provenance, watermarking and continuous analysis that show where software, data and AI models came from, whether they were tampered with, and whether they can be trusted.
kind: direction
status: active
layers: [S, I, E]
topics: [verifiable-computation, secure-software-engineering, transparency-accountability]
members: [qinyi-li, yi-liu, wei-song, he-zhang]
featured: true
order: 4
pub_query: topic=secure-software-engineering
---

Modern systems are assembled from packages, pre-trained models, datasets and agent skills produced by people you will never meet. Supply-chain attacks exploit this: a poisoned dataset, an evil model configuration or a malicious dependency can compromise every downstream user.

This direction builds the evidence needed to trust what you run.

**Threads of work**

- Detecting malicious and vulnerable components in software and AI supply chains, from code repositories to model hubs and agent skill stores.
- Watermarking and attribution for AI-generated text, images and video, together with attacks that test how robust those watermarks really are.
- Cryptographic provenance and verifiable computation so that build, training and inference steps produce checkable evidence.
- Toolchains such as browser-accessible static analysis and LLM-guided fuzzing that make continuous supply-chain assurance practical for developers.

Outputs feed the [Digital Content Protector](/projects/digital-content-protector/) work with CSIRO Data61 and our software-assurance tooling.
