# Dual-Sensor Pulse Arrival Time (PAT / PTT) Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of dual-sensor Pulse Arrival Time (PAT), Pulse Transit Time (PTT), pulse wave velocity (PWV), and arterial elasticity.

```mermaid
flowchart TD
    ECG_R["ECG R-Wave Peak Timestamp"] --> DualSync["Time Difference Integration (PAT)"]
    PPG_Foot["Distal PPG Pulse Foot Timestamp"] --> DualSync
    DualSync --> PEP_Sub["PEP Subtraction (PTT = PAT - PEP)"]
    PEP_Sub --> PWV_Calc["Pulse Wave Velocity & Moens-Korteweg Modeling"]
    PWV_Calc --> ComplianceScore["Arterial Vascular Compliance Engine"]
    ComplianceScore --> Agent["OpenClaw / Hermes Personal Agent Actions"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Hemodynamic Moens-Korteweg Principles**: Implements validated equations linking pulse wave transit to arterial wall stiffness.
- **Continuous Cuffless Cardiovascular Monitoring**: Enables continuous beat-to-beat vascular tone assessment.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import PulseArrivalTimeClient

client = PulseArrivalTimeClient()
result = client.evaluate_pulse_transit(
    pat_ms=215.0,
    pre_ejection_period_ms=85.0,
    arterial_path_length_m=0.82
)
print("Pulse Wave Velocity:", result["pulse_wave_velocity_pwv_m_s"], "m/s")
print("Classification:", result["classification"])
```

## License
Apache-2.0
