from abc import ABC, abstractmethod
from typing import List, Dict, Any
import uuid

class BaseScanner(ABC):
    def __init__(self, name: str, language: str):
        self.name = name
        self.language = language

    @abstractmethod
    def can_scan(self, file_path: str) -> bool:
        """Determines whether this scanner handles the specified file."""
        pass

    @abstractmethod
    def scan_file(self, file_path: str, relative_path: str) -> List[Dict[str, Any]]:
        """
        Scans a single file and returns raw finding dicts.
        Dict format:
        {
            "detector": str,
            "file_path": str,
            "line_number": int,
            "matched_text": str,
            "surrounding_context": str,
            "language": str,
            "algorithm_hint": str,
            "library_hint": str,
            "confidence": float,
            "metadata": dict
        }
        """
        pass
