import pytest
from app.engines.purpose_classifier import classify_crypto_purpose
from app.engines.risk_engine import calculate_risk_score, classify_risk_type
from app.engines.priority_engine import calculate_priority
from app.engines.pqc_recommender import recommend_pqc_alternative
from app.engines.mosca_engine import evaluate_mosca_roadmap
from app.services.scan_service import derive_asset_context_inputs

def test_purpose_classifier_specific_cases():
    # 1. RSA in Cipher.getInstance -> Encryption
    p1, c1 = classify_crypto_purpose("RSA/ECB/PKCS1Padding", 'Cipher.getInstance("RSA/ECB/PKCS1Padding")', "Cipher cipher = Cipher.getInstance(...)")
    assert p1 == "Encryption"
    assert c1 >= 0.85

    # 2. KeyPairGenerator -> Key Generation
    p2, c2 = classify_crypto_purpose("RSA", "KeyPairGenerator.getInstance('RSA')", "keyGen.initialize(2048)")
    assert p2 == "Key Generation"

    # 3. Signature -> Digital Signature
    p3, c3 = classify_crypto_purpose("SHA256withECDSA", "Signature.getInstance('SHA256withECDSA')", "signature.initSign(key)")
    assert p3 == "Digital Signature"

    # 4. KeyAgreement / ECDH -> Key Establishment
    p4, c4 = classify_crypto_purpose("ECDH", "KeyAgreement.getInstance('ECDH')", "keyAgree.init(key)")
    assert p4 == "Key Establishment"

    # 5. MessageDigest -> Hashing
    p5, c5 = classify_crypto_purpose("MD5", "MessageDigest.getInstance('MD5')", "md.digest(input)")
    assert p5 == "Hashing"

    # 6. Ambiguous RSA without Cipher/Signature/KeyPairGenerator -> Unknown
    p6, c6 = classify_crypto_purpose("RSA", "String algo = 'RSA';", "generic comment mentioning RSA")
    assert p6 == "Unknown"
    assert c6 == 0.30

def test_risk_score_asset_variability():
    # Verify that different assets receive distinct, asset-specific risk scores (not uniform 71.8)
    s1, c1, l1, d1 = derive_asset_context_inputs("RSA", "Encryption", "com/security/CryptoService.java", "Java Scanner")
    r1 = calculate_risk_score("RSA", s1, c1, l1, d1)
    
    s2, c2, l2, d2 = derive_asset_context_inputs("MD5", "Hashing", "utils/helper.java", "Java Scanner")
    r2 = calculate_risk_score("MD5", s2, c2, l2, d2)

    s3, c3, l3, d3 = derive_asset_context_inputs("OPENSSL", "TLS", "Dockerfile", "Container Scanner")
    r3 = calculate_risk_score("OPENSSL", s3, c3, l3, d3)

    assert r1["total_score"] != r2["total_score"]
    assert r2["total_score"] != r3["total_score"]
    assert r1["total_score"] > 80.0 # Critical RSA Key Encapsulation
    assert r3["total_score"] < 40.0 # Container surface hint

def test_risk_explanation_factor_breakdown():
    res = calculate_risk_score("RSA", "Critical", "Critical", 25, "High")
    assert "Contributing Factor Scores:" in res["explanation"]
    assert "Quantum Vulnerability=95.0" in res["explanation"]
    assert "Data Sensitivity=100.0" in res["explanation"]

def test_purpose_aware_pqc_recommendations():
    # Encryption -> ML-KEM
    rec_enc = recommend_pqc_alternative("RSA", "Encryption")
    assert "ML-KEM" in rec_enc["candidate_algorithm"]

    # Digital Signature -> ML-DSA / SLH-DSA
    rec_sig = recommend_pqc_alternative("ECDSA", "Digital Signature")
    assert "ML-DSA" in rec_sig["candidate_algorithm"] or "SLH-DSA" in rec_sig["candidate_algorithm"]

    # Symmetric AES -> Retain modern symmetric encryption (DO NOT replace with ML-KEM/ML-DSA)
    rec_aes = recommend_pqc_alternative("AES-256-GCM", "Encryption")
    assert "Retain modern symmetric encryption" in rec_aes["reason"]
    assert "ML-KEM" not in rec_aes["candidate_algorithm"]

    # Weak Hashes -> SHA-256
    rec_md5 = recommend_pqc_alternative("MD5", "Hashing")
    assert "SHA-256" in rec_md5["candidate_algorithm"]

    # Ambiguous RSA -> Manual Cryptographic Review Required
    rec_amb = recommend_pqc_alternative("RSA", "Unknown")
    assert "Manual Cryptographic Review Required" in rec_amb["candidate_algorithm"]

def test_mosca_engine():
    m_urgent = evaluate_mosca_roadmap(max_data_lifetime_years=15, estimated_migration_time_years=2, planning_threat_horizon_years=10)
    assert m_urgent["mosca_status"] == "URGENT"

    m_acc = evaluate_mosca_roadmap(max_data_lifetime_years=7, estimated_migration_time_years=2, planning_threat_horizon_years=10)
    assert m_acc["mosca_status"] == "ACCELERATE"

    m_planned = evaluate_mosca_roadmap(max_data_lifetime_years=3, estimated_migration_time_years=2, planning_threat_horizon_years=10)
    assert m_planned["mosca_status"] == "PLANNED"
