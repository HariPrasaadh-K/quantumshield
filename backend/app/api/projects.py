from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.project import ProjectResponse, ProjectGithubCreate, ProjectCreate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return ProjectService.get_projects(db)

@router.get("/{id}", response_model=ProjectResponse)
def get_project(id: str, db: Session = Depends(get_db)):
    return ProjectService.get_project_by_id(db, id)

@router.post("/upload", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def upload_project_zip(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return ProjectService.upload_zip_project(db=db, name=name, file=file)

@router.post("/github", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_github_project(
    payload: ProjectGithubCreate,
    db: Session = Depends(get_db)
):
    return ProjectService.create_github_project(db=db, name=payload.name, github_url=payload.github_url)

@router.post("/demo", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_demo_project_endpoint(
    db: Session = Depends(get_db)
):
    import os
    demo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "demo-project"))
    if not os.path.exists(demo_path):
        raise HTTPException(status_code=404, detail="Demo project path does not exist.")

    return ProjectService.create_project(
        db=db,
        name="QuantumShield Demo Project",
        source_type="demo",
        source_url=demo_path
    )
