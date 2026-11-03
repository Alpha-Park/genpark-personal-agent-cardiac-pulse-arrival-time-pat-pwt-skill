"""
Example Usage: Dual-Sensor Pulse Arrival Time (PAT) / Pulse Transit Time (PTT).
Demonstrates calculation of cuffless pulse wave velocity and arterial compliance.
"""

from client import PulseArrivalTimeClient


def main():
    client = PulseArrivalTimeClient()
    print("=== Pulse Arrival Time (PAT) & Arterial Compliance Demo ===")

    # Test Case 1: Healthy compliant arterial vasculature (Young adult)
    res1 = client.evaluate_pulse_transit(
        pat_ms=215.0,
        pre_ejection_period_ms=85.0,
        arterial_path_length_m=0.82
    )
    print("\nTest Case 1: Healthy Arterial Compliance")
    print(f"  Pulse Arrival Time (PAT): {res1['pulse_arrival_time_pat_ms']} ms")
    print(f"  Pre-Ejection Period (PEP): {res1['pre_ejection_period_pep_ms']} ms")
    print(f"  Pulse Transit Time (PTT): {res1['pulse_transit_time_ptt_ms']} ms")
    print(f"  Pulse Wave Velocity (PWV): {res1['pulse_wave_velocity_pwv_m_s']} m/s")
    print(f"  Compliance Score: {res1['arterial_compliance_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Arterial stiffening / high sympathetic vasoconstriction
    res2 = client.evaluate_pulse_transit(
        pat_ms=160.0,
        pre_ejection_period_ms=80.0,
        arterial_path_length_m=0.82
    )
    print("\nTest Case 2: Arterial Stiffening / Accelerated Wave")
    print(f"  PTT: {res2['pulse_transit_time_ptt_ms']} ms | PWV: {res2['pulse_wave_velocity_pwv_m_s']} m/s")
    print(f"  Compliance Score: {res2['arterial_compliance_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()
