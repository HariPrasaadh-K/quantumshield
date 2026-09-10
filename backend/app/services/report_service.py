import os
import json
import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from app.models.project import Project
from app.models.scan import Scan
from app.services.asset_service import AssetService
from app.services.roadmap_service import RoadmapService
from app.cbom.generator import generate_cbom_json
from app.core.config import settings

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ReportService:
    @staticmethod
    def export_cbom_json(db: Session, project_id: str) -> Dict[str, Any]:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")

        assets = AssetService.get_project_assets(db, project_id)
        latest_scan = db.query(Scan).filter(Scan.project_id == project_id, Scan.status == "completed").order_by(Scan.started_at.desc()).first()

        scan_info = {
            "scan_id": latest_scan.id if latest_scan else "N/A",
            "completed_at": latest_scan.completed_at.isoformat() if latest_scan and latest_scan.completed_at else "N/A"
        }

        cbom_data = generate_cbom_json(project_name=project.name, scan_info=scan_info, assets=assets)
        return cbom_data

    @staticmethod
    def generate_pdf_report(db: Session, project_id: str) -> str:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")

        assets = AssetService.get_project_assets(db, project_id)
        risk_summary = AssetService.get_risk_summary(db, project_id)
        roadmap = RoadmapService.get_latest_roadmap(db, project_id)

        pdf_filename = f"quantumshield_report_{project_id[:8]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(settings.REPORTS_DIR, pdf_filename)

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#7C3AED'),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'ReportSubTitle',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#4B5563'),
            spaceAfter=15
        )
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1F2937'),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#374151')
        )
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Italic'],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#6B7280'),
            spaceBefore=15
        )

        story = []

        # 1. Header & Title
        story.append(Paragraph("QUANTUMSHIELD", title_style))
        story.append(Paragraph("Quantum-Safe Cryptographic Bill of Materials (CBOM) & Risk Assessment Report", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7C3AED'), spaceAfter=15))

        # 2. Project Information
        story.append(Paragraph("1. Executive Summary & Project Context", h2_style))
        proj_info_data = [
            [Paragraph("<b>Project Name:</b>", body_style), Paragraph(project.name, body_style)],
            [Paragraph("<b>Source Type:</b>", body_style), Paragraph(project.source_type.upper(), body_style)],
            [Paragraph("<b>Report Date:</b>", body_style), Paragraph(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), body_style)],
            [Paragraph("<b>Total Crypto Assets:</b>", body_style), Paragraph(str(risk_summary['total_crypto_assets']), body_style)],
        ]
        t_proj = Table(proj_info_data, colWidths=[140, 380])
        t_proj.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_proj)
        story.append(Spacer(1, 10))

        # 3. Risk Breakdown Table
        story.append(Paragraph("2. Cryptographic Risk & Priority Distribution", h2_style))
        risk_data_table = [
            ["Metric", "Count", "Classification Note"],
            ["Quantum Vulnerable Assets", str(risk_summary['quantum_vulnerable']), "RSA, ECC, ECDSA, ECDH, DH vulnerable to Shor's Algorithm"],
            ["Classical Weaknesses", str(risk_summary['classical_weakness']), "MD5, SHA-1, DES legacy algorithms"],
            ["Monitor Items", str(risk_summary['monitor_items']), "AES-256 / Modern hashes (Monitor key length & margins)"],
            ["P0 Immediate Planning", str(risk_summary['priority_distribution'].get('P0', 0)), "Critical business exposure + long data lifetime"],
            ["P1 High Priority", str(risk_summary['priority_distribution'].get('P1', 0)), "High risk assets in active business paths"],
        ]
        t_risk = Table(risk_data_table, colWidths=[160, 60, 300])
        t_risk.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7C3AED')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        story.append(t_risk)
        story.append(Spacer(1, 12))

        # 4. Inventory Table
        story.append(Paragraph("3. Discovered Cryptographic Inventory (CBOM)", h2_style))
        inv_headers = ["Algorithm", "Purpose", "Risk Type", "Score", "Priority", "File Location"]
        inv_table_data = [inv_headers]

        for asset in assets[:15]: # Top 15 assets
            inv_table_data.append([
                Paragraph(asset.algorithm, body_style),
                Paragraph(asset.crypto_purpose, body_style),
                Paragraph(asset.risk_type, body_style),
                Paragraph(str(asset.risk_score), body_style),
                Paragraph(asset.priority, body_style),
                Paragraph(f"{asset.file_path}:{asset.line_number}", body_style)
            ])

        t_inv = Table(inv_table_data, colWidths=[70, 90, 65, 45, 45, 205])
        t_inv.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
            ('PADDING', (0,0), (-1,-1), 4),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        story.append(t_inv)
        story.append(Spacer(1, 12))

        # 5. PQC Recommendations
        story.append(Paragraph("4. Recommended Post-Quantum Alternatives (NIST FIPS Standardized)", h2_style))
        rec_table_data = [["Current Primitive", "Purpose", "Candidate NIST PQC Target", "Migration Complexity"]]
        for asset in assets[:8]:
            if hasattr(asset, "recommendation") and asset.recommendation:
                rec = asset.recommendation
                rec_table_data.append([
                    Paragraph(rec.current_algorithm, body_style),
                    Paragraph(rec.current_purpose, body_style),
                    Paragraph(rec.candidate_algorithm, body_style),
                    Paragraph(rec.migration_complexity, body_style)
                ])
        
        t_rec = Table(rec_table_data, colWidths=[90, 90, 250, 90])
        t_rec.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_rec)
        story.append(Spacer(1, 12))

        # 6. Mosca Analysis & Roadmap
        if roadmap:
            story.append(Paragraph("5. Mosca Theorem Migration Roadmap", h2_style))
            story.append(Paragraph(f"<b>Planning Threat Horizon:</b> {roadmap.planning_threat_horizon_years} years", body_style))
            story.append(Paragraph(f"<b>Assessment Rationale:</b> {roadmap.explanation}", body_style))
            story.append(Spacer(1, 6))

        # 7. Disclaimer
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#9CA3AF'), spaceBefore=15, spaceAfter=8))
        story.append(Paragraph(
            "<b>Disclaimer:</b> QuantumShield candidate migration guidance is provided for security planning and risk prioritizing purposes only. "
            "All cryptographic algorithm replacements must be validated in non-production environments before deployment.",
            disclaimer_style
        ))

        doc.build(story)
        return pdf_path
