from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    name: str
    source_type: str
    source_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectGithubCreate(BaseModel):
    name: str
    github_url: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
