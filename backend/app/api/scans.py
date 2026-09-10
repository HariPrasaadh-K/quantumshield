from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.scan import ScanResponse
from app.services.scan_service import ScanService

router = APIRouter(prefix="/projects", tags=["Scans"])

@router.post("/{id}/scan", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
def start_scan(id: str, db: Session = Depends(get_db)):
    return ScanService.execute_scan(db=db, project_id=id)

@router.get("/{id}/scans", response_model=List[ScanResponse])
def get_project_scans(id: str, db: Session = Depends(get_db)):
    return ScanService.get_scans_by_project(db=db, project_id=id)

@router.get("/{id}/scans/{scan_id}", response_model=ScanResponse)
def get_scan_details(id: str, scan_id: str, db: Session = Depends(get_db)):
    return ScanService.get_scan_by_id(db=db, scan_id=scan_id)
