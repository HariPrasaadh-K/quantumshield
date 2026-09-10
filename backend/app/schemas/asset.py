from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.risk import RiskAssessmentResponse
from app.schemas.recommendation import RecommendationResponse
from app.schemas.finding import RawFindingResponse

class CryptoAssetBase(BaseModel):
    name: str
    algorithm: str
    crypto_purpose: str = "Unknown"
    purpose_confidence: float = 0.5
    file_path: str
    line_number: int = 1
    language: Optional[str] = None
    library: Optional[str] = None
    risk_type: str = "Unknown"
    risk_score: float = 0.0
    priority: str = "P3"
    data_sensitivity: str = "Medium"
    business_criticality: str = "Medium"
    data_lifetime_years: int = 10
    migration_difficulty: str = "Medium"
    status: str = "active"

class CryptoAssetUpdate(BaseModel):
    data_sensitivity: Optional[str] = None
    business_criticality: Optional[str] = None
    data_lifetime_years: Optional[int] = None
    migration_difficulty: Optional[str] = None

class CryptoAssetResponse(CryptoAssetBase):
    id: str
    scan_id: str
    created_at: datetime
    risk_assessment: Optional[RiskAssessmentResponse] = None
    recommendation: Optional[RecommendationResponse] = None

    class Config:
        from_attributes = True

class CryptoAssetDetailResponse(CryptoAssetResponse):
    raw_evidence: Optional[List[RawFindingResponse]] = Field(default_factory=list)
