from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix="/projects", tags=["Reports & Export"])

@router.get("/{id}/export/json")
def export_cbom_json(id: str, db: Session = Depends(get_db)):
    cbom_data = ReportService.export_cbom_json(db=db, project_id=id)
    return JSONResponse(
        content=cbom_data,
        headers={"Content-Disposition": f"attachment; filename=cbom_{id[:8]}.json"}
    )

@router.get("/{id}/export/pdf")
def export_pdf_report(id: str, db: Session = Depends(get_db)):
    pdf_path = ReportService.generate_pdf_report(db=db, project_id=id)
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"quantumshield_report_{id[:8]}.pdf"
    )
