from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ScanResponse(BaseModel):
    id: str
    project_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    files_scanned: int = 0
    findings_found: int = 0
    assets_found: int = 0
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
