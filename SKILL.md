---
name: genpark-personal-agent-cardiac-pulse-arrival-time-pat-pwt-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for evaluating dual-sensor Pulse Arrival Time (PAT), Pulse Transit Time (PTT), pulse wave velocity, and arterial compliance.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Dual-Sensor Pulse Arrival Time (PAT / PTT) Skill

A sovereign personal agent capability for assessing arterial vascular elasticity, decomposing pulse arrival latency from cardiac pre-ejection period (PEP), and deriving cuffless pulse wave velocity (PWV).

## Core Capabilities
- **PAT to PTT Decomposition**: Subtacts electromechanical delay (PEP) to extract pure arterial transit time.
- **Pulse Wave Velocity (PWV)**: Derives arterial wave propagation speed (m/s) without inflating pressure cuffs.
- **Arterial Compliance Score**: 0-100 index rating vascular wall elasticity and resistance to pulsatile shear stress.
- **Cardiovascular Lifestyle Guidance**: Actionable recommendations on Zone 2 conditioning and sodium/potassium moderation.

## Fast Invocation
```python
from client import PulseArrivalTimeClient

client = PulseArrivalTimeClient()
res = client.evaluate_pulse_transit(
    pat_ms=215.0,
    pre_ejection_period_ms=85.0,
    arterial_path_length_m=0.82
)
print("PTT:", res["pulse_transit_time_ptt_ms"], "ms")
print("PWV:", res["pulse_wave_velocity_pwv_m_s"], "m/s")
print("Compliance Score:", res["arterial_compliance_score"])
```
