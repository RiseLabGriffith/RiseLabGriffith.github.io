---
title: Secure and Auditable AI Agents
date: 2026-09-06
summary: Finding, measuring and containing the security risks of LLM agents and their skill and tool ecosystems, so that agents acting on behalf of people and organisations can be trusted and audited.
kind: direction
status: active
layers: [I, E, R]
topics: [llm-agent-security, engineering-toolchains]
members: [yi-liu, leo-zhang, yanjun-zhang, wei-song, zhihao-chen]
lead: Dr Yi Liu
featured: false
order: 1
pub_query: topic=llm-agent-security
---

LLM agents now read email, browse the web, run code and call tools through skill marketplaces and protocols such as the Model Context Protocol. Every one of those channels is an attack surface: a malicious skill can exfiltrate credentials, a poisoned document can inject instructions, and an over-permissive tool can turn a helpful assistant into an insider threat.

This direction combines our work on jailbreak and prompt-injection attacks, large-scale empirical studies of agent skill ecosystems, and defences that operate at the boundary between the model and the world.

**What we are building**

- Measurement of the agent skill supply chain, from vulnerable skills at scale to deliberately malicious ones and credential leakage in agent workflows.
- Detection methods that recognise malicious or unsafe skills, tools and protocol integrations before they run.
- Permission models, runtime monitors and audit trails that keep agent actions within policy and make them reviewable after the fact.
- Benchmarks and red-team pipelines, shared with the [Continuous Assurance](/projects/continuous-assurance-red-team/) direction, so defences are evaluated under realistic attacks.

The work spans the I layer (defending intelligent systems), the E layer (deployable controls and monitoring) and the R layer (accountability and transparency of agent behaviour).
