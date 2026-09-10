"""
NIST Post-Quantum Cryptography Recommendation Engine.
Provides candidate migration targets according to NIST FIPS 203, 204, and 205.
"""
from typing import Dict, Any

PQC_DISCLAIMER = "Candidate migration guidance — validate before production deployment."

def recommend_pqc_alternative(
    algorithm: str,
    purpose: str,
    risk_type: str = "Quantum"
) -> Dict[str, Any]:
    algo_upper = (algorithm or "").upper().strip()
    purpose_clean = (purpose or "Unknown").strip()

    # Default fallback container
    candidate = "Manual Cryptographic Review Required"
    reason = "Unrecognized algorithm or ambiguous usage pattern requiring security audit."
    complexity = "Medium"
    perf = "Evaluate key size, ciphertext expansion, and signature size overheads."
    compat = "Check TLS protocol versions, SDK support, and hardware acceleration availability."
    confidence = 0.50

    # 1. Symmetric Encryption (AES) - DO NOT replace with ML-KEM or ML-DSA
    if any(s in algo_upper for s in ["AES", "CHACHA20"]):
        candidate = "AES-256-GCM / Modern Symmetric Margin"
        reason = (
            "Retain modern symmetric encryption (AES). Symmetric ciphers are not broken by Shor's algorithm. "
            "Do NOT replace symmetric ciphers with Post-Quantum KEM or signature schemes (ML-KEM / ML-DSA). "
            "Enforce 256-bit key length (AES-256) to maintain a 128-bit quantum security margin against Grover's algorithm."
        )
        complexity = "Low"
        perf = "AES-NI hardware acceleration maintains high performance."
        compat = "Fully compatible across all modern platforms."
        confidence = 0.95

    # 2. Asymmetric Key Encapsulation / Key Establishment (KEM)
    elif purpose in ("Key Establishment", "Key Encapsulation") or any(k in algo_upper for k in ["ECDH", "DH"]):
        candidate = "ML-KEM-768 (Module-Lattice-Based Key-Encapsulation Mechanism - NIST FIPS 203)"
        reason = (
            "ML-KEM (formerly Kyber) is the primary NIST-standardized Post-Quantum KEM for general key exchange. "
            "It provides security based on the hardness of solving the Module Learning-With-Errors (MLWE) problem."
        )
        complexity = "Medium"
        perf = "Fast key generation and encapsulation; public key size (~1184 bytes for ML-KEM-768) is larger than RSA/ECC."
        compat = "Requires hybrid KEM support (e.g. X25519 + ML-KEM-768) during transition."
        confidence = 0.95

    # 3. Asymmetric Digital Signatures (ECDSA, DSA, Ed25519)
    elif purpose == "Digital Signature" or any(k in algo_upper for k in ["ECDSA", "DSA", "ED25519"]):
        candidate = "ML-DSA-65 (NIST FIPS 204) / SLH-DSA-128 (NIST FIPS 205)"
        reason = (
            "ML-DSA (formerly Dilithium) is the primary NIST-standardized Post-Quantum signature algorithm. "
            "Stateless hash-based SLH-DSA (formerly SPHINCS+) is recommended as a conservative alternative where lattice assumptions are concerned."
        )
        complexity = "High"
        perf = "Signatures are larger (~2420 bytes for ML-DSA-44) than RSA/ECDSA; SLH-DSA has higher signature size and verification time."
        compat = "May impact network payload size, TLS handshake packet size, and certificate chain encoding."
        confidence = 0.95

    # 4. Asymmetric Encryption (RSA Cipher / PQC KEM Target)
    elif purpose == "Encryption" and "RSA" in algo_upper:
        candidate = "ML-KEM-768 (NIST FIPS 203)"
        reason = "Migrate RSA public-key encryption to ML-KEM for post-quantum key encapsulation and hybrid data encryption."
        complexity = "High"
        perf = "Requires updated protocol libraries supporting hybrid or pure post-quantum KEMs."
        compat = "Transition via hybrid ECDH + ML-KEM recommended."
        confidence = 0.90

    # 5. Key Generation (KeyPairGenerator / KeyGenerator)
    elif purpose == "Key Generation" and any(q in algo_upper for q in ["RSA", "ECDSA", "ECDH", "DSA"]):
        candidate = "ML-KEM-768 Keypair / ML-DSA-65 Keypair Generator"
        reason = "Migrate asymmetric keypair generation to NIST-approved ML-KEM (Key Exchange) or ML-DSA (Digital Signature) keypair generators."
        complexity = "High"
        perf = "Fast PQC key generation routines available in OpenSSL 3.2+ and Bouncy Castle 1.77+."
        compat = "Requires updating crypto provider registrations."
        confidence = 0.85

    # 6. RSA with Ambiguous Purpose
    elif "RSA" in algo_upper:
        if purpose in ("Key Establishment", "Key Encapsulation"):
            candidate = "ML-KEM-768 (NIST FIPS 203)"
            reason = "RSA key establishment should be migrated to ML-KEM for quantum-resistant key exchange."
            complexity = "High"
            perf = "Fast KEM routines; larger public keys."
            compat = "Requires hybrid KEM provider."
            confidence = 0.90
        elif purpose == "Digital Signature":
            candidate = "ML-DSA-65 (NIST FIPS 204) / SLH-DSA-128 (NIST FIPS 205)"
            reason = "RSA signature scheme should be migrated to ML-DSA or stateless hash-based SLH-DSA."
            complexity = "High"
            perf = "Signatures are larger than RSA; SLH-DSA provides conservative hash-based security."
            compat = "Requires updating signature verification code."
            confidence = 0.90
        else:
            candidate = "Manual Cryptographic Review Required"
            reason = "RSA purpose is ambiguous in source code context. Inspect whether RSA is used for encryption, signatures, or key exchange before selecting a PQC migration path."
            complexity = "High"
            perf = "Depends on selected target PQC algorithm."
            compat = "Manual code audit required to separate signing from key exchange."
            confidence = 0.40

    # 7. Legacy Weak Hashes (MD5, SHA-1) & Ciphers (DES, 3DES)
    elif any(k in algo_upper for k in ["MD5", "SHA-1", "SHA1", "DES", "3DES", "RC4"]):
        candidate = "SHA-256 / SHA-384 / Modern Hash Standard"
        reason = (
            f"Migrate classical weak algorithm {algorithm} to an approved modern cryptographic standard "
            f"(e.g. SHA-256 or SHA-384 for hashing, AES-256 for symmetric encryption)."
        )
        complexity = "Low"
        perf = "Negligible performance impact; native CPU instructions available."
        compat = "Universally supported across all web/enterprise frameworks."
        confidence = 0.95

    # 8. TLS / Certificates
    elif purpose in ("TLS", "Certificate") or "TLS" in algo_upper or "SSL" in algo_upper:
        candidate = "Hybrid Post-Quantum TLS 1.3 (e.g. X25519 + ML-KEM-768)"
        reason = "Migrate TLS configurations to hybrid post-quantum key exchange mechanisms supported in OpenSSL 3.2+ and modern web browsers."
        complexity = "Medium"
        perf = "Slightly increased ClientHello / ServerHello payload size."
        compat = "Ensure web servers and client SDKs support post-quantum key exchange groups."
        confidence = 0.90

    return {
        "current_algorithm": algorithm,
        "current_purpose": purpose_clean,
        "candidate_algorithm": candidate,
        "reason": reason,
        "migration_complexity": complexity,
        "performance_considerations": perf,
        "compatibility_considerations": compat,
        "confidence": confidence,
        "disclaimer": PQC_DISCLAIMER
    }
