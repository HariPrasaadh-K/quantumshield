import os
from pathlib import Path
from typing import List, Tuple, Optional

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "build", "dist", "target", ".idea", ".vscode", ".next"
}

JAVA_EXTENSIONS = {".java"}
PYTHON_EXTENSIONS = {".py", ".pyw"}
JS_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
MANIFEST_FILENAMES = {"pom.xml", "requirements.txt", "package.json", "build.gradle", "build.gradle.kts", "pyproject.toml"}
CONTAINER_FILENAMES = {"dockerfile", "dockerfile.dev", "dockerfile.prod", "containerfile"}

def is_ignored_directory(dir_name: str) -> bool:
    return dir_name in IGNORED_DIRS

def walk_project_files(root_path: str) -> List[str]:
    valid_files = []
    root = Path(root_path)
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Modify dirnames in-place to skip ignored directories
        dirnames[:] = [d for d in dirnames if not is_ignored_directory(d)]
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            valid_files.append(file_path)
            
    return valid_files

def get_relative_path(full_path: str, base_path: str) -> str:
    try:
        return os.path.relpath(full_path, base_path).replace("\\", "/")
    except Exception:
        return str(full_path).replace("\\", "/")

def get_surrounding_context(lines: List[str], line_num: int, context_lines: int = 3) -> str:
    """
    Extract surrounding context around line_num (1-indexed).
    """
    start = max(0, line_num - 1 - context_lines)
    end = min(len(lines), line_num + context_lines)
    
    snippet_lines = []
    for idx in range(start, end):
        prefix = " > " if idx == line_num - 1 else "   "
        snippet_lines.append(f"{prefix}{idx + 1}: {lines[idx].rstrip()}")
        
    return "\n".join(snippet_lines)

def safe_read_lines(file_path: str, max_bytes: int = 10 * 1024 * 1024) -> Tuple[List[str], bool]:
    """
    Reads text lines safely. Returns (lines, truncated_flag).
    """
    if os.path.getsize(file_path) > max_bytes:
        return ([], True)
        
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        return (lines, False)
    except Exception:
        return ([], True)
