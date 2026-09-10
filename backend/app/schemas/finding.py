from typing import Optional, Any, Dict
from pydantic import BaseModel, Field

class RawFindingResponse(BaseModel):
    id: str
    scan_id: str
    detector: str
    file_path: str
    line_number: int
    matched_text: str
    surrounding_context: Optional[str] = None
    language: Optional[str] = None
    algorithm_hint: Optional[str] = None
    library_hint: Optional[str] = None
    confidence: float = 0.5
    finding_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        from_attributes = True
