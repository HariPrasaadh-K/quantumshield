import os
import tempfile
import pytest
from app.scanners.java_scanner import JavaScanner
from app.scanners.python_scanner import PythonScanner
from app.scanners.javascript_scanner import JavaScriptScanner
from app.scanners.library_scanner import LibraryScanner
from app.scanners.container_scanner import ContainerScanner

def test_java_scanner():
    scanner = JavaScanner()
    code = 'Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");'
    with tempfile.NamedTemporaryFile(suffix=".java", mode="w+", delete=False) as f:
        f.write(code)
        f_path = f.name

    try:
        findings = scanner.scan_file(f_path, "Test.java")
        assert len(findings) > 0
        assert findings[0]["algorithm_hint"] == "RSA/ECB/PKCS1PADDING"
    finally:
        os.remove(f_path)

def test_python_scanner():
    scanner = PythonScanner()
    code = 'import hashlib\nhashlib.md5(b"test")'
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w+", delete=False) as f:
        f.write(code)
        f_path = f.name

    try:
        findings = scanner.scan_file(f_path, "test.py")
        assert len(findings) > 0
        assert any(f["algorithm_hint"] in ("MD5", "HASHLIB") for f in findings)
    finally:
        os.remove(f_path)

def test_javascript_scanner():
    scanner = JavaScriptScanner()
    code = 'const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);'
    with tempfile.NamedTemporaryFile(suffix=".js", mode="w+", delete=False) as f:
        f.write(code)
        f_path = f.name

    try:
        findings = scanner.scan_file(f_path, "auth.js")
        assert len(findings) > 0
        assert "AES-256-GCM" in findings[0]["algorithm_hint"]
    finally:
        os.remove(f_path)

def test_library_scanner():
    scanner = LibraryScanner()
    code = '<dependency><groupId>org.bouncycastle</groupId><artifactId>bcprov-jdk15on</artifactId></dependency>'
    with tempfile.NamedTemporaryFile(prefix="pom", suffix=".xml", mode="w+", delete=False) as f:
        f.write(code)
        f_path = f.name

    try:
        findings = scanner.scan_file(f_path, "pom.xml")
        assert len(findings) > 0
        assert findings[0]["confidence"] == 0.40
    finally:
        os.remove(f_path)

def test_container_scanner():
    scanner = ContainerScanner()
    code = 'RUN apt-get install -y openssl certbot'
    with tempfile.NamedTemporaryFile(prefix="Dockerfile", mode="w+", delete=False) as f:
        f.write(code)
        f_path = f.name

    try:
        findings = scanner.scan_file(f_path, "Dockerfile")
        assert len(findings) > 0
        assert findings[0]["confidence"] == 0.30
    finally:
        os.remove(f_path)
