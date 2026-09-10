"""
Context-aware Cryptographic Purpose Classifier Engine.
"""
from typing import Tuple

def classify_crypto_purpose(algorithm: str, matched_text: str, context: str) -> Tuple[str, float]:
    """
    Classifies the cryptographic purpose based on algorithm name and surrounding source code context.
    Returns (purpose_name, confidence).
    """
    algo_upper = (algorithm or "").upper().strip()
    text_lower = f"{matched_text} {context}".lower()

    # 1. High-confidence API method & constructor matches
    if "cipher" in text_lower or "createcipher" in text_lower or "createdecipher" in text_lower:
        return ("Encryption", 0.90)

    if "keypairgenerator" in text_lower or "generatekeypair" in text_lower:
        return ("Key Generation", 0.85)

    if "keyagreement" in text_lower:
        return ("Key Establishment", 0.95)

    if "signature" in text_lower or "createsign" in text_lower or "createverify" in text_lower:
        return ("Digital Signature", 0.95)

    if "messagedigest" in text_lower or "createhash" in text_lower or "createhmac" in text_lower:
        return ("Hashing", 0.90)

    # 2. Algorithm-specific deterministic rules
    if any(k in algo_upper for k in ["ECDH", "DIFFIE", "DH"]):
        return ("Key Establishment", 0.95)

    if any(k in algo_upper for k in ["ECDSA", "DSA", "ED25519", "ED448"]):
        return ("Digital Signature", 0.95)

    if any(k in algo_upper for k in ["AES", "DES", "3DES", "BLOWFISH", "CHACHA20", "RC4"]):
        return ("Encryption", 0.90)

    if "HMAC" in algo_upper or "hmac" in text_lower:
        return ("MAC", 0.90)

    if any(k in algo_upper for k in ["MD5", "SHA-1", "SHA-256", "SHA-384", "SHA-512", "SHA1", "SHA256", "SHA384", "SHA512", "HASHLIB"]):
        if "sign" in text_lower or "signature" in text_lower:
            return ("Digital Signature", 0.70)
        return ("Hashing", 0.90)

    if "TLS" in algo_upper or "SSL" in algo_upper or "https" in text_lower or "ssl" in text_lower:
        return ("TLS", 0.85)

    if "CERT" in algo_upper or "X509" in algo_upper or "x.509" in text_lower:
        return ("Certificate", 0.85)

    # 3. RSA specific context analysis
    if "RSA" in algo_upper:
        sign_score = text_lower.count("sign") + text_lower.count("verify") + text_lower.count("signature")
        cipher_score = text_lower.count("cipher") + text_lower.count("encrypt") + text_lower.count("decrypt")
        keygen_score = text_lower.count("keypair") + text_lower.count("keygenerator") + text_lower.count("generatekey")

        if cipher_score > sign_score and cipher_score > keygen_score:
            return ("Encryption", 0.85)
        elif sign_score > cipher_score and sign_score > keygen_score:
            return ("Digital Signature", 0.85)
        elif keygen_score > 0:
            return ("Key Generation", 0.80)
        elif "exchange" in text_lower or "dh" in text_lower or "agreement" in text_lower:
            return ("Key Establishment", 0.80)
        else:
            # Ambiguous RSA remains Unknown with low confidence (never default blindly to Key Establishment)
            return ("Unknown", 0.30)

    return ("Unknown", 0.30)
