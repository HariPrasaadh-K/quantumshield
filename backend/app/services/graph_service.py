from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.scan import Scan
from app.models.dependency import Dependency
from app.services.asset_service import AssetService
from app.graph.dependency_graph import build_dependency_graph

class GraphService:
    @staticmethod
    def get_project_dependency_graph(db: Session, project_id: str) -> Dict[str, Any]:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        assets = AssetService.get_project_assets(db, project_id)
        
        latest_scan = (
            db.query(Scan)
            .filter(Scan.project_id == project_id, Scan.status == "completed")
            .order_by(Scan.started_at.desc())
            .first()
        )

        dependencies = []
        if latest_scan:
            dependencies = db.query(Dependency).filter(Dependency.scan_id == latest_scan.id).all()

        graph_data = build_dependency_graph(
            project_name=project.name,
            assets=assets,
            dependencies=dependencies
        )
        return graph_data
