import os
import uuid
import datetime
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.scan import Scan
from app.models.finding import RawFinding
from app.models.crypto_asset import CryptoAsset
from app.models.risk import RiskAssessment
from app.models.recommendation import Recommendation
from app.models.dependency import Dependency

from app.scanners import get_scanners_for_file, ALL_SCANNERS
from app.utils.file_utils import walk_project_files, get_relative_path
from app.engines.purpose_classifier import classify_crypto_purpose
from app.engines.risk_engine import calculate_risk_score
from app.engines.priority_engine import calculate_priority
from app.engines.pqc_recommender import recommend_pqc_alternative

def derive_asset_context_inputs(
    algorithm: str,
    purpose: str,
    file_path: str,
    detector: str
) -> Tuple[str, str, int, str]:
    """
    Derives asset-specific contextual inputs based on primitive, purpose, location, and detector.
    Returns (data_sensitivity, business_criticality, data_lifetime_years, migration_difficulty).
    """
    algo_upper = (algorithm or "").upper()
    file_lower = (file_path or "").lower()
    detector_lower = (detector or "").lower()

    # 1. Defaults
    sensitivity = "Medium"
    criticality = "Medium"
    lifetime = 10
    difficulty = "Medium"

    # 2. Surface / Container Hints (Low impact)
    if "dockerfile" in file_lower or "container" in detector_lower:
        sensitivity = "Low"
        criticality = "Low"
        lifetime = 2
        difficulty = "Low"
        return sensitivity, criticality, lifetime, difficulty

    # 3. Manifest Library Dependencies
    if "manifest" in detector_lower or file_lower in ("pom.xml", "requirements.txt", "package.json"):
        sensitivity = "Medium"
        criticality = "Medium"
        lifetime = 5
        difficulty = "Medium"
        return sensitivity, criticality, lifetime, difficulty

    # 4. Asymmetric Cryptography (RSA, ECDSA, ECDH, DH) in core source files
    if any(q in algo_upper for q in ["RSA", "ECDSA", "ECDH", "DH", "DSA"]):
        difficulty = "High" # PKI / Key exchange / cert migration is complex
        if any(k in file_lower for k in ["crypto", "security", "auth", "key"]):
            sensitivity = "Critical"
            criticality = "Critical"
        else:
            sensitivity = "High"
            criticality = "High"

        if purpose in ("Key Establishment", "Encryption"):
            lifetime = 20 # Long-term Secrecy for encrypted data
        elif purpose == "Digital Signature":
            lifetime = 15 # Legal contract / audit lifetime
        else:
            lifetime = 10
        return sensitivity, criticality, lifetime, difficulty

    # 5. Legacy / Classical Weak Hashes & Ciphers (MD5, DES, 3DES)
    if any(c in algo_upper for c in ["MD5", "DES", "3DES", "RC4", "SHA-1"]):
        difficulty = "Low" if "MD5" in algo_upper else "Medium"
        sensitivity = "Low" if "MD5" in algo_upper else "Medium"
        criticality = "Medium"
        lifetime = 5
        return sensitivity, criticality, lifetime, difficulty

    # 6. Symmetric Modern Ciphers (AES)
    if "AES" in algo_upper:
        difficulty = "Low"
        sensitivity = "High" if "crypto" in file_lower or "auth" in file_lower else "Medium"
        criticality = "High"
        lifetime = 10
        return sensitivity, criticality, lifetime, difficulty

    return sensitivity, criticality, lifetime, difficulty

class ScanService:
    @staticmethod
    def execute_scan(db: Session, project_id: str) -> Scan:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        scan_id = str(uuid.uuid4())
        scan = Scan(
            id=scan_id,
            project_id=project_id,
            status="running",
            started_at=datetime.datetime.utcnow()
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)

        source_dir = project.source_url
        if not source_dir or not os.path.exists(source_dir):
            scan.status = "failed"
            scan.error_message = "Source directory missing or inaccessible."
            db.commit()
            return scan

        try:
            # 1. Discover files
            all_file_paths = walk_project_files(source_dir)
            scan.files_scanned = len(all_file_paths)

            # 2. Run static scanners
            all_raw_findings = []
            for full_path in all_file_paths:
                rel_path = get_relative_path(full_path, source_dir)
                scanners = get_scanners_for_file(full_path)
                
                for scanner in scanners:
                    findings = scanner.scan_file(full_path, rel_path)
                    all_raw_findings.extend(findings)

            scan.findings_found = len(all_raw_findings)

            # Save Raw Findings to DB
            raw_finding_models = []
            for rf in all_raw_findings:
                rf_model = RawFinding(
                    id=str(uuid.uuid4()),
                    scan_id=scan_id,
                    detector=rf["detector"],
                    file_path=rf["file_path"],
                    line_number=rf["line_number"],
                    matched_text=rf["matched_text"],
                    surrounding_context=rf["surrounding_context"],
                    language=rf["language"],
                    algorithm_hint=rf["algorithm_hint"],
                    library_hint=rf["library_hint"],
                    confidence=rf["confidence"],
                    finding_metadata=rf["metadata"]
                )
                raw_finding_models.append(rf_model)

            db.add_all(raw_finding_models)
            db.flush()

            # 3. Deduplicate findings into Crypto Assets
            asset_groups: Dict[tuple, List[RawFinding]] = {}
            for rf_m in raw_finding_models:
                key = (rf_m.file_path, rf_m.line_number, (rf_m.algorithm_hint or "Unknown").upper())
                asset_groups.setdefault(key, []).append(rf_m)

            crypto_assets = []
            risk_assessments = []
            recommendations = []

            for (f_path, line_num, algo), findings_list in asset_groups.items():
                primary_finding = max(findings_list, key=lambda x: x.confidence)
                
                # Purpose Classification
                purpose, purpose_conf = classify_crypto_purpose(
                    algorithm=algo,
                    matched_text=primary_finding.matched_text,
                    context=primary_finding.surrounding_context or ""
                )

                asset_id = str(uuid.uuid4())
                
                # Derive asset-specific initial context inputs
                sens, crit, life, diff = derive_asset_context_inputs(
                    algorithm=algo,
                    purpose=purpose,
                    file_path=f_path,
                    detector=primary_finding.detector
                )

                # Risk calculation with asset-specific parameters
                risk_data = calculate_risk_score(
                    algorithm=algo,
                    data_sensitivity=sens,
                    business_criticality=crit,
                    data_lifetime_years=life,
                    migration_difficulty=diff
                )

                priority_level, priority_exp = calculate_priority(
                    risk_score=risk_data["total_score"],
                    risk_type=risk_data["risk_type"],
                    data_sensitivity=sens,
                    business_criticality=crit,
                    data_lifetime_years=life
                )

                # Create Asset
                asset = CryptoAsset(
                    id=asset_id,
                    scan_id=scan_id,
                    name=f"{algo} in {os.path.basename(f_path)}:{line_num}",
                    algorithm=algo,
                    crypto_purpose=purpose,
                    purpose_confidence=purpose_conf,
                    file_path=f_path,
                    line_number=line_num,
                    language=primary_finding.language,
                    library=primary_finding.library_hint,
                    risk_type=risk_data["risk_type"],
                    risk_score=risk_data["total_score"],
                    priority=priority_level,
                    data_sensitivity=sens,
                    business_criticality=crit,
                    data_lifetime_years=life,
                    migration_difficulty=diff,
                    status="active"
                )
                crypto_assets.append(asset)

                # Risk Assessment Model
                risk_model = RiskAssessment(
                    id=str(uuid.uuid4()),
                    asset_id=asset_id,
                    quantum_vulnerability_score=risk_data["quantum_vulnerability_score"],
                    data_sensitivity_score=risk_data["data_sensitivity_score"],
                    data_lifetime_score=risk_data["data_lifetime_score"],
                    business_criticality_score=risk_data["business_criticality_score"],
                    migration_difficulty_score=risk_data["migration_difficulty_score"],
                    total_score=risk_data["total_score"],
                    risk_type=risk_data["risk_type"],
                    explanation=risk_data["explanation"]
                )
                risk_assessments.append(risk_model)

                # PQC Recommendation Model
                rec_data = recommend_pqc_alternative(
                    algorithm=algo,
                    purpose=purpose,
                    risk_type=risk_data["risk_type"]
                )

                rec_model = Recommendation(
                    id=str(uuid.uuid4()),
                    asset_id=asset_id,
                    current_algorithm=algo,
                    current_purpose=purpose,
                    candidate_algorithm=rec_data["candidate_algorithm"],
                    reason=rec_data["reason"],
                    migration_complexity=rec_data["migration_complexity"],
                    performance_considerations=rec_data["performance_considerations"],
                    compatibility_considerations=rec_data["compatibility_considerations"],
                    confidence=rec_data["confidence"],
                    disclaimer=rec_data["disclaimer"]
                )
                recommendations.append(rec_model)

            db.add_all(crypto_assets)
            db.add_all(risk_assessments)
            db.add_all(recommendations)
            db.flush()

            # 4. Generate dependencies
            dependencies = []
            if len(crypto_assets) > 1:
                file_map: Dict[str, List[CryptoAsset]] = {}
                for ca in crypto_assets:
                    file_map.setdefault(ca.file_path, []).append(ca)

                for f_path, assets_in_file in file_map.items():
                    if len(assets_in_file) > 1:
                        for i in range(len(assets_in_file) - 1):
                            dep = Dependency(
                                id=str(uuid.uuid4()),
                                scan_id=scan_id,
                                source_asset_id=assets_in_file[i].id,
                                target_asset_id=assets_in_file[i + 1].id,
                                relationship_type="USES",
                                confidence=0.85,
                                evidence=f"Co-located in source file {f_path}"
                            )
                            dependencies.append(dep)

            db.add_all(dependencies)

            scan.assets_found = len(crypto_assets)
            scan.status = "completed"
            scan.completed_at = datetime.datetime.utcnow()
            db.commit()
            db.refresh(scan)

            return scan

        except Exception as e:
            db.rollback()
            scan.status = "failed"
            scan.error_message = str(e)
            db.commit()
            raise HTTPException(status_code=500, detail=f"Scan execution failed: {str(e)}")

    @staticmethod
    def get_scans_by_project(db: Session, project_id: str) -> List[Scan]:
        return db.query(Scan).filter(Scan.project_id == project_id).order_by(Scan.started_at.desc()).all()

    @staticmethod
    def get_scan_by_id(db: Session, scan_id: str) -> Scan:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found.")
        return scan
