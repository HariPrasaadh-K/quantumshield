"""
Quantum Migration Priority Engine.
Categorizes assets into P0, P1, P2, P3 priorities with explanatory rationale.
"""
from typing import Tuple

def calculate_priority(
    risk_score: float,
    risk_type: str,
    data_sensitivity: str,
    business_criticality: str,
    data_lifetime_years: int
) -> Tuple[str, str]:
    """
    Returns (priority_level, explanation).
    Priority levels: P0 (Immediate), P1 (High), P2 (Planned), P3 (Monitor).
    """
    is_quantum = (risk_type == "Quantum")
    is_classical = (risk_type == "Classical")
    is_high_sens = data_sensitivity in ("High", "Critical")
    is_high_crit = business_criticality in ("High", "Critical")
    is_long_life = data_lifetime_years >= 10

    if (is_quantum and is_high_sens and is_long_life) or risk_score >= 78.0:
        priority = "P0"
        explanation = "High quantum exposure + critical/sensitive business asset + long data lifetime makes this an immediate migration planning candidate (P0)."
    elif (is_quantum and (is_high_sens or is_high_crit)) or is_classical or risk_score >= 60.0:
        priority = "P1"
        explanation = "High risk asset in an active business system requiring prioritized PQC migration planning (P1)."
    elif risk_score >= 40.0:
        priority = "P2"
        explanation = "Moderate risk asset scheduled for planned PQC migration during upcoming upgrade cycles (P2)."
    else:
        priority = "P3"
        explanation = "Low urgency asset or modern symmetric cipher. Retain and monitor under standard cryptographic maintenance (P3)."

    return priority, explanation
