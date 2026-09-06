---
title: Continuous Assurance and Red-Team Pipelines
summary: Reusable benchmarks, automated penetration testing, fuzzing and adversarial evaluation that measure whether software, networks and AI systems stay secure as they change.
kind: direction
status: active
layers: [E, R, I]
topics: [evaluation-red-team, evaluation-verification-assurance, operational-assurance]
members: [yi-liu, wei-song, leo-zhang, yanjun-zhang]
lead: Dr Yi Liu and Dr Wei Song
order: 5
pub_query: topic=evaluation-red-team
---

Security is not a property you establish once. Dependencies update, models are fine-tuned, prompts change and attackers adapt. RISE builds evaluation pipelines that run continuously and produce evidence an organisation can act on.

**Components**

- LLM-driven penetration testing, starting from [PentestGPT](/projects/pentestgpt/) and extending to evaluation of what makes an agent effective at real-world testing.
- Fuzzing and program analysis for memory-safety and protocol vulnerabilities, including LLM-guided greybox fuzzing.
- Safety and robustness benchmarks for language, vision-language and video models: jailbreak resistance, over-refusal, toxic-prompt detection, hallucination and harmful-content surfacing.
- Adversarial evaluation of learning systems against poisoning, backdoor and evasion attacks, building on the R layer's defences.
- Assurance cases that combine these results into measurable, reproducible evidence.

The pipelines are designed to plug into development and operations workflows so that regressions are caught before deployment.
