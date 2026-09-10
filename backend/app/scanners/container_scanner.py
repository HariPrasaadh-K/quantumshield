import os
import re
from typing import List, Dict, Any
from app.scanners.base import BaseScanner
from app.utils.file_utils import CONTAINER_FILENAMES, safe_read_lines, get_surrounding_context
from app.utils.crypto_patterns import CONTAINER_PATTERNS

class ContainerScanner(BaseScanner):
    def __init__(self):
        super().__init__(name="Container Surface Scanner", language="Dockerfile")

    def can_scan(self, file_path: str) -> bool:
        filename = os.path.basename(file_path).lower()
        return "dockerfile" in filename or filename in CONTAINER_FILENAMES

    def scan_file(self, file_path: str, relative_path: str) -> List[Dict[str, Any]]:
        findings = []
        lines, truncated = safe_read_lines(file_path)
        if truncated or not lines:
            return findings

        for line_idx, line_content in enumerate(lines):
            line_num = line_idx + 1
            
            for pattern_obj in CONTAINER_PATTERNS:
                regex = pattern_obj["pattern"]
                matches = re.finditer(regex, line_content, re.IGNORECASE)
                
                for match in matches:
                    matched_text = match.group(0)
                    context = get_surrounding_context(lines, line_num)
                    
                    # Treated strictly as a low-confidence surface hint
                    findings.append({
                        "detector": self.name,
                        "file_path": relative_path,
                        "line_number": line_num,
                        "matched_text": line_content.strip(),
                        "surrounding_context": context,
                        "language": "Dockerfile",
                        "algorithm_hint": pattern_obj["algorithm"],
                        "library_hint": pattern_obj["hint"],
                        "confidence": 0.30,
                        "metadata": {
                            "surface_hint": True,
                            "pattern_name": pattern_obj["name"]
                        }
                    })

        return findings
