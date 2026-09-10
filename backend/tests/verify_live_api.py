import sys
import json
import urllib.request
import urllib.parse

BASE_URL = "http://127.0.0.1:8000/api"

def make_req(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    if data is not None and not isinstance(data, (bytes, str)):
        data = json.dumps(data).encode('utf-8')
        headers["Content-Type"] = "application/json"
    elif isinstance(data, str):
        data = data.encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        content = resp.read()
        ctype = resp.headers.get("Content-Type", "")
        if "json" in ctype:
            return resp.status, json.loads(content.decode('utf-8'))
        return resp.status, content

def run_live_validation():
    print("=== QUANTUMSHIELD LIVE END-TO-END VALIDATION ===")

    # 1. Health
    status, body = make_req(f"{BASE_URL}/health")
    print(f"[1] Health Check: Status {status}, Response: {body}")
    assert status == 200 and body["status"] == "healthy"

    # 2. Create Demo Project
    status, proj = make_req(f"{BASE_URL}/projects/demo", method="POST")
    print(f"[2] Create Demo Project: Status {status}, Project ID: {proj['id']}")
    assert status == 201
    proj_id = proj["id"]

    # 3. Trigger Scan
    status, scan = make_req(f"{BASE_URL}/projects/{proj_id}/scan", method="POST")
    print(f"[3] Scan Execution: Status {status}, Status: {scan['status']}, Assets Found: {scan['assets_found']}")
    assert status == 202 and scan["status"] == "completed" and scan["assets_found"] > 0

    # 4. Fetch Assets
    status, assets = make_req(f"{BASE_URL}/projects/{proj_id}/assets")
    print(f"[4] Fetch Assets: Total {len(assets)} assets discovered.")
    assert status == 200 and len(assets) > 0

    algos = set(a["algorithm"].upper() for a in assets)
    purposes = set(a["crypto_purpose"] for a in assets)
    priorities = set(a["priority"] for a in assets)
    risk_types = set(a["risk_type"] for a in assets)

    print(f"    - Algorithms Discovered: {algos}")
    print(f"    - Purposes Classified: {purposes}")
    print(f"    - Risk Types Identified: {risk_types}")
    print(f"    - Priorities Assigned: {priorities}")

    # Check key algorithms exist
    assert any("RSA" in a for a in algos), "RSA not found"
    assert any("AES" in a for a in algos), "AES not found"
    assert any("MD5" in a for a in algos), "MD5 not found"
    assert any("ECDSA" in a or "SHA" in a for a in algos), "Signatures/Hashes not found"

    # 5. Fetch Single Asset Detail & Raw Evidence
    first_asset = assets[0]
    status, detail = make_req(f"{BASE_URL}/projects/{proj_id}/assets/{first_asset['id']}")
    print(f"[5] Single Asset Detail ({first_asset['algorithm']}): Status {status}")
    print(f"    - Raw Evidence Count: {len(detail.get('raw_evidence', []))}")
    if detail.get('raw_evidence'):
        print(f"    - Sample Code Snippet: {detail['raw_evidence'][0]['matched_text']}")
    assert status == 200 and len(detail.get('raw_evidence', [])) > 0

    # 6. Update Asset Context Parameters (Recalculate Risk & Priority)
    orig_score = first_asset["risk_score"]
    status, updated_asset = make_req(
        f"{BASE_URL}/projects/{proj_id}/assets/{first_asset['id']}",
        method="PATCH",
        data={
            "data_sensitivity": "Critical",
            "business_criticality": "Critical",
            "data_lifetime_years": 25,
            "migration_difficulty": "High"
        }
    )
    print(f"[6] Context Parameter Update: Status {status}")
    print(f"    - Old Risk Score: {orig_score} -> New Risk Score: {updated_asset['risk_score']}")
    print(f"    - New Priority: {updated_asset['priority']}")
    assert status == 200 and updated_asset["risk_score"] >= orig_score

    # 7. Fetch PQC Recommendations
    status, recs = make_req(f"{BASE_URL}/projects/{proj_id}/recommendations")
    print(f"[7] PQC Recommendations: Total {len(recs)} guidance entries generated.")
    assert status == 200 and len(recs) > 0

    rsa_rec = next((r for r in recs if "RSA" in r["current_algorithm"].upper()), None)
    ecdsa_rec = next((r for r in recs if "ECDSA" in r["current_algorithm"].upper()), None)
    aes_rec = next((r for r in recs if "AES" in r["current_algorithm"].upper()), None)
    md5_rec = next((r for r in recs if "MD5" in r["current_algorithm"].upper()), None)

    if rsa_rec:
        print(f"    - RSA Target: {rsa_rec['candidate_algorithm']}")
    if ecdsa_rec:
        print(f"    - ECDSA Target: {ecdsa_rec['candidate_algorithm']}")
    if aes_rec:
        print(f"    - AES Guidance: {aes_rec['candidate_algorithm']} ({aes_rec['reason'][:60]}...)")
    if md5_rec:
        print(f"    - MD5 Target: {md5_rec['candidate_algorithm']}")

    assert aes_rec is not None and "Retain modern symmetric" in aes_rec["reason"]
    assert md5_rec is not None and "SHA-256" in md5_rec["candidate_algorithm"]

    # 8. Test Mosca Roadmap with Custom Migration Time Parameter (Z=5)
    status, roadmap = make_req(
        f"{BASE_URL}/projects/{proj_id}/roadmap",
        method="POST",
        data={
            "planning_threat_horizon_years": 10,
            "default_migration_time_years": 5
        }
    )
    print(f"[8] Mosca Roadmap Evaluation: Status {status}")
    print(f"    - Status: {roadmap['mosca_status']}")
    print(f"    - Required Window: {roadmap['required_security_window_years']} years (Max Lifetime + 5 yrs migration)")
    print(f"    - Horizon (X): {roadmap['planning_threat_horizon_years']} years")
    print(f"    - Phases: {len(roadmap['phases'])} phases")
    assert status == 200 and roadmap["required_security_window_years"] >= 15

    # 9. Dependency Graph
    status, graph = make_req(f"{BASE_URL}/projects/{proj_id}/dependency-graph")
    print(f"[9] Dependency Graph: Status {status}, Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")
    assert status == 200 and len(graph["nodes"]) > 0

    # 10. Export CycloneDX CBOM JSON
    status, cbom = make_req(f"{BASE_URL}/projects/{proj_id}/export/json")
    print(f"[10] CycloneDX CBOM JSON: Status {status}, SpecVersion: {cbom['specVersion']}, Components: {len(cbom['components'])}")
    assert status == 200 and cbom["bomFormat"] == "CycloneDX" and len(cbom["components"]) > 0

    # 11. Export PDF Report
    status, pdf_bytes = make_req(f"{BASE_URL}/projects/{proj_id}/export/pdf")
    print(f"[11] PDF Report Export: Status {status}, Output Size: {len(pdf_bytes)} bytes")
    assert status == 200 and len(pdf_bytes) > 2000

    # 12. Risk Summary
    status, summary = make_req(f"{BASE_URL}/projects/{proj_id}/risk-summary")
    print(f"[12] Risk Summary: Status {status}")
    print(f"     Total Assets: {summary['total_crypto_assets']}")
    print(f"     Quantum Vulnerable: {summary['quantum_vulnerable']}")
    print(f"     Classical Weakness: {summary['classical_weakness']}")
    print(f"     Monitor Items: {summary['monitor_items']}")
    print(f"     Risk Bands: Critical={summary['critical_risk']}, High={summary['high_risk']}, Medium={summary['medium_risk']}, Low={summary['low_risk']}")
    print(f"     Priority Distribution: {summary['priority_distribution']}")
    assert status == 200 and summary["total_crypto_assets"] == len(assets)

    print("\n[SUCCESS] ALL LIVE END-TO-END BACKEND API VALIDATION STEPS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_live_validation()
