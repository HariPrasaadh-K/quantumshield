from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class RoadmapCreateRequest(BaseModel):
    planning_threat_horizon_years: int = 10
    default_migration_time_years: int = 2

class RoadmapPhase(BaseModel):
    order: int
    name: str
    status: str # pending, in_progress, completed
    description: str
    asset_count: int = 0

class RoadmapResponse(BaseModel):
    id: str
    project_id: str
    planning_threat_horizon_years: int
    generated_at: datetime
    phases: List[Dict[str, Any]] = Field(default_factory=list)
    urgent_asset_count: int = 0
    high_priority_count: int = 0
    explanation: Optional[str] = None
    mosca_status: Optional[str] = None
    required_security_window_years: Optional[int] = None

    class Config:
        from_attributes = True
