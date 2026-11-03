"""
Dual-Sensor Pulse Arrival Time (PAT) / Pulse Transit Time (PTT) Engine.
Provides deterministic, zero-dependency modeling of electrocardiogram to photoplethysmogram
pulse arrival latency, pulse wave velocity (PWV), and arterial vascular compliance kinetics.
"""

from typing import Dict, Any, List, Optional


class PulseArrivalTimeClient:
    """
    Deterministic client for calculating Pulse Arrival Time (PAT) and Pulse Transit Time (PTT).
    Decomposes vascular transit delay from cardiac pre-ejection period (PEP) to derive
    cuffless pulse wave velocity (PWV) and arterial elasticity metrics.
    """

    def __init__(self):
        pass

    def evaluate_pulse_transit(
        self,
        pat_ms: float,
        pre_ejection_period_ms: float = 85.0,
        arterial_path_length_m: float = 0.82
    ) -> Dict[str, Any]:
        """
        Calculates PTT = PAT - PEP and PWV = distance / (PTT in seconds).
        Normative values for young/middle-aged adults:
        - PAT (ECG to finger PPG): 190 - 240 ms
        - PEP: 70 - 100 ms
        - PTT: 110 - 160 ms
        - PWV: 5.2 - 7.6 m/s
        """
        if pat_ms <= 0 or pre_ejection_period_ms <= 0 or arterial_path_length_m <= 0:
            return {"error": "PAT, PEP, and path length must be strictly positive"}

        if pat_ms <= pre_ejection_period_ms:
            return {"error": "PAT must exceed PEP to derive valid pulse transit time"}

        ptt_ms = round(pat_ms - pre_ejection_period_ms, 1)
        ptt_sec = ptt_ms / 1000.0

        pwv_m_s = round(arterial_path_length_m / ptt_sec, 2)

        # Arterial Compliance Score (0 - 100):
        # PWV 5.4 - 7.2 m/s -> 88 - 98.
        # PWV > 9.5 m/s -> < 45 (Arterial stiffening).
        if 5.4 <= pwv_m_s <= 7.2:
            score = 90.0 + min(10.0, (7.2 - pwv_m_s) * 5.0)
        elif 4.8 <= pwv_m_s < 5.4:
            score = 80.0 + ((pwv_m_s - 4.8) / 0.6) * 10.0
        elif 7.2 < pwv_m_s <= 8.5:
            score = 70.0 + ((8.5 - pwv_m_s) / 1.3) * 18.0
        elif pwv_m_s < 4.8:
            score = 75.0 - (4.8 - pwv_m_s) * 20.0
        else:
            score = max(5.0, 70.0 - (pwv_m_s - 8.5) * 22.0)

        compliance_score = round(min(100.0, max(5.0, score)), 1)

        if pwv_m_s <= 7.2:
            tier = "OPTIMAL_ARTERIAL_COMPLIANCE"
            interp = f"Flexible arterial tree with normal transit delay (PTT {ptt_ms} ms, PWV {pwv_m_s} m/s); low vascular wall stiffness."
            guidance = "Arterial compliance and buffering capacity are optimal. Sustain cardiovascular conditioning."
        elif pwv_m_s <= 8.5:
            tier = "PRESERVED_VASCULAR_ELASTICITY"
            interp = f"Standard pulse wave velocity ({pwv_m_s} m/s, PTT {ptt_ms} ms); acceptable age-adjusted arterial elasticity."
            guidance = "Normal vascular tone. Maintain dietary hydration, electrolyte balance, and regular aerobic exercise."
        elif pwv_m_s <= 10.0:
            tier = "BORDERLINE_ARTERIAL_STIFFENING"
            interp = f"Shortened pulse transit time (PTT {ptt_ms} ms, PWV {pwv_m_s} m/s); points to elevated sympathetic vasoconstriction or vascular stiffness."
            guidance = "Elevated arterial wave speed. Incorporate daily 30-minute brisk walking and monitor resting blood pressure."
        else:
            tier = "ELEVATED_VASCULAR_STIFFNESS_PULSATILITY"
            interp = f"Significantly elevated PWV ({pwv_m_s} m/s > 10.0 m/s); indicates marked arterial wall rigidity and transmission of high pulsatile stress."
            guidance = "High arterial stiffness detected. Recommend clinical cuff-based ambulatory blood pressure assessment and formal cardiology review."

        return {
            "pulse_arrival_time_pat_ms": pat_ms,
            "pre_ejection_period_pep_ms": pre_ejection_period_ms,
            "pulse_transit_time_ptt_ms": ptt_ms,
            "arterial_path_length_m": arterial_path_length_m,
            "pulse_wave_velocity_pwv_m_s": pwv_m_s,
            "arterial_compliance_score": compliance_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
