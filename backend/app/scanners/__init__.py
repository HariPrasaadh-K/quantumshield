from app.scanners.base import BaseScanner
from app.scanners.java_scanner import JavaScanner
from app.scanners.python_scanner import PythonScanner
from app.scanners.javascript_scanner import JavaScriptScanner
from app.scanners.library_scanner import LibraryScanner
from app.scanners.container_scanner import ContainerScanner

ALL_SCANNERS = [
    JavaScanner(),
    PythonScanner(),
    JavaScriptScanner(),
    LibraryScanner(),
    ContainerScanner(),
]

def get_scanners_for_file(file_path: str):
    return [scanner for scanner in ALL_SCANNERS if scanner.can_scan(file_path)]

__all__ = [
    "BaseScanner",
    "JavaScanner",
    "PythonScanner",
    "JavaScriptScanner",
    "LibraryScanner",
    "ContainerScanner",
    "ALL_SCANNERS",
    "get_scanners_for_file",
]
