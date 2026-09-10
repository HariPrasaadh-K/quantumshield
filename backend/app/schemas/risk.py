from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RiskAssessmentResponse(BaseModel):
    id: str
    asset_id: str
    quantum_vulnerability_score: float
    data_sensitivity_score: float
    data_lifetime_score: float
    business_criticality_score: float
    migration_difficulty_score: float
    total_score: float
    risk_type: str
    explanation: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
