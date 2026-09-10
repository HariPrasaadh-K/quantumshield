"""
Quantum & Classical Risk Assessment Engine.
Pure deterministic functions with zero database side-effects.
"""
from typing import Dict, Any

QUANTUM_VULNERABLE_ALGOS = {"RSA", "ECC", "ECDSA", "ECDH", "DH", "DSA", "ED25519", "ED448"}
CLASSICAL_WEAK_ALGOS = {"MD5", "SHA-1", "SHA1", "DES", "3DES", "RC4", "BLOWFISH"}
MONITOR_ALGOS = {"AES", "AES-128", "AES-256", "SHA-256", "SHA-384", "SHA-512", "SHA256", "SHA384", "SHA512", "HMAC"}

def classify_risk_type(algorithm: str) -> str:
    algo = (algorithm or "").upper().strip()
    if any(q in algo for q in QUANTUM_VULNERABLE_ALGOS):
        return "Quantum"
    if any(c in algo for c in CLASSICAL_WEAK_ALGOS):
        return "Classical"
    if any(m in algo for m in MONITOR_ALGOS):
        return "Monitor"
    return "Unknown"

def calculate_risk_score(
    algorithm: str,
    data_sensitivity: str = "Medium",
    business_criticality: str = "Medium",
    data_lifetime_years: int = 10,
    migration_difficulty: str = "Medium"
) -> Dict[str, Any]:
    risk_type = classify_risk_type(algorithm)
    
    # 1. Quantum / Algorithm vulnerability score (0-100) - 35% weight
    if risk_type == "Quantum":
        q_score = 95.0
    elif risk_type == "Classical":
        q_score = 85.0
    elif risk_type == "Monitor":
        q_score = 30.0
    else:
        q_score = 40.0

    # 2. Data Sensitivity score (0-100) - 20% weight
    ds_map = {"Critical": 100.0, "High": 80.0, "Medium": 50.0, "Low": 20.0}
    ds_score = ds_map.get(data_sensitivity, 50.0)

    # 3. Data Protection Lifetime score (0-100) - 20% weight
    if data_lifetime_years >= 20:
        dl_score = 100.0
    elif data_lifetime_years >= 10:
        dl_score = 75.0
    elif data_lifetime_years >= 5:
        dl_score = 50.0
    else:
        dl_score = 25.0

    # 4. Business Criticality score (0-100) - 15% weight
    bc_map = {"Critical": 100.0, "High": 80.0, "Medium": 50.0, "Low": 20.0}
    bc_score = bc_map.get(business_criticality, 50.0)

    # 5. Migration Difficulty score (0-100) - 10% weight
    md_map = {"High": 90.0, "Medium": 60.0, "Low": 30.0}
    md_score = md_map.get(migration_difficulty, 60.0)

    # Weighted calculation:
    # 35% Quantum vulnerability + 20% Data sensitivity + 20% Data lifetime + 15% Business criticality + 10% Migration difficulty
    total_score = round(
        (q_score * 0.35) +
        (ds_score * 0.20) +
        (dl_score * 0.20) +
        (bc_score * 0.15) +
        (md_score * 0.10),
        1
    )

    # Determine risk band
    if total_score >= 81.0:
        band = "CRITICAL"
    elif total_score >= 61.0:
        band = "HIGH"
    elif total_score >= 31.0:
        band = "MEDIUM"
    else:
        band = "LOW"

    # Build factor breakdown string
    factors_summary = (
        f"Contributing Factor Scores: Quantum Vulnerability={q_score} (35%), "
        f"Data Sensitivity={ds_score} (20%), Data Lifetime={dl_score} (20%), "
        f"Business Criticality={bc_score} (15%), Migration Difficulty={md_score} (10%)."
    )

    # Build full risk explanation
    if risk_type == "Quantum":
        explanation = (
            f"{algorithm} relies on asymmetric mathematical hardness (e.g., integer factorization or discrete logarithms) "
            f"which is vulnerable to Shor's algorithm on a cryptographically relevant quantum computer. "
            f"{factors_summary} Yields a total weighted risk score of {total_score} ({band})."
        )
    elif risk_type == "Classical":
        explanation = (
            f"{algorithm} is a legacy algorithm with classical mathematical weaknesses (e.g. collision or key space vulnerabilities). "
            f"{factors_summary} Immediate migration to modern standards is recommended regardless of quantum computing timeline."
        )
    elif risk_type == "Monitor":
        explanation = (
            f"{algorithm} is a symmetric algorithm or modern hash function. Symmetric encryption (like AES-256) is not broken by Shor's algorithm, "
            f"though Grover's algorithm effectively halves symmetric key space. "
            f"{factors_summary} Monitor key length and security margins."
        )
    else:
        explanation = (
            f"Unclassified or surface-level cryptographic reference for {algorithm} requiring manual audit. "
            f"{factors_summary}"
        )

    return {
        "quantum_vulnerability_score": q_score,
        "data_sensitivity_score": ds_score,
        "data_lifetime_score": dl_score,
        "business_criticality_score": bc_score,
        "migration_difficulty_score": md_score,
        "total_score": total_score,
        "risk_type": risk_type,
        "risk_band": band,
        "explanation": explanation
    }
