import uuid
import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.roadmap import Roadmap
from app.services.asset_service import AssetService
from app.engines.mosca_engine import evaluate_mosca_roadmap

class RoadmapService:
    @staticmethod
    def generate_roadmap(
        db: Session,
        project_id: str,
        planning_threat_horizon_years: int = 10,
        default_migration_time_years: int = 2
    ) -> Roadmap:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        assets = AssetService.get_project_assets(db, project_id)
        max_lifetime = max([a.data_lifetime_years for a in assets], default=10)
        
        p0_count = sum(1 for a in assets if a.priority == "P0")
        p1_count = sum(1 for a in assets if a.priority == "P1")

        mosca_data = evaluate_mosca_roadmap(
            max_data_lifetime_years=max_lifetime,
            estimated_migration_time_years=default_migration_time_years,
            planning_threat_horizon_years=planning_threat_horizon_years,
            urgent_count=p0_count,
            high_count=p1_count
        )

        roadmap_id = str(uuid.uuid4())
        roadmap = Roadmap(
            id=roadmap_id,
            project_id=project_id,
            planning_threat_horizon_years=planning_threat_horizon_years,
            generated_at=datetime.datetime.utcnow(),
            phases=mosca_data["phases"],
            urgent_asset_count=p0_count,
            high_priority_count=p1_count,
            explanation=mosca_data["explanation"],
            mosca_status=mosca_data["mosca_status"],
            required_security_window_years=mosca_data["required_security_window_years"]
        )

        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)
        return roadmap

    @staticmethod
    def get_latest_roadmap(db: Session, project_id: str) -> Optional[Roadmap]:
        return (
            db.query(Roadmap)
            .filter(Roadmap.project_id == project_id)
            .order_by(Roadmap.generated_at.desc())
            .first()
        )
