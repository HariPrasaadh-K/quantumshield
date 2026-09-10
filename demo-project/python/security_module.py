import hashlib
import ssl
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import hashes
from Crypto.Cipher import AES, DES

def generate_legacy_rsa_keys():
    # RSA Key Generation (Quantum Vulnerable)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key

def hash_user_password_md5(password: str) -> str:
    # Classical Weak Hash
    return hashlib.md5(password.encode()).hexdigest()

def hash_data_sha256(data: bytes) -> str:
    # Modern Secure Hash
    return hashlib.sha256(data).hexdigest()

def create_legacy_des_cipher(key: bytes):
    # Classical Weak Cipher (DES)
    return DES.new(key, DES.MODE_ECB)

def configure_tls_session():
    # TLS context hint
    ctx = ssl.create_default_context()
    ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    return ctx
