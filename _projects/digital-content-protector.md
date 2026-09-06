---
title: Digital Content Protector
date: 2026-09-06
summary: Deployable verification of watermarks in AI-generated and AI-edited content, developed with CSIRO Data61 to help platforms and users tell authentic media from manipulated media.
kind: software
status: active
layers: [R, S, E]
topics: [transparency-accountability, verifiable-computation]
members: [wei-song]
lead: Dr Wei Song
partners: [CSIRO Data61]
order: 2
pub_query: q=watermark
---

Watermarks are the leading proposal for labelling AI-generated images, video and text, but a watermark is only useful if it survives real-world editing and if verification is available where content is consumed.

Digital Content Protector (DCP) is a content-verification system built with CSIRO Data61. It combines:

- verification services that check embedded watermarks in images and video and report confidence to the user;
- robustness testing informed by our query-free, black-box attacks on deepfake watermarking defences, so that the deployed checks are measured against the strongest known adversaries;
- integration points for platforms, newsrooms and regulators that need provenance evidence at scale.

DCP is part of RISE's [verifiable provenance](/projects/verifiable-provenance-supply-chain/) direction and complements our research on watermarking for large language models.
