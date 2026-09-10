"""
CycloneDX 1.5/1.6 CBOM (Cryptographic Bill of Materials) JSON Generator.
Outputs standard-compliant CycloneDX structure with QuantumShield PQC properties.
"""
import uuid
import datetime
from typing import Dict, Any, List

def generate_cbom_json(project_name: str, scan_info: Dict[str, Any], assets: List[Any]) -> Dict[str, Any]:
    """
    Generates CycloneDX CBOM JSON schema structure.
    """
    bom_ref_prefix = f"urn:uuid:{uuid.uuid4()}"
    
    cbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": bom_ref_prefix,
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "tools": [
                {
                    "vendor": "QuantumShield",
                    "name": "QuantumShield CBOM Intelligence Engine",
                    "version": "1.0.0"
                }
            ],
            "component": {
                "type": "application",
                "name": project_name,
                "bom-ref": f"{project_name.lower().replace(' ', '-')}-root"
            }
        },
        "components": [],
        "dependencies": []
    }

    component_refs = []

    for asset in assets:
        comp_ref = f"cbom-asset-{asset.id}"
        component_refs.append(comp_ref)

        # Standard CycloneDX Cryptographic Asset Component
        crypto_component = {
            "type": "cryptographic-asset",
            "name": asset.name,
            "bom-ref": comp_ref,
            "description": f"Cryptographic primitive {asset.algorithm} used for {asset.crypto_purpose}",
            "evidence": {
                "occurrences": [
                    {
                        "location": asset.file_path,
                        "line": asset.line_number
                    }
                ]
            },
            "properties": [
                {"name": "quantumshield:algorithm", "value": asset.algorithm},
                {"name": "quantumshield:purpose", "value": asset.crypto_purpose},
                {"name": "quantumshield:purposeConfidence", "value": str(asset.purpose_confidence)},
                {"name": "quantumshield:riskType", "value": asset.risk_type},
                {"name": "quantumshield:riskScore", "value": str(asset.risk_score)},
                {"name": "quantumshield:priority", "value": asset.priority},
                {"name": "quantumshield:dataSensitivity", "value": asset.data_sensitivity},
                {"name": "quantumshield:businessCriticality", "value": asset.business_criticality},
                {"name": "quantumshield:dataLifetimeYears", "value": str(asset.data_lifetime_years)},
                {"name": "quantumshield:migrationDifficulty", "value": asset.migration_difficulty}
            ]
        }

        # Include PQC recommendation if populated
        if hasattr(asset, "recommendation") and asset.recommendation:
            rec = asset.recommendation
            crypto_component["properties"].extend([
                {"name": "quantumshield:pqcCandidate", "value": rec.candidate_algorithm},
                {"name": "quantumshield:pqcReason", "value": rec.reason},
                {"name": "quantumshield:migrationComplexity", "value": rec.migration_complexity}
            ])

        cbom["components"].append(crypto_component)

    # Core dependency binding
    cbom["dependencies"].append({
        "ref": f"{project_name.lower().replace(' ', '-')}-root",
        "dependsOn": component_refs
    })

    return cbom
