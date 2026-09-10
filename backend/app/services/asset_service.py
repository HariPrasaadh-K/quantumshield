from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.scan import Scan
from app.models.crypto_asset import CryptoAsset
from app.models.finding import RawFinding
from app.models.risk import RiskAssessment
from app.models.recommendation import Recommendation
from app.schemas.asset import CryptoAssetUpdate
from app.engines.risk_engine import calculate_risk_score
from app.engines.priority_engine import calculate_priority
from app.engines.pqc_recommender import recommend_pqc_alternative

class AssetService:
    @staticmethod
    def get_project_assets(
        db: Session,
        project_id: str,
        algorithm: Optional[str] = None,
        crypto_purpose: Optional[str] = None,
        risk_type: Optional[str] = None,
        priority: Optional[str] = None,
        language: Optional[str] = None
    ) -> List[CryptoAsset]:
        # Get latest completed scan for project
        latest_scan = (
            db.query(Scan)
            .filter(Scan.project_id == project_id, Scan.status == "completed")
            .order_by(Scan.started_at.desc())
            .first()
        )
        if not latest_scan:
            return []

        query = db.query(CryptoAsset).filter(CryptoAsset.scan_id == latest_scan.id)
        
        if algorithm:
            query = query.filter(CryptoAsset.algorithm.ilike(f"%{algorithm}%"))
        if crypto_purpose:
            query = query.filter(CryptoAsset.crypto_purpose.ilike(f"%{crypto_purpose}%"))
        if risk_type:
            query = query.filter(CryptoAsset.risk_type.ilike(f"%{risk_type}%"))
        if priority:
            query = query.filter(CryptoAsset.priority == priority.upper())
        if language:
            query = query.filter(CryptoAsset.language.ilike(f"%{language}%"))

        return query.all()

    @staticmethod
    def get_asset_by_id(db: Session, asset_id: str) -> Dict[str, Any]:
        asset = db.query(CryptoAsset).filter(CryptoAsset.id == asset_id).first()
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found.")

        # Find matching raw findings evidence
        raw_findings = (
            db.query(RawFinding)
            .filter(
                RawFinding.scan_id == asset.scan_id,
                RawFinding.file_path == asset.file_path,
                RawFinding.line_number == asset.line_number
            )
            .all()
        )

        return {
            "asset": asset,
            "raw_evidence": raw_findings
        }

    @staticmethod
    def update_asset_context(db: Session, asset_id: str, updates: CryptoAssetUpdate) -> CryptoAsset:
        asset = db.query(CryptoAsset).filter(CryptoAsset.id == asset_id).first()
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found.")

        if updates.data_sensitivity is not None:
            asset.data_sensitivity = updates.data_sensitivity
        if updates.business_criticality is not None:
            asset.business_criticality = updates.business_criticality
        if updates.data_lifetime_years is not None:
            asset.data_lifetime_years = updates.data_lifetime_years
        if updates.migration_difficulty is not None:
            asset.migration_difficulty = updates.migration_difficulty

        # Recalculate Risk
        risk_data = calculate_risk_score(
            algorithm=asset.algorithm,
            data_sensitivity=asset.data_sensitivity,
            business_criticality=asset.business_criticality,
            data_lifetime_years=asset.data_lifetime_years,
            migration_difficulty=asset.migration_difficulty
        )

        asset.risk_score = risk_data["total_score"]
        asset.risk_type = risk_data["risk_type"]

        # Recalculate Priority
        priority_level, priority_exp = calculate_priority(
            risk_score=risk_data["total_score"],
            risk_type=risk_data["risk_type"],
            data_sensitivity=asset.data_sensitivity,
            business_criticality=asset.business_criticality,
            data_lifetime_years=asset.data_lifetime_years
        )
        asset.priority = priority_level

        # Update Risk Assessment Model
        risk_assessment = db.query(RiskAssessment).filter(RiskAssessment.asset_id == asset_id).first()
        if risk_assessment:
            risk_assessment.quantum_vulnerability_score = risk_data["quantum_vulnerability_score"]
            risk_assessment.data_sensitivity_score = risk_data["data_sensitivity_score"]
            risk_assessment.data_lifetime_score = risk_data["data_lifetime_score"]
            risk_assessment.business_criticality_score = risk_data["business_criticality_score"]
            risk_assessment.migration_difficulty_score = risk_data["migration_difficulty_score"]
            risk_assessment.total_score = risk_data["total_score"]
            risk_assessment.risk_type = risk_data["risk_type"]
            risk_assessment.explanation = risk_data["explanation"]

        # Update Recommendation Model
        rec_data = recommend_pqc_alternative(
            algorithm=asset.algorithm,
            purpose=asset.crypto_purpose,
            risk_type=asset.risk_type
        )
        rec_model = db.query(Recommendation).filter(Recommendation.asset_id == asset_id).first()
        if rec_model:
            rec_model.candidate_algorithm = rec_data["candidate_algorithm"]
            rec_model.reason = rec_data["reason"]
            rec_model.migration_complexity = rec_data["migration_complexity"]
            rec_model.performance_considerations = rec_data["performance_considerations"]
            rec_model.compatibility_considerations = rec_data["compatibility_considerations"]

        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def get_risk_summary(db: Session, project_id: str) -> Dict[str, Any]:
        assets = AssetService.get_project_assets(db, project_id)
        
        total_assets = len(assets)
        quantum_vulnerable = sum(1 for a in assets if a.risk_type == "Quantum")
        classical_weak = sum(1 for a in assets if a.risk_type == "Classical")
        monitor_items = sum(1 for a in assets if a.risk_type == "Monitor")

        risk_bands = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for a in assets:
            if a.risk_score >= 81.0:
                risk_bands["CRITICAL"] += 1
            elif a.risk_score >= 61.0:
                risk_bands["HIGH"] += 1
            elif a.risk_score >= 31.0:
                risk_bands["MEDIUM"] += 1
            else:
                risk_bands["LOW"] += 1

        priority_dist = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        for a in assets:
            priority_dist[a.priority] = priority_dist.get(a.priority, 0) + 1

        algo_dist = {}
        purpose_dist = {}
        for a in assets:
            algo_dist[a.algorithm] = algo_dist.get(a.algorithm, 0) + 1
            purpose_dist[a.crypto_purpose] = purpose_dist.get(a.crypto_purpose, 0) + 1

        return {
            "total_crypto_assets": total_assets,
            "quantum_vulnerable": quantum_vulnerable,
            "classical_weakness": classical_weak,
            "monitor_items": monitor_items,
            "critical_risk": risk_bands["CRITICAL"],
            "high_risk": risk_bands["HIGH"],
            "medium_risk": risk_bands["MEDIUM"],
            "low_risk": risk_bands["LOW"],
            "priority_distribution": priority_dist,
            "algorithm_distribution": algo_dist,
            "purpose_distribution": purpose_dist
        }
