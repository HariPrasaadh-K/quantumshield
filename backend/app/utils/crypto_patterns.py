"""
Cryptographic patterns for multi-language static scanning.
"""

JAVA_PATTERNS = [
    # Cipher / KeyGenerator / Signature / KeyPairGenerator
    {"name": "Java Cipher getInstance", "pattern": r'Cipher\.getInstance\s*\(\s*["\']([^"\']+)["\']\s*\)', "type": "api"},
    {"name": "Java KeyPairGenerator getInstance", "pattern": r'KeyPairGenerator\.getInstance\s*\(\s*["\']([^"\']+)["\']\s*\)', "type": "api"},
    {"name": "Java KeyGenerator getInstance", "pattern": r'KeyGenerator\.getInstance\s*\(\s*["\']([^"\']+)["\']\s*\)', "type": "api"},
    {"name": "Java MessageDigest getInstance", "pattern": r'MessageDigest\.getInstance\s*\(\s*["\']([^"\']+)["\']\s*\)', "type": "api"},
    {"name": "Java Signature getInstance", "pattern": r'Signature\.getInstance\s*\(\s*["\']([^"\']+)["\']\s*\)', "type": "api"},
    {"name": "Java KeyAgreement getInstance", "pattern": r'KeyAgreement\.getInstance\s*\(\s*["\']([^"\']+)["\']\s*\)', "type": "api"},
    {"name": "Java SecureRandom", "pattern": r'new\s+SecureRandom\s*\(', "type": "api"},
    {"name": "Java BouncyCastle Provider", "pattern": r'BouncyCastleProvider|org\.bouncycastle', "type": "library"},
    {"name": "Java Security / Crypto Imports", "pattern": r'import\s+(?:java\.security|javax\.crypto)\.', "type": "import"},
    
    # Generic algorithm mentions in Java code
    {"name": "RSA Keyword", "pattern": r'\bRSA\b', "type": "keyword", "algorithm": "RSA"},
    {"name": "ECDSA Keyword", "pattern": r'\bECDSA\b', "type": "keyword", "algorithm": "ECDSA"},
    {"name": "ECDH Keyword", "pattern": r'\bECDH\b', "type": "keyword", "algorithm": "ECDH"},
    {"name": "AES Keyword", "pattern": r'\bAES(?:-\d{3})?(?:-[A-Z0-9]+)?\b', "type": "keyword", "algorithm": "AES"},
    {"name": "DES Keyword", "pattern": r'\bDES\b', "type": "keyword", "algorithm": "DES"},
    {"name": "3DES Keyword", "pattern": r'\b(?:3DES|DESede|TripleDES)\b', "type": "keyword", "algorithm": "3DES"},
    {"name": "MD5 Keyword", "pattern": r'\bMD5\b', "type": "keyword", "algorithm": "MD5"},
    {"name": "SHA-1 Keyword", "pattern": r'\bSHA-?1\b', "type": "keyword", "algorithm": "SHA-1"},
    {"name": "SHA-256 Keyword", "pattern": r'\bSHA-?256\b', "type": "keyword", "algorithm": "SHA-256"},
    {"name": "SHA-384 Keyword", "pattern": r'\bSHA-?384\b', "type": "keyword", "algorithm": "SHA-384"},
    {"name": "SHA-512 Keyword", "pattern": r'\bSHA-?512\b', "type": "keyword", "algorithm": "SHA-512"},
    {"name": "DH Keyword", "pattern": r'\bDiffieHellman\b|\bDH\b', "type": "keyword", "algorithm": "DH"},
    {"name": "DSA Keyword", "pattern": r'\bDSA\b', "type": "keyword", "algorithm": "DSA"},
]

PYTHON_PATTERNS = [
    {"name": "Python hashlib", "pattern": r'hashlib\.(md5|sha1|sha256|sha384|sha512|new\s*\(\s*["\']([^"\']+)["\']\s*\))', "type": "api"},
    {"name": "Python Cryptography Primitive", "pattern": r'from\s+cryptography\.hazmat\.primitives(?:\.asymmetric|\.ciphers|\.hashes)?\s+import\s+([A-Za-z0-9_,\s]+)', "type": "import"},
    {"name": "Python PyCryptodome Cipher", "pattern": r'from\s+Crypto\.Cipher\s+import\s+([A-Za-z0-9_,\s]+)', "type": "import"},
    {"name": "Python PyCryptodome PublicKey", "pattern": r'from\s+Crypto\.PublicKey\s+import\s+([A-Za-z0-9_,\s]+)', "type": "import"},
    {"name": "Python SSL context", "pattern": r'ssl\.create_default_context|ssl\.PROTOCOL_', "type": "api"},
    
    # Generic algorithm mentions
    {"name": "RSA Keyword", "pattern": r'\bRSA\b', "type": "keyword", "algorithm": "RSA"},
    {"name": "ECDSA Keyword", "pattern": r'\bECDSA\b', "type": "keyword", "algorithm": "ECDSA"},
    {"name": "ECDH Keyword", "pattern": r'\bECDH\b', "type": "keyword", "algorithm": "ECDH"},
    {"name": "AES Keyword", "pattern": r'\bAES\b', "type": "keyword", "algorithm": "AES"},
    {"name": "DES Keyword", "pattern": r'\bDES\b', "type": "keyword", "algorithm": "DES"},
    {"name": "3DES Keyword", "pattern": r'\b(?:3DES|TripleDES)\b', "type": "keyword", "algorithm": "3DES"},
    {"name": "MD5 Keyword", "pattern": r'\bMD5\b', "type": "keyword", "algorithm": "MD5"},
    {"name": "SHA-1 Keyword", "pattern": r'\bSHA-?1\b', "type": "keyword", "algorithm": "SHA-1"},
    {"name": "SHA-256 Keyword", "pattern": r'\bSHA-?256\b', "type": "keyword", "algorithm": "SHA-256"},
]

JAVASCRIPT_PATTERNS = [
    {"name": "JS crypto createCipheriv", "pattern": r'crypto\.createCipheriv\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS crypto createDecipheriv", "pattern": r'crypto\.createDecipheriv\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS crypto generateKeyPair", "pattern": r'crypto\.generateKeyPair(?:Sync)?\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS crypto createHash", "pattern": r'crypto\.createHash\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS crypto createHmac", "pattern": r'crypto\.createHmac\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS crypto createSign", "pattern": r'crypto\.createSign\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS crypto createVerify", "pattern": r'crypto\.createVerify\s*\(\s*["\']([^"\']+)["\']', "type": "api"},
    {"name": "JS node:crypto import", "pattern": r'require\(["\']node:crypto["\']\)|from\s+["\']node:crypto["\']|require\(["\']crypto["\']\)', "type": "import"},

    # Generic algorithm mentions
    {"name": "RSA Keyword", "pattern": r'\bRSA\b', "type": "keyword", "algorithm": "RSA"},
    {"name": "ECDSA Keyword", "pattern": r'\bECDSA\b', "type": "keyword", "algorithm": "ECDSA"},
    {"name": "ECDH Keyword", "pattern": r'\bECDH\b', "type": "keyword", "algorithm": "ECDH"},
    {"name": "AES Keyword", "pattern": r'\bAES(?:-\d{3})?(?:-[A-Z0-9]+)?\b', "type": "keyword", "algorithm": "AES"},
    {"name": "DES Keyword", "pattern": r'\bDES\b', "type": "keyword", "algorithm": "DES"},
    {"name": "3DES Keyword", "pattern": r'\b3DES\b', "type": "keyword", "algorithm": "3DES"},
    {"name": "MD5 Keyword", "pattern": r'\bMD5\b', "type": "keyword", "algorithm": "MD5"},
    {"name": "SHA-1 Keyword", "pattern": r'\bSHA-?1\b', "type": "keyword", "algorithm": "SHA-1"},
    {"name": "SHA-256 Keyword", "pattern": r'\bSHA-?256\b', "type": "keyword", "algorithm": "SHA-256"},
    {"name": "TLS Keyword", "pattern": r'\bTLS\b', "type": "keyword", "algorithm": "TLS"},
    {"name": "SSL Keyword", "pattern": r'\bSSL\b', "type": "keyword", "algorithm": "SSL"},
]

CONTAINER_PATTERNS = [
    {"name": "Container OpenSSL", "pattern": r'\bopenssl\b', "algorithm": "OpenSSL", "hint": "OpenSSL binary / package in container"},
    {"name": "Container TLS", "pattern": r'\btls\b', "algorithm": "TLS", "hint": "TLS reference in container config"},
    {"name": "Container SSL", "pattern": r'\bssl\b', "algorithm": "SSL", "hint": "SSL reference in container config"},
    {"name": "Container Certbot", "pattern": r'\bcertbot\b', "algorithm": "Certbot", "hint": "Certbot automated certificate tool"},
    {"name": "Container Certificate", "pattern": r'\bcertificate|\.crt|\.pem|\.key\b', "algorithm": "X.509 Certificate", "hint": "Certificate file / reference in container"},
    {"name": "Container X509", "pattern": r'\bx509\b', "algorithm": "X.509", "hint": "X.509 PKI standard reference"},
]

# Known crypto dependency packages per package manager
MANIFEST_DEPENDENCIES = {
    "pom.xml": [
        {"package": "bcprov-jdk", "algorithm": "Bouncy Castle", "hint": "Bouncy Castle Java Provider"},
        {"package": "bcpkix-jdk", "algorithm": "Bouncy Castle PKIX", "hint": "Bouncy Castle PKIX/CMS/PKCS"},
        {"package": "org.bouncycastle", "algorithm": "Bouncy Castle", "hint": "Bouncy Castle Cryptography API"},
        {"package": "commons-codec", "algorithm": "Apache Commons Codec", "hint": "Encoder/Decoder utilities"},
        {"package": "jjwt", "algorithm": "Java JWT", "hint": "JSON Web Token library"},
        {"package": "nimbus-jose-jwt", "algorithm": "Nimbus JOSE JWT", "hint": "JOSE & JWT library"},
    ],
    "requirements.txt": [
        {"package": "cryptography", "algorithm": "PyCA Cryptography", "hint": "Python Cryptography recipes & primitives"},
        {"package": "pycryptodome", "algorithm": "PyCryptodome", "hint": "Low-level cryptographic library"},
        {"package": "pycrypto", "algorithm": "PyCrypto", "hint": "Legacy Python Cryptography Toolkit"},
        {"package": "pynacl", "algorithm": "PyNaCl", "hint": "Python binding to libsodium"},
        {"package": "pyopenssl", "algorithm": "PyOpenSSL", "hint": "Python wrapper around OpenSSL"},
        {"package": "jose", "algorithm": "python-jose", "hint": "JOSE implementation in Python"},
        {"package": "pyjwt", "algorithm": "PyJWT", "hint": "Python JWT library"},
        {"package": "hashlib", "algorithm": "hashlib", "hint": "Standard python hashing"},
    ],
    "package.json": [
        {"package": "crypto-js", "algorithm": "CryptoJS", "hint": "JavaScript library of crypto standards"},
        {"package": "node-forge", "algorithm": "Node Forge", "hint": "Native JS TLS and PKI implementation"},
        {"package": "bcrypt", "algorithm": "bcrypt", "hint": "Password hashing algorithm"},
        {"package": "jsonwebtoken", "algorithm": "jsonwebtoken", "hint": "JWT implementation"},
        {"package": "elliptic", "algorithm": "elliptic", "hint": "Fast Elliptic Curve Cryptography in JS"},
        {"package": "sjcl", "algorithm": "SJCL", "hint": "Stanford Javascript Crypto Library"},
        {"package": "tweetnacl", "algorithm": "TweetNaCl", "hint": "Port of TweetNaCl / secret-key & public-key crypto"},
    ]
}
