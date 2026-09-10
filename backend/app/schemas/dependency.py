from typing import Optional
from pydantic import BaseModel

class DependencyResponse(BaseModel):
    id: str
    scan_id: str
    source_asset_id: str
    target_asset_id: str
    relationship_type: str
    confidence: float = 0.8
    evidence: Optional[str] = None

    class Config:
        from_attributes = True
