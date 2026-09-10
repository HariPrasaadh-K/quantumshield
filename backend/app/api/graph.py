from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.graph_service import GraphService

router = APIRouter(prefix="/projects", tags=["Dependency Graph"])

@router.get("/{id}/dependency-graph")
def get_dependency_graph(id: str, db: Session = Depends(get_db)):
    return GraphService.get_project_dependency_graph(db=db, project_id=id)
