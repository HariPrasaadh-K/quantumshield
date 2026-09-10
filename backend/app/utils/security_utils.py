import os
import shutil
import zipfile
import re
from urllib.parse import urlparse
from fastapi import HTTPException, status
from app.core.config import settings

def validate_github_url(url: str) -> str:
    """
    Validates that a URL is a valid public GitHub repository URL to prevent SSRF and invalid requests.
    """
    if not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GitHub URL is required.")
        
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL scheme. Must be http or https.")
        
    domain = parsed.netloc.lower()
    if domain not in ("github.com", "www.github.com"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only GitHub URLs (github.com) are supported.")
        
    path = parsed.path.strip("/")
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid GitHub repository path. Expected owner/repo.")
        
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
        
    # Strictly validate characters
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', owner) or not re.match(r'^[a-zA-Z0-9_\-\.]+$', repo):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid character in GitHub repository URL.")
        
    clean_url = f"https://github.com/{owner}/{repo}.git"
    return clean_url

def safe_extract_zip(zip_path: str, extract_dir: str):
    """
    Safely extracts a ZIP file enforcing Zip-Slip protection and archive limits.
    """
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file missing.")
        
    file_size = os.path.getsize(zip_path)
    if file_size > settings.MAX_ZIP_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"ZIP archive size ({file_size} bytes) exceeds limit of {settings.MAX_ZIP_SIZE_BYTES} bytes.")

    target_dir_abs = os.path.abspath(extract_dir)
    os.makedirs(target_dir_abs, exist_ok=True)

    total_uncompressed_size = 0
    file_count = 0

    with zipfile.ZipFile(zip_path, 'r') as zf:
        infolist = zf.infolist()
        if len(infolist) > settings.MAX_FILES_IN_ARCHIVE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Archive contains too many files ({len(infolist)} > max {settings.MAX_FILES_IN_ARCHIVE}).")

        for member in infolist:
            # Zip-Slip check
            member_path = os.path.abspath(os.path.join(target_dir_abs, member.filename))
            if not member_path.startswith(target_dir_abs + os.sep) and member_path != target_dir_abs:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Zip Slip path traversal attempt detected.")

            if member.file_size > settings.MAX_SINGLE_FILE_SIZE_BYTES:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File {member.filename} exceeds max file size limit.")

            total_uncompressed_size += member.file_size
            if total_uncompressed_size > settings.MAX_UNCOMPRESSED_SIZE_BYTES:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Archive total uncompressed size limit exceeded.")

            file_count += 1

        # Extract safely
        zf.extractall(target_dir_abs)

def cleanup_directory(dir_path: str):
    """
    Safely removes a temporary directory.
    """
    if dir_path and os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
        except Exception:
            pass
