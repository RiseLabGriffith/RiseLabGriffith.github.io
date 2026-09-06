---
title: Privacy-Preserving Cyber-Threat Intelligence Sharing
summary: Letting organisations pool indicators, incidents and attack analytics without exposing the sensitive data behind them, using secure computation, differential privacy and cryptographic access control.
kind: direction
status: proposed
layers: [S, I, E]
topics: [privacy-preserving-data, secure-computation, threat-intelligence-analytics]
members: [leo-zhang, yanjun-zhang, qinyi-li]
featured: true
order: 2
pub_query: topic=privacy-preserving-data
---

Effective cyber defence depends on sharing what each organisation sees, yet the most useful signals, such as internal logs, victim details and proprietary detections, are exactly the ones organisations cannot release. The result is that threat intelligence is shared late, coarsely or not at all.

This direction designs sharing mechanisms in which privacy is guaranteed by construction rather than by trust. It draws on our work on federated and privacy-preserving learning, inference and reconstruction attacks, secure aggregation, and cryptographic protocols for authenticated, access-controlled data exchange.

**Planned demonstrator**

- A cross-organisation analytics pipeline in which indicators are matched and aggregated under secure multi-party computation or differential privacy.
- Threat-detection models trained federatedly across partners, hardened against the poisoning and inference attacks studied in the R and S layers.
- Cryptographic access control so that contributors can prove provenance and control who can query their data.

The demonstrator is planned with government and industry partners; see [Join Us](/join/#partners) if you would like to be involved.
