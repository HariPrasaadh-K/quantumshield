from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.roadmap import RoadmapCreateRequest, RoadmapResponse
from app.services.roadmap_service import RoadmapService

router = APIRouter(prefix="/projects", tags=["Roadmap"])

@router.post("/{id}/roadmap", response_model=RoadmapResponse)
def generate_roadmap(
    id: str,
    payload: RoadmapCreateRequest,
    db: Session = Depends(get_db)
):
    roadmap = RoadmapService.generate_roadmap(
        db=db,
        project_id=id,
        planning_threat_horizon_years=payload.planning_threat_horizon_years,
        default_migration_time_years=payload.default_migration_time_years
    )
    return roadmap

@router.get("/{id}/roadmap", response_model=RoadmapResponse)
def get_roadmap(id: str, db: Session = Depends(get_db)):
    roadmap = RoadmapService.get_latest_roadmap(db=db, project_id=id)
    if not roadmap:
        # Generate default roadmap if none exists
        roadmap = RoadmapService.generate_roadmap(db=db, project_id=id)
    return roadmap
