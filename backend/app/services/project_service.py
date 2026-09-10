import os
import uuid
import shutil
import tempfile
import git
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.models.project import Project
from app.core.config import settings
from app.utils.security_utils import validate_github_url, safe_extract_zip, cleanup_directory

class ProjectService:
    @staticmethod
    def create_project(db: Session, name: str, source_type: str, source_url: Optional[str] = None) -> Project:
        proj_id = str(uuid.uuid4())
        project = Project(
            id=proj_id,
            name=name,
            source_type=source_type,
            source_url=source_url,
            status="active"
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_projects(db: Session) -> List[Project]:
        return db.query(Project).order_by(Project.created_at.desc()).all()

    @staticmethod
    def get_project_by_id(db: Session, project_id: str) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
        return project

    @staticmethod
    def upload_zip_project(db: Session, name: str, file: UploadFile) -> Project:
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only .zip files are allowed.")
            
        proj_dir = os.path.join(settings.UPLOAD_TMP_DIR, f"proj_{uuid.uuid4().hex}")
        os.makedirs(proj_dir, exist_ok=True)
        
        zip_path = os.path.join(proj_dir, "uploaded.zip")
        try:
            with open(zip_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            extract_target = os.path.join(proj_dir, "source")
            safe_extract_zip(zip_path, extract_target)
            
            project = ProjectService.create_project(
                db=db,
                name=name or file.filename.replace(".zip", ""),
                source_type="zip",
                source_url=extract_target
            )
            return project
        except Exception as e:
            cleanup_directory(proj_dir)
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Failed to process ZIP upload: {str(e)}")

    @staticmethod
    def create_github_project(db: Session, name: str, github_url: str) -> Project:
        clean_url = validate_github_url(github_url)
        proj_dir = os.path.join(settings.UPLOAD_TMP_DIR, f"gh_{uuid.uuid4().hex}")
        os.makedirs(proj_dir, exist_ok=True)
        
        extract_target = os.path.join(proj_dir, "source")
        
        try:
            # Clone statically using git Python
            git.Repo.clone_from(clean_url, extract_target, depth=1)
            
            project = ProjectService.create_project(
                db=db,
                name=name,
                source_type="github",
                source_url=extract_target
            )
            return project
        except Exception as e:
            cleanup_directory(proj_dir)
            raise HTTPException(status_code=400, detail=f"Failed to clone GitHub repository: {str(e)}")
