"""
Mosca Theorem-based Migration Analysis Engine.
Formula:
X = Planning Threat Horizon (years)
Y = Max Data Protection Lifetime (years)
Z = Estimated Migration Time (years)

Required Security Window = Y + Z

Condition:
If Y + Z > X -> URGENT
If Y + Z >= X - 2 -> ACCELERATE
Else -> PLANNED
"""
from typing import Dict, Any, List

MOSCA_DISCLAIMER = (
    "The planning threat horizon is a configurable planning parameter "
    "and is not a prediction of when a cryptographically relevant quantum computer will arrive."
)

def evaluate_mosca_roadmap(
    max_data_lifetime_years: int,
    estimated_migration_time_years: int = 2,
    planning_threat_horizon_years: int = 10,
    urgent_count: int = 0,
    high_count: int = 0
) -> Dict[str, Any]:
    """
    Evaluates Mosca theorem and generates phased roadmap timeline details.
    """
    required_security_window = max_data_lifetime_years + estimated_migration_time_years

    if required_security_window > planning_threat_horizon_years:
        mosca_status = "URGENT"
        summary_text = (
            f"URGENT: Required security window ({required_security_window} years = {max_data_lifetime_years} yrs data lifetime + "
            f"{estimated_migration_time_years} yrs migration) exceeds the configured planning threat horizon "
            f"({planning_threat_horizon_years} years). Data protected today may be exposed to 'Harvest Now, Decrypt Later' quantum attacks."
        )
    elif required_security_window >= (planning_threat_horizon_years - 2):
        mosca_status = "ACCELERATE"
        summary_text = (
            f"ACCELERATE: Required security window ({required_security_window} years) is close to the threat horizon "
            f"({planning_threat_horizon_years} years). PQC migration planning and hybrid pilots must be initiated immediately."
        )
    else:
        mosca_status = "PLANNED"
        summary_text = (
            f"PLANNED: Required security window ({required_security_window} years) falls within the threat horizon "
            f"({planning_threat_horizon_years} years). Follow standard PQC migration phases."
        )

    phases = [
        {
            "order": 1,
            "name": "1. Discovery & CBOM Inventory",
            "status": "completed",
            "description": "Scan repositories, identify cryptographic primitives, and catalog Cryptographic Bill of Materials (CBOM).",
            "asset_count": urgent_count + high_count
        },
        {
            "order": 2,
            "name": "2. Risk & Impact Assessment",
            "status": "in_progress" if mosca_status in ("URGENT", "ACCELERATE") else "pending",
            "description": "Evaluate quantum vulnerability, data protection lifetime, and business criticality across discovered assets.",
            "asset_count": urgent_count
        },
        {
            "order": 3,
            "name": "3. Inventory Validation & Prioritization",
            "status": "pending",
            "description": "Validate P0/P1 asset priority rankings with application security leads and system owners.",
            "asset_count": high_count
        },
        {
            "order": 4,
            "name": "4. PQC Algorithm Pilot & Benchmarking",
            "status": "pending",
            "description": "Deploy NIST FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA) candidates in non-production testbeds to benchmark key size & latency.",
            "asset_count": 0
        },
        {
            "order": 5,
            "name": "5. Hybrid Classical + Post-Quantum Migration",
            "status": "pending",
            "description": "Implement dual-algorithm hybrid schemes (e.g. ECDH + ML-KEM) to preserve classical compliance while ensuring quantum resilience.",
            "asset_count": 0
        },
        {
            "order": 6,
            "name": "6. Production Migration",
            "status": "pending",
            "description": "Deprecate legacy RSA/ECC key exchanges and signatures in favor of standardized PQC algorithms in production.",
            "asset_count": 0
        },
        {
            "order": 7,
            "name": "7. Validation & Continuous CBOM Monitoring",
            "status": "pending",
            "description": "Establish continuous automated CBOM scanning in CI/CD pipelines to prevent crypto agility regression.",
            "asset_count": 0
        }
    ]

    return {
        "mosca_status": mosca_status,
        "max_data_lifetime_years": max_data_lifetime_years,
        "estimated_migration_time_years": estimated_migration_time_years,
        "planning_threat_horizon_years": planning_threat_horizon_years,
        "required_security_window_years": required_security_window,
        "explanation": summary_text,
        "disclaimer": MOSCA_DISCLAIMER,
        "phases": phases
    }
