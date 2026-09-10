from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.asset import CryptoAssetResponse, CryptoAssetUpdate, CryptoAssetDetailResponse
from app.schemas.recommendation import RecommendationResponse
from app.services.asset_service import AssetService
from app.models.crypto_asset import CryptoAsset
from app.models.recommendation import Recommendation

router = APIRouter(prefix="/projects", tags=["Crypto Assets"])

@router.get("/{id}/assets", response_model=List[CryptoAssetResponse])
def get_assets(
    id: str,
    algorithm: Optional[str] = Query(None),
    purpose: Optional[str] = Query(None),
    risk: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return AssetService.get_project_assets(
        db=db,
        project_id=id,
        algorithm=algorithm,
        crypto_purpose=purpose,
        risk_type=risk,
        priority=priority,
        language=language
    )

@router.get("/{id}/assets/{asset_id}", response_model=CryptoAssetDetailResponse)
def get_asset_detail(id: str, asset_id: str, db: Session = Depends(get_db)):
    detail = AssetService.get_asset_by_id(db=db, asset_id=asset_id)
    asset = detail["asset"]
    raw_evidence = detail["raw_evidence"]

    response = CryptoAssetDetailResponse.model_validate(asset)
    response.raw_evidence = raw_evidence
    return response

@router.patch("/{id}/assets/{asset_id}", response_model=CryptoAssetResponse)
def update_asset_context(
    id: str,
    asset_id: str,
    updates: CryptoAssetUpdate,
    db: Session = Depends(get_db)
):
    return AssetService.update_asset_context(db=db, asset_id=asset_id, updates=updates)

@router.get("/{id}/risk-summary")
def get_risk_summary(id: str, db: Session = Depends(get_db)):
    return AssetService.get_risk_summary(db=db, project_id=id)

@router.get("/{id}/recommendations", response_model=List[RecommendationResponse])
def get_recommendations(id: str, db: Session = Depends(get_db)):
    assets = AssetService.get_project_assets(db=db, project_id=id)
    asset_ids = [a.id for a in assets]
    if not asset_ids:
        return []
    recs = db.query(Recommendation).filter(Recommendation.asset_id.in_(asset_ids)).all()
    return recs
