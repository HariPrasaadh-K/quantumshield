from typing import Optional
from pydantic import BaseModel

class RecommendationResponse(BaseModel):
    id: str
    asset_id: str
    current_algorithm: str
    current_purpose: str
    candidate_algorithm: str
    reason: str
    migration_complexity: str
    performance_considerations: Optional[str] = None
    compatibility_considerations: Optional[str] = None
    confidence: float
    disclaimer: str

    class Config:
        from_attributes = True
