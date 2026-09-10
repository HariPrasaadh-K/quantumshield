import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal

client = TestClient(app)

def test_full_e2e_scan_pipeline():
    # 1. Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

    # 2. Create Demo Project
    res_demo = client.post("/api/projects/demo")
    assert res_demo.status_code == 201
    proj_id = res_demo.json()["id"]

    # 3. Trigger Scan on Demo Project
    res_scan = client.post(f"/api/projects/{proj_id}/scan")
    assert res_scan.status_code == 202
    scan_data = res_scan.json()
    assert scan_data["status"] == "completed"
    assert scan_data["assets_found"] > 0

    # 4. Fetch Discovered Crypto Assets
    res_assets = client.get(f"/api/projects/{proj_id}/assets")
    assert res_assets.status_code == 200
    assets = res_assets.json()
    assert len(assets) > 0

    # Confirm specific findings exist
    algos = [a["algorithm"].upper() for a in assets]
    assert any("RSA" in a for a in algos)
    assert any("AES" in a for a in algos)
    assert any("MD5" in a for a in algos)

    # 5. Fetch Risk Summary
    res_risk = client.get(f"/api/projects/{proj_id}/risk-summary")
    assert res_risk.status_code == 200
    risk_summary = res_risk.json()
    assert risk_summary["total_crypto_assets"] > 0
    assert risk_summary["quantum_vulnerable"] > 0

    # 6. Fetch PQC Recommendations
    res_recs = client.get(f"/api/projects/{proj_id}/recommendations")
    assert res_recs.status_code == 200
    recs = res_recs.json()
    assert len(recs) > 0

    # 7. Fetch Dependency Graph
    res_graph = client.get(f"/api/projects/{proj_id}/dependency-graph")
    assert res_graph.status_code == 200
    graph = res_graph.json()
    assert len(graph["nodes"]) > 0

    # 8. Generate Mosca Roadmap
    res_roadmap = client.get(f"/api/projects/{proj_id}/roadmap")
    assert res_roadmap.status_code == 200
    roadmap = res_roadmap.json()
    assert len(roadmap["phases"]) == 7

    # 9. Export CycloneDX CBOM JSON
    res_cbom = client.get(f"/api/projects/{proj_id}/export/json")
    assert res_cbom.status_code == 200
    cbom = res_cbom.json()
    assert cbom["bomFormat"] == "CycloneDX"
    assert len(cbom["components"]) > 0

    # 10. Export PDF Report
    res_pdf = client.get(f"/api/projects/{proj_id}/export/pdf")
    assert res_pdf.status_code == 200
    assert res_pdf.headers["content-type"] == "application/pdf"
    assert len(res_pdf.content) > 1000
